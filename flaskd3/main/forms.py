from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskd3.models import User

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                        validators = [DataRequired(), Length(min = 2, max=20)])
    """length => Length"""
    email = StringField('Email', 
                        validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose another one')


class SubmitGraphForm(FlaskForm):
    #title = StringField('Title', validators=[DataRequired()])
    #content = TextAreaField('Content', validators=[DataRequired()])
    #picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    image_file = FileField('Update Graph Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')
