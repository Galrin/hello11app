from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from pony.orm import desc, commit
from werkzeug.exceptions import abort

from hello11app import Post, Role, RoleDenyRoute, User
from hello11app.auth import login_required, route_access

_name = "final_setup"
bp = Blueprint("main_" + _name, __name__)


@bp.route("/setup" + _name)
@login_required
@route_access
def index():



    return jsonify({"success": True, "message": "Hello World!"})




@bp.route("/create/role", methods=("GET", "POST"))
@login_required
@route_access
def reg_api():
    print("path exist"
          if request.path in [role.route for role in g.user.role.role_routes]
          else "path not in set")
    print(request.path)
    print([role.route for role in g.user.role.role_routes], sep='\n')

    r = Role(name="admin", access_flags="rwxq", role_routes=[
        RoleDenyRoute(route="/auth/create/role"),
        # RoleDenyRoute(route="/auth/create/rul"),
        # RoleDenyRoute(route="/auth/create/reole"),
        # RoleDenyRoute(route="/auth/create/roale")
    ])

    #User.get(id=g.user.id).set(role=r)

    commit()

    return jsonify({"result": "ok"})