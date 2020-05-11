# Import required modules
import os.path
import json
import base64
import paho.mqtt.client as mqtt
from datetime import datetime
date = datetime.now()

# Defines global variables
USERNAME = "test-lora-20190306"
PASSWORD = "ttn-account-v2.oJuJizx84tOEq9EGPYvqW2P0HNNEL3upyVMB9A5hxoA"
DEVICE_ID = "fipy1"

TTN_BROKER_ADDR = 'eu.thethings.network'
TTN_BROKER_PORT = 8883

SUBSCRIBE_TOPIC = '{}/devices/{}/up'.format(USERNAME, DEVICE_ID)
PUBLISH_TOPIC = '{}/devices/{}/down'.format(USERNAME, DEVICE_ID)


def on_connect(client, userdata, flags, rc):
    """Callback triggered after the connection to the broker."""
    print('Connected to TTN broker, waiting for incoming messages')

    # Now that we are connected, we can subscribe to the device uplink topic.
    client.subscribe(SUBSCRIBE_TOPIC)

def on_message(client, userdata, msg):
    """Callback triggered for each message received from the server."""
    print("Message received on topic: {}".format(msg.topic))

    # MQTT payload is a JSON string
    data = json.loads(msg.payload.decode('utf-8'))
    #print (data)
    # Message payload is in the 'payload_raw' field and is encoded in base64
    print(data['payload_fields'])
    json_object = json.dumps(data['payload_fields'], indent = 6)
    with open("sample.json", "w") as outfile:
      outfile.write(json_object)

def start():
    """Create the client and connect it to the broker."""
    client = mqtt.Client()
    client.tls_set(keyfile=os.path.join(os.path.dirname(__file__),
                                        'mqtt-ca.pem'))
    client.username_pw_set(USERNAME, password=PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(TTN_BROKER_ADDR, port=TTN_BROKER_PORT, keepalive=60)


    return client


if __name__ == '__main__':
    try:
        client = start()
        client.loop_forever()
    except KeyboardInterrupt:
        # Smoothly close the connection to the broker
        client.disconnect()
