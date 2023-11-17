import mysql.connector
import requests

# MySQL 데이터베이스 연결 및 커서 생성
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'realtime_seoul_db',
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 장소 정보 조회 함수
def get_places_from_db():
    select_query = "SELECT area FROM realtime_seoul"
    cursor.execute(select_query)
    places = cursor.fetchall()
    return [place[0] for place in places]

# 위도 경도 정보 조회 함수 (Kakao Maps API)
def get_coordinates(api_key, place_name):
    base_url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {api_key}",
    }
    params = {
        "query": place_name
    }

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()
    
    if data.get("documents"):
        location = data["documents"][0]
        latitude = location["y"]
        longitude = location["x"]
        return latitude, longitude
    else:
        print(f"Failed to retrieve coordinates for {place_name}")
        return 0, 0

# 위도 경도 정보를 DB에 저장하는 함수
def insert_coordinates_to_db(place_name, latitude, longitude):
    insert_query = "INSERT INTO places (name, latitude, longitude) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (place_name, latitude, longitude))
    conn.commit()

# 사용자의 Kakao Maps API 키를 입력해주세요
api_key = "01049594b54ccad9ff46e783c0743987"

# 데이터베이스에서 장소 정보 가져오기
places_data = get_places_from_db()

# 장소 이름과 해당 장소의 위도 경도를 출력
for place_name in places_data:
    coordinates = get_coordinates(api_key, place_name)
    if coordinates:
        print(f"{place_name}: {coordinates}")
        insert_coordinates_to_db(place_name, *coordinates)

# DB 연결 종료
conn.close()

# 7개 지역은 직접 찾아 넣음
