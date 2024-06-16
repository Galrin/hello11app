from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from pony.orm import desc
from werkzeug.exceptions import abort

from hello11app import Post, db
from hello11app.auth import login_required, route_access

bp = Blueprint("main_books", __name__)

books = {
    1: "build",
    2: "contract",
    3: "service",
    4: "basic",
    5: "general_ledger"
}


@bp.route("/main/books")
@login_required
@route_access
def index():
    return render_template("main/books.html")


@bp.route('/main/api/book/')
@bp.route('/main/api/book/<int:book_index>')
def get_data(book_index = 1):
    try:
        rows = db.select(f"SELECT * FROM `{books[book_index]}`")
        #for row in rows:
        #    print(row[0], row[1], row[2])
        print(jsonify({"success": True, "data": rows, "book_name": books[book_index], "book_index": book_index}))

    except Exception as e:
        print("error", str(e))
        return jsonify({"book_index": book_index, "book_name": books[book_index], "success": False, "error": str(e), "data": [
            [1,2,3],
            [2,3,4],
            [3,4,5]
        ]})

    return jsonify({"success": True, "data": rows, "book_name": books[book_index], "book_index": book_index})

