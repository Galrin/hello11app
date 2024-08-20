from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from pony.orm import desc
from werkzeug.exceptions import abort

from hello11app import InvoiceItem, User
from hello11app.auth import login_required, route_access

bp = Blueprint("main_reports", __name__)


@bp.route("/main/reports")
@login_required
@route_access
def index():
    items = InvoiceItem.select().order_by(desc(InvoiceItem.upload_date))
    return render_template("main/reports.html", items=items)

