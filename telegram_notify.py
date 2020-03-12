import telegram
import config

bot= telegram.Bot(token= config.TELEGRAM_TOKEN)

def send_msg(msg):
    # 공개 그룹일 시 아이디로 메시지 전송 가능
    bot.sendMessage('@ShowCoronaNews', msg, parse_mode=telegram.ParseMode.HTML)