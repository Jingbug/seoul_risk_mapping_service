# seoul_risk_mapping_service

서울시 핫스팟 실시간 위험도를 측정하는 웹 서비스

1. 최초 1회 insert_realtime_city.py 실행
2. sql_query MySQL 에서 실
3. csv_to_db.py
4. Borough_identification.py
5. get_loc.py
6. 백 그라운드 프로세스로 update_realtime_city.py 실행
7. app.py로 Flask 실행

※결측치 발생 여부
  - 위도, 경도 7 장소를 0, 0으로 지정
  - 서울 자치구가 아닌 장소 3곳 결측 데이터 발생
