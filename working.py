import pyttsx3
import datetime
from datetime import datetime as dt
import time
import speech_recognition as sr
import turtle
from gtts import gTTS
import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import random
import requests 
from bs4 import BeautifulSoup
import wikipedia
import webbrowser
import pywhatkit as kit
import pyautogui
import instaloader
import getpass
import sys
import taskkill
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtCore import QObject, QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui, QtWidgets
from game import Ui_game






disease_data = {
    "cold": {
        "info": "The common cold is a viral infection of your nose and throat (upper respiratory tract).",
        "medication": "Over-the-counter cold medications such as decongestants, antihistamines, and pain relievers may help relieve symptoms."
    },
    "flu": {
        "info": "Influenza, commonly known as the flu, is a contagious respiratory illness caused by influenza viruses.",
        "medication": "Antiviral drugs may be prescribed to treat the flu. Over-the-counter medications can help relieve symptoms."
    },
    "headache": {
         "info":       "A headache is pain or discomfort in the head or face area. Types of headaches include migraine, tension, and cluster. Headaches can be primary or secondary."
                       "If it is secondary, it is caused by another condition.",
         "medication": "The main medicines for tension headaches are simple pain relieving medicines. These include paracetamol."
                       "aspirin and non-steroidal anti-inflammatory drugs (NSAIDs) such as ibuprofen."
    },
    # Add more diseases and their information here
}

def get_disease_input():
    speak("can you specify the disease you are facing. You can speak or type the disease name. Down below")
    print("Assistant: Please specify the disease you are facing. You can speak or type the disease name.")
    choice = input("Enter '1' for voice input, '2' for text input: ")
    if choice == '1':
        return recognize_speech()
    elif choice == '2':
        return input("Enter the disease name: ").lower()
    else:
        return "Invalid choice. Please try again."

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Assistant: Please state the disease you are facing.")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return "Sorry, I could not understand what you said."
        except sr.RequestError:
            return "Sorry, there was an error with the service."

def diagnose_disease(query):
    for disease, data in disease_data.items():
        if disease in query:
            return data["info"], data["medication"]
    return "I'm sorry, I couldn't recognize the disease.", ""




class VoiceChanger:
    def __init__(self, engine):
        self.engine = engine

    def change_voice(self, gender):
        voices = self.engine.getProperty('voices')


        if gender.lower() == 'male':
            self.engine.setProperty('voice', voices[0].id)
        elif gender.lower() == 'female':
            self.engine.setProperty('voice', voices[1].id)
        else:
            print("Invalid gender. Please choose 'male' or 'female'.")



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices');
#selected_voice = 1
#engine.setProperty('voice', voices[selected_voice].id)
engine.setProperty('voices', voices[len(voices) - 1].id)
engine.runAndWait()

voice_changer = VoiceChanger(engine)


# Load the trained model
model = load_model("C:/Users/Shubham/Desktop/AndroidGui/asl_model.h5")

# Define the class labels
class_labels = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to preprocess the input frame
def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (64, 64))
    normalized_frame = resized_frame / 255.0
    expanded_frame = np.expand_dims(normalized_frame, axis=0)
    return expanded_frame

# Function to recognize hand gestures and speak out the detected gesture
def recognize_gestures():
    # Open camera
    cap = cv2.VideoCapture(0)

    # Check if camera is opened
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    # Variable to store time of the last speech output
    last_speech_time = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame is successfully captured
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Preprocess frame
        preprocessed_frame = preprocess_frame(frame)

        # Make prediction
        prediction = model.predict(preprocessed_frame)
        predicted_class = class_labels[np.argmax(prediction)]

        # Display prediction
        cv2.putText(frame, predicted_class, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Sign Language Detection', frame)

        # Check if it's been at least 2 seconds since the last speech output
        current_time = cv2.getTickCount()
        if current_time - last_speech_time > 2 * cv2.getTickFrequency():
            # Speak out the detected gesture
            engine.say(predicted_class)
            engine.runAndWait()
            last_speech_time = current_time

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()



def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()




def take_password():
    # Function to take password input
    speak("Please enter the password to unlock the assistant:")
    password = getpass.getpass("Enter Password: ")
    return password


def set_password():
    # Function to set a new password
    speak("Please set a new password for the assistant:")
    password = getpass.getpass("Set Password: ")
    with open("password.txt", "w") as f:
        f.write(password)
    speak("Password set successfully.")
    

def lock_assistant():
    # Function to lock the assistant
    password = take_password()
    with open("password.txt", "r") as f:
        stored_password = f.read().strip()

    if password == stored_password:
        speak("Assistant unlocked.")
        return False
    else:
        speak("Incorrect password. Please try again.")
        return True

def unlock_assistant():
    # Function to unlock the assistant
    password = take_password()
    with open("password.txt", "r") as f:
        stored_password = f.read().strip()

    if password == stored_password:
        speak("Assistant already unlocked.")
    else:
        speak("Incorrect password. The assistant is still locked.")



def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time




def tellDay():
     
   day = datetime.datetime.today().weekday() + 1
     
   Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
                4: 'Thursday', 5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
     
   if day in Day_dict.keys():
      day_of_the_week = Day_dict[day]
      print(day_of_the_week)
      speak("The day is " + day_of_the_week)
      #speak("do you have any plan today..")
      #speak("i like to help if need to be..")



def tellMonth():
     
   month = datetime.datetime.today().month + 0
     
   Month_dict = {1: 'January', 2: 'February', 3: 'March',
                  4: 'April', 5: 'May', 6: 'June',
                  7: 'July', 8: 'August', 9: 'September', 10: 'Octomber',
                  11: 'November', 12:'December'}
     
   if month in Month_dict.keys():
      day_of_the_month = Month_dict[month]
      print(day_of_the_month)
      speak("The month is " + day_of_the_month)



def sing_a_song_a():

    song_lyrics ="""
    By myself sometimes.
    To give my mind some space.
    Yeah, I know, yeah, I know that it hurts,
    """

    language_code = 'en'
    tts = gTTS(text=song_lyrics, lang=language_code, slow=False)
    tts.save("assistant_song.mp3")
    os.system("start assistant_song.mp3")



def sing_song():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 180)  # Speed of speech

    # Text to be singing
    song_lyrics = [
        "I'm a little teapot, short and stout",
        "Here is my handle, here is my spout",
        "When I get all steamed up, hear me shout",
        "Tip me over and pour me out"
    ]

    # Sing each line of the song
    for line in song_lyrics:
        engine.say(line)
        engine.runAndWait()
        time.sleep(1)  # Pause between lines

    # Close the text-to-speech engine
    #engine.stop()
        


def draw_attractive_design2():
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    pen = turtle.Turtle()
    pen.speed(10)
    turtle.bgcolor("black")  
    pen.pensize(2)

    initial_size = 30  

    for i in range(200):
        pen.color(colors[i % 6])
        pen.forward(initial_size + i)
        pen.left(59)

    pen.hideturtle()


def exit_drawing_window():
    turtle.bye()
    speak("Exiting the drawing window..")





def start_drawing():
    turtle.setup(width=600, height=500)
    turtle.reset()
    turtle.hideturtle()
    turtle.speed(0)
    turtle.bgcolor('black')

    c = 0
    x = 0

    colors = [

        (1.00, 0.00, 0.00),(1.00, 0.03, 0.00),(1.00, 0.05, 0.00),(1.00, 0.07, 0.00),(1.00, 0.10, 0.00),(1.00, 0.12, 0.00),(1.00, 0.15, 0.00),(1.00, 0.17, 0.00),(1.00, 0.20, 0.00),(1.00, 0.23, 0.00),(1.00, 0.25, 0.00),(1.00, 0.28, 0.00),(1.00, 0.30, 0.00),(1.00, 0.33, 0.00),(1.00, 0.35, 0.00),(1.00, 0.38, 0.00),(1.00, 0.40, 0.00),(1.00, 0.42, 0.00),(1.00, 0.45, 0.00),(1.00, 0.47, 0.00),
#orangey colors
        (1.00, 0.50, 0.00),(1.00, 0.53, 0.00),(1.00, 0.55, 0.00),(1.00, 0.57, 0.00),(1.00, 0.60, 0.00),(1.00, 0.62, 0.00),(1.00, 0.65, 0.00),(1.00, 0.68, 0.00),(1.00, 0.70, 0.00),(1.00, 0.72, 0.00),(1.00, 0.75, 0.00),(1.00, 0.78, 0.00),(1.00, 0.80, 0.00),(1.00, 0.82, 0.00),(1.00, 0.85, 0.00),(1.00, 0.88, 0.00),(1.00, 0.90, 0.00),(1.00, 0.93, 0.00),(1.00, 0.95, 0.00),(1.00, 0.97, 0.00),
#yellowy colors
        (1.00, 1.00, 0.00),(0.95, 1.00, 0.00),(0.90, 1.00, 0.00),(0.85, 1.00, 0.00),(0.80, 1.00, 0.00),(0.75, 1.00, 0.00),(0.70, 1.00, 0.00),(0.65, 1.00, 0.00),(0.60, 1.00, 0.00),(0.55, 1.00, 0.00),(0.50, 1.00, 0.00),(0.45, 1.00, 0.00),(0.40, 1.00, 0.00),(0.35, 1.00, 0.00),(0.30, 1.00, 0.00),(0.25, 1.00, 0.00),(0.20, 1.00, 0.00),(0.15, 1.00, 0.00),(0.10, 1.00, 0.00),(0.05, 1.00, 0.00),
#greenish colors
        (0.00, 1.00, 0.00),(0.00, 0.95, 0.05),(0.00, 0.90, 0.10),(0.00, 0.85, 0.15),(0.00, 0.80, 0.20),(0.00, 0.75, 0.25),(0.00, 0.70, 0.30),(0.00, 0.65, 0.35),(0.00, 0.60, 0.40),(0.00, 0.55, 0.45),(0.00, 0.50, 0.50),(0.00, 0.45, 0.55),(0.00, 0.40, 0.60),(0.00, 0.35, 0.65),(0.00, 0.30, 0.70),(0.00, 0.25, 0.75),(0.00, 0.20, 0.80),(0.00, 0.15, 0.85),(0.00, 0.10, 0.90),(0.00, 0.05, 0.95),
#blueish colors
        (0.00, 0.00, 1.00),(0.05, 0.00, 1.00),(0.10, 0.00, 1.00),(0.15, 0.00, 1.00),(0.20, 0.00, 1.00),(0.25, 0.00, 1.00),(0.30, 0.00, 1.00),(0.35, 0.00, 1.00),(0.40, 0.00, 1.00),(0.45, 0.00, 1.00),(0.50, 0.00, 1.00),(0.55, 0.00, 1.00),(0.60, 0.00, 1.00),(0.65, 0.00, 1.00),(0.70, 0.00, 1.00),(0.75, 0.00, 1.00),(0.80, 0.00, 1.00),(0.85, 0.00, 1.00),(0.90, 0.00, 1.00),(0.95, 0.00, 1.00)
       
    ]

    while x < 1000:
        idx = int(c)
        color = colors[idx]
        turtle.color(color)
        turtle.forward(x)
        turtle.right(98)
        x = x + 1
        c = c + 0.1
    #turtle.done()

def exit_drawing_window():
    turtle.bye()
    speak("Existing the Drawing window....")




        

def sing1_song():
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 180)  # Speed of speech

    # Text to be sung
    song_lyrics = [
        "chippi chippi chapa chapa",
        "Llegó el chaparro mejorando el swing"
        "A lo tranquilin el sonido clean"
        "Sin fin para ti para mí pa la mami"
        "De costa costa de Cancún a miami",
        "chippi chippi chappa chappa ruby ruby rabba rabba",
        "Tip me over and pour me out"
    ]

    # Sing each line of the song
    for line in song_lyrics:
        engine.say(line)
        engine.runAndWait()
        time.sleep(1)  # Pause between lines

    # Close the text-to-speech engine
    #engine.stop()
        




def wish():
   #year = int(datetime.datetime.now().year)
   #month = int(datetime.datetime.now().month)
   #date = int(datetime.datetime.now().day)
   hour = int(datetime.datetime.now().hour)
   #speak(date)
   #speak(month)
   #speak(year)
   tt = time.strftime("%I. And %M minutes, %S seconds %p:")
   tt1 = time.strftime("%B : %D :")



   if hour >= 0 and hour <= 12:
      speak("Good Moring ,I am Android 2 Point O.")
      #speak("Good To see YOu")
      #speak(f"The Current Time is {tt}!")
      #speak(f"the current month and date is.{tt1}!...")

   elif hour >= 12 and hour <= 18:
      speak("Good AfterNoon, I am Android 2 Point O.")
      #speak("Glad To be With You Today..")
      #speak(f"The current Time Is {tt}!.")
      #speak(f"the current month and date is. {tt1}!...")
      #speak("The cUrrent Date is!")
      #speak(date)
      #speak(month)
      #speak(year)
   else:
      speak(f"Good Evening.....its, {tt}")
      speak("Hey How You Doing")
      #speak(f"How Can i help You..., {tt}")
   speak("How may i help you..!")




def object_detection():
    #image_path = 'room.jpg'
    prototxt_path = 'C:\\Users\\Shubham\\Desktop\\dectection\\MobileNetSSD_deploy.prototxt'
    model_path = 'C:\\Users\\Shubham\\Desktop\\dectection\\MobileNetSSD_deploy.caffemodel'

    min_confidence = 0.2

    classes = ["background","monitor","specs","sheep",
               "chair", "bottle","person", "people","bus","pc"
               "cellphone","tvmonitor","glasses","car","face",
               "train", "mobile", "flowepot", "carpet","tv",
               "flowepot", "carpet","cup"]

    np.random.seed(543210)
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    cap = cv2.VideoCapture(0)

    while True:
        _, image = cap.read()
        height, width = image.shape[0], image.shape[1]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130)

        net.setInput(blob)
        detected_objects = net.forward()

        for i in range(detected_objects.shape[2]):
            confidence = detected_objects[0][0][i][2]

            if confidence > min_confidence:
                class_index = int(detected_objects[0, 0, i, 1])
                upper_left_x = int(detected_objects[0, 0, i, 3] * width)
                upper_left_y = int(detected_objects[0, 0, i, 4] * height)
                lower_right_x = int(detected_objects[0, 0, i, 5] * width)
                lower_right_y = int(detected_objects[0, 0, i, 6] * height)

                prediction_text = f"{classes[class_index]}: {confidence:.2f}%"
                cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[class_index], 3)
                cv2.putText(image, prediction_text, (upper_left_x, upper_left_y - 15 if upper_left_y > 30 else upper_left_y + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)

        cv2.imshow("Detected Objects", image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break;

    cap.release()
    cv2.destroyAllWindows()





def get_user_input(question):
    return input(question + " ")



def predict_future():
    print("Welcome to the Future Predictor!")
    name = get_user_input("What is your name : ")
    age = get_user_input("How old are you: ")
    color = get_user_input("What is your favorite color: ")
    animal = get_user_input("Pick an animal you like: ")
    number = get_user_input("Choose a number between 1 and 10: ")

    # Generate a random response
    predictions = [
        "You will discover a new passion in the coming months!",
        "Unexpected opportunities will lead to success!",
        "Take a moment to appreciate the small things in life.",
        "Adventure awaits you in the near future!",
        "Embrace change; it will bring positive outcomes."
    ]


    print("\nHere's your future prediction, {}:".format(name))
    print(random.choice(predictions))



def calculate_math_expression(expression):
    try:
        result = eval(expression)
        speak(f"The result of {expression} is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that. Please provide a valid mathematical expression.")
        print(f"Error: {e}")





class MainThread(QThread):
   def __init__(self):
      super(MainThread,self).__init__()

   def run(self):
      self.TaskExecution()


   def take_password(self):
       take_password()


   def set_password(self):
       set_password()

   def lock_assistant(self):
       return lock_assistant()
   
   def unlock_assistant(self):
       unlock_assistant()


   def exit_application(self):
       speak("Exiting the application. You may have great day..")
       sys.exit()

   def clear_screen(self):
       os.system('cls' if os.name == 'nt' else 'clear')
       speak("Screen cleared.")

    


   def set_alarm(self):
    while True:
       speak("How would you like to set the alarm? You can tell me the time in HH:MM AM/PM format.")
       time_input = self.takecommand()

       if time_input.lower() == 'cancel':
           print("Alarm setting canceled..")
           break

       try:
            alarm_time = datetime.datetime.strptime(time_input, "%I:%M %p")
       except ValueError:
            speak("Invalid time format. Please use HH:MM AM/PM.")
            continue
            #return

       current_datetime = datetime.datetime.now()
       alarm_datetime = datetime.datetime(current_datetime.year, current_datetime.month, current_datetime.day,
                                           alarm_time.hour, alarm_time.minute)
       time_difference = (alarm_datetime - current_datetime).total_seconds()

       if time_difference <= 0:
          speak("Invalid time. Please choose a future time.")
       else:
          speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}. Waiting for the specified time before notifying...")

        # Wait for the specified time before notifying
          time.sleep(int(time_difference))

        # Notify through voice
          engine = pyttsx3.init()
          engine.say("Time to wake up....!")
          engine.runAndWait()
          break





   def takecommand(self):
      
    try:
      
      r = sr.Recognizer()
      with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=4, phrase_time_limit=11)
    except Exception as e:
        speak("error detected in the file..")
        speak("Error detected in the audio input. Please provide the command in written text.")
        speak("completed")
        return input("Enter Your Command: ")
        #return "none"
      
    try:
       print("Recognizing......")
       query = r.recognize_google(audio, language='en-in')
       print(f"your commnad: {query}\n")


    except Exception as e :
        print(e)
        #speak("Can you reapeat that again please..")
        #return "none"
        return input("Enter your Command: ")
    query = query.lower()
    return query
   

   

   #if __name__ == "__main__":
   def TaskExecution(self):
       wish()
       while True:
            self.query = self.takecommand()
            
            if "open chrome" in self.query:
               speak("Openning Google Chrome..")
               npath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" 
               os.startfile(npath)

            elif "close chrome" in self.query:
                speak("Closing google chrome..")
                os.system(f"taskkill /im chrome.exe /f")


            elif "open word doc" in self.query:
                speak("Openning Word Document..")
                upath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                os.startfile(upath)

            elif "close word doc" in self.query:
                speak("Here I go, Closing Power Point")
                os.system(f"taskkill /im WINWORD.EXE /f")


            elif "open excel sheet" in self.query:
                speak("Openning Excel sheet...")
                zpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
                os.startfile(zpath)
            
            elif "close excel sheet" in self.query:
                speak("Here I go, Closing Power Point")
                os.system(f"taskkill /im EXCEL.EXE /f")


            elif 'change voice' in self.query:
                gender = 'male' if 'male' in self.query else 'female'
                voice_changer.change_voice(gender)
                engine.say(f"Voice changed to {gender}. How can I assist you?")
                engine.runAndWait()


            elif "open powerpoint" in self.query:
                speak("Opening Power Point..")
                xpath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"
                os.startfile(xpath)


            elif "close powerpoint" in self.query:
                speak("Here I go, Closing Power Point")
                os.system(f"taskkill /im POWERPNT.EXE /f")


            elif "minimise the window" in self.query:
                pyautogui.hotkey("winleft", "down")  # Minimize the window
                speak("Minimizing the window...")

            elif "maximize the window" in self.query:
                pyautogui.hotkey("winleft", "up")  # Maximize the window
                speak("Maximizing the window...")


            elif " recognise gestures" in self.query:
                speak("Recognizing. Guestures using camera here i go..")
                recognize_gestures()



            elif "cure disease" in self.query:
                disease_query = get_disease_input()
                print("You specified:", disease_query)
                if 'exit' in disease_query:
                    break
                disease_info, medication = diagnose_disease(disease_query)
                response = f"{disease_info} For this condition, the recommended medication is: {medication}"
                print(response)
                speak(response)



            elif "draw a design" in self.query:
                speak("Drawing an attractive design for you.")
                draw_attractive_design2()

            elif "exit the window" in self.query:
                speak("existing the turtle window")
                exit_drawing_window()


            elif "start drawing" in self.query:
                speak("drawing an another attractive design for yaa..")
                start_drawing()

            elif "exit the window two" in self.query:
                speak("exisiting the turtle window Two..")
                exit_drawing_window()


            elif "open note" in self.query:
               speak("Openning Note Pad..")
               apath = "C:\\Windows\\notepad.exe"
               os.startfile(apath)
        
            elif "open command prompt" in self.query:
               speak("openning command prompt..")
               os.system("start cmd")

            
            elif "open camera" in self.query:
               speak("openning Camera..")
               cap = cv2.VideoCapture(0)

               while True:
                  ret, img = cap.read()
                  cv2.imshow('webcam', img)

                  k = cv2.waitKey(50)
                  if k==27 or "exit camera" in self.takecommand().lower():
                     speak("Closing the camera...")
                     cap.release()
                     cv2.destroyAllWindows()
                     break;
               #cap.release()
               #cv2.destroyAllWindows()


            elif "exit camera" in self.query or "close camera" in self.query:
               speak("Closing the camera...")
               cv2.destroyAllWindows()



            elif "play music" in self.query:
                  speak("Playing Music, Hope You will enjoy...")
                  music_dir = "C:\\Users\\Shubham\\Downloads\\Documents\\music"
                  songs = os.listdir(music_dir)
                  #rd = random.choice(songs)
                  for song in songs:
                     if song.endswith('.mp3'):
                        os.startfile(os.path.join(music_dir, song))#rd
                        #os.startfile(os.path.join(music_dir, rd))


            elif "volume up" in self.query:
                pyautogui.press("volumeup")

            elif "volume down" in self.query:
                pyautogui.press("volumedown")

            elif "volume mute" in self.query or "mute" in self.query:
                pyautogui.press("volumemute")
                


            elif "wikipedia" in self.query:
                  speak("searching wikipedia.....")
                  query = query.replace("wikipedia", "")
                  results = wikipedia.summary(query, sentences=2)
                  speak("According to wikipedia..")
                  speak(results)
                  #print(results)

                
                

            elif "show wikipedia" in self.query:
                speak("Searching Wikipedia...")
                query = self.query.replace("wikipedia", "")
                query = query.strip()  # Remove leading and trailing whitespaces
                if query:  # Check if the query is not empty
                    try:
                        results = wikipedia.summary(query, sentences=2)
                        speak("According to Wikipedia...")
                        speak(results)
                        self.ui.textBrowser.setText(results)
                    except wikipedia.exceptions.DisambiguationError as e:
                            speak("Disambiguation error. Please try again.")
                    except wikipedia.exceptions.PageError as e:
                            speak("Page not found. Please try again.")
                    except Exception as e:
                            speak("An error occurred. Please try again.")
                else:
                    speak("Please provide a search term.")






            elif "open youtube" in self.query:
                  speak("Openning YouTube , Here you go...")
                  webbrowser.open("www.youtube.com")

            elif "open google" in self.query:
                  speak("Here I go, What do you want me to serach on google..")
                  cm = self.takecommand().lower()
                  webbrowser.open(f"{cm}")     

            elif "play youtube video" in self.query:
                  speak("playing youtube video...here i go")
                  kit.playonyt("dicovery")


            elif "close note" in self.query:
                speak("Here I go, Closing note test")
                os.system(f"taskkill /im notepad.exe /f")


            elif "tell us temperature" in self.query:
                search = "temperature in mumbai"
                url = f"https://www.google.com/search?q={search}"
                r = requests.get(url)
                data = BeautifulSoup(r.text,"html.parser")
                temp = data.find("div", class_ = "BNeawe").text
                speak(f"current{search} is {temp}")

            

            elif "set alarm" in self.query:
                speak("How would you like to set the alarm? You can tell me the time in HH:MM AM/PM format.")
                tt = self.takecommand()
                tt = tt.replace("set alarm to ", "")
                tt = tt.replace(".","")
                tt = tt.upper()
                import MyAlarm
                MyAlarm.alarm(tt)

                  
            #elif "Can you sing a song for us" in self.query or "sing" in self.query:
                ##speak("Alright i might sond bit funny")
                #speak("here i go, Hope you will like it")
                #sing_song()


            #elif "sing different song for us" in self.query or "sing another song" in self.query:
                #speak("alright here i go Another song")
                #speak("Hope you will enjoy it")
                #sing1_song()
    

            elif "sing a song " in self.query or "can you perform for us" in self.query:
                speak("OHH yea.. i will sure")
                speak("well to be honest im quite nervouse.")
                speak("But here i go..")
                sing_a_song_a()

            
            elif "calculate" in self.query or "do math" in self.query:
               speak("Sure, what mathematical expression would you like me to calculate?")
               math_expression = self.takecommand()
               calculate_math_expression(math_expression)




            elif "what is the day today" in self.query or "day" in self.query:
                tellDay()


            elif "what is the time" in self.query or "tell time" in self.query:
                current_time = get_current_time()
                speak(f"The current time is {current_time}")



            elif "What month is going on" in self.query or "month" in self.query:
                tellMonth()
                 
                 

            elif "show instagram profile" in self.query or "profile on instagram" in self.query:
                speak("Can you Confirm your Username for me please..")
                speak("Enter Your Username Down Below...")
                name = input("Enter Your Username Here:  ")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"Take a look at the profile that you have mentioned {name}")
                time.sleep(5)
                speak("would you like to download profile picture of this account..")
                condition = self.takecommand().lower()
                if "yes" in condition:
                    mod = instaloader.instaloader()
                    mod.download_profile(name, profile_pic_only = True)
                    speak("Profile pic has been downloaded successfully..")
                    speak("it has been saved in the main folder..")
                else:
                    pass
                speak("Alright....")


            elif "who are you" in self.query or "introduce yourself" in self.query:
                    assistant = '''Hello, I am a robot sort of. Your personal Assistant.
                     I am here to make your life easier. You can command me to perform
                     various tasks such as managing your schedule sums or opening applications etcetra'''
                    speak(assistant)


            elif "Whats Programming Language" in self.query or "What do you know about Coding" in self.query:
                    assistant = ''' A programming language is describe by the syntax and semantics.
                     it gets it's basis from formal language. A language usually has at least one implementation,
                     in the form of a compiler or interpreter, allowing programs written in the language to be executed.
                     Programming language theory is the studies of computer science thats studies the design,
                     implementation, analysis, characterization and classification of programming language.'''
                    speak(assistant)


            elif "can you predict my future" in self.query:
                speak("Alright... Let me see Ok. Great!")
                speak("You will have to give few answers of my question.")
                speak("based on that. i will tell you, What your future...would be")
                speak("I hope your ready...")
                predict_future()

            
            elif "start object detection" in self.query:
                speak("Starting object detection. Press 'q' to exit.")
                object_detection()



            elif "set clock" in self.query:
                speak("setting alarm for you...")
                self.set_alarm()


            #elif "check the volume frequency" in self.query:
                #speak("Checking the frequency of the volume")
                #voice_frequency_volume()


            elif "set new password" in self.query:
                speak("Setting new password for you...")
                set_password()


            elif "lock the assistant" in self.query:
                speak("locking the assistant")
                lock_assistant()


            elif "exit" in self.query or "close" in self.query or "goodbye" in self.query:
                self.exit_application()
            

            elif "clear" in self.query or "clear screen" in self.query:
                self.clear_screen()


            elif "no thanks" in self.query or "No question Thanks Im done" in self.query:
                  speak("Good to see that i was able to help you...")
                  speak("have a great day..")
                  sys.exit()

            speak("Anything else You want to Help you With. ")
            #speak("in Case, you goT any question need to be")
            #speak("i'd be really really quick with it...")





if __name__ == "__main__":
    mainExecution = MainThread()
    startExecution = MainThread()

class Main(QMainWindow):
   def __init__(self):
      super().__init__()
      self.ui = Ui_game()
      self.ui.setupUi(self)
      self.ui.pushButton.clicked.connect(self.startTask)
      self.ui.pushButton_2.clicked.connect(self.close)
   def startTask(self):
      self.ui.movie = QtGui.QMovie("C:\\Users\\Shubham\\Desktop\\pics\\backgrunds.gif")
      self.ui.label.setMovie(self.ui.movie)
      self.ui.movie.start()
      self.ui.movie = QtGui.QMovie("C:\\Users\\Shubham\\Desktop\\andro00\\robot.png")
      self.ui.label_2.setMovie(self.ui.movie)
      self.ui.movie.start()
      timer = QTimer(self)
      timer.timeout.connect(self.showTime)
      timer.start(1000)
      #startExecution.start()


   def showTime(self):
      current_time = QTime.currentTime()
      current_date = QDate.currentDate()
      label_time = current_time.toString('hh:mm:ss')
      label_date = current_date.toString(Qt.ISODate)
      self.ui.textBrowser.setText(label_date)
      self.ui.textBrowser_2.setText(label_time)



app = QApplication(sys.argv)
Androoid2O = Main()
Androoid2O.show()
#exit(app.exec_())


if not os.path.isfile("password.txt"):
    mainExecution.set_password()


while mainExecution.lock_assistant():
    pass


startExecution.start()
exit(app.exec_())
   

