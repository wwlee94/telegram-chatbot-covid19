import crawler
import telegram_notify as telegram_bot

data = crawler.get_total_cityline()
telegram_bot.send_msg(data)