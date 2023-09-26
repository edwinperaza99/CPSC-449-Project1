-- Create the Class table
CREATE TABLE IF NOT EXISTS Class (
    CourseCode INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL
);

-- Create the Section table
CREATE TABLE IF NOT EXISTS Section (
    SectionNumber INTEGER PRIMARY KEY AUTOINCREMENT,
    CourseCode INTEGER NOT NULL,
    InstructorID INTEGER NOT NULL,
    CurrentEnrollment INTEGER NOT NULL,
    MaxEnrollment INTEGER NOT NULL,
    Waitlist INTEGER NOT NULL,
    FOREIGN KEY (CourseCode) REFERENCES Class (CourseCode),
    FOREIGN KEY (InstructorID) REFERENCES Instructor (CWID)
);

-- Create the Instructor table
CREATE TABLE IF NOT EXISTS Instructor (
    CWID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Middle TEXT NULL,
    LastName TEXT NOT NULL
);

-- Create the Student table
CREATE TABLE IF NOT EXISTS Student (
    CWID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Middle TEXT NULL,
    LastName TEXT NOT NULL
);

-- Create the RegistrationList table
CREATE TABLE IF NOT EXISTS RegistrationList (
    RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
    StudentID INTEGER NOT NULL,
    ClassID INTEGER NOT NULL,
    EnrollmentDate DATETIME DEFAULT (CURRENT_TIMESTAMP),
    Status TEXT NOT NULL CHECK (Status IN ('enrolled', 'waitlisted', 'dropped')),
    FOREIGN KEY (StudentID) REFERENCES Student (CWID),
    FOREIGN KEY (ClassID) REFERENCES Section (SectionNumber)
);
