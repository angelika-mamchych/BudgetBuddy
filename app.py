# -*- coding: utf-8 -*-

from flask import request, render_template, redirect, url_for, jsonify
import models as m
from settings import app, db


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
    total_left = total_amount
    for step in flow.steps:
        if step.type == 'fixed':
            fee = step.amount
            # all our fee equals step.amount in the end they all will be in the list fee=[] and total_left=total_amount-fee[]
            fees.append(fee)
        else:
            # step.type == 'percent'
            fee = total_left * step.amount / 100
            fees.append(fee)
        total_left -= fee

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
    flows = m.Flow.query.filter(m.Flow.id.in_(ids)).all()
    return render_template("flows_compare.html", flows=flows)


@app.route("/flows_compare", methods=['POST'])
def flow_compare_result():
    ids = request.args.getlist('ids')
    # dummy_fees = {
    #     25: {
    #         'flow_fees': [4, 5, 6],
    #         'left': 55,
    #     },
    #     30: {
    #         'flow_fees': [8, 9],
    #         'left': 77,
    #     }
    #}
    fees = {}
    flows = m.Flow.query.filter(m.Flow.id.in_(ids)).all()
    total_amount = float(request.form['totalamount'].strip())
    total_left = total_amount
    flow_fees = []
    for flow in flows:
        for step in flow.steps:
            if step.type == 'percent':
                 step_fee = total_left * step.amount / 100
                 flow_fees.append(step_fee)
            else:
                step_fee = step.amount
                flow_fees.append(step_fee)
            total_left -= step_fee

            fees[flow.id] = {
                'flow_fees': flow_fees,
                'left': total_amount - step_fee
            }


    return render_template(
        "flows_compare.html",
        flows=flows,
        fees=fees
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
    db.session.delete(m.Flow.query.get(flow_id))
    db.session.commit()
    return redirect(url_for('show_flows'))


if __name__ == "__main__":
    app.run()

