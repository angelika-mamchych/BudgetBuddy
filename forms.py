from wtforms import Form, StringField, validators, DecimalField, RadioField, PasswordField


class FlowForm(Form):
    name = StringField('Flow Name', validators=[validators.input_required()])
    stepname1 = StringField("Step Name", validators=[validators.input_required()])
    amount1 = DecimalField("Amount", validators=[validators.input_required()])
    steptype1 = RadioField('Type', choices=[('fixed', 'Fixed'), ('percent', 'Percent')])
    stepname2 = StringField("Step Name", validators=[validators.input_required()])
    amount2 = DecimalField("Amount", validators=[validators.input_required()])
    steptype2 = RadioField('Type', choices=[('fixed', 'Fixed'), ('percent', 'Percent')])
    stepname3 = StringField("Step Name", validators=[validators.input_required()])
    amount3 = DecimalField("Amount", validators=[validators.input_required()])
    steptype3 = RadioField('Type', choices=[('fixed', 'Fixed'), ('percent', 'Percent')])


class SignupForm(Form):
    username = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField("Email", [validators.Length(min=6, max=50)])
    password = PasswordField("Password", [validators.DataRequired()])
