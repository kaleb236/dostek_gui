from PyQt5.QtCore import QThread, pyqtSignal
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "NCT/mqtt/channel/odom"
topic_2 = 'NCT/mqtt/channel/positions'
topic_robit = "NCT/mqtt/channel/chat"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

class MyThread(QThread):
    value = pyqtSignal(list)
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            message = msg.payload.decode()
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.value.emit(message.split(','))
            
        client.subscribe(topic)
        client.on_message = on_message
    
    def runf(self):
        client = connect_mqtt()
        self.subscribe(client)
        client.loop_forever()
    def run(self):
        self.runf()