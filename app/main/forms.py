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

    sel_rpt_lvl = SelectField('Please select for Select Report Level', choices=[
        ('Country Level', 'Country Level'),
        ('Company Level', 'Company Level')
    ], validators=[DataRequired()])

    # sel_cty_comp = SelectField('Select Report Level',
    #                            choices=[('None','None')],
    #                            validators=[DataRequired()]
    #                            )

    schedule_cycle = SelectField('Please select for Select schedule cycle', choices=[
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ],validators=[DataRequired()])

    wk_date_start = DateField('Please select for Weekending Date Range Start date',
                    render_kw = {'class': 'datepicker','type':'date'},
                    validators=[DataRequired()]
                              )
    wk_date_end = DateField('Please select for Weekending Date Range End date',
                    render_kw = {'class': 'datepicker', 'type': 'date'},
                    validators=[DataRequired()]
                            )
    # 'Weekending Date Range Start date': 'wk_date_start',
    # 'Weekending Date Range End date': 'wk_date_end',

    sel_rpt_format = SelectField('Please select for Select Report Format', choices=[
        ('Result 1-10', 'Result 1-10')],
        validators=[DataRequired()]
        )
    sel_rpt_crit = SelectField('Please select for Select Report Criteria', choices=[
        ('Account ID', 'Account ID'),
        ('Employee Serial', 'Employee Serial')],
        validators=[DataRequired()]
                               )
    sel_acc_emp = SelectField('Please select for Account / Employee',
                              choices=[
                                ('Account', 'Account'),
                                ('Employee', 'Employee')],
                              validators=[DataRequired()]
                              )
    input_field = StringField('Input Field: Please input your Account ID or '
                              'Serial Numbers. Use Comma to separate them.',
                              validators=[DataRequired()])

    run_date = DateField('Please set the first run date for your schedule task',
                         render_kw={'class': 'datepicker', 'type': 'date'},
                         validators=[DataRequired()]
                         )