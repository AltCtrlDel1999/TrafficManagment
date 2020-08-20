import mysql.connector
import time
from tkinter import *
from PIL import Image, ImageTk

myconn = mysql.connector.connect(host="localhost", user="root", password="root", database="traffic")
cur = myconn.cursor(prepared=True)
root = Tk()
root.wm_title("Tkinter window")
root.geometry("1000x720")
load = Image.open("ab.png")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.image = render
img.place(x=0, y=0, width=1000, height=720)

cnt2 = Label(root, text="count2")
cnt2.pack()
cnt2.place(x=550, y=100)
cnt0 = Label(root, text="count0")
cnt0.pack()
cnt0.place(x=410, y=600)
cnt1 = Label(root, text="count1")
cnt1.pack()
cnt1.place(x=250, y=270)
cnt3 = Label(root, text="count3")
cnt3.pack()
cnt3.place(x=700, y=420)

canvas0 = Canvas(root, width=60, height=30, bg="black")
canvas0.pack()
canvas0.place(x=350, y=170)
oval0 = canvas0.create_oval(2, 2, 30, 30, fill='black')
oval1 = canvas0.create_oval(32, 2, 60, 31, fill='black')
canvas0.itemconfig(oval0, outline='white')
canvas1 = Canvas(root, width=30, height=60, bg="black")
canvas1.pack()
canvas1.place(x=650, y=200)
oval2 = canvas1.create_oval(2, 2, 30, 30, fill='black')

oval3 = canvas1.create_oval(2, 32, 30, 60, fill='black')

canvas2 = Canvas(root, width=60, height=30, bg="black")
canvas2.pack()
canvas2.place(x=590, y=510)
oval4 = canvas2.create_oval(2, 2, 30, 30, fill='black')
oval5 = canvas2.create_oval(32, 2, 60, 31, fill='black')

canvas3 = Canvas(root, width=30, height=60, bg="black")
canvas3.pack()
canvas3.place(x=315, y=430)
oval6 = canvas3.create_oval(2, 2, 30, 30, fill='black')
oval7 = canvas3.create_oval(2, 32, 30, 60, fill='black')


def change_green(k):
    print(k)
    if k == 0:
        canvas0.itemconfig(oval0, fill="green")
        root.update()
        canvas0.itemconfig(oval1, fill="black")
        root.update()
    elif k == 1:
        canvas1.itemconfig(oval2, fill="green")
        root.update()
        canvas1.itemconfig(oval3, fill="black")
        root.update()
    elif k == 2:
        canvas2.itemconfig(oval4, fill="green")
        root.update()
        canvas2.itemconfig(oval5, fill="black")
        root.update()
    elif k == 3:
        canvas3.itemconfig(oval6, fill="green")
        root.update()
        canvas3.itemconfig(oval7, fill="black")
        root.update()


def change_red(k):
    print(k)
    if k == 0:
        canvas0.itemconfig(oval1, fill="red")
        root.update()
        canvas0.itemconfig(oval0, fill="black")
        root.update()
    elif k == 1:
        canvas1.itemconfig(oval3, fill="red")
        root.update()
        canvas1.itemconfig(oval2, fill="black")
        root.update()
    elif k == 2:
        canvas2.itemconfig(oval5, fill="red")
        root.update()
        canvas2.itemconfig(oval4, fill="black")
        root.update()
    elif k == 3:
        canvas3.itemconfig(oval7, fill="red")
        root.update()
        canvas3.itemconfig(oval6, fill="black")
        root.update()


def start():
    i = 0
    ltime = 60
    count = 0

    while i < 4:
        # take cnt[i] & ltime[i] from database
        cur.execute("select count from test where lane = %s", (i,))
        count1 = cur.fetchall()
        for cnt in count1:
            count = cnt[0]

        cur.execute("select ltime from test where lane = %s", (i,))
        ltime1 = cur.fetchall()
        for lt in ltime1:
            ltime = lt[0]
        # ctime calculation function
        ctime = int((count / ltime) * 20)
        # print(ctime)
        print(count)
        print(ltime)
        print("\n")
        # make cnt[i] = 0
        cur.execute("update test set count = 0  where lane = %s", (i,))
        myconn.commit()
        # make signal green for ctime
        change_green(i)
        # rounding off ctime
        # sleep for ctime
        time.sleep(ctime)

        if i == 0:
            str1 = str(count)
            cnt0.config(text=str1)
            cnt0.update_idletasks()

        elif i == 1:
            str1 = str(count)
            cnt1.config(text=str1)
            cnt1.update_idletasks()

        elif i == 2:
            str1 = str(count)
            cnt2.config(text=str1)
            cnt2.update_idletasks()

        elif i == 3:
            str1 = str(count)
            cnt3.config(text=str1)
            cnt3.update_idletasks()

        # make signal red
        change_red(i)
        # ltime = ctime in database
        cur.execute("update test set ltime = %s where lane =%s", (ctime, i))
        myconn.commit()

        i += 1
        if i == 4:
            i = 0


b = Button(root, text="start", command=start)
b.pack()
b.place(x=20, y=20)
root.mainloop()
