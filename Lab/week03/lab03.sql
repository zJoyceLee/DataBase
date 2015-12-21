/* mysql -u root -p make_ten_million < ./lab03.sql */
/*
USE make_ten_million;

DROP INDEX name_ASC on make_ten_million;

SYSTEM echo "1. 验证在1000万个以上记录时在索引和不索引时的查询时间区别: "
SYSTEM echo "Without  index: "
SELECT id, name FROM make_ten_million WHERE name = 'n10024';

SYSTEM echo "Create a index id_ASC: "
CREATE INDEX name_ASC on make_ten_million(name ASC);

SYSTEM echo "With index: "
SELECT id, name FROM  make_ten_million WHERE name = 'n10024';
SYSTEM  echo "";
*/

USE school;

SYSTEM echo "2. 查询每个学生选课情况（包括没有选修课程的学生）: "
SELECT DISTINCT
    Students.id as S_id,
    Students.name as S_name,
    CourseSelection.semester,
    CourseSelection.teacher_id as T_id,
    /*Teachers.name,*/
    CourseSelection.course_id
    /*Courses.name as course_name*/
FROM
     (Students, Courses, Teachers) LEFT JOIN CourseSelection
     ON
          Students.id = CourseSelection.student_id AND
          Courses.id = CourseSelection.course_id AND
          Teachers.id = CourseSelection.teacher_id
WHERE
    Students.id NOT IN (SELECT student_id FROM CourseSelection) OR
    NOT(Teachers.id IS NULL or
            Semester IS  NULL or
            Courses.id IS  NULL )
GROUP BY
    S_id,
    S_name,
    CourseSelection.semester,
    course_id,
    teacher_id;
    /*course_name,
    Teachers.name;*/
SYSTEM echo "";

CREATE TEMPORARY TABLE CS_tmp SELECT * FROM CourseSelection;
CREATE TEMPORARY TABLE S_tmp SELECT * FROM Students;
CREATE TEMPORARY TABLE OC_tmp SELECT * FROM OpenCourses;
SYSTEM echo "Add a student who has taken part in all courses. ";
INSERT INTO S_tmp(id, name, gender, birthday, birthplace, cellphone, college_id) VALUES
("1108", "李羽", "女", "1995-03-09", "上海", "12317897890", "01");

INSERT INTO OC_tmp(semester, course_id, teacher_id, time) VALUES
("2013-2014秋季", "08301001", "0101", "星期一5-8");

INSERT INTO CS_tmp(student_id, semester, course_id, teacher_id, usual_time_score, exam_score, overall_score) VALUES
("1108",  "2012-2013秋季", "08305001", "0103", 60, 60, 60),
("1108",  "2012-2013冬季", "08305002", "0101", 60, 60, 60),
("1108",  "2012-2013冬季", "08305003", "0102", 60, 60, 60),
("1108",  "2013-2014秋季", "08305004", "0101", 60, 60, 60),
("1108",  "2013-2014冬季", "08302001", "0101", 60, 60, 60),
("1108",  "2013-2014秋季", "08301001", "0101", 60, 60, 60);

SYSTEM echo "3. 检索所有课程都选修的的学生的学号与姓名: "
SELECT S_tmp.id, S_tmp.name
FROM S_tmp
WHERE NOT EXISTS (
    SELECT * FROM Courses WHERE NOT EXISTS (
        SELECT * FROM CS_tmp
        WHERE S_tmp.id = CS_tmp.student_id AND
                      Courses.id = CS_tmp.course_id));
SYSTEM echo "";
DROP TABLE S_tmp;
DROP TABLE OC_tmp;
DROP TABLE CS_tmp;

SYSTEM echo "4. 检索选修课程包含1106同学所学全部课程的学生学号和姓名。";
SELECT DISTINCT
    Students.id,
    Students.name
FROM
    Students
WHERE
    NOT EXISTS (
        SELECT * FROM CourseSelection AS CS1 WHERE
            CS1.student_id = '1106' AND
            NOT EXISTS (
                SELECT * FROM CourseSelection AS CS2 WHERE (
                    CS2.student_id != '1106' AND
                    CS2.student_id = Students.id AND
                    CS2.course_id = CS1.course_id)));
SYSTEM echo "";

SYSTEM echo "5. 查询每门课程中分数最高的学生学号和学生姓名: ";
/*
SELECT X.course_id, X.student_id as S_id, Students.name, X.overall_score
FROM CourseSelection as X, Students
GROUP BY X.course_id, S_id, Students.name, X.overall_score
WHERE
    X.student_id = Students.id AND
    NOT EXISTS (
    SELECT * FROM CourseSelection as Y
    WHERE Y.overall_score > X.overall_score)
ORDER BY
    1, 2;
*/

SELECT
    CourseSelection.course_id,
    CourseSelection.student_id as S_id,
    Students.name,
    CourseSelection.overall_score
FROM CourseSelection, Students
WHERE
    Students.id = CourseSelection.student_id AND
    CourseSelection.overall_score IN (
        SELECT MAX(overall_score)
        FROM CourseSelection
        GROUP BY CourseSelection.course_id);

SYSTEM echo "";

SYSTEM echo "6.查询年龄小于本学院平均年龄，所有课程总评成绩";
SYSTEM echo "都高于所选课程平均总评成绩的学生学号、姓名和平";
SYSTEM echo "均总评成绩，按年龄排序: ";
/*
SELECT CourseSelection.student_id, Students.name, AVG(overall_score) as AvgScore
FROM CourseSelection, Students
WHERE
    CourseSelection.student_id = Students.id, Student AND
    (YEAR(CURDATE()) - YEAR(Students.birthday)) < (
        SELECT AVG(YEAR(CURDATE())-YEAR(Students.birthday))
        FROM Students, Colleges
        WHERE
            Students.college_id = Colleges.id
        GROUP BY Students.birthday)
GROUP BY
    CourseSelection.student_id,
    Students.name;

SELECT id, name, YEAR(CURDATE()) - YEAR(Students.birthday) as age, college_id FROM Students
WHERE (YEAR(CURDATE())-YEAR(Students.birthday)) < AVG(YEAR(CURDATE())-YEAR(Students.birthday))
GROUP BY Students.birthday;
*/

SELECT DISTINCT
    Students.id as S_id,
    Students.name,
    AVG(CourseSelection.overall_score) AS "AVG Overall Score"
FROM
    Students,
    CourseSelection,
    (
        SELECT
            CourseSelection.course_id,
            AVG(CourseSelection.overall_score) AS avg_score
        FROM
            CourseSelection
        GROUP BY
            CourseSelection.course_id
        ) AS AVGScoreTable,
    (
       SELECT
           Students.id,
           YEAR(CURDATE()) - YEAR(Students.birthday) AS age,
           Students.college_id
       FROM
           Students
    ) AS AgeTable,
    (
         SELECT
             Students.college_id,
             AVG(YEAR(CURDATE()) - YEAR(Students.birthday)) AS avg_age
         FROM
             Students
         GROUP BY
             Students.college_id
     ) AS AVGAgeTable
WHERE
    Students.id = CourseSelection.student_id AND
    Students.id = AgeTable.id AND
    Students.college_id = AgeTable.college_id AND
    CourseSelection.course_id = AVGScoreTable.course_id AND
    CourseSelection.overall_score > AVGScoreTable.avg_score AND
    AgeTable.age < AVGAgeTable.avg_age
GROUP BY
    Students.id
ORDER BY
    AgeTable.age ASC;

SYSTEM echo "";
