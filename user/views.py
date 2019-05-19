from flask import Blueprint, render_template, request, session, redirect, url_for, abort
import bcrypt

from user.models import User
from user.forms import RegistrationForm, LoginForm, EditProfileForm, PasswordForm
from user.decorators import login_required
from utilities.storage import upload_image_file

user_page = Blueprint('user_page', __name__)

@user_page.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None
    
    if request.method == 'POST' and form.validate():
        user = User.objects.filter(email=form.email.data.lower()).first()
        if user:
            if bcrypt.checkpw(form.password.data, user.password):
                session['email'] = user.email
                return redirect(request.args.get('next') or url_for('hello'))
                user = None
        if not user:
            error = 'Your email or password was entered incorrecly!'
    return render_template('user/login.html', form = form, error= error)
# def login():
#     user = User(name = 'Cassie', password = '123', email = 'email@gmail.com')
#     user.save() # save in the mongo db
#     return "Hello, {}! Your email address is {}.".format(user.name, user.email)
@user_page.route('/signup', methods =['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        
        user = User(
            name = form.name.data,
            email = form.email.data.lower(),
            password = hashed_password
        )
        user.save()
        
        return '{} signed up!'.format(form.name.data)
    return render_template('user/signup.html', form = form)

@user_page.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('user_page.login'))

@user_page.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    user = User.objects.filter(email = session['email']).first()
    if user:
        error = None
        message = None
        form = EditProfileForm(obj = user)
        
        if request.method == 'POST' and form.validate():
            if user.email != form.email.data.lower():
                if User.objects.filter(email = form.email.data.lower()).first():
                    error = "Email is already in use."
                else:
                    session['email'] = form.email.data.lower()
            if not error:
                form.populate_obj(user)
                image_url = upload_image_file(request.files.get('image'), 'profile_image', str(user.id))
                if image_url:
                    user.profile_image = image_url
                user.save()
                message = "Profile updated"
                
        return render_template('user/edit.html', user=user, form = form, error = error, message = message)
    else:
        abort(404)
        
@user_page.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    user = User.objects.filter(email=session.get('email')).first()
    if user:
        error = None
        message = None
        form = PasswordForm()
        if request.method == 'POST' and form.validate():
            if bcrypt.checkpw(form.old_password.data, user.password):
                slat = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(form.new_password.data, salt)
                user.password = hashed_password
                user.save()
                message = 'Password updated'
            else:
                error = 'Your old password was incorrect'
        return render_template('user/password.html', form=form, error=error, message=message)
    else:
        abort(404)
                
                
                
                
        
        
    
    
    
