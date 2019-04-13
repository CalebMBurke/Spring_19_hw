#!/usr/bin/python

import sqlite3
import cgitb; cgitb.enable()

print("Content-Type: text/html\n\n")

query_ldr = "SELECT ldr_val FROM t2;"

connection = sqlite3.connect('/var/www/test/test.db')
cursor = connection.cursor()
cursor.execute(query)
results = cursor.fetchall()
print(results)
cursor.close()
connection.close()


