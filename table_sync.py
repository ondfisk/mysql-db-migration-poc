# python3 -m venv .venv
# source .venv/bin/activate
# python3 -m pip install python-dotenv mysql-connector-python

from dotenv import load_dotenv
import os
import sys
import mysql.connector
import re

column_pattern = re.compile(r"^\s*`([^`]+)`\s+(\w+(?:\([^)]*\))?)(.*)$", re.IGNORECASE | re.MULTILINE)
character_set_pattern = re.compile(r"\s+CHARACTER SET\s+\w+", re.IGNORECASE)
collate_pattern = re.compile(r"\s+COLLATE\s+\w+", re.IGNORECASE)
comment_pattern = re.compile(r"\s+COMMENT\s+'[^']+'", re.IGNORECASE)


def generate_alter_statements(connection, schema_name, table_name):
    table_definition = get_table_definition(connection, schema_name, table_name)
    lines = table_definition.split("\n")

    yield f"ALTER TABLE {schema_name}.{table_name} CONVERT TO CHARSET DEFAULT;"

    if "COMMENT" in lines[-1]:
        yield f"ALTER TABLE {schema_name}.{table_name} COMMENT '';"

    for line in lines:
        alter = False
        stripped = line.strip()
        match = column_pattern.match(stripped)
        if match:
            column_name = match.group(1)
            column_type = match.group(2)
            column_details = match.group(3)

            if column_details[-1] == ",":
                column_details = column_details[0:-1]

            if "unsigned" in column_details:
                column_details = column_details.replace("unsigned", "")
                alter = True

            if "CHARACTER SET" in column_details:
                column_details = character_set_pattern.sub("", column_details)
                alter = True

            if "COLLATE" in column_details:
                column_details = collate_pattern.sub("", column_details)
                alter = True

            if "COMMENT" in column_details:
                column_details = comment_pattern.sub("", column_details)
                alter = True

            if alter:
                yield f"ALTER TABLE {schema_name}.{table_name} MODIFY {column_name} {column_type} {column_details.strip()};"


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=os.getenv("MYSQL_PORT"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    )


def get_tables(connection, schema):
    with connection.cursor() as cursor:
        query = """
            SELECT
                TABLE_NAME
            FROM
                information_schema.TABLES
            WHERE
                TABLE_SCHEMA = %s
            ORDER BY
                TABLE_NAME;
        """
        cursor.execute(query, (schema,))

        return cursor.fetchall()


def get_table_definition(connection, schema_name, table_name):
    with connection.cursor() as cursor:
        query = f"SHOW CREATE TABLE {schema_name}.{table_name};" ""
        cursor.execute(query)
        row = cursor.fetchone()
        return row[1]


def write_output(file, query):
    with open(file, "a") as f:
        f.write(query + "\n")


def main():
    schema_name = "classicmodels5"
    file_name = "alter_collation.sql"
    write_output(file_name, "SET FOREIGN_KEY_CHECKS=0;")
    write_output(file_name, f"ALTER DATABASE {schema_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;")
    with get_connection() as connection:
        tables = get_tables(connection, schema_name)
        for (table_name,) in tables:
            alter_statements = generate_alter_statements(connection, schema_name, table_name)
            for alter_statement in alter_statements:
                write_output(file_name, alter_statement)


if __name__ == "__main__":
    load_dotenv()
    sys.exit(main())
