from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="realtime_seoul_db"
    )

    mycursor = mydb.cursor()

    sql = "SELECT name, latitude, longitude, borough, time, di, safe_score FROM realtime_seoul, places WHERE realtime_seoul.area = places.name"
    mycursor.execute(sql)

    # Fetch the results
    result = mycursor.fetchall()

    # Pass the result to the template
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
