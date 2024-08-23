# Implementation
#a. Set Up Environment
#Install Python and Required Libraries

 # pip install speechrecognition pyttsx3 spacy transformers

#Download NLP Models
python -m spacy download en_core_web_sm

#Speech Recognition
import speech_recognition as sr
import pyttsx3
import spacy
import threading
import datetime
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Initialize speech recognition and TTS engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
nlp = spacy.load("en_core_web_sm")

# Setup Google Calendar API (place your own credentials)
def google_calendar_service():
    creds = None
    # Load credentials from token.json or authenticate
    # Code to authenticate with Google API

    service = build('calendar', 'v3', credentials=creds)
    return service

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and return text
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Service is down."

# Function to process NLP and determine intent
def process_nlp(text):
    doc = nlp(text)
    intents = {"reminder": ["remind", "reminder"], "email": ["email", "send email"], "calendar": ["schedule", "calendar", "event"]}
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")

    for intent, keywords in intents.items():
        if any(keyword in text for keyword in keywords):
            return intent
    return "unknown"

# Function to handle different tasks
def handle_tasks(intent, text):
    if intent == "reminder":
        # Add code to set a reminder
        speak("Setting a reminder.")
    elif intent == "email":
        # Add code to send an email
        speak("Composing and sending an email.")
    elif intent == "calendar":
        schedule_event(text)
    else:
        speak("I can't perform this command.")

# Function to schedule events using Google Calendar API
def schedule_event(text):
    service = google_calendar_service()
    event = {
        'summary': 'New Event',
        'location': 'Online',
        'description': 'A new event from your AI assistant.',
        'start': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=2)).isoformat() + 'Z',
            'timeZone': 'UTC',
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    speak(f"Event created: {event.get('htmlLink')}")

# Main function to run the assistant
def main():
    while True:
        text = recognize_speech()
        if text:
            intent = process_nlp(text)
            handle_tasks(intent, text)

if __name__ == "__main__":
    main()
import speech_recognition as sr
import pyttsx3
import spacy
import threading
import datetime
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Initialize speech recognition and TTS engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
nlp = spacy.load("en_core_web_sm")

# Setup Google Calendar API (place your own credentials)
def google_calendar_service():
    creds = None
    # Load credentials from token.json or authenticate
    # Code to authenticate with Google API

    service = build('calendar', 'v3', credentials=creds)
    return service

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and return text
def recognize_speech():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I did not understand that."
    except sr.RequestError:
        return "Service is down."

# Function to process NLP and determine intent
def process_nlp(text):
    doc = nlp(text)
    intents = {"reminder": ["remind", "reminder"], "email": ["email", "send email"], "calendar": ["schedule", "calendar", "event"]}
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")

    for intent, keywords in intents.items():
        if any(keyword in text for keyword in keywords):
            return intent
    return "unknown"

# Function to handle different tasks
def handle_tasks(intent, text):
    if intent == "reminder":
        # Add code to set a reminder
        speak("Setting a reminder.")
    elif intent == "email":
        # Add code to send an email
        speak("Composing and sending an email.")
    elif intent == "calendar":
        schedule_event(text)
    else:
        speak("I can't perform this command.")

# Function to schedule events using Google Calendar API
def schedule_event(text):
    service = google_calendar_service()
    event = {
        'summary': 'New Event',
        'location': 'Online',
        'description': 'A new event from your AI assistant.',
        'start': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=2)).isoformat() + 'Z',
            'timeZone': 'UTC',
        }
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    speak(f"Event created: {event.get('htmlLink')}")

# Main function to run the assistant
def main():
    while True:
        text = recognize_speech()
        if text:
            intent = process_nlp(text)
            handle_tasks(intent, text)

if __name__ == "__main__":
    main()
