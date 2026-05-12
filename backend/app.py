from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)

# =========================
# DATABASE CONFIG RAILWAY
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
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )

        print("DATABASE CONNECTED")
        return conn

    except Exception as e:
        print("DATABASE ERROR:", str(e))
        raise e


# =========================
# HOME ROUTE
# =========================

@app.route('/')
def home():
    return jsonify({
        "message": "Backend Flask Railway Running"
    })


# =========================
# GET ALL RENTALS
# =========================

@app.route('/rentals', methods=['GET'])
def get_rentals():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM rentals"
        cursor.execute(query)

        rentals = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(rentals)

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

        print("DATA RECEIVED:", data)

        customer_name = data['customer_name']
        car_model = data['car_model']
        rental_days = data['rental_days']

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO rentals
        (customer_name, car_model, rental_days)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (
            customer_name,
            car_model,
            rental_days
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "Rental berhasil ditambahkan"
        }), 201

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
# RUN APP
# =========================

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port
    )