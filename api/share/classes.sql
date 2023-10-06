-- classes.sql

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;

-- Create the Users table
DROP TABLE IF EXISTS Users;
CREATE TABLE IF NOT EXISTS Users (
    CWID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Middle TEXT NULL,
    LastName TEXT NOT NULL,
    Role TEXT NOT NULL CHECK (role IN ('instructor', 'registrar', 'student'))
);

-- Create the Class table
DROP TABLE IF EXISTS Class;
CREATE TABLE IF NOT EXISTS Class (
    CourseCode TEXT PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL
);

-- Create the Section table
DROP TABLE IF EXISTS Section;
CREATE TABLE IF NOT EXISTS Section (
    SectionNumber INTEGER NOT NULL,
    CourseCode TEXT NOT NULL,
    InstructorID INTEGER NOT NULL,
    CurrentEnrollment INTEGER NOT NULL,
    MaxEnrollment INTEGER NOT NULL,
    Waitlist INTEGER NOT NULL,
    SectionStatus TEXT NOT NULL CHECK (SectionStatus IN ('open', 'closed')),
    PRIMARY KEY (SectionNumber, CourseCode),
    FOREIGN KEY (CourseCode) REFERENCES Class (CourseCode),
    FOREIGN KEY (InstructorID) REFERENCES Users (CWID)
);


-- Create the RegistrationList table
DROP TABLE IF EXISTS RegistrationList;
CREATE TABLE IF NOT EXISTS RegistrationList (
    RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INTEGER NOT NULL,
    CourseCode TEXT NOT NULL,
    SectionNumber INTEGER NOT NULL,
    EnrollmentDate DATETIME DEFAULT (CURRENT_TIMESTAMP),
    Status TEXT NOT NULL CHECK (Status IN ('enrolled', 'waitlisted', 'dropped')),
    FOREIGN KEY (StudentID) REFERENCES Users (CWID),
    FOREIGN KEY (CourseCode, SectionNumber) REFERENCES Section (CourseCode, SectionNumber)
);

-- pre populate database
-- Class Table
INSERT INTO Class (CourseCode, Name, Department) VALUES
    ('CPSC-101', 'Introduction to Programming', 'Computer Science'),
    ('CPSC-111', 'Data Structures and Algorithms', 'Computer Science'),
    ('MATH-201', 'Calculus I', 'Mathematics'),
    ('PHYS-301', 'Physics for Engineers', 'Physics'),
    ('PYS-101', 'Introduction to Psychology', 'Psychology'),
    ('ENG-541', 'English Composition', 'English'),
    ('ART-271', 'Art History', 'Art'),
    ('CHEM-101', 'Introduction to Chemistry', 'Chemistry'),
    ('HIST-281', 'World History', 'History'),
    ('ECON-554', 'Microeconomics', 'Economy');


-- -- Users Table
INSERT INTO Users (Name, Middle, LastName, Role) VALUES
    ('John', 'A.', 'Smith', 'instructor'),
    ('Jane', 'M.', 'Doe' ,'instructor'),
    ('Robert', 'E.', 'Johnson', 'instructor'),
    ('Emily', NULL, 'Davis' ,'registrar'),
    ('Michael', 'J.', 'Wilson', 'student'),
    ('Susan', 'K.', 'Brown', 'student'),
    ('David', 'P.', 'Miller', 'student'),
    ('Jennifer', NULL, 'Clark', 'student'),
    ('Richard', 'R.', 'White', 'student'),
    ('Sarah', 'L.', 'Anderson', 'student'),
    ('William', 'T.', 'Lee', 'student'),
    ('Karen', NULL, 'Martinez', 'student'),
    ('Thomas', 'S.', 'Taylor', 'student'),
    ('Laura', 'M.', 'Garcia', 'student'),
    ('Steven', NULL, 'Harris', 'student');

-- -- Section Table
INSERT INTO Section (sectionNumber, CourseCode, InstructorID, CurrentEnrollment, MaxEnrollment, Waitlist, SectionStatus) VALUES
    (1, 'CPSC-101', 1, 1, 30, 1, 'open'),
    (5, 'CPSC-101', 1, 1, 30, 0, 'open'),
    (1, 'CPSC-111', 2, 0, 35, 0, 'open'),
    (5, 'MATH-201', 3, 2, 25, 0, 'open'),
    (1, 'PHYS-301', 3, 1, 20, 0, 'open'),
    (3, 'PYS-101', 2, 2, 35, 0, 'open');

-- -- RegistrationList Table
INSERT INTO RegistrationList (StudentID, CourseCode, SectionNumber, Status) VALUES
    (5,'MATH-201', 5, 'dropped'),
    (5, 'PHYS-301',1, 'dropped'),
    (5, 'CPSC-101', 1, 'waitlisted'),
    (6, 'PYS-101', 3, 'enrolled'),
    (6, 'CPSC-101', 5, 'enrolled'),
    (7, 'MATH-201', 5, 'enrolled'),
    (7, 'PYS-101', 3, 'enrolled'),
    (8, 'PHYS-301', 1, 'enrolled'),
    (9, 'CPSC-101', 1, 'enrolled'),
    (10, 'CPSC-101', 1, 'enrolled'),
    (11, 'PHYS-301', 1, 'dropped'),
    (12, 'PHYS-301', 1, 'dropped'),
    (13, 'PHYS-301', 1, 'dropped');


    
COMMIT;
