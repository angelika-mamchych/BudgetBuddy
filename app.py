# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for

from data import get_data

app = Flask(__name__)


@app.route("/")
def form():
    return render_template("home.html")


@app.route("/flow")
def flow_form():
    return render_template("flow_form.html")


@app.route("/flow_create", methods=['GET', 'POST'])
def flow_create():
    flowname = request.form['flowname'].strip()
    errors = []
    if not flowname:
        errors.append('Please put flowname')

    amount = request.form["amount1"]
    if not amount:
        errors.append('Please put amount')

    if errors:
        return render_template("flow_form.html", errors=errors)
    # save to DB
    # validate etc
    return redirect(url_for('flow_item', flow_id=1))


@app.route("/flow/<int:flow_id>")
def flow_item(flow_id):
    # get from DB by flow_id
    return render_template("flow_item.html", flow=get_data()[flow_id])


if __name__ == "__main__":
    app.run(debug=True)