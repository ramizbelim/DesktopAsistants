import speech_recognition as sr
import os
import pyttsx3
import datetime
import webbrowser
import openai
from config import apikey
import random
import numpy as np
# engine = pyttsx3.init() 
#
# def say(text):
#     engine.say(text)
#     engine.runAndWait()
#

import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Ramiz: {query}\n Jarvis:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="write an email for my new job proposal",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    speaker.speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for propmt : {prompt} \n ***************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="write an email for my new job proposal",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing.....")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occured. Sorry from Jarvis"

if __name__ == '__main__':
    print('PyCharm')
    speaker.speak("jarvis A I")
    while True:
        print("Listening....")
        query = takeCommand()
        sites = [["YouTube","https://www.youtube.com"],
                 ["wikipedia","https://www.wikipedia.com"],
                 ["Google","https://www.google.com"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speaker.speak(f"Opening {site[0]} Sir......")
                webbrowser.open(site[1])

        if "open music" in query:
            musicPath = "F:/Mobile Data/audio/01 - Azhar - Bol Do Na Zara [DJMaza.Link].mp3"
            os.startfile((musicPath))

        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            speaker.speak(f"Sir the time is {strfTime}")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
