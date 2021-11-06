
import urllib.request as httplib
import json
import ssl

context=ssl.create_default_context()

#資料庫
import pymysql as MySQLdb
db=MySQLdb.connect(host="127.0.0.1",user="admin",password="admin",db="mydatabase")
cursor=db.cursor()  #連接

import schedule
import time


def job():
    print("資料抓取執行中...")
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-B0075-001?Authorization=rdec-key-123-45678-011121314"
    req = httplib.Request(url)
    reponse = httplib.urlopen(req, context=context)
    if reponse.code == 200:
        contents = reponse.read()
        data = json.loads(contents)
        # 麥寮地區 station ID=1456
        data = data['records']['seaSurfaceObs']['location'][0]['stationObsTimes']['stationObsTime']
        # 時間
        # print(data[0]['dataTime'])
        # 浪高
        # print(data[0]['weatherElements']['tideHeight'])
        # 浪潮
        # print(data[0]['weatherElements']['tideLevel'])

        for data2 in data:
            sql = "INSERT INTO `tide_table` (`tidetime`, `tideHeight`, `tideLevel`)" + \
                  "VALUES ('[value-1]','[value-2]','[value-3]')"
            # sql = sql.replace("[value-1]", "null")
            sql = sql.replace("[value-1]", str(data2['dataTime']))
            sql = sql.replace("[value-2]", str(data2['weatherElements']['tideHeight']))
            sql = sql.replace("[value-3]", str(data2['weatherElements']['tideLevel']))
            cursor.execute(sql)
        db.commit()
        db.close()
    print("資料抓取完畢")

schedule.every(5).minutes.do(job) #設定每5分鐘執行一次

job()

while True:
    schedule.run_pending()
    time.sleep(5)
