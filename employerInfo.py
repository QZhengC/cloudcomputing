from flask import Blueprint, render_template, request, redirect, url_for, session, request, Flask
from pymysql import connections
import os
import boto3
from config import *
from flask_session import Session

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

employer_session = Flask(__name__)
employer_session.config['SESSION_TYPE'] = 'filesystem'
employer_session.config['SECRET_KEY'] = 'your_secret_key'
Session(employer_session)
employer_app = Blueprint('employer_app', __name__)


@employer_app.route("/employerLoginPage", methods=['GET'])
def employer_login_page():
    return render_template('employerLogin.html')


@employer_app.route("/employerSignUpPage", methods=['GET'])
def employer_sign_up_page():
    return render_template('employerSignUp.html')


@employer_app.route("/employer_signup", methods=['POST'])
def employerSignUp():
    employer_id = request.form['employer_id']
    company_name = request.form['company_name']
    company_number = request.form['company_number']
    company_email = request.form['company_email']
    employer_password = request.form['employer_password']
    employer_address = request.form['employer_address']

    cursor = db_conn.cursor()
    try:
        # SQL INSERT query
        insert_query = "INSERT INTO employer (employer_id, company_name, company_number, company_email, employer_password, employer_address) VALUES (%s, %s, %s, %s, %s, %s)"
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
def employerSignUpOutput():
    # Retrieve the name from the URL parameter
    company_name = request.args.get('company_name')
    return redirect(url_for('employerPage.html'))


@employer_app.route("/employer-add-job-page", methods=['GET'])
def employerAddJobPost():
    return render_template('addJobPost.html')


@employer_app.route("/employer-menu-page", methods=['GET'])
def employer_Menu():
    return render_template('employerMenu.html')


@employer_app.route("/employer-login", methods=['GET', 'POST'])
def employer_login():
    if request.method == 'POST':
        employer_id = request.form['employer_id']
        employer_password = request.form['employer_password']
        cursor = db_conn.cursor()

        try:
            query = "SELECT * FROM employer WHERE employer_id = %s AND employer_password = %s"
            cursor.execute(query, (employer_id, employer_password))
            employer = cursor.fetchone()

            if employer:
                # Authentication successful, set session variables
                session['employer_id'] = employer_id
                # Redirect to the dashboard route
                return redirect(url_for('employer_app.employer_Menu'))
            else:
                return "Login Failed"

        except Exception as e:
            # Handle exceptions here, e.g., database connection issues
            return str(e)

        finally:
            cursor.close()

    return render_template('employerLogin.html')


@employer_app.route("/add-job-post", methods=['POST'])
def add_job_post():
    if 'is_authenticated' in session and session['is_authenticated']:
        # Access user information from the session
        employer_id = session['employer_id']
        company_name = session['company_name']
    else:
        return "unauthorized"

    job_name = request.form('job_name')
    job_description = request.form('job_description')
    salary = request.form('salary')

    cursor = db_conn.cursor()
    try:
        # SQL INSERT query
        insert_query = "INSERT INTO job_post (employer_id, company_name, job_name, job_description, salary) VALUES (%s, %s, %s, %s, %f)"
        cursor.execute(insert_query, (employer_id, company_name, job_name,
                       job_description, salary))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    # Redirect to the output page
    return render_template('employer.html', employer_id=employer_id, company_name=company_name)


if __name__ == '__main__':
    employer_app.run(host='0.0.0.0', port=80, debug=True)
