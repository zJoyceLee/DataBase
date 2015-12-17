/* mysql -u root -p teach < ./4_6.sql */

USE teach;

SYSTEM echo "4_6. 试用SQL查询语句表达下列对教学数据库中三个基本表S、SC、C的查询："
SYSTEM echo "1. 统计有学生选修的课程门数: ";
SELECT COUNT(C.cno) as "HaveStudent" FROM C WHERE C.cno IN (
    SELECT SC.cno FROM SC);
SYSTEM echo "";

SYSTEM echo "2. 求选修C4课程的学生的平均年龄: ";
SELECT AVG(S.age) as "AverageAge" FROM S, SC
WHERE S.sno = SC.sno AND SC.cno = "C4";
SYSTEM echo "";

SYSTEM echo "3. 求LIU老师所授课程的每门课程的学生平均成绩: ";
SELECT SC.cno, AVG(SC.grade) as "AverageGrade" FROM SC
GROUP BY SC.cno HAVING SC.cno IN (
    SELECT C.cno FROM C WHERE C.tname = "liu");
SYSTEM echo "";

SYSTEM echo "4. 统计每门课程的学生选修人数(超过10人的课程才统计).";
SYSTEM echo "要求输出课程号和选修人数，查询结果按人数降序排列，";
SYSTEM echo "若人数相同，按课程号升序排列: ";
SELECT SC.cno, COUNT(SC.sno) FROM SC
GROUP BY SC.cno HAVING COUNT(SC.sno) > 10
ORDER BY 2 DESC, 1;
SYSTEM echo ""

SYSTEM echo "5. 检索学号比WANG同学大，而年龄比他小的学生姓名: ";
SELECT X.sname FROM S as X
WHERE
    X.sno > SOME(SELECT sno FROM S as Y WHERE Y.sname LIKE "wang%" AND X.age < Y.age);
/*
    X.sno > ALL(SELECT sno FROM S WHERE sname LIKE  "wang%") AND
    X.age < ALL(SELECT sno FROM S WHERE sname LIKE "wang%");
*/
SYSTEM echo "";

SYSTEM echo "6. 检索姓名以WANG打头的所有学生的姓名和年龄: ";
SELECT sname, age FROM S WHERE Sname LIKE "wang%";
SYSTEM echo "";

SYSTEM echo "7. 在SC中检索成绩为空值的学生学号和课程号: ";
SELECT sno, cno FROM SC WHERE grade IS NULL;
SYSTEM echo "";

SYSTEM echo "8. 求年龄大于女同学平均年龄的男学生姓名和年龄: ";
SELECT sname, age FROM S
WHERE
    sex = "M" AND
    age > (SELECT AVG(age) FROM S WHERE sex = "F");
SYSTEM echo "";

SYSTEM echo "9. 求年龄大于所有女同学年龄的男学生姓名和年龄: ";
SELECT sname, age FROM S
WHERE
    sex = "M" AND
    age > ALL(SELECT age FROM S WHERE sex = "F");
SYSTEM echo "";
