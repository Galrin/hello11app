from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from pony.orm import desc
from werkzeug.exceptions import abort

from pony_blog import Post
from pony_blog.auth import login_required

bp = Blueprint("main_distributions", __name__)


@bp.route("/main_distributions")
@login_required
def index():
    return render_template("main/distributions.html")
