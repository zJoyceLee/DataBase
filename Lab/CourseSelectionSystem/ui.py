# SQL
import MySQLdb
# bar chart
import numpy as np
import matplotlib.pyplot as plt
# ui gtk3
from gi.repository import Gtk, GLib
# time
import datetime
# datetime.datetime.now().date() -> datetime.datetime.date(2015, 12, 31)

# Database: connect to database::mySchool
db = MySQLdb.connect("localhost", "root", "1", "mySchool")
cursor = db.cursor()

# Flag:
database_connection_is_closed = False


class StudentInfoWindow(Gtk.Window):
    """
    Student Info UI
    """
    def __init__(self):
        Gtk.Window.__init__(self, title =  "Student Information")
        self.set_border_width(10)
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.stu_list = []
        ss = "SELECT * FROM S;"
        cursor.execute(ss)
        results = cursor.fetchall()
        for row in results:
            mytuple = (row[0], row[1], row[2], int(row[3]), row[4], row[5], row[5])
            self.stu_list.append(mytuple)

        self.counter_record_label = Gtk.Label("Record counter: %d" % len(self.stu_list))
        self.grid.add(self.counter_record_label)

        self.stu_info_liststore = Gtk.ListStore(str, str, str, int, str, str, str)
        for ref in self.stu_list:
            self.stu_info_liststore.append(list(ref))
        self.stu_filter = self.stu_info_liststore.filter_new()
        self.treeview = Gtk.TreeView.new_with_model(self.stu_filter)
        self.title_list = ["id", "name","gender", "age", "college", "user", "pswd"]
        for i, column_title in enumerate(self.title_list):
            renderer = Gtk.CellRendererText()
            column= Gtk.TreeViewColumn(column_title, renderer, text = i)
            self.treeview.append_column(column)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 1, 3, 8)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()

        add_button = Gtk.Button("Add")
        add_button.connect("clicked",  self.on_add_clicked)
        save_button = Gtk.Button("Save")
        save_button.connect("clicked", self.on_save_clicked)
        del_button = Gtk.Button("Del")
        del_button.connect("clicked", self.on_del_clicked)
        close_button = Gtk.Button("Close")
        close_button.connect("clicked", self.on_close_clicked)
        self.grid.attach(add_button, 0, 9, 1, 1)
        self.grid.attach(save_button, 1, 9, 1, 1)
        self.grid.attach(del_button, 2, 9, 1, 1)
        self.grid.attach(close_button, 3, 9, 1, 1)

        enter_label = Gtk.Label("Enter here: ")
        self.grid.attach(enter_label, 3, 1, 1, 1)

        self.entries = list()
        for i in self.title_list:
            if i == "age":
                i = "20"
            entry = Gtk.Entry()
            entry.set_text(i)
            self.entries.append(entry)

        for i, entry in enumerate(self.entries[0:]):
            self.grid.attach(self.entries[i], 3, 2 + i, 1, 1)


    def on_add_clicked(self, widget):
        print("add...")
        val_list = []
        for i in range(0, 7):
            val = self.entries[i].get_text()
            if i == 3:
                val = int(val)
            val_list.append(val)

        ss = "SELECT sno FROM S;"
        cursor.execute(ss)
        results = cursor.fetchall()
        flag = True
        for row in results:
            if row[0].upper() == val_list[0].upper():
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                           Gtk.ButtonsType.OK, "This is an Error MessageDialog")
                dialog.format_secondary_text(
                    "The user is exist...")
                dialog.run()
                dialog.destroy()
                flag = False
        if flag == True:
            ss = "INSERT INTO S(sno, sname, sex, age, sdept, login, pswd) VALUES \
                      ('%s', '%s', '%s', %d, '%s', '%s', '%s');\
                      " % (val_list[0],val_list[1],val_list[2],val_list[3],val_list[4],val_list[5],val_list[6])
            cursor.execute(ss)
            self.stu_list.append(val_list[0])
            self.counter_record_label.set_text("Record counter: %d" % len(self.stu_list))
            self.stu_info_liststore.append(val_list)
            for i in range(0, 7):
                self.entries[i].set_text(self.title_list[i])

    def on_save_clicked(self, widget):
        print("save...")
        db.commit()

    def on_del_clicked(self, widget):
        print("delete...")
        val = self.entries[0].get_text()
        flag = False
        for i in self.stu_info_liststore:
            if i[0].upper() == val.upper():
                val = i[0]
                print(val)
                self.stu_info_liststore.remove(i.iter)
                flag = True
                break
        if flag == False:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                    Gtk.ButtonsType.OK, "This is an Error MessageDialog")
            dialog.format_secondary_text(
                "The user is not exist...")
            dialog.run()
            dialog.destroy()
        else:
            ss = "DELETE FROM Selected WHERE sno = '%s';" % val
            cursor.execute(ss)
            ss = "DELETE FROM SC WHERE sno = '%s';" % val
            cursor.execute(ss)
            ss = "DELETE FROM S WHERE sno = '%s';" % val
            cursor.execute(ss)

            for data in self.stu_list:
                if data[0] == val:
                    self.stu_list.remove(data)
            self.counter_record_label.set_text("Record counter: %s" % len(self.stu_list))

            for i in range(0, 7):
                self.entries[i].set_text(self.title_list[i])

    def on_close_clicked(self, widget):
        print("close...")
        self.close()


class CourseInfoWindow(Gtk.Window):
    """
    Course Info UI
    """
    def __init__(self):
        Gtk.Window.__init__(self, title =  "Class Information")
        self.set_border_width(10)
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.class_list = []
        ss = "SELECT * FROM C;"
        cursor.execute(ss)
        results = cursor.fetchall()
        for row in results:
            mytuple = (row[0], row[1], int(row[2]), row[3], row[4])
            self.class_list.append(mytuple)

        self.counter_record_label = Gtk.Label("Record counter: %d" % len(self.class_list))
        self.grid.add(self.counter_record_label)

        self.class_info_liststore = Gtk.ListStore(str, str, int, str, str)
        for ref in self.class_list:
            self.class_info_liststore.append(list(ref))
        self.class_filter = self.class_info_liststore.filter_new()
        self.treeview = Gtk.TreeView.new_with_model(self.class_filter)
        self.title_list = ["id", "name","credit", "college", "teacher"]
        for i, column_title in enumerate(self.title_list):
            renderer = Gtk.CellRendererText()
            column= Gtk.TreeViewColumn(column_title, renderer, text = i)
            self.treeview.append_column(column)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 1, 3, 8)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()

        add_button = Gtk.Button("Add")
        add_button.connect("clicked",  self.on_add_clicked)
        save_button = Gtk.Button("Save")
        save_button.connect("clicked", self.on_save_clicked)
        del_button = Gtk.Button("Del")
        del_button.connect("clicked", self.on_del_clicked)
        close_button = Gtk.Button("Close")
        close_button.connect("clicked", self.on_close_clicked)
        self.grid.attach(add_button, 0, 9, 1, 1)
        self.grid.attach(save_button, 1, 9, 1, 1)
        self.grid.attach(del_button, 2, 9, 1, 1)
        self.grid.attach(close_button, 3, 9, 1, 1)

        enter_label = Gtk.Label("Enter here: ")
        self.grid.attach(enter_label, 3, 1, 1, 1)

        self.entries = list()
        for i in self.title_list:
            if i == "credit":
                i = "4"
            entry = Gtk.Entry()
            entry.set_text(i)
            self.entries.append(entry)

        for i, entry in enumerate(self.entries[0:]):
            self.grid.attach(self.entries[i], 3, 2 + i, 1, 1)


    def on_add_clicked(self, widget):
        print("add...")
        val_list = []
        for i in range(0, 5):
            val = self.entries[i].get_text()
            if i == 2:
                val = int(val)
            val_list.append(val)

        ss = "SELECT sno FROM S;"
        cursor.execute(ss)
        results = cursor.fetchall()
        flag = True
        for row in results:
            if row[0].upper() == val_list[0].upper():
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                           Gtk.ButtonsType.OK, "This is an Error MessageDialog")
                dialog.format_secondary_text(
                    "The class is exist...")
                dialog.run()
                dialog.destroy()
                flag = False
        if flag == True:
            ss = "INSERT INTO C(cno, cname, credit, cdept, tname) VALUES \
                      ('%s', '%s', %d, '%s', '%s');\
                      " % (val_list[0],val_list[1],val_list[2],val_list[3],val_list[4])
            cursor.execute(ss)
            self.class_list.append(val_list)
            self.counter_record_label.set_text("Record counter: %d" % len(self.class_list))
            self.class_info_liststore.append(val_list)
            for i in range(0, 5):
                self.entries[i].set_text(self.title_list[i])

    def on_save_clicked(self, widget):
        print("save...")
        db.commit()

    def on_del_clicked(self, widget):
        print("delete...")
        val = self.entries[0].get_text()
        flag = False
        for i in self.class_info_liststore:
            if i[0].upper() == val.upper():
                val = i[0]
                print(val)
                self.class_info_liststore.remove(i.iter)
                flag = True
                break
        if flag == False:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                    Gtk.ButtonsType.OK, "This is an Error MessageDialog")
            dialog.format_secondary_text(
                "The class is not exist...")
            dialog.run()
            dialog.destroy()
        else:
            ss = "DELETE FROM Selected WHERE cno = '%s';" % val
            cursor.execute(ss)
            ss = "DELETE FROM SC WHERE cno = '%s';" % val
            cursor.execute(ss)
            ss = "DELETE FROM C WHERE cno = '%s';" % val
            cursor.execute(ss)

            for data in self.class_list:
                if data[0] == val:
                    self.class_list.remove(data)
            self.counter_record_label.set_text("Record counter: %s" % len(self.class_list))
            for i in range(0, 5):
                self.entries[i].set_text(self.title_list[i])

    def on_close_clicked(self, widget):
        print("close...")
        self.close()


class TeacherWindow(Gtk.Window):
    """
    Teacher UI: Grade management
    """

    def __init__(self, userName):
        Gtk.Window.__init__(self, title = "Grade Management")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(10)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        """
        choices = ["Maintentance", "StudentInfo", "CourseInfo"]
        choices_combo = Gtk.ComboBoxText()
        choices_combo.set_entry_text_column(0)
        choices_combo.connect("changed", self.on_choice_combo_changed)
        for choice in choices:
            choices_combo.append_text(choice)
        self.grid.add(choices_combo)


        maintenance_button = Gtk.Button(label = "Maintentance")
        maintenance_button.connect("clicked", self.on_maintenance_clicked)
        """
        studentInfo_button = Gtk.Button(label = "StudentInfo")
        studentInfo_button.connect("clicked", self.on_studentInfo_clicked)
        self.grid.add(studentInfo_button)
        courseInfo_button = Gtk.Button(label = "CouresInfo")
        courseInfo_button.connect("clicked", self.on_courseInfo_clicked)
        self.grid.attach(courseInfo_button, 1, 0, 1, 1)

        running_button = Gtk.Button(label = "Running")
        running_button.connect("clicked", self.on_running_clicked)
        self.grid.attach(running_button, 2, 0, 1, 1)
        close1_button = Gtk.Button(label = "Close")
        close1_button.connect("clicked", self.on_close_clicked)
        self.grid.attach(close1_button, 3, 0, 1, 1)

        self.className_label = Gtk.Label(label = "Class: ", halign = Gtk.Align.START)
        self.teacherName_label = Gtk.Label(
            label = ("Teacher: %s" % userName), halign = Gtk.Align.START)

        self.selectClass_label = Gtk.Label("Please select a class: ", halign = Gtk.Align.START)
        self.student_and_grade_label = Gtk.Label(
            label = "Students and grade in the class: ", halign = Gtk.Align.START)

        self.find_button = Gtk.Button(label = "Find")
        self.find_button.connect("clicked", self.on_find_clicked)
        self.input_button = Gtk.Button(label = "Input")
        self.input_button.connect("clicked", self.on_input_clicked)
        self.gradeDistribution_button = Gtk.Button(label = "Grade Distribution")
        self.gradeDistribution_button.connect("clicked", self.on_gradeDistribution_clicked)
        self.close2_button = Gtk.Button(label = "Close")
        self.close2_button.connect("clicked", self.on_close_clicked)

        # Layout
        self.grid.attach(self.className_label, 0, 1, 2, 1)
        self.grid.attach(self.teacherName_label, 2, 1, 2, 1)
        self.grid.attach(self.selectClass_label, 0, 2, 2, 1)
        self.grid.attach(self.student_and_grade_label, 2, 2, 2, 1)
        self.grid.attach(self.find_button, 4, 3, 1, 1)
        self.grid.attach(self.input_button, 4, 4, 1, 1)
        self.grid.attach(self.close2_button, 4, 5, 1, 1)
        self.grid.attach(self.gradeDistribution_button, 0, 4, 2, 1)

        # ComboBox
        cnames = [""]
        ss = "SELECT cname FROM C WHERE tname = '%s';" % userName
        cursor.execute(ss)
        results = cursor.fetchall()
        for row in results:
            cnames.append(row[0])
        print(cnames)
        cname_combo = Gtk.ComboBoxText()
        cname_combo.set_entry_text_column(0)
        cname_combo.connect("changed", self.on_cname_combo_changed)
        for cname in cnames:
            cname_combo.append_text(cname)
        self.grid.attach(cname_combo, 0, 3, 2, 1)

        # TreeView student_id and grade
        self.combo_text = ""
        self.sno_and_grade_list = []
        ss = "SELECT cno, sno, grade FROM SC;"
        cursor.execute(ss)
        results = cursor.fetchall()
        for row in results:
            mytuple = (row[0], row[1], int(row[2]))
            self.sno_and_grade_list.append(mytuple)
        self.sno_and_grade_liststore = Gtk.ListStore(str, str, int)
        for ref in self.sno_and_grade_list:
            self.sno_and_grade_liststore.append(list(ref))
        self.current_filter_cno = ""
        self.cno_filter = self.sno_and_grade_liststore.filter_new()
        self.cno_filter.set_visible_func(self.cno_filter_func)
        self.treeview = Gtk.TreeView.new_with_model(self.cno_filter)
        for i, column_title in enumerate(["class id", "student id", "grade"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text = i)
            self.treeview.append_column(column)
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 2, 3, 2, 4)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()

        sno_label = Gtk.Label(label = "Student id: ", halign = Gtk.Align.START)
        self.grid.attach(sno_label, 0, 5, 1, 1)
        grade_label = Gtk.Label(label = "Grade: ", halign = Gtk.Align.START)
        self.grid.attach(grade_label, 0, 6, 1, 1)
        self.sno_entry = Gtk.Entry()
        self.sno_entry.set_sensitive(False)
        # self.grid.attach_next_to(self.sno_entry, sno_label, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach(self.sno_entry, 1, 5, 1, 1)
        self.grade_entry = Gtk.Entry()
        self.grade_entry.set_sensitive(False)
        self.grid.attach(self.grade_entry, 1, 6, 1, 1)

    """
    def on_maintenance_clicked(self, widget):
        print("clicked maintenance")
        stuInfoWin = StudentInfoWindow()
        stuInfoWin.show_all()
    """

    def on_studentInfo_clicked(self, widget):
        stuInfoWin = StudentInfoWindow()
        stuInfoWin.show_all()

    def on_courseInfo_clicked(self, widget):
        courseInfoWin = CourseInfoWindow()
        courseInfoWin.show_all()

    def on_running_clicked(self, widget):
        print("running")

    def on_close_clicked(self, widget):
        global database_connection_is_closed
        if database_connection_is_closed == False:
            print("database: close connection...")
            db.close()
            database_connection_is_closed = True
        Gtk.main_quit()

    def on_find_clicked(self, widget):
        print("find")
        dispCname = ""
        ss = "SELECT cno FROM C WHERE cname = '%s';" % self.combo_text
        cursor.execute(ss)
        result = cursor.fetchone()
        if result is not None:
            dispCname = result[0]
        self.current_filter_cno = dispCname
        self.cno_filter.refilter()

    def on_input_clicked(self, widget):
        if widget.get_label() == "Input":
            print("input")
            widget.set_label("Save")
            self.find_button.set_sensitive(False)
            self.gradeDistribution_button.set_sensitive(False)
            self.close2_button.set_sensitive(False)

            self.sno_entry.set_sensitive(True)
            self.grade_entry.set_sensitive(True)

        elif widget.get_label() == "Save":
            print("Save...")
            widget.set_label("Input")
            self.find_button.set_sensitive(True)
            self.gradeDistribution_button.set_sensitive(True)
            self.close2_button.set_sensitive(True)

            sno = self.sno_entry.get_text()
            if sno != "":
                grade = int(self.grade_entry.get_text())
            else:
                grade = 0

            ss = "SELECT cno FROM C WHERE cname = '%s';\
                 " % self.combo_text
            cursor.execute(ss)
            result = cursor.fetchone()
            if result is not None:
                cno = result[0]
                ss = "SELECT sno FROM SC WHERE cno = '%s';" % cno
                cursor.execute(ss)
                results = cursor.fetchall()
                sno_list = []
                for row in results:
                    if sno.upper() == row[0].upper():
                        sno = row[0]
                    sno_list.append(row[0])

                if sno in sno_list:
                    print("Change student: %s's grade to %s." % (sno, grade))

                    ss = "DELETE FROM SC WHERE sno = '%s' \
                          AND cno = '%s';" % (sno, cno)
                    cursor.execute(ss)
                    db.commit()

                    sql = "INSERT INTO SC(sno, cno, grade) VALUES \
                           ('%s', '%s', %d)" % (sno, cno, grade)
                    cursor.execute(sql)
                    db.commit()

                    self.sno_and_grade_liststore.clear()
                    self.sno_and_grade_list = []

                    ss = "SELECT cno, sno, grade FROM SC;"
                    cursor.execute(ss)
                    results = cursor.fetchall()
                    for row in results:
                        mytuple = (row[0], row[1], int(row[2]))
                        self.sno_and_grade_list.append(mytuple)

                    for ref in self.sno_and_grade_list:
                        self.sno_and_grade_liststore.append(list(ref))

                else:
                    print("Cannot save null...")
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                          Gtk.ButtonsType.OK, "This is an Error MessageDialog")
                    dialog.format_secondary_text("Student id not exist...")
                    dialog.run()
                    dialog.destroy()
                    self.current_filter_cno = cno
                    self.cno_filter.refilter()


            else:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                           Gtk.ButtonsType.OK, "This is an Error MessageDialog")
                dialog.format_secondary_text("Cannot save null...")
                dialog.run()
                dialog.destroy()

            self.sno_entry.set_text("")
            self.grade_entry.set_text("")
            self.sno_entry.set_sensitive(False)
            self.grade_entry.set_sensitive(False)

    def on_gradeDistribution_clicked(self, widget):
        """
        picture everyCourse avgGrade
        """

        ss = "SELECT DISTINCT cno, AVG(grade) FROM SC GROUP BY cno;"
        cursor.execute(ss)
        results = cursor.fetchall()
        n = len(results)

        # className : grade
        d = {}
        for row in results:
            # add className: grade into dict d
            d[row[0]] = float(row[1])
#        print(d)
#        {'C8': 88.0, 'C3': 79.0, 'C2': 71.5, 'C1': 80.0, 'C6': 66.0, 'C4': 78.0}
        gradeMeans = tuple(d.values())
        ind = np.arange(n)
        width =  0.35
        fig, ax = plt.subplots()
        rects = ax.barh(ind, gradeMeans, width, color = 'y')
        ax.set_xlabel('Scores')
        ax.set_title('Grade Distribution')
        ax.set_yticks(ind + width)
        cname = []
        for i in range(0,len(d.keys())):
            ss = "SELECT cname FROM C WHERE cno = '%s';" % d.keys()[i]
            cursor.execute(ss)
            result = cursor.fetchone()
            cname.append(result[0])
        cname = tuple(cname)
        ax.set_yticklabels(cname)

        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                width  = rect.get_width()
                text_y = rect.get_y() + rect.get_height() / 2.
                text_x = 1.05 * width
                ax.text(text_x, text_y,
                        '%d' % int(width), ha = 'center', va = 'bottom')

        autolabel(rects)
        plt.show()

    def on_cname_combo_changed(self, combo):
        self.combo_text = combo.get_active_text()
        if self.combo_text != None:
            print("Selected: cname = %s" % self.combo_text)
            self.className_label.set_text("Class: %s" % self.combo_text)

    def on_choice_combo_changed(self, combo):
        self.combo_text = combo.get_active_text()
        if self.combo_text != None:
            print("Selected: table = %s" % self.combo_text)

    def cno_filter_func(self, model, iter, data):
        if self.current_filter_cno is None or self.current_filter_cno == "None":
            return True
        else:
            return model[iter][0] == self.current_filter_cno


class GradeRecord(Gtk.Window):
    """
    Grade Record UI: show user(student) Grade Info
    """
    def __init__(self, userName):
        Gtk.Window.__init__(self, title = "Grade Record")
        self.set_border_width(20)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(10)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        ss = "SELECT sname FROM S WHERE sno = '%s';" % userName
        cursor.execute(ss)
        result = cursor.fetchone()
        self.info_label = Gtk.Label("%s   %s"
                                     % (userName, result[0]))
        self.title_label = Gtk.Label("Student Grade Record")

        self.time_label = Gtk.Label("%s" % str(datetime.datetime.now().date()))

        self.grid.add(self.info_label)
        self.grid.attach(self.title_label, 1, 0, 1,  1)
        self.grid.attach(self.time_label, 2, 0, 1, 1)

        self.grade_list = []
        ss = "SELECT C.cno, C.cname, SC.grade, C.credit, C.tname FROM C, SC \
                  WHERE C.cno = SC.cno AND SC.sno = '%s';" % userName
        cursor.execute(ss)
        results = cursor.fetchall()
        for row in results:
            myTuple = (row[0], row[1], int(row[2]), int(row[3]), row[4])
            self.grade_list.append(myTuple)

        self.liststore = Gtk.ListStore(str, str, int, int, str)
        for ref in self.grade_list:
            self.liststore.append(list(ref))

        self.grade_filter = self.liststore.filter_new()

        self.gradeTreeview = Gtk.TreeView.new_with_model(self.grade_filter)
        for i, column_title in enumerate(["id", "name", "grade", "credit", "teacher"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text = i)
            self.gradeTreeview.append_column(column)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 2, 3, 6)
        self.scrollable_treelist.add(self.gradeTreeview)

        ss = "SELECT AVG(grade) FROM SC WHERE sno = '%s';" % userName
        cursor.execute(ss)
        result = cursor.fetchone()
        self.average_score_label = Gtk.Label("Average Score: %s" % result[0])

        self.grid.attach(self.average_score_label, 0, 8, 1, 2)


class StudentWindow(Gtk.Window):
    """
    Student UI: show user(student) info, grade, selectable course
    and do course selection
    """

    def __init__(self, userName):
        # title
        Gtk.Window.__init__(self, title = "Student Select Class System")
        self.set_border_width(20)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(5)
        self.grid.set_column_spacing(10)
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.userName = userName


        self.studentInfo_list = []
        # List: student Information: [('S1', 'LiMing', 19, 'M', 'Computer Software')]
        ss = "SELECT sno, sname, age, sex, sdept FROM S WHERE sno = '%s';" % self.userName
        cursor.execute(ss)
        # results is a tuple
        results = cursor.fetchall()
        for row in results:
            myTuple = (row[0], row[1], int(row[2]), row[3], row[4])
            self.studentInfo_list.append(myTuple)


        self.hasAttended_list = []
        # List: has attended class:
        hasAttendedStr = "SELECT C.cno, C.cname, SC.grade FROM C, SC \
                  WHERE C.cno = SC.cno AND SC.sno = '%s';" % self.userName
        cursor.execute(hasAttendedStr)
        results = cursor.fetchall()
        for row in results:
            myTuple = (row[0], row[1], int(row[2]))
            self.hasAttended_list.append(myTuple)


        self.selectable_list = []
        # List: selectable class
        selectableStr = "SELECT * FROM C;"
        cursor.execute(selectableStr)
        selectableResults = cursor.fetchall()
        for row in selectableResults:
            selectableTuple = (row[0], row[1], int(row[2]), row[3], row[4])
            self.selectable_list.append(selectableTuple)

        # List: selected class: []
        self.selected_list = self.selectable_list

        # Labels:
        self.studentInfo_label = Gtk.Label("Stuent Information: ")
        self.hasAttended_label = Gtk.Label("Has Attended Class: ")
        self.selectable_label = Gtk.Label("Selectable Class: ")
        self.selected_label = Gtk.Label("Has Selected Class: ")
        self.entry_label = Gtk.Label("Type the Class No. : ")

        # Entry
        self.entry = Gtk.Entry()

        # Buttons:
        look_grade_record_button = Gtk.Button(label = "Grade Record")
        look_grade_record_button.connect("clicked", self.on_look_grade_record_clicked)
        take_the_class_button = Gtk.Button(label = "Take")
        take_the_class_button.connect("clicked", self.on_take_the_class_clicked)
        drop_the_closs_button = Gtk.Button(label = "Drop")
        drop_the_closs_button.connect("clicked", self.on_drop_the_class_clicked)
        close_button = Gtk.Button(label = "Close")
        close_button.connect("clicked", self.on_close_clicked)


        # TreeView: student information-----------------------------------------
        # Creating the ListStore model
        self.studentInfo_liststore = Gtk.ListStore(str, str, int, str, str)
        for studentInfo_ref in self.studentInfo_list:
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
        for hasAttended_ref in self.hasAttended_list:
            self.hasAttended_liststore.append(list(hasAttended_ref))

        self.hasAttended_filter = self.hasAttended_liststore.filter_new()

        self.hasAttendedTreeview = Gtk.TreeView.new_with_model(self.hasAttended_filter)
        for i, column_title in enumerate(["class id", "name", "grade"]):
            hasAttended_renderer = Gtk.CellRendererText()
            hasAttended_column = Gtk.TreeViewColumn(column_title, hasAttended_renderer, text = i)
            self.hasAttendedTreeview.append_column(hasAttended_column)


        # TreeView: selectable class--------------------------------------------
        # Creating the ListStore model
        self.selectable_liststore = Gtk.ListStore(str, str, int, str, str)
        for selectable_ref in self.selectable_list:
            self.selectable_liststore.append(list(selectable_ref))

        self.selectable_filter = self.selectable_liststore.filter_new()

        self.selectableTreeview = Gtk.TreeView.new_with_model(self.selectable_filter)
        for i, column_title in enumerate(["id", "name", "credit", "college", "teacher"]):
            selectable_renderer = Gtk.CellRendererText()
            selectable_column = Gtk.TreeViewColumn(column_title, selectable_renderer, text = i)
            self.selectableTreeview.append_column(selectable_column)


        # TreeView: selected class----------------------------------------------
        self.selected_liststore = Gtk.ListStore(str, str, int, str, str)
        for selected_ref in self.selected_list:
            self.selected_liststore.append(list(selected_ref))

        self.current_filter_cnoList = []
        ss = "SELECT cno FROM Selected WHERE sno = '%s';" % userName
        cursor.execute(ss)
        results = cursor.fetchall()
        for row in results:
            self.current_filter_cnoList.append(row[0])


        self.selected_filter = self.selected_liststore.filter_new()
        self.selected_filter.set_visible_func(self.selected_filter_func)

        self.selectedTreeview = Gtk.TreeView.new_with_model(self.selected_filter)
        for i, column_title in enumerate(["id", "name", "credit", "college", "teacher"]):
            selected_renderer = Gtk.CellRendererText()
            selected_column = Gtk.TreeViewColumn(column_title, selected_renderer, text = i)
            self.selectedTreeview.append_column(selected_column)


        # setting up the  layout,  putting the treeview in a scrollwindow
        self.grid.add(self.studentInfo_label)

        # Layout: studentInfo
        self.studentInfo_scrollable_treelist = Gtk.ScrolledWindow()
        self.studentInfo_scrollable_treelist.set_vexpand(True)
        # (0: col, 1:row, 2:2*width(label_stuInfo), 2:2*height(label_stuInfo))
        self.grid.attach(self.studentInfo_scrollable_treelist, 0, 1, 2, 2)
        self.studentInfo_scrollable_treelist.add(self.studentInfoTreeview)

        # Layout: hasAttended
        self.grid.attach(self.hasAttended_label, 0, 4, 1, 1)
        self.hasAttended_scrollable_treelist = Gtk.ScrolledWindow()
        self.hasAttended_scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.hasAttended_scrollable_treelist, 0, 5, 2, 6)
        self.hasAttended_scrollable_treelist.add(self.hasAttendedTreeview)

        self.grid.attach(look_grade_record_button, 0, 11, 2, 1)

        # Layout: selectable
        self.grid.attach(self.selectable_label, 2, 0, 1, 1)
        self.selectable_scrollable_treelist = Gtk.ScrolledWindow()
        self.selectable_scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.selectable_scrollable_treelist, 2, 1, 3, 5)
        self.selectable_scrollable_treelist.add(self.selectableTreeview)

        # Layout: selected
        self.grid.attach(self.selected_label, 2, 6, 1, 1)
        self.selected_scrollable_treelist = Gtk.ScrolledWindow()
        self.selected_scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.selected_scrollable_treelist, 2, 7, 3, 5)
        self.selected_scrollable_treelist.add(self.selectedTreeview)

        # Layout:
        self.grid.attach(self.entry_label, 5, 0, 1, 1)
        self.grid.attach(self.entry, 5, 1, 1, 1)
        self.grid.attach(take_the_class_button, 5, 3, 1, 1)
        self.grid.attach(drop_the_closs_button, 5, 5, 1, 1)
        self.grid.attach(close_button, 5, 7, 1, 1)

        self.show_all()

    def selected_filter_func(self, model, iter, data):
        if self.current_filter_cnoList is None:
            return True
        else:
            return model[iter][0] in self.current_filter_cnoList

    # Button Function
    def on_look_grade_record_clicked(self, widget):
        gradeWin = GradeRecord(userName)
        gradeWin.show_all()

    def on_take_the_class_clicked(self, widget):
        cno = self.entry.get_text().upper()
        ss = "SELECT  cno FROM Selected \
                  WHERE sno = '%s' AND cno = '%s';" % (userName, cno)
        cursor.execute(ss)
        result = cursor.fetchone()
        if result is not None:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.OK, "This is an Error MessageDialog")
            dialog.format_secondary_text("You have selected the class...")
            dialog.run()
            dialog.destroy()
        else:
            ss = "SELECT * FROM C WHERE cno = '%s';" % cno
            cursor.execute(ss)
            val = cursor.fetchone()
            sql = "INSERT INTO Selected(sno, cno, cname, credit, cdept, tname) \
            VALUES('%s', '%s', '%s', '%d', '%s', '%s'); \
            " % (self.userName, val[0], val[1], int(val[2]), val[3], val[4])
            cursor.execute(sql)
            db.commit()
            self.current_filter_cnoList.append(cno)
            self.selected_filter.refilter()

    def on_drop_the_class_clicked(self, widget):
        cno = self.entry.get_text().upper()
        sql = "DELETE FROM Selected WHERE sno = '%s' AND \
                    cno = '%s';" % (self.userName, cno)
        cursor.execute(sql)
        db.commit()

        self.current_filter_cnoList = list(set(self.current_filter_cnoList))
        print(self.current_filter_cnoList)

        if  cno in self.current_filter_cnoList:
            self.current_filter_cnoList.remove('%s' % cno)
            self.selected_filter.refilter()
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.OK, "This is an Error MessageDialog")
            dialog.format_secondary_text("Cannot drop a not exist class...")
            dialog.run()
            dialog.destroy()


    def on_close_clicked(self, widget):
        print("Goodby...")
        global database_connection_is_closed

        if database_connection_is_closed == False:
            print("database: close connection...")
            db.close()
            database_connection_is_closed = True
        Gtk.main_quit()
        print("button::%s" % database_connection_is_closed)


class LoginWindow(Gtk.Window):
    """
    Login UI: user login
    """

    def __init__(self):
        # title
        Gtk.Window.__init__(self, title = "Login")

        # grid for layout
        grid = Gtk.Grid()
        self.add(grid)

        # label
        self.userNameLabel = Gtk.Label('UserName: ')
        self.passwdLabel = Gtk.Label('Passwd:     ')

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

        grid.attach(self.loginButton, 1, 2, 1, 1)
        grid.attach(self.closeButton, 2, 2, 1, 1)

    # Login Button
    def on_loginButton_clicked(self, widget):
        # login user group
        # student group
        Students = []
        sql = "SELECT * FROM S;"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            user = row[0]
            pswd = row[6]
            myTuple = (user, pswd)
            Students.append(myTuple)

        # teachers group, 0:0 is test user
        Teachers = [("0", "0")]
        sql = "SELECT DISTINCT * FROM C;"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            myTuple = (row[4], "000")
            Teachers.append(myTuple)

        # login
        global userName
        userName = self.userNameEntry.get_text()
        passwd = self.passwdEntry.get_text()
        # group by
        # student login
        if (userName.upper(), passwd) in Students:
            userName = userName.upper()
            stuWin = StudentWindow(userName)
            stuWin.show_all()

        # studentSuccessfulLogin(userName)
        # teacher login
        elif (userName, passwd) in Teachers:
            print("Teacher login successful")
            teacherWin = TeacherWindow(userName)
            teacherWin.show_all()

            # teacherSuccessfulLogin(userName)
        # error: not in user group or passwd wrong
        else:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.OK, "This is an Error MessageDialog")
            dialog.format_secondary_text("Login Failure:\n userName is wrong or passwd is wrong...")
            dialog.run()
            dialog.destroy()

    # close Button
    def on_closeButton_clicked(self, widget):
        print("Goodby...")
        # close window
        global database_connection_is_closed
        if database_connection_is_closed == False:
            print("close connection...")
            db.close()
            database_connection_is_closed = True
        Gtk.main_quit()

    # visible passwd
    def on_visible_toggled(self, button):
        value = button.get_active()
        self.passwdEntry.set_visibility(value)

if __name__ == '__main__':
    try:
        loginWin = LoginWindow()
        loginWin.connect("delete-event", Gtk.main_quit)
        loginWin.show_all()
        Gtk.main()
    except e:
        print(e)

    if database_connection_is_closed == False:
        print("close connection...")
        db.close()
        database_connection_is_closed = True
