#!/usr/bin/env python3
"""
Use Case Points (UCP) Calculator

This script calculates UCP metrics from provided counts and complexity factors.

Usage:
    python calculate_ucp.py --uaw 24 --uucw 562.4 --tcf 1.40 --ecf 0.86
    python calculate_ucp.py --config ucp_input.json
"""

import argparse
import json
from typing import Dict, Optional


def calculate_tcf(t_factors: Dict[str, float]) -> float:
    """
    Calculate Technical Complexity Factor (TCF).

    Args:
        t_factors: Dictionary of {"T1": rating, "T2": rating, ...}

    Returns:
        TCF value (0.6 to 1.4 capped)
    """
    # Standard weights for T1-T13
    weights = {
        "T1": 2.0,   # Distributed System
        "T2": 1.0,   # Response Time/Performance
        "T3": 1.0,   # End-user Efficiency
        "T4": 1.0,   # Complex Internal Processing
        "T5": 1.0,   # Code Reusability
        "T6": 0.5,   # Easy to Install
        "T7": 0.5,   # Easy to Use
        "T8": 2.0,   # Portability
        "T9": 1.0,   # Easy to Change
        "T10": 1.0,  # Concurrent Users
        "T11": 1.0,  # Security Features
        "T12": 1.0,  # Direct Access for 3rd Parties
        "T13": 1.0,  # Special User Training
        # AI/ML-specific (T14-T20)
        "T14": 2.0,  # ML Model Complexity
        "T15": 2.0,  # Data Volume/Velocity
        "T16": 1.5,  # Data Quality Challenges
        "T17": 1.0,  # Model Explainability
        "T18": 1.5,  # Real-time Inference
        "T19": 1.0,  # MLOps Maturity
        "T20": 1.5,  # AI Bias & Fairness
    }

    t_factor_sum = 0.0
    for factor_id, rating in t_factors.items():
        weight = weights.get(factor_id, 1.0)
        t_factor_sum += rating * weight

    tcf = 0.6 + (0.01 * t_factor_sum)

    # Cap at 1.4 per UCP standard
    tcf = min(tcf, 1.4)

    return round(tcf, 2)


def calculate_ecf(e_factors: Dict[str, float]) -> float:
    """
    Calculate Environmental Complexity Factor (ECF).

    Args:
        e_factors: Dictionary of {"E1": rating, "E2": rating, ...}

    Returns:
        ECF value (0.4 to 1.4 range)
    """
    # Weights for E1-E8
    # Note: E7-E8 are inverse (higher = worse)
    weights = {
        "E1": 1.5,   # Familiar with Development Process
        "E2": 0.5,   # Application Experience
        "E3": 1.0,   # Object-Oriented Experience
        "E4": 0.5,   # Lead Analyst Capability
        "E5": 1.0,   # Motivation
        "E6": 2.0,   # Stable Requirements
        "E7": -1.0,  # Part-Time Staff (inverse)
        "E8": -1.0,  # Difficult Programming Language (inverse)
    }

    e_factor_sum = 0.0
    for factor_id, rating in e_factors.items():
        weight = weights.get(factor_id, 0.0)
        e_factor_sum += rating * weight

    ecf = 1.4 + (-0.03 * e_factor_sum)

    return round(ecf, 2)


def calculate_ucp(
    uaw: float,
    uucw: float,
    tcf: Optional[float] = None,
    ecf: Optional[float] = None,
    t_factors: Optional[Dict[str, float]] = None,
    e_factors: Optional[Dict[str, float]] = None,
    framework_leverage: float = 1.0
) -> Dict[str, float]:
    """
    Calculate UCP from provided metrics.

    Args:
        uaw: Unadjusted Actor Weight
        uucw: Unadjusted Use Case Weight
        tcf: Technical Complexity Factor (or provide t_factors)
        ecf: Environmental Complexity Factor (or provide e_factors)
        t_factors: Technical factor ratings (if tcf not provided)
        e_factors: Environmental factor ratings (if ecf not provided)
        framework_leverage: Framework leverage factor (default 1.0)

    Returns:
        Dictionary with UCP calculations
    """
    # Calculate TCF if not provided
    if tcf is None and t_factors:
        tcf = calculate_tcf(t_factors)
    elif tcf is None:
        tcf = 1.0  # Neutral default

    # Calculate ECF if not provided
    if ecf is None and e_factors:
        ecf = calculate_ecf(e_factors)
    elif ecf is None:
        ecf = 1.0  # Neutral default

    uucp = uaw + uucw
    adjusted_ucp = uucp * tcf * ecf
    realistic_ucp = adjusted_ucp * framework_leverage

    return {
        "uaw": round(uaw, 2),
        "uucw": round(uucw, 2),
        "uucp": round(uucp, 2),
        "tcf": round(tcf, 2),
        "ecf": round(ecf, 2),
        "adjusted_ucp": round(adjusted_ucp, 2),
        "framework_leverage": round(framework_leverage, 2),
        "realistic_ucp": round(realistic_ucp, 2)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Calculate Use Case Points (UCP)"
    )
    parser.add_argument("--uaw", type=float, help="Unadjusted Actor Weight")
    parser.add_argument("--uucw", type=float, help="Unadjusted Use Case Weight")
    parser.add_argument("--tcf", type=float, help="Technical Complexity Factor")
    parser.add_argument("--ecf", type=float, help="Environmental Complexity Factor")
    parser.add_argument(
        "--framework-leverage",
        type=float,
        default=1.0,
        help="Framework leverage factor (0.6-1.0)"
    )
    parser.add_argument(
        "--config",
        "-c",
        help="JSON config file with all inputs"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed breakdown"
    )

    args = parser.parse_args()

    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
        result = calculate_ucp(**config)
    elif args.uaw is not None and args.uucw is not None:
        result = calculate_ucp(
            uaw=args.uaw,
            uucw=args.uucw,
            tcf=args.tcf,
            ecf=args.ecf,
            framework_leverage=args.framework_leverage
        )
    else:
        parser.print_help()
        return

    if args.verbose:
        print("=" * 50)
        print("USE CASE POINTS CALCULATION")
        print("=" * 50)
        print(f"Unadjusted Actor Weight (UAW):     {result['uaw']}")
        print(f"Unadjusted Use Case Weight (UUCW): {result['uucw']}")
        print(f"Unadjusted Use Case Points (UUCP): {result['uucp']}")
        print("-" * 50)
        print(f"Technical Complexity Factor (TCF): {result['tcf']}")
        print(f"Environmental Factor (ECF):        {result['ecf']}")
        print("-" * 50)
        print(f"Adjusted UCP:                      {result['adjusted_ucp']}")
        print(f"Framework Leverage Factor:         {result['framework_leverage']}")
        print(f"Realistic UCP:                     {result['realistic_ucp']}")
        print("=" * 50)
    else:
        print(f"Realistic UCP: {result['realistic_ucp']}")

    return result


if __name__ == "__main__":
    main()
