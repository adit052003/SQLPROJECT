import pymysql
import sys
sys.path.append('../') # Make sure we can access config.py
import config

def connect_db():
    database = pymysql.connect(
        host = config.MYSQL_HOST,
        user = config.MYSQL_USER,
        password = config.MYSQL_PASSWORD,
        db = config.MYSQL_DB
    )
    return database

def parse_sql(filename):
    with open(filename, 'r') as file:
        stmts = []
        DELIMITER = ';'
        stmt = None
        comment = False

        for line in file.readlines():
            # Get rid of comments and empty lines
            if "/*" in line: 
                line = line.split("/*")[0]
                comment = True
            if comment and "*/" in line:
                comment = False
                line = line.split("*/")[-1]
            line = line.strip()
            if comment: continue
            if not line: continue
            if line.startswith('--'): continue

            # Add to the current statement
            if stmt != None:
                stmt += ' ' + line.strip()
                # End statement if delimiter found
                if line.strip().endswith(DELIMITER):
                    stmts.append(stmt)
                    stmt = None
            else:
                # Update delimiter to new delimiter
                if line.lower().startswith('delimiter'):
                    DELIMITER = line.split()[1]
                    stmts.append(line)
                # Start new statement
                else:
                    if line.strip().endswith(DELIMITER):
                        stmts.append(line.strip())
                    else:
                        stmt = line.strip()
        return stmts

def delete_tables(cursor):
    # Get Table Names
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (config.MYSQL_DB,))
    tables = cursor.fetchall()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for (table,) in tables:
        cursor.execute(f"DROP TABLE {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

def run_init(cursor):
    statements = parse_sql("db_init.sql")
    for statement in statements:
        print(statement)
        cursor.execute(statement)

def rebuild_db():
    db = connect_db()
    with db.cursor() as cursor:
        delete_tables(cursor)
        run_init(cursor)
    db.commit()

if __name__ == "__main__":
    rebuild_db()