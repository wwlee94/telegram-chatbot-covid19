# 👾 Covid-19 코로나 텔레그램 봇
 *[Show Corona News 챗봇](https://t.me/ShowCoronaNews)* 에 참가하여 매일 오전 10시에 코로나 확진자 정보, 매일 11시~19시 사이 1시간마다 실시간 뉴스 정보를 텔레그램 메시지로 주기적으로 알림을 받을 수도 있고 `@ShowMeCorona_bot` 챗봇에 여러 커맨드를 입력해 코로나 확진자 데이터, 네이버의 실시간 뉴스 등 원하는 정보를 조회할 수 있습니다.

## 사용법
### 👨🏻‍💻 1. 텔레그램 챗봇에 접속하기 !
`@ShowMeCorona_bot` 아이디를 검색해서 질병관리본부, 네이버 RSS 데이터를 이용한 정보를 받아보세요.
### 📬 2. 텔레그램 그룹에 접속하기 (구독) !
*[Show Corona News 챗봇](https://t.me/ShowCoronaNews)* 에 접속해서 매일 오전 10시에 코로나 확진자 알림과 네이버 실시간 코로나 뉴스를 주기적으로 받아보세요.

## 💻 챗봇 로컬로 실행하기
### 의존성 모듈 설치
```
pip3 install -r requirements.txt 
```

### 환경 변수 설정
```
config.py 파일에 텔레그램을 생성해서 발급 받은 Token을 대입
```

### 실행하기
```
python3 app.py
```
실행 이후 자신이 생성한 챗봇에 메시지를 보내봅니다 :)

### 추가) 그룹을 만들어 그룹 메시지를 보내는 법
1. 텔레그램 대화 탭으로 이동합니다.
2. 메시지 추가 아이콘 클릭합니다.
3. 그룹을 생성한 후 만들었던 개인 챗봇을 초대합니다.
4. 챗봇을 관리자로 승격시킨 후 링크 공유로 그룹 아이디 생성 (`'t.me/'` 이후 문자가 그룹 아이디)
5. telegram_notify.py 파일에 생성한 그룹 아이디를 대입해줍니다.
    > bot.sendMessage('@그룹아이디', ...)
6. 아무 파일이나 생성 후 telegram_notify를 import해서 테스트 해보면 끝 !

## 배포
### 1. 챗봇 서버는 Heroku에 서버 App 생성 후 배포
### 2. 코로나 확진자 수 & 네이버 뉴스 알리미는 Github Actions (CI/CD) 사용하여 스케줄링

### 참고 사이트
* [네이버 뉴스](https://www.naver.com)
* [질병관리본부 - 코로나 발생동향](http://ncov.mohw.go.kr)
* [텔레그램 챗봇 API](https://core.telegram.org/bots)
* [챗봇 생성 및 초기 설정](https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html)