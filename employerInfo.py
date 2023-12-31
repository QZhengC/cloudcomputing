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


@employer_app.route("/employerSignUpPop", methods=['GET'])
def employer_sign_up_pop():
    return render_template('login.html', obj1="empSign")


@employer_app.route("/employerSignUpPage", methods=['GET'])
def employer_sign_up_page():
    return render_template('employerSignUp.html')


@employer_app.route("/employerAddJobPage", methods=['GET'])
def employer_add_job_page():
    return render_template('addJobPost.html')


@employer_app.route("/employer-signup-output", methods=['GET'])
def employerSignUpOutput():
    # Retrieve the name from the URL parameter
    company_name = request.args.get('company_name')
    return render_template('employerMenu.html')


@employer_app.route("/employer-add-job-output", methods=['GET'])
def employerAddJobOutput():
    job_name = request.args.get('job_name')
    return render_template('addJobPostOutput.html')


@employer_app.route("/employer-update-job-output", methods=['GET'])
def employerUpdateJobOutput():
    job_id = request.args.get('job_id')
    return render_template('updateJobOutput.html', job_id=job_id)


@employer_app.route("/employer-menu-page", methods=['GET'])
def employer_Menu():
    return render_template('employerMenu.html')


@employer_app.route("/employer-delete-job-page", methods=['GET'])
def delete_job_page():
    return render_template('deleteJob.html')

# SIGN UP AND LOGIN


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

# ADD JOB REDIRECT PAGE


@employer_app.route("/add-job-post/<employer_id>", methods=['GET'])
def add_job_post(employer_id):
    if 'employer_id' in session and session['employer_id'] == employer_id:
        # Access user information from the session
        employer_id = session['employer_id']
        return render_template("addJobPost.html", employer_id=employer_id)
    else:
        return render_template('employerLogin.html')


# ADD JOB FUNCTION
@employer_app.route("/employer-add-job", methods=["POST"])
def emloyer_add_job():
    if 'employer_id' in session:
        employer_id = session['employer_id']

        job_id = request.form['job_id']
        job_name = request.form['job_name']
        job_description = request.form['job_description']
        salary = request.form['salary']

        cursor = db_conn.cursor()
        try:
            # SQL INSERT query
            select_query = "SELECT company_name FROM employer WHERE employer_id = %s"
            cursor.execute(select_query, (employer_id,))
            company_name = cursor.fetchone()

            insert_query = "INSERT INTO job_post (employer_id, company_name ,job_id, job_name, job_description, salary) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (employer_id, company_name, job_id,
                           job_name, job_description, salary))
            db_conn.commit()
            return redirect(url_for('employer_app.employerAddJobOutput', job_name=job_name))
        except Exception as e:
            db_conn.rollback()
            return str(e)
        finally:
            cursor.close()
    else:
        return redirect(url_for('main_app.home'))


# EDIT JOB -> REDIRECT TO DISPLAY
@employer_app.route("/edit-job-post/<employer_id>", methods=['GET'])
def view_job_post_page(employer_id):
    if 'employer_id' in session and session['employer_id'] == employer_id:
        # Access user information from the session
        employer_id = session['employer_id']
        return render_template("viewJobPost.html", employer_id=employer_id)
    else:
        return render_template('employerLogin.html')


# DISPLAY JOB FUNCTION
@employer_app.route("/view-job-post/<employer_id>", methods=['GET'])
def view_job_post(employer_id):
    # Check if the employer is logged in (has an active session)
    if 'employer_id' in session and session['employer_id'] == employer_id:
        cursor = db_conn.cursor()
        try:
            # Query the database to retrieve job posts associated with the employer
            query = "SELECT * FROM job_post WHERE employer_id = %s"
            cursor.execute(query, (employer_id,))
            job_post = cursor.fetchall()

            jobs = []
            for row in job_post:
                job = {
                    "job_id": row[2],
                    "job_name": row[3],
                    "job_description": row[4],
                    "salary": row[5]
                }
                jobs.append(job)
            if not jobs:
                jobs.append("No Rows Found")

            return render_template('viewJobPost.html', jobs=jobs)

        except Exception as e:
            # Handle exceptions here, e.g., database connection issues
            return str(e)
        finally:
            cursor.close()
    else:
        # If the employer is not logged in, redirect them to the login page
        return redirect(url_for('employer_app.employer_login_page'))


@employer_app.route("/display-update-job", methods=['POST'])
def display_choice_of_update():
    if 'employer_id' in session:
        cursor = db_conn.cursor()
        job_id = request.form['job_id']
        try:
            query = "SELECT * FROM job_post WHERE job_id = %s"
            cursor.execute(query, (job_id,))
            job_data = cursor.fetchone()
            if not job_data:
                return render_template('noJobsFound.html')

            job = {
                "job_id": job_data[2],
                "job_name": job_data[3],
                "job_description": job_data[4],
                "salary": job_data[5]
            }

            return render_template('displayUpdateDetails.html', job=job)

        except Exception as e:
            return str(e)
        finally:
            cursor: cursor.close()


@employer_app.route("/update-job", methods=['POST'])
def update_job():
    if 'employer_id' in session:

        cursor = db_conn.cursor()
        employer_id = session['employer_id']

        updated_info = {
            "job_id": request.form['job_id'],
            "job_name": request.form['job_name'],
            "job_description": request.form['job_description'],
            "salary": request.form['salary'],
        }

        try:
            companyNameQuery = "SELECT company_name FROM employer WHERE employer_id = %s"
            cursor.execute(companyNameQuery, (employer_id,))
            company_name = cursor.fetchone()

            update_query = """
                            UPDATE job_post 
                            SET employer_id = %s, company_name = %s, job_id = %s, 
                                job_name = %s, job_description = %s, salary = %s 
                            WHERE job_id = %s
                        """
            cursor.execute(update_query, (
                employer_id, company_name,
                updated_info["job_id"], updated_info["job_name"],
                updated_info["job_description"], updated_info["salary"],
                updated_info['job_id'],
            ))
            db_conn.commit()

            return redirect(url_for('employer_app.employerUpdateJobOutput', job_id=updated_info['job_id']))

        except Exception as e:
            db_conn.rollback()
            return str(e)
        finally:
            cursor.close()
    else:
        return redirect(url_for('main_app.home'))


@employer_app.route("/delete-job", methods=['POST'])
def delete_job():
    job_id = request.form['job_id']
    if 'employer_id' in session:
        cursor = db_conn.cursor()
        try:
            query = "DELETE FROM job_post where job_id = %s"
            cursor.execute(query, (job_id))
            db_conn.commit()

            return render_template('deleteJobOutput.html', job_id=job_id)

        except Exception as e:
            db_conn.rollback()
            return str(e)
        finally:
            cursor.close()
    else:
        return redirect(url_for('main_app.home'))


if __name__ == '__main__':
    employer_app.run(host='0.0.0.0', port=80, debug=True)
