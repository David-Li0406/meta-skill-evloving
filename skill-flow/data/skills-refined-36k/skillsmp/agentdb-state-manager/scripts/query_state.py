#!/usr/bin/env python3
"""Query current workflow state from AgentDB.

Usage:
    python query_state.py [--slug SLUG] [--dependencies] [--task TASK_ID]
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Query workflow state from AgentDB")
    parser.add_argument("--slug", help="Filter by workflow slug")
    parser.add_argument("--dependencies", action="store_true", help="Show task dependencies")
    parser.add_argument("--task", help="Show dependencies for specific task")
    args = parser.parse_args()

    # Query current state (latest record per object)
    query = """
    SELECT DISTINCT ON (object_id)
        object_id, object_type, object_state, object_metadata
    FROM workflow_records
    ORDER BY object_id, record_datetimestamp DESC;
    """

    if args.dependencies:
        # Query task dependencies using metadata
        query = """
        WITH current_states AS (
            SELECT DISTINCT ON (object_id)
                object_id, object_type, object_state, object_metadata
            FROM workflow_records
            WHERE object_type = 'task'
            ORDER BY object_id, record_datetimestamp DESC
        )
        SELECT object_id, object_state,
               json_extract_string(object_metadata, '$.depends_on') as dependencies
        FROM current_states;
        """

    print("SQL Query (to be executed via AgentDB):")
    print(query)
    print("\nNOTE: In actual execution, would query AgentDB and display results")


if __name__ == "__main__":
    main()
