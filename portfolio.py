from flask import Blueprint, render_template, request, redirect, url_for, session
from pymysql import connections
import os
from flask_session import Session
from config import *
import boto3
from botocore.exceptions import NoCredentialsError

portfolio_app = Blueprint('portfolio_app', __name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)

@portfolio_app.route("/qz-portfolio", methods=['GET'])
def qz_portfolio():
    return render_template('qzPortfolio.html')

@portfolio_app.route("/wx-portfolio", methods=['GET'])
def wx_portfolio():
    return render_template('wxPortfolio.html')

@portfolio_app.route("/jl-portfolio", methods=['GET'])
def jl_portfolio():
    return render_template('jlPortfolio.html')

@portfolio_app.route("/wh-portfolio", methods=['GET'])
def wh_portfolio():
    return render_template('whPortfolio.html')

@portfolio_app.route("/zh-portfolio", methods=['GET'])
def zh_portfolio():
    return render_template('zhPortfolio.html')