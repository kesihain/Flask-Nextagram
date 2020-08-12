from flask import Blueprint, render_template,Flask, request,redirect,url_for,flash
from flask_login import login_required, login_user, current_user
from models.user import User
from models.image import Image
from models.user_follower_rel import UserFollowerRel
from instagram_web.util.helpers import upload_file_to_s3, check_user
from werkzeug import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash

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
    user=User.get_or_none(User.username==username)
    # images=Image.select().join(User).where(Image.user_id==username)
    print(current_user.idols)
    print('here')
    return render_template('users/show.html',user=user)


@users_blueprint.route('/', methods=["GET"])
def index():
    return render_template('users/index.html')


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    return render_template('users/edit.html')


@users_blueprint.route('update/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(User.id==id)
    username=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    current_password=request.form.get('current_password')
    error_messages=[]
    if not user:
        error_messages.append('User does not exist')
    if current_user.id != int(id):
        error_messages.append('Cannnot edit user other than yourself')
    if not check_password_hash(user.password_hash,current_password):
        error_messages.append('Key in the correct current password')
    if len(error_messages)==0:
        if username != "":
            User.update({User.username:username}).where(User.id==int(id)).execute()
        if email != "":
            User.update({User.email:email}).where(User.id==int(id)).execute()
        if password != "":
            if len(password)<6 and re.search(r"[a-z]",password) and re.search(r"[A-Z]",self.password) and re.search(r"[\[ \] \* \$ \% \^ \& \# \? ]", self.password):
                User.update({User.password:password}).where(User.id==int(id)).execute()
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash(error_messages)
        return render_template('users/edit.html')

@users_blueprint.route('upload/<id>', methods=['POST'])
@login_required
def upload(id):
    user = User.get_or_none(User.id==id)
    if "display_pic" in request.files:
        file= request.files["display_pic"]
        file.filename=secure_filename(file.filename)
        #get path to s3 bucket
        image_path=upload_file_to_s3(file,user.username)
        #update user with image path
        user.image_path=image_path
        if user.save():
            return redirect(url_for('users.show',username=current_user.username))
        else:
            [flash(error) for error in user.errors]
            return redirect(url_for("users.edit", id=id))    
        
    else:
        # flash(error_messages)
        return render_template('users/edit.html')

@users_blueprint.route('/<id>/create_relationship', methods=['POST'])
@login_required
def follow(id):
    user=User.get_by_id(int(id))
    relationship= [ rel for rel in UserFollowerRel.select().where((UserFollowerRel.follower_id==current_user.id) & (UserFollowerRel.following_id==int(id)))]
    if len(relationship) ==0:
        user.follow(User.get_by_id(current_user.id))
    else:
        flash('You are already following this user')
    return redirect(url_for('users.show',username=user.username))

@users_blueprint.route('/<id>/destroy_relationship', methods=['POST'])
@login_required
def unfollow(id):
    user=User.get_by_id(int(id))
    relationship= UserFollowerRel.select().where((UserFollowerRel.follower_id==current_user.id) & (UserFollowerRel.following_id==int(id)))
    if len(relationship) !=0:
        User.get_by_id(current_user.id).unfollow(user)
    else:
        flash('You are not following this user')
    return redirect(url_for('users.show',username=user.username))
    
@users_blueprint.route('<id>/update_make_private', methods=['POST'])
@login_required
def make_private(id):
    if check_user(id):
        User.update({User.is_private:True}).where(User.id==id).execute()
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash('Cannot change privacy for user other than yourself','danger')
        return redirect(url_for('users.show',username=current_user.username)) 

@users_blueprint.route('<id>/update_make_public', methods=['POST'])
@login_required
def make_public(id):
    if check_user(id):
        User.update({User.is_private:False}).where(User.id==id).execute()
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash('Cannot change privacy for user other than yourself','danger')
        return redirect(url_for('users.show',username=current_user.username)) 
    

