from typing import List, Optional
from pydantic import BaseModel
from typing import List

class AvailableClass(BaseModel):
    course_code: int
    course_name: str
    department: str
    instructor_first_name: str
    instructor_last_name: str
    current_enrollment: int
    max_enrollment: int
    waitlist: int
    section_number: int


class AvailableClassResponse(BaseModel):
    available_classes: List[AvailableClass]

