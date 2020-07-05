import tkinter as tk
from symbols import symbols
from stock import Stock
from options import Options

menu_options = ["volume", "open-interest"]

class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        window_h = self.winfo_screenheight()
        window_w = self.winfo_screenwidth()
        self.geometry("%dx%d+0+0" % (window_w, window_h))
        self.main_frame = tk.Frame(self)
        self.main_frame.place(relwidth=1, relheight=1)

        self.show_frame(StartPage, "",  "")

    # to display the current frame passed as
    # parameter
    def show_frame(self, page, ticker, detail):
        if detail == "":
            self.main_frame = tk.Frame(self)
            self.main_frame.place(relwidth=1, relheight=1)
            frame = page(self.main_frame, self)
        else:
            frame = page(self.main_frame, self, ticker, detail) 
        frame.place(relwidth=1, relheight=1)
        #frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Adds menubotton with various options
        mb = tk.Menubutton(self, text="Sort options by", width=10)
        mb.place(relx=0.6, rely=0.09)
        mb.menu = tk.Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label=menu_options[0], command=lambda: controller.show_frame(OptionsPage, self.ticker, menu_options[0]))
        mb.menu.add_command(label=menu_options[1], command=lambda: controller.show_frame(OptionsPage, self.ticker, menu_options[1]))

        self.entry = tk.Entry(self, width=20, bg="white")
        self.entry.place(relx=0.5, rely=0.1, anchor='center')
        self.entry.bind('<KeyRelease>', self.on_key_release)

        self.listbox = tk.Listbox(self, exportselection=False)
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
        chosen = self.listbox.get(self.listbox.curselection())
        self.entry.delete(0, len(chosen))
        self.entry.insert(0, chosen)
        chosen_list = chosen.split("(")
        self.ticker = chosen_list[len(chosen_list) - 1].split(")")[0]

#creates a frame with scrolling capabilities
class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.view = tk.Frame(self.canvas, background="#ffffff") 
        #creates a scrollbar
        self.scroll= tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((4,4), window=self.view, anchor="nw", tags="self.view")

        #binds and event whenever size of view frame changes
        self.view.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)            


class OptionsPage(tk.Frame):
    def __init__(self, parent, controller, ticker, detail):  #are these, parameters rigth?????
        tk.Frame.__init__(self, parent)
        self.ticker = ticker;
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage, "", ""), padx=10, pady=10)
        back_button.place(relx=0, rely=0)

        new_frame = tk.Frame(controller, bg="grey")
        new_frame.place(relx=0.5, rely=0.5, relwidth=0.7, relheight=0.7, anchor="center")

        self.scrollFrame = ScrollFrame(new_frame) # add a new scrollable frame.
        
        # Now add some controls to the scrollframe. 
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        """for row in range(100):
            a = row
            tk.Label(self.scrollFrame.view, text="%s" % row, width=3, borderwidth="1", 
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Button(self.scrollFrame.view, text=t, command=lambda x=a: self.printMsg("Hello " + str(x))).grid(row=row, column=1) """
        """for num in range(1, 26):
            tk.Label(self.scrollFrame.view, text="%s" % num, width=3, borderwidth="1", relief="solid").grid(row=num, column=0)
            tk.Button(self.scrollFrame.view, text="Option contract:$38").grid(row=num, column=1) """
        self.display_options()

        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)

    def display_options(self):
        stock_obj = Stock(self.ticker)
        option_obj = Options(stock_obj.get_options_chain(), self.ticker)
        formatted_options = option_obj.volume_formatted()
        for num in range(1, 26):
            tk.Label(self.scrollFrame.view, text="%s" % num, width=5).grid(row=num, column=0)
            tk.Button(self.scrollFrame.view, text=formatted_options[num - 1]["data"]).grid(row=num, column=1)
            tk.Label(self.scrollFrame.view, text="volume: %s" % formatted_options[num - 1]["volume"]).grid(row=num, column=2)

    


# Driver Code
app = tkinterApp()
app.title("Options Ranker")
app.mainloop()
