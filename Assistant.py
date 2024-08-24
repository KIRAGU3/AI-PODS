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

# Setup Google Calendar API (replace with your own credentials)
def google_calendar_service():
    creds = None
    # Code to authenticate with Google API
    service = build('calendar', 'v3', credentials=creds)
    return service

# Setup Weather API
WEATHER_API_KEY = 'your_weather_api_key'
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get('main'):
        weather = response['main']
        description = response['weather'][0]['description']
        return f"The current temperature in {city} is {weather['temp']}°C with {description}."
    else:
        return "Sorry, I couldn't fetch the weather details."

# Setup News API
NEWS_API_KEY = 'your_news_api_key'
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get('articles', [])
    if articles:
        top_articles = articles[:3]
        news_summary = 'Here are the top news headlines: '
        for article in top_articles:
            news_summary += article['title'] + ". "
        return news_summary
    else:
        return "Sorry, I couldn't fetch the news."

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
    intents = {
        "reminder": ["remind", "reminder"],
        "email": ["email", "send email"],
        "calendar": ["schedule", "calendar", "event"],
        "weather": ["weather", "temperature"],
        "news": ["news", "headlines"],
        "play music": ["play music", "play song", "music"],
        "control device": ["turn on", "turn off", "set", "control"],
        "note taking": ["note", "remember", "write down"],
    }
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")

    for intent, keywords in intents.items():
        if any(keyword in text for keyword in keywords):
            return intent
    return "unknown"

# Function to handle different tasks
def handle_tasks(intent, text):
    if intent == "reminder":
        speak("Setting a reminder.")
    elif intent == "email":
        speak("Composing and sending an email.")
    elif intent == "calendar":
        schedule_event(text)
    elif intent == "weather":
        city = text.split("in")[-1].strip() if "in" in text else "your location"
        weather_info = get_weather(city)
        speak(weather_info)
    elif intent == "news":
        news = get_news()
        speak(news)
    elif intent == "play music":
        play_music(text)
    elif intent == "control device":
        control_device(text)
    elif intent == "note taking":
        take_note(text)
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

# Function to play music (example integration with Spotify)
def play_music(text):
    # Add integration with Spotify API or local music player
    speak("Playing your favorite music.")

# Function to control smart home devices (example)
def control_device(text):
    # Add integration with smart home devices (e.g., Philips Hue, SmartThings)
    speak("Controlling your smart home devices.")

# Function to take notes and manage to-do lists
def take_note(text):
    # Add integration with note-taking services (e.g., Google Keep, Microsoft To-Do)
    speak("Taking a note.")

# Main function to run the assistant
def main():
    while True:
        text = recognize_speech()
        if text:
            intent = process_nlp(text)
            handle_tasks(intent, text)

if __name__ == "__main__":
    main()

