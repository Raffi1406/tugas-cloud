from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)

# =========================
# DATABASE CONFIG
# =========================

DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
DB_PORT = int(os.getenv("MYSQLPORT", 3306))

# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():

    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

# =========================
# HOME
# =========================

@app.route('/')
def home():

    return jsonify({
        "message": "Backend aktif"
    })

# =========================
# GET RENTALS
# =========================

@app.route('/rentals', methods=['GET'])
def get_rentals():

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM rentals")

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:

        print("GET ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500

# =========================
# ADD RENTAL
# =========================

@app.route('/rentals', methods=['POST'])
def add_rental():

    try:

        data = request.get_json()

        print("DATA:", data)

        nama = data['nama']
        ps = data['ps']
        durasi = data['durasi']

        total_harga = int(durasi) * 5000

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO rentals
        (nama, ps, durasi, total_harga, status)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            nama,
            ps,
            durasi,
            total_harga,
            'Aktif'
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Rental berhasil ditambahkan"
        })

    except Exception as e:

        print("POST ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500

# =========================
# DELETE RENTAL
# =========================

@app.route('/rentals/<int:id>', methods=['DELETE'])
def delete_rental(id):

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM rentals WHERE id=%s"

        cursor.execute(query, (id,))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Rental berhasil dihapus"
        })

    except Exception as e:

        print("DELETE ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500

# =========================
# STATS
# =========================

@app.route('/stats', methods=['GET'])
def stats():

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        SELECT
            COUNT(*) AS total_rental,
            COALESCE(SUM(total_harga), 0) AS total_pendapatan
        FROM rentals
        """

        cursor.execute(query)

        data = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "data": data
        })

    except Exception as e:

        print("STATS ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500

# =========================
# RUN APP
# =========================

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )