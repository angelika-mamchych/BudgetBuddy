# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config.update(dict(
    MYSQL_USER="root",
    MYSQL_PASSWORD="mysql2Lika",
    MYSQL_DB="budgetbuddy",
    MYSQL_CURSORCLASS="DictCursor",
    DEBUG=True,
))

mysql = MySQL(app)

@app.route("/")
def form():
    return render_template("home.html")


@app.route("/flow")
def flow_form():
    return render_template("flow_form.html")


@app.route("/flow_create", methods=['GET', 'POST'])
def flow_create():
    flowname = request.form['flowname'].strip()
    stepname1 = request.form['stepname1'].strip()
    stepname2 = request.form['stepname2'].strip()
    stepname3 = request.form['stepname3'].strip()
    steptype1 = request.form['steptype1'].strip()
    steptype2 = request.form['steptype2'].strip()
    steptype3 = request.form['steptype3'].strip()
    amount1 = request.form['amount1'].strip()
    amount2 = request.form['amount2'].strip()
    amount3 = request.form['amount3'].strip()

    errors = []
    if not flowname:
        errors.append('Please put flowname')

    amount = request.form["amount1"]
    if not amount:
        errors.append('Please put amount')

    if errors:
        return render_template("flow_form.html", errors=errors)

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO results values(NULL, "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
        flowname, stepname1, stepname2,  stepname3, steptype1, steptype2, steptype3, amount1, amount2, amount3))
    mysql.connection.commit()
    return redirect(url_for('flow_item', flow_id=cur.lastrowid - 1))


@app.route("/flow/<int:flow_id>")
def flow_item(flow_id):
    # get from DB by flow_id
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM results')
    rv = cur.fetchall()
    return render_template("flow_item.html", flow=rv[flow_id])


if __name__ == "__main__":
    app.run()