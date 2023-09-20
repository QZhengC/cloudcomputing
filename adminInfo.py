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

@admin_app.route("/adminAdmin", methods=['GET'])
def admin_admin():
    return render_template('adminAdmin.html')

@admin_app.route("/adminStudent", methods=['GET'])
def admin_student():
    return render_template('adminStudent.html')

@admin_app.route("/adminEmployer", methods=['GET'])
def admin_employer():
    return render_template('adminEmployer.html')

@admin_app.route("/adminTutor", methods=['GET'])
def admin_tutor():
    return render_template('adminTutor.html')

@admin_app.route("/admin-login", methods=['GET','POST'])
def admin_login():
    admin_id = request.form['admin_id']
    admin_password = request.form['admin_password']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM admin_accounts WHERE admin_id = %s AND password = %s"
        cursor.execute(query, (admin_id, admin_password))
        admin = cursor.fetchone()

        if admin:
            return render_template('adminAdmin.html')
        else:
            return render_template('login.html')

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-add-student", methods=['GET','POST'])
def add_student():
    stu_id = request.form['stu_id']
    stu_first_name = request.form['stu_first_name']
    stu_last_name = request.form['stu_last_name']
    stu_phone = request.form['stu_phone']
    stu_mail = request.form['stu_mail']
    stu_pass = request.form['stu_pass']
    stu_addr = request.form['stu_addr']
    stu_course = request.form['stu_course']
    stu_intake = request.form['stu_intake']
    stu_skill = request.form['stu_skill']
    stu_cgpa = request.form['stu_cgpa']

    cursor = db_conn.cursor()

    try:
        query = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (stu_id, stu_first_name, stu_last_name, stu_phone, stu_mail, stu_pass, stu_addr, stu_course, stu_intake, stu_skill, stu_cgpa))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminStudent.html', obj1="addSuccess")

@admin_app.route("/admin-findu-student", methods=['GET','POST'])
def findu_student():
    stu_id = request.form['stu_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM students WHERE student_id = %s"
        cursor.execute(query, (stu_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminStudent.html', obj1="uFindSuccess", att1=stu_id, 
                                   att2=result[1], att3=result[2], att4=result[3], att5=result[4], att6=result[5], 
                                   att7=result[6], att8=result[7], att9=result[8], att10=result[9], att11=result[10], )
        else:
            return render_template('adminStudent.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-findd-student", methods=['GET','POST'])
def findd_student():
    stu_id = request.form['stu_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM students WHERE student_id = %s"
        cursor.execute(query, (stu_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminStudent.html', obj1="dFindSuccess", att1=stu_id, 
                                   att2=result[1], att3=result[2], att4=result[3], att5=result[4], att6=result[5], 
                                   att7=result[6], att8=result[7], att9=result[8], att10=result[9], att11=result[10], )
        else:
            return render_template('adminStudent.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-update-student", methods=['POST'])
def update_student():
    stu_id = request.form['stu_id']
    stu_first_name = request.form['stu_first_name']
    stu_last_name = request.form['stu_last_name']
    stu_phone = request.form['stu_phone']
    stu_mail = request.form['stu_mail']
    stu_pass = request.form['stu_pass']
    stu_addr = request.form['stu_addr']
    stu_course = request.form['stu_course']
    stu_intake = request.form['stu_intake']
    stu_skill = request.form['stu_skill']
    stu_cgpa = request.form['stu_cgpa']

    cursor = db_conn.cursor()

    try:
        query = "UPDATE students SET first_name = %s, last_name = %s, phone_number = %s, email = %s, password = %s, current_address = %s, course_of_study = %s, year_intake = %s, skills_learned = %s, cgpa = %s WHERE student_id = %s"
        cursor.execute(query, (stu_first_name, stu_last_name, stu_phone, stu_mail, stu_pass, stu_addr, stu_course, stu_intake, stu_skill, stu_cgpa, stu_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminStudent.html', obj1="updateSuccess")

@admin_app.route("/admin-delete-student", methods=['POST'])
def delete_student():
    stu_id = request.form['stu_id']

    cursor = db_conn.cursor()

    try:
        query = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(query, (stu_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminStudent.html', obj1="deleteSuccess")

@admin_app.route("/admin-add-admin", methods=['GET','POST'])
def add_admin():
    admin_id = request.form['admin_id']
    admin_password = request.form['admin_password']

    cursor = db_conn.cursor()

    try:
        query = "INSERT INTO admin_accounts VALUES (%s, %s)"
        cursor.execute(query, (admin_id, admin_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminAdmin.html', obj1="addSuccess")

@admin_app.route("/admin-findu-admin", methods=['GET','POST'])
def findu_admin():
    admin_id = request.form['admin_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM admin_accounts WHERE admin_id = %s"
        cursor.execute(query, (admin_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminAdmin.html', obj1="uFindSuccess", att1=admin_id, att2=result[1])
        else:
            return render_template('adminAdmin.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-findd-admin", methods=['GET','POST'])
def findd_admin():
    admin_id = request.form['admin_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM admin_accounts WHERE admin_id = %s"
        cursor.execute(query, (admin_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminAdmin.html', obj1="dFindSuccess", att1=admin_id, att2=result[1])
        else:
            return render_template('adminAdmin.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-update-admin", methods=['POST'])
def update_admin():
    admin_id = request.form['admin_id']
    admin_password = request.form['admin_password']

    cursor = db_conn.cursor()

    try:
        query = "UPDATE admin_accounts SET password = %s WHERE admin_id = %s"
        cursor.execute(query, (admin_password, admin_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminAdmin.html', obj1="updateSuccess")

@admin_app.route("/admin-delete-admin", methods=['POST'])
def delete_admin():
    admin_id = request.form['admin_id']

    cursor = db_conn.cursor()

    try:
        query = "DELETE FROM admin_accounts WHERE admin_id = %s"
        cursor.execute(query, (admin_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminAdmin.html', obj1="deleteSuccess")