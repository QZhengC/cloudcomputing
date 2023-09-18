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

employer_app = Blueprint('employer_app', __name__)


@employer_app.route("/employerLoginPage", methods=['GET'])
def student_login_page():
    return render_template('employerLogin.html')


@employer_app.route("/employer_signup", methods=['POST'])
def signUp():
    employer_id = request.form['employer_id']
    company_name = request.form['company_name']
    company_number = request.form['company_number']
    company_email = request.form['company_email']
    employer_password = request.form['employer_password']
    employer_address = request.form['employer_address']

    cursor = db_conn.cursor()
    try:
        # SQL INSERT query
        insert_query = "INSERT INTO students (employer_id, company_name, company_number, company_email, employer_password, employer_address) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (employer_id, company_name, company_number,
                       company_email, employer_password, employer_address))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    # Redirect to the output page
    return render_template('employerSignUpOutput.html', employer_id=employer_id, company_name=company_name)


@employer_app.route("/employer-signup-output", methods=['GET'])
def signUpOutput():
    # Retrieve the name from the URL parameter
    company_name = request.args.get('company_name')
    return redirect(url_for('employerPage.html'))


@employer_app.route("/employer-login", methods=['POST'])
def student_login():
    employer_id = request.form['employer_id']
    employer_password = request.form['employer_password']

    cursor = db_conn.cursor()

    try:
        # Query the database to check if the student exists and the password is correct
        query = "SELECT * FROM employer WHERE employer_id = %s AND employer_password = %s"
        cursor.execute(query, (employer_id, employer_password))
        employer = cursor.fetchone()

        if employer:
            # Student is authenticated, you can set up a session or JWT token here
            # Redirect to the student dashboard or homepage
            return redirect(url_for('menu.html'))  # SUBJECT TO BE CHANGES

        else:
            # Authentication failed, you can redirect to an error page or show an error message
            return render_template('employerLogin.html')

    except Exception as e:
        # Handle exceptions here, e.g., database connection issues
        return str(e)

    finally:
        cursor.close()


if __name__ == '__main__':
    employer_app.run(host='0.0.0.0', port=80, debug=True)
