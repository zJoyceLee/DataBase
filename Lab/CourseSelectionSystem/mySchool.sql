/* mysql -u root -p < ./mySchool.sql */

DROP DATABASE IF EXISTS mySchool;
CREATE DATABASE mySchool CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE mySchool;

CREATE TABLE S(
    sno CHAR(4),
    sname CHAR(8),
    sex CHAR(2),
    age CHAR(2),
    sdept CHAR(10),
    logn CHAR(20),
    pswd CHAR(20),
    PRIMARY KEY(sno)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;

CREATE TABLE C(
    cno CHAR(4),
    cname CHAR(20),
    credit INTEGER,
    cdept CHAR(10),
    tname CHAR(8),
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

INSERT INTO S(sno, sname, sex, age, sdept, logn, pswd) VALUES
("S1", "李铭", "男", "19", "计算机软件", "S1", "001"),
("S2", "刘晓鸣", "男", "20", "计算机应用", "S2", "002"),
("S3", "李明", "男", "22", "计算机应用", "S3", "003"),
("S4", "张鹰", "女", "21", "计算机软件", "S4", "004"),
("S5", "刘竟静", "女", "22", "计算机软件", "S5", "005"),
("S6", "刘成刚", "男", "21", "计算机软件", "S6", "006"),
("S7", "王铭", "男", "22", "计算机应用", "S7", "007"),
("S8", "宣明尼", "女", "18", "计算机应用", "S8", "008"),
("S9", "柳红利", "女", "19", "计算机软件", "S9", "009");

INSERT INTO C(cno, cname, credit, cdept, tname) VALUES
("C1",  "PASCAL", 4, "计算机应用", "王晓名"),
("C2",  "数据结构", 4, "计算机应用", "刘红"),
("C3",  "离散数学", 4, "计算机应用", "李严劲"),
("C4",  "计算机原理", 6, "计算机软件", "王晓名"),
("C5",  "数据库原理", 4, "计算机应用", "吴志钢"),
("C6",  "Windows技术", 4, "计算机软件", "吴志钢"),
("C8",  "编译原理", 4, "计算机软件", "蒋莹岳"),
("C9",  "系统结构", 6, "计算机应用", "刘红");

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
