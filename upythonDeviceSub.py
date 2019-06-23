'''
Copyright 2019 Agnese Salutari.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License
'''

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    subTopic = "myDevice/commands"
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("myDevice/commands")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    receivedMsg = msg.payload.decode()
    print("Received Message: " + receivedMsg)
    if receivedMsg == "helloAnswer":
        print("Hi! :)")


def main():
    # mqtt iconfiguration
    hostName = "localhost"
    portNumber = 1883
    keepAliveSec = 60
    bindAddress = ""
    # mqtt is used for communication
    client = mqtt.Client()
    client.connect(host=hostName, port=portNumber, keepalive=keepAliveSec, bind_address=bindAddress)
    print("Ready!")
    while True:
        client.on_connect = on_connect
        client.on_message = on_message
        client.loop_forever()


if __name__ == '__main__':
    main()
    
