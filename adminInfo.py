from flask import Blueprint,Flask, render_template, request, redirect, url_for
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

admin_app = Blueprint('admin_app', __name__)

@admin_app.route("/admin-login", methods=['POST'])
def admin_login():
    admin_id = request.form['admin_id']
    password = request.form['password']

    cursor = db_conn.cursor()

    try:
        # Query the admin_accounts table to check if the admin account exists
        query = "SELECT * FROM admin_accounts WHERE admin_id = %s AND password = %s"
        cursor.execute(query, (admin_id, password))
        admin = cursor.fetchone()

        if admin:
            # Admin is authenticated, you can set up a session or JWT token here
            # Redirect to the admin dashboard or homepage
            return redirect(url_for('adminMenu.html'))

        else:
            # Authentication failed, you can redirect to an error page or show an error message
            return render_template('adminLogin.html')

    except Exception as e:
        # Handle exceptions here, e.g., database connection issues
        return str(e)

    finally:
        cursor.close()
