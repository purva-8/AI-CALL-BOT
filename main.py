import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
import os
import pygame
import uuid
import time
from pymongo import MongoClient

# Initialize the recognizer
recognizer = sr.Recognizer()

# Set your API key here
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

# MongoDB Setup
client = MongoClient("mongodb+srv://divyanshgaba2017:xjeJJeDvoQPF544J@cluster0.on2ct.mongodb.net/")
db = client["dental_clinic"]
appointments_collection = db["appointments"]

def recognize_speech_from_mic(prompt_text):
    with sr.Microphone() as source:
        speak_text(prompt_text)
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Request failed; check your internet connection.")
            return None

def generate_response(prompt):
    try:
        response = model.generate_content(messages=[{"role": "system", "content": prompt}])
        message = response.choices[0].message['content'].strip()
        print(f"AI Response: {message}")  # Debugging statement
        return message
    except Exception as e:
        print(f"Failed to generate response: {e}")
        return "I'm sorry, I'm having trouble understanding you right now."

def speak_text(text, lang='en'):
    if not text:
        print("No text to speak.")
        return
    
    unique_filename = f"{uuid.uuid4()}.mp3"
    
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(unique_filename)
        pygame.mixer.music.load(unique_filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        time.sleep(0.5)

        pygame.mixer.music.unload()
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
    
    finally:
        try:
            os.remove(unique_filename)
        except Exception as e:
            print(f"Error deleting file: {e}")

def handle_conversation():
    print("Welcome to XYZ Dental Clinic.")
    speak_text("Welcome to XYZ Dental Clinic", lang='en')

    print("If you want to book an appointment say book an appointment")
    print("If you want to know about our services say services")
    print("If you want to talk to a human representative say speak to a human")
    print("If you want to know about our emergency contact number say emergency contact")
    speak_text("If you want to book an appointment say book an appointment")
    speak_text("If you want to know about our services say services")
    speak_text("If you want to talk to a human representative say speak to a human")
    speak_text("If you want to know about our emergency contact number say emergency contact")
    
    while True:
        user_input = recognize_speech_from_mic("Please state your request.")
        
        if user_input:
            user_input_lower = user_input.lower()
            
            if "book an appointment" in user_input_lower:
                date = None
                time_slot = None

                # Ask for the appointment date
                while not date:
                    date = recognize_speech_from_mic("Please provide the date for your appointment.")
                    if not date:
                        print("I didn't catch that. Please provide the date for your appointment.")
                        speak_text("I didn't catch that. Please provide the date for your appointment.")
                
                # Ask for the appointment time
                while not time_slot:
                    time_slot = recognize_speech_from_mic("Please provide the time for your appointment.")
                    if not time_slot:
                        print("I didn't catch that. Please provide the time for your appointment.")
                        speak_text("I didn't catch that. Please provide the time for your appointment.")

                # Check if the appointment time is available
                existing_appointment = appointments_collection.find_one({"date": date, "time": time_slot})
                if existing_appointment:
                    print(f"Sorry, there is already an appointment booked on {date} at {time_slot}.")
                    speak_text(f"Sorry, there is already an appointment booked on {date} at {time_slot}.")
                else:
                    patient_name = recognize_speech_from_mic("Please provide your name.")
                    if patient_name:
                        appointment = {
                            "date": date,
                            "time": time_slot,
                            "patient_name": patient_name
                        }
                        appointments_collection.insert_one(appointment)
                        print(f"Your appointment has been booked for {date} at {time_slot}.")
                        speak_text(f"Your appointment has been booked for {date} at {time_slot}.")
                    else:
                        print("Could not get the patient name. Appointment not booked.")
                        speak_text("Could not get the patient name. Appointment not booked.")

                print("Is there anything else I can assist you with?")
                speak_text("Is there anything else I can assist you with?")
                
            elif "speak to a human" in user_input_lower:
                print("Please wait while I connect you to a human representative.")
                speak_text("Please wait while I connect you to a human representative.")

                print("Is there anything else I can assist you with?")
                speak_text("Is there anything else I can assist you with?")
                
            elif "services" in user_input_lower or "dental services" in user_input_lower:
                services_info = "We offer a variety of dental services including cleanings, fillings, root canals, and orthodontics."
                print(services_info)
                speak_text(services_info)

                print("Is there anything else I can assist you with?")
                speak_text("Is there anything else I can assist you with?")

            elif "appointment availability" in user_input_lower:
                availability_info = "Appointments are available Monday to Friday from 9 AM to 5 PM"
                print(availability_info)
                speak_text(availability_info)

                print("Is there anything else I can assist you with?")
                speak_text("Is there anything else I can assist you with?")

            elif "clinic hours" in user_input_lower or "working hours" in user_input_lower:
                hours_info = "Our clinic is open Monday to Friday, from 9 AM to 5 PM, and Saturday from 10 AM to 2 PM."
                print(hours_info)
                speak_text(hours_info)

                print("Is there anything else I can assist you with?")
                speak_text("Is there anything else I can assist you with?")

            elif "emergency contact" in user_input_lower:
                emergency_info = "In case of a dental emergency, please call our emergency line at 123-456-7890."
                print(emergency_info)
                speak_text(emergency_info)

                print("Is there anything else I can assist you with?")
                speak_text("Is there anything else I can assist you with?")
            
            elif "no" in user_input_lower or "nothing" in user_input_lower or "exit" in user_input_lower:
                print("Thank you for contacting us. Have a great day!")
                speak_text("Thank you for contacting us. Have a great day!")
                break
                
            else:
                # Generate a response using the AI model if none of the predefined conditions are met
                prompt = f"You are a receptionist at a dental clinic. A patient says: {user_input}. How would you respond?"
                response = generate_response(prompt)
                speak_text(response)
                
        else:
            print("I didn't catch that. Could you please repeat?")
            speak_text("I didn't catch that. Could you please repeat?")

if __name__ == "__main__":
    pygame.mixer.init()
    handle_conversation()
