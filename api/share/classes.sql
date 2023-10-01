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
    CourseCode INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL
);

-- Create the Section table
DROP TABLE IF EXISTS Section;
CREATE TABLE IF NOT EXISTS Section (
    SectionNumber INTEGER NOT NULL,
    CourseCode INTEGER NOT NULL,
    InstructorID INTEGER NOT NULL,
    CurrentEnrollment INTEGER NOT NULL,
    MaxEnrollment INTEGER NOT NULL,
    Waitlist INTEGER NOT NULL,
    PRIMARY KEY (SectionNumber, CourseCode),
    FOREIGN KEY (CourseCode) REFERENCES Class (CourseCode),
    FOREIGN KEY (InstructorID) REFERENCES Users (CWID)
);


-- Create the RegistrationList table
DROP TABLE IF EXISTS RegistrationList;
CREATE TABLE IF NOT EXISTS RegistrationList (
    RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INTEGER NOT NULL,
    CourseCode INTEGER NOT NULL,
    SectionNumber INTEGER NOT NULL,
    EnrollmentDate DATETIME DEFAULT (CURRENT_TIMESTAMP),
    Status TEXT NOT NULL CHECK (Status IN ('enrolled', 'waitlisted', 'dropped')),
    FOREIGN KEY (StudentID) REFERENCES Users (CWID),
    FOREIGN KEY (CourseCode, SectionNumber) REFERENCES Section (CourseCode, SectionNumber)
);

-- pre populate database
-- Class Table
INSERT INTO Class (CourseCode, Name, Department) VALUES
    (101, 'Introduction to Programming', 'CPSC'),
    (111, 'Data Structures and Algorithms', 'CPSC'),
    (201, 'Calculus I', 'MATH'),
    (301, 'Physics for Engineers', 'PHYS'),
    (101, 'Introduction to Psychology', 'PYS'),
    (541, 'English Composition', 'ENG'),
    (271, 'Art History', 'ART'),
    (101, 'Introduction to Chemistry', 'CHEM'),
    (281, 'World History', 'HIST'),
    (554, 'Microeconomics', 'ECON');


-- Users Table
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

-- Section Table
INSERT INTO Section (sectionNumber, CourseCode, InstructorID, CurrentEnrollment, MaxEnrollment, Waitlist) VALUES
    (1, 101, 1, 25, 30, 5),
    (5, 101, 2, 22, 30, 8),
    (1, 111, 3, 28, 35, 7),
    (5, 111, 4, 20, 25, 5),
    (1, 201, 5, 18, 20, 2),
    (3, 201, 6, 32, 35, 3),

-- RegistrationList Table
INSERT INTO RegistrationList (StudentID, CourseCode, SectionNumber, Status) VALUES
    (5, 1, 'enrolled'),
    (5, 1, 'dropped'),
    (5, 2, 'waitlisted'),
    (6, 3, 'enrolled'),
    (6, 4, 'enrolled'),
    (7, 5, 'enrolled'),
    (7, 6, 'enrolled'),
    (8, 7, 'enrolled'),
    (9, 8, 'enrolled'),
    (10, 9, 'enrolled'),
    (11, 10, 'enrolled'),
    (12, 11, 'enrolled'),
    (13, 12, 'enrolled'),
    (14, 13, 'enrolled'),
    (15, 14, 'enrolled');
    
COMMIT;