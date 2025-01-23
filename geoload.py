import urllib.request
import sqlite3
import json
import time
import ssl

# Google Maps API 키를 입력하세요
api_key = 'AIzaSyCIUTe4sQAQX7xynLDF3Z1Pxy5LSqt1Vqs'  # Google Cloud Console에서 생성한 API 키로 대체하세요
serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# SSL 인증 문제 해결
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# SQLite 데이터베이스 초기화
conn = sqlite3.connect("geodata.sqlite")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT UNIQUE, geodata TEXT)
''')

with open("where.data", encoding="utf-8") as f:
    addresses = f.readlines()

for address in addresses:
    address = address.strip()
    if len(address) < 1:
        continue

    print(f"Looking up: {address}")

    cur.execute("SELECT geodata FROM Locations WHERE address = ?", (address,))
    row = cur.fetchone()
    if row:
        print("Found in database:", address)
        continue

    url = serviceurl + urllib.parse.urlencode({"address": address, "key": api_key})
    print("Retrieving:", url)

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()

    print(f"Retrieved {len(data)} characters:", data[:20].replace("\n", " "))

    try:
        js = json.loads(data)
    except:
        print("Failed to parse JSON")
        continue

    if "status" not in js or js["status"] != "OK":
        print("=== Failure To Retrieve ===")
        print(data)
        continue

    cur.execute("INSERT INTO Locations (address, geodata) VALUES (?, ?)", (address, data))
    conn.commit()
    time.sleep(1)

print("Run complete")
