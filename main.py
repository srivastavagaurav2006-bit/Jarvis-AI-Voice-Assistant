import requests
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your Key Here>"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()

    pygame.mixer.music.load('temp.mp3')

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = OpenAI(
        api_key="<Your Key Here>",
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content


def processCommand(c):

    if "open google" in c.lower():
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    # PLAY MUSIC
    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "", 1).strip()

        print("Song requested:", song)

        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            print("Opening:", link)
            webbrowser.open(link)
        else:
            speak("Sorry, I don't have that song in my library.")

    elif "news" in c.lower():

        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if r.status_code == 200:

            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":

    speak("Initializing Jarvis....")

    while True:

        r = sr.Recognizer()

        print("Waiting for Jarvis...")

        try:
            # Wait for wake word
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=3
                )

            word = r.recognize_google(audio)

            print("You said:", word)

            if word.lower() == "jarvis":

                speak("Ya")

                # Jarvis is now continuously active
                while True:

                    try:
                        with sr.Microphone() as source:
                            print("Jarvis Active...")
                            audio = r.listen(
                                source,
                                timeout=5,
                                phrase_time_limit=5
                            )

                        command = r.recognize_google(audio)

                        print("Command:", command)

                        # Stop Jarvis completely
                        if command.lower().strip() == "over and out":
                            speak("Goodbye.")
                            exit()

                        processCommand(command)

                    except sr.WaitTimeoutError:
                        print("Command timed out.")

                    except sr.UnknownValueError:
                        print("Could not understand command.")

        except sr.WaitTimeoutError:
            print("Waiting for Jarvis...")

        except sr.UnknownValueError:
            print("Could not understand.")

        except Exception as e:
            print("Error:", e)