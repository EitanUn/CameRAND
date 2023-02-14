import tkinter as tk
from tkinter import ttk
from threading import Thread, Event
from files import idle_prime

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
        for F in (StartPage, SSH, Page2, Collector):
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
        label.grid(row=2, column=1, columnspan=3, pady=170, padx=50)

        button1 = ttk.Button(self, text="\nSSH Client\n",
                             command=lambda: controller.show_frame(SSH),
                             width=20)

        # putting the button in its place by
        # using grid
        button1.grid(row=5, column=1, padx=45, pady=10)

        # button to show frame 2 with text layout2
        button2 = ttk.Button(self, text="\nRNG\n",
                             command=lambda: controller.show_frame(Page2),
                             width=20)

        # putting the button in its place by
        # using grid
        button2.grid(row=5, column=2, padx=45, pady=10)

        button2 = ttk.Button(self, text="\nChat Client\n",
                             command=lambda: controller.show_frame(Page2),
                             width=20)

        # putting the button in its place by
        # using grid
        button2.grid(row=5, column=3, padx=45, pady=10)


# second window frame page1
class SSH(tk.Frame):

    def __init__(self, parent, controller):
        self._s = ttk.Style()
        self._s.configure('coll.TButton')
        self._collectbg = False
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 1", font=LARGEFONT)
        label.grid(row=0, column=4, padx=400, pady=200)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Home",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.place(x=10, y=10, height=150, width=200)

        # button to show frame 2 with text
        # layout2
        self.button2 = ttk.Button(self, text="Page 2",
                                  command=lambda: controller.show_frame(Collector), style='coll.TButton')

        # putting the button in its place by
        # using grid
        self.button2.place(x=0, y=475, height=200, width=300)


# third window frame page2
class Collector(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._done = Event()
        self._coll = Thread(target=idle_prime, args=(self._done, ))
        label = ttk.Label(self, text="Beep Boop!\nCollecting...", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=100)

        # button to show frame 3 with text
        # layout3
        button1 = ttk.Button(self, text="\nStart Collector\n",
                             command=lambda: self._coll.start())

        # putting the button in its place by
        # using grid
        button1.grid(row=2, column=1, padx=10, pady=10)

        button2 = ttk.Button(self, text="\nStop Collector\n",
                             command=lambda: self.stop(controller))

        # putting the button in its place by
        # using grid
        button2.grid(row=3, column=1, padx=10, pady=10)

    def stop(self, controller):
        self._done.set()
        self._coll.join()
        controller.show_frame(SSH)




class Page2(tk.Frame):
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


# Driver Code
if __name__ == '__main__':
    app = Gui()
    app.minsize(1200, 675)
    app.maxsize(1200, 675)
    s = ttk.Style()
    s.configure('.', font=('Helvetica', 20))
    app.mainloop()
