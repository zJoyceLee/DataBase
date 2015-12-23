/* mysql -u root -p school < ./test.sql */

SYSTEM echo "1. 用四种方法表达查询：检索马小红老师所授课程的学期，课程号，上课时间: "
SYSTEM echo "(1) 多表连接: "
SELECT DISTINCT LEFT(semester, 9) as "School Year", RIGHT(semester, 2) as "Semester", course_id, time
FROM OpenCourses, Teachers
WHERE OpenCourses.teacher_id = Teachers.id AND Teachers.name = "马小红";
SYSTEM echo;

SYSTEM echo "(2) 嵌套: "
SELECT DISTINCT LEFT(semester, 9) as "School Year", RIGHT(semester, 2) as "Semester", course_id, time
FROM OpenCourses
WHERE teacher_id = (SELECT DISTINCT id FROM Teachers WHERE name = "马小红");
SYSTEM echo;

SYSTEM echo "(3) in: "
SELECT DISTINCT LEFT(semester, 9) as "School Year", RIGHT(semester, 2) as "Semester", course_id, time
FROM OpenCourses
WHERE teacher_id IN (SELECT id FROM Teachers WHERE name = "马小红");
SYSTEM echo;

SYSTEM echo "(4) Substring: "
SELECT DISTINCT SUBSTRING(semester, 1, 10) as "School Year", SUBSTRING(semester, 10, 2) as "Semester", course_id, time
FROM OpenCourses, Teachers
WHERE OpenCourses.teacher_id = Teachers.id AND Teachers.name = "马小红";
SYSTEM echo;

SYSTEM echo "(5) Exists: "
SELECT DISTINCT SUBSTRING(semester, 1, 10) as "School Year", SUBSTRING(semester, 10, 2) as "Semester", course_id, time
FROM OpenCourses
WHERE EXISTS (SELECT * FROM Teachers WHERE OpenCourses.teacher_id = Teachers.id and Teachers.name = "马小红");
SYSTEM echo;


SYSTEM echo "(6) Exists: "
SELECT DISTINCT SUBSTRING(semester, 1, 10) as "School Year", SUBSTRING(semester, 10, 2) as "Semester", course_id, time
FROM OpenCourses
WHERE EXISTS (SELECT * FROM Teachers WHERE name = "马小红");
SYSTEM echo;


SYSTEM echo "2. 检索有学生重修的教师编号和姓名: "
SYSTEM echo "(1) 嵌套: "
SELECT DISTINCT id, name
FROM Teachers
WHERE id = (SELECT DISTINCT CS1.teacher_id 
            FROM CourseSelection as CS1, CourseSelection as CS2 
            WHERE CS1.student_id = CS2.student_id AND CS1.course_id = CS2.course_id AND CS1.semester > CS2.semester);
SYSTEM echo;

SYSTEM echo "(2) 多表连接: "
SELECT DISTINCT Teachers.id, Teachers.name
FROM Teachers, CourseSelection as CS1, CourseSelection as CS2 
WHERE CS1.student_id = CS2.student_id AND CS1.course_id = CS2.course_id AND CS1.semester > CS2.semester AND Teachers.id = CS1.teacher_id;
SYSTEM echo;

/*SYSTEM echo "(3) Group by: "
SELECT DISTINCT id, name
FROM Teachers, 
WHERE id in (SELECT CourseSelection.teacher_id 
            FROM CourseSelection 
            GROUP BY CourseSelection.student_id 
            HAVING COUNT(CourseSelection.course_id) > 1);
SYSTEM echo;*/
