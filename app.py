from flask import Flask, request, jsonify, redirect
import mysql.connector
import string
import random
from datetime import datetime
from config import MYSQL_CONFIG

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(**MYSQL_CONFIG)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def home():
    return "<h2>URL Shortener API is running!</h2><p>Use a tool like Postman to test the endpoints.</p>"


@app.route('/shorten', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify(error="URL is required"), 400

    original_url = data['url']
    short_code = generate_short_code()

    conn = get_db()
    cursor = conn.cursor()

    while True:
        cursor.execute("SELECT id FROM urls WHERE short_code = %s", (short_code,))
        if cursor.fetchone() is None:
            break
        short_code = generate_short_code()

    cursor.execute("""
        INSERT INTO urls (original_url, short_code)
        VALUES (%s, %s)
    """, (original_url, short_code))
    conn.commit()

    new_id = cursor.lastrowid
    cursor.execute("SELECT created_at, updated_at FROM urls WHERE id = %s", (new_id,))
    created_at, updated_at = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({
        "id": new_id,
        "url": original_url,
        "shortCode": short_code,
        "createdAt": created_at.isoformat() + "Z",
        "updatedAt": updated_at.isoformat() + "Z"
    }), 201

@app.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, original_url, created_at, updated_at, access_count
        FROM urls WHERE short_code = %s
    """, (short_code,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return jsonify(error="Short URL not found"), 404

    id, original_url, created_at, updated_at, access_count = row

    cursor.execute("""
        UPDATE urls SET access_count = access_count + 1 WHERE short_code = %s
    """, (short_code,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "id": id,
        "url": original_url,
        "shortCode": short_code,
        "createdAt": created_at.isoformat() + "Z",
        "updatedAt": updated_at.isoformat() + "Z"
    })

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE short_code = %s", (short_code,))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify(error="Short URL not found"), 404

    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_stats(short_code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, original_url, created_at, updated_at, access_count
        FROM urls WHERE short_code = %s
    """, (short_code,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return jsonify(error="Short URL not found"), 404

    id, original_url, created_at, updated_at, access_count = row
    return jsonify({
        "id": id,
        "url": original_url,
        "shortCode": short_code,
        "createdAt": created_at.isoformat() + "Z",
        "updatedAt": updated_at.isoformat() + "Z",
        "accessCount": access_count
    })

if __name__ == '__main__':
    app.run(debug=True)