USE school;

SYSTEM echo "2. 用多种方法表达查询：检索同时选修了“数据库原理”和“离散数学”的学生学号和姓名:  "
SYSTEM echo "(1)"
SELECT DISTINCT Students.id, Students.name
FROM Students, CourseSelection as DB, CourseSelection as Math, Courses
WHERE
    Students.id = DB.student_id AND
    DB.student_id = Math.student_id AND
    DB.course_id in (SELECT Courses.id FROM Courses WHERE Courses.name = "数据库原理") AND
    Math.course_id in (SELECT Courses.id FROM Courses WHERE Courses.name = "离散数学");
/*
SYSTEM echo "(2)"
SELECT  DISTINCT id, name
FROM
     SELECT DISTINCT Students.id, Students.name
     FROM Students WHERE Students.id in (
         SELECT CourseSelection.student_id FROM CourseSelection
         WHERE CourseSelection.course_id in (
             SELECT Courses.id FROM Courses WHERE Courses.name = "离散数学"
          )
      ) as myTable
WHERE myTable.id in (
    SELECT CourseSelection.student_id FROM CourseSelection
    WHERE CourseSelection.course_id in (
        SELECT Courses.id FROM Courses WHERE Courses.name = "数据库原理"
     )
);*/
SYSTEM echo "";

SYSTEM echo "3.查询每门课的排名，输出课程号，学号，总评成绩，排名；按课程号升序，课程相同按排名从高到低。（提示：某个同学一门课的排名就是该门课成绩大于等于他的人数）:"
SELECT DISTINCT
    X.course_id,
    X.student_id as S_id,
    X.overall_score as Score,
    count(*) as Ranking
FROM
    CourseSelection as X,
    CourseSelection as Y
WHERE
    (X.overall_score < Y.overall_score OR
    (X.student_id = Y.student_id AND X.student_id = Y.student_id)) AND
    X.course_id = Y.course_id
GROUP BY
    X.course_id,
    X.student_id,
    X.overall_score
ORDER BY
    1,
    4;
