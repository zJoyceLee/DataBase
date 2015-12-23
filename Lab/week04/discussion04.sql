/* mysql -u root -p school < ./disscussion04.sql */

USE school;

SYSTEM echo "2.1 . 用多种方法表达查询：检索刘晓明不学的课程的课程号: ";

SYSTEM echo "(1) ";
SELECT Courses.id FROM Courses WHERE Courses.id NOT IN (
    SELECT course_id FROM CourseSelection WHERE student_id IN (
        (SELECT Students.id  FROM Students WHERE Students.name = "刘晓明")));

SYSTEM echo "(2) ";
SELECT Courses.id FROM Courses WHERE Courses.id NOT IN (
    SELECT Courses.id FROM Courses, CourseSelection, Students
    WHERE
        Students.name = "刘晓明" AND
        CourseSelection.student_id  = Students.id AND
        Courses.id = CourseSelection.course_id);

SYSTEM echo "(3) ";
SELECT Courses.id FROM Courses WHERE NOT EXISTS (
    SELECT * FROM CourseSelection
    WHERE
        Courses.id = CourseSelection.course_id AND
        CourseSelection.student_id IN (
            SELECT Students.id FROM Students WHERE Students.name = "刘晓明"));
SYSTEM echo "";

SYSTEM echo  "2.2 删除没有开课的学院: ";
CREATE TEMPORARY TABLE Courses_tmp SELECT * FROM Courses;
CREATE TEMPORARY TABLE Students_tmp SELECT * FROM Students;
CREATE TEMPORARY TABLE Teachers_tmp SELECT * FROM Teachers;
CREATE TEMPORARY TABLE Colleges_tmp SELECT * FROM Colleges;

SYSTEM echo "Courses_tmp: ";
SELECT * FROM Courses_tmp;

DELETE FROM Courses_tmp
WHERE Courses_tmp.college_id IN (
    SELECT Courses.college_id FROM Courses WHERE Courses.id NOT IN (
        SELECT OpenCourses.course_id FROM OpenCourses));

SYSTEM echo "Courses_tmp After Delete: ";
SELECT * FROM Courses_tmp;


SYSTEM echo "Students_tmp: ";
SELECT * FROM Students_tmp;

DELETE FROM Students_tmp
WHERE Students_tmp.college_id IN (
    SELECT Courses.college_id FROM Courses WHERE Courses.id NOT IN (
        SELECT OpenCourses.course_id FROM OpenCourses));

SYSTEM echo "Students_tmp After Delete: ";
SELECT * FROM Students_tmp;


SYSTEM echo "Teachers_tmp";
SELECT * FROM Teachers_tmp;

DELETE FROM Teachers_tmp
WHERE Teachers_tmp.college_id IN (
    SELECT Courses.college_id FROM Courses WHERE Courses.id NOT IN (
        SELECT OpenCourses.course_id FROM OpenCourses));

SYSTEM echo "Teachers_tmp After Delete: ";
SELECT * FROM Teachers_tmp;


SYSTEM echo "Colleges_tmp: ";
SELECT * FROM Colleges_tmp;

DELETE FROM Colleges_tmp
WHERE Colleges_tmp.id IN (
    SELECT Courses.college_id FROM Courses WHERE Courses.id NOT IN (
        SELECT OpenCourses.course_id FROM OpenCourses));

SYSTEM echo "Colleges_tmp After Delete: "
SELECT * FROM Colleges_tmp;

DROP TABLE Teachers_tmp;
DROP TABLE Students_tmp;
DROP TABLE Courses_tmp;
DROP TABLE Colleges_tmp;
SYSTEM echo "";

SYSTEM echo "3. VIEW:";
SYSTEM echo "3.1 判断实验课第一题的视图能否更新: ";
SYSTEM echo "建立计算机学院总评不及格成绩学生的视图，";
SYSTEM echo "包括学生学号、姓名、性别、手机、所选课程和成绩: ";
CREATE VIEW CES_Flunk_overallScore(id, name, gender, cellphone, course_id, grade) AS (
    SELECT DISTINCT
        Students.id,
        Students.name,
        Students.gender,
        Students.cellphone,
        CourseSelection.course_id,
        CourseSelection.overall_score
    FROM
        Students,
        CourseSelection,
        Courses,
        Colleges
    WHERE
        Students.id = CourseSelection.student_id AND
        Students.college_id = Colleges.id AND
        Courses.id = CourseSelection.course_id AND
        Colleges.name = "计算机学院" AND
        (CourseSelection.overall_score < 60 OR CourseSelection.overall_score IS NULL)
);

SYSTEM echo "CES_Flunk_overallScore View:   ";
SELECT * FROM CES_Flunk_overallScore;
/*UPDATE CES_Flunk_overallScore SET grade = grade*1.5;*/
SYSTEM echo "This View Cannot Update."
DROP VIEW CES_Flunk_overallScore;
SYSTEM echo "";

SYSTEM echo "(2)设计一个能更新的视图，要求更新后的数据满足视图定义的范围:"
SYSTEM echo "“系统结构”还未有总评成绩的选课视图。";
SYSTEM echo "写出如下对视图的更新命令，并判断是否可行，如不可行请说出理由";

CREATE TABLE CS_tmp SELECT * FROM CourseSelection;
CREATE VIEW SystemStructureNotEvaluate(s_id, semester, course_id, t_id, u_score, e_score, o_score) AS (
    SELECT
        student_id, semester, course_id, teacher_id,
        usual_time_score, exam_score, overall_score
    FROM CS_tmp
    WHERE CS_tmp.course_id IN (
        SELECT id FROM Courses WHERE Courses.name = "系统结构")) WITH CHECK OPTION;
SELECT * FROM SystemStructureNotEvaluate;

SYSTEM echo "插入数据(1107, 2013-2014秋季, 08305004, 0101, null，null，null)";
/*
INSERT INTO SystemStructureNotEvaluate(s_id, semester, course_id, t_id, u_score, e_score, o_score) VALUES
("1107", "2013-2014秋季", "08305004", "0101", NULL, NULL, NULL);
SYSTEM echo "After Insert: ";
SELECT * FROM SystemStructureNotEvaluate;
*/
SYSTEM echo "error::ERROR 1062 (23000) at line 134: Duplicate entry '1107-2013-2014秋季-08305004' for key 'PRIMARY'."

SYSTEM echo "插入数据(1107, 2012-2013冬季, 08305002，0102, null，null，null)";
/*
INSERT INTO SystemStructureNotEvaluate(s_id, semester, course_id, t_id, u_score, e_score, o_score) VALUES
("1107", "2012-2013冬季", "08305002", "0102", NULL, NULL, NULL);
SYSTEM echo "After Insert: ";
SELECT * FROM SystemStructureNotEvaluate;
*/
SYSTEM echo "error::ERROR 1369 (HY000) at line 145: CHECK OPTION failed 'school.SystemStructureNotEvaluate'"

SYSTEM echo "将所有学生平时成绩增加10分,但不能超过100分";
UPDATE SystemStructureNotEvaluate SET u_score = u_score + 10 WHERE u_score <= 90;
UPDATE SystemStructureNotEvaluate SET u_score = 100 WHERE u_score > 90;
UPDATE SystemStructureNotEvaluate SET u_score = 10 WHERE u_score IS NULL;
SYSTEM echo "After update: "
SELECT * FROM SystemStructureNotEvaluate;
DROP VIEW SystemStructureNotEvaluate;
DROP TABLE CS_tmp;
