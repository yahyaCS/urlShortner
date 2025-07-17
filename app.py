from flask import Flask, request, jsonify, redirect
import mysql.connector
import string
import random
from datetime import datetime
from config import MYSQL_CONFIG