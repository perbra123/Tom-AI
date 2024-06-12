from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pyttsx3

def extract_information(url):
 try:
  response=requests.get(url)
  if response.status_code==200:
   soup=BeautifulSoup(response.content,"html.parser")
   paragraphs=soup.find_all("p")
   print("Extracted info:")
   extracted_text = " "
   for paragraph in paragraphs:
    text=paragraph.text.strip()
    if text:
     extracted_text+=text+"\n"
     if len(text)>60:
      break
     print(extracted_text)
   else:
      print(f"failed:", response.status_code)
      return False
 except:
   print("error:")
   return False
 return True

def speak_text(text, rate=150):
 engine=pyttsx3.init()
 engine.setProperty("rate", rate)
 engine.say(text)
 engine.runAndWait()

def answer_question(question):
 query=f"{question}"
 try:
  search_results=search(query, num_results=2)
  for result in search_results:
   print("here:")
   if extract_information(result):
    return
   print("error. trying next url.")
  print("error")
 except Exception as e:
  print("error", str(e))

speak_text("hey")
while True:
 user_input=input("You:")
 if user_input.lower()=="exit":
   print("bye")
   break
 answer_question(user_input)
