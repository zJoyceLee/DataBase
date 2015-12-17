/* mysql -u root -p teach < ./4_2.sql  */

SYSTEM echo "4.2 对于教学数据库的三个基本表,  试用SQL的查询语句表达下列查询："
SYSTEM echo "1. 检索liu老师所授课程的课号和课名：";
SELECT cno,cname FROM C WHERE tname = "liu";
SYSTEM echo "";

SYSTEM echo "2. 检索年龄大于23岁的男学生的学号和姓名: ";
SELECT sno, sname FROM S WHERE age > 23 AND sex = "M";
SYSTEM echo "";

SYSTEM echo "3. 检索学号为S3的学生所学课程的课程名和任课教师名: ";
SELECT cname, tname FROM C WHERE cno IN (
    SELECT SC.cno FROM SC WHERE SC.sno = "S3");
SYSTEM echo"";

SYSTEM echo "4. 检索至少选修LIU老师所授课程中一门课程的女学生姓名: ";
SELECT S.sname FROM S WHERE S.sex = "F" AND S.sno IN (
    SELECT SC.sno FROM SC WHERE SC.cno IN (
        SELECT C.cno FROM C WHERE C.tname = "liu"));
SYSTEM echo"";

SYSTEM echo "5. 检索WANG同学不学的课程的课程号:  ";
SELECT C.cno FROM C WHERE C.cno NOT IN (
    SELECT SC.cno FROM SC WHERE SC.sno = (
        SELECT DISTINCT S.sno FROM S WHERE S.sname like "wang%"));
SYSTEM echo "";

SYSTEM echo "6. 检索至少选修两门课程的学生学号:  ";
SELECT sno FROM SC GROUP BY sno HAVING COUNT(cno) >= 2;
SYSTEM echo "";

SYSTEM echo "7. 检索全部学生都选修的课程的课程号与课程名: ";
SELECT C.cno, C.cname FROM C WHERE NOT EXISTS(
    SELECT * FROM S WHERE NOT EXISTS(
        SELECT * FROM SC WHERE SC.sno = S.sno AND SC.cno = C.cno));
SYSTEM echo "";

SYSTEM echo "8. 检索选修课程包含LIU老师所授课的学生学号: ";
SELECT SC.sno FROM SC WHERE SC.cno IN (
    SELECT C.cno FROM C WHERE C.tname = "liu");
SYSTEM echo "";
