from flask import Blueprint, render_template, request, redirect, url_for, session
from pymysql import connections
import os
from flask_session import Session
from config import *
import boto3
from botocore.exceptions import NoCredentialsError

student_app = Blueprint('student_app', __name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

@student_app.route("/studentLoginPage", methods=['GET'])
def student_login_page():
    return render_template('studentLogin.html')


@student_app.route("/studentSignUpPop", methods=['GET'])
def student_sign_up_pop():
    return render_template('login.html', obj1="stuSign")


@student_app.route("/studentSignUpPage", methods=['GET'])
def student_signUp_page():
    return render_template('studentSignUp.html')


@student_app.route("/signup", methods=['POST'])
def signUp():
    student_id = request.form['student_id']
    supervisor_id = request.form['supervisor_id']
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
    profile_picture = request.files['profile_picture']

    cursor = db_conn.cursor()

    try:
        # SQL INSERT query
        insert_query = "INSERT INTO students (student_id, supervisor_id, first_name, last_name, phone_number, email, password, current_address, course_of_study, year_intake, skills_learned, cgpa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (student_id, supervisor_id, first_name, last_name, phone_number, email,
                       password, current_address, course_of_study, year_intake, skills_learned, cgpa))
        db_conn.commit()
        stud_name = "" + first_name + " " + last_name

        session['student_id'] = student_id
        profile_picture_in_s3 = "student_id-" + str(student_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            s3.Bucket(custombucket).put_object(Key=profile_picture_in_s3, Body=profile_picture)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                profile_picture_in_s3)
            
        except Exception as e:
            return str(e)

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('studentSignUpOutput.html', student_id=student_id, name=stud_name)

@student_app.route("/signup-output", methods=['GET'])
def signUpOutput():
    return render_template('studentMenu.html')

@student_app.route("/resume-student", methods=['GET'])
def resume_student():
    return render_template('studentResume.html')

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
            session['student_id'] = student_id
            return redirect(url_for('student_app.signUpOutput'))

        else:
            # Authentication failed, you can redirect to an error page or show an error message
            return render_template('login.html')

    except Exception as e:
        # Handle exceptions here, e.g., database connection issues
        return str(e)

    finally:
        cursor.close()

@student_app.route("/view-and-edit/<student_id>", methods=['GET'])
def view_and_edit(student_id):
    # Check if the student is logged in (has an active session)
    if 'student_id' in session and session['student_id'] == student_id:
        cursor = db_conn.cursor()

        try:
            # Query the database to retrieve the student's information based on student_id
            query = "SELECT * FROM students WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            student = cursor.fetchone()

            if student:
                # Pass the student's information to the template
                return render_template('studentViewEdit.html', student=student)

            else:
                # Handle the case where the student is not found
                return render_template('studentNotFound.html')

        except Exception as e:
            # Handle exceptions here, e.g., database connection issues
            return str(e)

        finally:
            cursor.close()
    else:
        # If the student is not logged in, redirect them to the login page
        return redirect(url_for('student_login_page'))


@student_app.route("/view/<student_id>", methods=['GET'])
def view(student_id):
    # Check if the student is logged in (has an active session)
    if 'student_id' in session and session['student_id'] == student_id:
        cursor = db_conn.cursor()

        try:
            # Query the database to retrieve the student's information based on student_id
            query = "SELECT * FROM students WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            student = cursor.fetchone()

            if student:
                # Pass the student's information to the template
                return render_template('studentView.html', student=student)

            else:
                # Handle the case where the student is not found
                return render_template('studentNotFound.html')

        except Exception as e:
            # Handle exceptions here, e.g., database connection issues
            return str(e)

        finally:
            cursor.close()
    else:
        # If the student is not logged in, redirect them to the login page
        return redirect(url_for('student_login_page'))

from flask import render_template, url_for, redirect

from flask import render_template, url_for, redirect

@student_app.route("/view-student", methods=['GET'])
def view_student():
    # Check if the student is logged in (has an active session)
    if 'student_id' in session:
        student_id = session['student_id']
        cursor = db_conn.cursor()

        try:
            # Retrieve the student's information from the database
            select_query = "SELECT * FROM students WHERE student_id = %s"
            cursor.execute(select_query, (student_id,))
            student_data = cursor.fetchone()

            if not student_data:
                # Handle the case where the student doesn't exist
                return render_template('student_not_found.html')

            # Convert the result into a dictionary for easier data access
            student = {
                "student_id": student_data[0],
                "supervisor_id": student_data[1],
                "first_name": student_data[2],
                "last_name": student_data[3],
                "phone_number": student_data[4],
                "email": student_data[5],
                "password": student_data[6],
                "current_address": student_data[7],
                "course_of_study": student_data[8],
                "year_intake": student_data[9],
                "skills_learned": student_data[10],
                "cgpa": student_data[11]
            }

            # Render a template to display the student's information
            return render_template('studentView.html', student=student)
        except Exception as e:
            # Handle any database errors
            return str(e)
        finally:
            cursor.close()
    else:
        # If the student is not logged in, redirect them to the login page
        return redirect(url_for('student_app.student_login_page'))


        
from flask import session, request, redirect, url_for

from flask import render_template  # Import render_template

@student_app.route("/update-student", methods=['POST'])
def update_student():
    # Check if the student is logged in (has an active session)
    if 'student_id' in session:
        updated_info = {
            "student_id": request.form['student_id'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "phone_number": request.form['phone_number'],
            "email": request.form['email'],
            "password": request.form['password'],
            "current_address": request.form['current_address'],
            "course_of_study": request.form['course_of_study'],
            "year_intake": request.form['year_intake'],
            "skills_learned": request.form['skills_learned'],
            "cgpa": request.form['cgpa'],
        }

        # Verify that the student_id in the session matches the one in the form
        if session['student_id'] == updated_info['student_id']:
            cursor = db_conn.cursor()

            try:
                # SQL UPDATE query to update student information
                update_query = """
                    UPDATE students 
                    SET first_name = %s, last_name = %s, phone_number = %s, 
                        email = %s, password = %s, current_address = %s, 
                        course_of_study = %s, year_intake = %s, 
                        skills_learned = %s, cgpa = %s
                    WHERE student_id = %s
                """
                cursor.execute(update_query, (
                    updated_info["first_name"], updated_info["last_name"], updated_info["phone_number"],
                    updated_info["email"], updated_info["password"], updated_info["current_address"],
                    updated_info["course_of_study"], updated_info["year_intake"],
                    updated_info["skills_learned"], updated_info["cgpa"], updated_info["student_id"]
                ))
                db_conn.commit()

                # Check if a new profile picture was uploaded
                if 'profile_picture' in request.files:
                    profile_picture = request.files['profile_picture']
                    # Use the same naming convention for the profile picture in S3
                    profile_picture_in_s3 = "student_id-" + str(updated_info["student_id"]) + "_image_file"
                    s3 = boto3.resource('s3')

                    try:
                        s3.Bucket(custombucket).put_object(Key=profile_picture_in_s3, Body=profile_picture)
                        bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                        s3_location = (bucket_location['LocationConstraint'])

                        if s3_location is None:
                            s3_location = ''
                        else:
                            s3_location = '-' + s3_location

                        object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                            s3_location,
                            custombucket,
                            profile_picture_in_s3)
                        
                    except Exception as e:
                        return str(e)

                # Redirect the student to the view and edit page or another appropriate page
                return redirect(url_for('student_app.signUpOutput', student_id=updated_info['student_id']))
            except Exception as e:
                db_conn.rollback()
                return str(e)
            finally:
                cursor.close()
        else:
            # If the student_id in the session doesn't match the one in the form, handle accordingly
            return redirect(url_for('student_app.student_login_page'))
    else:
        # If the student is not logged in, redirect them to the login page
        return redirect(url_for('student_app.student_login_page'))
    
@student_app.route("/upload-resume", methods=['POST'])
def upload_resume():
    # Check if the student is logged in (has an active session)
    if 'student_id' in session:
        try:
            # Get the uploaded resume file
            resume = request.files['resume']

            if resume:
                # Generate a unique key for the resume file in S3
                student_id = session['student_id']
                student_resume = f"student_id-{student_id}_resume.{resume.filename.split('.')[-1]}"
                s3 = boto3.resource('s3')

                try:
                        s3.Bucket(custombucket).put_object(Key=student_resume, Body=resume)
                        bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                        s3_location = (bucket_location['LocationConstraint'])

                        if s3_location is None:
                            s3_location = ''
                        else:
                            s3_location = '-' + s3_location

                        object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                            s3_location,
                            custombucket,
                            student_resume)
                        
                except Exception as e:
                    return str(e)

                # Redirect to a success page or any other appropriate action
                return render_template('studentMenu.html')
            
        except Exception as e:
            return str(e)

    else:
        # If the student is not logged in, redirect them to the login page
        return redirect(url_for('student_login_page'))


@student_app.route("/student_view_jobs")
def student_view_jobs():
    # Check if the student is logged in (has an active session)
    if 'student_id' in session:
        cursor = db_conn.cursor()
        try:
            # Query the database to retrieve all job posts
            query = "SELECT * FROM job_post"
            cursor.execute(query)
            job_posts = cursor.fetchall()

            if not job_posts:
                return render_template('noJobsFound.html')

            jobs = []
            for row in job_posts:
                job = {
                    "company_name" : row [1],
                    "job_name": row[3],
                    "job_description": row[4],
                    "job_salary": row[5],
                }
                jobs.append(job)

            return render_template('studentViewJob.html', jobs=jobs)

        except Exception as e:
            # Handle exceptions here, e.g., database connection issues
            return str(e)
        finally:
            cursor.close()
    else:
        # If the student is not logged in, redirect them to the login page
        return redirect(url_for('student_login_page'))


if __name__ == '__main__':
    student_app.run(host='0.0.0.0', port=80, debug=True)



