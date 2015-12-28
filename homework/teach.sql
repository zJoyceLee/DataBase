/* mysql -u root -p < ./teach.sql */

DROP DATABASE IF EXISTS teach;
CREATE DATABASE teach CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE teach;

CREATE TABLE S (
    sno CHAR(2) NOT NULL,
    sname CHAR(8) NOT NULL,
    age INT(2),
    sex CHAR(2),
    sdept CHAR(10),
    PRIMARY KEY(sno)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE Students (
    sno CHAR(2) NOT NULL,
    sname CHAR(8) NOT NULL,
    sex CHAR(2)
) ENGiNE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE C (
    cno CHAR(2) NOT NULL,
    cname CHAR(10) NOT NULL,
    cdept CHAR(10),
    tname CHAR(10),
    PRIMARY KEY(cno)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE SC (
    sno CHAR(2) NOT NULL,
    cno CHAR(2) NOT NULL,
    grade INT(3),
    PRIMARY KEY(sno, cno),
    FOREIGN KEY(sno) REFERENCES S(sno),
    FOREIGN KEY(cno) REFERENCES C(cno)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

INSERT INTO S(sno, sname, age, sex, sdept) VALUES
("S1", "chengh", 19, "M", "计算机"),
("S3", "liuss", 19, "F", "通讯"),
("S4", "ligq", 19, "M", "法学"),
("S6", "jiangty", 19, "M", "国际贸易"),
("S8", "wangl", 19, "F", "计算机"),
("S9", "Lee", 18, "F", "计算机"),
("S2", "Joyce", 25, "F", "计算机"),
("S5", "Poker", 26, "M", "计算机");

INSERT INTO C(cno, cname, cdept, tname) VALUES
("C2", "离散数学", "计算机", "wanghw"),
("C3", "maths", "通讯", "qianh"),
("C4", "数据结构", "计算机", "mal"),
("C1", "计算机原理", "计算机", "li"),
("C5", "DB", "计算机", "liu"),
("C6", "Analyze", "计算机", "shangb");

INSERT INTO SC(sno, cno, grade) VALUES
("S3", "C3", 87),
("S1", "C2", 88),
("S4", "C3", 79),
("S8", "C4", 83),
("S1", "C3", 76),
("S6", "C3", 68),
("S1", "C1", 78),
("S6", "C1", 88),
("S3", "C2", 64),
("S1", "C4", 86),
("S8", "C2", 78),
("S1", "C5", 90),
("S2", "C5", NULL),
("S8", "C3", 30),
("S2", "C3", 56),
("S9", "C3", NULL),
("S5", "C3", 90);
