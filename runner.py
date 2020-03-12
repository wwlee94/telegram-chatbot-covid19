import crawler
import telegram_notify as telegram_bot

time = crawler.get_update_time() # 업데이트 날짜
data = crawler.get_total_cityline() # 국내 확진자 정보
telegram_bot.send_msg(time + data)