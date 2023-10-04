from sqlite3 import Connection
from typing import List, Union

from fastapi import HTTPException, status
from loguru import logger

from .models import (
    AvailableClass,
    QueryStatus,
    Registration,
    RegistrationStatus,
    UserRole,
)

LIST_AVAILABLE_SQL_QUERY = """
	SELECT available_classes.name as 'course_name', available_classes.coursecode as 'course_code', 
    available_classes.department, available_classes.currentenrollment as 'current_enrollment', 
    available_classes.waitlist, available_classes.maxenrollment as "max_enrollment", 
    available_classes.sectionnumber as "section_number", 
    ur.name as "instructor_first_name", ur.lastname as "instructor_last_name"  
    FROM Users ur, (SELECT cl.coursecode, cl.name, cl.department, sc.currentenrollment, 
    sc.maxenrollment, sc.waitlist, sc.sectionnumber, sc.instructorid FROM "Class" as cl 
    join section as sc on cl.coursecode = sc.coursecode WHERE cl.Department = '{department_name}') 
    as available_classes where ur.cwid = available_classes.instructorid
"""
class DBException(Exception):
    def __init__(self, error_detail:str) -> None:
        self.error_detail = error_detail


    
def get_available_classes(db_connection: Connection, department_name: str) -> List[AvailableClass]:
    """Query database to get available classes for a given department name

    Args:
        db_connection (Connection): SQLite Connection 
        department_name (str): Department name

    Returns:
        List[AvailableClass]: List of available classes
    """
    result = []
    query = LIST_AVAILABLE_SQL_QUERY.format(department_name=department_name)
    cursor = db_connection.cursor()
    rows =  cursor.execute(query)
    if rows.rowcount == 0:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= f'Record not found for given department_name:{department_name}')
    for row in rows:
        available_class = AvailableClass(course_name=row[0], 
                                     course_code=row[1],
                                     department=row[2],
                                     current_enrollment=row[3],
                                     waitlist=row[4],
                                     max_enrollment=row[5],
                                     section_number=row[6],
                                     instructor_first_name=row[7],
                                     instructor_last_name=row[8])
        result.append(available_class)
    cursor.close()
    return result
    

def check_user_role(db_connection: Connection, student_id: int)-> Union[str, None]:
    logger.info('Checking user role')
    query = f"""
            SELECT role FROM Users where CWID = {student_id} 
            """
    cursor = db_connection.cursor()
    rows =  cursor.execute(query)
    if rows.rowcount == 0:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= f'Record not found for given student_id:{student_id}')
    result = UserRole.NOT_FOUND
    for row in rows:
        result = row[0]
    return result

#  def check_student_class_status(db_connection:Database,student_id:int, class_id:int, status:str)->str:
#     logger.info('checking_student_class_status')
#     # query = 

def count_waitlist_registration(db_connection: Connection, section_id: int)->int:
    logger.info('Checking waitlist registration')
    query = f"""SELECT COUNT(*) FROM RegistrationList WHERE ClassID = {section_id} and Status = 'waitlisted'
    """
    cursor = db_connection.cursor()
    rows =  cursor.execute(query)
    if rows.rowcount == 0:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= f'Record not found for given section_id:{section_id}')
    result = 0
    for row in rows:
        result = row[0]
    return result

def check_enrollment_eligibility(db_connection: Connection, section_id: int, course_code: int)->str:
    logger.info('Checking enrollment eligibility')
    query = f"""SELECT CurrentEnrollment as 'current_enrollment', MaxEnrollment as 'max_enrollment', Waitlist as 'waitlist' FROM "Section" WHERE CourseCode = {course_code} and SectionNumber = {section_id}
    """
    cursor = db_connection.cursor()
    rows =  cursor.execute(query)
    if rows.rowcount == 0:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= f'Record not found for given section_id:{section_id} and course_code:{course_code}')
    query_result = {}
    for row in rows:
        query_result['current_enrollment'] = row[0]
        query_result['max_enrollment'] = row[1]
        query_result['waitlist'] = row[2]
    
    # First check whether there is capacity to enroll in a section
    if query_result['max_enrollment'] - query_result['current_enrollment'] >= 1:
        return RegistrationStatus.ENROLLED
    
    waitlist_count = count_waitlist_registration(db_connection, section_id)
    if query_result['waitlist'] > waitlist_count:
        return RegistrationStatus.WAITLISTED
    
    return RegistrationStatus.NOT_ELIGIBLE

def complete_registration(db_connection: Connection, registration: Registration, course_code: int) -> str:
    logger.info('Starting registration')
    insert_query = f"""
    INSERT INTO RegistrationList (StudentID, ClassID, Status) VALUES ({registration.student_id}, {registration.class_id}, '{registration.enrollment_status}')
    """
    update_query = f"""
    UPDATE "Section" SET CurrentEnrollment = CurrentEnrollment + 1 WHERE SectionNumber = {registration.class_id} and CourseCode = {course_code}
    """
    cursor = db_connection.cursor()
    cursor.execute("BEGIN")
    try:
        cursor.execute(insert_query)
        cursor.execute(update_query)
        cursor.execute("COMMIT")
    except Exception as err:
        logger.error(err)
        cursor.execute("ROLLBACK")
        logger.info('Rolling back transaction')
        raise DBException(error_detail = 'Fail to register')
    finally:
        cursor.close()

    return QueryStatus.SUCCESS
    


        
