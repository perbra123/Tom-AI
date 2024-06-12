from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pyttsx3
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

def extract_information(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            paragraphs = soup.find_all("p")
            extracted_text = ""
            for paragraph in paragraphs:
                text = paragraph.get_text(strip=True)
                if text:
                    extracted_text += text + "\n"
                    if len(extracted_text) > 200:
                        break
            return extracted_text.strip()
        else:
            return None
    except Exception as e:
        print("Error:", e)
        GPIO.output(12, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(12, GPIO.LOW)
        return None

def speak_text(text, rate=125):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()

def answer_question(question):
    query = f"{question} site:wikipedia.org"
    try:
        search_results = search(query, num_results=1)
        for result in search_results:
            extracted_info = extract_information(result)
            if extracted_info:
                print("Extracted info:")
                GPIO.output(12, GPIO.HIGH)
                GPIO.output(12, GPIO.LOW)
                print(extracted_info)
                speak_text(extracted_info)
                return
        print("No relevant information found.")
    except Exception as e:
        print("Error:", e)

speak_text("Hey! Ask me anything.")
GPIO.output(14, GPIO.HIGH)
GPIO.output(15, GPIO.LOW)
GPIO.output(18, GPIO.HIGH)
GPIO.output(25, GPIO.HIGH)
GPIO.output(7, GPIO.LOW)
GPIO.output(8, GPIO.HIGH)
time.sleep(1)
GPIO.output(14, GPIO.HIGH)
GPIO.output(15, GPIO.HIGH)
GPIO.output(18, GPIO.LOW)
GPIO.output(25, GPIO.HIGH)
GPIO.output(8, GPIO.LOW)
GPIO.output(7, GPIO.HIGH)
time.sleep(2)
GPIO.output(14, GPIO.HIGH)
GPIO.output(15, GPIO.LOW)
GPIO.output(18, GPIO.HIGH)
GPIO.output(25, GPIO.HIGH)
GPIO.output(7, GPIO.LOW)
GPIO.output(8, GPIO.HIGH)
time.sleep(1)
GPIO.output(14, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(18, GPIO.LOW)
GPIO.output(25, GPIO.LOW)
GPIO.output(7, GPIO.LOW)
GPIO.output(8, GPIO.LOW)
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    elif user_input.lower() == "bye":
        break


    answer_question(user_input)
