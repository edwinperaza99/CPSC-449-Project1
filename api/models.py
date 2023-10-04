from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from enum import Enum

class AvailableClass(BaseModel):
    course_code: str
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


class EnrollmentResponse(BaseModel):
    enrollment_status: str
    enrollment_date: Optional[datetime] = None

class EnrollmentRequest(BaseModel):
    section_number: int
    course_code: str
    student_id: int

class RegistrationStatus(str, Enum):
    ENROLLED = 'enrolled'
    WAITLISTED = 'waitlisted'
    NOT_ELIGIBLE = 'not_eligible'
    DROPPED = "dropped"

class Registration(BaseModel):
    section_number: int #Section Number
    student_id: int
    enrollment_status: str
    course_code: str

class QueryStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"

class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    REGISTRAR = "registrar"
    NOT_FOUND = "not_found"