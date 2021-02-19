

import sqlite3 as sq
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import pandas as pd
import matplotlib.pyplot as plt
import socket
import requests
import bs4

# ----------------------------------------------------------for front page internet------------------------------------------------------------------------
try:
    con = socket.create_connection(("www.google.com", 80))
    print("internet connected")
    res = requests.get(
        "https://weather.com/en-IN/weather/today/l/22.08,82.14?par=google&temp=c")
    print(res)
    soup = bs4.BeautifulSoup(res.text, "lxml")
# location
    data1 = soup.find('h1')
    data1text = data1.text.split("W")
    data1f = data1text[0]
    print(data1text[0])
# temp
    data2 = soup.find('span', {
                      "class":  "_-_-node_modules-@wxu-components-src-organism-CurrentConditions-CurrentConditions--tempValue--3KcTQ"})
    # print(data2)
    data2text = data2.text
    data2f = data2text + "C"
    print(data2text)
# time
    data3 = soup.find('div', {
                      "class": "_-_-node_modules-@wxu-components-src-organism-CurrentConditions-CurrentConditions--timestamp--1SWy5"})
    data3text = data3.text.split(" ")
    data3f = data3text[2] + " " + data3text[3]
    print(data3text[2] + " " + data3text[3])

# date
    res2 = requests.get("https://www.calendardate.com/todays.htm")
    # print(res2)
    soup2 = bs4.BeautifulSoup(res2.text, "lxml")
    data6 = soup2('p')
    data6ans = data6[0].text.split(" ")
    ans2 = data6ans[3] + " " + data6ans[4]+" " + data6ans[5]+" "+data6ans[6]
    print(ans2)

# -----------------------------------------------------------qotd---------------------------------------------------------------------------------
    res4 = requests.get("https://www.brainyquote.com/quote_of_the_day")
    # print(res)
    soup3 = bs4.BeautifulSoup(res4.text, "lxml")
    #data = soup3.find_all('a')
    # print(data)
    data7 = soup3.find('img')
    print(data7)
    data7text = data7['alt']
    data7textf = ' " '+data7text+' " '
except Exception as e:
    print("error", e)

# ----------------------------------------------------------image download---------------------------------------------------------------------


def image_download():
    data8 = soup3.find('img')
    #imgsrc = data8['data-img-url']
    # print(imgsrc)
    # print(data8['data-img-url'])
    img_url = "https://www.brainyquote.com"+data8['data-img-url']
    import datetime
    dt = datetime.datetime.now().date()
    imgname = "qotd " + str(dt) + ".jpg"
    with open(imgname, "wb") as f:
        r1 = requests.get(img_url)
        f.write(r1.content)
        print("downloaded !!")
        showinfo("SUCCESS", "qotd downloaded :)))")


# --------------------------------------------------------table---------------------------------------------------------------------------------------------

con = None
try:
    con = sq.connect("student.db")
    print("database connected")
    cur = con.cursor()
#	cur.execute("CREATE TABLE student(Rno integer, Name text, Marks integer)")
    con.commit()
except Exception as e:
    print("creation issue-->", e)
finally:
    if con is not None:
        con.close()
        # print("disconnected")

# --------------------------------------------------------functions--------------------------------------------------------------------------------------


def add():
    adst.deiconify()
    win.withdraw()


def view():
    stdata.delete(1.0, END)
    vist.deiconify()
    win.withdraw()
    con = None
    try:
        con = sq.connect("student.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM student")
        res = cur.fetchall()
        print(res)
        info = " "
        for r in res:
            info = " rollno : " + \
                str(r[0])+"\n" + " name: " + str(r[1]) + \
                " \n" + " marks: " + str(r[2]) + ("\n"*2)
            stdata.insert(INSERT, info)
    except Exception as e:
        print(e)


def update():
    cupst.deiconify()
    win.withdraw()


def delete():
    dest.deiconify()
    win.withdraw()


def charts():
    con = sq.connect("student.db")
    df = pd.read_sql_query("select * from student", con)
    # print(df)
    # print(df["Marks"])
    mark = df.sort_values(by="Marks", ascending=0)
    # print(mark)
    plotdata = mark.head()
    print(plotdata)
    pname = list(plotdata["Name"])
    pmarks = list(plotdata["Marks"])
    plt.bar(pname, pmarks)
    plt.xlabel("Names")
    plt.ylabel("marks")
    plt.title("Performance Analysis")
    plt.grid()
    plt.show()


'''
def find():
	fist.deiconify()
	win.withdraw()
'''


def asave():
    arno_e.focus()
    con = None
    try:
        rno = arno_e.get()
        name = aname_e.get()
        marks = amarks_e.get()
        con = sq.connect("student.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM student")
        res = cur.fetchall()
        print(res)
        flag = False
        for r in res:
            if r[0] == int(rno):
                showerror("error", "rno exists")
                flag = True
                arno_e.delete(0, END)
                aname_e.delete(0, END)
                amarks_e.delete(0, END)
                break
        if flag == False:
            if rno.isdigit() == False:
                showerror("error", "Roll Number should be INTEGER ONLY.")
            elif len(name) < 2 or name.isalpha() == False:
                showerror("error", "invalid name")
                aname_e.delete(0, END)
            elif marks.isdigit() == 0:
                showerror("error", "Marks can be INTEGER ONLY .")
            elif int(marks) < 0 or int(marks) > 100:
                showerror("error", "invalid marks")
                amarks_e.delete(0, END)
            else:
                con = sq.connect("student.db")
                cur = con.cursor()
                with con:
                    cur.execute("INSERT INTO student VALUES(?,?,?)",
                                (rno, name, marks))
                print("add student successful !")
                showinfo("success", "record added")
                aname_e.delete(0, END)
                arno_e.delete(0, END)
                amarks_e.delete(0, END)
    except Exception as e:
        print("save issue--->", e)
        showerror("InValid Input !",
                  "Please Check You Have Provided All The Inputs.")
        #aname_e.delete(0, END)
        #arno_e.delete(0, END)
        #amarks_e.delete(0, END)


#	finally:
#		print(rno, name,marks)

def aback():
    aname_e.delete(0, END)
    arno_e.delete(0, END)
    amarks_e.delete(0, END)
    win.deiconify()
    adst.withdraw()


def vback():
    win.deiconify()
    vist.withdraw()


def usave():
    # ---------------------------------update both name and marks---------------------------------------------------------------------
    uname_e.focus()
    con = None
    try:
        urno = urno_e.get()
        uname = uname_e.get()
        umarks = umarks_e.get()
        if urno.isdigit() == False:
            showerror("ERROR", " Roll numberShould be INTEGER only ")
        elif len(uname) < 2 or uname.isalpha() == False:
            showerror("error", "invalid name")
            uname_e.delete(0, END)
        elif umarks.isdigit() == False:
            showerror("ERROR", " Marks Should be INTEGER only")
        elif int(umarks) < 0 or int(umarks) > 100:
            showerror("error", " marks should be in range 0-100")
            umarks_e.delete(0, END)
        else:
            con = sq.connect("student.db")
            cur = con.cursor()
            with con:
                cur.execute(
                    """UPDATE  student SET marks = ?, name  =? WHERE rno = ?""", (umarks, uname, urno))
            print("updated")
            showinfo("success", "Record  updated")
            urno_e.delete(0, END)
            uname_e.delete(0, END)
            umarks_e.delete(0, END)

    except Exception as e:
        print("update error--->", e)
        showerror("InValid Input !",
                  "Please Check You Have Provided All The Inputs.")
        uname_e.delete(0, END)
        umarks_e.delete(0, END)


def uback():
    uname_e.delete(0, END)
    urno_e.delete(0, END)
    umarks_e.delete(0, END)
    win.deiconify()
    upst.withdraw()


def dsave():
    drno_e.focus()
    try:
        delrno = int(drno_e.get())
        con = sq.connect("student.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM student")
        res = cur.fetchall()
        flag = False
        for r in res:
            if r[0] == int(delrno):
                flag = True
                with con:
                    cur.execute("DELETE FROM student WHERE rno = ?", (delrno,))
                print("deleted")
                showinfo("SUCCESS", "record deleted")

        if flag == False:
            showerror("ERROR", "Roll number does not exist.")
            drno_e.delete(0, END)
    except Exception as e:
        print("Error--->", e)
        showerror("Invalid input ", "Enter A valid Roll Number.")
        drno_e.delete(0, END)
        drno_e.focus()


def dback():
    drno_e.delete(0, END)
    win.deiconify()
    dest.withdraw()

#uproll = int(centry.get())


def confirm():
    centry.focus()
    con = None
    try:
        uproll = int(centry.get())
        con = sq.connect("student.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM student")
        res = cur.fetchall()
        flag = False
        for r in res:
            if r[0] == uproll:
                print(" exists")
                flag = True
    # -------------------------------------------going to update window----------------------------------------------------------------
                centry.delete(0, END)
                upst.deiconify()
                cupst.withdraw()
                urno_e.insert(1, uproll)
                break
        if flag == False:
            print("dne")
            showerror("error", "Rno not found, try again")
            centry.delete(0, END)
    except Exception as e:
        print("fetch error---->", e)
        showerror("Invalid Input", "Enter A Valid Roll Number")
        centry.delete(0, END)


def cback():
    centry.delete(0, END)
    win.deiconify()
    cupst.withdraw()
# def confirmupdate(uproll):
#	upst.deiconify()
#	cupst.withdraw()
#	r = urno_e.insert(0,uproll)


def delall():
    result = askquestion("delete", "are you sure?")
    if result == 'yes':
        con = sq.connect("student.db")
        cur = con.cursor()
        with con:
            cur.execute("DELETE  FROM student ")
        print("deleted")
        showinfo("success", "all records deleted succesfully")
    else:
        print("all records are safe")
        showinfo("INFO", "all records are safe")


'''
def findback():
	win.deiconify()
	fist.withdraw()
'''

# ---------------------------------------------------------home page----------------------------------------------------------------------------------
win = Tk()
win.title("Home Page")
win.geometry("500x500")
win.config(bg="light green")
# add fonts and bg to title and window????

lbl = Label(win, text="Welcome to Student Management System ",
            font=("arial", 10, "bold"))
lbl.pack(pady="10")
addbtn = Button(win, width="10", text="ADD", font=(
    "arial", 10, "bold"), background="light grey", command=add)
addbtn.pack(pady="14")
viewbtn = Button(win, width="10", text="VIEW ", font=(
    "arial", 10, "bold"), background="light grey", command=view)
viewbtn.pack(pady="14")
updbtn = Button(win, width="10", text="UPDATE ", font=(
    "arial", 10, "bold"), background="light grey", command=update)
updbtn.pack(pady="14")
dltbtn = Button(win, width="10", text="DELETE ", font=(
    "arial", 10, "bold"), background="light grey", command=delete)
dltbtn.pack(pady="14")
chartbtn = Button(win, width="10", text="CHARTS", font=(
    "arial", 10, "bold"), background="light grey", command=charts)
chartbtn.pack(pady="14")
'''
findbtn = Button(win, width = "10", text = "FIND" ,font = ("arial", 10, "bold"), background= "light grey", command = find)
findbtn.pack(pady = "14")
'''
loc = Label(win, bd='4', relief="flat", text="Location : " + data1f)
temp = Label(win, text="Temperature : " + data2f)
qotd = Label(win, text="QOTD : " + data7textf)
time = Label(win, text="Time : " + data3f)
date = Label(win,  text="Date: " + ans2)
downloadbtn = Button(win, width="13", text="Download QOTD", font=(
    "arial", 10, "bold"), background="light grey", command=image_download)
date.place(x=5, y=350)
time.place(x=300, y=350)
loc.place(x=5, y=380)
temp.place(x=300, y=380)
qotd.place(x=5, y=420)
downloadbtn.place(x=3,  y=443)

# border?????????????


# --------------------------------------------------------------------add student-------------------------------------------------------------------------------------
# add student window
adst = Toplevel(win)
adst.title("Add student")
adst.geometry("500x500")
adst.configure(background="#f7e0d0")
adst.withdraw()  # so that sari windows ek sath na appear ho

arno_l = Label(adst, text="Enter rno: ", font=('arial', 10, 'bold'))
arno_e = Entry(adst, width=15)
aname_l = Label(adst, text="Enter Name: ", font=('arial', 10, 'bold'))
aname_e = Entry(adst, width=15)
amarks_l = Label(adst, text="Enter Marks: ", font=('arial', 10, 'bold'))
amarks_e = Entry(adst, width=15)
asave = Button(adst, text="SAVE", font=("arial", 10, "bold"),
               background="light grey", command=asave)
aback = Button(adst, text="BACK", font=("arial", 10, "bold"),
               background="light grey", command=aback)
arno_e.focus()
arno_l.pack(pady=10)
arno_e.pack(pady=10)
aname_l.pack(pady=10)
aname_e.pack(pady=10)
amarks_l.pack(pady=10)
amarks_e.pack(pady=10)
asave.pack(pady=11)
aback.pack(pady=11)
# ---------------------------------------------------------------update student------------------------------------------------------------------------------------
# update student window
upst = Toplevel(win)
upst.title("update Students")
upst.geometry("500x500")
upst.config(bg="#e3d4ca")
upst.withdraw()

urno_l = Label(upst, text="Enter rno: ", font=('arial', 10, 'bold'))
urno_e = Entry(upst, width=15)
uname_l = Label(upst, text="Enter Name: ", font=('arial', 10, 'bold'))
uname_e = Entry(upst, width=15)
umarks_l = Label(upst, text="Enter Marks: ", font=('arial', 10, 'bold'))
umarks_e = Entry(upst, width=15)
usave = Button(upst, text="SAVE", font=("arial", 10, "bold"),
               background="light grey", command=usave)
uback = Button(upst, text="BACK", font=("arial", 10, "bold"),
               background="light grey", command=uback)
uname_e.focus()
urno_l.pack(pady=11)
urno_e.pack(pady=11)
uname_l.pack(pady=11)
uname_e.pack(pady=11)
umarks_l.pack(pady=11)
umarks_e.pack(pady=11)
usave.pack(pady=11)
uback.pack(pady=11)

# ---------------------------------------------------------view student-----------------------------------------------------------------------------------------
# view student window
vist = Toplevel(win)
vist.title("View Students")
vist.geometry("500x500")
vist.configure(background="orange")
vist.withdraw()  # so that sari windows ek sath na appear ho

stulbl = Label(vist,  text="STUDENT RECORDS")
vback = Button(vist, text="BACK", width=10,
               background="light grey", command=vback)
stdata = ScrolledText(vist, width=50, height=40)
vback.pack(side="bottom")
stdata.pack(pady=20)
stulbl.place(x=230, y=5)
#list = Listbox(vist, width = 250, height = 250)
#list.pack(side = 'left')


# -----------------------------------------------------------------delete student--------------------------------------------------------------------------------------
# delete student window
dest = Toplevel(win)
dest.title(" Remove Students")
dest.geometry("500x500")
dest.config(bg='#f5ddce')
dest.withdraw()

drno_l = Label(dest, text="Enter rno: ", font=('arial', 10, 'bold'))
drno_e = Entry(dest, width=15)
dsave = Button(dest, text="DELETE", width=10, font=(
    "arial", 10, "bold"), background="light grey", command=dsave)
dback = Button(dest, text="BACK", width=10, font=(
    "arial", 10, "bold"), background="light grey", command=dback)
delall = Button(dest, text="DELETE ALL RECORDS", width=20, font=(
    "arial", 10, "bold"), background="light grey", command=delall)
drno_e.focus()
drno_l.pack(pady=11)
drno_e.pack(pady=11)
dsave.pack(pady=11)
dback.pack(pady=11)
delall.pack(pady=78)


# ---------------------------------------------------------confirm update---------------------------------------------------------------------------
cupst = Toplevel(win)
cupst.title("Confirm Updates")
cupst.geometry("500x500")
cupst.config(bg='#ceebe4')
cupst.withdraw()

clabel = Label(cupst, text="enter rno you wanna update")
centry = Entry(cupst)
confirm = Button(cupst, text="Confirm", command=confirm)
cback = Button(cupst, text="cancel", command=cback)
centry.focus()
clabel.pack(pady=10)
centry.pack(pady=10)
confirm.pack(pady=10)
cback.pack(pady=10)
centry.focus()


win.mainloop()
