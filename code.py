import pyttsx3                                #pip install pyttsx3
import speech_recognition as sr               #pip install SpeechRecognition #pip install PyAudio #pip install setuptools
import os                                     
import webbrowser                             
import subprocess                             
import datetime                               
import wikipedia                              #pip install wikipedia
import requests                               #no need to install anything #allows us to use external APIs #openweatherorg    
from bs4 import BeautifulSoup                 #pip install beautifulsoup4
from freeGPT import Client                    

engine = pyttsx3.init()         #instance of pyttsx3
engine.setProperty('rate', 150) #to set the speed rate

#TEXT TO SPEECH
def say(text) :
    print(f"🤖: {text}")
    engine.say(text)
    engine.runAndWait()


#SPEECH TO TEXT
def takeCommand() :
    r = sr.Recognizer()
    while 1 :
        with sr.Microphone() as source :
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            say("I am Listening...")
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio)
                print("👨:", end = " "), print(query)
                return query
            except Exception as e:
                r = sr.Recognizer()
                continue





if __name__ == '__main__':
    say("Hello I am Aura AI")

    while 1:
        query = takeCommand()       #if voice input is working use this line

        #say("I am listening...")      #if voice is not working
        #query = input(f"👨: ")       #use these two lines

        #interacting with webbroweser
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"], ]
        if "Open".lower() in query.lower():
            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])

        elif "google" in query.lower():
            say("web search for the same has been opened in browser")
            URL = "https://www.google.co.in/search?q=" + query
            webbrowser.open(URL)
        elif "image" in query.lower() or "picture" in query.lower():
            say("web search for the same has been opened in browser")
            URL = "https://yandex.com/images/search?text=" + query
            webbrowser.open(URL)

        #using datetime module
        elif "time".lower() in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} {min}")

        #Weather information
        elif "weather".lower() in query.lower():
            str = ""
            i = query.find("of")
            i += 3
            while i < len(query):
                str += query[i]
                i = i+1
            cityname = str
            #print(cityname)
            say("wait a moment....")
            weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&units=imperial&APPID={"253682c0bd759acfb4255d4aa08c3dd7"}")
            data = weather_data.json()
            main = data['main']
            temperature = main['temp']
            humidity = main['humidity']
            pressure = main['pressure']
            say(f"temperature is {round((temperature-32)*5/9, 2)}°C")
            say(f"humidity is {humidity}%")
            say(f"pressure is {pressure}hPa")

        #Using Beautiful Soup for WebScrapping
        elif "who".lower() in query.lower() or "what".lower() in query.lower():
            URL = "https://www.google.co.in/search?q=" + query
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57'
            }
            page = requests.get(URL, headers=headers)  #page is the json response
            soup = BeautifulSoup(page.content, 'html.parser')  #soup is the parse tree
            results = soup.find_all(class_='Z0LcW') #if answer is not in one word class Z0LcW will return None  #find_all to search in this parse tree
            if results:
                for result in results:
                    say(result.get_text())
            else:
                prompt = query
                try:
                    resp = Client.create_completion("gpt3", prompt)
                    say(resp)
                except Exception as e:
                    say("Unable to fetch the response sorry for incovenience")

        #interacting with operating system features
        elif "shutdown" in query.lower() or "shut down" in query.lower():
                say("are you sure")
                #temp = takeCommand()
                temp = input()
                if "y" in temp.lower() or "Y" in temp.lower():
                    say("Thanks for talking to me")
                    say("Immediate shutdown taking place")
                    os.system("shutdown /s /t 5")
                    say("exiting myself now")
                    exit()
                else:
                    say("I'm ready to talk to you again !!")
        elif "open calculator".lower() in query.lower():
            say("Opening Calculator")
            subprocess.Popen("C:\\Windows\\System32\\calc.exe")

        #using wikipedia
        elif "tell me about".lower() in query.lower():
            str = ""
            i = query.find("about")
            i += 6
            while i < len(query):
                str += query[i]
                i = i+1

            # print(str)
            temp = str
            say("wait gathering information....")
            result = wikipedia.summary(temp)
            say(result)

        elif "Quit".lower() in query.lower() or "Bye".lower() in query.lower():
            say("thanks for using me... wishing you a good day ahead")
            exit()
        else:
            prompt = query
            try:
                resp = Client.create_completion("gpt3", prompt)
                say(resp)
            except Exception as e:
                say("Unable to fetch the response sorry for incovenience")