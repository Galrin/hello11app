from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from pony.orm import desc
from werkzeug.exceptions import abort

from hello11app.auth import login_required, route_access

_name = "forecast"
bp = Blueprint("main_" + _name, __name__)


@bp.route("/main/" + _name)
@login_required
@route_access
def index():
    return render_template("main/" + _name + ".html")
