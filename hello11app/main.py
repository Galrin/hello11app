from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from pony.orm import desc
from werkzeug.exceptions import abort

#from . import Post
from .auth import login_required

bp = Blueprint("main", __name__)


@bp.route("/main")
@login_required
def index():
    return render_template("main/index.html")
