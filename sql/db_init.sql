/*
* This file is used to recreate the database from scratch 
* Modify this with any database changes
*/
CREATE SCHEMA IF NOT EXISTS stoodle;

CREATE TABLE IF NOT EXISTS test (
	id INTEGER PRIMARY KEY,
    name VARCHAR(20) NOT NULL
);

INSERT INTO test (id, name) VALUES (1, "Jack");