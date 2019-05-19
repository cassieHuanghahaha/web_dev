from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators, ValidationError
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed
from user.models import User


class BaseUserForm(FlaskForm):
    name = StringField('Your name', [validators.DataRequired(), validators.Length(min=2, max=30)])
    email = EmailField('Email Address', [validators.DataRequired(), validators.Email()])
    
class RegistrationForm(BaseUserForm):
    password = PasswordField('New Password', [
               validators.DataRequired(),
               validators.EqualTo('confirm', message = 'Password must match')
    ])
    confirm = PasswordField('Repeat Password')
    
    def validate_email(FlaskForm, field):
        if User.objects.filter(email = field.data.lower()).first():
            raise ValidationError('Email address already in use')
    
 
class EditProfileForm(BaseUserForm):
    image = FileField('Profile image',
                      validators = [FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 
                                                'Only allowed .jpg .npg and .gif files')])
    bio = StringField('Bio', widget = TextArea(), validators = [validators.Length(max=200)])
    
class LoginForm(FlaskForm):
    email = EmailField('Email Address', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    
    
class PasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', [validators.DataRequired()])
    new_password = PasswordField('New Password', [validators.DataRequired(),
                                                  validators.EqualTo('confirm', message='Passwords mush match')])
    confirm = PasswordField('Confirm Password')