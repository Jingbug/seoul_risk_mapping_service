import mysql.connector

# MySQL 데이터베이스에 연결
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="realtime_seoul_db"
)

mycursor = mydb.cursor()

try: 
    # 인구 밀집도에 따른 안전도 데이터 전처리
    def population_proc():
        data = {}
        
        sql = "select area, di from realtime_seoul"
        mycursor.execute(sql)

        # 결과 가져오기
        result = mycursor.fetchall()
        
        # 여유 -> 3, 보통 -> 1, 약간붐빔 -> 2, 붐빔 - > 4 의 수치를 부여
        for i in result:
            if i[1] == '여유':
                data[i[0]]=3
            elif i[1] == '보통':
                data[i[0]]=1
            elif i[1] == '약간 붐빔':
                data[i[0]]=2
            elif i[1] == '붐빔':
                data[i[0]]=4
        
        return data
    
    # 시각에 따른 안전도 데이터 전처리
    def realtime_proc():
        data = {}
        sql = "select area, time from realtime_seoul"
        mycursor.execute(sql)
        
        # 결과 가져오기
        result = mycursor.fetchall()
        
        for i in result:
            # 시각에서 시간 부분만 슬라이싱
            time = int(i[1][-5:-3])
            
            # # 00~06 심야 -> 3, 06~12 오전 -> 1, 12~18 오후 -> 2, 18~24 야간 -> 4 의 수치를 부여
            if 00 <= time < 6: data[i[0]]=3
            elif 6 <= time < 12: data[i[0]]=1
            elif 12 <= time < 18: data[i[0]]=2
            elif 18 <= time < 24: data[i[0]]=4
        
        return data
    
    def select_borough_proc():
        data = {}
        sql = "select name, crime_data.safe_score from crime_data, places where crime_data.area = places.borough"
        mycursor.execute(sql)
        
        # 결과 가져오기
        result = mycursor.fetchall()
        
        # 가져온 데이터를 딕셔너리로 변환
        for row in result:
            data[row[0]]=int(row[1])
            
        return data
    
    def combine_dictionaries(dict1, dict2):
        result_dict = dict1.copy()

        for key, value in dict2.items():
            if key in result_dict:
                result_dict[key] += value
            else:
                result_dict[key] = value

        return result_dict

    def update_places(result_2):
        sql = "UPDATE places SET safe_score = %s WHERE name = %s"
        for area, safe_score in result_2.items():
            mycursor.execute(sql, (safe_score, area))
    
        mydb.commit()
        
    pdict = population_proc()
    tdict = realtime_proc()
    bdict = select_borough_proc()
    
    result = combine_dictionaries(tdict, pdict)
    result_2 = combine_dictionaries(result, bdict)
    
    update_places(result_2)
    
finally:
    mydb.close()