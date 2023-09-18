from flask import Blueprint, render_template, request, redirect, url_for
from pymysql import connections
import os
import boto3
from config import *

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)

student_app = Blueprint('student_app', __name__)

@student_app.route("/studentLoginPage", methods=['GET'])
def student_login_page():
    return render_template('studentLogin.html')

@student_app.route("/signup", methods=['POST'])
def signUp():
    student_id = request.form['student_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']
    email = request.form['email']
    password = request.form['password']
    current_address = request.form['current_address']
    course_of_study = request.form['course_of_study']
    year_intake = request.form['year_intake']
    skills_learned = request.form['skills_learned']
    cgpa = request.form['cgpa']

    cursor = db_conn.cursor()

    try:
        # SQL INSERT query
        insert_query = "INSERT INTO students (student_id, first_name, last_name, phone_number, email, password, current_address, course_of_study, year_intake, skills_learned, cgpa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (student_id, first_name, last_name, phone_number, email, password, current_address, course_of_study, year_intake, skills_learned, cgpa))
        db_conn.commit()
        stud_name = "" + first_name + " " + last_name

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    # Redirect to the additional information page
    return render_template('studentSignUpOutput.html', student_id=student_id, name=stud_name)


@student_app.route("/signup-output", methods=['GET'])
def signUpOutput():
    # Retrieve the name from the URL parameter
    name = request.args.get('name')

    return redirect(url_for('studentMenu.html'))

@student_app.route("/student-login", methods=['POST'])
def student_login():
    student_id = request.form['student_id']
    password = request.form['password']

    cursor = db_conn.cursor()

    try:
        # Query the database to check if the student exists and the password is correct
        query = "SELECT * FROM students WHERE student_id = %s AND password = %s"
        cursor.execute(query, (student_id, password))
        student = cursor.fetchone()

        if student:
            # Student is authenticated, you can set up a session or JWT token here
            # Redirect to the student dashboard or homepage
            return redirect(url_for('menu.html'))

        else:
            # Authentication failed, you can redirect to an error page or show an error message
            return render_template('login.html')

    except Exception as e:
        # Handle exceptions here, e.g., database connection issues
        return str(e)

    finally:
        cursor.close()


if __name__ == '__main__':
    student_app.run(host='0.0.0.0', port=80, debug=True)
