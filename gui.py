import tkinter as tk
from tkinter import ttk
LARGEFONT = ("Verdana", 35)
from symbols import symbols


class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        """container = tk.Frame(self)   
        container.pack(side = "top", fill = "both", expand = True)  
   
        container.grid_rowconfigure(0, weight = 1) 
        container.grid_columnconfigure(0, weight = 1) """
        window_h = self.winfo_screenheight()
        window_w = self.winfo_screenwidth()
        self.geometry("%dx%d+0+0" % (window_w, window_h))
        main_frame = tk.Frame(self)
        main_frame.place(relwidth=1, relheight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):

            frame = F(main_frame, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            #frame.grid(row = 0, column = 0, sticky ="nsew")
            frame.place(relwidth=1, relheight=1)

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        #label = ttk.Label(self, text ="Startpage")

        # putting the grid in its place by using
        # grid
        #label.grid(row = 0, column = 4, padx = 10, pady = 10)
        mb = tk.Menubutton(self, text="Sort options by", width=10)
        mb.place(relx=0.6, rely=0.09)
        mb.menu = tk.Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_checkbutton(label="Highest volume", command=lambda: controller.show_frame(Page1))
        mb.menu.add_checkbutton(label="Highest Open Interest")

        self.entry = tk.Entry(self, width=20, bg="white")
        self.entry.place(relx=0.5, rely=0.1, anchor='center')
        self.entry.bind('<KeyRelease>', self.on_key_release)

        self.listbox = tk.Listbox(self)
        self.listbox.place(relx=0.5, rely=0.12, anchor='n')
        self.listbox.bind('<<ListboxSelect>>', self.selected)
        self.update_listbox(symbols)

    def on_key_release(self, event):
        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()
        # get data from test_list
        if value == '':
            data = symbols
        else:
            data = []
            for symbol in symbols:
                if value in symbol.lower():
                    data.append(symbol)
        # update data in listbox
        self.update_listbox(data)

    def update_listbox(self, data):
        # delete previous data
        self.listbox.delete(0, 'end')
        # sorting data
        data = sorted(data, key=str.lower)
        # put new data
        for item in data:
            self.listbox.insert('end', item)

    def selected(self, event):
        #chosen = event.widget.get(event.widget.curselection())
        chosen = self.listbox.get(self.listbox.curselection())
        self.entry.delete(0, len(chosen))
        self.entry.insert(0, chosen)


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        # button to show frame 2 with text
        # layout2
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.place(relx=0, rely=0)

        window = tk.Frame(self, bg='blue') 
        window.place(relx=0.2, rely=0.2, relwidth=0.75, relheight=0.75)


# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page 2", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

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
app = tkinterApp()
app.title("Options Ranker")
app.mainloop()
