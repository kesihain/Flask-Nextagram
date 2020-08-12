from flask import Blueprint, render_template,Flask, request,redirect,url_for,flash
from flask_login import login_required, login_user, current_user
from models.user import User
from models.image import Image
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug import secure_filename

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    return render_template('images/edit.html')


@images_blueprint.route('upload/<id>', methods=['POST'])
@login_required
def upload(id):
    user = User.get_or_none(User.id==int(id))
    if "images" in request.files:
        file= request.files["images"]
        file.filename=secure_filename(file.filename)
        #get path to s3 bucket
        image_path=upload_file_to_s3(file,user.username)
        #update user with image path
        image=Image(image_path=image_path,user_id=id)
        if image.save():
            flash('Success: Uploaded image')
            return redirect(url_for('users.show',username=current_user.username))
        else:
            [flash(error) for error in user.errors]
            return redirect(url_for("images.edit", id=id))    
        
    else:
        # flash(error_messages)
        return render_template('images/edit.html')