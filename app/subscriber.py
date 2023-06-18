# python3.6

import random
import ssl

from paho.mqtt import client as mqtt_client


broker = 'vash.tech'
port = 8883
topic = "1/monitor/water"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'admin'
password = 'password'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def connack_string(connack_code):
        print({f"connack_code {connack_code}"})

    def on_log(client, userdata, level, buff):
        print(buff)

    client = mqtt_client.Client(client_id)
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
    client.on_log = on_log
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
