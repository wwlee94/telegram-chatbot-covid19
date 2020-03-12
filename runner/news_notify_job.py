import sys
sys.path.append('../')
from crawler import naver_news
import telegram_notify as telegram_bot

print('NAVER 뉴스 기사 크롤링 시작')
news = naver_news.get_current_news()
if news:
    print('NAVER 기사 전송 성공 !')
    telegram_bot.send_msg(news)