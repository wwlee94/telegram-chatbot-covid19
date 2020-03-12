import sys
sys.path.append('../')
import telegram_notify as telegram_bot

message = f'[ Show Corona Infos ]\n코로나 알리미를 시작합니다 🙇🏻\n\n📲질병관리본부, 네이버RSS 데이터를\n사용하여 국내 코로나 총 확진자 수와\n네이버 뉴스를 받아볼 수 있습니다 :)\n\n[ 매일 오전 10시 ]\n국내 코로나 총 확진자 수 알림\n[ 매 30분 ~ 1시간 ]\n실시간 네이버 최신 뉴스 알림\n\n질문 사항은 wwlee9410@gmail.com\n\nCreated by LEE, Woo-won\n'
telegram_bot.send_msg(message)