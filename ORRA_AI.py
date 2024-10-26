from wsgiref import headers
import sys
import pyttsx3 
import speech_recognition as sr
import datetime
from datetime import date
import wikipedia 
import webbrowser
import os
import subprocess as sp
import pywhatkit
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder
import psutil
from youtubesearchpython import VideosSearch
import threading
import time
import queue
import pyjokes
import tkinter as tk


i = 2

question = "how are you"
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def assistant(assist):
    voices = engine.getProperty('voices')
    if assist == 'ortan':
        engine.setProperty('voice', voices[0].id)
    else: 
        engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...") 
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    except Exception as e:
        return "None"

def LogIn():
    check = 1
    excel_file = 'database.xlsx'
    df = pd.read_excel(excel_file)
    while True:
        name = input("Enter Username: ")
        password = input("Enter the password: ")
        for index, row in df.iterrows():
            if row['Name'] == name and row['Password'] == password:
                global gen
                global assist
                gen = row['Gender']
                assist = row['Assist_Voice']
                check = 2
                assistant(assist)
        if check == 2:
            speak("Login successfully")
            break
        else:
            speak("Invalid Username and Password")

def Registration():
    while True:
        name = input("Enter name: ")
        if " " not in name:
            break
        else:
            print("Invalid name. Please enter a name without spaces.\n")
    while True:
        phone_number = input("Enter phone number: ")
        if len(phone_number) > 10 or len(phone_number) < 10:
            print("Phone number must contain 10 digits\n")
        else:
            break
    gender = input("Enter gender: \n")
    password = input("Enter the Password: \n")
    print("Voices available-: \n ORTAN \n SERA \n")
    assist_voice = input("Enter the voice: ")
    data = {
        'Name': [name],
        'Gender': [gender],
        'Phone Number': [phone_number],
        'Password': [password],
        'Assist_Voice': [assist_voice]
    }
    df = pd.DataFrame(data)
    existing_data = pd.DataFrame()
    excel_file = 'database.xlsx'
    try:
        existing_data = pd.read_excel(excel_file)
    except FileNotFoundError:
        pass
    combined_data = pd.concat([existing_data, df], ignore_index=True)
    combined_data.to_excel(excel_file, index=False)
    
    
def exit_assistant():
    sys.exit()

def start_assistant():
 
    print("press 1 for Log in")
    print("press 2 for Register yourself")
    choice = int(input("ENTER:"))
    if choice == 1:
        LogIn()
    else:
        Registration()
        speak("Registration successfully, Now please log in")
        LogIn()
        
    hour = int(datetime.datetime.now().hour)
    
    
    if gen == "female" or gen =="f" or gen =="Female" or gen =="F": 
        strTime = datetime.datetime.now().strftime("%H:%M")
        if hour >= 0 and hour < 12:
            speak("hello")
            speak(f"Good Morning ma'am!, I am {assist} an your desktop assistant. The time is {strTime}, How may i help you")
        
        elif hour >= 12 and hour < 18:
            speak("hello")
            speak(f"Good Afternoon ma'am!, I am {assist} an your desktop assistant. The time is {strTime}, How may i help you")
        
        else:
            speak("hello")
            speak(f"Good Evening ma'am!, I am {assist} an your desktop assistant. The time is {strTime}, How may i help you")
            
        while True:   
                query = takeCommand().lower()         
                if 'when'  in query:
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("okay ma'am")
                    speak("According to Wikipedia")
                    speak(results)
                    
                elif 'what' in query:
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("okay ma'am")
                    speak("According to Wikipedia")
                    speak(results)
                    
                
                    
                elif 'which' in query:
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("okay ma'am")
                    speak("According to Wikipedia")
                    speak(results)
                    
                elif 'explain' in query or 'why' in query:
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("okay ma'am")
                    speak("According to Wikipedia")
                    speak(results)

                elif 'hello' in query or 'hi' in query :
                    
                    speak("hello ma'am")

                elif question in query:
                    speak('i am fine')

                elif 'play song' in query:
                    Name = ""
                    speak("Which song would you like me to play, ma'am?")
                    Songs = takeCommand()
                    videosSearch = VideosSearch(Songs, limit=1)
                    x = videosSearch.result()
                    url = x['result'][0]['thumbnails'][0]['url']
                    y = url.replace('https://i.ytimg.com/vi/', "")
                    for i in y:
                        if i != '/':
                            Name = Name + i
                        else:
                            break
                    webbrowser.open("https://www.youtube.com/watch?v=" + Name) 

                elif 'camera' in query:
                    sp.run('start microsoft.windows.camera:', shell=True)

                

                elif 'exit the program' in query or 'stop' in query or 'exit' in query:
                    speak("okay ma'am, exiting the program.")
                    sys.exit()                

                elif 'send' in query:
                        df= pd.read_excel(r'F:\ujjwal\code study material\AI\Contacts.xlsx', sheet_name= 'Sheet1')
                        df2= df.set_index('naam')
                        speak("tell me to whom i send message\n")
                        num_ = takeCommand()
                        df1= df2['number'][num_]
                        print(df1)
                        speak("okay now What should I say?")
                        content = takeCommand()
                        pywhatkit.sendwhatmsg_instantly(df1, content, 10, False)
                        r = sr.Recognizer()
                        r.pause_threshold = 5
                        speak('message sent successfully')

                

                elif 'create' in query:
                    f= open("file_1.txt", "w")
                    speak("what to write in the file")
                    crt = takeCommand()
                    a= f.write(crt)
                    speak("file saved successfully")
                    print(a)
                    f.close()

                elif 'find my location' in query or 'location' in query:
                    ip_add= requests.get('https://api.ipify.org').text
                    url = 'https://get.geojs.io/v1/ip/geo/'+ ip_add + '.json'
                    geo_q =requests.get(url)
                    geo_d= geo_q.json()
                    state= geo_d['city']
                    country= geo_d['country']
                    URL1="https://www.google.co.in/maps/place/"+str(state)
                    webbrowser.open(URL1)
                    speak(f"ma'am, You Are Now In {state, country}.")


                elif 'headline' in query:
                    url = 'https://www.indiatoday.in/india'
                    response = requests.get(url)

                    soup = BeautifulSoup(response.text, 'html.parser')
                    headlines = soup.find('body').find_all('h2')
                    for i, x in enumerate(headlines[:5]):  
                        print(x.text.strip())
                        speak(x.text.strip())
                
                elif 'news' in query:
                    url = 'https://www.indiatoday.in/india'
                    response = requests.get(url)

                    soup = BeautifulSoup(response.text, 'html.parser')
                    headlines = soup.find('body').find_all('h2')
                    for i, x in enumerate(headlines[:5]):  
                        print(x.text.strip())
                        speak(x.text.strip())

                elif 'open' in query:
                    a1= query[4:]
                    a2= a1.replace(" ", "")
                    a3= 'https://www.'+a2
                    webbrowser.open(a3)

                elif 'thank you' in query:
                    speak('welcome')
                    
                elif 'bye' in query:
                    break
                
                elif 'joke' in query:
                    speak(pyjokes.get_joke())
                    
                elif "who made you" in query or "who created you" in query:
                    speak("I have been created by Ujjwal Sir.")
     
                elif "" in query:
                    speak("getting in sleep mode")
                    speak("say wake up to wake me up")
                    
                    while True:
                        user=takeCommand()
                        if "wake up" in user:
                            speak("yes ma'am how may i help you")
                            break
                
    elif gen == "male" or gen == "m" or gen == "Male" or gen == "M": 
        strTime = datetime.datetime.now().strftime("%H:%M")
        if hour >= 0 and hour < 12:
            speak("hello")
            speak(f"Good Morning sir!, I am {assist} an your desktop assistant. The time is {strTime}, How may i help you")
            
        elif hour >= 12 and hour < 18:
            speak("hello")
            speak(f"Good Afternoon sir!, I am {assist} an your desktop assistant. The time is {strTime}, How may i help you")
            
        else:
            speak("hello")
            speak(f"Good Evening sir!, I am {assist} an your desktop assistant. The time is {strTime}, How may i help you")
            
        while True:
                query = takeCommand().lower()          
                if 'when' in query: 
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("okay sir")
                    speak("According to Wikipedia")
                    speak(results)
                    
                elif 'what' in query: 
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("okay sir")
                    speak("According to Wikipedia")
                    speak(results)
                    
                
                    
                elif 'which' in query: 
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("okay sir")
                    speak("According to Wikipedia")
                    speak(results)
                    
                elif 'explain' in query: 
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    speak("okay sir")
                    speak("According to Wikipedia")
                    speak(results)

                elif 'hello' in query or 'hi' in query:
                    
                    speak("hello sir")

                elif question in query:
                    speak('i am fine')

                elif 'play song' in query:
                    Name = ""
                    speak("Which song would you like me to play, sir?")
                    Songs = takeCommand()
                    videosSearch = VideosSearch(Songs, limit=1)
                    x = videosSearch.result()
                    url = x['result'][0]['thumbnails'][0]['url']
                    y = url.replace('https://i.ytimg.com/vi/', "")
                    for i in y:
                        if i != '/':
                            Name = Name + i
                        else:
                            break
                    webbrowser.open("https://www.youtube.com/watch?v=" + Name)

                elif 'camera' in query:
                    sp.run('start microsoft.windows.camera:', shell=True)

                

                elif 'send' in query:
                        df= pd.read_excel(r'F:\ujjwal\code study material\AI\Contacts.xlsx', sheet_name= 'Sheet1')
                        df2= df.set_index('naam')
                        speak("tell me to whom i send message\n")
                        num_ = takeCommand()
                        df1= df2['number'][num_]
                        print(df1)
                        speak("okay now What should I say?")
                        content = takeCommand()
                        pywhatkit.sendwhatmsg_instantly(df1, content, 10, False)
                        r = sr.Recognizer()
                        r.pause_threshold = 5
                        speak('message sent successfully')


                elif 'create' in query:
                    f= open("file_1.txt", "w")
                    speak("what to write in the file")
                    crt = takeCommand()
                    a= f.write(crt)
                    speak("file saved successfully")
                    print(a)
                    f.close()

                elif 'find my location' in query or 'location' in query:
                    ip_add= requests.get('https://api.ipify.org').text
                    url = 'https://get.geojs.io/v1/ip/geo/'+ ip_add + '.json'
                    geo_q =requests.get(url)
                    geo_d= geo_q.json()
                    state= geo_d['city']
                    country= geo_d['country']
                    URL1="https://www.google.co.in/maps/place/"+str(state)
                    webbrowser.open(URL1)
                    speak(f"Sir, You Are Now In {state, country}.")

                        
                elif 'headline' in query:
                    url = 'https://www.indiatoday.in/india'
                    response = requests.get(url)

                    soup = BeautifulSoup(response.text, 'html.parser')
                    headlines = soup.find('body').find_all('h2')
                    for i, x in enumerate(headlines[:5]):  
                        print(x.text.strip())
                        speak(x.text.strip())
                
                elif 'news' in query:
                    url = 'https://www.indiatoday.in/india'
                    response = requests.get(url)

                    soup = BeautifulSoup(response.text, 'html.parser')
                    headlines = soup.find('body').find_all('h2')
                    for i, x in enumerate(headlines[:5]):  
                        print(x.text.strip())
                        speak(x.text.strip())

                elif 'open' in query:
                    a1= query[4:]
                    a2= a1.replace(" ", "")
                    a3= 'https://www.'+a2+'.com'
                    webbrowser.open(a3)

                elif 'thank you' in query:
                    speak('welcome')
                
                elif 'exit the program' in query or 'stop' in query or 'exit' in query:
                    speak('okay sir, exiting the program.')
                    sys.exit()
                
                elif 'joke' in query:
                    speak(pyjokes.get_joke())
                 
                elif "who made you" in query or "who created you" in query:
                    speak("I have been created by Ujjwal Sir.")
                    
                elif "" in query:
                    speak("getting in sleep mode")
                    speak("say wake up to wake me up")
                    
                    while True:
                        user=takeCommand()
                        if "wake up" in user:
                            speak("yes sir how may i help you")
                            break
                        
                        
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("700x650")

label = tk.Label(root, text="Welcome to Voice Assistant", font=("Helvetica", 14))
label.pack(pady=10)

label = tk.Label(root, text="Made by uj_dev", font=("Helvetica", 10))
label.pack(pady=10)

start_button = tk.Button(root, text="Start Assistant", command=start_assistant)
start_button.pack()

exit_button = tk.Button(root, text="Exit Assistant", command=exit_assistant)
exit_button.pack()


label = tk.Label(root, text="This assistant can perform the following tasks:", font=("Helvetica", 10))
label.pack(pady=10)





info_text = {
    "Wikipedia": "- Provide information from Wikipedia.\n (e.g., 'Explain me about [topic]')",
    "Greetings": "- Respond to greetings and provide random greetings.",
    "Play song": "- Play music or songs based on user input.\n (e.g., 'Play a song')",
    "Send WhatsApp": "- Send WhatsApp messages.\n (e.g., 'Send a WhatsApp message')",
    "Text File": "- Create and write to a text file. (e.g., 'Create a text file')",
    "Your Location": "- Retrieve and show location information.\n (e.g., 'Find my locaion?')",
    "News": "- Display the latest headlines and news.\n (e.g., 'Tell me the news')",
    "Open Websites": "- Open websites based on user input.\n (e.g., 'Open [website]')",
    "Jokes": "- Share jokes.\n (e.g., 'Tell me a joke')",
    "Creator Info": "- Share information about the creator.\n (e.g., 'Who made you?')",
    "Sleep Mode": "- Enter sleep mode and wake up.\n (e.g., 'Enter sleep mode')",
    "Exit": "- Exit the assistant.\n (e.g., 'Goodbye')"
}

info_visible = {task: False for task in info_text}

def toggle_info_visibility(task):
    global info_visible
    if not info_visible[task]:
        info_label.config(text=info_text[task])
        info_visible[task] = True
    else:
        info_label.config(text="")
        info_visible[task] = False

def show_guide():
    guide = """
    How to interact with the assistant:
    - You can ask questions like:
      - "Tell me about [any topic you want to ask]"
      - "Play a song"
      - "Send a WhatsApp message"
      - "Create a text file"
      - "Ask to find your location"
    - You can say "Thank you" or "Goodbye" to end the interaction.
    """
    info_label.config(text=guide)

for task in info_text:
    task_button = tk.Button(root, text=f" {task} ", command=lambda t=task: toggle_info_visibility(t), font=("Helvetica", 8))
    task_button.pack()

guide_button = tk.Button(root, text="Show User Guide", command=show_guide, font=("Helvetica", 8))
guide_button.pack()

info_label = tk.Label(root, text="", wraplength=250)
info_label.pack()



root.mainloop()
