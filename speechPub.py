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

import speech_recognition as sr
import paho.mqtt.client as mqtt


# Online recognizer
def googleListenToMicrophone(language='en-US', listeningTime=5, timeout=0.5, readyMsg="Ok", confirmMsg="Received",
                       showTextMsg="Text: ", errorMsg="Error"):
    # language is the language used in the speech, language="it-IT" for Italian.
    # listeningTime is the time used for listening, in seconds.
    # readyMsg is the string printed when the system is ready for listening.
    # confirmMsg is the string printed when speech has been recorded.
    # showTextMsg is the string printed when speech text is shown.
    # errorMsg is the string printed when an error occurs.
    assert isinstance(readyMsg, str)
    assert isinstance(confirmMsg, str)
    assert isinstance(showTextMsg, str)
    assert isinstance(errorMsg, str)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        try:
            print(readyMsg)
            audio = r.listen(source, phrase_time_limit=listeningTime, timeout=timeout)
            print(confirmMsg)
            text = r.recognize_google(audio, language=language)  # Internet connection needed
            print(showTextMsg + text)
            return text
        except Exception as e:
            print(errorMsg)
            return e


# Offline recognizer
def sphinxListenToMicrophone(language='en-US', listeningTime=5, timeout=0.5, readyMsg="Ok", confirmMsg="Received",
                       showTextMsg="Text: ", errorMsg="Error"):
    # language is the language used in the speech, language="it-IT" for Italian.
    # listeningTime is the time used for listening, in seconds.
    # readyMsg is the string printed when the system is ready for listening.
    # confirmMsg is the string printed when speech has been recorded.
    # showTextMsg is the string printed when speech text is shown.
    # errorMsg is the string printed when an error occurs.
    assert isinstance(readyMsg, str)
    assert isinstance(confirmMsg, str)
    assert isinstance(showTextMsg, str)
    assert isinstance(errorMsg, str)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print(readyMsg)
        audio = r.listen(source, phrase_time_limit=listeningTime, timeout=timeout)
        print(confirmMsg)
        try:
            text = r.recognize_sphinx(audio)  # Offline recognizer
            print(showTextMsg + text)
            return text
        except Exception as e:
            print(errorMsg)
            return e


def findInText(pieceOfText, text, answer=""):
    # pieceOfText is the string to find.
    # text is the string to analyze.
    # answer is the string printed if pieceOfText has been found inside text.
    if not isinstance(pieceOfText, str):
        pieceOfText = str(pieceOfText)
    if not isinstance(text, str):
        text = str(text)
    if not isinstance(answer, str):
        answer = str(answer)
    if pieceOfText in text.lower():
        print(text.lower())
        print(answer)
        return True
    return False


def main():
    # speech recognizer configuration
    phraseTime = 3  # Listening time (seconds)
    timeout = 0.45
    readyMsg = "I'm listening, you can speak :)"
    confirmMsg = "Message received. I'm processing..."
    showTextMsg = "You told: "
    errorMsg = "Sorry, I didn't understand :("
    # mqtt iconfiguration
    hostName = "localhost"
    portNumber = 1883
    keepAliveSec = 60
    bindAddress = ""
    pubTopic = "myDevice/commands"
    # mqtt is used for communication
    client = mqtt.Client()
    client.connect(host=hostName, port=portNumber, keepalive=keepAliveSec, bind_address=bindAddress)
    while True:
        recordedText = googleListenToMicrophone( language='en-US', listeningTime=phraseTime, timeout=timeout,
                                           readyMsg=readyMsg, confirmMsg=confirmMsg,
                                           showTextMsg=showTextMsg, errorMsg=errorMsg)
        if findInText(pieceOfText="hello", text=recordedText, answer="Hi there! :)"):
            client.publish(topic=pubTopic, payload="helloAnswer");



if __name__ == '__main__':
    main()
    
