import MySQLdb
# database: testDatabase

# connect example---------------------------------------------------------------
# fetchone example--------------------------------------------------------------
def connectSql():
    # open database connection
    db = MySQLdb.connect("localhost", "root", "1", "testDatabase")

    # prepare a curser object using curser() method
    cursor = db.cursor()

    # execute SQL query using execute() method
    cursor.execute("SELECT VERSION()")

    # fetch a single row using fetchone() method
    data = cursor.fetchone()

    print("Database version: %s." %data)

    #disconnect from server
    db.close()



# creat table example-----------------------------------------------------------
def createTable():
    # open database connection
    db = MySQLdb.connect("localhost", "root", "1", "testDatabase")

    # prepare a curser object using curser() method
    cursor = db.cursor()

    # drop table if it already exist using execute() method
    cursor.execute("DROP TABLE IF EXISTS EMPLOYEE;")

    # create table as per requirement
    sql = """CREATE TABLE EMPLOYEE (
                   FIRST_NAME CHAR(20) NOT NULL,
                   LAST_NAME CHAR(20),
                   AGE INT,
                   SEX CHAR(1),
                   INCOME FLOAT);
    """

    cursor.execute(sql)

    # disconnect from server
    db.close()



# insert values into table example----------------------------------------------
def insert():
    db = MySQLdb.connect("localhost", "root", "1", "testDatabase")
    cursor = db.cursor()

    # prepare sql query to insert a record into the database
    sql = """INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)
                   VALUES ('Mac', 'Mahan', 20, 'M', 2000)
    """
    try:
        # execute the sql command
        cursor.execute(sql)
        # commit your changes in the database
        db.commit()
    except:
        # rollback in case there is any error
        db.rollback()

    db.close()
# insert values into table example----------------------------------------------
def insertDynamic():
    db = MySQLdb.connect("localhost", "root", "1", "testDatabase")
    cursor = db.cursor()
    # prepare sql query to insert a record into the database
    sql = "INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) \
                  VALUES ('%s', '%s', '%d', '%c', '%f'); " % \
                  ('Mac', 'Mahan', 20, 'M', 2000)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()

    db.close()



# find income over 1000 and print in screen example-----------------------------
def findIncomeOver1000():
    db = MySQLdb.connect("localhost", "root", "1", "testDatabase")
    cursor = db.cursor()
    # prepare sql query to insert a record into the database
    sql = "SELECT * FROM EMPLOYEE WHERE INCOME > %f;" % (1000)

    cursor.execute(sql)

    try:
        # fetch all the rows in a list of lists
        results = cursor.fetchall()
        for row in results:
            fname = row[0]
            lname = row[1]
            age = row[2]
            sex = row[3]
            income = row[4]
            print("fname = %s, lname = %s, age = %d, sex = %s, income = %f" % \
                     (fname, lname, age, sex, income))
    except:
        print("Error: unable to fetch data! ")
    db.close()



# update example----------------------------------------------------------------
def update():
    db = MySQLdb.connect("localhost", "root", "1", "testDatabase")
    cursor = db.cursor()
    sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
    cursor.execute(sql)
    try:
        # commit your changes in the database
        db.commit()
    except:
        # rollback in case there is any error
        db.rollback
    db.close()



# delete example----------------------------------------------------------------
def delete():
    db = MySQLdb.connect("localhost", "root", "1", "testDatabase")
    cursor = db.cursor()
    sql = "DELETE FROM EMPLOYEE WHERE AGE > '%d'" % (20)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()


# Test:
connectSql()
createTable()
insertDynamic()
findIncomeOver1000()
update()
findIncomeOver1000()
delete()
findIncomeOver1000()

# C-x r t
# C-x r k
