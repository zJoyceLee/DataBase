/* mysql -u root -p teach < ./4_7.sql */

USE teach;

SYSTEM echo "4_7. 试用SQL更新语句表达对教学数据库中三个基本表S、SC、C的各个更新操作: ";
SYSTEM echo "S Table: ";
SELECT * FROM S;

SYSTEM echo "1. 往基本表S中插入一个学生元组('S0', 'WU', 18): ";
INSERT INTO S(sno, sname, age, sex, sdept) VALUES
("S0", "WU", 18, NULL, NULL);

SYSTEM echo "After Insert into S: ";

SELECT * FROM S;
SYSTEM echo "";

SYSTEM echo "2. 在基本表S中检索每一门课程成绩都大于等于80分的学生学号、姓名和性别,";
SYSTEM echo "并把检索到的值送往另一个已存在的基本表Students(S＃，SANME，SEX): ";
SELECT sno, sname, sex FROM S
WHERE
    sno NOT IN (SELECT sno FROM SC WHERE (grade < 80 OR grade IS NULL)) AND
    sno IN (SELECT sno FROM SC);

SYSTEM echo "Students Table: ";
SELECT * FROM Students;

INSERT INTO Students(sno, sname, sex)
    SELECT sno, sname, sex FROM S
    WHERE
        sno NOT IN (SELECT sno FROM SC WHERE (grade < 80 OR grade IS NULL)) AND
        sno IN (SELECT sno FROM SC);
SYSTEM echo "After Insert into Students:  ";
SELECT * FROM Students;
SYSTEM echo "";

SYSTEM echo "3. 在基本表SC中删除尚无成绩的选课元组: ";
SYSTEM echo "SC Table: ";
SELECT * FROM SC;

DELETE FROM SC
WHERE grade IS NULL;

SYSTEM echo "After delete SC: ";
SELECT * FROM SC;
SYSTEM echo "";

SYSTEM echo "4. 把WANG同学的学习选课和成绩全部删去: ";
SYSTEM echo "SC Table: ";
SELECT * FROM SC;

DELETE FROM SC
WHERE sno IN (SELECT sno FROM S WHERE sname LIKE "wang%");

SYSTEM echo "After delete SC: ";
SELECT * FROM SC;
SYSTEM echo "";

SYSTEM echo "5. 把选修MATHS课不及格的成绩全改为空值: ";
SYSTEM echo "SC Table: ";
SELECT * FROM SC;

UPDATE SC SET grade = NULL
WHERE
    grade < 60 AND
    cno IN (SELECT C.cno FROM C WHERE C.cname = "maths");

SYSTEM echo "After update SC:  ";
SELECT * FROM SC;
SYSTEM echo "";


CREATE TEMPORARY TABLE SC_tmp SELECT * FROM SC;

SYSTEM echo "6. 把低于总平均成绩的女同学成绩提高5%: ";
SYSTEM echo "SC Table: ";
SELECT * FROM SC;

UPDATE SC SET grade = grade * 1.05
WHERE
    sno IN (SELECT S.sno FROM S WHERE S.sex = "F") AND
    grade < (SELECT AVG(SC_tmp.grade) FROM SC_tmp);

DROP TABLE SC_tmp;

SYSTEM echo "After update SC: ";
SELECT * FROM SC;
SYSTEM echo "";

SYSTEM echo "7. 在基本表SC中修改C4课程的成绩，若成绩小于等于75分时提高5%，";
SYSTEM echo "若成绩大于75分时提高4%(用两个UPDATE语句实现):";
SYSTEM echo "SC Table: ";
SELECT * FROM SC;

UPDATE SC SET grade = grade * 1.04
WHERE cno = "C4" AND grade > 75;

UPDATE SC SET grade = grade * 1.05
WHERE cno = "C4" AND grade <= 75;

SYSTEM echo "After update SC";
SELECT * FROM SC;
SYSTEM echo "";
