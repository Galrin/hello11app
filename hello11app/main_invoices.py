import csv
import datetime
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, current_app
)
import pymysql

import time

from pony.orm import desc, commit, select
from werkzeug.exceptions import abort

from hello11app import InvoiceItem
from hello11app import db
from hello11app.auth import login_required

bp = Blueprint("main_invoices", __name__)

from config import Config

@bp.route("/main/invoices")
@login_required
def index():
    items = InvoiceItem.select().order_by(desc(InvoiceItem.upload_date))
    return render_template("main/invoices.html", items=items)


def setInvoice(conn, company, year, account_number, account_position, service_index, contract_index, date, cost, item_id):

    _date_split = date.split('.')
    if len(_date_split) == 3:
        date = _date_split[2] + "-" + _date_split[1] + "-" + _date_split[0]
    elif date == "":
        date = "0000-00-00"  # datetime.datetime.now().strftime("%Y-%m-%d")

    _cost_split = cost.split(',')
    if len(_cost_split) == 2:
        cost = _cost_split[0] + "." + _cost_split[1]

    cost = cost.replace(' ', '')

    sql = f'''INSERT INTO invoice (`Компания`, `Год` ,`Номер счета`, `Позиция счета`, `ID услуги`, `ID договора`, `Дата отражения счета в учетной системе`, `Стоимость без НДС`) VALUES ("{company}", "{year}", "{account_number}", "{account_position}", "{service_index}", "{contract_index}", "{date}", {cost});'''
    cur = conn.cursor()

    cur.execute(sql)


@bp.errorhandler(400) # type: ignore
def err():
    return jsonify({"error": '400'}), 400


@bp.route('/main/api/intent/invoice/<string:file_name>')
def get_data(file_name):
    fullpath = os.path.join(current_app.instance_path, 'upload_files', file_name)
    try:
        with open(fullpath, 'r', encoding="utf8", errors='ignore') as file:
            conn = pymysql.connect(host=Config.DATABASE_HOST,
                                   user=Config.DATABASE_USER,
                                   password=Config.DATABASE_PASSWORD,
                                   db=Config.DATABASE_NAME)
            cur = conn.cursor()
            cur.execute('TRUNCATE TABLE invoice')
            conn.commit()


            reader = csv.reader(file, delimiter=',')
            file_content = list(reader)

            item = InvoiceItem(file_name=file_name,
                               upload_date=datetime.datetime.now(),
                               rows_count=len(file_content),
                               upload_from_user_id=session["user_id"])
            commit()
            print(item)
            # setInvoiceList(file_content[1:], item.id)
            for row in file_content[1:]:
                setInvoice(conn, company=row[0],
                           year=row[1],
                           account_number=row[2],
                           account_position=row[3],
                           service_index=row[4],
                           contract_index=row[5],
                           date=row[6],
                           cost=row[7],
                           item_id=item.id
                           )
            print("done")
            conn.commit()
            conn.close()
    except Exception as e:
        print("error", str(e))
        return jsonify({"file_name": file_name, "success": False, "error": str(e)}), 400

    session['invoice_item'] = item.id
    return jsonify(
        {"file_name": file_name, "success": True, "rows_count": len(file_content)})

@bp.route('/invoice/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return 'Ошибка загрузки'

    file = request.files['file']

    if file.filename == '':
        return 'Файл не выбран'
    filename = os.path.join(current_app.instance_path, 'upload_files', file.filename) # type: ignore
    file.save(filename)
    return '{result:"success"}'

@bp.route('/invoice/active/<int:id>')
@login_required
def active_invoice(id):
    session['invoice_item'] = id
    item = InvoiceItem.get(id=id)
    result = active_invoice_data(item.file_name, item.id)
    print("active result: ", result["success"])
    #if result
    return '{result:"success"}', 200

@bp.route('/invoice/delete/<int:id>')
@login_required
def delete_invoice(id):
    item = InvoiceItem.get(id=id)
    item.delete()
    commit()
    if session["invoice_item"] == id:
        item = InvoiceItem.select().order_by(desc(InvoiceItem.upload_date)).limit(1)
        session["invoice_item"] = 0 if not len(item) else item[0].id
        conn = pymysql.connect(host=Config.DATABASE_HOST,
                                   user=Config.DATABASE_USER,
                                   password=Config.DATABASE_PASSWORD,
                                   db=Config.DATABASE_NAME)
        cur = conn.cursor()
        cur.execute('TRUNCATE TABLE invoice')
        conn.commit()
        conn.close()
    return '{result:"success"}', 200


def active_invoice_data(file_name, item_id):
    fullpath = os.path.join(current_app.instance_path, 'upload_files', file_name)
    try:
        with open(fullpath, 'r', encoding="utf8", errors='ignore') as file:
            conn = pymysql.connect(host=Config.DATABASE_HOST,
                                   user=Config.DATABASE_USER,
                                   password=Config.DATABASE_PASSWORD,
                                   db=Config.DATABASE_NAME)
            cur = conn.cursor()
            cur.execute('TRUNCATE TABLE invoice')
            conn.commit()


            reader = csv.reader(file, delimiter=',')
            file_content = list(reader)

            # setInvoiceList(file_content[1:], item.id)
            for row in file_content[1:]:
                setInvoice(conn, company=row[0],
                           year=row[1],
                           account_number=row[2],
                           account_position=row[3],
                           service_index=row[4],
                           contract_index=row[5],
                           date=row[6],
                           cost=row[7],
                           item_id=item_id
                           )
            print("done")
            conn.commit()
            conn.close()
    except Exception as e:
        print("error", str(e))
        return {"file_name": file_name, "success": False, "error": str(e)}

    return {"file_name": file_name, "success": True, "rows_count": len(file_content)}
