from wtforms import Form, BooleanField, StringField, PasswordField, validators,SelectField, DateField
from wtforms.validators import DataRequired

class RegistrationForm(Form):
    # 'Select Report Level': 'sel_rpt_lvl',
    # 'Select Country/Company': 'sel_cty_comp',
    # 'Weekending Date Range Start date': 'wk_date_start',
    # 'Weekending Date Range End date': 'wk_date_end',
    # 'Select Report Format': 'sel_rpt_format',
    # 'Select Report Criteria': 'sel_rpt_crit',
    # 'Account / Employee': 'sel_acc_emp',
    # 'Input Field': 'input_field',

    sel_rpt_lvl = SelectField('Select Report Level', choices=[
        ('Country Level', 'Country Level'),
        ('Company Level', 'Company Level')
    ])

    # sel_cty_comp = SelectField('Select Report Level')

    schedule_cycle = SelectField('Select schedule cycle', choices=[
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ])

    wk_date_start = DateField('Weekending Date Range Start date, format is yy-mm-dd', format='%Y-%m-%d')
    wk_date_end = DateField('Weekending Date Range End date, format is yy-mm-dd', format='%Y-%m-%d')
    # 'Weekending Date Range Start date': 'wk_date_start',
    # 'Weekending Date Range End date': 'wk_date_end',

    sel_rpt_format = SelectField('Select Report Format', choices=[
        ('Result 1-10', 'Result 1-10')
    ])
    sel_rpt_crit = SelectField('Select Report Criteria', choices=[
        ('Account ID', 'Account ID'),
        ('Employee Serial', 'Employee Serial')
    ])
    sel_acc_emp = SelectField('Account / Employee', choices=[
        ('Account', 'Account'),
        ('Employee', 'Employee')
    ])
    input_field = StringField('Input Field', validators=[DataRequired()])

    run_date = DateField('schedule task run date', format='%Y-%m-%d')