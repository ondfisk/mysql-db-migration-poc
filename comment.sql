-- Get table comments
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    TABLE_COMMENT
FROM
    information_schema.TABLES
WHERE
    TABLE_TYPE = 'BASE TABLE' AND
    TABLE_COMMENT != '' AND
    TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');

-- Remove table comments
SELECT
    CONCAT("ALTER TABLE ", TABLE_SCHEMA, ".", TABLE_NAME, " COMMENT '';")
FROM
    information_schema.TABLES
WHERE
    TABLE_TYPE = 'BASE TABLE' AND
    TABLE_COMMENT != '' AND
    TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');

-- Get column comments
SELECT
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    c.COLUMN_NAME,
    c.COLUMN_COMMENT
FROM
    information_schema.TABLES AS t
    JOIN information_schema.COLUMNS AS c ON t.TABLE_SCHEMA = c.TABLE_SCHEMA AND t.TABLE_NAME = c.TABLE_NAME
WHERE
    t.TABLE_TYPE = 'BASE TABLE' AND
    c.COLUMN_COMMENT != '' AND
    t.TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys');

-- Remove column comments
SELECT
    CONCAT('ALTER TABLE ', '`',TABLE_NAME,'` ',
       'MODIFY COLUMN `', COLUMN_NAME,'` ',
        COLUMN_TYPE,
        IF(IS_NULLABLE = 'no', ' NOT NULL ', ''),
        IF(COLUMN_DEFAULT IS NULL, '', CONCAT(' DEFAULT ', QUOTE(COLUMN_DEFAULT))), ';')
    AS COLUMN_DEFINITION
FROM
    information_schema.COLUMNS
WHERE
    TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys') AND
    COLUMN_COMMENT != '';
