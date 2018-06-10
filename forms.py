from wtforms import Form, StringField, validators, DecimalField, RadioField


class FlowForm(Form):
    flowname = StringField('Flow Name', validators=[validators.input_required()])
    stepname1 = StringField("Step Name", validators=[validators.input_required()])
    amount1 = DecimalField("Amount", validators=[validators.input_required()])
    steptype1 = RadioField('Type', choices=[('fixed', 'Fixed'), ('percent', 'Percent')])
    stepname2 = StringField("Step Name", validators=[validators.input_required()])
    amount2 = DecimalField("Amount", validators=[validators.input_required()])
    steptype2 = RadioField('Type', choices=[('fixed', 'Fixed'), ('percent', 'Percent')])
    stepname3 = StringField("Step Name", validators=[validators.input_required()])
    amount3 = DecimalField("Amount", validators=[validators.input_required()])
    steptype3 = RadioField('Type', choices=[('fixed', 'Fixed'), ('percent', 'Percent')])
