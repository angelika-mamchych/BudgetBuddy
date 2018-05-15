from wtforms import Form, StringField, validators, IntegerField, RadioField


class FlowForm(Form):
    flowname = StringField('Flow Name', validators=[validators.input_required()])
    stepname1 = StringField("Step Name", validators=[validators.input_required()])
    amount1 = IntegerField("Fee", validators=[validators.input_required()])
    #type = RadioField('Type', choices=['Fixed', 'Percent'])
    stepname2 = StringField("Step Name", validators=[validators.input_required()])
    amount2 = IntegerField("Fee", validators=[validators.input_required()])