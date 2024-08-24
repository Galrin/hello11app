import datetime
import os
from types import NoneType

import pymysql
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, send_file, session, url_for, jsonify
)
from pony.orm import desc
from werkzeug.exceptions import abort

from hello11app import DistributedItem, InvoiceItem
from hello11app.auth import login_required, route_access
from config import Config

bp = Blueprint("main_distributions", __name__)


@bp.route("/main/distributions")
@login_required
@route_access
def index():
    try:
        item = InvoiceItem.get(id=session["invoice_item"])#InvoiceItem.select().order_by(desc(InvoiceItem.upload_date)).limit(1)[0]
        if(item is NoneType):
            raise TypeError("Only integers are allowed")

        distributed = list(DistributedItem.select().order_by(desc(DistributedItem.date)))
        print("item is ", type(item))
        print("item is ", item)
        print("distributed is ", type(distributed))
        print("distributed len ", len(distributed))
        return render_template("main/distributions.html", file_name=item.file_name, rows_count=item.rows_count, distributed=distributed)
    except Exception:
        return render_template("main/distributions.html", file_name="None", rows_count=0, distributed=list())

@bp.route("/distribution/request/start", methods=['POST'])
def request_start():
    file_name = request.form.get('file_name') or ""
    sql = request.form['sql']
 
    print(file_name)
    print(sql)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fullname = 'distributed_' + date + "_" + file_name
    fullpath = os.path.join(current_app.instance_path, 'upload_files', fullname)
    print(f"'{fullpath}'")
    try:
        conn = pymysql.connect(host=Config.DATABASE_HOST,
                               user=Config.DATABASE_USER,
                               password=Config.DATABASE_PASSWORD,
                               db=Config.DATABASE_NAME)
        cur = conn.cursor()
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        #print([x[0] for x in cur.description])
        rowcount = cur.rowcount
        descr1 = [x[0] for x in cur.description]
        # что за дичь :D
        descr_dict = dict()
        i = 0
        dict_len = len(descr1)
        while i < dict_len:
            descr_dict[descr1[i]] = i
            i+=1
        print(descr_dict)

        print("Total number of rows in table: ", cur.rowcount)

        with open(fullpath, 'w') as f:
            [f.write('"' + x[0].replace('"', '\""') + '",') for x in cur.description]
            f.write('"Счет главной книги"')
            f.write("\r\n")
            for record in records:                
                #print(record)
                for column in record:
                    #print(str(column))
                    col = (str(column) if column != None else "")
                    f.write('"'+ col + '",')
                    gk = getGK(conn, cur,
        record[descr_dict["Класс услуги"]],
        record[descr_dict["Услуга"]],
        record[descr_dict["Класс ОС"]],
        record[descr_dict['Признак "Используется в основной деятельности"']],
        record[descr_dict['Признак "Способ использования"']]
                    )
                    #print(gk)
                f.write('"'+ (gk if gk is not None else "") + '"'
                )
                f.write("\r\n")

        conn.close()
    except Exception as e:
        #print(e)
        pass
        #return jsonify({"success": False, 'message': e}), 400
    DistributedItem(file_name=file_name,
                    date=date,
                    rows_count=rowcount, 
                    invoice=session['invoice_item'])
    return jsonify(
        {"file_name": file_name,
         "date": date,
         "success": True,
         "rows_input_count": len([2, 2]),
         "rows_output_count": rowcount,
         "csv_name": fullname
            #,'csv': records
         })


def getGK(
    conn,
    cur,
    service_class,
    service_index,
    oc_class,
    char1,
    char2
):
    
    gk_query  = f"""SELECT `account_number` FROM general_ledger_params WHERE service_class = "{service_class}" AND service_index = "{service_index}" AND oc_class = "{oc_class}" AND char1 = "{char1}" AND char2 = "{char2}" LIMIT 1;"""

    try:
        cur.execute(gk_query)
        rec = cur.fetchone()
        conn.commit()
        return rec[0]
    except Exception as e:
        #print(e)
        pass
    return ""

@bp.route("/distribution/csv/<string:file_name>")
def get_csv(file_name):
    fullpath = os.path.join(current_app.instance_path, 'upload_files', 'distributed_' + file_name)

    return send_file(fullpath, as_attachment=True)