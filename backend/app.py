import os
import time
import json
import redis
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Koneksi Redis: Menggunakan DATABASE_URL dari Railway jika ada
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def get_db_connection():
    # Menggunakan DATABASE_URL untuk PostgreSQL agar otomatis konek di Railway
    # Format biasanya: postgresql://user:password@host:port/database
    db_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(db_url)
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                task VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        cached_stats = redis_client.get('stats')
        if cached_stats:
            return jsonify({'data': json.loads(cached_stats), 'source': 'cache'}), 200

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute('SELECT COUNT(*) FROM todos')
        total = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM todos WHERE completed = TRUE')
        completed = cur.fetchone()[0]
        
        cur.close()
        conn.close()

        stats = {
            'total': total,
            'completed': completed,
            'pending': total - completed
        }

        redis_client.setex('stats', 30, json.dumps(stats))
        return jsonify({'data': stats, 'source': 'database'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos', methods=['GET', 'POST'])
def handle_todos():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            cur.execute('INSERT INTO todos (task) VALUES (%s) RETURNING id', (data['task'],))
            new_id = cur.fetchone()[0]
            conn.commit()
            redis_client.delete('stats')
            cur.close()
            conn.close()
            return jsonify({'id': new_id, 'task': data['task'], 'completed': False}), 201
        
        cur.execute('SELECT id, task, completed FROM todos')
        todos = [{'id': row[0], 'task': row[1], 'completed': row[2]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(todos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Beri waktu database untuk ready
    time.sleep(3)
    init_db()
    # PENTING: Gunakan port dari environment variable Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)