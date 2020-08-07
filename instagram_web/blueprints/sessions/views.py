from flask import Blueprint, render_template,Flask, request,redirect,url_for,flash
from flask_login import login_user,logout_user,login_required
from models.user import User
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint('sessions',
                                __name__,
                                template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    login_cred= request.form.get('login_cred')
    password = request.form.get('password')
    user=User.get_or_none((User.username==login_cred) |( User.email==login_cred))
    if user:
        valid_login=check_password_hash(user.password_hash,password)
        if valid_login:
            flash('Successful login')
            login_user(user)
            return render_template('sessions/index.html')
        else:
            flash('Failed login: Password does not match')
            return render_template('sessions/new.html')
    else:
        flash('Failed login: Username or email does not exist')
        return render_template('sessions/new.html')

@sessions_blueprint.route('/delete')
@login_required
def destroy():
    logout_user()
    return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@sessions_blueprint.route('/', methods=["GET"])
def index():
    return render_template('sessions/index.html')


@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass