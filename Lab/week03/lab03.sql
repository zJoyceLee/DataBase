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

SYSTEM echo "Add a student who has taken part in all courses. ";
INSERT INTO Students(id, name, gender, birthday, birthplace, cellphone, college_id) VALUES
("1108", "李羽", "女", "1995-03-09", "上海", "12317897890", "01");

INSERT INTO OpenCourses(semester, course_id, teacher_id, time) VALUES
("2013-2014秋季", "08301001", "0101", "星期一5-8");

INSERT INTO CourseSelection(student_id, semester, course_id, teacher_id, usual_time_score, exam_score, overall_sore) VALUES
("1108",  "2012-2013秋季", "08305001", "0103", null, null, null),
("1108",  "2012-2013冬季", "08305002", "0101", null, null, null),
("1108",  "2012-2013冬季", "08305003", "0102", null, null, null),
("1108",  "2013-2014秋季", "08305004", "0101", null, null, null),
("1108",  "2013-2014冬季", "08302001", "0101", null, null, null),
("1108",  "2013-2014秋季", "08301001", "0101", null, null, null);

SYSTEM echo "3. 检索所有课程都选修的的学生的学号与姓名: "
SELECT Students.id, Students.name
FROM Students
WHERE NOT EXISTS (
    SELECT * FROM Courses WHERE NOT EXISTS (
        SELECT * FROM CourseSelection
        WHERE Students.id = CourseSelection.student_id AND
                      Courses.id = CourseSelection.course_id));
SYSTEM echo "";

SYSTEM echo "4. 检索选修课程包含1106同学所学全部课程的学生学号和姓名。";
SELECT
    Students.id,
    Students.name
FROM Students
WHERE
