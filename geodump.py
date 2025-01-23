import sqlite3
import json
import codecs

# SQLite 데이터베이스 연결
conn = sqlite3.connect("geodata.sqlite")
cur = conn.cursor()

# JavaScript 파일 생성
fhand = codecs.open("where.js", "w", "utf-8")
fhand.write("myData = [\n")

count = 0
for row in cur.execute("SELECT * FROM Locations"):
    data = str(row[1])
    try:
        js = json.loads(data)
    except:
        continue

    if not ("status" in js and js["status"] == "OK"):
        continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0:
        continue

    where = js["results"][0]["formatted_address"]
    try:
        print(where, lat, lng)

        if count > 0:
            fhand.write(",\n")
        output = f'{{"lat": {lat}, "lng": {lng}, "name": "{where}"}}'
        fhand.write(output)
        count += 1
    except:
        continue

fhand.write("\n];\n")
fhand.close()
print("Data has been written to where.js")
