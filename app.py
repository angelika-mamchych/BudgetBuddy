# -*- coding: utf-8 -*-

from flask import abort, flash, request, render_template, redirect, url_for, jsonify, session
import models as m
from forms import SignupForm
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
    flow = m.Flow(name=flow_json['name'], user_id=user_id_or_none())
    for step in flow_json['steps']:
        flow.steps.append(m.Step(**step))
        # flow.steps.append(m.Step(name=step['name'], type=step['type'], amount=step['amount']))

    db.session.add(flow)
    db.session.commit()

    return jsonify(flow.as_dict())


@app.route("/flows/<int:flow_id>", methods=['GET'])
def flow_item(flow_id):
    flow = m.Flow.query.filter_by(id=flow_id, user_id=user_id_or_none()).first()

    if not flow:
        return abort(404)

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
            fees.append(fee)
        else:
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
    flows = m.Flow.query.filter(m.Flow.user_id == user_id_or_none()).all()
    return render_template("show_flows.html", flows=flows)


@app.route("/flows_compare", methods=['GET'])
def flows_compare():
    ids = request.args.getlist('ids')
    flows = m.Flow.query.filter(m.Flow.id.in_(ids)).all()
    return render_template("flows_compare.html", flows=flows)


@app.route("/flows_compare", methods=['POST'])
def flow_compare_result():
    ids = request.args.getlist('ids')
    fees = {}
    flows = m.Flow.query.filter(m.Flow.id.in_(ids)).all()
    total_amount = float(request.form['totalamount'].strip())

    for flow in flows:
        total_left = total_amount
        flow_fees = []
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
            'left': total_left
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


@app.route("/sign_in", methods=['GET', 'POST'])
def signin_form():
    if request.method == 'POST':
        user = m.User.query.filter_by(email=request.form['email']).first()

        if not user:
            flash('Email was not found.', 'danger')
            return render_template("signin.html")

        if request.form['password'] == user.password:
            session['user'] = user.as_dict()
            flash('Successfully logged in!', 'success')
            return redirect(url_for('show_flows'))
        else:
            flash('Password is not correct!', 'danger')

    return render_template("signin.html")


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['user'] = None
    flash('You were logged out.', 'success')
    return redirect(url_for('signin_form'))


@app.route("/sign_up", methods=['GET', 'POST'])
def signup_form():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        user = m.User(
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            password=str(form.password.data.strip())
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('signin_form'))

    return render_template('signup.html', form=form, buttontext='Sign Up')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/.well-known/acme-challenge/<string:filename>', methods=['GET'])
def https_check(filename):
    with open('.well-known/acme-challenge/{}'.format(filename), 'r') as f:
        read_data = f.read()

    return read_data


@app.before_request
def before_request():
    if request.url.startswith('http://bb.oleksii.org'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)


def user_id_or_none():
    if session.get('user', None):
        return session['user']['id']
    return None


if __name__ == "__main__":
    app.run()
