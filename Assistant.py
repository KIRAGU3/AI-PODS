import os
import sys
import logging
from pydub import AudioSegment
from pydub.playback import play
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr
import pyttsx3
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)

# Spotify API credentials (replace with your credentials)
SPOTIPY_CLIENT_ID = 'your_spotify_client_id'
SPOTIPY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback/'
SCOPE = 'user-library-read'

# Speech recognition and synthesis setup
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def setup_spotify():
    """Set up Spotify API client."""
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIPY_CLIENT_ID,
            client_secret=SPOTIPY_CLIENT_SECRET,
            redirect_uri=SPOTIPY_REDIRECT_URI,
            scope=SCOPE
        ))
        logging.info("Spotify client setup successfully.")
        return sp
    except Exception as e:
        logging.error(f"Error setting up Spotify client: {e}")
        sys.exit(1)

def fetch_playlists(sp):
    """Fetch current user's playlists."""
    try:
        results = sp.current_user_playlists()
        logging.info("Fetched playlists successfully.")
        return results
    except Exception as e:
        logging.error(f"Error fetching playlists: {e}")
        return None

def play_audio_file(file_path):
    """Play an audio file."""
    try:
        audio = AudioSegment.from_file(file_path)
        play(audio)
        logging.info("Played audio file successfully.")
    except Exception as e:
        logging.error(f"Error playing audio file: {e}")

def speak(text):
    """Convert text to speech."""
    try:
        engine.say(text)
        engine.runAndWait()
        logging.info(f"Spoke: {text}")
    except Exception as e:
        logging.error(f"Error in speech synthesis: {e}")

def listen():
    """Listen for voice input and return the recognized text."""
    try:
        with sr.Microphone() as source:
            logging.info("Listening...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            logging.info(f"Recognized: {text}")
            return text
    except sr.UnknownValueError:
        logging.error("Speech recognition could not understand audio.")
        return None
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def get_weather(city):
    """Fetch weather information for a given city."""
    API_KEY = 'your_weather_api_key'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            weather = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"The weather in {city} is {weather} with a temperature of {temp}°C."
        else:
            return f"Couldn't fetch weather data for {city}."
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return "Error fetching weather data."

def main():
    """Main function to run the audio assistant."""
    sp = setup_spotify()

    while True:
        # Listen for user command
        command = listen()

        if command:
            if "playlist" in command.lower():
                playlists = fetch_playlists(sp)
                if playlists:
                    response = "Your playlists are: "
                    for idx, playlist in enumerate(playlists['items']):
                        response += f"{idx + 1}. {playlist['name']}. "
                    speak(response)
                else:
                    speak("I couldn't fetch your playlists.")

            elif "play" in command.lower():
                sample_audio_path = 'sample_audio.mp3'
                if os.path.exists(sample_audio_path):
                    play_audio_file(sample_audio_path)
                    speak("Playing audio file.")
                else:
                    speak("Sample audio file not found.")

            elif "weather" in command.lower():
                city = command.split("weather in")[-1].strip()
                weather_info = get_weather(city)
                speak(weather_info)

            elif "exit" in command.lower():
                speak("Goodbye!")
                break

            else:
                speak("Sorry, I didn't understand that command.")

if __name__ == '__main__':
    main()

