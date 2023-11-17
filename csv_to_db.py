import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# MySQL 연결 정보 설정
config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'realtime_seoul_db',
}

# CSV 파일 경로
csv_file_path = './result_2.csv'

try:
    # MySQL 연결 생성
    cnx = mysql.connector.connect(**config)

    # 커서 생성
    cursor = cnx.cursor()

    # CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(csv_file_path, encoding='cp949')

    # 테이블 생성 쿼리
    table_name = 'your_table_name'
    create_table_query = f"CREATE TABLE IF NOT EXISTS crime_data ("

    for column in df.columns:
        create_table_query += f"{column} VARCHAR(255), "

    create_table_query = create_table_query[:-2]  # 마지막 쉼표 제거
    create_table_query += ")"

    # 테이블 생성
    cursor.execute(create_table_query)

    # 데이터프레임의 데이터를 테이블에 삽입
    for index, row in df.iterrows():
        insert_query = f"INSERT INTO crime_data ({', '.join(df.columns)}) VALUES {tuple(row.values)}"

        cursor.execute(insert_query)

    # 변경사항 커밋
    cnx.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("MySQL 접속 권한이 없습니다.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("데이터베이스에 접근할 수 없습니다.")
    else:
        print(err)

finally:
    # 연결 종료
    if 'cnx' in locals() and cnx.is_connected():
        cursor.close()
        cnx.close()