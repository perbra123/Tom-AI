from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pyttsx3

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
                print(extracted_info)
                speak_text(extracted_info)
                return
        print("No relevant information found.")
    except Exception as e:
        print("Error:", e)

speak_text("Hey! Ask me anything.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    answer_question(user_input)
