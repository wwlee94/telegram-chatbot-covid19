import config
import requests
from telegram.ext import (Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler)
from telegram import (ReplyKeyboardMarkup, KeyboardButton)
from crawler import (covid_data, naver_news)
from runner import logger
import time

command_help = '* 도움말 - /help \n* 국내 총 확진자 수 - /total\n* 시도별 확진자 수 - /citylines\n* 네이버뉴스 바로 받기 - /naver_news\n* 코로나 알림 등록 - /notify\n* 공적마스크 판매 현황 - /find_mask\n'

def _start(bot, update):
    user = update.message.from_user
    name = f'{user.last_name}, {user.first_name} 유저 접속' 
    print(logger.info(name))

    message = f'[ Show Corona Infos ]\n코로나 알리미를 시작합니다 🙇🏻\n\n📲 질병관리본부, 네이버 RSS를 이용해\n국내 코로나 총 확진자 수와 실시간으로\n최신 뉴스를 받아볼 수 있습니다 :)\n\n🙋🏻‍♀️‍/help 명령어를 입력 후 이용하세요 !\n첫 명령어는 5~10초 소요될 수 있습니다.\n\n질문 사항은 wwlee9410@gmail.com\n\nCreated by LEE, Woo-won\n'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _help(bot, update):
    message = f'📬 코로나 챗봇 도우미입니다 :)\n\n{command_help}'
    bot.send_message(chat_id=update.message.chat_id, text=message)

def _total(bot, update):
    data = covid_data.get_total_cityline() # 국내 확진자 정보
    bot.send_message(chat_id=update.message.chat_id, text=data)

def _citylines(bot, update):
    data = covid_data.get_all_citylines() # 국내 도시별 확진자 정보
    bot.send_message(chat_id=update.message.chat_id, text=data)

def _naver_news(bot, update):
    news = naver_news.get_current_news_diff(update.message.from_user.first_name) # 네이버 뉴스
    bot.send_message(chat_id=update.message.chat_id, text=news, parse_mode='HTML')

def _find_mask(bot, update):
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton('현재 위치 공유 하기',request_location=True)]],
        resize_keyboard= True,
        one_time_keyboard=True,
        selective=True
    )
    message = '[ 공적마스크 판매 현황 조회 ]\n\n🏥 공적마스크 판매처 및 재고 현황을 보려면\n👾 챗봇이 현재 위치를 가져올 수 있도록\n위치 공유 버튼을 클릭해주세요 !\n\n🚫 위치 전송 에러가 발생하게 되거나\n챗봇에 아무런 반응이 없다면 🚫\n\n1. 직접 각 디바이스 설정에 들어가서\n사용자 위치 공유를 허용해주세요 !\n2. 또는 현재 위치를 직접 전송해주세요 !\nTip) Clip 아이콘을 클릭합니다. \n-> Location 클릭 후 현재 위치 전송 !'
    bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=reply_markup)

def _location(bot, update):
    message = None
    if update._effective_message:
        message = update._effective_message
    else:
        message = update.message
    current_pos = (message.location.latitude, message.location.longitude)

    stores = public_mask_api(current_pos, 2)

    mask = {
        'plenty' : '✅ 충분함 - 100개 이상',
        'some' : '📳 적당함 - 30개 이상 100개 미만',
        'few' : '🆘 부족함 - 2개 이상 30개 미만',
        'empty' : '🚫 판매중지 - 재고 없음',
        'break' : '🚫 판매중지 - 재고 없음'
    }

    wcon_x, wcon_y = transcoord_api(current_pos[1], current_pos[0])
    # q = 공적마스크판매처
    message = f"[ 공적마스크 판매처 및 재고 현황 조회 ]\n\n📦 마스크 재고 상태 분류 📦\n{mask['plenty']}\n{mask['some']}\n{mask['few']}\n{mask['empty']}\n가까운 판매처 2곳은 현재위치 기준\n500m 이내의 재고 많은 순입니다 :)\n\n🗺 주변 모든 판매처 보기\n<a href='https://m.map.kakao.com/actions/searchView?q=%ea%b3%b5%ec%a0%81%eb%a7%88%ec%8a%a4%ed%81%ac%ed%8c%90%eb%a7%a4%ec%b2%98&wx={wcon_x}&wy={wcon_y}#!/all/map/place'>https://map.kakao.com</a>"
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='HTML', disable_web_page_preview=1)

    message = None
    for store in stores:
        time.sleep(1)
        message = f"[ 가까운 판매처 바로 가기 ]\n🏨 판매처 - {store['name']}\n{mask[store['remain_stat']]}\n⏰ 입고시간 - {store['stock_at']}\n\n🗺 길찾기\n<a href='{store['url']}'>https://map.kakao.com</a>"
        bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode='HTML')

def _notify(bot, update):
    message = '[ 코로나 뉴스 알리미 구독 ]\n\n📰 NAVER 코로나 실시간 뉴스를 꾸준하게\n실시간 알림으로 받아보려면 ~!\n👾 텔레그램 챗봇에 참여해보세요 !\nhttps://t.me/ShowCoronaNews'
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

# 좌표 WGS84 -> WCONGNAMUL 변환
def transcoord_api(x_loc, y_loc):
    transcoord_url = f'https://dapi.kakao.com/v2/local/geo/transcoord.json?x={x_loc}&y={y_loc}&input_coord=WGS84&output_coord=WCONGNAMUL'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization' : f'KakaoAK {config.KAKAO_API_KEY}'
    }

    res = requests.get(transcoord_url, headers= headers)
    wcon = res.json()['documents'][0]

    return wcon['x'], wcon['y']

# 공적마스크 API 호출
def public_mask_api(pos, count):
    public_mask = 'https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json'
    payload = {
        'lat': pos[0],
        'lng': pos[1],
        'm': 500
    }
    res = requests.get(public_mask, params=payload)
    stores = res.json()['stores']

    # 재고 상태 - 100개 이상(녹색): 'plenty' / 30개 이상 100개미만(노랑색): 'some' / 2개 이상 30개 미만(빨강색): 'few' / 1개 이하(회색): 'empty' / 판매중지: 'break'
    stat = {
        'plenty' : [],
        'some' : [],
        'few' : [],
        'empty' : [],
        'break' : []
    }
    types = list(stat.keys()) # dict key 순서대로 저장됨

    # 재고 상태 분류
    for store in stores:
        for _type in types:
            if store['remain_stat'] == _type:
                stat[_type].append(store)

    # plenty부터 쭉 찾으면서 3개 추출
    stores = []
    complete = False
    for _type in types:
        if stat[_type] and complete is False: 
            for store in stat[_type]:
                stores.append(store)
                if len(stores) == count:
                    complete = True
                    break

    s_x, s_y = transcoord_api(pos[1], pos[0])
    # url 링크 추가
    for store in stores:
        e_x, e_y = transcoord_api(store['lng'], store['lat'])
        kakao_map = f"https://map.kakao.com/?sX={s_x}&sY={s_y}&sName=현재+위치&eX={e_x}&eY={e_y}&eName={store['name']}"
        store['url'] = kakao_map
    
    return stores