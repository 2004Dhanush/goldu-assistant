import os
import time
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

engine = pyttsx3.init()
engine.setProperty('rate', 180)  # speaking rate
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice

WAKE_WORD = "goldu"

def speak(text):
    print(f"Goldu: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    speak("Hey Dhanush! Your Goldu is ready to assist you.")
    while True:
        print("Say something...")
        text = listen().lower()
        if WAKE_WORD in text:
            speak("Yes, tell me.")
            command = listen()
            if command:
                response = ask_gpt(command)
                speak(response)

if __name__ == "__main__":
    main()
