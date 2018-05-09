from wtforms import Form, StringField, validators, IntegerField, RadioField


class FlowForm(Form):
    flowname = StringField('Flow Nameeee', validators=[validators.input_required()])
    amount1 = IntegerField("Fee", validators=[validators.input_required()])
    #type = RadioField('Type', choices=['Fixed', 'Percent'])
    amount2 = IntegerField("Fee", validators=[validators.input_required()])