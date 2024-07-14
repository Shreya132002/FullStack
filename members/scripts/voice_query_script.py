# members/utils/voice_query.py
from django.db import models
from django.utils import timezone
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import pygame
import requests
from members.models import CropPrice

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something in Kannada...")
        recognizer.adjust_for_ambient_noise(source,duration=5)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="kn-IN")
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        speak(translate_to_kannada("Sorry, could not understand ."))
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, dest='en')
    return translation.text
def translate_to_kannada(text):
    translator = Translator()
    translation = translator.translate(text, dest='kn')
    return translation.text

statename = 'Karnataka'

def get_crop_price_english(crop_name):
    api_key = '579b464db66ec23bdd000001877ac7662958412b7a49de4e2e55a6d0'
    api_url = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070'

    params = {
        'api-key': api_key,
        'format': 'json',
        'filters[commodity]': crop_name,
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get('records', [])

        if not records:
            
            kan_crop= translate_to_kannada(crop_name)

            # If external API data is not available, query from your local database
            local_data = CropPrice.objects.filter(crop_name=kan_crop).first()
            print("From local data",local_data)
            if local_data:
                onekg=float(local_data.modal_price)/100
               
                onekg=str(onekg)
                print(f" {kan_crop} Modal Price: {local_data.modal_price}")
                speak(f" {kan_crop} ಬೆಲೆ: {local_data.modal_price} ರೂಪಾಯಿ ಮತ್ತು 1 ಕಿಲೋಗ್ರಾಂಗಾಗಿ {onekg} ರೂಪಾಯಿ")
                price = f"{local_data.crop_name}  {local_data.modal_price}ರೂಪಾಯಿ ಮತ್ತು 1 ಕಿಲೋಗ್ರಾಂಗಾಗಿ {onekg}"
                price=translate_to_kannada(price)

            else:
                

                speak("ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ")
                price = f"{'No data'}"
                price = translate_to_kannada(price)
        


        else:
            crop = translate_to_kannada(crop_name)

            for record in records:

                onekg=float(record.get('modal_price'))/100
               
                onekg=str(onekg)
                print(f"{crop_name}Market: {record.get('market')}, Arrival Date: {record.get('arrival_date')}, Modal Price: {record.get('modal_price')}")
                speak(f"{crop}ಬರವಿ ದಿನಾಂಕ: {record.get('arrival_date')},  ಬೆಲೆ: {record.get('modal_price')} ರೂಪಾಯಿ ಮತ್ತು 1 ಕಿಲೋಗ್ರಾಂಗಾಗಿ {onekg} ರೂಪಾಯಿ")
                break
            price = f"{crop} ಬೆಲೆ {records[0]['modal_price']}ರೂಪಾಯಿ ಮತ್ತು 1 ಕಿಲೋಗ್ರಾಂಗಾಗಿ {onekg}"
            print("Retrived price", price)
            # price = translate_to_kannada(price)


    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

    return price


def speak(text):
    kannada_text = gTTS(text=text, lang='kn', slow=False)
    kannada_text.save("output.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    # Block until the audio finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(15)
    pygame.mixer.quit()

    # Remove the audio file after playing
    os.remove("output.mp3")

def process_voice_query():
    global  input_text
    while True:
        speak("ಹೇಳಿ")
        input_text = recognize_speech()
        if input_text:
            print(f"You said (Kannada): {input_text}")

            

            english_text = translate_to_english(input_text)
            print(f"In English: {english_text}")
            
            result = get_crop_price_english(english_text)

            # Save the voice query to the database

            return result  # Return both English and Kannada results
            # Save the voice query to the database

def query(crop_name):
    

    
            crop_name = translate_to_kannada(crop_name)

            crop_prices = CropPrice.objects.all()
            print(crop_prices)
            local_data = CropPrice.objects.filter(crop_name=crop_name).first()
            print(local_data)
            if local_data:
                onekg=float(local_data.modal_price)/100
               
                onekg=str(onekg)
                print(f" {crop_name} Modal Price: {local_data.modal_price}")
                speak(f" {crop_name} ಬೆಲೆ: {local_data.modal_price} ರೂಪಾಯಿ ಮತ್ತು 1 ಕಿಲೋಗ್ರಾಂಗಾಗಿ {onekg} ರೂಪಾಯಿ")
                price = f"{local_data.crop_name}  {local_data.modal_price}ರೂಪಾಯಿ ಮತ್ತು 1 ಕಿಲೋಗ್ರಾಂಗಾಗಿ {onekg}"
                price=translate_to_kannada(price)

            else:
                

                speak("ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ")
                price = f"{'No data'}"
                price = translate_to_kannada(price)
        


   

            return price


