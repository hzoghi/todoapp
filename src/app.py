"""
    Simple flask app to create a server for the todo app and handle the database
"""
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
