import requests
import mysql.connector
import time

# MySQL 데이터베이스에 연결
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="realtime_seoul_db"
)

mycursor = mydb.cursor()

def get_district_from_coordinates(api_key, latitude, longitude):
    base_url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
    
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }
    
    params = {
        "x": longitude,
        "y": latitude
    }
    
    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # HTTP 오류가 발생한 경우 예외 발생
        result = response.json()
        
        if result.get("documents"):
            region = result["documents"][0]
            district_name = region["region_2depth_name"]
            return district_name
        else:
            return None
        
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something went wrong", err)

def insert_borough(name, district):
    # places 테이블에 자치구 업데이트
    sql = "UPDATE places SET borough = %s WHERE name = %s"
    mycursor.execute(sql, (district, name))
    mydb.commit()
    

def get_coordinates_from_mysql():
    # places 테이블에서 위도와 경도 가져오기
    sql = "SELECT name, latitude, longitude FROM places;"
    
    mycursor.execute(sql)
    coordinates = mycursor.fetchall()
    
    return coordinates

# 사용 예시
api_key = "01049594b54ccad9ff46e783c0743987"

coordinates = get_coordinates_from_mysql()

for coord in coordinates:
    name = coord[0]
    latitude = coord[1]
    longitude = coord[2]
    
    district = get_district_from_coordinates(api_key, latitude, longitude)
    insert_borough(name, district)
    time.sleep(2)
    
mydb.close()