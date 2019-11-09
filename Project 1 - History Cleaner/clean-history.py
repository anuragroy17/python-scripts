import sqlite3
import re

# find your 'History' file
userName = input("Your Username: ")

conn = sqlite3.connect(f'C:/Users/{userName}/AppData/Local/Google/Chrome/User Data/Default/History')
c = conn.cursor()

result = True
id = 0

term1 = input("1st Search Term: ")
term2 = input("2nd Search Term: ")
term3 = input("3rd Search Term: ")

while result:
    result = False
    ids = []

    for row in c.execute(f"SELECT id, url FROM urls WHERE url LIKE '%{term1}%' or url LIKE '%{term2}%' or url LIKE '%{term3}%'"):
        print (row)
        id = row[0]
        ids.append((id,))

    c.executemany('DELETE FROM urls WHERE id=?', ids)
    conn.commit()

conn.close()