import MySQLdb

# print Table
def printResult(cursor, sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print(row)
    print("\n")


# Students:operate after login successful---------------------------------------
def studentSuccessfulLogin(userName):
    db = MySQLdb.connect("localhost", "root", "1", "mySchool")
    cursor = db.cursor()

    # Student Information-------------------------------------------------------
    def studentInformation():
        print("Student Information: ")
        sql = "SELECT * FROM S WHERE sno = '%s';" % userName
        printResult(cursor, sql)


    # Has Attended Class--------------------------------------------------------
    def hasAttendedClass():
        print("Has Attended Class: ")
        sql = "SELECT C.cno, C.cname FROM C WHERE C.cno IN ( \
        SELECT SC.cno FROM SC WHERE SC.sno = '%s');" % userName
        printResult(cursor, sql)


    # Selectable Class----------------------------------------------------------
    def selectableClass():
        print("Selectable Class: ")
        sql = "SELECT * FROM C;"
        printResult(cursor, sql)


    # Has Selected Class--------------------------------------------------------
    def hasSelectedClass():
        print("Has Selected Class: ")
        sql = "SELECT cno, cname, credit, cdept, tname \
                   FROM Selected WHERE sno = '%s';" % userName
        printResult(cursor, sql)


    # input cno for operating
    def inputCno():
        cno = raw_input("Please enter cno: ")
        cno = cno.upper()
        return cno


    # Select Class--------------------------------------------------------------
    def selectClass():
        print("Select Class: ")
        cno = inputCno()
        ss = "SELECT * FROM C WHERE cno = '%s'" % cno
        cursor.execute(ss)
        results = cursor.fetchall()
        for row in results:
            cname = row[1]
            credit = row[2]
            cdept = row[3]
            tname = row[4]
        sql = "INSERT INTO Selected(sno, cno, cname, credit, cdept, tname) VALUES \
        ('%s', '%s', '%s', '%d', '%s', '%s');" % (userName, cno, cname, credit, cdept, tname)
        cursor.execute(sql)
        db.commit()
        hasSelectedClass()


    # Delete Class--------------------------------------------------------------
    def deleteClass():
        print("Delete Class: ")
        cno = inputCno()
        sql = "DELETE FROM Selected WHERE sno = '%s' AND cno = '%s'" % (userName, cno)
        cursor.execute(sql)
        db.commit()
        hasSelectedClass()


    # grade record
    def gradeRecord():
        sql = "SELECT C.cno, C.cname, SC.grade, C.credit, C.tname \
                   FROM C, SC WHERE C.cno = SC.cno AND SC.sno = '%s';" % userName
        cursor.execute(sql)
        results =  cursor.fetchall()
        print("%s Grade Record: " %  userName)
        for row in results:
            cno = row[0]
            cname = row[1]
            grade = row[2]
            credit = row[3]
            tname = row[4]
            print("'%s', '%s', %d, %d, '%s'" % (cno, cname, grade, credit, tname))



    studentInformation()
    hasAttendedClass()
    selectableClass()
    selectClass()
    selectClass()
    deleteClass()
    gradeRecord()

    db.close()




# print table and record count
def printTableAndLen(cursor, sql):
    cursor.execute(sql)
    results = cursor.fetchall()
    counter = len(results)
    print("Record Counter: %d" % counter)
    for row in results:
        print(row)
    print("\n")


# Teachers Successful Login
def teacherSuccessfulLogin(userName):
    db = MySQLdb.connect("localhost", "root", "1", "mySchool")
    cursor = db.cursor()

    # display student information
    def studentMaintenance():
        print("Students Information: ")
        sql = "SELECT * FROM S;"
        printTableAndLen(cursor, sql)


    # display class information
    def classMaintenance():
        print("Class Information: ")
        sql = "SELECT * FROM C;"
        printTableAndLen(cursor, sql)


    # display Sno and grade
    def theSnoAndGrade(tname, cname):
        print("This Sno and Grade: ")
        sql = "SELECT SC.sno, SC.grade FROM SC WHERE SC.cno IN (\
        SELECT C.cno FROM C \
        WHERE C.tname = '%s' AND C.cname = '%s');" % (tname, cname)
        printResult(cursor, sql)

    # alter grade
    def alterGrade(cname):
        ss = "SELECT cno FROM C WHERE cname = '%s';" % cname
        cursor.execute(ss)
        result = cursor.fetchone()
        cno = result[0]
        changedSno = raw_input("Change Sno: ")
        changedSno = changedSno.upper()
        newGrade = raw_input(" to ")
        newGrade = int(newGrade)
        sql = "DELETE FROM SC WHERE sno = '%s' \
                   AND cno = '%s';"% (changedSno, cno)
        cursor.execute(sql)
        db.commit()
        sql = "INSERT INTO SC(sno, cno, grade) VALUES \
                   ('%s', '%s', %d)" % (changedSno, cno, newGrade)
        cursor.execute(sql)
        db.commit()
        theSnoAndGrade(userName, cname)


    # print grade distribution
    def gradeDistribution():
        pass



    # selectable class
    def chooseCname():
        print("Please choose cname: ")
        sql = "SELECT cname FROM C WHERE tname = '%s';" % userName
        printResult(cursor, sql)
        cname = raw_input("Cname: ")
        theSnoAndGrade(userName, cname)
        alterGrade(cname)





    studentMaintenance()
    classMaintenance()
    chooseCname()





# login user group
# students group
Students = [("S1", "001"), ("S2", "002"), ("S3", "003"), ("S4", "004"),
       ("S5", "005"), ("S6", "006"), ("S7", "007"), ("S8", "008"), ("S9", "009")]
# teachers group
Teachers= [("WangXiaoming", "000"), ("LiuHong", "000"),
           ("LiJinyan", "000"), ("WuZhigang", "000"), ("JiangYingyue", "000"), ]

# login
userName = raw_input("user name: ")
passwd = raw_input("passwd: ")

# group by
# student login
if (userName.upper(), passwd) in Students:
    userName = userName.upper()
    print("user login successful! \n")
    studentSuccessfulLogin(userName)
# teacher login
elif (userName, passwd) in Teachers:
    print("user login successful! \n")
    teacherSuccessfulLogin(userName)
# error
else:
    print("user login failure! \n")
