import telegram
import config

bot= telegram.Bot(token= config.TELEGRAM_TOKEN)

def send_msg(msg):
    bot.sendMessage(config.CHAT_ID, msg, parse_mode=telegram.ParseMode.HTML)