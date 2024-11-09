# SQLPROJECT

This is a term project for CMPT 339 at Trinity Western University

## Development Setup

### Setup code environment
1) Clone the repository locally
2) Run `python -m venv venv`
3) Run `venv/Scripts/activate` if on Windows
4) Run `pip install -r requirements.txt`

### Setup database
1) Create a new database in MySQL Workbench called `stoodle`
2) Apply `sql/db_init.sql` to the database

Optional:
3) Create a new user with `CREATE USER '[USERNAME]'@'localhost' IDENTIFIED BY '[PASSWORD]';`
4) Give this user access to the database with `GRANT ALL PRIVILEGES ON stoodle.* TO '[USERNAME]'@'localhost';`

### Environment variables
Create `application.cfg` in the root folder with the following contents
```
# Database Connection
MYSQL_HOST = 'localhost'
MYSQL_DB = 'stoodle'
MYSQL_USER = '[USERNAME]'
MYSQL_PASSWORD = '[PASSWORD]'
SECRET_KEY = '[SECRET_KEY]'
```

### Running

5) Run `flask run` to test the website locally. (Optionally add `--debug` for hot reloading)
