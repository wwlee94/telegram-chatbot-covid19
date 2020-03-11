import crawler
import telegram_notify as telegram_bot


# total_data = crawler.get_all_citylines()
# print(total_data)

data = crawler.get_total_cityline()
telegram_bot.send_msg(data)