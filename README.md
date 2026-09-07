# MySQL Database Migration PoC

Run MySQL:

```sh
 docker run --name my-mysql --restart unless-stopped -e MYSQL_ROOT_PASSWORD=secret -v $HOME/mysql-data:/var/lib/mysql -d mysql:9.7.2
 ```

 ## Column Diff

```sql
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    ORDINAL_POSITION,
    COLUMN_DEFAULT,
    IS_NULLABLE,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    CHARACTER_SET_NAME,
    COLLATION_NAME,
    GROUP_CONCAT(TABLE_SCHEMA ORDER BY TABLE_SCHEMA SEPARATOR ', ')
 FROM
    information_schema.COLUMNS
WHERE
    TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
GROUP BY
    TABLE_NAME,
    COLUMN_NAME,
    ORDINAL_POSITION,
    COLUMN_DEFAULT,
    IS_NULLABLE,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    CHARACTER_SET_NAME,
    COLLATION_NAME
HAVING
    COUNT(*) < (SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys'))
ORDER BY
    TABLE_NAME,
    COLUMN_NAME
;
```

## Missing columns

```sql
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    GROUP_CONCAT(TABLE_SCHEMA ORDER BY TABLE_SCHEMA SEPARATOR ', ')
FROM
    information_schema.COLUMNS
WHERE
    TABLE_SCHEMA NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys')
GROUP BY
    TABLE_NAME,
    COLUMN_NAME
HAVING
    COUNT(*) < (SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME NOT IN ('mysql', 'information_schema', 'performance_schema', 'sys'))
ORDER BY
    TABLE_NAME,
    COLUMN_NAME
;
```

## Missing tables

```sql
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
```

## Notes

### Change datatype

```sql
ALTER TABLE customers MODIFY COLUMN city varchar(50) NOT NULL;
```

### Move column

```sql
ALTER TABLE customers MODIFY COLUMN city varchar(50) NOT NULL AFTER addressLine2;
```

## Rename column

```sql
ALTER TABLE customers CHANGE COLUMN city city2 varchar(50) NOT NULL;
```

### Column comment

```sql
ALTER TABLE customers MODIFY COLUMN city varchar(50) NOT NULL COMMENT "It's a city";
```

### Auto increment

#### Add

```sql
SET FOREIGN_KEY_CHECKS=0;
ALTER TABLE customers MODIFY COLUMN customerNumber int AUTO_INCREMENT;
SET FOREIGN_KEY_CHECKS=1;
```

#### Remove

```sql
SET FOREIGN_KEY_CHECKS=0;
ALTER TABLE customers MODIFY COLUMN customerNumber int;
SET FOREIGN_KEY_CHECKS=1;
```
