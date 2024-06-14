from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from pony.orm import desc
from werkzeug.exceptions import abort

from . import Post
from .auth import login_required

bp = Blueprint("cover", __name__)


@bp.route("/home")
@bp.route("/intro")
@bp.route("/")
def index():
    return render_template("cover/index.html")


@bp.route("/about")
def about():
    return render_template("cover/about.html")


@bp.route("/restrict")
def restrict():
    return render_template("cover/restrict.html")
