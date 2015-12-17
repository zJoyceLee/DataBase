//STL
#include<isotream>
#include<vector>

void ChargeDNO(){
  EXEC SQL BEGIN DECLARE SECTION;
      int maxage;
      char id[7], name[9], gender[3], college_id[4], newcollege_id[4];
  EXEC SQL END DECLARE  SECTION;

  gets(maxage);

  //--Definition Cursor--------------------------
  EXEC SQL DECLARE myCursor CURSOR FOR
    SELECT id, name, gender, college_id
    FROM Students
    WHERE YEAR(CURDATE()) - YEAR(birthday) > :maxage;
  //----------------------------------------------------
  //----------------------------------------------------
  EXEC SQL OPEN myCursor;
  EXEC SQL FETCH FROM myCursor INTO :id, :name, :gender, :college_id;
  while(1) {
    if(SQLCA.SQLSTATE != '00000')
      break;
    printf("%s, %s, %s, %s", id, name, gender, college_id);
    printf("UPDATE College_id?");
    scanf("%c", &yn);
    if(yn == 'y' or yn == 'Y') {
      printf("INPUT NEW College_id: ");
      //--Update College_id------------------------
      EXEC SQL UPDATE Students SET college_id = :newcollege_id WHERE CURRENT OF myCursor;
      //----------------------------------------------------
      scanf("%c", &newcollege_id);
      EXEC SQL FETCH FROM myCursor INTO :id, :name, :gender, :college_id;
    }
  }
  EXEC SQL CLOSE myCursor;
}


int main(int argc, char *argv[]) {
    ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
