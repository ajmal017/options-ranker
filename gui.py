import tkinter as tk
from symbols import symbols
from stock import Stock
from options import Options
from PIL import ImageTk, Image

menu_options = {"volume": "volume_formatted",
                "open-interest": "open_interest_formatted"}


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
    def show_frame(self, page, ticker, method):
        self.main_frame = tk.Canvas(self)
        self.main_frame.place(relwidth=1, relheight=1)
        if method == "":
            frame = page(self.main_frame, self)
        else:
            frame = page(self.main_frame, self, ticker, method) 
        frame.place(relwidth=1, relheight=1)
        frame.tkraise()


#display the start page where user input is taken
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        image = tk.PhotoImage(file="img/new_background.png")
        label = tk.Label(self, image=image) 
        label.image = image
        label.pack()

        #Adds menubotton with various options
        mb = tk.Menubutton(self, text="Sort options by", width=10)
        mb.place(relx=0.6, rely=0.09)
        mb.menu = tk.Menu(mb, tearoff=0)
        mb["menu"] = mb.menu
        mb.menu.add_command(label="volume", command=lambda: controller.show_frame(OptionsPage, self.ticker, menu_options["volume"]))
        mb.menu.add_command(label="open-interest", command=lambda: controller.show_frame(OptionsPage, self.ticker, menu_options["open-interest"]))

        #adds entry box for user input
        self.entry = tk.Entry(self, width=20, bg="white")
        self.entry.place(relx=0.5, rely=0.1, anchor='center')
        self.entry.bind('<KeyRelease>', self.on_key_release)

        #listbox for displaying posible stock tickers
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

    #stores user choice of company/ticker
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

#this page displays 25 the options sort by a specified criteria
class OptionsPage(tk.Frame):
    def __init__(self, parent, controller, ticker, method): 
        tk.Frame.__init__(self, parent)
        self.ticker = ticker
        self.method = method
        self.parent = parent
        self.controller = controller
        #place a background
        image = tk.PhotoImage(file="img/new_background.png")
        label = tk.Label(self, image=image) 
        label.image = image
        label.pack()

        #back button to return to previous page
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage, "", ""), padx=10, pady=10)
        back_button.place(relx=0, rely=0)

        reverse_button = tk.Button(self, text="Reverse", command=lambda: self.reverse_order())
        reverse_button.place(relx=0.15, rely=0.15)      
        new_frame = tk.Frame(controller, bg="grey")
        new_frame.place(relx=0.5, rely=0.5, relwidth=0.6, relheight=0.6, anchor="center")
        # add a new scrollable frame.
        self.scrollFrame = ScrollFrame(new_frame) 
        self.display_options(True)

        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scrollFrame.pack(side="top", fill="both", expand=True)

    #displays 25 different options as button that can be clicked for more information
    def display_options(self, order):
        stock_obj = Stock(self.ticker)
        option_obj = Options(stock_obj.get_options_chain(), self.ticker)
        sorted_options = getattr(option_obj, self.method)(order)
        #canvas = tk.Canvas(self, width=500, height=500)
        #canvas.pack()
        #image = ImageTk.PhotoImage(Image.open("img/new_background.png"))
        
        #canvas.create_image(0,0,image=image)

        #formatted_options = option_obj.volume_formatted()
        for num in range(1, 26):
            tk.Label(self.scrollFrame.view, text="%s" % num, width=5).grid(row=num, column=0)
            tk.Button(
                self.scrollFrame.view, 
                text=sorted_options[num - 1]["data"], 
                command=lambda: self.show_frame(OptionContract, stock_obj, sorted_options[num - 1]["full_data"])).grid(row=num, column=1)
            tk.Label(self.scrollFrame.view, text=sorted_options[num - 1]["print_metric"]).grid(row=num, column=2)

    def reverse_order(self):
        pass

    #displays the new page
    def show_frame(self, page, stock_obj, option):
        frame = page(self.controller, stock_obj, option, self.method)
        frame.place(relwidth=1, relheight=1)
        frame.tkraise()

#this page displays more data for a single options contract
class OptionContract(tk.Frame):
    def __init__(self, controller, stock_obj, option, method):
        tk.Frame.__init__(self)
        self.stock_obj = stock_obj
        self.option = option
        image = tk.PhotoImage(file="img/new_background.png")
        label = tk.Label(self, image=image) 
        label.image = image
        label.pack()
        #back button to go to previous page
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(OptionsPage, stock_obj.get_ticker(), method), padx=10, pady=10)
        back_button.place(relx=0, rely=0)

        self.options_data()

    #displays extensive data on a single options contract
    def options_data(self):
        text = tk.Text(self, font=("Helvetica", 20), padx=20)
        contract_data = """strike price: {}\t\t\t\t\ttype: {}\nbid: {}\t\t\t\t\task: {}\n
                        expiration date: {}\t\t\t\t\timplied volatility: {}
                        \nvolume: {}\t\t\t\t\topen-interest: {}\nGreeks\ndelta: {}\t\t\t\t\tgamma: {}\n
                        theta: {}\t\t\t\t\tvega: {}\nrho: {}""".format(
                            self.option["strike"], 
                            self.option["type"], 
                            self.option["bid"],
                            self.option["ask"],
                            self.option["expirationDate"], 
                            self.option["impliedVolatility"],
                            self.option["volume"], 
                            self.option["openInterest"],
                            self.option["delta"],
                            self.option["gamma"],
                            self.option["theta"],
                            self.option["vega"],
                            self.option["rho"])
        text.insert(tk.INSERT, contract_data)
        text.place(relwidth=.6, relheight=.6, relx= 0.5, rely=0.5, anchor="center")



# Driver Code
app = tkinterApp()
'''canvas = tk.Canvas(app, width=300, height=300)
canvas.grid(row = 0, column=0)
image = ImageTk.PhotoImage(Image.open("img/new_background.png")) '''

app.title("Options Ranker")
app.mainloop()
