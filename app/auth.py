from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    return redirect(url_for('auth.login'))

@auth.route("/login")
def login():
    return render_template("login.html")