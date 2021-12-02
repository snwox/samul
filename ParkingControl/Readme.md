# Parking Control
```
app.py 는 라즈베리파이에서 flask 웹서버를 실행시키는 소스이고,
car.py 는 라즈베리파이에서 번호판을 인식한 뒤 소켓을 이용해 서버로 전송하는 소스입니다.
module 폴더에 있는 licensePlate.py 가 ai 를 이용해 번호판을 탐지하는 소스입니다.
static/js 폴더에 있는 파일은 각각 메인페이지의 dom 객체에 접근해
타이머와 상태, 신규차량을 업데이트하는 소스입니다.
```
