import MySQLdb

db = MySQLdb.connect("localhost", "root", "1", "make_ten_million")

cursor = db.cursor()

cursor.execute("CREATE TABLE  make_ten_million("
               "id int(8) NOT NULL, name char(20) NOT NULL, PRIMARY KEY (id)"
               ") ENGINE=InnoDB DEFAULT CHARSET=utf8;")

# cursor.execute("CREATE INDEX id_ASC on  make_ten_million(id ASC);")

# cursor.execute("CREATE INDEX id_DEC on  make_ten_million(id DEC);")

for i in range(0, 10000):
    ss = "INSERT  INTO make_ten_million(id, name) VALUES"

    for j  in range(0, 1000):
        ss += ( "('" + str(i*1000 + j) + "', 'n" + str(i*1000 + j) + "'),\n")

    ss = ss[:-2]
    ss += ";"

    cursor.execute(ss)
    db.commit()
    print "execute "  + str(i * 1000 + j)  + "finished!\n!"
