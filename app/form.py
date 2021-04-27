from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms import SelectField, DateField, TextField
from wtforms.validators import DataRequired


class RegisterAccountForm(FlaskForm):
    # account_id = auto-generated
    balance = IntegerField('balance', validators=[DataRequired()])
    # acc_status = True (have just created --> cannot be LOCKED (False)
    role = SelectField('role', choices=['Bank Clerk','Customer'], validators=[DataRequired()])
    """ table: account """

    login_name = StringField('login_name', validators=[DataRequired()])
    register_pass = PasswordField('register_pass',validators=[DataRequired()])
    """ table: loginInfo """
    submit = SubmitField('Confirmed and move next ?')


class RegisterPersonalInfoForm(FlaskForm):
    # su_id = auto-increase --> no need to care
    fullname = StringField('fullname', validators=[DataRequired()])
    # account_id = foreign key (above)
    address = StringField('address', validators=[DataRequired()])
    phone_number = StringField('phone_number', validators=[DataRequired()])
    """ table: systemUser """
    submit = SubmitField('I confirmed my personal information !')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    login_pass = PasswordField('login_pass', validators=[DataRequired()])
    submit = SubmitField('Confirm Login ?')


class SendMoneyForm(FlaskForm):
    money_amt = IntegerField('money_amt', validators=[DataRequired()])
    receiver_account = IntegerField('receiver_id', validators=[DataRequired()])
    message = StringField('message')
    submit = SubmitField('Submit')


