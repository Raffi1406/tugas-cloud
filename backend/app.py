import os
import time
import json
import redis
import pymysql
from urllib.parse import urlparse
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    db_url = os.environ.get('MYSQL_URL')
    url = urlparse(db_url)
    return pymysql.connect(
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],
        port=url.port or 3306
    )

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama_penyewa VARCHAR(255) NOT NULL,
                nomor_ps INT NOT NULL,
                durasi INT NOT NULL,
                status VARCHAR(50) DEFAULT 'Aktif'
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except:
        pass

REDIS_URL = os.environ.get('REDIS_URL')
redis_client = redis.from_url(REDIS_URL, decode_responses=True) if REDIS_URL else None

@app.route('/rentals', methods=['GET', 'POST'])
def handle_rentals():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            cur.execute('INSERT INTO rentals (nama_penyewa, nomor_ps, durasi) VALUES (%s, %s, %s)', 
                       (data['nama'], data['ps'], data['durasi']))
            new_id = cur.lastrowid
            conn.commit()
            if redis_client:
                redis_client.delete('stats_ps')
            cur.close()
            conn.close()
            return jsonify({'id': new_id, 'nama': data['nama'], 'ps': data['ps'], 'durasi': data['durasi']}), 201
        
        cur.execute('SELECT id, nama_penyewa, nomor_ps, durasi, status FROM rentals ORDER BY id DESC')
        rentals = [{'id': r[0], 'nama': r[1], 'ps': r[2], 'durasi': r[3], 'status': r[4]} for r in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(rentals), 200
    except:
        return jsonify([]), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        if redis_client:
            cached = redis_client.get('stats_ps')
            if cached:
                return jsonify({'data': json.loads(cached), 'source': 'cache'}), 200

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM rentals')
        total = cur.fetchone()[0]
        cur.close()
        conn.close()

        stats = {'total_rental': total}
        if redis_client:
            redis_client.setex('stats_ps', 30, json.dumps(stats))
        return jsonify({'data': stats, 'source': 'database'}), 200
    except:
        return jsonify({'data': {'total_rental': 0}}), 200

if __name__ == '__main__':
    time.sleep(3)
    init_db()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)