/* mysql -u root  -p teach < test.sql */
SELECT C.cno, C.cname FROM C WHERE  NOT EXISTS(
    SELECT * FROM S WHERE NOT EXISTS(
        SELECT * FROM SC));

SYSTEM echo "with connect";
SELECT C.cno, C.cname FROM C WHERE  NOT EXISTS(
    SELECT * FROM S WHERE NOT EXISTS(
        SELECT * FROM SC WHERE SC.sno = S.sno AND SC.cno = C.cno));
