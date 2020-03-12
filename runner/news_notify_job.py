import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 절대경로 방법으로 상위 경로 추가
from crawler import naver_news
import telegram_notify as telegram_bot
import logger

news = naver_news.get_current_news()
if news:
    print(logger.info('NAVER 뉴스 기사 전송 성공 !'))
    telegram_bot.send_msg(news)