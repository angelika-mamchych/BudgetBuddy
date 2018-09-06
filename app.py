# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, jsonify
from forms import FlowForm
from flask_sqlalchemy import SQLAlchemy
import models as m

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='mysql://root:mysql2Lika@localhost/budgetbuddy',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=True,
))

db = SQLAlchemy(app)


@app.route("/")
def form():
    return render_template("home.html")


@app.route("/new_flow", methods=['GET'])
def flow_form():

    return render_template("flow_form.html", flow=None, buttontext='Create Flow')


@app.route("/new_flow", methods=['POST'])
def flow_create():
    flow_json = request.get_json()
    flow = m.Flow(name=flow_json['name'])
    for step in flow_json['steps']:
        flow.steps.append(m.Step(**step))
        # flow.steps.append(m.Step(name=step['name'], type=step['type'], amount=step['amount']))

    db.session.add(flow)
    db.session.commit()

    return jsonify(flow.as_dict())


@app.route("/flows/<int:flow_id>", methods=['GET'])
def flow_item(flow_id):
    flow = m.Flow.query.filter_by(id=flow_id).first()
    if request.is_json:
        return jsonify(flow.as_dict())
    else:
        return render_template("flow_item.html", flow=flow)


@app.route("/flows/<int:flow_id>", methods=['POST'])
def flow_item_result(flow_id):
    # get from DB by flow_id
    flow = m.Flow.query.filter_by(id=flow_id).first()
    total_amount = float(request.form['totalamount'].strip())
    fees = []
    for step in flow.steps:
        if step.type == 'fixed':
            fee = step.amount
            # all our fee equals step.amount
            # in the end they all will be in
            # the list fee=[] and total_left=total_amount-fee[]
            fees.append(fee)
        else:
            # step.type == 'percent'
            fee = step.amount / 100 * total_amount
            fees.append(fee)

    total_fee = 0
    for fee in fees:
        total_fee += fee
    total_left = total_amount - total_fee
    # total_left = total_amount - sum(fees)

    return render_template(
        "flow_item.html",
        flow=flow,
        fees=fees,
        total_left=round(total_left, 2)
    )


@app.route("/flows")
def show_flows():
    flows = m.Flow.query.all()
    return render_template("show_flows.html", flows=flows)


@app.route("/flows_compare", methods=['GET'])
def flows_compare():
    ids = request.args.getlist('ids')
    flows = m.Flow.query.filter(Flow.id.in_(ids)).all()
    return render_template("flows_compare.html", flows=flows)


@app.route("/flows_compare", methods=['POST'])
def flow_compare_result():
    ids = request.args.getlist('ids')
    flows = m.Flow.query.filter(Flow.id.in_(ids)).all()
    total_amount = float(request.form['totalamount'].strip())
    total_lefts = []
    step_one_fees = []
    step_two_fees = []
    step_three_fees = []
    for flow in flows:
        fee = 0
        if flow.steptype1.lower() == 'percent':
            step1_fee = total_amount * flow.amount1 / 100
            fee += step1_fee
        else:
            step1_fee = flow.amount1
            fee += flow.amount1

        if flow.steptype2 == 'percent':
            step2_fee = (total_amount - fee) * flow.amount2 / 100
            fee += step2_fee
        else:
            step2_fee = flow.amount2
            fee += flow.amount2

        if flow.steptype3 == 'percent':
            step3_fee = (total_amount - fee) * flow.amount3 / 100
            fee += step3_fee
        else:
            step3_fee = flow.amount3
            fee += flow.amount3
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
    # take flow object from db
    flow = m.Flow.query.filter_by(id=flow_id).first()

    if request.method == 'POST':
        # take flow dic from json which came from react UI
        flow_json = request.get_json()
        flow.name = flow_json['name']
        # at this moment only change name and add step works
        for step in flow_json['steps']:
            if not step.get('id'):
                flow.steps.append(m.Step(**step))
            else:
                for db_step in flow.steps:
                    if db_step.id == step['id']:
                        db_step.name = step['name']
                        db_step.type = step['type']
                        db_step.amount = step['amount']
        db.session.commit()

        return jsonify(flow.as_dict())
    else:
        return render_template('flow_form.html', flow=flow, buttontext="Edit Flow")


@app.route('/delete_flow/<int:flow_id>', methods=['POST'])
def delete_flow(flow_id):
    m.Flow.query.filter_by(id=flow_id).delete()
    return redirect(url_for('show_flows'))


if __name__ == "__main__":
    app.run()

