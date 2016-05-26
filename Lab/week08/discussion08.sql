/* mysql -u root -p school < discussion08.sql */
USE school;

SYSTEM echo "1. 请用SQL，关系代数，元组关系演算，域关系演算写出如下查询：";
SYSTEM echo "检索同时选修了“08305001”和“08305002”的学生学号和姓名.";

SYSTEM echo "(1)";
SELECT DISTINCT
    Students.id,
    Students.name
FROM
    CourseSelection as cs5001,
    CourseSelection as cs5002,
    Students
WHERE
    cs5001.student_id = Students.id AND
    cs5002.student_id = Students.id AND
    cs5001.course_id = "08305001" AND
    cs5002.course_id = "08305002"
ORDER BY Students.id ASC;

SYSTEM echo "(2)";
SELECT Students.id, Students.name FROM Students
WHERE Students.id IN((
    (SELECT CourseSelection.student_id FROM CourseSelection
    WHERE CoureseSelection.course_id = "08305001")
    intersect
    (SELECT CouresSelection.student_id FROM CourseSelection
    WHERE CourseSelection.course_id = "08305002"))
ORDER BY Student.id ASC;

SYSTEM echo "(3)";
SELECT Students.id, Students.name FROM Students
