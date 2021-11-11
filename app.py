from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')