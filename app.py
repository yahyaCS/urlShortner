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