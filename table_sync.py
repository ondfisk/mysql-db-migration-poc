# python3 -m venv .venv
# source .venv/bin/activate
# python3 -m pip install python-dotenv mysql-connector-python

from dotenv import load_dotenv
import os
import sys
import mysql.connector

def get_connection():
    load_dotenv()
    with mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        port=os.getenv('MYSQL_PORT'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
    ) as connection:
        return connection


def get_missing_tables(connection):
    connection.reconnect()
    cursor = connection.cursor()
    query = """
        SELECT
            TABLE_NAME,
            COUNT(*),
            GROUP_CONCAT(TABLE_SCHEMA ORDER BY TABLE_SCHEMA SEPARATOR ', ')
        FROM
            information_schema.TABLES
        WHERE
            TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
        GROUP BY
            TABLE_NAME
        HAVING
            COUNT(*) < (SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys'))
        ORDER BY
            TABLE_NAME;
    """
    cursor.execute(query)

    return cursor.fetchall()


def get_databases_missing_table(connection, table_name):
    connection.reconnect()
    cursor = connection.cursor()
    query = """
        SELECT
            TABLE_NAME,
            COUNT(*),
            GROUP_CONCAT(TABLE_SCHEMA ORDER BY TABLE_SCHEMA SEPARATOR ', ')
        FROM
            information_schema.TABLES
        WHERE
            TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
        GROUP BY
            TABLE_NAME
        HAVING
            COUNT(*) < (SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys'))
        ORDER BY
            TABLE_NAME;
    """
    cursor.execute(query)

    return cursor.fetchall()

def main():
    connection = get_connection()
    if not connection:
        return 1

    missing_tables = get_missing_tables(connection)

    print("table", "count", "databases")
    for table in missing_tables:
        print(*table)


if __name__ == "__main__":
    sys.exit(main())
