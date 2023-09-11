from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, FileField
from wtforms.validators import DataRequired, EqualTo, Email

class UserCreateForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired()])
    
class UserLoginForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class UserImageForm(FlaskForm):
    file = FileField('파일', validators=[DataRequired()])