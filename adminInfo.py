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

@admin_app.route("/adminJob", methods=['GET'])
def admin_job():
    return render_template('adminJob.html')

@admin_app.route("/adminLogin", methods=['GET','POST'])
def admin_login():
    admin_id = request.form['admin_id']
    admin_password = request.form['admin_password']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM admin_accounts WHERE admin_id = %s AND password = %s"
        cursor.execute(query, (admin_id, admin_password))
        admin = cursor.fetchone()

        if admin:
            return render_template('adminAdmin.html', obj1="first", att1=admin_id)
        else:
            return render_template('login.html')

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-add-student", methods=['GET','POST'])
def add_student():
    stu_id = request.form['stu_id']
    stu_suid = request.form['stu_suid']
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
        query = "INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (stu_id, stu_suid, stu_first_name, stu_last_name, stu_phone, stu_mail, stu_pass, stu_addr, stu_course, stu_intake, stu_skill, stu_cgpa))
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
                                   att7=result[6], att8=result[7], att9=result[8], att10=result[9], att11=result[10], att12=result[11])
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
                                   att7=result[6], att8=result[7], att9=result[8], att10=result[9], att11=result[10], att12=result[11])
        else:
            return render_template('adminStudent.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-update-student", methods=['POST'])
def update_student():
    stu_id = request.form['stu_id']
    stu_suid = request.form['stu_suid']
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
        query = "UPDATE students SET supervisor_id = %s, first_name = %s, last_name = %s, phone_number = %s, email = %s, password = %s, current_address = %s, course_of_study = %s, year_intake = %s, skills_learned = %s, cgpa = %s WHERE student_id = %s"
        cursor.execute(query, (stu_suid, stu_first_name, stu_last_name, stu_phone, stu_mail, stu_pass, stu_addr, stu_course, stu_intake, stu_skill, stu_cgpa, stu_id))
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
        cursor.execute(query, (admin_id, admin_password))
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

@admin_app.route("/admin-add-employer", methods=['GET','POST'])
def add_employer():
    emp_id = request.form['emp_id']
    emp_name = request.form['emp_name']
    emp_num = request.form['emp_num']
    emp_mail = request.form['emp_mail']
    emp_password = request.form['emp_password']
    emp_addr = request.form['emp_addr']

    cursor = db_conn.cursor()

    try:
        query = "INSERT INTO employer VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (emp_id, emp_name, emp_num, emp_mail, emp_password, emp_addr))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminEmployer.html', obj1="addSuccess")

@admin_app.route("/admin-findu-employer", methods=['GET','POST'])
def findu_employer():
    emp_id = request.form['emp_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM employer WHERE employer_id = %s"
        cursor.execute(query, (emp_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminEmployer.html', obj1="uFindSuccess", att1=emp_id, att2=result[1], att3=result[2], att4=result[3], att5=result[4], att6=result[5])
        else:
            return render_template('adminEmployer.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-findd-employer", methods=['GET','POST'])
def findd_employer():
    emp_id = request.form['emp_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM employer WHERE employer_id = %s"
        cursor.execute(query, (emp_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminEmployer.html', obj1="dFindSuccess", att1=emp_id, att2=result[1], att3=result[2], att4=result[3], att5=result[4], att6=result[5])
        else:
            return render_template('adminEmployer.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-update-employer", methods=['POST'])
def update_employer():
    emp_id = request.form['emp_id']
    emp_name = request.form['emp_name']
    emp_num = request.form['emp_num']
    emp_mail = request.form['emp_mail']
    emp_password = request.form['emp_password']
    emp_addr = request.form['emp_addr']

    cursor = db_conn.cursor()

    try:
        query = "UPDATE employer SET company_name = %s, company_number = %s, company_email = %s, employer_password = %s, employer_address = %s WHERE employer_id = %s"
        cursor.execute(query, (emp_name, emp_num, emp_mail, emp_password, emp_addr, emp_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminEmployer.html', obj1="updateSuccess")

@admin_app.route("/admin-delete-employer", methods=['POST'])
def delete_employer():
    emp_id = request.form['emp_id']

    cursor = db_conn.cursor()

    try:
        query = "DELETE FROM employer WHERE employer_id = %s"
        cursor.execute(query, (emp_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminEmployer.html', obj1="deleteSuccess")

@admin_app.route("/admin-add-jobpost", methods=['GET','POST'])
def add_jobpost():
    emp_id = request.form['emp_id']
    emp_name = request.form['emp_name']
    job_id = request.form['job_id']
    job_name = request.form['job_name']
    job_des = request.form['job_des']
    job_sal = request.form['job_sal']

    cursor = db_conn.cursor()

    try:
        query = "INSERT INTO job_post VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (emp_id, emp_name, job_id, job_name, job_des, job_sal))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminJob.html', obj1="addSuccess")

@admin_app.route("/admin-findu-jobpost", methods=['GET','POST'])
def findu_jobpost():
    job_id = request.form['job_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM job_post WHERE job_id = %s"
        cursor.execute(query, (job_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminJob.html', obj1="uFind1Success", att1=result[0], att2=result[1], att3=job_id, att4=result[3], att5=result[4], att6=result[5])
        else:
            return render_template('adminJob.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-findd-jobpost", methods=['GET','POST'])
def findd_jobpost():
    job_id = request.form['job_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM job_post WHERE job_id = %s"
        cursor.execute(query, (job_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminJob.html', obj1="dFind1Success", att1=result[0], att2=result[1], att3=job_id, att4=result[3], att5=result[4], att6=result[5])
        else:
            return render_template('adminJob.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-update-jobpost", methods=['POST'])
def update_jobpost():
    emp_id = request.form['emp_id']
    emp_name = request.form['emp_name']
    job_id = request.form['job_id']
    job_name = request.form['job_name']
    job_des = request.form['job_des']
    job_sal = request.form['job_sal']

    cursor = db_conn.cursor()

    try:
        query = "UPDATE job_post SET employer_id = %s, company_name = %s, job_name = %s, job_description = %s, salary = %s WHERE job_id = %s"
        cursor.execute(query, (emp_id, emp_name, job_name, job_des, job_sal, job_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminJob.html', obj1="updateSuccess")

@admin_app.route("/admin-delete-jobpost", methods=['POST'])
def delete_jobpost():
    job_id = request.form['job_id']

    cursor = db_conn.cursor()

    try:
        query = "DELETE FROM job_post WHERE job_id = %s"
        cursor.execute(query, (job_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminJob.html', obj1="deleteSuccess")

@admin_app.route("/admin-add-jobapplied", methods=['GET','POST'])
def add_jobapplied():
    app_id = request.form['app_id']
    stu_id = request.form['stu_id']
    emp_id = request.form['emp_id']
    job_id = request.form['job_id']


    cursor = db_conn.cursor()

    try:
        query = "INSERT INTO job_applied VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (app_id, stu_id, emp_id, job_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminJob.html', obj1="addSuccess")

@admin_app.route("/admin-findu-jobapplied", methods=['GET','POST'])
def findu_jobapplied():
    app_id = request.form['app_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM job_applied WHERE application_id = %s"
        cursor.execute(query, (app_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminJob.html', obj1="uFind2Success", att1=app_id, att2=result[1], att3=result[2], att4=result[3])
        else:
            return render_template('adminJob.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-findd-jobapplied", methods=['GET','POST'])
def findd_jobapplied():
    app_id = request.form['app_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM job_applied WHERE application_id = %s"
        cursor.execute(query, (app_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminJob.html', obj1="dFind2Success", att1=app_id, att2=result[1], att3=result[2], att4=result[3])
        else:
            return render_template('adminJob.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-update-jobapplied", methods=['POST'])
def update_jobapplied():
    app_id = request.form['app_id']
    stu_id = request.form['stu_id']
    emp_id = request.form['emp_id']
    job_id = request.form['job_id']

    cursor = db_conn.cursor()

    try:
        query = "UPDATE job_applied SET student_id = %s, employer_id = %s, job_id = %s WHERE application_id = %s"
        cursor.execute(query, (stu_id, emp_id, job_id, app_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminJob.html', obj1="updateSuccess")

@admin_app.route("/admin-delete-jobapplied", methods=['POST'])
def delete_jobapplied():
    app_id = request.form['app_id']

    cursor = db_conn.cursor()

    try:
        query = "DELETE FROM job_applied WHERE application_id = %s"
        cursor.execute(query, (app_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminJob.html', obj1="deleteSuccess")

@admin_app.route("/admin-add-tutor", methods=['GET','POST'])
def add_tutor():
    sup_id = request.form['sup_id']
    sup_name = request.form['sup_name']
    sup_password = request.form['sup_password']


    cursor = db_conn.cursor()

    try:
        query = "INSERT INTO supervisor VALUES (%s, %s, %s)"
        cursor.execute(query, (sup_id, sup_name, sup_password))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminTutor.html', obj1="addSuccess")

@admin_app.route("/admin-findu-tutor", methods=['GET','POST'])
def findu_tutor():
    sup_id = request.form['sup_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM supervisor WHERE supervisor_id = %s"
        cursor.execute(query, (sup_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminTutor.html', obj1="uFindSuccess", att1=sup_id, att2=result[1], att3=result[2])
        else:
            return render_template('adminTutor.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-findd-tutor", methods=['GET','POST'])
def findd_tutor():
    sup_id = request.form['sup_id']

    cursor = db_conn.cursor()

    try:
        query = "SELECT * FROM supervisor WHERE supervisor_id = %s"
        cursor.execute(query, (sup_id))
        result = cursor.fetchone()

        if result:
            return render_template('adminTutor.html', obj1="dFindSuccess", att1=sup_id, att2=result[1], att3=result[2])
        else:
            return render_template('adminTutor.html', obj1="findFailed")

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

@admin_app.route("/admin-update-tutor", methods=['POST'])
def update_tutor():
    sup_id = request.form['sup_id']
    sup_name = request.form['sup_name']
    sup_password = request.form['sup_password']

    cursor = db_conn.cursor()

    try:
        query = "UPDATE supervisor SET supervisor_name = %s, supervisor_password = %s WHERE supervisor_id = %s"
        cursor.execute(query, (sup_name, sup_password, sup_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminTutor.html', obj1="updateSuccess")

@admin_app.route("/admin-delete-tutor", methods=['POST'])
def delete_tutor():
    sup_id = request.form['sup_id']

    cursor = db_conn.cursor()

    try:
        query = "DELETE FROM supervisor WHERE supervisor_id = %s"
        cursor.execute(query, (sup_id))
        db_conn.commit()

    except Exception as e:
        db_conn.rollback()
        return str(e)

    finally:
        cursor.close()

    return render_template('adminTutor.html', obj1="deleteSuccess")