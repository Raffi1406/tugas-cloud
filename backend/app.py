import os
import time
import json
import redis
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Inisialisasi Redis
REDIS_URL = os.environ.get('REDIS_URL')
redis_client = redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None

def get_db_connection():
    # Menggunakan DATABASE_URL otomatis dari Railway
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

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
        print("Database initialized successfully")
    except Exception as e:
        print(f"Init DB Error: {e}")

@app.route('/todos', methods=['GET', 'POST'])
def handle_todos():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'task' not in data:
                return jsonify({"error": "No task provided"}), 400
                
            cur.execute('INSERT INTO todos (task) VALUES (%s) RETURNING id, task, completed', (data['task'],))
            new_row = cur.fetchone()
            conn.commit()
            if redis_client:
                redis_client.delete('stats')
            return jsonify({'id': new_row[0], 'task': new_row[1], 'completed': new_row[2]}), 201

        # Jika GET
        cur.execute('SELECT id, task, completed FROM todos ORDER BY id DESC')
        todos = [{'id': row[0], 'task': row[1], 'completed': row[2]} for row in cur.fetchall()]
        cur.close()
        return jsonify(todos), 200 # Mengembalikan ARRAY []
        
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify([]), 500 # Tetap kirim array kosong agar frontend tidak "Format data salah"
    finally:
        if conn:
            conn.close()

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        if redis_client:
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
        if redis_client:
            redis_client.setex('stats', 30, json.dumps(stats))
        return jsonify({'data': stats, 'source': 'database'}), 200
    except:
        return jsonify({'data': {'total': 0, 'completed': 0, 'pending': 0}}), 200

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)