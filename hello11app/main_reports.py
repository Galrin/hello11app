from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from pony.orm import desc
from werkzeug.exceptions import abort

from hello11app import Post
from hello11app.auth import login_required, route_access

bp = Blueprint("main_reports", __name__)


@bp.route("/main/reports")
@login_required
@route_access
def index():
    return render_template("main/reports.html")
