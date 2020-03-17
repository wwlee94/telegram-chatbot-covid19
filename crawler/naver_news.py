import sys
sys.path.append('../')
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

TOPIC = '코로나'
# BASE_URL = 'https://media.daum.net/syndication/today_sisa.rss' # 다음 기사
BASE_URL = f'http://newssearch.naver.com/search.naver?where=rss&query={TOPIC}&field=1&nx_search_query=&nx_and_query=&nx_sub_query=&nx_search_hlquery=&is_dts=0'
visited_link = {}
def get_current_news(chat_id = "runner-id"):
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

        helper = f'[ NAVER 실시간 뉴스 ]\n📰 {date.year}년 {date.month}월 {date.day}일 {date.hour}시 {date.minute}분\n\n'
        if ten_minutes_ago <= date:    
            # 사용자별 방문한 링크 조사
            if chat_id in list(visited_link.keys()):
                if link in visited_link[chat_id]: continue
                visited_link[chat_id].append(link)
            else:
                visited_link[chat_id] = [link]

            print(f'{datetime.now()}: id: {chat_id} / count: {len(visited_link[chat_id])} / {visited_link[chat_id]}')
            data += f'{title}\n'
            data += f'{link}'
            return helper + data
            
    return '📪 새로운 뉴스가 없습니다 :)'