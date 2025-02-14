import tkinter as tk



class QuickDrawApp:
    def __init__(self,time=20):
        self.conversion = {0: 'aircraft carrier', 1: 'banana', 2: 'barn', 3: 'basket', 4: 'bat', 5: 'bracelet', 6: 'bridge', 7: 'bucket', 8: 'cake', 9: 'cow', 10: 'door', 11: 'drill', 12: 'duck', 13: 'ear', 14: 'elbow', 15: 'envelope', 16: 'eraser', 17: 'face', 18: 'fence', 19: 'fire hydrant', 20: 'floor lamp', 21: 'foot', 22: 'fork', 23: 'garden hose', 24: 'garden', 25: 'golf club', 26: 'grass', 27: 'guitar', 28: 'hamburger', 29: 'hand', 30: 'harp', 31: 'headphones', 32: 'hexagon', 33: 'raccoon', 34: 'saxophone', 35: 'scissors', 36: 'shark', 37: 'snowflake', 38: 'squirrel', 39: 'sun', 40: 'sword', 41: 't-shirt', 42: 'telephone', 43: 'The Mona Lisa', 44: 'toaster', 45: 'traffic light', 46: 'trombone', 47: 'wine glass', 48: 'yoga', 49: 'zigzag'}

        self.root = tk.Tk()

        self.title = tk.Label(self.root, text="Quick Draw",anchor="center", font=("MV Boli",25),bg="#FFD139")
        self.title.place(relx=0.15)

        tk.Label(self.root, text="Your Word is:", anchor="center", font=("Ink Free", 15), bg="#FFD139").place(relx=0.28,y=50)

        self.currentWord = tk.Label(self.root, text="PLACEHOLDER", anchor="center", font=("Ink Free", 18), bg="#FFD139")
        self.currentWord.place(relx=.50,y=100,anchor="center")

        self.canvas = tk.Canvas(self.root, width=256, height=256, bg='white')
        self.canvas.bind('<B1-Motion>', self.__draw)
        self.canvas.place(x=0, rely=0.25)


        self.submit = tk.Button(self.root, text="Submit",font=("Ink Free",14),width=10,bg="#FFD139",relief='solid',command=self.__submit)
        self.submit.place(relx=0.13,rely=0.75)

        self.time=time
        self.timer = tk.Label(self.root,text=self.time,font=("Ink Free",14),bg="#FFD139",relief="raised",width=4)
        self.timer.place(relx=0.70,rely=0.76)

        self.feedback = tk.Label(self.root, text="FEEDBACK", anchor="center", font=("Ink Free", 15), bg="#FFD139")
        self.feedback.place(relx=.50,rely=0.9,anchor="center")

        self.root.geometry('256x550')
        self.root.configure(background="#FFD139")
        self.root.resizable(0,0)
        self.root.mainloop()

    def __submit(self):
        pass

    def __draw(self,x):
        mouseX=x.x
        mouseY=x.y
        self.canvas.create_oval(mouseX-5,mouseY-5,mouseX+5,mouseY+5,fill="black")
        pass

if __name__ == '__main__':
    QuickDrawApp(10)