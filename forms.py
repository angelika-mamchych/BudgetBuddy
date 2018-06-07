from wtforms import Form, StringField, validators, IntegerField, RadioField


class FlowForm(Form):
    flowname = StringField('Flow Name', validators=[validators.input_required()])
    stepname1 = StringField("Step Name", validators=[validators.input_required()])
    amount1 = IntegerField("Amount", validators=[validators.input_required()])
    steptype1 = RadioField('Type', choices=['Fixed', 'Percent'])
    stepname2 = StringField("Step Name", validators=[validators.input_required()])
    amount2 = IntegerField("Amount", validators=[validators.input_required()])
    steptype2 = RadioField('Type', choices=['Fixed', 'Percent'])
    stepname3 = StringField("Step Name", validators=[validators.input_required()])
    amount3 = IntegerField("Amount", validators=[validators.input_required()])
    steptype3 = RadioField('Type', choices=['Fixed', 'Percent'])