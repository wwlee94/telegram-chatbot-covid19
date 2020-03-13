import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from crawler import covid_data
import telegram_notify as telegram_bot
import logger

time = covid_data.get_update_time() # 업데이트 날짜
print(f'코로나 데이터 업데이트 일: {time}')

data = covid_data.get_total_cityline() # 국내 확진자 정보

print(logger.info('코로나 데이터 크롤링 잡 실행 !'))
telegram_bot.send_msg(data)