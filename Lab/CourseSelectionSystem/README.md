Course Selection System
============

A small project about  Database implement Course Selection and Grade Management via MySQL and Python


Environment
----

* Ubuntu 14.04 LTS
* MySQL 5.7
* Python 2.7
* [GTK+](http://python-gtk-3-tutorial.readthedocs.org/en/latest/install.html)

About The Project
----

* mySchool.sql: create database
* 001.py: impl roughly in command line
* **ui.py: the Application**

How to run the application:

    python ui.py

About Connect
----

How to connect to the Database in Python:

    pip install MySQL-python

Code in .py like this:

    import MySQLdb
    db = MySQLdb.connect('localhost', user, passwd, dbName, charset='utf8')
    cursor = db.cursor()

    ss="SQL string"
    cursor.execute()

    results = cursor.fetchall()
    for row in results:
        """ 'row' is one row in table """
        pass

About UI
----
Implement via Gtk3

[some tutorial: python-gtk-3-tutorial](http://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html)

What I used:

* [listUI: TreeView](http://python-gtk-3-tutorial.readthedocs.io/en/latest/treeview.html)
* [combobox](http://python-gtk-3-tutorial.readthedocs.io/en/latest/combobox.html)
* [Dialogs for error](http://python-gtk-3-tutorial.readthedocs.io/en/latest/dialogs.html)
