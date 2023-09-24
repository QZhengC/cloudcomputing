from flask import Blueprint, render_template, request, redirect, url_for, session
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

main_app = Blueprint('main_app', __name__)


@main_app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('login.html')


@main_app.route("/backToMenu", methods=['POST'])
def backhome():
    session.clear()
    return render_template('login.html')
