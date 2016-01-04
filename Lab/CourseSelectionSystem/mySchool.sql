/* mysql -u root -p < ./mySchool.sql */

DROP DATABASE IF EXISTS mySchool;
CREATE DATABASE mySchool CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE mySchool;

CREATE TABLE S(
    sno CHAR(4),
    sname CHAR(20),
    sex VARCHAR(10),
    age CHAR(2),
    sdept CHAR(20),
    login CHAR(20),
    pswd CHAR(20),
    PRIMARY KEY(sno)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;;

CREATE TABLE C(
    cno CHAR(4),
    cname CHAR(20),
    credit INTEGER,
    cdept CHAR(20),
    tname CHAR(20),
    PRIMARY KEY(cno)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE SC(
    sno CHAR(4),
    cno CHAR(4),
    grade INTEGER,
    PRIMARY KEY(sno, cno),
    FOREIGN KEY(sno) REFERENCES S(sno),
    FOREIGN KEY(cno) REFERENCES C(cno)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE Selected(
    sno CHAR(4),
    cno CHAR(4),
    cname CHAR(20),
    credit INTEGER,
    cdept CHAR(20),
    tname CHAR(20),
    PRIMARY KEY(sno, cno),
    FOREIGN KEY(sno) REFERENCES S(sno),
    FOREIGN KEY(cno) REFERENCES C(cno)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

INSERT INTO S(sno, sname, sex, age, sdept, login, pswd) VALUES
("S1", "LiMing", "M", "19", "Computer Software", "S1", "001"),
("S2", "LiuXiaoming", "M", "20", "Computer Application", "S2", "002"),
("S3", "LiMing", "M", "22", "Computer Application", "S3", "003"),
("S4", "ZhangYing", "F", "21", "Computer Software", "S4", "004"),
("S5", "LiuJingjing", "F", "22", "Computer Software", "S5", "005"),
("S6", "LiuChenggang", "M", "21", "Computer Software", "S6", "006"),
("S7", "WangMing", "M", "22", "Computer Application", "S7", "007"),
("S8", "XuanMingni", "F", "18", "Computer Application", "S8", "008"),
("S9", "LiuHongli", "F", "19", "Computer Software", "S9", "009");

INSERT INTO C(cno, cname, credit, cdept, tname) VALUES
("C1",  "PASCAL", 4, "Computer Application", "WangXiaoming"),
("C2",  "Data Structure", 4, "Computer Application", "LiuHong"),
("C3",  "Discrete Mathematics", 4, "Computer Application", "LiJinyan"),
("C4",  "Computer Principle", 6, "Computer Software", "WangXiaoming"),
("C5",  "Database Principle", 4, "Computer Application", "WuZhigang"),
("C6",  "Windows Technologies", 4, "Computer Software", "WuZhigang"),
("C8",  "Compile Principle", 4, "Computer Software", "JiangYingyue"),
("C9",  "System Structure", 6, "Computer Application", "LiuHong");

INSERT INTO SC(sno, cno, grade) VALUES
("S1", "C2", 56),
("S1", "C4", 78),
("S1", "C6", 66),
("S1", "C8", 88),
("S3", "C1", 88),
("S3", "C2", 76),
("S4", "C1", 67),
("S4", "C2", 76),
("S4", "C3", 67),
("S5", "C1", 67),
("S5", "C2", 78),
("S5", "C3", 91),
("S6", "C1", 78);
