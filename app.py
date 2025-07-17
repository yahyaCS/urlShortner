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