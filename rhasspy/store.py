import json
import requests

# pip install paho-mqtt
import paho.mqtt.client as mqtt

MQTT_HOST   = "localhost"
MQTT_PORT   = 3306
API_URL     = "http://localhost:8081/api"
API_SESSION = "abcd1234"

def on_connect(client, userdata, flags, rc):
    """Called when connected to MQTT broker."""
    client.subscribe("hermes/intent/#")
    print("Connected. Waiting for intents.")


def on_disconnect(client, userdata, flags, rc):
    """Called when disconnected from MQTT broker."""
    client.reconnect()


def on_message(client, userdata, msg):
    """Called each time a message is received on a subscribed topic."""
    nlu_payload = json.loads(msg.payload)
    if nlu_payload["intent"]["intentName"] == "GetAmount":
        print("Got intent: ", nlu_payload["intent"]["intentName"])

        # Intent
        thing = nlu_payload["slots"][0]["value"]["value"]
        print("Thing: " + thing)

        # Get amount
        req = requests.get(API_URL + "/v1/items", headers={"Content-Type": "application/json", "X-StoRe-Session": API_SESSION})
        items = json.loads(req.content)
        myItem = list(filter(lambda item: item["name"].lower() == thing.lower(), items))[0]
        amount = myItem["amount"]
        print("Amount: " + str(amount))

        # Speak the text from the intent
        sentence = str(amount)

        site_id = nlu_payload["siteId"]
        client.publish("hermes/tts/say", json.dumps({"text": sentence, "siteId": site_id}))


# Create MQTT client and connect to broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(, SKILL_PORT)
client.loop_forever()
