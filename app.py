from flask import Flask, render_template, request, redirect, url_for
from studentInfo import student_app
from adminInfo import admin_app

app = Flask(__name__)

# Register student and admin blueprints
app.register_blueprint(student_app)
app.register_blueprint(admin_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
