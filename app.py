from flask import Flask
from studentInfo import student_app
from portfolio import portfolio_app
from adminInfo import admin_app
from tutorInfo import tutor_app
from main import main_app
from employerInfo import employer_app
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)  # Initialize the Session extension


# Register student and admin blueprints
app.register_blueprint(main_app)
app.register_blueprint(portfolio_app)
app.register_blueprint(student_app)
app.register_blueprint(admin_app)
app.register_blueprint(employer_app)
app.register_blueprint(tutor_app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
