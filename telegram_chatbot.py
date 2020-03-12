from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from crawler import covid_data
import config

command_help = '* 도움말 - /help \n* 국내 총 확진자 수 - /total\n* 시도별 확진자 수 - /citylines \n'

def _start(bot, update):
    chat = update.message.chat
    print(chat.last_name +', '+chat.first_name)
    message = f'코로나 알리미를 시작합니다 🙇🏻\n아래 사이트에서 데이터를 파싱해 국내 코로나 확진자 수를 알려드립니다. \n{command_help}Created by LEE, Woo-won\n  http://ncov.mohw.go.kr/'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _help(bot, update):
    message = f'📬 코로나 챗봇 알리미입니다.\n{command_help}'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _total(bot, update):
    time = covid_data.get_update_time() # 업데이트 날짜
    data = covid_data.get_total_cityline() # 국내 확진자 정보
    bot.send_message(chat_id=update.message.chat_id, text=time + data)

def _citylines(bot, update):
    time = covid_data.get_update_time() # 업데이트 날짜
    data = covid_data.get_all_citylines() # 국내 도시별 확진자 정보
    bot.send_message(chat_id=update.message.chat_id, text=time + data)

def _notify(boy, update):
    message = '📰 NAVER 코로나 최신 뉴스를 실시간으로 받아보시려면 아래 챗봇에 참여해주세요 !\nhttps://t.me/ShowMeCorona'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _unknown(bot, update):
    command = update.message.text
    if command not in ['/start', '/help', '/total', '/citylines']:
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
    dispatcher.add_handler(CommandHandler('notify', _notify))
    dispatcher.add_handler(MessageHandler(Filters.command, _unknown))

    # Run the bot until you press Ctrl-C
    updater.idle()
    updater.stop()