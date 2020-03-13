import config
import requests
from telegram.ext import (Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler)
from telegram import (ReplyKeyboardMarkup, KeyboardButton)
from crawler import (covid_data, naver_news)
from runner import logger

command_help = '* 도움말 - /help \n* 국내 총 확진자 수 - /total\n* 시도별 확진자 수 - /citylines\n* 네이버뉴스 바로 받기 - /naver_news\n* 코로나 알림 등록 - /notify\n* 공적마스크 판매 현황 - /find_mask\n'

def _start(bot, update):
    user = update.message.from_user
    name = f'{user.last_name}, {user.first_name} 유저 접속' 
    print(logger.info(name))

    message = f'[ Show Corona Infos 🦠]\n코로나 알리미를 시작합니다 🙇🏻\n\n📲 질병관리본부, 네이버 RSS를 이용해\n국내 코로나 총 확진자 수와 실시간으로\n최신 뉴스를 받아볼 수 있습니다 :)\n\n🙋🏻‍♀️‍/help 명령어를 입력 후 이용하세요 !\n첫 명령어는 5~10초 소요될 수 있습니다.\n\n질문 사항은 wwlee9410@gmail.com\n\nCreated by LEE, Woo-won\n'
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

def _find_mask(bot, update):
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton('현재 위치 공유 하기',request_location=True)]],
        resize_keyboard= True,
        one_time_keyboard=True,
        selective=True
    )
    message = '[ 공적마스크 판매 현황 조회 😷]\n🏥 공적마스크 판매처 및 재고 현황을 보려면\n👾 챗봇이 현재 위치를 가져올 수 있도록\n위치 공유를 허용해주세요 !\n\n🚫 위치 전송 에러가 발생하게 되거나\n챗봇에 아무런 반응이 없다면 ❗️\n\n1. 직접 각 디바이스 설정에 들어가서\n사용자 위치 공유를 허용해주세요 !\n2. 현재 위치를 직접 전송해주세요 !'
    bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=reply_markup)

def _location(bot, update):
    message = None
    if update._effective_message:
        message = update._effective_message
    else:
        message = update.message
    current_pos = (message.location.latitude, message.location.longitude)

    result = public_mask_api(current_pos)
    print(result)

def _notify(bot, update):
    message = '📰 NAVER 코로나 최신 뉴스를 꾸준하게\n실시간 알림으로 받아보려면 ~!\n텔레그램 챗봇에 참여해보세요 !\nhttps://t.me/ShowCoronaNews'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='해당 명령어는 존재하지 않습니다 🙅🏻‍♂️')

def _error(bot, update, error):
    print(logger.info(error))

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
    dispatcher.add_handler(CommandHandler('find_mask', _find_mask))
    dispatcher.add_handler(CommandHandler('notify', _notify))
    
    # Filters의 역할?
    dispatcher.add_handler(MessageHandler(Filters.location, _location)) 
    dispatcher.add_handler(MessageHandler(Filters.command, _unknown)) # 등록되지 않은 커맨드가 filter에 걸려서 핸들러로 받음

    # bot's error handler
    dispatcher.add_error_handler(_error)

    # Run the bot until you press Ctrl-C
    updater.idle()
    updater.stop()

# 공적마스크 API 호출
def public_mask_api(pos):
    public_mask = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json'
    payload = {
        'lat': pos[0],
        'lng': pos[1],
        'm': 500
    }
    res = requests.get(public_mask, params=payload)
    stores = res.json()['stores']

    types = ['plenty', 'some', 'few', 'empty', 'break']
    stat = {
        types[0] : [],
        types[1] : [],
        types[2] : [],
        types[3] : [],
        types[4] : []
    } # 재고 상태[100개 이상(녹색): 'plenty' / 30개 이상 100개미만(노랑색): 'some' / 2개 이상 30개 미만(빨강색): 'few' / 1개 이하(회색): 'empty' / 판매중지: 'break']

    # 분류
    for store in stores:
        for _type in types:
            if store['remain_stat'] == _type:
                stat[_type].append(store)

    # plenty부터 쭉 찾으면서 3개 추출
    result = []
    for _type in types:
        if stat[_type]: 
            for store in stat[_type]:
                result.append(store)
                if len(result) == 3:
                    break
    
    # url 링크 추가
    for res in result:
        # s: start, e: end, lat: latitude, lng: longitude, text: name
        naver_map = f"http://map.naver.com/index.nhn?&slat={pos[0]}&slng={pos[1]}&elat={res['lat']}&elng={res['lng']}&etext={res['name']}&menu=route&pathType=3"
        res['url'] = naver_map
    
    return result