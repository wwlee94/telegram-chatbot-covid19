# Covid-19 코로나 텔레그램 봇
매일 오전 10시, 오후 6시에 텔레그램 알림을 받거나 커맨드로 원하는 정보를 조회할 수 있습니다.

## 사용법
### 👨🏻‍💻 1. 텔레그램 챗봇에 접속하기 !
`@ShowMeCorona_bot` 아이디를 검색해서 최근 데이터를 원할 때 조회해보세요.
### 📬 2. 텔레그램 그룹에 접속하기 !
*[ShowMeCorona 챗봇](https://t.me/ShowMeCorona)* 에 접속해서 매일 오전 10시, 오후 6시에 알림을 받아보세요.

## 실행해보기
### 모듈 설치
```
pip3 install -r requirements.txt 
```

### 환경 변수 설정
```
config.py 파일에 텔레그램을 생성해서 발급 받은 Token을 입력
```

### 테스트 실행
텔레그램으로 메시지를 보내봅니다.
```
python3 app.py
```

## 참고 사이트
http://ncov.mohw.go.kr