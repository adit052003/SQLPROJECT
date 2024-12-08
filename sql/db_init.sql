/*
* This file is used to recreate the database from scratch 
* Modify this with any database changes
*/

CREATE TABLE Files (
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Filename VARCHAR(255) NOT NULL
);

CREATE TABLE Users (
	ID INTEGER PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE Professors (
	ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL
);

CREATE TABLE Courses (
	ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    Code VARCHAR(255),
    Description TEXT,
    ImageID INTEGER,
    FOREIGN KEY (ImageID) REFERENCES Files(ID)
		ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE TABLE Sessions (
	ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    CourseID INTEGER NOT NULL,
    Title VARCHAR(256) NOT NULL,
    ProfessorID INTEGER NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Classroom VARCHAR(64),
    Time VARCHAR(64),
    Description TEXT,
    FOREIGN KEY (CourseID) REFERENCES Courses(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (ProfessorID) REFERENCES Professors(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE CourseSections(
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    CourseID INTEGER NOT NULL,
    Title VARCHAR(256) nOT NULL,
    PageID INTEGER NOT NULL,
    FOREIGN KEY (CourseID) REFERENCES Courses(ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE JoinedCourses (
	UserID INTEGER NOT NULL,
    CourseID INTEGER NOT NULL,
    JoinDate DATETIME NOT NULL DEFAULT NOW(),
    ViewDate DATETIME NOT NULL DEFAULT NOW(),
    PinIndex INTEGER,
    PRIMARY KEY (UserID, CourseID),
    FOREIGN KEY (UserID) REFERENCES Users(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
	FOREIGN KEY (CourseID) REFERENCES Courses(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE CourseRatings (
	UserID INTEGER NOT NULL,
    CourseID INTEGER NOT NULL,
    Rating INTEGER NOT NULL,
    PRIMARY KEY (UserID, CourseID),
    FOREIGN KEY (UserID) REFERENCES Users(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
	FOREIGN KEY (CourseID) REFERENCES Courses(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE SessionRatings (
	UserID INTEGER NOT NULL,
    SessionID INTEGER NOT NULL,
    Rating INTEGER NOT NULL,
    PRIMARY KEY (UserID, SessionID),
    FOREIGN KEY (UserID) REFERENCES Users(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
	FOREIGN KEY (SessionID) REFERENCES Sessions(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Pages (
    ID INT AUTO_INCREMENT PRIMARY KEY,      
    CourseID INT NOT NULL,                   
    Title VARCHAR(255) NOT NULL,             
    SectionIndex INT NOT NULL,               
    Content TEXT,                            
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
    FOREIGN KEY (CourseID) REFERENCES Courses(ID) ON DELETE CASCADE
);


-- Sample Data

-- A user with email `test@gmail.com` and password `test`
INSERT INTO Users (ID, FirstName, LastName, Email, Password) VALUES (1, "Test", "Test", "test@gmail.com", 'scrypt:32768:8:1$wwbniKshCMoT63yt$ebd4195e3b04f0cc2545a67aae05dd806a076b327fe8ceb84846491c9baaab4816df41f2bc72eee3a7ad2bb54e87c85ea340e0236aa1a11103d03cd675f83f8a');

INSERT INTO Professors (FirstName, LastName) VALUES ("Andrew", "Park");
INSERT INTO Professors (FirstName, LastName) VALUES ("Ryan", "Kopke");
INSERT INTO Professors (FirstName, LastName) VALUES ("Chris", "Morissey");

INSERT INTO Courses (Title, Code, Description) VALUES ("Introduction to Database Management Systems", "CMPT 339", "Learn about Databases");
INSERT INTO Courses (Title, Code) VALUES ("Life and Letters of Paul", "RELS 352");
INSERT INTO Courses (Title, Code) VALUES ("Introduction to Logic", "PHIL 103");
INSERT INTO Courses (Title, Code) VALUES ("Articulatory Phonetics", "LING 230");
INSERT INTO Courses (Title, Code) VALUES ("Modern Algebra", "MATH 450");
INSERT INTO Courses (Title, Code) VALUES ("Introduction to Linguistics", "LING 101");
INSERT INTO Courses (Title, Code) VALUES ("Human Flourishing", "FNDN 102");

INSERT INTO Sessions (CourseID, ProfessorID, Title, StartDate, EndDate, Classroom, Time, Description) VALUES (1, 1, "Fall 2024", STR_TO_DATE('September 4 2024', '%M %d %Y'), STR_TO_DATE('December 9 2024', '%M %d %Y'), "NEU 37", "TR 9:30 - 10:45 AM", "Teaches very well");
INSERT INTO Sessions (CourseID, ProfessorID, Title, StartDate, EndDate, Classroom, Time) VALUES (1, 1, "Spring 2022", STR_TO_DATE('September 4 2022', '%M %d %Y'), STR_TO_DATE('December 9 2022', '%M %d %Y'), "NEU 37", "TR 9:30 - 10:45 AM");
INSERT INTO Sessions (CourseID, ProfessorID, Title, StartDate, EndDate, Classroom, Time) VALUES (4, 2, "Fall 2024", STR_TO_DATE('September 4 2024', '%M %d %Y'), STR_TO_DATE('December 9 2024', '%M %d %Y'), "CANIL 209", "TR 12:00 - 1:15 PM / F 1:30 - 2:45 PM");
INSERT INTO Sessions (CourseID, ProfessorID, Title, StartDate, EndDate, Classroom, Time) VALUES (3, 3, "Fall 2024", STR_TO_DATE('September 4 2024', '%M %d %Y'), STR_TO_DATE('December 9 2024', '%M %d %Y'), "RNT 121", "TR 1:30 - 2:45 AM");
INSERT INTO Sessions (CourseID, ProfessorID, Title, StartDate, EndDate, Classroom, Time) VALUES (6, 2, "Spring 2024 A", STR_TO_DATE('January 10 2024', '%M %d %Y'), STR_TO_DATE('April 17 2024', '%M %d %Y'), "CANIL 208", "MW 12:00 - 1:15 PM");
INSERT INTO Sessions (CourseID, ProfessorID, Title, StartDate, EndDate, Classroom, Time) VALUES (6, 2, "Spring 2024 B", STR_TO_DATE('January 10 2024', '%M %d %Y'), STR_TO_DATE('April 17 2024', '%M %d %Y'), "CANIL 218", "WF 3:00 - 4:15 PM");

INSERT INTO CourseSections (CourseID, Title, PageID) VALUES (1, "Unit 1", 1);
INSERT INTO CourseSections (CourseID, Title, PageID) VALUES (1, "Unit 2", 2);
INSERT INTO CourseSections (CourseID, Title, PageID) VALUES (1, "Unit 3", 3);

INSERT INTO JoinedCourses (UserID, CourseID, PinIndex) VALUES (1, 1, 1);
INSERT INTO JoinedCourses (UserID, CourseID, PinIndex) VALUES (1, 5, 2);
INSERT INTO JoinedCourses (UserID, CourseID) VALUES (1, 2);
INSERT INTO JoinedCourses (UserID, CourseID) VALUES (1, 3);

INSERT INTO CourseRatings (UserID, CourseID, Rating) VALUES (1, 1, 10);
INSERT INTO CourseRatings (UserID, CourseID, Rating) VALUES (1, 2, 9);
INSERT INTO CourseRatings (UserID, CourseID, Rating) VALUES (1, 3, 6);
INSERT INTO CourseRatings (UserID, CourseID, Rating) VALUES (1, 6, 10);

INSERT INTO SessionRatings (UserID, SessionID, Rating) VALUES (1, 1, 10);
INSERT INTO SessionRatings (UserID, SessionID, Rating) VALUES (1, 2, 7);
INSERT INTO SessionRatings (UserID, SessionID, Rating) VALUES (1, 3, 10);

INSERT INTO Pages (CourseID, Title, SectionIndex, Content)
VALUES
    (1, 'Introduction to Python', 1, 'This is an introduction to Python programming.'),
    (1, 'Data Types and Variables', 2, 'Learn about data types and variables in Python.'),
    (2, 'Course Overview', 1, 'Welcome to the advanced mathematics course.'),
    (2, 'Functions and Graphs', 2, 'An introduction to mathematical functions and graphs.');

