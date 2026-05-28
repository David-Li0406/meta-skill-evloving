#!/usr/bin/env python3
"""
Vocabulary Package Validator

Validates vocabulary packages against structural and coherence rules.
See references/validation-rules.md for rule specifications.

Usage:
    python validate_vocab.py vocab.json
    python validate_vocab.py vocab.json --strict
    python validate_vocab.py vocab.json --format json
"""

import json
import sys
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class ValidationResult:
    severity: Severity
    rule: str
    message: str
    path: Optional[str] = None

    def __str__(self) -> str:
        loc = f" at {self.path}" if self.path else ""
        return f"[{self.severity.value}] {self.rule}: {self.message}{loc}"


def validate_vocab(vocab: dict) -> list[ValidationResult]:
    """Run all validation rules against a vocabulary package."""
    results = []

    # Build indexes for reference checks
    concept_ids = {c["id"] for c in vocab.get("concepts", [])}
    axis_ids = {a["id"] for a in vocab.get("axes", [])}
    char_ids = {ch["id"] for ch in vocab.get("characteristics", [])}
    char_by_id = {ch["id"]: ch for ch in vocab.get("characteristics", [])}

    # R1: Unique identifiers
    results.extend(_check_unique_ids(vocab.get("concepts", []), "concept"))
    results.extend(_check_unique_ids(vocab.get("axes", []), "axis"))
    results.extend(_check_unique_ids(vocab.get("characteristics", []), "characteristic"))

    # R2: Relation targets exist
    for i, rel in enumerate(vocab.get("relations", [])):
        if rel.get("sourceId") not in concept_ids:
            results.append(ValidationResult(
                Severity.ERROR, "R2",
                f"Relation sourceId '{rel.get('sourceId')}' does not exist",
                f"relations[{i}]"
            ))
        if rel.get("targetId") not in concept_ids:
            results.append(ValidationResult(
                Severity.ERROR, "R2",
                f"Relation targetId '{rel.get('targetId')}' does not exist",
                f"relations[{i}]"
            ))

    # R3: Axis references exist
    for i, ch in enumerate(vocab.get("characteristics", [])):
        if ch.get("axisId") and ch["axisId"] not in axis_ids:
            results.append(ValidationResult(
                Severity.ERROR, "R3",
                f"Characteristic axisId '{ch['axisId']}' does not exist",
                f"characteristics[{i}]"
            ))

    for i, rel in enumerate(vocab.get("relations", [])):
        if rel.get("axisId") and rel["axisId"] not in axis_ids:
            results.append(ValidationResult(
                Severity.ERROR, "R3",
                f"Relation axisId '{rel['axisId']}' does not exist",
                f"relations[{i}]"
            ))

    # Process each concept
    for i, concept in enumerate(vocab.get("concepts", [])):
        cid = concept.get("id", f"<unnamed-{i}>")
        path = f"concepts[{i}] ({cid})"

        # R24: Preferred label present
        if not concept.get("prefLabel"):
            results.append(ValidationResult(
                Severity.ERROR, "R24",
                "Concept has no prefLabel",
                path
            ))

        # R9: Stable concepts need definitions
        if concept.get("status") == "stable":
            if not concept.get("definitions"):
                results.append(ValidationResult(
                    Severity.ERROR, "R9",
                    "Stable concept has no definitions",
                    path
                ))

        # R12, R13, R14, R15: Compound concept rules
        if concept.get("kind") == "compound":
            components = concept.get("components", [])
            
            if len(components) < 2:
                results.append(ValidationResult(
                    Severity.ERROR, "R12",
                    f"Compound concept has {len(components)} components (minimum 2)",
                    path
                ))
            
            component_axes = [c.get("axisId") for c in components]
            if len(set(component_axes)) != len(component_axes):
                results.append(ValidationResult(
                    Severity.ERROR, "R13",
                    "Compound concept has duplicate axis in components",
                    path
                ))
            
            for j, comp in enumerate(components):
                if comp.get("conceptId") not in concept_ids:
                    results.append(ValidationResult(
                        Severity.ERROR, "R14",
                        f"Component conceptId '{comp.get('conceptId')}' does not exist",
                        f"{path}.components[{j}]"
                    ))
                if comp.get("axisId") not in axis_ids:
                    results.append(ValidationResult(
                        Severity.ERROR, "R14",
                        f"Component axisId '{comp.get('axisId')}' does not exist",
                        f"{path}.components[{j}]"
                    ))
            
            has_multi = any(d.get("scope") == "multi" for d in concept.get("definitions", []))
            if not has_multi:
                results.append(ValidationResult(
                    Severity.WARNING, "R15",
                    "Compound concept has no multi-scope definition",
                    path
                ))

        # Process each definition
        for j, defn in enumerate(concept.get("definitions", [])):
            dpath = f"{path}.definitions[{j}]"

            # R5: Axis-scope definitions require parent
            if defn.get("scope") == "axis" and not defn.get("parentId"):
                results.append(ValidationResult(
                    Severity.ERROR, "R5",
                    "Axis-scope definition has no parentId",
                    dpath
                ))
            if defn.get("axisId") and not defn.get("parentId"):
                results.append(ValidationResult(
                    Severity.ERROR, "R5",
                    "Definition with axisId has no parentId",
                    dpath
                ))

            # R6: Parent reference exists
            if defn.get("parentId") and defn["parentId"] not in concept_ids:
                results.append(ValidationResult(
                    Severity.ERROR, "R6",
                    f"Definition parentId '{defn['parentId']}' does not exist",
                    dpath
                ))

            # R4: Characteristic references exist
            for char_id in defn.get("delimitingCharacteristicIds", []):
                if char_id not in char_ids:
                    results.append(ValidationResult(
                        Severity.ERROR, "R4",
                        f"Delimiting characteristic '{char_id}' does not exist",
                        dpath
                    ))

            # R7: No cross-axis contamination
            if defn.get("axisId"):
                for char_id in defn.get("delimitingCharacteristicIds", []):
                    char = char_by_id.get(char_id)
                    if char and char.get("axisId") != defn["axisId"]:
                        results.append(ValidationResult(
                            Severity.ERROR, "R7",
                            f"Characteristic '{char_id}' is from axis '{char.get('axisId')}' "
                            f"but definition is on axis '{defn['axisId']}'",
                            dpath
                        ))

            # R3: Definition axis reference exists
            if defn.get("axisId") and defn["axisId"] not in axis_ids:
                results.append(ValidationResult(
                    Severity.ERROR, "R3",
                    f"Definition axisId '{defn['axisId']}' does not exist",
                    dpath
                ))

            # R8: Root definitions have no parent
            if defn.get("scope") == "root" and defn.get("parentId"):
                results.append(ValidationResult(
                    Severity.ERROR, "R8",
                    "Root-scope definition has a parentId",
                    dpath
                ))

    # R10: Stable concepts need siblings
    results.extend(_check_siblings(vocab))

    # R16, R17, R18, R19: Relation rules
    seen_relations = set()
    for i, rel in enumerate(vocab.get("relations", [])):
        rpath = f"relations[{i}]"

        # R18: No self-referential relations
        if rel.get("sourceId") == rel.get("targetId"):
            results.append(ValidationResult(
                Severity.ERROR, "R18",
                f"Relation is self-referential: {rel.get('sourceId')}",
                rpath
            ))

        # R17: Associative relations have labels
        if rel.get("type") == "associative" and not rel.get("label"):
            results.append(ValidationResult(
                Severity.WARNING, "R17",
                "Associative relation has no label",
                rpath
            ))

        # R19: No duplicate relations
        rel_key = (rel.get("type"), rel.get("sourceId"), rel.get("targetId"), rel.get("axisId"))
        if rel_key in seen_relations:
            results.append(ValidationResult(
                Severity.WARNING, "R19",
                f"Duplicate relation: {rel.get('type')} from {rel.get('sourceId')} to {rel.get('targetId')}",
                rpath
            ))
        seen_relations.add(rel_key)

    # R20, R21, R22: Mapping rules
    for i, mapping in enumerate(vocab.get("mappings", [])):
        mpath = f"mappings[{i}]"

        # R20: Mapping concept references exist
        if mapping.get("conceptId") not in concept_ids:
            results.append(ValidationResult(
                Severity.ERROR, "R20",
                f"Mapping conceptId '{mapping.get('conceptId')}' does not exist",
                mpath
            ))

        # R21: Lossy mappings documented
        if mapping.get("mappingType") == "lossy" and not mapping.get("notes"):
            results.append(ValidationResult(
                Severity.WARNING, "R21",
                "Lossy mapping has no notes explaining what is lost",
                mpath
            ))

        # R22: Mapping versions valid
        sv = mapping.get("sinceVersion")
        if sv and not re.match(r"^\d+\.\d+\.\d+$", sv):
            results.append(ValidationResult(
                Severity.WARNING, "R22",
                f"sinceVersion '{sv}' is not valid semver",
                mpath
            ))

    # R25: No orphan concepts
    results.extend(_check_orphans(vocab))

    return results


def _check_unique_ids(items: list, entity_type: str) -> list[ValidationResult]:
    """Check for duplicate IDs within an entity type."""
    results = []
    seen = {}
    for i, item in enumerate(items):
        item_id = item.get("id")
        if item_id in seen:
            results.append(ValidationResult(
                Severity.ERROR, "R1",
                f"Duplicate {entity_type} ID '{item_id}' (first at index {seen[item_id]})",
                f"{entity_type}s[{i}]"
            ))
        else:
            seen[item_id] = i
    return results


def _check_siblings(vocab: dict) -> list[ValidationResult]:
    """Check that stable concepts have siblings on their defining axis (R10)."""
    results = []

    # Build index: (parentId, axisId) -> list of concept IDs
    axis_siblings: dict[tuple, list[str]] = {}
    for concept in vocab.get("concepts", []):
        for defn in concept.get("definitions", []):
            if defn.get("axisId") and defn.get("parentId"):
                key = (defn["parentId"], defn["axisId"])
                axis_siblings.setdefault(key, []).append(concept["id"])

    # Check stable concepts
    for i, concept in enumerate(vocab.get("concepts", [])):
        if concept.get("status") != "stable":
            continue
        for defn in concept.get("definitions", []):
            if defn.get("axisId") and defn.get("parentId"):
                key = (defn["parentId"], defn["axisId"])
                siblings = axis_siblings.get(key, [])
                if len(siblings) < 2:
                    results.append(ValidationResult(
                        Severity.WARNING, "R10",
                        f"Stable concept has no siblings on axis '{defn['axisId']}' "
                        f"under parent '{defn['parentId']}'",
                        f"concepts[{i}] ({concept['id']})"
                    ))
    return results


def _check_orphans(vocab: dict) -> list[ValidationResult]:
    """Check for concepts with no incoming generic or partitive relations (R25)."""
    results = []
    
    # Find concepts that are targets of generic or partitive relations
    has_parent = set()
    for rel in vocab.get("relations", []):
        if rel.get("type") in ("generic", "partitive"):
            has_parent.add(rel.get("sourceId"))

    # Check concepts
    for i, concept in enumerate(vocab.get("concepts", [])):
        cid = concept.get("id")
        
        # Skip if it has a root-scope definition
        is_root = any(d.get("scope") == "root" for d in concept.get("definitions", []))
        if is_root:
            continue
        
        if cid not in has_parent:
            results.append(ValidationResult(
                Severity.WARNING, "R25",
                "Concept has no incoming generic or partitive relation (orphan)",
                f"concepts[{i}] ({cid})"
            ))

    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate vocabulary package")
    parser.add_argument("file", help="Path to vocabulary package JSON file")
    parser.add_argument("--strict", action="store_true", 
                       help="Treat warnings as errors")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                       help="Output format")
    args = parser.parse_args()

    # Load vocabulary
    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(path) as f:
            vocab = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate
    results = validate_vocab(vocab)

    # Filter by severity if strict
    errors = [r for r in results if r.severity == Severity.ERROR]
    warnings = [r for r in results if r.severity == Severity.WARNING]

    # Output
    if args.format == "json":
        output = {
            "file": str(path),
            "errors": len(errors),
            "warnings": len(warnings),
            "results": [
                {
                    "severity": r.severity.value,
                    "rule": r.rule,
                    "message": r.message,
                    "path": r.path
                }
                for r in results
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"Validating: {path}")
        print(f"Errors: {len(errors)}, Warnings: {len(warnings)}")
        print()
        
        if errors:
            print("ERRORS:")
            for r in errors:
                print(f"  {r}")
            print()
        
        if warnings:
            print("WARNINGS:")
            for r in warnings:
                print(f"  {r}")
            print()

    # Exit code
    if errors:
        sys.exit(1)
    if args.strict and warnings:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
