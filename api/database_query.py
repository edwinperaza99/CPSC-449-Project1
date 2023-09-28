from typing import List
from databases import Database
from typing import List
from .models import AvailableClass

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

async def get_available_classes(db: Database, department_name: str) -> List[AvailableClass]:
    """Query database to get available classes for a given department name

    Args:
        db (Database): SQLite Database 
        department_name (str): Department name

    Returns:
        List[AvailableClass]: List of available classes
    """
    result = []
    query = LIST_AVAILABLE_SQL_QUERY.format(department_name=department_name)
    rows = await db.fetch_all(query=query)
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
    return result
    