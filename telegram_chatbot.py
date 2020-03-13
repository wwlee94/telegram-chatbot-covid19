import config
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from crawler import (covid_data, naver_news)
from runner import logger

command_help = '* 도움말 - /help \n* 국내 총 확진자 수 - /total\n* 시도별 확진자 수 - /citylines\n* 네이버뉴스 바로 받기 - /naver_news\n* 코로나 알림 등록 - /notify\n'

def _start(bot, update):
    user = update.message.from_user
    name = f'{user.last_name}, {user.first_name} 유저 접속' 
    print(logger.info(name))

    message = f'[ Show Corona Infos ]\n코로나 알리미를 시작합니다 🙇🏻\n\n📲 질병관리본부, 네이버 RSS를 이용해\n국내 코로나 총 확진자 수와 실시간으로\n최신 뉴스를 받아볼 수 있습니다 :)\n\n/help 명령어를 입력해서 이용해보세요 !\n첫 명령어는 5~10초 소요될 수 있습니다.\n\n질문 사항은 wwlee9410@gmail.com\n\nCreated by LEE, Woo-won\n'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _help(bot, update):
    message = f'📬 코로나 챗봇 도우미입니다 :)\n{command_help}'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _total(bot, update):
    data = covid_data.get_total_cityline() # 국내 확진자 정보
    bot.send_message(chat_id=update.message.chat_id, text=data)

def _citylines(bot, update):
    data = covid_data.get_all_citylines() # 국내 도시별 확진자 정보
    bot.send_message(chat_id=update.message.chat_id, text=data)

def _naver_news(bot, update):
    news = naver_news.get_current_news() # 네이버 뉴스
    bot.send_message(chat_id=update.message.chat_id, text=news)

def _notify(bot, update):
    message = '📰 NAVER 코로나 최신 뉴스를 꾸준하게\n실시간 알림으로 받아보려면 ~!\n텔레그램 챗봇에 참여해보세요 !\nhttps://t.me/ShowCoronaNews'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='해당 명령어는 존재하지 않습니다 🙅🏻‍♂️')

def _run():
    updater = Updater(config.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Run the bot & Register handler
    updater.start_polling()
    dispatcher.add_handler(CommandHandler('start', _start))
    dispatcher.add_handler(CommandHandler('help', _help))
    dispatcher.add_handler(CommandHandler('total', _total))
    dispatcher.add_handler(CommandHandler('citylines', _citylines))
    dispatcher.add_handler(CommandHandler('naver_news', _naver_news))
    dispatcher.add_handler(CommandHandler('notify', _notify))
    dispatcher.add_handler(MessageHandler(Filters.command, _unknown))

    # Run the bot until you press Ctrl-C
    updater.idle()
    updater.stop()