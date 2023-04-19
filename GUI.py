"""
Author: Eitan Unger
Date: 29/02/23
description: A file to build the client GUI
"""
import logging
import os
import pickle
import time
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from threading import Thread, Event
from files import idle_prime, keygen, save_image
from tkinter.filedialog import askdirectory
from chaotic_source import Random, test_camera
from test_client import client_thread

LARGEFONT = ("Verdana", 80)
SERVER = ()


class ChatClient:
    """
    A chat client class for the chat function of the CameRAND app
    """
    def __init__(self, screen, ip, port, name):
        """
        Init method for the chat client
        """
        self.finished = Event()
        self.in_buf = []
        name_f = [name]
        self.window = tk.Toplevel(screen)  # create new screen for the chat
        self.window.minsize(1200, 675)
        self.window.maxsize(1200, 675)
        self.chat = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, font=("Times New Roman", 15))  # chat itself
        self.chat.configure(state="disabled")  # make the chat read only
        # create client (message I/O) thread to handle communications
        self.network_thread = Thread(target=client_thread,
                                     args=((ip, int(port)), name_f, self.finished, self.in_buf, self.chat))
        self.textvar = tk.StringVar()
        # create an entry for writing messages
        self.ent = ttk.Entry(self.window, textvariable=self.textvar, font=("Verdana", 10),
                             validate='key', validatecommand=self.validatecommand)

        # write user data on side for easier use
        info = f"My name: \n%s\n\n\nServer-\n\nip: \n%s\n\nport: \n%s" % (name, ip, port)

        self.data = ttk.Label(self.window, text=info, font=("Verdana", 15))
        self.send_img = tk.PhotoImage(file="send.png")
        self.send_but = ttk.Button(self.window, command=lambda: self.send(), image=self.send_img)  # send button

        self.chat.place(x=200, y=20, width=950, height=600)
        self.ent.place(x=200, y=625, width=900, height=40)
        self.data.place(x=25, y=100, width=150, height=400)
        self.send_but.place(x=1100, y=625, width=50, height=40)

        self.network_thread.start()  # start thread
        self.window.mainloop()
        self.finished.set()
        self.network_thread.join()  # close and join thread on window close

    def send(self):
        """
        sends a message from the input entry to the client thread's input
        """
        if not self.textvar.get() == "":
            # since pasting a message bypasses validate, send only 500 chars
            self.in_buf.append(self.textvar.get()[0:500])
            self.textvar.set("")

    def validatecommand(self):
        """
        validate function for the input
        """
        return len(self.textvar.get()) < 500


class Gui(tk.Tk):
    """
    A class that holds the master GUI window
    """
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        """
        Init function that builds a window holding a single container, switching between each sub-window (frame)
        """
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

    def show_frame(self, cont):
        """
        A function to display the frame passed as the parameter
        """
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    """
    The start page frame
    """
    def __init__(self, parent, controller):
        """
        init for the start page
        """
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
    """
    The SSH keygen frame
    """
    def __init__(self, parent, controller):
        """
        init for the SSH keygen page
        """
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
        """
        A function that gets a directory using tk dialogue and stores it in the frame object
        """
        self.path_info = askdirectory()
        dirname = "Dir: " + self.path_info.split("/")[-1]
        self.button.configure(text=dirname)


# third window frame page2
class Collector(tk.Frame):
    """
    The prime number collector frame
    """
    def __init__(self, parent, controller):
        """
        init for the prime number collector page
        """
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
        """
        Function to start the prime collector thread
        """
        self._coll = Thread(target=idle_prime, args=(self._done,))
        self._coll.start()

    def stop(self, controller):
        """
        function to stop the thread and exit the page back to the SSH keygen window
        """
        self._done.set()
        self._coll.join()
        controller.show_frame(SSH)


class Rand(tk.Frame):
    """
    The RNG frame
    """
    def __init__(self, parent, controller: Gui):
        """
        init for the RNG page
        """
        tk.Frame.__init__(self, parent)
        self.random = Random()
        self.random.pause()
        label1 = ttk.Label(self, text="RNG", font=("Verdana", 40))
        label1.place(x=1050, y=0)

        button1 = ttk.Button(self, text="Home",
                             command=lambda: self.exit(controller))
        button1.place(x=10, y=10, height=150, width=200)

        sep = ttk.Separator(self, orient="vertical")
        sep.place(x=596, y=0, height=675, width=8)

        start_l = ttk.Label(self, text="Start:")
        end_l = ttk.Label(self, text="End:")
        start_l.place(x=50, y=170, height=50, width=80)
        end_l.place(x=50, y=230, height=50, width=80)

        self.startval = tk.StringVar()
        self.endval = tk.StringVar()

        start = ttk.Entry(self, textvariable=self.startval, style='TButton',
                          validate='key', validatecommand=self.validate_start)
        start.place(x=130, y=170, height=50, width=400)

        end = ttk.Entry(self, textvariable=self.endval, style='TButton',
                        validate='key', validatecommand=self.validate_end)
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

    def exit(self, controller):
        """
        A function that deletes the temporary image and exits the window
        """
        if os.path.exists('temp.png'):
            os.remove('temp.png')
        controller.show_frame(StartPage)

    def generate(self):
        """
        A function to get 2 random numbers from the entries and generate an integer in between them
        """
        self.random.cont()
        start = self.startval.get()
        end = self.endval.get()
        if int(start) >= int(end):
            val = "Invalid start/end"
        else:
            val = self.random.get_int_range(int(start), int(end) - 1)
        self.resultval = str(val)
        self.result.configure(text=("Number: " + str(val)))
        self.random.pause()

    def copy_val(self, gui: Gui):
        """
        A function that copies the value of the button pressed, notifies the user through the
        button text and later resets the button text
        """
        gui.clipboard_clear()
        gui.clipboard_append(self.resultval)
        self.result.configure(text="Copied to clipboard")
        gui.update()
        time.sleep(0.3)
        self.result.configure(text=("Number: " + self.resultval))
        gui.update()

    def gen_image(self):
        """
        A function to generate a random image and place it in the label created for it
        """
        self.random.cont()
        self.random.rand_pic("temp.png")
        self.img = tk.PhotoImage(file="temp.png")
        self.image.configure(image=self.img)
        self.random.pause()

    def validate_start(self):
        """
        validate function for the start number input
        """
        return self.startval.get() == "" or self.startval.get().isnumeric()

    def validate_end(self):
        """
        validate function for the end number input
        """
        return self.endval.get() == "" or self.endval.get().isnumeric()


class Chat(tk.Frame):
    """
    The chat page frame
    """
    def __init__(self, parent, controller):
        """
        init for the chat main page
        """
        tk.Frame.__init__(self, parent)
        self.screen = controller
        self.chats = []

        label1 = ttk.Label(self, text="Chat", font=("Verdana", 40))
        label1.place(x=1050, y=0)

        button1 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.place(x=10, y=10, height=150, width=200)

        self.ip = tk.StringVar()
        self.port = tk.StringVar()
        self.name = tk.StringVar()

        label2 = ttk.Label(self, text="Server host name: (IPv4):", font=("Verdana", 15))
        label3 = ttk.Label(self, text="port:", font=("Verdana", 15))
        label4 = ttk.Label(self, text="Display Name:", font=("Verdana", 15))

        label2.place(x=400, y=200, width=275, height=40)
        label3.place(x=700, y=200, width=100, height=40)
        label4.place(x=500, y=325, height=50, width=200)

        ip_ent = ttk.Entry(self, textvariable=self.ip, style='TButton', font=("Verdana", 15))
        port_ent = ttk.Entry(self, textvariable=self.port, style='TButton', font=("Verdana", 15))
        name_ent = ttk.Entry(self, textvariable=self.name, style='TButton', font=("Verdana", 15))

        ip_ent.place(x=400, y=265, width=275, height=50)
        port_ent.place(x=700, y=265, width=100, height=50)
        name_ent.place(x=500, y=400, height=50, width=200)

        button2 = ttk.Button(self, text="Connect",
                             command=lambda: self.connect())
        button2.place(x=500, y=500, height=100, width=200)

    def connect(self):
        self.chats.append(ChatClient(self.screen, self.ip.get(), self.port.get(), self.name.get()))

# make other chat window


def style():
    """
    A function holding all style changes
    """
    s = ttk.Style()
    s.configure('.', font=('Helvetica', 20))
    s.configure('TButton', background="#000000")
    s.configure(style='Large.TButton', font=('Helvetica', 40))
    s.configure(style='Small.TButton', font=('Helvetica', 12))


def main():
    """
    Main function- makes sure the primes database file exists, then creates the window,
    sets its size and calls the main loop
    """
    if not os.path.exists("primes.bin"):
        with open("primes.bin", "wb") as file:
            pickle.dump([], file)
    if not test_camera():
        messagebox.showerror("Camera not found", "The computer's camera is not available")
        return
    app = Gui()
    app.minsize(1200, 675)
    app.maxsize(1200, 675)
    style()
    app.mainloop()


# Driver Code
if __name__ == '__main__':
    if os.path.exists('temp.png'):
        os.remove('temp.png')
    print("".isnumeric())
    logging.basicConfig(filename="rsagen.log", level=logging.DEBUG)
    main()
