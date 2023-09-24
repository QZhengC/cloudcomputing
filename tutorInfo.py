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


@tutor_app.route("/supervisorLoginPage", methods=['GET'])
def tutor_Menu():
    return render_template('tutorMenu.html')


@tutor_app.route("/supervisor-Login", methods=['POST', 'GET'])
def tutor_login():
    if request.method == 'POST':
        tutor_id = request.form['tutor_id']
        tutor_password = request.form['tutor_password']
        cursor = db_conn.cursor()
        try:
            query = "SELECT * FROM tutor WHERE tutor_id = %s AND tutor_password = %s"
            cursor.execute(query, (tutor_id, tutor_password))
            tutor = cursor.fetchone()
            if tutor:
                session['tutor_id'] = tutor_id
                return redirect(url_for(tutor_app.tutor_Menu))
            else:
                return "Login Failed"
        except Exception as e:
            return str(e)
        finally:
            cursor.close()
    return render_template('login.html')


if __name__ == '__main__':
    tutor_app.run(host='0.0.0.0', port=80, debug=True)
