from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import crawler
import config

def _start(bot, update):
    message = '코로나 알리미를 시작합니다 🙇🏻\n아래 사이트에서 데이터를 파싱해 국내 코로나 확진자 수를 알려드립니다. \n* 도움말 - /help \n* 확진자 수 보기 - /show \nCreated by LEE, Woo-won\n  http://ncov.mohw.go.kr/'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _help(bot, update):
    message = '📬 코로나 챗봇 알리미입니다.\n* 도움말 - /help \n* 확진자 수 보기 - /show \n'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _show(bot, update):
    # 사용한 유저 이름? 로그 띄우기 or 파일 저장
    # 업데이트 날짜도 띄우기
    data = crawler.get_total_cityline()
    bot.send_message(chat_id=update.message.chat_id, text=data)

def _unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='해당 명령어는 존재하지 않습니다 🙅🏻‍♂️')

def _run():
    updater = Updater(config.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Run the bot & Register handler
    updater.start_polling()
    dispatcher.add_handler(CommandHandler('start', _start))
    dispatcher.add_handler(CommandHandler('help', _help))
    dispatcher.add_handler(CommandHandler('show', _show))
    dispatcher.add_handler(MessageHandler(Filters.command, _unknown))

    # Run the bot until you press Ctrl-C
    updater.idle()
    updater.stop()