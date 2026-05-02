from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import redis
import json
import time
import os

app = Flask(__name__)
CORS(app)

redis_client = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379, decode_responses=True)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'todos_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password')
    )
    return conn

def init_db():
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

@app.route('/stats', methods=['GET'])
def get_stats():
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

@app.route('/todos', methods=['GET', 'POST'])
def handle_todos():
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

if __name__ == '__main__':
    time.sleep(5)
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)