from flask import Blueprint, jsonify, request
import mysql.connector
from flask_cors import CORS

# Membuat blueprint untuk API
api_blueprint = Blueprint('api', __name__)
CORS(api_blueprint)

# Koneksi ke database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # Ganti dengan host database Anda
        user="root",            # Ganti dengan username database Anda
        password="",            # Ganti dengan password database Anda
        database="db_iotparkir" # Nama database
    )

# Route untuk API hello (GET)
@api_blueprint.route('/hello', methods=['GET'])
def api_hello():
    return jsonify({"message": "Halo dari Flask API (di file api.py)!"})

# Route untuk registrasi pengguna (POST)
@api_blueprint.route('/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Body JSON tidak boleh kosong"}), 400
        if 'username' not in data or 'password' not in data or 'email' not in data:
            return jsonify({"error": "Field 'username', 'password', dan 'email' harus ada"}), 400

        username = data['username']
        password = data['password']
        email = data['email']

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO users (username, password, email)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (username, password, email))
        conn.commit()

        return jsonify({"message": "Registrasi berhasil!"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": f"Terjadi kesalahan pada database: {err}"}), 500

    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

# Route untuk login pengguna (POST)
@api_blueprint.route('/login', methods=['POST'])
def api_login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Body JSON tidak boleh kosong"}), 400
        if 'username' not in data or 'password' not in data:
            return jsonify({"error": "Field 'username' dan 'password' harus ada"}), 400

        username = data['username']
        password = data['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query untuk memeriksa username dan password
        query = """
        SELECT id, username, email FROM users
        WHERE username = %s AND password = %s
        """
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return jsonify({
                "message": "Login berhasil!",
                "user": {
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email']
                }
            }), 200
        else:
            return jsonify({"error": "Username atau password salah"}), 401

    except mysql.connector.Error as err:
        return jsonify({"error": f"Terjadi kesalahan pada database: {err}"}), 500

    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
