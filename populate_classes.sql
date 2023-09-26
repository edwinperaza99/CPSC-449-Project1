-- Class Table
INSERT INTO Class (Name, Department) VALUES
    ('Introduction to Programming', 'Computer Science'),
    ('Data Structures and Algorithms', 'Computer Science'),
    ('Calculus I', 'Mathematics'),
    ('Physics for Engineers', 'Physics'),
    ('Introduction to Psychology', 'Psychology'),
    ('English Composition', 'English'),
    ('Art History', 'Art'),
    ('Introduction to Chemistry', 'Chemistry'),
    ('World History', 'History'),
    ('Microeconomics', 'Economics'),
    ('Introduction to Sociology', 'Sociology'),
    ('Business Ethics', 'Business'),
    ('Introduction to Biology', 'Biology'),
    ('Introduction to Music', 'Music'),
    ('Physical Education', 'Physical Education');

-- Instructor Table
INSERT INTO Instructor (Name, Middle, LastName) VALUES
    ('John', 'A.', 'Smith'),
    ('Jane', 'M.', 'Doe'),
    ('Robert', 'E.', 'Johnson'),
    ('Emily', NULL, 'Davis'),
    ('Michael', 'J.', 'Wilson'),
    ('Susan', 'K.', 'Brown'),
    ('David', 'P.', 'Miller'),
    ('Jennifer', NULL, 'Clark'),
    ('Richard', 'R.', 'White'),
    ('Sarah', 'L.', 'Anderson'),
    ('William', 'T.', 'Lee'),
    ('Karen', NULL, 'Martinez'),
    ('Thomas', 'S.', 'Taylor'),
    ('Laura', 'M.', 'Garcia'),
    ('Steven', NULL, 'Harris');

-- Student Table
INSERT INTO Student (Name, Middle, LastName) VALUES
    ('Alice', 'M.', 'Johnson'),
    ('Bob', 'A.', 'Smith'),
    ('Charlie', 'B.', 'Davis'),
    ('David', NULL, 'Wilson'),
    ('Ella', 'J.', 'Brown'),
    ('Frank', 'L.', 'Miller'),
    ('Grace', 'P.', 'Clark'),
    ('Hannah', 'S.', 'White'),
    ('Ian', NULL, 'Anderson'),
    ('Jessica', 'T.', 'Lee'),
    ('Kevin', NULL, 'Martinez'),
    ('Lily', 'S.', 'Taylor'),
    ('Mark', 'M.', 'Garcia'),
    ('Nora', NULL, 'Harris'),
    ('Oliver', 'R.', 'Anderson');

-- Section Table
INSERT INTO Section (CourseCode, InstructorID, CurrentEnrollment, MaxEnrollment, Waitlist) VALUES
    (1, 1, 25, 30, 5),
    (1, 2, 22, 30, 8),
    (2, 3, 28, 35, 7),
    (3, 4, 20, 25, 5),
    (4, 5, 18, 20, 2),
    (5, 6, 32, 35, 3),
    (6, 7, 28, 30, 2),
    (7, 8, 20, 25, 5),
    (8, 9, 22, 30, 8),
    (9, 10, 30, 35, 5),
    (10, 11, 25, 30, 5),
    (11, 12, 26, 30, 4),
    (12, 13, 20, 25, 5),
    (13, 14, 22, 30, 8),
    (14, 15, 30, 35, 5);

-- RegistrationList Table
INSERT INTO RegistrationList (StudentID, ClassID, Status) VALUES
    (1, 1, 'enrolled'),
    (2, 1, 'enrolled'),
    (3, 2, 'enrolled'),
    (4, 3, 'enrolled'),
    (5, 4, 'enrolled'),
    (6, 5, 'enrolled'),
    (7, 6, 'enrolled'),
    (8, 7, 'enrolled'),
    (9, 8, 'enrolled'),
    (10, 9, 'enrolled'),
    (11, 10, 'enrolled'),
    (12, 11, 'enrolled'),
    (13, 12, 'enrolled'),
    (14, 13, 'enrolled'),
    (15, 14, 'enrolled');
