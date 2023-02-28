import logging
import os
import pickle
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread, Event
from files import idle_prime, keygen, save_image
from tkinter.filedialog import askdirectory
from chaotic_source import Random


LARGEFONT = ("Verdana", 80)


class Gui(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        # creating a container
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, SSH, Chat, Collector, Rand):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="CameRAND", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=2, column=1, columnspan=3, pady=130, padx=50)

        button1 = ttk.Button(self, text="\n\nSSH Client\n\n",
                             command=lambda: controller.show_frame(SSH),
                             width=20)

        # putting the button in its place by
        # using grid
        button1.grid(row=5, column=1, padx=45, pady=10)

        # button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="\n\nRNG\n\n",
                             command=lambda: controller.show_frame(Rand),
                             width=20)

        # putting the button in its place by
        # using grid
        button2.grid(row=5, column=2, padx=45, pady=10)

        button2 = ttk.Button(self, text="\n\nChat Client\n\n",
                             command=lambda: controller.show_frame(Chat),
                             width=20)

        # putting the button in its place by
        # using grid
        button2.grid(row=5, column=3, padx=45, pady=10)


# second window frame page1
class SSH(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.path_info = ""
        label1 = ttk.Label(self, text="SSH", font=("Verdana", 40))
        label1.place(x=1050, y=0)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.place(x=10, y=10, height=150, width=200)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text="Generate Primes\n in Background...",
                             command=lambda: controller.show_frame(Collector))

        # putting the button in its place by
        # using grid
        button2.place(x=0, y=500, height=175, width=250)

        label2 = ttk.Label(self, text="Select Directory:", style='TButton')
        label2.place(y=170, x=400, width=400, height=75)

        self.button = ttk.Button(self, text="Dir...",
                                 command=lambda: self.get_dir())
        self.button.place(y=250, height=50, x=450, width=300)

        button3 = ttk.Button(self, text="Generate", style='Large.TButton',
                             command=lambda: keygen(self.path_info))
        button3.place(y=350, height=200, x=350, width=500)

    def get_dir(self):
        self.path_info = askdirectory()
        dirname = "Dir: " + self.path_info.split("/")[-1]
        self.button.configure(text=dirname)


# third window frame page2
class Collector(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._done = Event()
        self._coll = None
        label = ttk.Label(self, text="Beep Boop!\nCollecting...", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=80)

        # button to show frame 3 with text
        # layout3
        button1 = ttk.Button(self, text="\n Start Collector \n",
                             command=lambda: self.start())

        # putting the button in its place by
        # using grid
        button1.grid(row=2, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="\n Stop Collector \n",
                             command=lambda: self.stop(controller))

        # putting the button in its place by
        # using grid
        button2.grid(row=3, column=1, padx=10, pady=10)

    def start(self):
        self._coll = Thread(target=idle_prime, args=(self._done,))
        self._coll.start()

    def stop(self, controller):
        self._done.set()
        self._coll.join()
        controller.show_frame(SSH)


class Rand(tk.Frame):
    def __init__(self, parent, controller: Gui):
        tk.Frame.__init__(self, parent)
        self.random = Random()
        self.random.pause()
        label1 = ttk.Label(self, text="RNG", font=("Verdana", 40))
        label1.place(x=1050, y=0)

        button1 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.place(x=10, y=10, height=150, width=200)

        sep = ttk.Separator(self, orient="vertical")
        sep.place(x=596, y=0, height=675, width=8)

        self.startval = tk.StringVar()
        self.startval.set("Start:")
        self.endval = tk.StringVar()
        self.endval.set("End:")

        start = ttk.Entry(self, textvariable=self.startval, style='TButton')
        start.place(x=130, y=170, height=50, width=400)

        end = ttk.Entry(self, textvariable=self.endval, style='TButton')
        end.place(x=130, y=230, height=50, width=400)

        button2 = ttk.Button(self, text="Generate integer",
                             command=lambda: self.generate())
        button2.place(x=130, y=300, height=50, width=400)
        self.resultval = "0"
        self.result = ttk.Button(self, text="Number: ",
                                 command=lambda: self.copy_val(controller))
        self.result.place(x=130, y=450, height=60, width=400)

        self.img = None
        self.image = ttk.Label(self, style='TButton')
        self.image.place(x=765, y=100, width=270, height=270)

        button3 = ttk.Button(self, text="Generate Random Image",
                             command=lambda: self.gen_image(), style='Small.TButton')
        button3.place(x=765, y=415, width=270, height=60)

        button4 = ttk.Button(self, text="Save...",
                             command=lambda: save_image('temp.png'))
        button4.place(x=825, y=500, width=150, height=60)

    def generate(self):
        self.random.cont()
        start = self.startval.get().split(":")[-1]
        end = self.endval.get().split(":")[-1]
        if not (start.isnumeric() and end.isnumeric() and int(start) < int(end)):
            val = "Invalid start/end"
        else:
            val = self.random.get_int_range(int(start), int(end) - 1)
        self.resultval = str(val)
        self.result.configure(text=("Number: " + str(val)))
        self.random.pause()

    def copy_val(self, gui: Gui):
        gui.clipboard_clear()
        gui.clipboard_append(self.resultval)
        self.result.configure(text="Copied to clipboard")
        gui.update()
        time.sleep(0.3)
        self.result.configure(text=("Number: " + self.resultval))
        gui.update()

    def gen_image(self):
        self.random.cont()
        self.random.rand_pic("temp.png")
        self.img = tk.PhotoImage(file="temp.png")
        self.image.configure(image=self.img)
        self.random.pause()



class Chat(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(SSH))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row=2, column=1, padx=10, pady=10)


def style():
    s = ttk.Style()
    s.configure('.', font=('Helvetica', 20))
    s.configure('TButton', background="#000000")
    s.configure(style='Large.TButton', font=('Helvetica', 40))
    s.configure(style='Small.TButton', font=('Helvetica', 12))


def main():
    if not os.path.exists("primes.bin"):
        with open("primes.bin", "wb") as file:
            pickle.dump([], file)
    app = Gui()
    app.minsize(1200, 675)
    app.maxsize(1200, 675)
    style()
    app.mainloop()


# Driver Code
if __name__ == '__main__':
    logging.basicConfig(filename="rsagen.log", level=logging.DEBUG)
    main()
