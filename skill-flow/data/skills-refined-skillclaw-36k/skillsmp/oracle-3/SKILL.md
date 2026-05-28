---
name: oracle
description: Oracle database operations including database link creation and management.
---

# Oracle

```sql
CREATE DATABASE LINK $LINK_NAME
    CONNECT TO $DB_USER  IDENTIFIED BY "$DB_PASS"
    USING '(DESCRIPTION=
                (ADDRESS=(PROTOCOL=TCP)(HOST=$DB_HOST)(PORT=1521))
                (CONNECT_DATA=(SID=$DB_NAME))
            )';

DROP DATABASE LINK $LINK_NAME;
```