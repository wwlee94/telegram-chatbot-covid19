import sys
sys.path.append('../')
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

TOPIC = '코로나'
BASE_URL = f'http://newssearch.naver.com/search.naver?where=rss&query={TOPIC}&field=1&nx_search_query=&nx_and_query=&nx_sub_query=&nx_search_hlquery=&is_dts=0'
# BASE_URL = 'https://media.daum.net/syndication/today_sisa.rss' # 다음
visited_link = []
# 알림일 경우 visited 또 따로 처리해야함 -> bool 변수 생성해야할 듯?? -> 러너를 다른 환경에서 실행됨 상관 ㄴ----------------------------------------------
def get_current_news():
    data = ''
    result = requests.get(BASE_URL)
    result.encoding = 'UTF-8'
    soup = BeautifulSoup(result.text, 'html.parser')

    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    ten_minutes_ago = now + timedelta(minutes=-10)

    items = soup.select('item')
    for item in items:
        title = item.select('title')[0].text
        # 태그가 제대로 안잡혀서 따로 파싱
        link = str(item).split('<link/>')[1]
        link = link.split('<description>')[0].strip()
        if link in visited_link: continue

        visited_link.append(link)
        date = item.select('pubDate')[0].text
        date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
        date = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)

        helper = f'[ NAVER 실시간 뉴스 ]\n{date.year}년 {date.month}월 {date.day}일 {date.hour}시 {date.minute}분\n\n'
        if ten_minutes_ago <= date:    
            data += f'📰 뉴스 제목\n{title}\n\n'
            data += f"<a href='{link}'>https://search.naver.com/search.naver?where=news</a>"
            return helper + data
            
    return '📪 새로운 뉴스가 없습니다 :)'

counter = [1]
visited = {}
def get_current_news_diff(chat_id):
    data = ''
    result = requests.get(BASE_URL)
    result.encoding = 'UTF-8'
    soup = BeautifulSoup(result.text, 'html.parser')

    now = datetime.now()
    now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    ten_minutes_ago = now + timedelta(minutes=-10)

    items = soup.select('item')
    for item in items:
        title = item.select('title')[0].text
        # 태그가 제대로 안잡혀서 따로 파싱
        link = str(item).split('<link/>')[1]
        link = link.split('<description>')[0].strip()
    
        date = item.select('pubDate')[0].text
        date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')
        date = datetime(date.year, date.month, date.day, date.hour, date.minute, date.second)

        helper = f'[ NAVER 실시간 뉴스 ]\n{date.year}년 {date.month}월 {date.day}일 {date.hour}시 {date.minute}분\n\n'
        if ten_minutes_ago <= date:    
            if chat_id in list(visited.keys()):
                if link in visited[chat_id]: continue
                visited[chat_id].append(link)
                counter[0] += 1
            else:
                visited[chat_id] = [link]

            print(f'{datetime.now()}: id: {chat_id} / count: {len(visited[chat_id])} / {visited[chat_id]}')
            print(f'counter: {counter}')
            data += f'📰 뉴스 제목\n{title}\n\n'
            data += f"<a href='{link}'>https://search.naver.com/search.naver?where=news</a>"
            return helper + data
            
    return '📪 새로운 뉴스가 없습니다 :)'