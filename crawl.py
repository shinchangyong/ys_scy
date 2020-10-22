# 게시판 테스트 데이터 수집을 위한 크롤링
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(host="localhost", port = 27017)
db = client.myweb
col = db.board

header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
for i in range(2):
    url = "https://modernclass.kr/board/free/list.html?board_no=1".format("데이터분석", i*10)

    res = requests.get(url, headers = header)

    bs = BeautifulSoup(res.text, "lxml")

    lists = bs.select("div.g")

    for li in lists:
        current_utc_time = round(datetime.utcnow().timestamp()*1000)

        try:
            title = li.select_one("h3.LC20lb").text
            contents = li.select_one("div.s").text
            col.insert_one({
                "name":"고말똥",
                "title": title,
                "contents":contents,
                "hit": 0,
                "regdate": current_utc_time
            })
        except:
            pass