/* mysql -u root -p teach < ./4_9.sql */

USE teach;

SYSTEM echo "4_9. 对于教学数据库中基本表SC，已建立下列视图:";
SYSTEM echo "CREATE VIEW S_GRADE(S#, C_NUM, AVG_GRADE)";
SYSTEM echo "    AS SELECT S#, COUNT(C#), AVG(GRADE)";
SYSTEM echo "        FROM SC";
SYSTEM echo "        GROUP BY SNO";
SYSTEM echo "试判断下列查询和更新是否允许执行. ";
SYSTEM echo "若允许，写出转换到基本表SC上的相应操作。";

CREATE VIEW S_GRADE(sno, c_num, avg_grade) as
    SELECT sno, COUNT(cno), AVG(grade)
    FROM SC
    GROUP BY sno;

SYSTEM echo "1. SELECT * FROM S_GRADE";
SYSTEM echo "Yes: ";

SYSTEM echo "View Result: ";
SELECT * FROM S_GRADE;

SYSTEM echo "Table Result: ";
SELECT sno, COUNT(cno), AVG(grade) FROM  SC GROUP BY sno;
SYSTEM echo "";


SYSTEM echo "2. SELECT sno, c_num FROM S_GRADE";
SYSTEM echo "    WHERE avg_grade > 80";
SYSTEM echo "Yes: ";

SYSTEM echo "View Result: ";
SELECT sno, c_num FROM S_GRADE WHERE avg_grade > 80;

SYSTEM echo "Table Result: ";
SELECT sno, COUNT(cno) FROM SC GROUP BY sno HAVING AVG(grade) > 80;

SYSTEM echo "";


SYSTEM echo "3. SELECT sno, avg_grade FROM S_GRADE";
SYSTEM echo "    WHERE c_num > (SELECT c_num ";
SYSTEM echo "        FROM S_GRADE WHERE sno = 'S4')";
SYSTEM echo "Yes: ";

SYSTEM echo "View Result: ";
SELECT sno, avg_grade FROM S_GRADE
WHERE
    c_num > (SELECT c_num FROM S_GRADE WHERE sno = "S4");

SYSTEM echo "Table Result: ";
SELECT sno, AVG(grade) FROM SC
GROUP BY sno
HAVING COUNT(cno) > (SELECT COUNT(cno) FROM SC WHERE sno = "S4");
SYSTEM echo "";


SYSTEM echo "3. SELECT sno, avg_grade FROM S_GRADE";
SYSTEM echo "    WHERE c_num > (SELECT c_num ";
SYSTEM echo "        FROM S_GRADE WHERE sno = 'S4')";
SYSTEM echo "Yes: ";
SYSTEM echo "with Group by: "

SYSTEM echo "View Result: ";
SELECT sno, avg_grade FROM S_GRADE
WHERE
    c_num > (SELECT c_num FROM S_GRADE WHERE sno = "S4");

SYSTEM echo "Table Result: ";
SELECT sno, AVG(grade) FROM SC
GROUP BY sno
HAVING COUNT(cno) > (SELECT COUNT(cno) FROM SC GROUP BY sno HAVING sno = "S4");
SYSTEM echo "";



SYSTEM echo "4.UPDATE S_GRADE SET c_num = c_num + 1";
SYSTEM echo "No.";
SYSTEM echo "";


SYSTEM echo "5. DELETE FROM S_GRADE WHERE c_num > 4";
SYSTEM echo "No.";
SYSTEM echo "";

DROP VIEW S_GRADE;
