
from tkinter import *
from tkinter import font
import datetime
import sqlite3
from tkinter import messagebox 
from tkinter import ttk




root=Tk()
root.geometry("1650x700")
root.title("Cafe Management System")

def title_label():
    title_font=font.Font(size=24)
    title=Label(root,text="CAFE MANAGEMENT SYSTEM",font=title_font, fg="black")
    title.pack()
title_label()

def Date_Time():
    t = datetime.datetime.now()
    mylabel2=Label ( root,text="Date : "+str(t.day) + "-" + str(t.month) + "-" + str(t.year),font=("Calibri",10,"bold") )
    mylabel2.pack()
    mylabel3=Label ( root,text= "Time : "+str(t.hour) + ":" + str(t.minute) + ":" + str(t.second),font=("Calibri",10,"bold"))
    mylabel3.pack()
Date_Time()


def Database():
    global connectn, cursor
    connectn = sqlite3.connect("Restaurant.db")
    cursor = connectn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Restaurantrecords(ordno text,piz text,bur text,ice text, dr text, ct text,sb text,tax text,sr text,tot text)")


   
orderno = StringVar()
pizza = StringVar()
burger = StringVar()
icecream = StringVar()
drinks = StringVar()
cost = StringVar()
subtotal = StringVar()
gst = StringVar()
service = StringVar()
total = StringVar()

def tottal():
    ord_n=orderno.get()
    piz=float(pizza.get())
    bur=float(burger.get())
    ic=float(icecream.get())
    drk=float(drinks.get())


    costpiz=piz*250
    costbur=bur*140
    costic=ic*90
    costdrk=drk*50
    costmeal=(costbur+costdrk+costic+costpiz)
    costgst=(costmeal)*0.18
    costsrt=(costmeal)*0.05
    totTax=(costgst+costsrt)
    total_amt=(costmeal+totTax)

    fcmeal=str(costmeal)
    fgst=str(costgst)
    fsrt=str(costsrt)
    ftot=str(total_amt)

    cost.set(fcmeal)
    subtotal.set(fcmeal)
    gst.set(fgst)
    service.set(fsrt) 
    total.set(ftot)

def reset():
        orderno.set("")
        pizza.set("")
        burger.set("")
        icecream.set("")
        drinks.set("")
        cost.set("")
        subtotal.set("")
        gst.set("")
        service.set("")
        total.set("")

frame = Frame(root, bg='white',highlightbackground="black", highlightthickness=2, width = 700, height=520,border=20)
frame.place(relx=0.93,rely=0.535,anchor='e')

my_tree = ttk.Treeview(frame)

style = ttk.Style()
style.configure("Treeview",
                foreground="black",
                rowheight=40,
                fieldbackground="white"
                )
style.map('Treeview',
        background=[('selected', 'lightblue')])


my_tree = ttk.Treeview(frame)
my_tree['columns'] = ("ordno", "piz", "bur", "ice", "dr", "ct", "sb", "tax", "sr", "tot")

horizontal_bar = ttk.Scrollbar(frame, orient="horizontal")
horizontal_bar.configure(command=my_tree.xview)
my_tree.configure(xscrollcommand=horizontal_bar.set)
horizontal_bar.pack(fill=X, side=BOTTOM)

vertical_bar = ttk.Scrollbar(frame, orient="vertical")
vertical_bar.configure(command=my_tree.yview)
my_tree.configure(yscrollcommand=vertical_bar.set)
vertical_bar.pack(fill=Y, side=RIGHT)

my_tree.column("#0", width=0, minwidth=0)
my_tree.column("ordno", anchor=CENTER, width=80, minwidth=25)
my_tree.column("piz", anchor=CENTER, width=60, minwidth=25)
my_tree.column("bur", anchor=CENTER, width=50, minwidth=25)
my_tree.column("ice", anchor=CENTER, width=80, minwidth=25)
my_tree.column("dr", anchor=CENTER, width=50, minwidth=25)
my_tree.column("ct", anchor=CENTER, width=50, minwidth=25)
my_tree.column("sb", anchor=CENTER, width=100, minwidth=25)
my_tree.column("tax", anchor=CENTER, width=50, minwidth=25)
my_tree.column("sr", anchor=CENTER, width=100, minwidth=25)
my_tree.column("tot", anchor=CENTER, width=50, minwidth=25)

my_tree.heading("ordno", text="Order No", anchor=CENTER)
my_tree.heading("piz", text="Pizza", anchor=CENTER)
my_tree.heading("bur", text="Burger", anchor=CENTER)
my_tree.heading("ice", text="Ice cream", anchor=CENTER)
my_tree.heading("dr", text="Drinks", anchor=CENTER)
my_tree.heading("ct", text="Cost", anchor=CENTER)
my_tree.heading("sb", text="Subtotal", anchor=CENTER)
my_tree.heading("tax", text="Tax", anchor=CENTER)
my_tree.heading("sr", text="Service", anchor=CENTER)
my_tree.heading("tot", text="Total", anchor=CENTER)

my_tree.pack() 

def DisplayData():
    Database()
    my_tree.delete(*my_tree.get_children())
    cursor = connectn.execute("SELECT * FROM Restaurantrecords")
    fetch = cursor.fetchall()
    for data in fetch:
        my_tree.insert('', 'end', values=(data))
    cursor.close()
    connectn.close()

DisplayData()

def Delete():
        Database()
        if not my_tree.selection():
            messagebox.showwarning("Warning", "Select data to delete")
        else:
            result = messagebox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                            icon="warning")
        if result == 'yes':
            curItem = my_tree.focus()
            contents = (my_tree.item(curItem))
            selecteditem = contents['values']
            my_tree.delete(curItem)
            cursor = connectn.execute("DELETE FROM Restaurantrecords WHERE ordno= %d" % selecteditem[0])
            connectn.commit()
            cursor.close()
            connectn.close

def exit():
        res=messagebox.askquestion('confirm', 'are you sure you want to exit?', icon="warning")
        if res == 'yes':
            root.destroy()
        else:
             return



def add():
        Database()
        orders = orderno.get()
        pizzas = pizza.get()
        burgers = burger.get()
        ices = icecream.get()
        drinkss = drinks.get()
        costs = cost.get()
        subtotals = subtotal.get()
        taxs = gst.get()
        services = service.get()
        totals = total.get()
        if orders == "" or pizzas == "" or burgers == "" or ices == "" or drinkss == "" or costs == "" or subtotals == "" or taxs == "" or services == "" or totals == "":
            messagebox.showinfo("Warning", "Please fill the empty field!!!")
        else:
            connectn.execute(
                'INSERT INTO Restaurantrecords (ordno, piz, bur , ice ,dr ,ct ,sb ,tax, sr, tot) VALUES (?,?,?,?,?,?,?,?,?,?)',
                (orders, pizzas, burgers, ices, drinkss, costs, subtotals, taxs, services, totals));
            connectn.commit()
            messagebox.showinfo("Message", "Stored successfully")
        
        DisplayData()
        connectn.close


def menucard():
    rt = Tk()
    rt.title("Menu Card")


    frame = Frame(rt, highlightbackground="black", highlightthickness=2, width=500, height=700, border=20)
    frame.pack(padx=20, pady=20)  

    title_font = font.Font(size=30)
    title = Label(rt, text="----MENU----", font=title_font, fg="black")
    title.place(relx=0.5, rely=0.1, anchor=CENTER)  


    items = ["PIZZA", "BURGER", "ICE CREAM", "DRINKS"]
    prices = ["250", "140", "90", "50"]

    def add_item():
        item_name = item_entry.get()
        item_price = price_entry.get()

        if item_name=="" or item_price=="":
             messagebox.showerror('Warning',"Please enter the name and price of the item to be added")
        
        if item_name and item_price: 
            items.append(item_name)
            prices.append(item_price)
            update_menu()

            item_entry.delete(0, END)
            price_entry.delete(0, END)
        messagebox.showinfo("Message", "Stored successfully")

    def update_menu():
       
        for widget in frame.winfo_children():
            widget.destroy()

   
        for i, item in enumerate(items):
            item_label = Label(rt, text=item, font=("Calibri", 14, "bold"))
            price_label = Label(rt, text=prices[i], font=("Calibri", 14, "bold"))
            
            item_label.place(relx=0.1, rely=0.2 + i*0.1, anchor='w')  
            price_label.place(relx=0.7, rely=0.2 + i*0.1, anchor='w')  

        

    item_label = Label(rt, text="Item Name:", font=("Calibri", 12))
    item_label.place(relx=0.1, rely=0.9, anchor='w')

    item_entry = Entry(rt, font=("Calibri", 12), width=15)
    item_entry.place(relx=0.3, rely=0.9, anchor='w')

    price_label = Label(rt, text="Price:", font=("Calibri", 12))
    price_label.place(relx=0.5, rely=0.9, anchor='w')

    price_entry = Entry(rt, font=("Calibri", 12), width=10)
    price_entry.place(relx=0.6, rely=0.9, anchor='w')


    add_button = Button(rt, text="Add Item", font=("Calibri", 12), command=add_item)
    add_button.place(relx=0.8, rely=0.9, anchor='w')

    update_menu()


    rt.mainloop()





def show_feedback():

    show_win = Tk()
    show_win.geometry("600x400")
    show_win.title("All Feedback")


    feedback_text = Text(show_win, width=70, height=20, wrap='word', state='normal')
    feedback_text.pack(padx=10, pady=10, fill='both', expand=True)

    scrollbar = Scrollbar(show_win, command=feedback_text.yview)
    scrollbar.pack(side='right', fill='y')
    feedback_text.config(yscrollcommand=scrollbar.set)

    try:
        with sqlite3.connect("Restaurant.db") as connectn:
            cursor = connectn.cursor()

            cursor.execute("SELECT * FROM FEEDBACK")
            rows = cursor.fetchall()
            
            
            if not rows:
                feedback_text.insert(END, "No feedback available.\n")
            else:
                for row in rows:
                    feedback_text.insert(END, f"Name: {row[0]}\n")
                    feedback_text.insert(END, f"Email: {row[1]}\n")
                    feedback_text.insert(END, f"Comments: {row[2]}\n")
                    feedback_text.insert(END, f"Experience: {row[3]}\n")
                    feedback_text.insert(END, f"Quality: {row[4]}\n")
                    feedback_text.insert(END, f"Menu Variety: {row[5]}\n")
                    feedback_text.insert(END, f"Cleanliness: {row[6]}\n")
                    feedback_text.insert(END, f"Value for Money: {row[7]}\n")
                    feedback_text.insert(END, "-" * 50 + "\n")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error occurred while connecting to the database: {e}")
        return 


    close_btn = Button(show_win, text="Close", command=show_win.destroy)
    close_btn.pack(pady=10)
    labb1=Label(show_win, font=('Verdana', 7), text="Excellent : 3").place(x=420, y=350)
    labb2=Label(show_win, font=('Verdana', 7), text="Good : 2" ).place(x=420, y=370)
    labb3=Label(show_win, font=('Verdana', 7), text="Average : 1").place(x=500, y=350)
    labb4=Label(show_win, font=('Verdana', 7), text="Poor : 0").place(x=500, y=370)

    show_win.mainloop()


from tkinter import Tk, Text, Button, IntVar, END, messagebox, Label, Entry, Checkbutton, W, TOP

def feedbackk():
    feed = Tk()
    feed.geometry("600x800")
    feed.title("Submit Feedback Form")

    connectn = sqlite3.connect("Restaurant.db")
    cursor = connectn.cursor()
   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS FEEDBACK(
            n TEXT,
            eid TEXT,
            com TEXT,
            feed1 INTEGER,
            feed2 INTEGER,
            feed3 INTEGER,
            feed4 INTEGER,
            feed5 INTEGER
        )
    """)

    # Input fields
    Label(feed, font=('Verdana', 15), text="Name:", fg="black").place(x=10, y=120)
    name = Entry(feed, width=25)
    name.place(x=15, y=160)

    Label(feed, font=('Verdana', 15), text="Email:", fg="black").place(x=280, y=120)
    email = Entry(feed, width=25)
    email.place(x=285, y=160)

    # Comments
    Label(feed, font=('Verdana', 15), text="Comments:", fg="black").place(x=10, y=520)
    txt = Text(feed, width=50, height=5)
    txt.place(x=15, y=570)

    # Feedback variables
    feedback_vars = [IntVar(value=0) for _ in range(20)]  # Create a list of IntVars for ratings

    def select_rating(category_index, rating):
        for i in range(4):  # Uncheck all checkboxes in this category
            if i != rating:
                feedback_vars[category_index * 4 + i].set(0)
        feedback_vars[category_index * 4 + rating].set(1)  # Set the selected rating

    def submit():
        n = name.get().strip()
        eid = email.get().strip()
        com = txt.get('1.0', END).strip()

        # Validate input
        if not n or not eid:
            messagebox.showerror("Input Error", "Name and Email cannot be empty.")
            return

        # Collect feedback ratings
        ratings = []
        for i in range(5):
            rating = -1
            for j in range(4):
                if feedback_vars[i * 4 + j].get() == 1:
                    rating = 3 - j  # Convert checkbox selection to rating
                    break
            ratings.append(rating)

        # Check if all ratings are provided
        if any(rating == -1 for rating in ratings):
            messagebox.showerror("Input Error", "Please provide ratings for all categories.")
            return

        # Insert feedback into the database
        try:
            cursor.execute("INSERT INTO FEEDBACK (n, eid, com, feed1, feed2, feed3, feed4, feed5) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                           (n, eid, com, *ratings))
            connectn.commit()
            messagebox.showinfo("Message", "Feedback inserted!")
            feed.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def cancel():
        feed.destroy()

    lb1 = Label(feed, font=("Calisto MT", 15, "bold"), text="Thanks for Visiting!", fg="black").pack(side=TOP)
    lbl2 = Label(feed, font=("calisto MT", 15), text="We're glad you chose us! Please tell us how it was!", fg="black").pack(side=TOP)

    # Rating Categories
    categories = [
        "Overall Experience",
        "Quality of Food and Drinks",
        "Menu Variety",
        "Cleanliness and Ambiance",
        "Value for Money"
    ]

    y_position = 200
    for i, category in enumerate(categories):
        Label(feed, font=('Verdana', 15), text=f"{i + 1}. {category}", fg="black").place(x=10, y=y_position)
        y_position += 30

        # Create Checkbuttons for each category
        Checkbutton(feed, text="Excellent", variable=feedback_vars[i * 4 + 0], 
                    command=lambda idx=i: select_rating(idx, 0)).place(x=15, y=y_position)
        Checkbutton(feed, text="Good", variable=feedback_vars[i * 4 + 1], 
                    command=lambda idx=i: select_rating(idx, 1)).place(x =15 + 100, y=y_position)
        Checkbutton(feed, text="Average", variable=feedback_vars[i * 4 + 2], 
                    command=lambda idx=i: select_rating(idx, 2)).place(x=15 + 200, y=y_position)
        Checkbutton(feed, text="Poor", variable=feedback_vars[i * 4 + 3], 
                    command=lambda idx=i: select_rating(idx, 3)).place(x=15 + 300, y=y_position)
        y_position += 30

    # Submit and Cancel buttons
    submit_btn = Button(feed, font=("Calibri", 15), text="Submit", fg="black", bg="green", bd=2, command=submit)
    submit_btn.place(x=15, y=680)
    cancel_btn = Button(feed, font=("Calibri", 15), text="Cancel", fg="black", bg="red", bd=2, command=cancel)
    cancel_btn.place(x=100, y=680)

    feed.mainloop()



show_btn = Button(root, text="Show All Feedback", command=show_feedback, font=("Calibri", 12), bg="grey", fg="white")
show_btn.place(relx=0.293 ,rely=0.67)

e1 = Entry(root,width=30,borderwidth=5,textvariable=orderno,font=("Calibri",10,"bold"))
e1.place(relx=0.08,rely=0.2,anchor='w')
myLabel1=Label(root,text="Order Number:",font=("Calibri",12,"bold"))
myLabel1.place(relx=0.01,rely=0.2,anchor='w')

lab=Label(root,text="---------Order Details--------",font=("Calibri",12,"bold"))
lab.place(relx=0.06,rely=0.25,anchor='w')

e2 = Entry(root,width=30,borderwidth=5,textvariable=pizza,font=("Calibri",10,"bold"))
e2.place(relx=0.08,rely=0.30,anchor='w')
myLabel2=Label(root,text="Pizza:",font=("Calibri",12,"bold"))
myLabel2.place(relx=0.03,rely=0.30,anchor='w')

e3 = Entry(root,width=30,borderwidth=5,textvariable=burger,font=("Calibri",10,"bold"))
e3.place(relx=0.08,rely=0.35,anchor='w')
myLabel3=Label(root,text="Burger:",font=("Calibri",12,"bold"))
myLabel3.place(relx=0.025,rely=0.35,anchor='w')

e4 = Entry(root,width=30,borderwidth=5,textvariable=icecream,font=("Calibri",10,"bold"))
e4.place(relx=0.08,rely=0.40,anchor='w')
myLabel4=Label(root,text="Ice Cream:",font=("Calibri",12,"bold"))
myLabel4.place(relx=0.02,rely=0.40,anchor='w')

e5 = Entry(root,width=30,borderwidth=5,textvariable=drinks,font=("Calibri",10,"bold"))
e5.place(relx=0.08,rely=0.45,anchor='w')
myLabel5=Label(root,text="Drinks:",font=("Calibri",12,"bold"))
myLabel5.place(relx=0.025,rely=0.45,anchor='w')

lab2=Label(root,text="-----------Bill Details----------",font=("Calibri",12,"bold"))
lab2.place(relx=0.06,rely=0.50,anchor='w')

e6 = Entry(root,width=30,borderwidth=5,textvariable=cost,font=("Calibri",10,"bold"))
e6.place(relx=0.08,rely=0.55,anchor='w')
myLabel6=Label(root,text="Cost:",font=("Calibri",12,"bold"))
myLabel6.place(relx=0.03,rely=0.55,anchor='w')

e7 = Entry(root,width=30,borderwidth=5,textvariable=subtotal,font=("Calibri",10,"bold"))
e7.place(relx=0.08,rely=0.60,anchor='w')
myLabel7=Label(root,text="Subtotal:",font=("Calibri",12,"bold"))
myLabel7.place(relx=0.025,rely=0.60,anchor='w')

e8 = Entry(root,width=30,borderwidth=5,textvariable=gst,font=("Calibri",10,"bold"))
e8.place(relx=0.08,rely=0.70,anchor='w')
myLabel8=Label(root,text="GST:",font=("Calibri",12,"bold"))
myLabel8.place(relx=0.035,rely=0.70,anchor='w')

e9 = Entry(root,width=30,borderwidth=5,textvariable=service,font=("Calibri",10,"bold"))
e9.place(relx=0.08,rely=0.75,anchor='w')
myLabel9=Label(root,text="Service Tax:",font=("Calibri",12,"bold"))
myLabel9.place(relx=0.02,rely=0.75,anchor='w')

e0 = Entry(root,width=30,borderwidth=5,textvariable=total,font=("Calibri",10,"bold"))
e0.place(relx=0.08,rely=0.80,anchor='w')
myLabel0=Label(root,text="Total:",font=("Calibri",12,"bold"))
myLabel0.place(relx=0.03,rely=0.80,anchor='w')
    

def buttons_FE():
    myButton1=Button(root,text="Menu Card",font=("Calibri",12,"bold"),height=3,width=12,borderwidth=5,bg="grey",command=menucard)
    myButton1.place(relx=0.3,rely=0.20,anchor='n')

    myButton2=Button(root,text="Add",font=("Calibri",12,"bold"),height=3,width=12,borderwidth=5,bg="grey",command=add)
    myButton2.place(relx=0.37,rely=0.20,anchor='n')

    myButton3=Button(root,text="Delete Record",font=("Calibri",12,"bold"),height=3,width=12,borderwidth=5,bg="grey",command=Delete)
    myButton3.place(relx=0.3,rely=0.31,anchor='n')

    myButton4=Button(root,text="Reset",font=("Calibri",12,"bold"),height=3,width=12,borderwidth=5,bg="grey",command=reset)
    myButton4.place(relx=0.37,rely=0.31,anchor='n')

    myButton5=Button(root,text="Total",font=("Calibri",12,"bold"),height=3,width=12,borderwidth=5,bg="grey",command=tottal)
    myButton5.place(relx=0.3,rely=0.42,anchor='n')

    myButton6=Button(root,text="Exit System",font=("Calibri",12,"bold"),height=3,width=12,borderwidth=5,bg="grey",command=exit)
    myButton6.place(relx=0.37,rely=0.42,anchor='n')

    myButton7=Button(root,text="FeedBack Form",font=("Calibri",12,"bold"),height=3,width=17,borderwidth=5,bg="grey",command=feedbackk)
    myButton7.place(relx=0.335,rely=0.55,anchor='n')
buttons_FE()



root.mainloop()
