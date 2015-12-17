/* mysql -u root -p school < ./lab04.sql */

USE school;

SYSTEM echo "1.建立计算机学院总评不及格成绩学生的视图，";
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

DROP VIEW CES_Flunk_overallScore;
SYSTEM echo "";

SYSTEM echo "2. 在CourseSelection表中插入记录，把每个学生没学过的课程都插入到表中";
SYSTEM echo "使得每个学生都选修每门课";
CREATE TEMPORARY TABLE  CS_tmp SELECT * FROM CourseSelection;
INSERT INTO CS_tmp(student_id, semester, course_id, teacher_id) (
    SELECT
        Students.id,
        OpenCourses.semester,
        OpenCourses.course_id,
        OpenCourses.teacher_id
    FROM
        OpenCourses,
        Students
    WHERE
        OpenCourses.course_id NOT IN (
            SELECT DISTINCT CourseSelection.course_id
            FROM CourseSelection
            WHERE CourseSelection.student_id = Students.id)
);
SYSTEM echo "CourseSelection: ";
SELECT * FROM CourseSelection;
SYSTEM echo "CS_tmp: ";
SELECT * FROM CS_tmp;
DROP TABLE CS_tmp;
SYSTEM echo ""

SYSTEM echo "3. 求年龄大于所有女同学年龄的男学生姓名和年龄: ";
SELECT name, YEAR(CURDATE())-YEAR(birthday) as age
FROM Students
WHERE
    gender = "男" AND
    birthday < ALL(SELECT birthday FROM Students WHERE gender = "女");
SYSTEM echo "";

SYSTEM echo "4. 在CourseSelection表中修改08305001课程的平时成绩，";
SYSTEM echo "若成绩小于等于75分时提高5%，若成绩大于75分时提高4%: ";
CREATE TEMPORARY TABLE CS_TMP SELECT * FROM CourseSelection;
UPDATE CS_TMP SET usual_time_score = usual_time_score*1.05
WHERE usual_time_score <= 75 AND course_id = "08305001";
UPDATE CS_TMP SET usual_time_score = usual_time_score*1.04
WHERE usual_time_score > 75 AND course_id = "08305001";
SELECT * FROM CS_TMP;
DROP TABLE CS_TMP;
SYSTEM echo "";

SYSTEM echo "5. 删除没有开课的学院: ";
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

SYSTEM echo "5. 查询优、良、中、及格、不及格学生人数: ";
SELECT DISTINCT
    (SELECT COUNT(student_id) FROM CourseSelection WHERE (overall_score >= 90)) as "A",
    (SELECT COUNT(student_id) FROM CourseSelection WHERE (overall_score < 90 AND overall_score >= 80)) as "B",
    (SELECT COUNT(student_id) FROM CourseSelection WHERE (overall_score < 80 AND overall_score >= 70)) as "C",
    (SELECT COUNT(student_id) FROM CourseSelection WHERE (overall_score >= 60)) as "及格",
    (SELECT COUNT(student_id) FROM CourseSelection WHERE (overall_score < 60)) as "不及格"
FROM CourseSelection;
SYSTEM echo "";
