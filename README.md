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
2) Apply `sql/db_init.sql` to the database (Or run a database rebuild later (see below))

Optional:
3) Create a new user with `CREATE USER '[USERNAME]'@'localhost' IDENTIFIED BY '[PASSWORD]';`
4) Give this user access to the database with `GRANT ALL PRIVILEGES ON stoodle.* TO '[USERNAME]'@'localhost';`

### Environment variables
Create `config.py` in the root folder with the following contents
```
# Database Connection
MYSQL_HOST = 'localhost'
MYSQL_DB = 'stoodle'
MYSQL_USER = '[USERNAME]'
MYSQL_PASSWORD = '[PASSWORD]'
SECRET_KEY = '[SECRET_KEY]'
```

USERNAME and PASSWORD are those used when setting up a database
SECRET_KEY is any sequence of characters and can be generated with `python -c 'import secrets; print(secrets.token_hex())'`

### Running

5) Run `flask run` to test the website locally. (Optionally add `--debug` for hot reloading)

### Rebuilding the database
Since this is active development, the database schema is changing frequently. The easiest way to keep up to date with this is to ensure sql/init_db.sql has the proper sql commands to setup the database and then use the rebuild_db.py script:
1) Run `cd sql`
2) Run `python rebuild_db.py`