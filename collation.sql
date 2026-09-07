-- TODO: Figure out how to set server default character set and collation

-- Get database defaults
SELECT
    SCHEMA_NAME,
    DEFAULT_CHARACTER_SET_NAME,
    DEFAULT_COLLATION_NAME
FROM
    information_schema.SCHEMATA
WHERE
    SCHEMA_NAME NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');

-- Update database defaults
SELECT
    CONCAT('ALTER DATABASE ', SCHEMA_NAME, ' CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;')
    SCHEMA_NAME
FROM
    information_schema.SCHEMATA
WHERE
    SCHEMA_NAME NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');

-- Get table collation
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    TABLE_COLLATION
FROM
    information_schema.TABLES
WHERE
    TABLE_TYPE = 'BASE TABLE' AND
    TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');

-- Update table collation (converts all columns)
SET foreign_key_checks = 0; -- set to 0, then run alter, then set to 1

SELECT
    CONCAT('ALTER TABLE ', TABLE_SCHEMA, '.', TABLE_NAME, ' CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;')
FROM
    information_schema.TABLES
WHERE
    TABLE_TYPE = 'BASE TABLE' AND
    TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');
