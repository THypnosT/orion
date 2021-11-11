from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import db, secrets, os

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = './static/images/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/')
def login():
    return render_template('login.html')