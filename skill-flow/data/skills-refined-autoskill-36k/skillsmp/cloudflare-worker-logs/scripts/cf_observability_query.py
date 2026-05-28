#!/usr/bin/env python3
"""Query Workers Observability telemetry data for logs and metrics."""

import argparse
from datetime import UTC, datetime, timedelta
import json
import os
import sys
from typing import Any

import httpx


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query Workers Observability API for logs and metrics"
    )
    parser.add_argument(
        "--view",
        choices=["events", "calculations", "invocations"],
        default="events",
        help="Query view type (default: events)",
    )
    parser.add_argument(
        "--minutes",
        type=int,
        default=60,
        help="Time range in minutes (default: 60, max: 10080 for 7 days)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Max results to return (default: 10)",
    )
    parser.add_argument(
        "--offset",
        help="Pagination offset (use $metadata.id from previous results)",
    )
    parser.add_argument(
        "--offset-by",
        type=int,
        help="Numeric offset for pagination",
    )
    parser.add_argument(
        "--offset-direction",
        choices=["next", "prev"],
        help="Pagination direction",
    )
    parser.add_argument(
        "--dry",
        action="store_true",
        help="Dry run - validate query without executing",
    )
    parser.add_argument(
        "--granularity",
        type=int,
        help="Time bucket granularity for calculations (auto-detected if omitted)",
    )
    parser.add_argument(
        "--filter",
        action="append",
        dest="filters",
        help="Filter in format key:operation:type:value (e.g., '$metadata.service:eq:string:llms')",
    )
    parser.add_argument(
        "--filter-combination",
        choices=["and", "or"],
        help="How to combine filters (default: and)",
    )
    parser.add_argument(
        "--calculation",
        action="append",
        dest="calculations",
        help="Calculation in format operator[:key[:key_type[:alias]]] (e.g., 'count', 'avg:wallTime:number:avg_wall')",
    )
    parser.add_argument(
        "--group-by",
        action="append",
        dest="group_bys",
        help="Field to group by in format value[:type] (e.g., '$metadata.service', '$metadata.level:string')",
    )
    parser.add_argument(
        "--order-by",
        help="Calculation alias to sort by",
    )
    parser.add_argument(
        "--order",
        choices=["asc", "desc"],
        default="desc",
        help="Sort order (default: desc)",
    )
    parser.add_argument(
        "--needle",
        help="Full-text search in log content",
    )
    parser.add_argument(
        "--needle-regex",
        action="store_true",
        help="Treat needle as regex",
    )
    args = parser.parse_args()

    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN")

    if not account_id:
        print(
            "Error: CLOUDFLARE_ACCOUNT_ID environment variable is required",
            file=sys.stderr,
        )
        return 1
    if not api_token:
        print(
            "Error: CLOUDFLARE_API_TOKEN environment variable is required",
            file=sys.stderr,
        )
        return 1

    now = datetime.now(UTC)
    from_time = now - timedelta(minutes=args.minutes)

    query_params: dict[str, Any] = {
        "datasets": ["cloudflare-workers"],
    }

    if args.filters:
        parsed_filters: list[dict[str, Any]] = []
        for f in args.filters:
            parts = f.split(":", 3)
            if len(parts) < 3:
                print(
                    f"Error: Invalid filter format '{f}'. Expected key:operation:type[:value]",
                    file=sys.stderr,
                )
                return 1
            filter_obj: dict[str, Any] = {
                "key": parts[0],
                "operation": parts[1],
                "type": parts[2],
            }
            if len(parts) == 4:
                filter_obj["value"] = parts[3]
            parsed_filters.append(filter_obj)
        if parsed_filters:
            query_params["filters"] = parsed_filters

    if args.filter_combination:
        query_params["filterCombination"] = args.filter_combination

    if args.needle:
        query_params["needle"] = {
            "value": args.needle,
            "isRegex": args.needle_regex,
            "matchCase": False,
        }

    if args.view == "calculations":
        if args.calculations:
            api_calculations: list[dict[str, Any]] = []
            for calc in args.calculations:
                parts = calc.split(":")
                calc_obj: dict[str, Any] = {"operator": parts[0]}
                if len(parts) >= 2:
                    calc_obj["key"] = parts[1]
                    calc_obj["keyType"] = parts[2] if len(parts) >= 3 else "number"
                if len(parts) >= 4:
                    calc_obj["alias"] = parts[3]
                api_calculations.append(calc_obj)
            query_params["calculations"] = api_calculations
        else:
            query_params["calculations"] = [{"operator": "count", "alias": "count"}]

        if args.group_bys:
            api_group_bys: list[dict[str, Any]] = []
            for gb in args.group_bys:
                parts = gb.split(":")
                api_group_bys.append(
                    {
                        "value": parts[0],
                        "type": parts[1] if len(parts) > 1 else "string",
                    }
                )
            query_params["groupBys"] = api_group_bys
            query_params["limit"] = args.limit

        if args.order_by:
            query_params["orderBy"] = {
                "value": args.order_by,
                "order": args.order,
            }

    payload: dict[str, Any] = {
        "queryId": "cf-observability-query",
        "view": args.view,
        "limit": args.limit,
        "timeframe": {
            "from": int(from_time.timestamp() * 1000),
            "to": int(now.timestamp() * 1000),
        },
        "parameters": query_params,
    }

    if args.dry:
        payload["dry"] = args.dry

    if args.granularity:
        payload["granularity"] = args.granularity

    if args.offset:
        payload["offset"] = args.offset

    if args.offset_by is not None:
        payload["offsetBy"] = args.offset_by

    if args.offset_direction:
        payload["offsetDirection"] = args.offset_direction

    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/workers/observability/telemetry/query"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    resp = httpx.post(url, headers=headers, json=payload, timeout=60.0)
    data = resp.json()

    if not data.get("success"):
        errors = data.get("errors", [])
        error_detail = data.get("error", {})
        if error_detail:
            errors.append(error_detail)
        print(f"API Error: {json.dumps(errors)}", file=sys.stderr)
        return 1

    result = data.get("result", {})

    if args.view == "events":
        events_data = result.get("events", {})
        events_list = events_data.get("events", [])
        if events_list:
            output: list[dict[str, Any]] = []
            for event in events_list:
                meta = event.get("$metadata", {})
                workers = event.get("$workers", {})
                workers_event = workers.get("event", {})
                formatted = {
                    "timestamp": meta.get("timestamp"),
                    "level": meta.get("level"),
                    "message": meta.get("message"),
                    "service": meta.get("service"),
                    "request_id": meta.get("requestId"),
                }
                if meta.get("error"):
                    formatted["error"] = meta.get("error")
                if meta.get("trigger"):
                    formatted["trigger"] = meta.get("trigger")
                if meta.get("origin"):
                    formatted["origin"] = meta.get("origin")
                # Extract non-redundant $workers fields
                if workers_event.get("response", {}).get("status") is not None:
                    formatted["status"] = workers_event["response"]["status"]
                if workers.get("outcome"):
                    formatted["outcome"] = workers.get("outcome")
                if workers.get("wallTimeMs") is not None:
                    formatted["wall_time_ms"] = workers.get("wallTimeMs")
                if workers.get("cpuTimeMs") is not None:
                    formatted["cpu_time_ms"] = workers.get("cpuTimeMs")
                if workers.get("truncated"):
                    formatted["truncated"] = workers.get("truncated")
                for k, v in event.items():
                    if not k.startswith("$"):
                        formatted[k] = v
                output.append(formatted)
            print(
                json.dumps(
                    {
                        "events": output,
                        "count": len(output),
                        "total": events_data.get("count", len(output)),
                    },
                    indent=2,
                )
            )
        else:
            series = events_data.get("series", [])
            if series:
                print(
                    json.dumps(
                        {"series": series[: args.limit], "total_buckets": len(series)},
                        indent=2,
                    )
                )
            else:
                print(json.dumps({"events": [], "count": 0}, indent=2))

    elif args.view == "calculations":
        calcs = result.get("calculations", [])
        timeseries = result.get("timeseries", {})
        if calcs:
            print(json.dumps({"calculations": calcs}, indent=2))
        elif timeseries:
            print(json.dumps({"timeseries": timeseries}, indent=2))
        else:
            print(json.dumps(result, indent=2))

    elif args.view == "invocations":
        invocations = result.get("invocations", [])
        if invocations:
            print(
                json.dumps(
                    {"invocations": invocations, "count": len(invocations)}, indent=2
                )
            )
        else:
            print(json.dumps(result, indent=2))

    else:
        print(json.dumps(result, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
