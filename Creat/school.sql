/* >> mysql -u root -p school < ./test.sql */

DROP DATABASE school;
CREATE DATABASE school CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE school;

CREATE TABLE Colleges (
	id CHAR(2) NOT NULL,
	name CHAR(255) NOT NULL,
	address VARCHAR(1024) NOT NULL,
	telephone CHAR(8),
	PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Students (
	id CHAR(5) NOT NULL,
	name CHAR(20) NOT NULL,
	gender CHAR(4) NOT NULL,
	birthday DATE,
	birthplace CHAR(255),
	cellphone CHAR(11),
	college_id CHAR(2),
	PRIMARY KEY(id),
	FOREIGN KEY(college_id) REFERENCES Colleges(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Teachers (
	id CHAR(4) NOT NULL,
	name CHAR(255) NOT NULL,
	gender CHAR(4) NOT NULL  CHECK (gender in ("男","女")),
	birthday DATE,
	title CHAR(30),
	salary FLOAT(2) CHECK (sarary >= 2500.00),
	college_id CHAR(2),
	PRIMARY KEY(id),
	FOREIGN KEY(college_id) REFERENCES Colleges(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Courses (
	id CHAR(8) NOT NULL,
	name CHAR(255) NOT NULL,
	credit INTEGER NOT NULL,
	class_hours INTEGER NOT NULL,
	college_id CHAR(2),
	PRIMARY KEY(id),
	FOREIGN KEY(college_id) REFERENCES Colleges(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE OpenCourses (
	semester CHAR(255) NOT NULL,
	course_id CHAR(8) NOT NULL,
	teacher_id CHAR(4) NOT NULL,
	time CHAR(255),
	PRIMARY KEY(semester, course_id, teacher_id, time),
	FOREIGN KEY(course_id) REFERENCES Courses(id),
	FOREIGN KEY(teacher_id) REFERENCES Teachers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE CourseSelection (
	student_id CHAR(4) NOT NULL,
	semester CHAR(255) NOT NULL,
	course_id CHAR(8) NOT NULL,
	teacher_id CHAR(4) NOT NULL,
	usual_time_score FLOAT(2),
	exam_score FLOAT(2),
	overall_score FLOAT(2),
	PRIMARY KEY (student_id, semester, course_id),
	FOREIGN KEY (student_id) REFERENCES Students(id),
	FOREIGN KEY (course_id) REFERENCES Courses(id),
	FOREIGN KEY (teacher_id) REFERENCES Teachers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE INDEX index01 ON Students (
	college_id ASC,
	name DESC
);

CREATE INDEX index02 ON Courses (
	name
);

INSERT INTO Colleges(id, name, address, telephone) VALUES
("01", "计算机学院", "上大东区三号楼", "65347567"),
("02", "通讯学院", "上大东区二号楼", "65341234"),
("03", "材料学院", "上大东区四号楼", "65347890"),
("54", "空", "空", "12345678");

INSERT INTO Students(id, name, gender, birthday, birthplace, cellphone, college_id) VALUES
("1101", "李明", "男", "1993-03-06", "上海", "13613005486", "02"),
("1102", "刘晓明", "男", "1992-12-08", "安徽", "18913457890", "01"),
("1103", "张颖", "女", "1993-01-05", "江苏", "18826490423", "01"),
("1104", "刘晶晶", "女", "1994-11-06", "上海", "13331934111", "01"),
("1105", "刘成刚", "男", "1991-06-07", "上海", "18015872567", "01"),
("1106", "李二麗", "女", "1993-05-04", "江苏", "18107620945", "01"),
("1107", "张晓峰", "男", "1992-08-16", "浙江", "13912341078", "01"),
("1108", "李羽哲", "女", "1995-03-09", "吉林", "18717897080"," 04");

INSERT INTO Teachers(id, name, gender, birthday, title, salary, college_id) VALUES
("0101", "陈迪茂", "男", "1973-03-06", "副教授", 3567.00, "01"),
("0102", "马小紅", "女", "1972-12-08", "讲师", 2845.00, "01"),
("0201", "张心颖", "女", "1960-01-05", "教授", 4200.00, "02"),
("0103", "吴宝刚", "男", "1980-11-06", "讲师", 2554.00, "01");

INSERT INTO Courses(id, name, credit, class_hours, college_id) VALUES
("08305001", "离散数学", 4, 40, "01"),
("08305002", "数据库原理", 4, 50, "01"),
("08305003", "数据结构", 4, 50, "01"),
("08305004", "系统结构", 6, 60, "01"),
("08301001", "分子物理学", 4, 40, "03"),
("08302001", "通信学", 3, 30, "02");

INSERT INTO OpenCourses(semester, course_id, teacher_id, time) VALUES
("2012-2013秋季", "08305001", "0103", "星期三5-8"),
("2012-2013冬季", "08305002", "0101", "星期三1-4"),
("2012-2013冬季", "08305002", "0102", "星期三1-4"),
("2012-2013冬季", "08305002", "0103", "星期三1-4"),
("2012-2013冬季", "08305003", "0102", "星期五5-8"),
("2013-2014秋季", "08305004", "0101", "星期二1-4"),
("2013-2014秋季", "08305001", "0102", "星期一5-8"),
("2013-2014冬季", "08302001", "0101", "星期一5-8");

INSERT INTO CourseSelection(student_id, semester, course_id, teacher_id, usual_time_score, exam_score, overall_score) 
VALUES
("1101", "2012-2013秋季", "08305001", "0103", 60, 60, 60),
("1102", "2012-2013秋季", "08305001", "0103", 87, 87, 87),
("1102", "2012-2013冬季", "08305002", "0101", 82, 82, 82),
("1102", "2013-2014秋季", "08305004", "0101", null, null, null),
("1103", "2012-2013秋季", "08305001", "0103", 56, 56, 56),
("1103", "2012-2013冬季", "08305002", "0102", 75, 75, 75),
("1103", "2012-2013冬季", "08305003", "0102", 84, 84, 84),
("1103", "2013-2014秋季", "08305001", "0102", null, null, null),
("1103", "2013-2014秋季", "08305004", "0101", null, null, null),
("1104", "2012-2013秋季", "08305001", "0103", 74, 74, 74),
("1104", "2013-2014冬季", "08302001", "0201", null, null, null),
("1106", "2012-2013秋季", "08305001", "0103", 85, 85, 85),
("1106", "2012-2013冬季", "08305002", "0103", 66, 66, 66),
("1107", "2012-2013秋季", "08305001", "0103", 90, 90, 90),
("1107", "2012-2013冬季", "08305003", "0102", 79, 79, 79),
("1107", "2013-2014秋季", "08305004", "0101", null, null, null);

