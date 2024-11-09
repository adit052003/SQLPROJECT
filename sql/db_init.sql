/*
* This file is used to recreate the database from scratch 
* Modify this with any database changes
*/
CREATE SCHEMA IF NOT EXISTS stoodle;

CREATE TABLE Users (
	ID INTEGER PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password_ VARCHAR(255) NOT NULL
);