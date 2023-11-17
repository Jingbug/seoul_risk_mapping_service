import requests
import mysql.connector
from datetime import datetime, timedelta
import time
import xmltodict
import logging

# 로깅 설정
logging.basicConfig(filename='api_logs.log', level=logging.INFO)

try:
    # MySQL 데이터베이스에 연결
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="realtime_seoul_db"
    )

    mycursor = mydb.cursor()

    # API에서 데이터 가져오기
    def get_data_from_api():
        my_list = [str(i).zfill(3) for i in range(1, 114)]
        all_list = []
        
        for i in my_list:
            url = 'http://openapi.seoul.go.kr:8088/487256555172797535385047436d45/xml/citydata/1/5/POI' + i

            print(url)
            response = requests.get(url)
            xml_response = response.text

            # XML 디코딩
            json_response = xmltodict.parse(xml_response)
            population = json_response["SeoulRtd.citydata"]["CITYDATA"]["LIVE_PPLTN_STTS"]["LIVE_PPLTN_STTS"]
            area = json_response['SeoulRtd.citydata']['CITYDATA']['AREA_NM']
            key_list = ['AREA_CONGEST_LVL', 'AREA_CONGEST_MSG', 'PPLTN_TIME']
            
            values_to_get = [population.get(key) for key in key_list]
            
            values_to_get.append(area)
            values_to_get = values_to_get[::-1]
            
            all_list.append(values_to_get)
            time.sleep(2)
            
        return all_list

    # MySQL에 데이터 쓰기
    def write_to_mysql(data):
        for item in data:
            sql = "INSERT INTO realtime_seoul (area, time, comment, di) VALUES (%s, %s, %s, %s)"
            val = (item[0], item[1], item[2], item[3])
            mycursor.execute(sql, val)

        mydb.commit()
        
    # 최초 데이터 삽입
    data = get_data_from_api()
    write_to_mysql(data)
    
# 에러 발생 시 로깅
except Exception as e:
    logging.exception("에러 발생: %s", e)

finally:
    # DB 연결 닫기
    mydb.close()