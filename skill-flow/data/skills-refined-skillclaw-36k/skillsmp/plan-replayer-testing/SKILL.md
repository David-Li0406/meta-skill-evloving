---
name: plan-replayer-testing
description: Expertise in adding new test cases for the TiDB plan replayer. Use when the user provides a plan replayer zip file and wants to create a new test.
---

# Plan Replayer Testing Expert

You are an expert in creating new test cases for the TiDB plan replayer. When a user asks you to add a new test, follow this procedure precisely.

### Prerequisites

Before you begin, ensure the user has provided the following information. If not, you must ask for it:

1.  The file path to the plan replayer zip file.
2.  The target path for the new test case (e.g., `abc/123`).

### Procedure

#### 1. Create Directories

Based on the user-provided target path, create the necessary directories for the test file and the replayer file.

```shell
# For a target path like "abc/123"
mkdir -p t/abc/123
mkdir -p replayer/abc/123
```

#### 2. Copy Plan Replayer File

Copy the user-provided zip file into the new `replayer/` subdirectory. **Do not change the filename.**

#### 3. Extract Information from Zip File

To get the necessary components for the test, you must extract them from the zip file.

a. Create a temporary directory: `TMP_DIR=$(mktemp -d)`
b. Unzip the file into it: `unzip /path/to/replayer.zip -d "$TMP_DIR"`
c. **Extract SQL Query**: Find and read the SQL file in the `$TMP_DIR/sql/` subdirectory.
d. **Extract Database Name**: Find any file in `$TMP_DIR/schema/` and read its content. Extract the database name from the `CREATE DATABASE` statement.
e. **Extract Timestamp**: Read the `$TMP_DIR/variables.toml` file and extract the string value for the `timestamp` variable. This is critical for making the test deterministic.
f. **Check for TiFlash Replica**: Check if the file `$TMP_DIR/table_tiflash_replica.txt` exists and is not empty. This determines if a special wait flag is needed.
g. **Cleanup**: Remember to remove the temporary directory: `rm -rf "$TMP_DIR"`

#### 4. Create the `.test` File

a.  **Determine Filename**:
    *   If the zip filename is `replayer_pZHg0IzNHaG9moOOzB0UqA==_1763627785193823416.zip`, the test filename should be `pZHg0.test`.
    *   If the filename is `query95.zip`, the test filename should be `query95.test`.
    *   If there's a naming conflict, append the date (`YYYYMMDD`) before the `.test` extension.

b.  **Write Content**: Create the `.test` file in the `t/` subdirectory you created. Use the following template, replacing all placeholders.

```sql
drop database if exists <database_name>;
plan replayer load './relative path of the replayer file relative to the project root';
--wait_tiflash_replica_ready

-- Replace date/time functions in the query with the extracted timestamp
-- e.g., CURRENT_DATE() becomes '<timestamp_value>'
explain format = 'plan_tree' <test query>;
select @@last_plan_from_cache,@@last_sql_use_alloc,@@last_plan_from_binding;
drop database if exists <database_name>;
```

*   If a TiFlash replica was detected (step 3.f), keep the `--wait_tiflash_replica_ready` line. Otherwise, remove it.

#### 5. Verify the Test

a.  Execute the test using the script bundled with the skill. The test path should not include the `.test` suffix.

    ```shell
    .gemini/skills/plan-replayer-testing/scripts/run-tests.sh -r <test_path>
    ```

b.  **Check for SQL Binding**: After the run, check the output. If the result for `@@last_plan_from_binding;` is `1`, you must modify the test to run twice: once with the binding and once without.

c.  **Modify for Binding**: If a binding was used, insert the following SQL block right after the first `select ...;` line in the `.test` file.

    ```sql
    set @old=@@timestamp;
    set @@timestamp=0;
    UPDATE mysql.bind_info SET status = 'deleted', update_time = NOW(6) WHERE source != 'builtin';
    admin reload bindings;
    set @@timestamp=@old;
    ```
    
    Then, duplicate the `explain ...;` and the final `select ...;` lines and append them to the file.

d.  **Re-record Result**: Run the test again with the `-r` flag to record the new, dual output.

    ```shell
    .gemini/skills/plan-replayer-testing/scripts/run-tests.sh -r <test_path>
    ```

If any step fails, analyze the error output and attempt to fix it before reporting back to the user.
