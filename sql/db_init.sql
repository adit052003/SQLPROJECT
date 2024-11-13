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

CREATE TABLE Courses (
	ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(255) NOT NULL,
    Code VARCHAR(255)
);

-- Add a dummy user with email `test@gmail.com` and password `test`
INSERT INTO Users (ID, FirstName, LastName, Email, Password) VALUES (1, "Test", "Test", "test@gmail.com", 'scrypt:32768:8:1$wwbniKshCMoT63yt$ebd4195e3b04f0cc2545a67aae05dd806a076b327fe8ceb84846491c9baaab4816df41f2bc72eee3a7ad2bb54e87c85ea340e0236aa1a11103d03cd675f83f8a');

INSERT INTO Courses (Title, Code) VALUES ("Introduction to Database Management Systems", "CMPT 339");
INSERT INTO Courses (Title, Code) VALUES ("Life and Letters of Paul", "RELS 352");
INSERT INTO Courses (Title, Code) VALUES ("Introduction to Logic", "PHIL 103");
INSERT INTO Courses (Title, Code) VALUES ("Articulatory Phonetics", "LING 230");
INSERT INTO Courses (Title, Code) VALUES ("Modern Algebra", "MATH 450");