import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

BASE_URL = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun='

def get_total_cityline():
    result = requests.get(BASE_URL)
    soup = BeautifulSoup(result.text, 'html.parser')


    table = soup.select('.num tbody tr.sumline')[0]
    string = ''
    tds = table.select('td')

    string += '🏥 최근 코로나 확진자 합계\n'
    string += f'[전일대비 확진자 증감] {tds[0].text}명\n'
    string += f'[확진 환자 수] {tds[1].text}명\n'
    string += f'[격리 환자 수] {tds[2].text}명\n'
    string += f'[사망자 수] {tds[3].text}명\n'
    string += f'[발생률 *] {tds[4].text}\n'

    helper = '\n💁🏻‍♀️ * 인구 10만 명당 (지역별 인구 출처 : 행정안전부 (’20.1월 기준))'
    return string + helper

# 테이블
# def get_all_citylines():
#     result = requests.get(BASE_URL)
#     # result.text -> 문자열 리턴, result.content -> 바이트 리턴
#     soup = BeautifulSoup(result.text, 'html.parser')

#     data =[]
#     title = [
#         '시도명',
#         '전일대비',
#         '확진자',
#         '사망자',
#         '발생률(*)'
#     ]
#     data.append(title)

#     table = soup.select('.num tbody tr')
#     for idx, row in enumerate(table[1:]):
#         result = []
#         city = row.select('th')[0].text
#         tds = row.select('td')

#         result.append(city) # 시도명
#         result.append(tds[0].text) # 전일대비 확진환자 증감
#         result.append(tds[1].text) # 확진 환자수
#         result.append(tds[3].text) # 사망자 수
#         result.append(tds[4].text) # 발생률
#         data.append(result)

#     return data

# 콘솔 확인용
def pretty_print(data):
    x = PrettyTable()

    x.field_names = data[0]

    for dat in data[1:]:
        x.add_row(dat)
    return x.get_string()
