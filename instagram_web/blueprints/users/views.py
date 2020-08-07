from flask import Blueprint, render_template,Flask, request,redirect,url_for,flash
from flask_login import login_required, login_user, current_user
from models.user import User
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    # if  not ( User.get_or_none(User.username == username) or len(username)<0):
    new_user = User(username=username,email=email,password=request.form.get('password'))
    if new_user.save():
        flash("Successful sign up")
        return redirect(url_for('users.index'))
    else:
        [flash(error) for error in new_user.errors]
        return render_template('users/new.html')


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    return render_template('users/show.html',username=username)


@users_blueprint.route('/', methods=["GET"])
def index():
    return render_template('users/index.html')


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    return render_template('users/edit.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(User.id==id)
    username=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    current_password=request.form.get('current_password')
    error_messages=[]
    if not user:
        error_messages.append('User does not exist')
    if current_user.id != id:
        error_messages.append('Cannnot edit user other than yourself')
    if current_password != current_user.password:
        error_messages.append('Key in the correct current password')
    if len(error_messages)==0:
        user.username=username
        user.email=email
        if password != "":
            if len(password)<6 and re.search(r"[a-z]",password) and re.search(r"[A-Z]",self.password) and re.search(r"[\[ \] \* \$ \% \^ \& \# \? ]", self.password):
                user.password=password
        return redirect(url_for('users.show'))
    else:
        flash(error_messages)
        render_template('users/show.html')
