"""KGX transformation module for CMM strain data."""

from cmm_ai_automation.transform.bacdive_source import (
    query_all_strains,
    query_bacdive_by_ids,
    query_random_sample,
    transform_bacdive_doc,
)
from cmm_ai_automation.transform.kgx import (
    KGXEdge,
    KGXNode,
    normalize_curie,
    split_list_field,
)
from cmm_ai_automation.transform.writer import (
    deduplicate_nodes,
    flatten_results,
    write_kgx_jsonl,
)

__all__ = [
    "KGXEdge",
    "KGXNode",
    "deduplicate_nodes",
    "flatten_results",
    "normalize_curie",
    "query_all_strains",
    "query_bacdive_by_ids",
    "query_random_sample",
    "split_list_field",
    "transform_bacdive_doc",
    "write_kgx_jsonl",
]
