"""Main module to run server and serve endpoints for clients."""

from asyncio import run
from datetime import datetime
import sqlite3

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn
from uvicorn.server import Server

from .database_query import (
    DBException,
    check_enrollment_eligibility,
    check_user_role,
    complete_registration,
    get_available_classes,
)
from .models import (
    AvailableClassResponse,
    EnrollmentRequest,
    EnrollmentResponse,
    QueryStatus,
    Registration,
    RegistrationStatus,
    UserRole,
)

app = FastAPI()
DATABASE_URL = "./api/share/classes.db"
db_connection = sqlite3.connect(DATABASE_URL)
db_connection.isolation_level = None


@app.on_event("shutdown")
async def shutdown():
    db_connection.close()

@app.get(path='/db_liveness', operation_id='check_db_health')
async def check_db_health():
    try:
        db_connection.cursor()
        return JSONResponse(content= {'status': 'ok'}, status_code = status.HTTP_200_OK)
    except Exception as ex:
        return JSONResponse(content= {'status': 'not connected'}, status_code = status.HTTP_503_SERVICE_UNAVAILABLE)


@app.get(path="/classes", operation_id="available_classes", response_model = AvailableClassResponse)
async def available_classes(department_name: str):
    """API to fetch list of available classes for a given department name.

    Args:
        department_name (str): Department name

    Returns:
        AvailableClassResponse: AvailableClassResponse model
    """
    result = get_available_classes(db_connection=db_connection, department_name=department_name)
    logger.info('Succesffuly exexuted available')
    return AvailableClassResponse(available_classes = result)

@app.post(path ="/enrollment", operation_id="course_enrollment", response_model= EnrollmentResponse)
async def course_enrollment(enrollment_request: EnrollmentRequest):
    """Allow enrollment of a course under given section for a student

    Args:
        enrollment_request (EnrollmentRequest): EnrollmentRequest model

    Raises:
        HTTPException: Raise HTTP exception when role is not authrorized
        HTTPException: Raise HTTP exception when query fail to execute in database

    Returns:
        EnrollmentResponse: EnrollmentResponse model
    """
    
    role = check_user_role(db_connection, enrollment_request.student_id)
    if role == UserRole.NOT_FOUND or role != UserRole.STUDENT:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'Enrollment not authorized for role:{role}')
    
    eligibility_status = check_enrollment_eligibility(db_connection, enrollment_request.section_number, enrollment_request.course_code)
    if eligibility_status == RegistrationStatus.NOT_ELIGIBLE:
        return EnrollmentResponse(enrollment_status = 'not eligible')

    try:
        registration = Registration(student_id = enrollment_request.student_id, enrollment_status = eligibility_status, 
                                    section_number = enrollment_request.section_number, course_code = enrollment_request.course_code) 
        insert_status = complete_registration(db_connection,registration)
        if insert_status == QueryStatus.SUCCESS:
            return EnrollmentResponse(enrollment_date = datetime.utcnow(), enrollment_status = eligibility_status)

    except DBException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= err.error_detail)    


async def main():
    """Start the server."""
    server = Server(uvicorn.Config(app=app, host="0.0.0.0", timeout_graceful_shutdown=30))
    await server.serve()

if __name__ == "__main__":
    run(main())

