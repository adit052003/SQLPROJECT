from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .db_manager import fetchone, executeCommit

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
    
    user = fetchone("SELECT * FROM Users WHERE `Email`=%s OR ID=%s", (email,student_id))
    if user: return redirect(url_for('auth.signup'))
    
    result = executeCommit(
        "INSERT INTO Users (`ID`, `FirstName`, `LastName`, `Email`, `Password`) VALUES (%s, %s, %s, %s, %s)", 
        (student_id, first_name, last_name, email, generate_password_hash(password, method='scrypt'))
    )
    print(result)
    
    return redirect(url_for('auth.login'))

@auth.route("/login")
def login():
    return render_template("login.html")