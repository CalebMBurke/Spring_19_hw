import paho.mqtt.client as mqtt
import sqlite3

MQTT_SERVER = "192.168.1.54"
MQTT_PATH = "test_channel"

# Callback when client receives CONNACK from server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscription on connect to resubscribe in event of reconnect
    client.subscribe(MQTT_PATH)

# Callback when a PUBLISH is received
def on_message(client, userdata, msg):
    print(msg.topic +" "+ str(msg.payload))
    add_value('test.db', msg.payload)

# Place data received into a database
def add_value(database_file, new_value):
    query = "INSERT INTO testTable (value) VALUES (?);"
    
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM testTable;")
    results = cursor.fetchall()
    print(results)
    cursor.execute(query, new_value)
    cursor.close()
    connection.commit()
    connection.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()

