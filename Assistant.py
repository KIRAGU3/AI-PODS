# Implementation
#a. Set Up Environment
#Install Python and Required Libraries

 # pip install speechrecognition pyttsx3 spacy transformers

#Download NLP Models
python -m spacy download en_core_web_sm

#Speech Recognition

import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, there's a problem with the speech recognition service.")
        return None
# NLP Processing

import spacy

nlp = spacy.load("en_core_web_sm")

def process_text(text):
    doc = nlp(text)
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")
    # Further processing based on entities and intent
    return doc
# Task Execution

import pyttsx3

def perform_task(text):
    engine = pyttsx3.init()
    if "reminder" in text:
        # Implement reminder functionality
        engine.say("Setting a reminder.")
    elif "email" in text:
        # Implement email functionality
        engine.say("Sending an email.")
    else:
        engine.say("I didn't understand the command.")
    engine.runAndWait() 
  
# Text-to-Speech
def text_to_speech(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait() 
  
#Integration
#Combine all components into a cohesive system.
def main():
    while True:
        command = recognize_speech()
        if command:
            doc = process_text(command)
            response = perform_task(command)
            text_to_speech(response)

if __name__ == "__main__":
    main()
