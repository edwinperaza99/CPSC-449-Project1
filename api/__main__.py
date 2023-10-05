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
    update_student_registration_status,
    addClass,
    check_class_exists,
    addSection,
    check_section_exists,
    deleteSection,
    changeSectionInstructor,
    freezeEnrollment
)
from .models import (
    AvailableClassResponse,
    EnrollmentRequest,
    EnrollmentResponse,
    QueryStatus,
    Registration,
    RegistrationStatus,
    UserRole,
    DropCourseResponse,
    AddClassResponse,
    AddClassRequest,
    DeleteSectionRequest,
    DeleteSectionResponse,
    ChangeInstructorRequest,
    ChangeInstructorResponse,
    FreezeEnrollmentRequest,
    FreezeEnrollmentResponse
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


##########   STUDENTS ENDPOINTS     ######################
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


@app.put(path = "/dropcourse", operation_id= "update_registration_status",response_model= DropCourseResponse)
async def update_registration_status(enrollment_request:EnrollmentRequest):
    try:
        registration = Registration(section_number= enrollment_request.section_number,
                                    student_id=enrollment_request.student_id,
                                    course_code=enrollment_request.course_code,
                                    enrollment_status='enrolled')
        update_student_registration_status(db_connection,registration)
        drop_course_response = DropCourseResponse(course_code=enrollment_request.course_code,
                                                   section_number=enrollment_request.section_number,
                                                   status='successful')
        return drop_course_response
    except DBException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=err.error_detail)

##########   REGISTRAR ENDPOINTS     ######################
@app.post(path="/classes", operation_id="add_class", response_model=AddClassResponse)
async def add_class(addClass_request: AddClassRequest):
    classExists = check_class_exists(db_connection, addClass_request.course_code)
    if classExists:
        try:
            response = addSection(db_connection, addClass_request.section_number, addClass_request.course_code, addClass_request.instructor_id, addClass_request.max_enrollment)
            if response == QueryStatus.SUCCESS:
                return AddClassResponse(addClass_status = 'Successfully added new section')
            else:
                return AddClassResponse(addClass_status = 'Failed to add Section')
        
        except DBException as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= err.error_detail)
    else:
        try:
            addClassResponse = addClass(db_connection, addClass_request.course_code, addClass_request.class_name, addClass_request.department)
            if addClassResponse == QueryStatus.SUCCESS:
                addSectionResponse = addSection(db_connection, addClass_request.section_number, addClass_request.course_code, addClass_request.instructor_id, addClass_request.max_enrollment)
                if addSectionResponse == QueryStatus.SUCCESS:
                    return AddClassResponse(addClass_status = 'Successfully added Class & Section')
                else:
                    return AddClassResponse(addClass_status = 'Failed to add Class & Section')
        
        except DBException as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= err.error_detail)

@app.delete(path="/sections", operation_id="delete_section", response_model=DeleteSectionResponse)  
async def delete_section(deleteSection_Request: DeleteSectionRequest):
    sectionExists = check_section_exists(db_connection, deleteSection_Request.course_code, deleteSection_Request.section_number)
    if not sectionExists:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'This section does not exist')
    response = deleteSection(db_connection, deleteSection_Request.course_code, deleteSection_Request.section_number)
    if response == QueryStatus.SUCCESS:
        return DeleteSectionResponse(deleteSection_status = 'Successfully deleted section ' + str(deleteSection_Request.section_number) + ' of course ' + deleteSection_Request.course_code)
    else:
        return DeleteSectionResponse(deleteSection_status = 'Failed to delete section')
    
@app.post(path="/changeSectionInstructor", operation_id="change_section_instructor", response_model=ChangeInstructorResponse)
async def change_section_instructor(changeInstructor_Request: ChangeInstructorRequest):
    sectionExists = check_section_exists(db_connection, changeInstructor_Request.course_code, changeInstructor_Request.section_number)
    if sectionExists == 0:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'This section does not exist')
    response = changeSectionInstructor(db_connection, changeInstructor_Request.course_code, changeInstructor_Request.section_number, changeInstructor_Request.instructor_id)
    if response == QueryStatus.SUCCESS:
        return ChangeInstructorResponse(changeInstructor_status = 'Successfully changed instructor of section ' + str(changeInstructor_Request.section_number))
    else:
        return ChangeInstructorResponse(changeInstructor_status = 'Failed to change instructor')
    
@app.post(path="/freezeEnrollment", operation_id='freeze_enrollment', response_model=FreezeEnrollmentResponse)
async def freeze_enrollment(freezeEnrollment_Request: FreezeEnrollmentRequest):
    sectionExists = check_section_exists(db_connection, freezeEnrollment_Request.course_code, freezeEnrollment_Request.section_number)
    if sectionExists == 0:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'This section does not exist')
    response = freezeEnrollment(db_connection, freezeEnrollment_Request.course_code, freezeEnrollment_Request.section_number)
    if response == QueryStatus.SUCCESS:
        return FreezeEnrollmentResponse(freezeEnrollment_status = 'Successfully freezed enrollment for section ' + str(freezeEnrollment_Request.section_number))
    else:
        return FreezeEnrollmentResponse(freezeEnrollment_status = 'Failed to freeze enrollment')

##########   REGISTRAR ENDPOINTS ENDS    ######################    
                                             


async def main():
    """Start the server."""
    server = Server(uvicorn.Config(app=app, host="0.0.0.0", timeout_graceful_shutdown=30))
    await server.serve()

if __name__ == "__main__":
    run(main())

