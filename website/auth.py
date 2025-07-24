from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from flask_login import login_user, logout_user, current_user
from . import login_manager






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


auth = Blueprint('auth', __name__)  

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_role == 'ADMIN':
            return redirect(url_for('views.admin_home'))
        elif current_user.user_role == 'STUDENT':
            return redirect(url_for('views.home'))
        elif current_user.user_role == 'TEACHER':
            return redirect(url_for('views.teacher_home'))
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if password == user.password:
                login_user(user, remember=True)
                if user.user_role == 'ADMIN':
                    return redirect(url_for('views.admin_home'))
                elif user.user_role == 'STUDENT':
                    return redirect(url_for('views.home'))
                elif user.user_role == 'TEACHER':
                    return redirect(url_for('views.teacher_home'))
            else:
                message = 'Invalid password'
        else:
            message = 'Invalid username'
        return render_template('login.html',message=message)
    return render_template('login.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up')
def sign_up():
    return "<p>Sign Up</p>"
