#!/usr/bin/python

#import cgitb

#cgitb.enable()

import sqlite3
import paho.mqtt.client as mqtt

MQTT_SERVER = "192.168.1.54"
MQTT_PATH = "test_channel"

# Callback for connection with MQTT server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    #subscribe to topic, resubscribing on reconnect
    client.subscribe(MQTT_PATH)

# Callback when a PUBLISH is received
def on_message(client, userdata, msg):
    raw = str(msg.payload.decode("utf-8"))
    ldr = raw.split(':')[0]
    ss = raw.split(':')[1]
    print(msg.topic)
    print(str(msg.payload.decode("utf-8")))
    print(ldr)
    print(ss)
    toTable = (ldr, ss)
    add_value('/var/www/test/test.db', toTable)

# Place received data in sqlite3 database
def add_value(database_file, toTable):
    query = "INSERT INTO t2(ldr_val, ss_val) VALUES (?, ?);"

    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute(query, toTable)
    cursor.close()
    connection.commit()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM t2;")
    results = cursor.fetchall()
    print(results)
    cursor.close()
    connection.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
