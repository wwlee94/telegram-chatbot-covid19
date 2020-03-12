import sys
sys.path.append('../')
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# BASE_URL = 'https://media.daum.net/syndication/today_sisa.rss' # 다음
BASE_URL = 'http://newssearch.naver.com/search.naver?where=rss&query=%EC%BD%94%EB%A1%9C%EB%82%98&field=1&nx_search_query=&nx_and_query=&nx_sub_query=&nx_search_hlquery=&is_dts=0'

def get_current_news():
    data = ''
    result = requests.get(BASE_URL)
    result.encoding = 'UTF-8'
    soup = BeautifulSoup(result.text, 'html.parser')

    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    five_minutes_ago = now + timedelta(minutes=-5)
    ten_minutes_ago = now + timedelta(minutes=-10)

    items = soup.select('item')
    for item in items:
        date = item.select('pubDate')[0].text
        date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
        date = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)

        title = item.select('title')[0].text
        # author = item.select('author')[0].text
        # category = item.select('category')[0].text
        if ten_minutes_ago <= date <= five_minutes_ago:
            helper = f'[ NAVER 뉴스 ] 🗞\n{date.year}년 {date.month}월 {date.day}일 {date.hour}시 {date.minute}분\n'
            # 태그가 제대로 안잡혀서 따로 파싱
            link = str(item).split('<link/>')[1]
            link = link.split('<description>')[0].strip()
            
            data += f'{title}\n'
            data += f'{link}'
            return helper + data
            break
    return None