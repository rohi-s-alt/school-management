# ------------COMPUTER SCIENCE PROJECT--------------
# --------------------2021-22-----------------------
# ------ Rohit ------- XII-D ------- Aaditya -------

# Importing
import datetime
import tkinter
import tkinter.simpledialog
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

editing = False

# Creating the global font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()

# Creating the Main Table (not deletable)
connector.execute(
    "CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT_0 "
    "(STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, "
    "EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)")
connector.commit()

# Creating a table to store Database lists
connector.execute(
    'CREATE TABLE IF NOT EXISTS BASELIST ("NAME" TEXT, "LABL" TEXT)')
connector.commit()

# Entering the first Database details
connector.execute(
    'INSERT INTO BASELIST (NAME, LABL) SELECT * FROM (SELECT "DATA1" AS NAME, '
    '"MAIN" AS LABL) AS temp WHERE NOT EXISTS (SELECT NAME FROM BASELIST '
    'WHERE NAME = "DATA1") LIMIT 1')
connector.commit()


# Creating the functions
# Reset Entry Fields
def reset_fields():
    if editing is True:
        canced()
    for i in ['name_strvar', 'email_strvar', 'contact_strvar',
              'gender_strvar', 'stream_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())


# Clear The List
def reset_form():
    tree.delete(*tree.get_children())
    reset_fields()


# Monitors Database Selection
def callback(*args):
    getform()
    disbutt()


# Disable next/previous button when at the first or last DataBase
def disbutt():
    dbase = datab_strvar.get()
    dat, lab = getlis()
    if dbase == dat[0]:
        butp["state"] = DISABLED
    else:
        butp["state"] = NORMAL

    if dbase == dat[-1]:
        butn["state"] = DISABLED
    else:
        butn["state"] = NORMAL


# Get index of the Database to be used
def gbasenum():
    dbase = datab_strvar.get()
    if dbase == "":
        basenum = 0
    else:
        basenum = int(dbase[4:]) - 1
    return basenum


# get the list of all the database
def getlis():
    curr = connector.execute(f'select * from BASELIST')
    data = curr.fetchall()
    dat = []
    lab = []
    for da in data:
        dat.append(da[0])
        lab.append(da[1])
    return dat, lab


# Fill the table with the Records from the specified Database
def getform():
    if editing is True:
        canced()
    tree.delete(*tree.get_children())

    curr = connector.execute(f'SELECT * FROM SCHOOL_MANAGEMENT_{gbasenum()}')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)

    uplbl()


# Update the label showing database name
def uplbl():
    dat, lab = getlis()
    dbase = datab_strvar.get()
    ind = dat.index(dbase)

    lbtext1.config(text=f'Students Records - {lab[ind]}')
    lbtext2.config(text=lab[ind])


# Create New database
def newbase():
    dat, lab = getlis()
    ter = "DATA" + str(int(dat[-1][4:]) + 1)

    valu = tkinter.simpledialog.askstring(title="Label",
                                          prompt="Enter Database Label",
                                          initialvalue=ter)
    if valu is None:
        pass
    else:
        connector.execute(f'INSERT INTO BASELIST VALUES ("{ter}","{valu}")')
        connector.commit()
        connector.execute(
            f"CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT_{int(dat[-1][4:])} "
            f"(STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, "
            f"EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)")
        connector.commit()
        datsel['menu'].add_command(label=ter,
                                   command=tkinter._setit(datab_strvar, ter))
        datab_strvar.set(ter)


# Delete a Database
def delbase():
    dbase = datab_strvar.get()
    getin = datsel['menu'].index(dbase)
    if dbase != "DATA1":
        answer = mb.askyesno(title='confirmation',
                             message='Are you sure that you want to delete?')
        if answer:
            datsel['menu'].delete(getin)
            connector.execute(f'DELETE FROM BASELIST WHERE NAME="{dbase}"')
            connector.commit()
            connector.execute(f'DROP TABLE SCHOOL_MANAGEMENT_{gbasenum()}')
            connector.commit()
            datab_strvar.set(datalist[0])
    else:
        mb.showerror('Error!', 'Cant delete the Main Record! Try Another!')


# Go the Previous Database
def butchgp():
    dat, lab = getlis()
    dbase = datab_strvar.get()
    ind = dat.index(dbase) - 1
    datab_strvar.set(dat[ind])


# Go to next database
def butchgn():
    dat, lab = getlis()
    dbase = datab_strvar.get()
    ind = dat.index(dbase) + 1
    datab_strvar.set(dat[ind])


# Renaming the Label
def renlab():
    dbase = datab_strvar.get()
    oldn = lbtext2.cget('text')
    if dbase != "DATA1":
        valu = tkinter.simpledialog.askstring(title="Rename Label", 
                                              prompt="Enter New Database Label",
                                              initialvalue=oldn)
        if valu is None:
            pass
        else:
            connector.execute(
                f"UPDATE BASELIST SET LABL = '{valu}' WHERE NAME = '{dbase}'")
            connector.commit()
        uplbl()
    else:
        mb.showerror('Error!', 'Cant rename the Main Record! Try Another!')


# Get the Database list in option menu
def getbase():
    dat, lab = getlis()
    for i in dat[1:]:
        datsel['menu'].add_command(label=i,
                                   command=tkinter._setit(datab_strvar, i))
    datab_strvar.set(dat[0])


# Add a new record
def add_record():
    global editing

    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    dobd = dob.get_date()
    stream = stream_strvar.get()

    if not name or not email or not contact or not gender or not dob or not stream:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            if editing is False:
                connector.execute(
                    f'INSERT INTO SCHOOL_MANAGEMENT_{gbasenum()} '
                    f'(NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) '
                    f'VALUES (?,?,?,?,?,?)',
                    (name, email, contact, gender, dobd, stream))
                connector.commit()
                mb.showinfo('Record added',
                            f"Record of {name} was successfully added")

            elif editing is True:
                current_item = tree.focus()
                values = tree.item(current_item)
                selection = values["values"]

                connector.execute(
                    f'UPDATE SCHOOL_MANAGEMENT_{gbasenum()} SET NAME="{name}", '
                    f'EMAIL="{email}", PHONE_NO="{contact}", GENDER="{gender}", '
                    f'DOB="{dobd}", STREAM="{stream}" '
                    f'WHERE STUDENT_ID={selection[0]}')
                connector.commit()
                mb.showinfo('Record Edited',
                            f"Record of {name} was successfully Edited")
                canced()
            getform()
            reset_fields()
        except:
            mb.showerror('Error',
                         'Something Went Wrong. PLease Try Again')


# Delete a record from the list
def remove_record():
    if editing is True:
        canced()
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        answer = mb.askyesno(title='confirmation',
                             message='Are you sure that you want to delete?')
        if answer:
            current_item = tree.focus()
            values = tree.item(current_item)
            selection = values["values"]

            tree.delete(current_item)

            connector.execute(
                f'DELETE FROM SCHOOL_MANAGEMENT_{gbasenum()} '
                f'WHERE STUDENT_ID=%d' % selection[0])
            connector.commit()

            mb.showinfo('Done',
                        'The record is successfully deleted.')

            getform()


# View the record
def view_record():
    if editing is True:
        canced()
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]),
                             int(selection[5][8:]))

        name_strvar.set(selection[1])
        email_strvar.set(selection[2])
        contact_strvar.set(selection[3])
        gender_strvar.set(selection[4])
        dob.set_date(date)
        stream_strvar.set(selection[6])


# Edit A Record
def edit_record():
    global editing
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        if editing is False:
            view_record()
            editing = True
            editrecbut.config(text='Cancel Editing')
            subrec.config(text='Submit and Edit Record')
        elif editing is True:
            canced()


# Cancel Editing
def canced():
    global editing

    editing = False
    reset_fields()
    editrecbut.config(text='Edit Record')
    subrec.config(text='Submit and Add Record')


# Initializing the GUI window
main = Tk()
main.title('School Management System')
main.geometry('1000x600')
main.resizable(1, 1)

# Style configuration
style = ttk.Style(main)
style.theme_use("clam")
style.configure("Treeview", background="#313031", foreground="white",
                fieldbackground="#313031")
style.map('Treeview', background=[('selected', '#BFBFBF')],
          foreground=[('selected', 'black')])
style.configure('TButton', font=('calibri', 20, 'bold'), borderwidth='4')
style.map('TButton', foreground=[('active', '!disabled', 'green')],
          background=[('active', 'black')])

lf_bg = '#313031'  # bg color for the left_frame
cf_bg = '#333436'  # bg color for the center_frame
lf_fg = '#E4E6EB'  # fg color for the left_frame

# Creating the StringVar variables
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
stream_strvar = StringVar()
datab_strvar = StringVar()

# Placing the components in the main window
Label(main, text="SCHOOL MANAGEMENT SYSTEM", font=headlabelfont, bg='#202020',
      fg='#E4E6EB').pack(side=TOP, fill=X)

left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)

center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)

right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)

# Placing components in the left frame
Label(left_frame, text="Name", font=labelfont, bg=lf_bg,
      fg=lf_fg).place(relx=0.5, rely=0.05, anchor="center")
Label(left_frame, text="Contact Number", font=labelfont, bg=lf_bg,
      fg=lf_fg).place(relx=0.5, rely=0.18, anchor="center")
Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg,
      fg=lf_fg).place(relx=0.5, rely=0.31, anchor="center")
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg,
      fg=lf_fg).place(relx=0.5, rely=0.44, anchor="center")
Label(left_frame, text="Date of Birth (DOB)", font=labelfont, bg=lf_bg,
      fg=lf_fg).place(relx=0.5, rely=0.57, anchor="center")
Label(left_frame, text="Stream", font=labelfont, bg=lf_bg,
      fg=lf_fg).place(relx=0.5, rely=0.7, anchor="center")

Entry(left_frame, width=0, textvariable=name_strvar, font=entryfont,
      justify='center', bg='#2f2f2f', fg='#9e9e9e',
      border=1).place(relx=0.5, rely=0.1, anchor="center", relwidth=0.5)
Entry(left_frame, width=0, textvariable=contact_strvar, font=entryfont,
      justify='center', bg='#2f2f2f', fg='#9e9e9e',
      border=1).place(relx=0.5, rely=0.23, anchor="center", relwidth=0.5)
Entry(left_frame, width=0, textvariable=email_strvar, font=entryfont,
      justify='center', bg='#2f2f2f', fg='#9e9e9e',
      border=1).place(relx=0.5, rely=0.36, anchor="center", relwidth=0.5)
Entry(left_frame, width=0, textvariable=stream_strvar, font=entryfont,
      justify='center', bg='#2f2f2f', fg='#9e9e9e',
      border=1).place(relx=0.5, rely=0.75, anchor="center", relwidth=0.5)

optt = OptionMenu(left_frame, gender_strvar, 'Male', "Female")
optt.config(bg='#2f2f2f', fg='#9e9e9e', highlightthickness=0)
optt.place(relx=0.5, rely=0.49, anchor="center", relwidth=0.5)

dob = DateEntry(left_frame, font=("Arial", 12), width=15, justify='center')
dob.place(relx=0.5, rely=0.62, anchor="center", relwidth=0.5)

subrec = Button(left_frame, text='Submit and Add Record', font=labelfont,
                command=add_record, border=1, width=18, bg="#333436",
                fg="#fff", activebackground="#313031", activeforeground="#fff")
subrec.place(relx=0.5, rely=0.85, anchor="center", relwidth=0.95)

# Placing components in the center frame
lbtext2 = Button(center_frame, text="", font=('Garamond', 10), command=renlab,
                 border=0, bg=cf_bg, fg='#A9A9A9')
lbtext2.place(relx=0.5, rely=0.08, anchor="center")

datalist = ['DATA1']
bslc = 0.125
datsel = OptionMenu(center_frame, datab_strvar, *datalist)
datsel.config(bg='#2f2f2f', fg='#9e9e9e', highlightthickness=0)
datsel.place(relx=0.5, rely=bslc, anchor="center", relwidth=0.5)
datab_strvar.set(datalist[0])
datab_strvar.trace("w", callback)

butp = Button(center_frame, text='<', font=('Garamond', 9), command=butchgp,
              bg="#333436", fg="#fff", activebackground="#313031",
              activeforeground="#fff")
butn = Button(center_frame, text='>', font=('Garamond', 9), command=butchgn,
              bg="#333436", fg="#fff", activebackground="#313031",
              activeforeground="#fff")
butp.place(relx=0.07, rely=bslc, anchor="w", relwidth=0.16, relheight=0.04)
butn.place(relx=0.93, rely=bslc, anchor="e", relwidth=0.16, relheight=0.04)

Button(center_frame, text='Delete Record', font=labelfont, command=remove_record,
       width=15, bg="#333436", fg="#fff", activebackground="#313031",
       activeforeground="#fff").place(relx=0.5, rely=0.25,
                                      anchor="center", relwidth=0.9)
Button(center_frame, text='View Record', font=labelfont, command=view_record,
       width=15, bg="#333436", fg="#fff", activebackground="#313031",
       activeforeground="#fff").place(relx=0.5, rely=0.34,
                                      anchor="center", relwidth=0.9)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields,
       width=15, bg="#333436", fg="#fff", activebackground="#313031",
       activeforeground="#fff").place(relx=0.5, rely=0.43,
                                      anchor="center", relwidth=0.9)
editrecbut = Button(center_frame, text='Edit Record', font=labelfont,
                    command=edit_record, width=15, bg="#333436", fg="#fff",
                    activebackground="#313031", activeforeground="#fff")
editrecbut.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.9)

Button(center_frame, text='ADD DATABASE', font=labelfont, command=newbase, width=15,
       bg="#333436", fg="#fff", activebackground="#313031",
       activeforeground="#fff").place(relx=0.5, rely=0.65,
                                      anchor="center", relwidth=0.9)
Button(center_frame, text='DEL DATABASE', font=labelfont, command=delbase, width=15,
       bg="#333436", fg="#fff", activebackground="#313031",
       activeforeground="#fff").place(relx=0.5, rely=0.75,
                                      anchor="center", relwidth=0.9)

# Placing components in the right frame
lbtext1 = Label(right_frame, text='Students Records', font=headlabelfont,
                bg='#2f2f2f', fg='#A9A9A9')
lbtext1.pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE, columns=(
    'Student ID', "Name", "Email Address", "Contact Number", "Gender",
    "Date of Birth", "Stream"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Date of Birth', text='DOB', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=30, stretch=NO)
tree.column('#2', width=100, stretch=NO)
tree.column('#3', width=150, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=70, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=100, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

# On start
getform()
getbase()

# Finalizing the GUI window
main.update()
main.mainloop()
