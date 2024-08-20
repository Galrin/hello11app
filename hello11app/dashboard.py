import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from pony.orm import desc
from werkzeug.exceptions import abort

# from . import Post
from . import Role
from .auth import login_required

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
#@bp.route("/")
@login_required
def index():
    """
    Show all the dashboard, most recent first.
    """
   # posts = Post.select().order_by(desc(Post.created))
    
    return render_template("dashboard/index.html")


@bp.route("/dashboard/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """
    Delete a post.

    Ensures that the post exists and that the logged-in user is the author of the post.
    """
    post = get_post(id)
    post.delete()

    return redirect(url_for("blog.index"))

@bp.route('/dashboard/upload_dialog', methods=['POST', 'GET'])
@login_required
def upload_dialog():
    filename = os.path.join(current_app.instance_path, 'upload_files', 'test.txt')
    try:
        Role(name="title", access_flags='rwxq')


        with open(filename, 'r') as f:

            file_content = f.read()
            # for line in f:
            #     file_content += line + '\n'
    except Exception as e:
        file_content = ""

    return render_template("dashboard/upload.html", list=file_content)
    
@bp.route('/dashboard/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return 'Ошибка загрузки'

    file = request.files['file']

    if file.filename == '':
        return 'Файл не выбран'
    filename = os.path.join(current_app.instance_path, 'upload_files', file.filename)
    # Adjust the destination path where you want to store the file
    file.save(filename)
    return '{result:"success"}'
