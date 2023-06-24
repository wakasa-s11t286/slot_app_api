from flask import Flask,g
from flask import render_template, request
import os
import sqlite3
import csv

app = Flask(__name__, static_folder='.', static_url_path='')

def get_db():
    if 'db' not in g:
        # データベースをオープンしてFlaskのグローバル変数に保存
        g.db = sqlite3.connect('slot_api.db')
    return g.db

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    pw = request.form.get("pw")
    print("入力されたパスワード：" + pw)
    
    if pw != "p@ssw0rd":
        print("パスワード認証エラー")
        return app.send_static_file('index.html')
    
    print("認証OK")

    file = request.files['file']
    # tempフォルダにアップロードファイルを保管
    file.save(os.path.join('./temp', file.filename))
   
    # データベースを開く
    con = get_db()
     # テーブル「商品一覧」の有無を確認
    cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='stand_data'")

    for row in cur:
        if row[0] == 0:
            # テーブルがなければ作成する
            craete_txt = "CREATE TABLE stand_data(id INTEGER PRIMARY KEY AUTOINCREMENT, stand_id INTEGER, total_cnt INTEGER, big_rate INTEGER, regular_rate INTEGER, addup_rate INTEGER, setting INTEGER, payout INTEGER, maxoutput INTEGER, chart text)"
            cur.execute(craete_txt)
    
    with open(os.path.join('./temp', file.filename), encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            print(row)
            # レコードを作る
            inset_txt = "INSERT INTO stand_data(stand_id, total_cnt, big_rate, regular_rate, addup_rate, setting, payout, maxoutput, chart) values("\
                +row[0] + ", " + row[1] + ", "+ row[2] + ", "+ row[3] + ", "+ row[4] + ", "+ row[5] + ", "+ row[6] + ", "+ row[7] + ", '"+ row[8] + "')"
            cur.execute(inset_txt)
            con.commit()
    
    
    return app.send_static_file('index.html')


@app.route('/hello/<name>')
def hello(name):
                    
    return name

@app.route('/getchart/<chart>')
def getchart(chart):

    con = get_db()
    cur = con.execute("select * from stand_data ")

    base_value = 200

    mobile_chart_list = chart.split(',')

    result_list = []

    for row in cur:
        chart_list = row[9].split(',')
        flg = False
        for cnt, c in enumerate(mobile_chart_list):
            #抽出する範囲を決定
            start = int(c) + base_value
            end = int(c) - base_value

            if start > int(chart_list[cnt]) and end < int(chart_list[cnt]):
                flg = True
            else:
                flg = False
                break
        
        if flg:
            result_list.append(row[9])
    
    if len(result_list) < 4:
        base_value = 300
        result_list = []

        cur = con.execute("select * from stand_data ")

        for row in cur:
            chart_list = row[9].split(',')
            flg = False
            for cnt, c in enumerate(mobile_chart_list):
                #抽出する範囲を決定
                start = int(c) + base_value
                end = int(c) - base_value

                if start > int(chart_list[cnt]) and end < int(chart_list[cnt]):
                    flg = True
                else:
                    flg = False
                    break
        
            if flg:
                result_list.append(row[9])
    
    if len(result_list) < 4:
        base_value = 400
        result_list = []

        cur = con.execute("select * from stand_data ")

        for row in cur:
            chart_list = row[9].split(',')
            flg = False
            for cnt, c in enumerate(mobile_chart_list):
                #抽出する範囲を決定
                start = int(c) + base_value
                end = int(c) - base_value

                if start > int(chart_list[cnt]) and end < int(chart_list[cnt]):
                    flg = True
                else:
                    flg = False
                    break
        
            if flg:
                result_list.append(row[9])

    if len(result_list) < 4:
        base_value = 500
        result_list = []

        cur = con.execute("select * from stand_data ")

        for row in cur:
            chart_list = row[9].split(',')
            flg = False
            for cnt, c in enumerate(mobile_chart_list):
                #抽出する範囲を決定
                start = int(c) + base_value
                end = int(c) - base_value

                if start > int(chart_list[cnt]) and end < int(chart_list[cnt]):
                    flg = True
                else:
                    flg = False
                    break
        
            if flg:
                result_list.append(row[9])
    
    if len(result_list) < 4:
        base_value = 800
        result_list = []

        cur = con.execute("select * from stand_data ")

        for row in cur:
            chart_list = row[9].split(',')
            flg = False
            for cnt, c in enumerate(mobile_chart_list):
                #抽出する範囲を決定
                start = int(c) + base_value
                end = int(c) - base_value

                if start > int(chart_list[cnt]) and end < int(chart_list[cnt]):
                    flg = True
                else:
                    flg = False
                    break
        
            if flg:
                result_list.append(row[9])
    
    temp_list = []
    for cnt, c in enumerate(result_list):
        if cnt == 3:
            break
        temp_list.append(c)
    
    json_obj ={
        "result":temp_list
    }

                    
    return json_obj

