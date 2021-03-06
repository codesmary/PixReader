#!/usr/bin/env python3

from google.cloud import texttospeech
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urlparse
from playsound import playsound
from dotenv import load_dotenv
import http.client
import keyboard
import urllib
import json
import os

focus_index = -1

class MyHTMLParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.in_body = False
        self.body_contents = ''
        self.url = url

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
        elif tag == "img":
            alt_text = ''
            for att in attrs:
                if att[0] == 'src':
                    parsed_uri = urlparse(self.url)
                    parsed_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
                    rel_url = att[1]
                    response = json.loads(get_picture_description(parsed_url + "/" + rel_url))
                    try:
                        alt_text = "Auto-generated caption: " + \
                            response["description"]["captions"][0].get("text")
                    except:
                        pass
                elif att[0] == 'alt':
                    alt_text = att[1]
                    break
            self.body_contents += alt_text

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False

    def handle_data(self, data):
        if self.in_body:
            data = data.replace("\\n", " ")
            data = data.encode('utf-8').decode('unicode-escape')
            self.body_contents += data

def get_body(url):
    parser = MyHTMLParser(url)
    html = urlopen(url)
    page = str(html.read())
    parser.feed(page)
    body = parser.body_contents
    return body

def speak(word):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=word)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)

    playsound('output.mp3')

def get_picture_description(url):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': MICROSOFT_CV_SUBSCRIPTION_KEY,
    }

    params = urllib.parse.urlencode({ 'maxCandidates': '1' })
    data = { 'url': url }

    try:
        conn = http.client.HTTPSConnection('southcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/describe?%s" % params, str(data), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def move_forward(body, length):
    global focus_index
    focus_index = (focus_index + 1) % length
    speak(body[focus_index])

def move_backward(body, length):
    global focus_index
    focus_index = focus_index - 1
    if focus_index < 0:
        focus_index = length - 1
    speak(body[focus_index])

if __name__ == "__main__":
    load_dotenv()

    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    MICROSOFT_CV_SUBSCRIPTION_KEY = os.getenv('MICROSOFT_CV_SUBSCRIPTION_KEY')
    
    speak("Please enter the website.")
    url = input("Please enter the website: ")
    speak("Please wait for the webpage to be loaded.")

    body = get_body(url).split()
    body_length = len(body)
    
    speak("Use Alt to advance, and Alt+Shift to go back a word.")

    keyboard.add_hotkey('alt', move_forward, args=[body, body_length])
    keyboard.add_hotkey('alt+shift', move_backward, args=[body, body_length])
    keyboard.wait('ctrl+c')
