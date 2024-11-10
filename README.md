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
        root.destroy()



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
    rt=Tk()
    rt.title("Menu Card")

    frame = Frame(rt,highlightbackground="black", highlightthickness=2, width = 230, height=200,border=20)
    frame.pack()

    title_font=font.Font(size=30)
    title=Label(rt,text="----MENU----",font=title_font, fg="black")
    title.place(relx=0.1,rely=0.1,anchor=CENTER)

    title.pack()

    myLab=Label(rt,text="PIZZA",font=("Calibri",14,"bold"))
    myLab.place(relx=0.1,rely=0.1,anchor='w')

    myLab1=Label(rt,text="BURGER",font=("Calibri",14,"bold"))
    myLab1.place(relx=0.1,rely=0.3,anchor='w')

    myLab2=Label(rt,text="ICE CREAM",font=("Calibri",14,"bold"))
    myLab2.place(relx=0.1,rely=0.5,anchor='w')

    myLab3=Label(rt,text="DRINKS",font=("Calibri",14,"bold"))
    myLab3.place(relx=0.1,rely=0.7,anchor='w')


    myLab=Label(rt,text="250/-",font=("Calibri",14,"bold"))
    myLab.place(relx=0.7,rely=0.1,anchor='w')

    myLab1=Label(rt,text="140/-",font=("Calibri",14,"bold"))
    myLab1.place(relx=0.7,rely=0.3,anchor='w')

    myLab2=Label(rt,text="90/-",font=("Calibri",14,"bold"))
    myLab2.place(relx=0.7,rely=0.5,anchor='w')

    myLab3=Label(rt,text="50/-",font=("Calibri",14,"bold"))
    myLab3.place(relx=0.7,rely=0.7,anchor='w')


def feedbackk():
        feed = Tk()
        feed.geometry("600x500")
        feed.title("Submit Feedback form")
        connectn = sqlite3.connect("Restaurant.db")
        cursor = connectn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS FEEDBACK(n text,eid text,feedback5 text,com text)")
        name = StringVar()
        email = StringVar()
        comments = StringVar()

        def submit():
            n = name.get()
            eid = email.get()
            com = txt.get('1.0', END)
            feedback1 = ""
            feedback2 = ""
            feedback3 = ""
            feedback4 = ""
            if (checkvar1.get() == "1"):
                feedback1 = "Excellent"
            if (checkvar2.get() == "1"):
                feedback2 = "Good"
            if (checkvar3.get() == "1"):
                feedback2 = "Average"
            if (checkvar4.get() == "1"):
                feedback2 = "Poor"
            feedback5 = feedback1 + " " + feedback2 + " " + feedback3 + " " + feedback4
            conn = sqlite3.connect("Restaurant.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO FEEDBACK VALUES ('" + n + "','" + eid + "','" + com + "','" + feedback5 + "')")
            messagebox.showinfo("message", "data inserted !")
            feed.destroy()

        def cancel():
            feed.destroy()

        lb1 = Label(feed, font=("Calisto MT", 15, "bold"), text="Thanks for Visiting!", fg="black").pack(side=TOP)
        lbl2 = Label(feed, font=("calisto MT", 15), text="We're glad you chose us ! Please tell us how it was!",
                     fg="black").pack(side=TOP)
        
        namelbl = Label(feed, font=('vardana', 15), text="Name:-", fg="black", bd=10, anchor=W).place(x=10, y=150)
        nametxt = Entry(feed, font=('vardana', 15), bd=6, insertwidth=2, bg="white", justify='right',
                        textvariable=name).place(x=15, y=185)
        emaillbl = Label(feed, font=('vardana', 15), text="Email:-", fg="black", bd=10, anchor=W).place(x=280, y=150)
        emailtxt = Entry(feed, font=('vardana', 15), bd=6, insertwidth=2, bg="white", justify='right',
                         textvariable=email).place(x=285, y=185)

        ratelbl = Label(feed, font=('vardana', 15), text="How would you rate us?", fg="black", bd=10, anchor=W).place(
            x=10, y=215)
        checkvar1 = StringVar()
        checkvar2 = StringVar()
        checkvar3 = StringVar()
        checkvar4 = StringVar()
        c1 = Checkbutton(feed, font=('Calibri', 10, "bold"), text="Excellent", bg="white", variable=checkvar1)
        c1.deselect()
        c1.place(x=15, y=265)
        c2 = Checkbutton(feed, font=('Calibri', 10, "bold"), text="Good", bg="white", variable=checkvar2, )
        c2.deselect()
        c2.place(x=120, y=265)
        c3 = Checkbutton(feed, font=('Calibri', 10, "bold"), text=" Average", bg="white", variable=checkvar3, )
        c3.deselect()
        c3.place(x=220, y=265)
        c4 = Checkbutton(feed, font=('Calibri', 10, "bold"), text="   Poor  ", bg="white", variable=checkvar4, )
        c4.deselect()
        c4.place(x=320, y=265)

        commentslbl = Label(feed, font=('Calibri', 15), text="Comments", fg="black", bd=10, anchor=W).place(x=10, y=300)
        txt = Text(feed, width=50, height=5)
        txt.place(x=15, y=335)
        submit = Button(feed, font=("Calibri", 15), text="Submit", fg="black", bg="green", bd=2, command=submit).place(
            x=145, y=430)
        
        cancel = Button(feed, font=("Calibri", 15), text="Cancel", fg="black", bg="red", bd=2, command=cancel).place(
            x=245, y=430)
        feed.mainloop()


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
