import tkinter as tk
#from PIL import Image, ImageTk
from symbols import symbols

def on_keyrelease(event):
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
    update_listbox(data)

def update_listbox(data):
    # delete previous data
    listbox.delete(0, 'end')
    # sorting data 
    data = sorted(data, key=str.lower)
    # put new data
    for item in data:
        listbox.insert('end', item)

def selected(event):
    #chosen = event.widget.get(event.widget.curselection())
    chosen = listbox.get(listbox.curselection())
    entry.delete(0, len(chosen))
    entry.insert(0, chosen)

app = tk.Tk()
app.title("Options Ranker")

#fit gui to the size of the screen
window_h = app.winfo_screenheight()
window_w = app.winfo_screenwidth()
app.geometry("%dx%d+0+0" % (window_w,window_h))

frame = tk.Frame(app, bg="blue")
frame.place(relwidth=1, relheight=1)
"""
background_image = tk.PhotoImage(file="img/NYSE.gif")
background_label = tk.Label(frame, image=background_image)
background_label.place(relwidth=1, relheight=1)
"""
mb = tk.Menubutton(frame, text="Sort options by", width=10)
mb.place(relx=0.6, rely=0.09)
mb.menu = tk.Menu(mb, tearoff=0)
mb["menu"] =  mb.menu
mb.menu.add_checkbutton(label="Highest volume")
mb.menu.add_checkbutton(label="Highest Open Interest")


entry = tk.Entry(frame, width=20, bg="white")
entry.place(relx=0.5, rely=0.1, anchor='center')
entry.bind('<KeyRelease>', on_keyrelease)

listbox = tk.Listbox(app)
listbox.place(relx=0.5, rely=0.12, anchor='n')
listbox.bind('<<ListboxSelect>>', selected)
update_listbox(symbols)

app.mainloop()
