/* mysql -u root -p school < ./test.sql */

SYSTEM echo "1.查询 2011 年进校年龄大于 20 岁的男学生的学号与姓名 ";
SELECT DISTINCT id, name FROM Students WHERE id LIKE "11%" AND (YEAR(NOW()) - YEAR(birthday)) > 20;
SYSTEM echo "";

SYSTEM echo "2. 检索刘晓明不学的课程的课程号";
SELECT DISTINCT course_id FROM OpenCourses WHERE OpenCourses.course_id NOT IN
(SELECT course_id FROM CourseSelection, Students
WHERE CourseSelection.student_id = Students.id AND Students.name = "刘晓明");
SYSTEM echo "";

SYSTEM echo "3. 检索马小红老师所授课程的学年,学期,课程号,上课时间"
SELECT DISTINCT LEFT(semester, 9) as "School Year", RIGHT(semester, 2) as "Semester", course_id, time
FROM OpenCourses, Teachers
WHERE OpenCourses.teacher_id = Teachers.id AND Teachers.name = "马小红";
SYSTEM echo "";

SYSTEM echo "4. 查询计算机学院男生总评成绩及格的课程号、课名、开课教师姓名,";
SYSTEM echo "按开课教师升序,课程号降序排序。";
SELECT DISTINCT
    Teachers.id as id,
    Courses.id as Courses_id,
    Courses.name as Courses_name,
    Teachers.name as Teachers_name

FROM
    CourseSelection,
    Teachers,
    Students,
    Courses,
    Colleges
WHERE
    CourseSelection.student_id = Students.id AND
    Teachers.id = CourseSelection.teacher_id AND
    Courses.id = CourseSelection.course_id AND
    Students.college_id = Colleges.id AND
    Students.gender = "男" AND
    Colleges.name = "计算机学院" AND
    CourseSelection.overall_score >= 60
ORDER BY
    Teachers.id ASC,
    Courses.id DESC,
    Courses.name,
    Teachers.name;
SYSTEM echo "";

SYSTEM echo "5. 检索学号比张颖同学大,年龄比张颖同学小的同学学号、姓名";
SELECT DISTINCT
    students_list.id,
    students_list.name
FROM
    Students as students_list,
    Students as zyinfo
WHERE
    students_list.id > zyinfo.id AND
    DATEDIFF(students_list.birthday, zyinfo.birthday) < 0
    AND zyinfo.name = "张颖";
SYSTEM echo "";

SYSTEM echo "6. 检索同时选修了“08305001”和“08305002”的学生学号和姓名"
SELECT DISTINCT
    Students.id,
    Students.name
FROM
    CourseSelection as cs5001,
    CourseSelection as cs5002, Students
WHERE
    cs5001.student_id = Students.id AND
    cs5002.student_id = Students.id AND
    cs5001.course_id = "08305001" AND
    cs5002.course_id = "08305002"
ORDER BY Students.id ASC;
SYSTEM echo "";
