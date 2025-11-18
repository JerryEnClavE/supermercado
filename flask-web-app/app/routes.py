from flask import render_template, redirect, url_for
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/redirect-example')
def redirect_example():
    return redirect(url_for('index'))