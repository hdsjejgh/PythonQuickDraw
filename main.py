import os
import tkinter as tk
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' #to get rid of the random warnings TF gives
import tensorflow as tf
import numpy as np
import threading
import random
from time import sleep
from gtts import gTTS
from playsound import playsound
from PIL import Image, ImageTk

class QuickDrawApp:
    def __init__(self,time:int=20):
        self.conversion = {0: 'aircraft carrier', 1: 'banana', 2: 'barn', 3: 'basket', 4: 'bat', 5: 'bracelet', 6: 'bridge', 7: 'bucket', 8: 'cake', 9: 'cow', 10: 'door', 11: 'drill', 12: 'duck', 13: 'ear', 14: 'elbow', 15: 'envelope', 16: 'eraser', 17: 'face', 18: 'fence', 19: 'fire hydrant', 20: 'floor lamp', 21: 'foot', 22: 'fork', 23: 'garden hose', 24: 'garden', 25: 'golf club', 26: 'grass', 27: 'guitar', 28: 'hamburger', 29: 'hand', 30: 'harp', 31: 'headphones', 32: 'hexagon', 33: 'raccoon', 34: 'saxophone', 35: 'scissors', 36: 'shark', 37: 'snowflake', 38: 'squirrel', 39: 'sun', 40: 'sword', 41: 't-shirt', 42: 'telephone', 43: 'The Mona Lisa', 44: 'toaster', 45: 'traffic light', 46: 'trombone', 47: 'wine glass', 48: 'yoga', 49: 'zigzag'} #converts index in probability vector to respective phrase
        self.feedbacks = ("I think its a{prediction}.", "Is it a{prediction}?", "It looks like a{prediction}.", "I see a{prediction}.",) #different feedbacks the Machine gives the user
        self.model = False #stores tensorflow model
        self.time=time #current time
        self.prediction = None #model's prediction
        loadthread = threading.Thread(target=self.__loadModel,daemon=True) #thread for loading model (not sure if it even works??)
        loadthread.start()

        self.__initializeWindow()


    def __loadModel(self):
        self.model = tf.keras.models.load_model('model.keras')
        print("Done")

    def __timer(self):
        while True:
            self.timer.config(text=self.time)
            sleep(1)
            self.time-=1
            if self.time%2 == 0: #every other second, make a guess
                if (p := self.__submit()) != self.prediction:
                    self.prediction = p
                    p = random.choice(self.feedbacks).format(prediction=("n " if p[0] in ('a','e','i','o','u') else ' ')+p) #formats the feeback
                    self.feedback.config(text=p) #sets text as feedback
                    while True: #says the feedback phrase thing
                        try:
                            tts = gTTS(p)
                            os.remove('media/tts.mp3')
                            tts.save('media/tts.mp3')
                            playsound('media/tts.mp3')
                            break
                        except:
                            pass
            if self.time<0: #lose when timer runs out
                self.__lose()
                break

    def __lose(self):
        pass

    def __initializeWindow(self):
        self.root = tk.Tk()
        self.mainframe = tk.Frame(self.root, background="#FFD139", width=256, height=550) #main game screen
        self.mainframe.pack()

        tk.Label(self.mainframe, text="Quick Draw", anchor="center", font=("MV Boli", 25), bg="#FFD139").place(relx=0.15) #title on main frame
        tk.Label(self.mainframe, text="Your Word is:", anchor="center", font=("Ink Free", 15), bg="#FFD139").place(relx=0.28,y=50) #word giver thing on main frame
        self.currentWord = tk.Label(self.mainframe, text="PLACEHOLDER", anchor="center", font=("Ink Free", 18),bg="#FFD139") #actual word
        self.currentWord.place(relx=.50, y=100, anchor="center")

        self.canvas = tk.Canvas(self.mainframe, width=256, height=256, bg='white') #actual drawing canvas
        self.canvas.bind('<B1-Motion>', self.__draw) #draws on canvas
        self.canvas.place(x=0, rely=0.25)

        self.submit = tk.Button(self.mainframe, text="Submit", font=("Ink Free", 12), width=10, bg="#FFD139",relief='solid', command=self.__submit) #submits drawing for prediction button (ill probably remove it)
        self.submit.place(relx=0.1, rely=0.75)

        self.clear = tk.Button(self.mainframe, text="X", font=("Ink Free", 14), width=1, bg="#FFD139", relief='solid',command=self.__clear) #clears canvas
        self.clear.place(relx=0.58, rely=0.75)

        self.timer = tk.Label(self.mainframe, text=self.time, font=("Ink Free", 14), bg="#FFD139", relief="raised",width=4) #timer
        self.timer.place(relx=0.70, rely=0.76)
        timerthread = threading.Thread(target=self.__timer, daemon=True) #thread that manages timer
        timerthread.start()

        self.feedback = tk.Label(self.mainframe, text="FEEDBACK", anchor="center", font=("Ink Free", 15), bg="#FFD139") #feedback given through this label
        self.feedback.place(relx=.50, rely=0.9, anchor="center")


        #title frame (ill add it later)
        #self.titleframe = tk.Frame(self.root, background="#FFD139", width=256, height=550)
        #tk.Label(self.titleframe, text="Quick Draw", anchor="center", font=("MV Boli", 30), bg="#FFD139").place(relx=0.08, rely=0.1)
        #with Image.open('media/logo.png') as img:
        #    resized = img.resize((100, 100))
        #    self.logo = tk.Label(self.titleframe,image=ImageTk.PhotoImage(resized))
        #    self.logo.pack()
        #self.titleframe.pack()


        self.root.geometry('256x550')
        self.root.configure()
        self.root.resizable(0, 0) #no resizing
        self.root.mainloop()

    def __submit(self) -> str:
        self.canvas.postscript(file='media/img.eps') #saves postscript temporarily in media folder
        with Image.open('media/img.eps') as img:
            img.load()
            img = img.convert("L") #makes postscript array greyscale (only 1 value per pixel not 3)
            img = img.resize((28,28)) #resizes (real)

            #img.show()
            img = np.array(img).reshape((1,28,28,1)) #resizes it to the correct input size
            img = 255-img #inverts array (it took me like 40 minutes to figure out why it wasn't working (i forgot to inver it))

            #print((np.array(img).reshape((1,28,28,1)))/255)
            prediction = self.conversion[self.model.predict((img)/255).argmax()] #prediction gotten
        os.remove('media/img.eps') #deletes postscript
        print(prediction)
        return prediction

    def __clear(self):
        self.canvas.delete('all') #jsust clear the canvas


    def __draw(self,x):
        mouseX=x.x
        mouseY=x.y
        self.canvas.create_oval(mouseX-4,mouseY-4,mouseX+4,mouseY+4,fill="black")

if __name__ == '__main__':
    QuickDrawApp(10)