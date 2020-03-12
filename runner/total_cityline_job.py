import sys
sys.path.append('../')
from crawler import covid_data
import telegram_notify as telegram_bot

print('코로나 발생동향 데이터 크롤링 시작')
time = covid_data.get_update_time() # 업데이트 날짜
data = covid_data.get_total_cityline() # 국내 확진자 정보

print('코로나 데이터 전송 성공 !')
telegram_bot.send_msg(time + data)