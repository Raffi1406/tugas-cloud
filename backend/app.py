import os
import time
import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# app.py (Bagian Konfigurasi)
DB_HOST = os.environ.get('MYSQLHOST', 'localhost')
DB_USER = os.environ.get('MYSQLUSER', 'root')
DB_PASSWORD = os.environ.get('MYSQLPASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'railway') # Kita pake DB_NAME yang baru lu bikin tadi
DB_PORT = int(os.environ.get('MYSQLPORT', 3306))
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
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
                total_harga INT NOT NULL,
                status VARCHAR(50) DEFAULT 'Aktif'
            );
        ''')
        
        cur.execute('SELECT COUNT(*) FROM rentals')
        if cur.fetchone()[0] == 0:
            dummy_data = [
                ('Budi', 1, 3, 15000, 'Aktif'),
                ('Andi', 4, 2, 10000, 'Aktif'),
                ('Citra', 2, 5, 25000, 'Selesai')
            ]
            cur.executemany('''
                INSERT INTO rentals (nama_penyewa, nomor_ps, durasi, total_harga, status) 
                VALUES (%s, %s, %s, %s, %s)
            ''', dummy_data)
            
        conn.commit()
        cur.close()
        conn.close()
        print("Database berhasil diinisialisasi!")
    except Exception as e:
        print(f"Error initializing DB: {e}")

@app.route('/rentals', methods=['GET', 'POST'])
def handle_rentals():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            durasi = int(data['durasi'])
            total_harga = durasi * 5000
            
            # Kita sebutkan nama kolomnya secara eksplisit biar nggak bentrok
            sql = "INSERT INTO rentals (nama_penyewa, nomor_ps, durasi, total_harga, status) VALUES (%s, %s, %s, %s, %s)"
            val = (data['nama'], data['ps'], durasi, total_harga, 'Aktif')
            
            cur.execute(sql, val)
            new_id = cur.lastrowid
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'id': new_id, 'nama': data['nama'], 'ps': data['ps'], 'durasi': durasi, 'total_harga': total_harga}), 201
        
        cur.execute('SELECT id, nama_penyewa, nomor_ps, durasi, total_harga, status FROM rentals ORDER BY id DESC')
        rentals = [{'id': r[0], 'nama': r[1], 'ps': r[2], 'durasi': r[3], 'total_harga': r[4], 'status': r[5]} for r in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(rentals), 200
    except Exception as e:
        # Biar ketauan di Log Railway lu errornya apa
        print(f"ERROR BANGET: {str(e)}") 
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*), COALESCE(SUM(total_harga), 0) FROM rentals')
        row = cur.fetchone()
        total_rental = row[0]
        total_pendapatan = row[1]
        cur.close()
        conn.close()

        stats = {'total_rental': total_rental, 'total_pendapatan': int(total_pendapatan)}
        return jsonify({'data': stats, 'source': 'database'}), 200
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'data': {'total_rental': 0, 'total_pendapatan': 0}}), 200

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)