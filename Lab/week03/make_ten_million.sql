/*  mysql  -u root -p < ./make_ten_million.sql  */
DROP DATABASE IF EXISTS  make_ten_million;
CREATE DATABASE make_ten_million CHARACTER SET  'utf8' COLLATE 'utf8_general_ci';

USE make_ten_million;

CREATE TABLE make_ten_million_Table (
        id INT(8)  NOT NULL,
        name CHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET = utf8;

INSERT INTO make_ten_million_Table(id, name) VALUES
("00000001", "1号"),
("00000002", "2号"),
("00000003", "3号"),
("00000004", "4号"),
("00000005", "5号"),
("00000006", "6号"),
("00000007", "7号"),
("00000008", "8号"),
("00000009", "9号");
