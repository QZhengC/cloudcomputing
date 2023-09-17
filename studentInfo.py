from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os

app = Flask(__name__)

db_conn = pymysql.connect(
    host='customhost',
    port=3306,
    user='customuser',
    password='custompass',
    database='customdb'
)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('studentSignUp.html')

@app.route("/signup", methods=['POST'])
def signUp():
    student_id = request.form['student_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']
    email = request.form['email']
    password = request.form['password']

    cursor = db_conn.cursor()

    try:
        # SQL INSERT query
        insert_query = "INSERT INTO students (student_id, first_name, last_name, phone_number, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (student_id, first_name, last_name, phone_number, email, password))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    # Redirect to the additional information page
    return redirect(url_for('additionalInfo', student_id=student_id, name=f'{first_name} {last_name}'))

@app.route("/additional-info", methods=['POST'])
def additionalInfo():
    # Handle the additional information form and insert it into the database
    student_id = request.form['student_id']
    current_address = request.form['current_address']
    course_of_study = request.form['course_of_study']
    year_intake = request.form['year_intake']
    skills_learned = request.form['skills_learned']
    cgpa = request.form['cgpa']

    cursor = db_conn.cursor()

    try:
        # SQL INSERT query for additional information
        insert_query = "INSERT INTO student_additional_info (student_id, current_address, course_of_study, year_intake, skills_learned, cgpa) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (student_id, current_address, course_of_study, year_intake, skills_learned, cgpa))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    # Redirect to the sign-up output page
    return redirect(url_for('signUpOutput', name=request.form['name']))

@app.route("/signup-output", methods=['GET'])
def signUpOutput():
    # Retrieve the name from the URL parameter
    name = request.args.get('name')

    return redirect(url_for('studentMenu.html'))

# Assuming you have a /student-login route defined in your Flask app

@app.route("/student-login", methods=['POST'])
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
    app.run(host='0.0.0.0', port=80, debug=True)
