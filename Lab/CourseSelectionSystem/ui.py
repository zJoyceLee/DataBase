# SQL
import MySQLdb
# bar chart
import numpy as np
import matplotlib.pyplot as plt
# ui gtk3
from gi.repository import Gtk, GLib

userName = "S1"
studentInfo_list = []
hasAttended_list = []

# student ui
class StudentWindow(Gtk.Window):

    # Database: connect to database::mySchool
    db = MySQLdb.connect("localhost", "root", "1", "mySchool")
    cursor = db.cursor()

    # List: student Information: [('S1', 'LiMing', 19, 'M', 'Computer Software')]
    ss = "SELECT sno, sname, age, sex, sdept FROM S WHERE sno = '%s';" % userName
    cursor.execute(ss)
    # results is a tuple
    results = cursor.fetchall()
    for row in results:
        myTuple = (row[0], row[1], int(row[2]), row[3], row[4])
        studentInfo_list.append(myTuple)

    # List: has attended class:
    #     [('C2', 'Data Structure', 56),
    #      ('C4', 'Computer Principle', 78),
    #      ('C6', 'Windows Technologies', 66),
    #      ('C8', 'Compile Principle', 88)]
    ss = "SELECT C.cno, C.cname, SC.grade FROM C, SC \
              WHERE C.cno = SC.cno AND SC.sno = '%s';" % userName
    cursor.execute(ss)
    results = cursor.fetchall()
    for row in results:
        myTuple = (row[0], row[1], int(row[2]))
        hasAttended_list.append(myTuple)


    # Database: close connect
    db.close()


    # class: __init__
    def __init__(self):
        # title
        Gtk.Window.__init__(self, title = "Student Select Class System")

        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # labels
        self.studentInfo_label = Gtk.Label("Stuent Information: ")
        self.hasAttended_label = Gtk.Label("Has Attended Class: ")

        # TreeView: student information-----------------------------------------
        # Creating the ListStore model
        self.studentInfo_liststore = Gtk.ListStore(str, str, int, str, str)
        for studentInfo_ref in studentInfo_list:
            self.studentInfo_liststore.append(list(studentInfo_ref))

        # Creating the filter, feeding it with the liststore model
        self.studenInfo_filter = self.studentInfo_liststore.filter_new()

        # Creat the treeview, making it use filter as a model, and adding the columns
        self.studentInfoTreeview = Gtk.TreeView.new_with_model(self.studenInfo_filter)
        for i, column_title in enumerate(["id", "name", "age", "gender", "college"]):
            studentInfo_renderer = Gtk.CellRendererText()
            studentInfo_column = Gtk.TreeViewColumn(column_title, studentInfo_renderer, text = i)
            self.studentInfoTreeview.append_column(studentInfo_column)


    # TreeView: has attended class----------------------------------------------
        self.hasAttended_liststore = Gtk.ListStore(str, str, int)
        for hasAttended_ref in hasAttended_list:
            self.hasAttended_liststore.append(list(hasAttended_ref))

        self.hasAttended_filter = self.hasAttended_liststore.filter_new()

        self.hasAttendedTreeview = Gtk.TreeView.new_with_model(self.hasAttended_filter)
        for i, column_title in enumerate(["class id", "name", "grade"]):
            hasAttended_renderer = Gtk.CellRendererText()
            hasAttended_column = Gtk.TreeViewColumn(column_title, hasAttended_renderer, text = i)
            self.hasAttendedTreeview.append_column(hasAttended_column)



        # setting up the  layout,  putting the treeview in a scrollwindow
        self.grid.add(self.studentInfo_label)

        # Layout: studentInfo
        self.studentInfo_scrollable_treelist = Gtk.ScrolledWindow()
        self.studentInfo_scrollable_treelist.set_vexpand(True)
        # (0: col, 1:row, 2:2*width(label_stuInfo), 3:3*height(label_stuInfo))
        self.grid.attach(self.studentInfo_scrollable_treelist, 0, 1, 2, 3)
        self.studentInfo_scrollable_treelist.add(self.studentInfoTreeview)

        # Layout: hasAttended:
        self.grid.attach(self.hasAttended_label, 0, 8, 1, 1)
        self.hasAttended_scrollable_treelist = Gtk.ScrolledWindow()
        self.hasAttended_scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.hasAttended_scrollable_treelist, 0, 9, 2, 6)
        self.hasAttended_scrollable_treelist.add(self.hasAttendedTreeview)


        self.show_all()





# login ui
class LoginWindow(Gtk.Window):
    def __init__(self):
        # title
        Gtk.Window.__init__(self, title = "Login")

        # grid for layout
        grid = Gtk.Grid()
        self.add(grid)

        # label
        self.userNameLabel = Gtk.Label('UserName: ')
        self.passwdLabel = Gtk.Label('Passwd:     ')
        self.promptLabel = Gtk.Label('Prompt: ')

        # entry : userName
        self.userNameEntry = Gtk.Entry()
        self.userNameEntry.set_text("user name...")

        # entry : passwd
        self.passwdEntry = Gtk.Entry()
        # self.passwdEntry.set_text("enter your passwd...")

        # visible passwd
        self.check_visible = Gtk.CheckButton("Visible")
        self.check_visible.connect("toggled", self.on_visible_toggled)
        self.check_visible.set_active(True)

        # button : Login
        self.loginButton = Gtk.Button(label = "Login")
        self.loginButton.connect("clicked", self.on_loginButton_clicked)

        # button : Close
        self.closeButton = Gtk.Button(label = "Close")
        self.closeButton.connect("clicked", self.on_closeButton_clicked)

        # layout: attach(xx, col, row, w, h)
        grid.add(self.userNameLabel)
        grid.attach(self.userNameEntry, 1, 0, 1, 1)

        grid.attach(self.passwdLabel, 0, 1, 1, 1)
        grid.attach(self.passwdEntry, 1, 1, 1, 1)
        grid.attach(self.check_visible, 2, 1, 1, 1)

        grid.attach(self.loginButton, 0, 2, 1, 1)
        grid.attach(self.closeButton, 2, 2, 1, 1)

        grid.attach(self.promptLabel, 0, 3, 3, 1)

    # Login Button
    def on_loginButton_clicked(self, widget):
        # login user group
        # students group
        Students = [("S1", "001"), ("S2", "002"), ("S3", "003"), ("S4", "004"),
               ("S5", "005"), ("S6", "006"), ("S7", "007"), ("S8", "008"), ("S9", "009")]
        # teachers group
        Teachers= [("WangXiaoming", "000"), ("LiuHong", "000"),
                   ("LiJinyan", "000"), ("WuZhigang", "000"), ("JiangYingyue", "000"), ]

        # login
        userName = self.userNameEntry.get_text()
        passwd = self.passwdEntry.get_text()

        # group by
        # student login
        if (userName.upper(), passwd) in Students:
            userName = userName.upper()
            self.promptLabel.set_text("Prompt: Student login successful...")
            # studentSuccessfulLogin(userName)
        # teacher login
        elif (userName, passwd) in Teachers:
            self.promptLabel.set_text("Prompt: Teacher login successful...")
            # teacherSuccessfulLogin(userName)
        # error: not in user group or passwd wrong
        else:
            self.promptLabel.set_text("Prompt: Login failure...")

    # close Button
    def on_closeButton_clicked(self, widget):
        print("Goodby.")
        # close window
        Gtk.main_quit()

    # visible passwd
    def on_visible_toggled(self, button):
        value = button.get_active()
        self.passwdEntry.set_visibility(value)

# win = LoginWindow()
win = StudentWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
