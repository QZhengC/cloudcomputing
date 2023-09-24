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

tutor_session = Flask(__name__)
tutor_session.config['SESSION_TYPE'] = 'filesystem'
tutor_session.config['SECRET_KEY'] = 'your_secret_key'
Session(tutor_session)
tutor_app = Blueprint('tutor_app', __name__)


@tutor_app.route("/supervisor-menu-page", methods=['GET'])
def supervisor_menu():
    return redirect(url_for('tutor_app.view_all_students'))


@tutor_app.route("/supervisor-login", methods=['POST', 'GET'])
def supervisor_login():
    if request.method == 'POST':
        supervisor_id = request.form['supervisor_id']
        supervisor_password = request.form['supervisor_password']

        cursor = db_conn.cursor()
        try:
            query = "SELECT * FROM supervisor WHERE supervisor_id = %s AND supervisor_password = %s"
            cursor.execute(query, (supervisor_id, supervisor_password))
            tutor = cursor.fetchone()
            if tutor:
                session['supervisor_id'] = supervisor_id
                return redirect(url_for('tutor_app.supervisor_menu'))

            else:
                return "Login Failed"
        except Exception as e:
            return str(e)
        finally:
            cursor.close()

    else:
        return redirect(url_for('main_app.home'))


@tutor_app.route("/view-all-student", methods=['GET'])
def view_all_students():
    if 'supervisor_id' in session:
        supervisor_id = session['supervisor_id']
        cursor = db_conn.cursor()
        query = "SELECT * FROM students"
        cursor.execute(query)
        student = cursor.fetchall()

        students = []
        for row in student:
            student_dict = {
                "student_id": row[0],
                "supervisor_id": row[1],
                "phone_number": row[4],
                "last_name": row[3],
                "email": row[5]
            }
            students.append(student_dict)
        if students is None:
            students.append("No rows")

        select_student_supervisor = "SELECT * FROM students WHERE supervisor_id = %s"
        cursor.execute(select_student_supervisor, (supervisor_id))
        student_under_supervisor = cursor.fetchall()

        studentSupervisor = []
        for row in student_under_supervisor:
            studentSupervisor = {
                "student_id": row[0],
                "supervisor_id": row[1],
                "phone_number": row[4],
                "last_name": row[3],
                "email": row[5]
            }
        if studentSupervisor is None:
            studentSupervisor.append(
                'No Students are currently under your supervision')

        return render_template("supervisorMenu.html", students=students, studentSupervisor=studentSupervisor)
    else:
        return redirect(url_for('main_app.home'))


@tutor_app.route("/add-student-under-supervisor", methods=['POST'])
def add_student_under_supervisor():
    if 'supervisor_id' in session:
        supervisor_id = session['supervisor_id']
        student_id = request.form['student_id']
        cursor = db_conn.cursor()
        try:
            chk_student = "SELECT supervisor_id FROM students WHERE student_id = %s"
            cursor.execute(chk_student, (student_id))
            check = cursor.fetchone()
            if check == None:
                return "student already have a supervisor"

            else:
                update_query = "UPDATE students SET supervisor_id = %s WHERE student_id =%s"
                cursor.execute(update_query, (supervisor_id, student_id))
                db_conn.commit()
                return redirect(url_for('tutor_app.supervisor_menu'))
        except Exception as e:
            db_conn.rollback()
            return str(e)
        finally:
            cursor.close()
    else:
        return redirect(url_for('main_app.home'))


if __name__ == '__main__':
    tutor_app.run(host='0.0.0.0', port=80, debug=True)
