"""
WASDE Data Validation Script

Validates parsed WASDE data against business rules and historical patterns.
"""

import json
from typing import Dict, List, Tuple, Any, Optional


# Validation tolerances by commodity (in their respective units)
BALANCE_TOLERANCES = {
    # Grains (million bushels for US, million metric tons for World)
    "wheat_us": 5.0,
    "wheat_world": 1.0,
    "corn_us": 10.0,
    "corn_world": 2.0,
    "rice_us": 1.0,  # million cwt
    "rice_world": 0.5,

    # Oilseeds
    "soybeans_us": 5.0,
    "soybeans_world": 1.0,
    "soybean_oil_us": 100.0,  # million pounds
    "soybean_meal_us": 100.0,  # thousand short tons

    # Cotton (million 480-lb bales)
    "cotton_us": 0.2,
    "cotton_world": 1.0,

    # Livestock (million pounds)
    "beef_us": 50.0,
    "pork_us": 50.0,
    "broiler_us": 50.0,

    # Sugar (1000 short tons)
    "sugar_us": 100.0,
    "sugar_mexico": 50.0
}

# Value ranges by commodity (min, max)
VALUE_RANGES = {
    "wheat_us": {
        "production": (1000, 3000),
        "ending_stocks": (300, 1500),
        "exports": (500, 1500)
    },
    "corn_us": {
        "production": (10000, 18000),
        "ending_stocks": (500, 3000),
        "exports": (1500, 3000),
        "ethanol": (4000, 6000)
    },
    "soybeans_us": {
        "production": (3500, 5000),
        "crushings": (2000, 2500),
        "exports": (1500, 2500),
        "ending_stocks": (100, 600)
    },
    "cotton_us": {
        "production": (10, 20),
        "mill_use": (2, 4),
        "exports": (10, 18),
        "ending_stocks": (2, 8)
    }
}


def validate_balance(
    data: Dict,
    commodity: str = None,
    tolerance: float = None
) -> Tuple[bool, float]:
    """
    Validate supply-demand balance formula.

    Balance: Ending Stocks = Beginning Stocks + Production + Imports - Total Use - Exports

    Args:
        data: Row data dictionary
        commodity: Commodity ID for tolerance lookup
        tolerance: Override tolerance value

    Returns:
        tuple: (is_valid, difference)
    """
    # Get tolerance
    if tolerance is None:
        tolerance = BALANCE_TOLERANCES.get(commodity, 5.0)

    # Get values
    beginning = data.get('beginning_stocks', 0) or 0
    production = data.get('production', 0) or 0
    imports_ = data.get('imports', 0) or 0
    exports = data.get('exports', 0) or 0
    ending = data.get('ending_stocks', 0) or 0

    # Total use might be explicit or need calculation
    total_use = data.get('total_use') or data.get('use_total')
    if total_use is None:
        domestic = data.get('domestic_total') or data.get('domestic_use', 0) or 0
        total_use = domestic + exports

    # Calculate expected ending stocks
    supply = beginning + production + imports_
    expected_ending = supply - total_use

    # Check balance
    diff = abs(ending - expected_ending)
    is_valid = diff <= tolerance

    return is_valid, diff


def validate_range(
    data: Dict,
    commodity: str
) -> List[Dict]:
    """
    Validate values are within historical ranges.

    Args:
        data: Row data dictionary
        commodity: Commodity ID

    Returns:
        list: List of range violations
    """
    issues = []
    ranges = VALUE_RANGES.get(commodity, {})

    for field, (min_val, max_val) in ranges.items():
        value = data.get(field)
        if value is None:
            continue

        if value < min_val:
            issues.append({
                "field": field,
                "value": value,
                "expected_range": (min_val, max_val),
                "issue": "below_minimum",
                "severity": "warning"
            })
        elif value > max_val:
            issues.append({
                "field": field,
                "value": value,
                "expected_range": (min_val, max_val),
                "issue": "above_maximum",
                "severity": "warning"
            })

    return issues


def validate_schema(
    data: Dict,
    commodity: str
) -> Tuple[bool, List[str]]:
    """
    Validate required fields are present.

    Args:
        data: Row data dictionary
        commodity: Commodity ID

    Returns:
        tuple: (is_valid, list of missing fields)
    """
    # Common required fields
    required = [
        'beginning_stocks',
        'production',
        'imports',
        'exports',
        'ending_stocks'
    ]

    # Commodity-specific required fields
    if 'soy' in commodity and '_us' in commodity:
        if 'oil' not in commodity and 'meal' not in commodity:
            required.append('crushings')

    if 'cotton' in commodity:
        required.append('mill_use')

    missing = [f for f in required if f not in data or data[f] is None]

    return len(missing) == 0, missing


def check_duplicates(
    df,
    key_columns: List[str]
) -> List[Dict]:
    """
    Check for duplicate rows based on key columns.

    Args:
        df: pandas DataFrame
        key_columns: Columns that form the unique key

    Returns:
        list: List of duplicate entries
    """
    duplicates = []

    # Find duplicates
    dup_mask = df.duplicated(subset=key_columns, keep=False)
    dup_rows = df[dup_mask]

    if len(dup_rows) > 0:
        for _, group in dup_rows.groupby(key_columns):
            if len(group) > 1:
                duplicates.append({
                    "key": {col: group.iloc[0][col] for col in key_columns},
                    "count": len(group),
                    "indices": group.index.tolist()
                })

    return duplicates


def validate_cross_table(
    us_data: Dict,
    world_data: Dict,
    commodity: str
) -> List[Dict]:
    """
    Validate consistency between US and World tables.

    Args:
        us_data: US table data
        world_data: World table data
        commodity: Commodity name

    Returns:
        list: List of inconsistencies
    """
    issues = []

    # US exports should be reflected in World data
    us_exports = us_data.get('exports')
    if us_exports and 'united_states' in world_data:
        world_us_exports = world_data['united_states'].get('exports')
        if world_us_exports:
            # Convert units if needed
            diff = abs(us_exports - world_us_exports)
            if diff > 1.0:  # Tolerance
                issues.append({
                    "type": "export_mismatch",
                    "us_value": us_exports,
                    "world_value": world_us_exports,
                    "difference": diff
                })

    return issues


def validate_crush_relationship(
    soybeans: Dict,
    oil: Dict,
    meal: Dict
) -> List[Dict]:
    """
    Validate crush relationship: soybean crush ≈ oil + meal production.

    Typical ratios:
    - 1 bushel (60 lbs) → 11 lbs oil (18.3%) + 48 lbs meal (80%)

    Args:
        soybeans: Soybean data
        oil: Soybean oil data
        meal: Soybean meal data

    Returns:
        list: List of inconsistencies
    """
    issues = []

    crush = soybeans.get('crushings')
    oil_prod = oil.get('production')
    meal_prod = meal.get('production')

    if crush and oil_prod:
        # Expected oil: crush (million bu) * 60 lbs/bu * 0.183 = million pounds
        expected_oil = crush * 60 * 0.183
        oil_diff_pct = abs(oil_prod - expected_oil) / expected_oil * 100

        if oil_diff_pct > 10:  # 10% tolerance
            issues.append({
                "type": "oil_production_mismatch",
                "actual": oil_prod,
                "expected": expected_oil,
                "difference_pct": oil_diff_pct
            })

    if crush and meal_prod:
        # Expected meal: crush (million bu) * 60 lbs/bu * 0.80 / 2000 = thousand short tons
        expected_meal = crush * 60 * 0.80 / 2000
        meal_diff_pct = abs(meal_prod - expected_meal) / expected_meal * 100

        if meal_diff_pct > 10:
            issues.append({
                "type": "meal_production_mismatch",
                "actual": meal_prod,
                "expected": expected_meal,
                "difference_pct": meal_diff_pct
            })

    return issues


def run_all_validations(
    data: Dict[str, Any],
    commodity: str
) -> Dict:
    """
    Run all validations on parsed data.

    Args:
        data: Parsed table data
        commodity: Commodity ID

    Returns:
        dict: Validation results
    """
    results = {
        "commodity": commodity,
        "valid": True,
        "checks": []
    }

    # Balance check
    balance_ok, balance_diff = validate_balance(data, commodity)
    results["checks"].append({
        "name": "balance_formula",
        "passed": balance_ok,
        "details": {"difference": balance_diff}
    })
    if not balance_ok:
        results["valid"] = False

    # Range check
    range_issues = validate_range(data, commodity)
    results["checks"].append({
        "name": "value_range",
        "passed": len(range_issues) == 0,
        "details": {"issues": range_issues}
    })

    # Schema check
    schema_ok, missing = validate_schema(data, commodity)
    results["checks"].append({
        "name": "schema",
        "passed": schema_ok,
        "details": {"missing_fields": missing}
    })
    if not schema_ok:
        results["valid"] = False

    return results


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate WASDE data")
    parser.add_argument("--input", type=str, required=True, help="Input JSON file")
    parser.add_argument("--commodity", type=str, required=True, help="Commodity ID")
    parser.add_argument("--output", type=str, help="Output JSON file")

    args = parser.parse_args()

    with open(args.input, 'r') as f:
        data = json.load(f)

    results = run_all_validations(data, args.commodity)

    output = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Results written to: {args.output}")
    else:
        print(output)
