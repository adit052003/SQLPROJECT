from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .db_manager import fetchone, executeCommit
from .models.user import User

auth = Blueprint("auth", __name__)

@auth.route("/signup")
def signup():
    return render_template("signup.html")

@auth.route("/signup", methods=['POST'])
def signup_post():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    
    user = User.findMatchOR(('Email', 'ID'), (email, student_id))
    if user: 
        if user.email.lower() == email.lower(): flash("Email address already registered")
        if str(user.id) == student_id: flash("Student ID already registered")
        return redirect(url_for('auth.signup'))
    
    result = executeCommit(
        "INSERT INTO Users (`ID`, `FirstName`, `LastName`, `Email`, `Password`) VALUES (%s, %s, %s, %s, %s)", 
        (student_id, first_name, last_name, email, generate_password_hash(password, method='scrypt'))
    )
    print(result)
    
    return redirect(url_for('auth.login'))

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=['POST'])
def login_post(): 
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.findMatchOR(('Email',), (email,)) #fetchone("SELECT `Password` FROM Users WHERE `Email`=%s", (email,))
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    print("Logging in:", login_user(user))
    return redirect(url_for('views.dashboard'))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))