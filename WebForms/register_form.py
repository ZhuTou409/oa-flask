from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from DataBaseModels.UserModels.user_models import EmployeeModelBase


class RegisterForm(FlaskForm):
    m_szUserName = StringField('UserName', validators=[DataRequired()])
    szEmail = StringField('EMail', validators=[DataRequired(), Email()])
    szPassword = StringField('Password', validators=[DataRequired()])
    szPasswordConfirm = StringField('PasswordConfirm', validators=[DataRequired(), EqualTo('Password')])
    submit = SubmitField('Register')
