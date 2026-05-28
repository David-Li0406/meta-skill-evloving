"""SPARQL result parsing functions."""

from __future__ import annotations


def parse_sparql_concept_results(results: list[dict]) -> list[dict[str, str]]:
    """Parse SPARQL results into concept dictionaries.

    Args:
        results: Raw SPARQL query results with uri, name, title, abstract bindings

    Returns:
        List of concept dictionaries with uri, name, title, abstract keys
    """
    return [
        {
            'uri': r['uri']['value'],
            'name': r['name']['value'],
            'title': r['title']['value'],
            'abstract': r['abstract']['value']
        }
        for r in results
    ]


def parse_sparql_claims_result(results: list[dict]) -> list[dict[str, str]]:
    """Parse SPARQL results into claim dictionaries.

    Args:
        results: Raw SPARQL query results with claim, text bindings

    Returns:
        List of claim dictionaries with uri, text keys
    """
    return [
        {'uri': r['claim']['value'], 'text': r['text']['value']}
        for r in results
    ]


def parse_sparql_count_result(results: list[dict]) -> int:
    """Parse SPARQL COUNT result.

    Args:
        results: Raw SPARQL query results with count binding

    Returns:
        Count as integer, or 0 if empty
    """
    if results and 'count' in results[0]:
        return int(results[0]['count']['value'])
    return 0


def parse_extraction_concepts(
    concepts_raw: list[dict]
) -> tuple[dict[str, str], list[dict[str, str]]]:
    """Parse extracted concepts into name->description map and relations.

    Args:
        concepts_raw: Raw concept list from LLM with name, description,
            broader, partOf, dependsOn

    Returns:
        Tuple of (concepts dict mapping name to description, list of relation dicts)
    """
    concepts = {}
    relations = []
    for c in concepts_raw:
        concepts[c['name']] = c.get('description')
        for rel in ['broader', 'partOf', 'dependsOn']:
            if c.get(rel):
                relations.append({
                    'from': c['name'],
                    'type': rel,
                    'to': c[rel]
                })
    return concepts, relations


def validate_claim_relations(
    relations: list[dict[str, str]],
    valid_from_uris: set[str],
    valid_to_uris: set[str]
) -> tuple[list[dict[str, str]], int]:
    """Validate and filter claim relations by URI validity.

    Args:
        relations: Raw relations with 'from_uri', 'type', 'to_uri'
        valid_from_uris: Set of valid source claim URIs
        valid_to_uris: Set of valid target claim URIs

    Returns:
        Tuple of (validated relations list, count of filtered invalid)
    """
    validated = []
    invalid_count = 0
    for r in relations:
        from_uri = r['from_uri']
        to_uri = r['to_uri']
        if from_uri in valid_from_uris and to_uri in valid_to_uris:
            validated.append({'from': from_uri, 'type': r['type'], 'to': to_uri})
        else:
            invalid_count += 1
    return validated, invalid_count
