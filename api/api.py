import sqlite3
import typing

from fastapi import FastAPI, Depends, Response, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# define setting for database and logging config
class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str

# define how to get database
def get_db():
    with contextlib.closing(sqlite3.connect(settings.database)) as db:
        db.row_factory = sqlite3.Row
        yield db

# define structure of how data should be sent and received
# for students: 
class ListClasses(BaseModel):
    course_code: int
    name: str
    department: str
    # define in query to change CWID with instructor name 
    instructor: str
    current_enrollment: int
    max_enrollment: int

class AttemptEnrollment(BaseModel):
    course_code: int
    section_code: int
    CWID: int
    status: str

class DropClass(BaseModel):
    course_code: int
    section: int
    CWID: int
    status: str

# for instructors: 
class ViewEnrollment(BaseModel):
    course_code: int
    section: int
    # instructor CWID 
    instructorID: int
    status: str

class ViewDropped(BaseModel):
    course_code: int
    section: int
    # instructor CWID 
    instructorID: int
    status: str

class DropStudent(BaseModel):
    course_code: int
    section: int
    current_enrollment: int
    # student CWID 
    CWID: int
    status: str

# for registrar:
class AddClass(BaseModel):
    course_code: int
    name: str
    department: str
    
class AddSection(BaseModel):
    course_code: int
    section: int
    current_enrollment: int
    max_enrollment: int
    instructorID: int
    
class ChangeInstructor(BaseModel):
    course_code: int
    section: int
    instructorID: int

# this is the max value for the waitlist
waitlistMax = 15


# endpoint to to get list of classes
# @app.get("/classes/")
