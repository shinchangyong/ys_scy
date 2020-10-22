from web_project import app, datetime, time

# flask에서 사용하는 template filter
@app.template_filter("datetime_format")
def datetime_format(value):
    if value is None:
        return ""

    # 클라이언트의 현재 시스템의 local 타임(컴퓨터의 시간)
    now_timestamp = time.time()
    
    # datetime 객체에는 fromtimestamp, utcfromtimestamp 함수가 있다.

    # fromtimestamp를 이용하면 클라이언트의 시간을 기준으로
    # datetime 객체를 만들어 준다.
    # 클라이언트의 local 타임을 datetime형식으로 만들어서 표현해줌
    print(datetime.fromtimestamp(now_timestamp))

    # utcfromtimestamp는 UTC datetime을 리턴한다.
    # db에 저장된 UTC format과 같은 형태로 반환
    print(datetime.utcfromtimestamp(now_timestamp))

    # 클라이언트의 현재 datetime형식의 시간 - 현재 datetime형식의 UTC 시간
    offset_time = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    print("offset_time : ", offset_time)

    # db에 있는 value는 db에 저장되어 있는 timestamp형식의 UTC time
    # db에 있는 value를 datetime 객체로 만든후 시간차를 더해줌
    # 새로운 value에 할당한다.
    value = datetime.fromtimestamp((int(value) / 1000))+ offset_time
    # # strftime : 시간을 원하는 string형태로 변환해줌.
    # return value.strftime("%Y-%m-%d %H:%M:%S")

 #########################################################################
    
    current_time = datetime.utcfromtimestamp(now_timestamp)
    
    # 글작성 날짜
    write_date = value.strftime('%Y-%m-%d')
    # 오늘 날짜
    today_date = current_time.strftime('%Y-%m-%d')

    if write_date == today_date:
        return value.strftime('%H:%M:%S')
    else:
        return value.strftime('%Y-%m-%d')


