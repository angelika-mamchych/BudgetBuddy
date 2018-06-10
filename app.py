# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
from forms import FlowForm
from helpers import dict2obj

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


@app.route("/new_flow")
def flow_form():
    return render_template("flow_form.html")


@app.route("/flow_create", methods=['POST'])
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
    return redirect(url_for('flow_item', flow_id=cur.lastrowid))


@app.route("/flows/<int:flow_id>", methods=['GET'])
def flow_item(flow_id):
    # get from DB by flow_id
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM results where id={}'.format(flow_id))
    flow = cur.fetchone()
    return render_template("flow_item.html", flow=flow)


@app.route("/flows/<int:flow_id>", methods=['POST'])
def flow_item_result(flow_id):
    # get from DB by flow_id
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM results where id={}'.format(flow_id))
    flow = cur.fetchone()
    total_amount = float(request.form['totalamount'].strip())

    if flow['steptype1'].lower() == 'percent':
        step1_fee = total_amount * flow['amount1'] / 100
        total_amount -= step1_fee
    else:
        step1_fee = flow['amount1']
        total_amount -= flow['amount1']

    if flow['steptype2'] == 'percent':
        step2_fee = total_amount * flow['amount2'] / 100
        total_amount -= step2_fee
    else:
        step2_fee = flow['amount2']
        total_amount -= flow['amount2']

    if flow['steptype3'] == 'percent':
        step3_fee = total_amount * flow['amount3'] / 100
        total_amount -= step3_fee
    else:
        step3_fee = flow['amount3']
        total_amount -= flow['amount3']

    return render_template(
        "flow_item.html",
        flow=flow,
        step1_fee=round(step1_fee, 2),
        step2_fee=round(step2_fee, 2),
        step3_fee=round(step3_fee, 2),
        total_left=round(total_amount, 2)
    )


@app.route("/flows")
def show_flows():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM results')
    flows = cur.fetchall()
    return render_template("show_flows.html", flows=flows)


@app.route("/flows_compare", methods=['GET'])
def flows_compare():
    ids = request.args.getlist('ids')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM results where id IN ({})'.format(", ".join(ids)))
    flows = cur.fetchall()
    return render_template("flows_compare.html", flows=flows)


@app.route("/flows_compare", methods=['POST'])
def flow_compare_result():
    ids = request.args.getlist('ids')
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM results where id IN ({})'.format(", ".join(ids)))
    flows = cur.fetchall()
    total_amount = float(request.form['totalamount'].strip())
    total_lefts = []
    step_one_fees = []
    step_two_fees = []
    step_three_fees = []
    for flow in flows:
        fee = 0
        if flow['steptype1'].lower() == 'percent':
            step1_fee = total_amount * flow['amount1'] / 100
            fee += step1_fee
        else:
            step1_fee = flow['amount1']
            fee += flow['amount1']

        if flow['steptype2'] == 'percent':
            step2_fee = (total_amount - fee) * flow['amount2'] / 100
            fee += step2_fee
        else:
            step2_fee = flow['amount2']
            fee += flow['amount2']

        if flow['steptype3'] == 'percent':
            step3_fee = (total_amount - fee) * flow['amount3'] / 100
            fee += step3_fee
        else:
            step3_fee = flow['amount3']
            fee += flow['amount3']
        total_left = total_amount - fee
        total_lefts.append(round(total_left, 2))
        step_one_fees.append(round(step1_fee, 2))
        step_two_fees.append(round(step2_fee, 2))
        step_three_fees.append(round(step3_fee, 2))
    return render_template(
        "flows_compare.html",
        flows=flows,
        step_one_fees=step_one_fees,
        step_two_fees=step_two_fees,
        step_three_fees=step_three_fees,
        total_lefts=total_lefts
    )


@app.route('/edit_flow/<int:flow_id>', methods=['GET', 'POST'])
def edit_flow(flow_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM results where id={}'.format(flow_id))

    flow_dic = cur.fetchone()

    flow = dict2obj(flow_dic)

    form = FlowForm(request.form, flow)

    if request.method == 'POST' and form.validate():
        flowname = form.flowname.data.strip()
        stepname1 = form.stepname1.data.strip()
        stepname2 = form.stepname2.data.strip()
        stepname3 = form.stepname3.data.strip()
        steptype1 = form.steptype1.data.strip()
        steptype2 = form.steptype2.data.strip()
        steptype3 = form.steptype3.data.strip()
        amount1 = form.amount1.data
        amount2 = form.amount2.data
        amount3 = form.amount3.data

        cur.execute(
            'UPDATE results SET flowname="{}", stepname1="{}", stepname2="{}", stepname3="{}", steptype1="{}", \
            steptype2="{}", steptype3="{}", amount1="{}", amount2="{}", amount3="{}" WHERE id={}'.format(
                flowname, stepname1, stepname2, stepname3, steptype1, steptype2, steptype3, amount1, amount2, amount3,
                flow_id))
        mysql.connection.commit()
        return redirect(url_for("flow_item", flow_id=flow_id))
    else:
        return render_template('edit_flow_form.html', form=form)


@app.route('/delete_flow/<int:flow_id>', methods=['POST'])
def delete_flow(flow_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM results WHERE id={}".format(flow_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('show_flows'))


if __name__ == "__main__":
    app.run()

