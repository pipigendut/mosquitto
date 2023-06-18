# python 3.6

import random
import time
import ssl

from paho.mqtt import client as mqtt_client


broker = 'vash.tech'
port = 8883
topic = "1/monitor/water"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username = 'admin'
password = 'password'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id, True, None, mqtt_client.MQTTv311)
    client.tls_set(
        ca_certs="/Users/pipigendut/Project/mosquitto/app/certs/chain.pem",
        certfile="/Users/pipigendut/Project/mosquitto/app/certs/cert.pem",
        keyfile="/Users/pipigendut/Project/mosquitto/app/certs/privkey.pem",
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS,
        ciphers=None,
    )
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"result {result}")
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
