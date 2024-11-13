/*
* This file is used to recreate the database from scratch 
* Modify this with any database changes
*/
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
    Code VARCHAR(255)
);

CREATE TABLE Sessions (
	ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    CourseID INTEGER NOT NULL,
    ProfessorID INTEGER NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    Classroom VARCHAR(64),
    Time VARCHAR(64),
    Title VARCHAR(4),
    FOREIGN KEY (CourseID) REFERENCES Courses(ID)
		ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (ProfessorID) REFERENCES Professors(ID)
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


-- Sample Data

-- A user with email `test@gmail.com` and password `test`
INSERT INTO Users (ID, FirstName, LastName, Email, Password) VALUES (1, "Test", "Test", "test@gmail.com", 'scrypt:32768:8:1$wwbniKshCMoT63yt$ebd4195e3b04f0cc2545a67aae05dd806a076b327fe8ceb84846491c9baaab4816df41f2bc72eee3a7ad2bb54e87c85ea340e0236aa1a11103d03cd675f83f8a');

INSERT INTO Professors (FirstName, LastName) VALUES ("Andrew", "Park");
INSERT INTO Professors (FirstName, LastName) VALUES ("Ryan", "Kopke");
INSERT INTO Professors (FirstName, LastName) VALUES ("Chris", "Morissey");

INSERT INTO Courses (Title, Code) VALUES ("Introduction to Database Management Systems", "CMPT 339");
INSERT INTO Courses (Title, Code) VALUES ("Life and Letters of Paul", "RELS 352");
INSERT INTO Courses (Title, Code) VALUES ("Introduction to Logic", "PHIL 103");
INSERT INTO Courses (Title, Code) VALUES ("Articulatory Phonetics", "LING 230");
INSERT INTO Courses (Title, Code) VALUES ("Modern Algebra", "MATH 450");
INSERT INTO Courses (Title, Code) VALUES ("Introduction to Linguistics", "LING 101");
INSERT INTO Courses (Title, Code) VALUES ("Human Flourishing", "FNDN 102");

INSERT INTO Sessions (CourseID, ProfessorID, StartDate, EndDate, Classroom, Time) VALUES (1, 1, STR_TO_DATE('September 4 2024', '%M %d %Y'), STR_TO_DATE('December 9 2024', '%M %d %Y'), "NEU 37", "TR 9:30 - 10:45 AM");
INSERT INTO Sessions (CourseID, ProfessorID, StartDate, EndDate, Classroom, Time) VALUES (1, 1, STR_TO_DATE('September 4 2022', '%M %d %Y'), STR_TO_DATE('December 9 2022', '%M %d %Y'), "NEU 37", "TR 9:30 - 10:45 AM");
INSERT INTO Sessions (CourseID, ProfessorID, StartDate, EndDate, Classroom, Time) VALUES (4, 2, STR_TO_DATE('September 4 2024', '%M %d %Y'), STR_TO_DATE('December 9 2024', '%M %d %Y'), "CANIL 209", "TR 12:00 - 1:15 PM / F 1:30 - 2:45 PM");
INSERT INTO Sessions (CourseID, ProfessorID, StartDate, EndDate, Classroom, Time) VALUES (3, 3, STR_TO_DATE('September 4 2024', '%M %d %Y'), STR_TO_DATE('December 9 2024', '%M %d %Y'), "RNT 121", "TR 1:30 - 2:45 AM");
INSERT INTO Sessions (CourseID, ProfessorID, StartDate, EndDate, Classroom, Time, Title) VALUES (6, 2, STR_TO_DATE('January 10 2024', '%M %d %Y'), STR_TO_DATE('April 17 2024', '%M %d %Y'), "CANIL 208", "MW 12:00 - 1:15 PM", "A");
INSERT INTO Sessions (CourseID, ProfessorID, StartDate, EndDate, Classroom, Time, Title) VALUES (6, 2, STR_TO_DATE('January 10 2024', '%M %d %Y'), STR_TO_DATE('April 17 2024', '%M %d %Y'), "CANIL 218", "WF 3:00 - 4:15 PM", "B");

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
