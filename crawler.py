import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=13&ncvContSeq=&contSeq=&board_id=&gubun='

def get_all_cityline():
    result = requests.get(BASE_URL)
    # result.text -> 문자열 리턴, result.content -> 바이트 리턴
    soup = BeautifulSoup(result.text, 'html.parser')

    total_data =[]
    title = [
        '시도명',
        '전일대비증감',
        '확진환자',
        '사망자',
        '발생률'
    ]
    total_data.append(title)

    table = soup.select('.num tbody tr')
    for idx, row in enumerate(table[1:]):
        result = []
        city = row.select('th')[0].text
        tds = row.select('td')

        result.append(city) # 시도명
        result.append(tds[0].text) # 전일대비 확진환자 증감
        result.append(tds[1].text) # 확진 환자수
        result.append(tds[3].text) # 사망자 수
        result.append(tds[4].text) # 발생률
        total_data.append(result)
    
    return total_data
