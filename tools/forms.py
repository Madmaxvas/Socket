import wtforms.validators
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, IntegerField, FileField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError
import email_validator
from flask_wtf.file import FileField, FileAllowed
class LoginForm(FlaskForm):
    username = StringField('Nickname', validators=[DataRequired()])  # Панель в который вводится никнейм
    password = PasswordField('Password', validators=[DataRequired()])  # Панель в который вводится пароль
    submit = SubmitField('Войти')  # Подтверждение кнопки "Войти (Залогиниться)"
    remeber_me = BooleanField("Запомнить меня")

class RegisterForm(FlaskForm):
    username = StringField('Nickname', validators=[DataRequired()])  # Панель в который вводится никнейм
    email = StringField('Email', validators=[wtforms.validators.Email(), DataRequired()])  # Панель в которое водиться
    password = PasswordField('Password', validators=[DataRequired()])  # Панель в который вводится пароль
    name = StringField('ФИО', validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")  # Подтверждение кнопки "Зарегестрироваться"
    def validate_tg(form, field):
        if len(field.data) > 50 and field.data[0] == "@":
            raise ValidationError('Name must be less than 50 characters')

class Videoupload(FlaskForm):
    name = StringField('Videoname', validators=[DataRequired()])
    opis = StringField('Opis', validators=[DataRequired()])
    tags = StringField('Tags',validators=[DataRequired()])
    photo = FileField(u'Image File',validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'bmp'])])
    video = FileField(u'Video File', validators=[DataRequired(), FileAllowed(['avi', 'wmw','mp4', 'mov','mpeg', 'flv'])])
