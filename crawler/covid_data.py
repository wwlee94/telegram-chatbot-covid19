import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import datetime

BASE_URL = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun='
helper = '\n💁🏻‍♀️ * 인구 10만 명당 \n(지역별 인구 출처 : 행정안전부 (’20.1월 기준))'

def get_update_time():
    result = requests.get(BASE_URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    today = datetime.datetime.now()
    
    time = soup.select('.timetable')[0].text.strip()
    time = time.split('.')
    
    date = f'[ {today.year}년 {time[0]}월 {time[1]}일자 업데이트 ]\n'
    return date

def get_total_cityline():
    result = requests.get(BASE_URL)
    soup = BeautifulSoup(result.text, 'html.parser')


    table = soup.select('.num tbody tr.sumline')[0]
    string = ''
    tds = table.select('td')
    if '-' not in tds[0].text:
        day_increase = f'+{tds[0].text}'
    else:
        day_increase = tds[0].text
    
    col = [0 for _ in range(4)]
    for i in range(1, 4):
        col[i] = format(int(tds[i].text), ',')

    string += '🏥 최근 코로나 확진자 합계\n'
    string += f'[확진 환자 수] {col[1]}명 ({day_increase})\n'
    string += f'[격리 해제 수] {col[2]}명\n'
    string += f'[사망자 수] {col[3]}명\n'
    string += f'[발생률 *] {tds[4].text}\n'

    return string + helper

# 테이블
def get_all_citylines():
    result = requests.get(BASE_URL)
    # result.text -> 문자열 리턴, result.content -> 바이트 리턴
    soup = BeautifulSoup(result.text, 'html.parser')

    result = []
    table = soup.select('.num tbody tr')

    for idx, row in enumerate(table[1:]):
        tds = row.select('td')
        city = row.select('th')[0].text # 시도명
        certain = format(int(tds[1].text), ',') # 확진 환자수
        if '-' not in tds[0].text:
            day_increase = f'+{tds[0].text}' # 전일대비 확진환자 증감
        else:
            day_increase = tds[0].text
    
        if day_increase == '+0': # 0이면 표기 안함
            string = f'{city}: {certain}\n'
        else:
            string = f'{city}: {certain} ({day_increase})\n'
        result.append([int(tds[1].text), string])
    
    result.sort(key= lambda x:x[0], reverse=True)
    certain_desc = '🗺 시도별 코로나 확진자 발생동향\n'
    for res in result:
        certain_desc += res[1]
    return certain_desc

# 콘솔 확인용
def pretty_print(data):
    x = PrettyTable()

    x.field_names = data[0]

    for dat in data[1:]:
        x.add_row(dat)
    return x.get_string()
