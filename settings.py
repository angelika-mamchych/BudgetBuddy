
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='mysql://root:mysql2Lika@localhost/budgetbuddy',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=True,
    SQLALCHEMY_ECHO=True,
))

app.secret_key = b'_5#y2L"Fjhgjguh\xec]/'

db = SQLAlchemy(app)