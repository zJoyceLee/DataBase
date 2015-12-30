# SQL
import MySQLdb
# bar chart
import numpy as np
import matplotlib.pyplot as plt
# ui gtk3
from gi.repository import Gtk, GLib

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
#            studentSuccessfulLogin(userName)
        # teacher login
        elif (userName, passwd) in Teachers:
            self.promptLabel.set_text("Prompt: Teacher login successful...")
#            teacherSuccessfulLogin(userName)
        # error
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

win = LoginWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
