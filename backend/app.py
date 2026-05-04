import os
import time
import json
import redis
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # WAJIB: Izin agar Frontend bisa akses Backend

# Koneksi Redis menggunakan URL dari Railway
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def get_db_connection():
    # Menggunakan DATABASE_URL otomatis dari Railway
    db_url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(db_url)

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
    except Exception as e:
        print(f"Database Init Error: {e}")

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        cached = redis_client.get('stats')
        if cached:
            return jsonify({'data': json.loads(cached), 'source': 'cache'}), 200

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM todos')
        total = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM todos WHERE completed = TRUE')
        completed = cur.fetchone()[0]
        cur.close()
        conn.close()

        stats = {'total': total, 'completed': completed, 'pending': total - completed}
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
            redis_client.delete('stats') # Hapus cache statistik
            cur.close()
            conn.close()
            return jsonify({'id': new_id, 'task': data['task'], 'completed': False}), 201
        
        cur.execute('SELECT id, task, completed FROM todos ORDER BY id DESC')
        todos = [{'id': row[0], 'task': row[1], 'completed': row[2]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(todos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    time.sleep(3) # Beri napas buat DB
    init_db()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)