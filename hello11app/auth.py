import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from pony.orm import commit
from werkzeug.security import check_password_hash, generate_password_hash

from . import User, RoleDenyRoute
from . import Role

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """
    View decorator that redirects anonymous users to the login page.
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user() -> None:
    """
    If a user id is stored in the session, load the user object from the database into ``g.user``.
    """
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.get(id=user_id)


@bp.app_errorhandler(400)
def bad_request(message):
    return jsonify({"success": False, "message": str(message)}), 400


@bp.route("/api/register", methods=('GET', 'POST'))
def api_register():
    error = None
    if not request.json or not request.json['username'] or not request.json['password']:
        error = "Необходимо заполнить все поля"
        return jsonify({"success": False, "message": error})
    # if not username:
    #     error = "Имя пользователья необходимо заполнить"
    # elif not password:
    #     error = "Пароль необходимо заполнить"
    username = request.json["username"]
    password = request.json["password"]
    if error is None:
        try:
            User(username=username, password=generate_password_hash(password))
            commit()  # Commit early to detect exception
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            error = f"Пользователь {username} уже зарегистрирован"
            return jsonify({"success": False, "message": error})
        else:
            # Success, go to the login page.
            flash(f"{username} вы успешно зарегистрировались!")
            return jsonify({"success": True, "message": url_for("main.index")})

    return jsonify({"success": False, "message": error})


@bp.route("/register", methods=("GET", "POST"))
def register():
    """
    Register a new user.

    Validates that the username is not already taken. Hashes the password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None

        if not username:
            error = "Имя пользователья необходимо заполнить"
        elif not password:
            error = "Пароль необходимо заполнить"

        if error is None:
            try:
                User(username=username, password=generate_password_hash(password))
                commit()  # Commit early to detect exception
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"Пользователь {username} уже зарегистрирован"
            else:
                # Success, go to the login page.
                flash(f"{username} вы успешно зарегистрировались!")
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/api/login", methods=("GET", "POST"))
def api_login():
    error = None
    if not request.json or not request.json['username'] or not request.json['password']:
        error = "Необходимо заполнить все поля"
        return jsonify({"success": False, "message": error})

    username = request.json["username"]
    password = request.json["password"]

    user = User.get(username=username)
    if user is None:
        error = "Пользователь неизвестен"
    elif not check_password_hash(user.password, password):
        error = "Введите верный пароль"

    if error is None:
        # store the user id in a new session and return to the index
        session.clear()
        session["user_id"] = user.id
        return jsonify({"success": True, "message": url_for("main.index")})

    return jsonify({"success": False, "message": error})


@bp.route("/login", methods=("GET", "POST"))
def login():
    """
    Log in a registered user by adding the user id to the session.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        if username != "" and password != "":
            user = User.get(username=username)
        else:
            user = None
            error = "пустые данные"

        if user is None:
            error = "Пользователь неизвестен"
        elif not check_password_hash(user.password, password):
            error = "Введите верный пароль"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("main.index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """
    Clear the current session, including the stored user id.
    """
    session.clear()

    return redirect(url_for("index"))


def route_access(view):
    """
    View decorator that redirects anonymous users to the login page.
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            if g.user.role is not None:
                if g.user.role.role_routes is not None:
                    if request.path in [role.route for role in g.user.role.role_routes]:
                        return redirect(url_for("cover.restrict"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/create/role", methods=("GET", "POST"))
@login_required
@route_access
def reg_api():
    print("path exist"
          if request.path in [role.route for role in g.user.role.role_routes]
          else "path not in set")
    print(request.path)
    print([role.route for role in g.user.role.role_routes], sep='\n')
    #User.get(id=g.user.id).set(username="111", role=Role(name="admin", access_flags="rwxq"))

    r = Role(name="admin", access_flags="rwxq", role_routes=[
        RoleDenyRoute(route="/auth/create/role"),
        RoleDenyRoute(route="/auth/create/rul"),
        RoleDenyRoute(route="/auth/create/reole"),
        RoleDenyRoute(route="/auth/create/roale")
    ])

    User.get(id=g.user.id).set(username="111", role=r)

    commit()
    # RoleDenyRoute(route="/auth/create/role", access_flags="rwxq", role=r)

    return jsonify({"result": "ok"})
