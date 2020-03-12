import config
import telegram
from runner import logger

bot= telegram.Bot(token= config.TELEGRAM_TOKEN)

def send_msg(msg):
    print(logger.info('Show Corona News에 그룹 메시지 전송 !'))
    # 공개 그룹일 시 아이디로 메시지 전송 가능
    bot.sendMessage('@ShowCoronaNews', msg, parse_mode=telegram.ParseMode.HTML)