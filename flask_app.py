import json
from flask import Flask,g
from flask import render_template, request,jsonify
import os
import sqlite3
import csv
import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

def get_db():
    if 'db' not in g:
        # データベースをオープンしてFlaskのグローバル変数に保存
        g.db = sqlite3.connect('slot_api.db')
    return g.db

@app.route('/')
def index():
    return render_template("index.html",result=None)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    
    pw = request.form.get("pw")
    print("入力されたパスワード：" + pw)
    
    if pw != "p@ssw0rd":
        print("パスワード認証エラー")
        return render_template("index.html", result=None)
    
    print("認証OK")

    file = request.files['file']
    # tempフォルダにアップロードファイルを保管
    file.save(os.path.join('./temp', file.filename))
   
    # データベースを開く
    con = get_db()
    # テーブル「台データ」の有無を確認
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
    
    return render_template("index.html", result=None)


@app.route('/getdevice', methods=['GET', 'POST'])
def getdevice():
    
    pw = request.form.get("pw")
    print("入力されたパスワード：" + pw)
    
    if pw != "p@ssw0rd":
        print("パスワード認証エラー")
        return render_template("index.html", result=None)
    
    print("認証OK")

   
    # データベースを開く
    con = get_db()
    # テーブル「端末データ」の有無を確認
    cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='device'")

    result = []

    for row in cur:
        if row[0] == 0:
            # テーブルがなければ作成する
            craete_txt = "CREATE TABLE device(id INTEGER PRIMARY KEY AUTOINCREMENT, uid text, date text, total INTEGER, big INTEGER, regular INTEGER, cbig INTEGER, cregular INTEGER, koyaku1 INTEGER, koyaku2 INTEGER, chart text)"
            cur.execute(craete_txt)
            
            
            # TODO:ダミー
            '''
            inset_txt = "INSERT INTO device(uid, date, total,big,regular,cbig,cregular,koyaku1,koyaku2,chart) values("\
                +"'AAAA123', '2023-06-01', 5000,23,15,1,0,800,98,'0,191,245,627,682,627,518,791,955,736,682,627,573,518,409,300,136,-27,27,-82,-136,-300,-409,-191,0,-27,136,0,27,136,245,136,0,-136,-27,245,627,682,736,518,736,518,464,409,300,136,191,300,191,464,573,736,736')"
            cur.execute(inset_txt)
            con.commit()
            inset_txt = "INSERT INTO device(uid, date, total,big,regular,cbig,cregular,koyaku1,koyaku2,chart) values("\
                +"'AAAA123', '2023-06-05', 5000,23,15,1,0,800,98,'0,-82,-136,-355,-27,300,464,518,355,245,573,464,1064,1009,900,955,736,518,355,136,355,191,27,-191,-136,-245,-355,-464,-573,-627,-682,-791,-573,-791,-900,-736,-682,-955,-736,-845,-900,-791,-900,-900')"
            cur.execute(inset_txt)
            con.commit()
            inset_txt = "INSERT INTO device(uid, date, total,big,regular,cbig,cregular,koyaku1,koyaku2,chart) values("\
                +"'BBBB23', '2023-06-11', 7000,33,18,3,1,1100,130,'0,-82,-136,-355,-27,300,464,518,355,245,573,464,1064,1009,900,955,736,518,355,136,355,191,27,-191,-136,-245,-355,-464,-573,-627,-682,-791,-573,-791,-900,-736,-682,-955,-736,-845,-900,-791,-900,-900')"
            cur.execute(inset_txt)
            con.commit()
            '''
        
        else:
            cur2 = con.execute("select * from device")
            for row2 in cur2:
                if row2[0] != 0:
                    result.append(row2[1])
    
    return render_template("index.html", result=result)

@app.route('/deletedevice', methods=['GET', 'POST'])
def deletedevice():
    
    target = request.form.get("pw")
    print("削除する端末ID：" + target)
    

    # データベースを開く
    con = get_db()
    # テーブル「端末データ」の有無を確認
    cur = con.execute("select * from device where uid ='" + target + "'")
    flag = False
    cnt = 0
    result = []
    for row in cur:
        if row[0]:
            #データがあれば削除
            flag = True
            cnt += 1
    
    if flag:
        delete_txt = "delete from  device where uid ='" + target + "'"
        cur.execute(delete_txt)
        con.commit()        
        
    result.append(str(cnt)+"件削除")
    return render_template("index.html", result=result)


@app.route('/detail/<device>')
def detail(device):
    
    tot_cnt = 0
    tot_win = 0
    tot_lose = 0
    tot_output = 0
    
    
    chart1_labels = []
    chart1_data = []
    chart1_title = []
    c1_color = ["#c0c0c0","#708090","#008000","#deb887","#dc143c","#4682b4","#228b22","#d2b48c","#c71585","#4169e1","#2e8b57",
                    "#f0e68c","#ff1493","#000080","#66cdaa","#ffd700","#db7093","#8fbc8f","#ffa500","#ffc0cb","#00bfff","#00fa9a",
                    "#b8860b","#ee82ee","#87ceeb","#7fff00","#a0522d","#da70d6","#00ffff","#556b2f","#b22222","#800080","#ffe4b5"]
    temp = []
    
    con = get_db()
    cur = con.execute("select * from device where uid = '" + device + "' limit 10")
    
    for row in cur:

        y_list = row[10].split(',')
        chart1_data.append(y_list)
        chart1_title.append(row[2])
        
        if len(temp) < len(y_list):
            temp = y_list
        
        tot_cnt += 1
        if int(y_list[-1]) > 0:
            tot_win += 1
        else:
            tot_lose += 1
        tot_output += int(y_list[-1])
         
    cnt = 0
    for i in temp:
        chart1_labels.append(cnt)
        cnt += 1

                   
    return render_template("detail.html", device=device,clabels=chart1_labels, cdata=chart1_data, ccolor=c1_color, ctitle=chart1_title,
                           tot_cnt=tot_cnt,tot_win=tot_win,tot_lose=tot_lose,tot_output=tot_output)

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

@app.route('/updatedata', methods=['POST'])
def updatedata():
    
    #リクエストパラメータをJSONから受取
    d = json.loads(request.data)
    device = str(d["device"])
    total = str(d["total"])
    big = str(d["big"])
    regular = str(d["regular"])
    cbig = str(d["cbig"])
    cregular = str(d["cregular"])
    koyaku1 = str(d["koyaku1"])
    koyaku2 = str(d["koyaku2"])
    chart = str(d["chart"])
    
    
    #現在日
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    
    con = get_db()
    # テーブル「端末データ」の有無を確認
    cur = con.execute("select count(*) from sqlite_master where TYPE='table' AND name='device'")
    for row in cur:
        if row[0] == 0:
            # テーブルがなければ作成する
            craete_txt = "CREATE TABLE device(id INTEGER PRIMARY KEY AUTOINCREMENT, uid text, date text, total INTEGER, big INTEGER, regular INTEGER, cbig INTEGER, cregular INTEGER, koyaku1 INTEGER, koyaku2 INTEGER, chart text)"
            cur.execute(craete_txt)
    
    # DB登録
    inset_txt = "INSERT INTO device(uid, date, total, big, regular, cbig, cregular, koyaku1, koyaku2, chart) values("\
        + "'" + device + "', '" + today + "', " + total + "," + big +"," + regular + "," + cbig + "," + cregular + "," + koyaku1 + "," + koyaku2 + ", '" + chart + "')"
    print("登録データSQL："+inset_txt)
    cur.execute(inset_txt)
    con.commit()

    
    json_obj ={
        "result":"/detail/" + device
    }

                    
    return json_obj


@app.route('/datatable')
def datatable():
    
    device = request.args.get("device","")
    
    con = get_db()
    cur = con.execute("select * from device where uid = '" + device + "'")
    
    rlist = []
    for row in cur:
        param = {
            'date': row[2], 
            'total':row[3], 
            'big': row[4], 
            'regular':row[5], 
            'cbig': row[6], 
            'cregular': row[7], 
            'addup':"1/" + str(round(row[3]/(row[4]+row[5]+row[6]+row[7]),2)),
            'koyaku1': str(row[8])+"(1/"+str(round(row[3]/row[8],2))+")" ,
            'koyaku2': str(row[9])+"(1/"+str(round(row[3]/row[9],2))+")"
        }
        rlist.append(param)
 
    
    return jsonify(ResultSet=rlist)