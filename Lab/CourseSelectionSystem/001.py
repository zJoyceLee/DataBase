import MySQLdb

# operate after login successful
def studentInformation():
    db = MySQLdb.connect("localhost", "root", "1", "mySchool", charset = "utf8")
    cursor = db.cursor()

    print("Student Information: \n")
    cursor.execute("SELECT * FROM S WHERE sno = '%s';" % userName)
    results = cursor.fetchall()
    for row in results:
        print(row)
    db.close()


# login
# Sno = {"S1": "001", "S2": "002", "S3":"003", "S4": "004",
#        "S5": "005", "S6": "006", "S7": "007", "S8": "008", "S9": "009"}

userName = raw_input("user name: ")
passwd = raw_input("passwd: ")

Sno = [("S1", "001"), ("S2", "002"), ("S3", "003"), ("S4", "004"),
       ("S5", "005"), ("S6", "006"), ("S7", "007"), ("S8", "008"), ("S9", "009")]

# login
if (userName, passwd) in Sno:
    print("user login successful! ")
    studentInformation()
else:
    print("user login failure! ")
