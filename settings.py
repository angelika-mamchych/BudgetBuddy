
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:////home/lika/budgetbuddy.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=True,
    SQLALCHEMY_ECHO=True,
))

app.secret_key = b'_5#y2L"Fjhgjguh\xec]/'

db = SQLAlchemy(app)
