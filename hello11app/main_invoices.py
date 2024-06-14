import csv
import datetime
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app
)

# from pony_blog import socketio
import time

from pony.orm import desc, commit
from werkzeug.exceptions import abort

from pony_blog import InvoiceItem
from pony_blog.auth import login_required

bp = Blueprint("main_invoices", __name__)


@bp.route("/main_invoices")
@login_required
def index():
    items = InvoiceItem.select().order_by(desc(InvoiceItem.upload_date))
    return render_template("main/invoices.html", items=items)


#
# @socketio.on('connect')
# def handle_connect():
#     # Обработка подключения клиента
#     print('Client connected')
#
# @bp.app_socketio.on('disconnect')
# def handle_disconnect():
#     # Обработка отключения клиента
#     print('Client disconnected')
#

@bp.errorhandler(400)
def err():
    return jsonify({"error": '400'}), 400


@bp.route('/main/api/intent/invoice/<string:file_name>')
def get_data(file_name):
    fullpath = os.path.join(current_app.instance_path, 'upload_files', file_name)
    try:
        with open(fullpath, 'r', encoding="utf8", errors='ignore') as file:
            reader = csv.reader(file, delimiter=',')
            file_content = list(reader)

            # print([text for text in file_content], len(file_content))
            # for row in file_content:
            # Invoice(row[0], row[1], row[2], row[3], row[4], row[5])

            InvoiceItem(file_name=file_name, upload_date=datetime.datetime.now(), rows_count=len(file_content))

            commit()
    except Exception as e:
        print("error", str(e))
        return jsonify({"file_name": file_name, "success": False, "error": str(e)}), 400

    return jsonify(
        {"file_name": file_name, "success": True, "rows_count": len(file_content)})

#     while True:
#         # Генерация данных или запрос к другому источнику данных
#         data = "New data here!"
#         # Отправка данных клиенту через веб-сокет
#         SocketIO.emit('new_data', data)
#         # Задержка перед следующей отправкой данных
#         time.sleep(5)  # Например, каждые 5 секунд
#     return "Data endpoint"
