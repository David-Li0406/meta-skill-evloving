#!/usr/bin/env python3
"""
Radulator Calculator Verification Script

This script computes expected values for all six Radulator calculators
to verify that the web app produces correct results.
"""

import json
import sys
from typing import Dict, Any


def adrenal_ct_washout(unenh: float, portal: float, delayed: float) -> Dict[str, Any]:
    """
    Calculate adrenal CT washout values.
    
    Args:
        unenh: Unenhanced HU value
        portal: Portal venous phase HU value
        delayed: Delayed phase (15 min) HU value
    
    Returns:
        Dictionary with absolute_washout, relative_washout, and interpretation
    """
    absolute_washout = ((portal - delayed) / (portal - unenh)) * 100
    relative_washout = ((portal - delayed) / portal) * 100
    
    # Interpretation thresholds: Absolute > 60%, Relative > 40%
    if absolute_washout > 60 and relative_washout > 40:
        interpretation = "Suggests benign adenoma"
    else:
        interpretation = "Does not meet criteria for adenoma"
    
    return {
        "absolute_washout": round(absolute_washout, 1),
        "relative_washout": round(relative_washout, 1),
        "interpretation": interpretation
    }


def adrenal_mri_chemical_shift(in_phase: float, out_phase: float) -> Dict[str, Any]:
    """
    Calculate adrenal MRI chemical shift values.
    
    Args:
        in_phase: In-phase signal intensity
        out_phase: Out-of-phase signal intensity
    
    Returns:
        Dictionary with SII, CSR, and interpretation
    """
    sii = ((in_phase - out_phase) / in_phase) * 100
    csr = in_phase / out_phase
    
    # Interpretation threshold: SII > 16.5%
    if sii > 16.5:
        interpretation = "Consistent with lipid-rich adenoma"
    else:
        interpretation = "Does not meet criteria for lipid-rich adenoma"
    
    return {
        "sii": round(sii, 2),
        "csr": round(csr, 3),
        "interpretation": interpretation
    }


def prostate_volume_psa_density(length: float, height: float, width: float, psa: float) -> Dict[str, Any]:
    """
    Calculate prostate volume and PSA density.
    
    Args:
        length: Prostate length in cm
        height: Prostate height in cm
        width: Prostate width in cm
        psa: PSA level in ng/mL
    
    Returns:
        Dictionary with volume, psa_density, and interpretation
    """
    volume = length * height * width * 0.52
    psa_density = psa / volume
    
    # Interpretation threshold: PSA density < 0.15 ng/mL²
    if psa_density < 0.15:
        interpretation = "Normal PSA density"
    else:
        interpretation = "Elevated PSA density"
    
    return {
        "volume": round(volume, 2),
        "psa_density": round(psa_density, 3),
        "interpretation": interpretation
    }


def renal_cyst_bosniak(homogeneous: bool, thin_wall: bool, no_septa_calc_enhancement: bool,
                       thickened_walls: bool = False, measurable_enhancement: bool = False) -> Dict[str, Any]:
    """
    Classify renal cyst using Bosniak classification.
    
    Args:
        homogeneous: Whether cyst has homogeneous water attenuation
        thin_wall: Whether wall is thin and imperceptible
        no_septa_calc_enhancement: No septa, calcifications, or enhancement
        thickened_walls: Thickened irregular walls or septa present
        measurable_enhancement: Measurable enhancement present
    
    Returns:
        Dictionary with classification and interpretation
    """
    if homogeneous and thin_wall and no_septa_calc_enhancement:
        classification = "Bosniak I"
        interpretation = "Benign simple cyst, no follow-up needed"
    elif thickened_walls and measurable_enhancement:
        classification = "Bosniak III"
        interpretation = "Indeterminate cystic mass, surgical exploration recommended"
    else:
        classification = "Bosniak II or IV"
        interpretation = "Further classification needed"
    
    return {
        "classification": classification,
        "interpretation": interpretation
    }


def spleen_size(length: float, age: int, sex: str) -> Dict[str, Any]:
    """
    Assess spleen size against upper limit of normal.
    
    Args:
        length: Craniocaudal length in cm
        age: Patient age in years
        sex: Patient sex ('Male' or 'Female')
    
    Returns:
        Dictionary with ULN, assessment, and interpretation
    """
    # Simplified ULN values (actual values vary by study)
    # These are approximate values based on common references
    if sex.lower() == 'male':
        if age < 40:
            uln = 13.0
        else:
            uln = 12.5
    else:  # female
        if age < 40:
            uln = 12.0
        else:
            uln = 11.5
    
    if length <= uln:
        assessment = "Normal"
        interpretation = "Spleen size within normal limits"
    else:
        assessment = "Splenomegaly"
        interpretation = f"Splenomegaly detected (exceeds ULN by {round(length - uln, 1)} cm)"
    
    return {
        "uln": uln,
        "assessment": assessment,
        "interpretation": interpretation
    }


def hip_dysplasia_indices(alpha_angle: float, beta_angle: float, femoral_coverage: float) -> Dict[str, Any]:
    """
    Classify hip dysplasia using Graf classification.
    
    Args:
        alpha_angle: Alpha angle in degrees
        beta_angle: Beta angle in degrees
        femoral_coverage: Femoral head coverage percentage
    
    Returns:
        Dictionary with classification and interpretation
    """
    if alpha_angle > 60 and beta_angle < 55:
        classification = "Type Ia (Normal)"
        interpretation = "Normal hip development"
    elif alpha_angle >= 50 and alpha_angle <= 60 and beta_angle < 77:
        classification = "Type II (Physiologic immaturity)"
        interpretation = "Physiologic immaturity, follow-up recommended"
    elif alpha_angle >= 43 and alpha_angle < 50 and beta_angle > 77:
        classification = "Type III (Dysplastic)"
        interpretation = "Hip dysplasia, treatment required"
    else:
        classification = "Type IV (Decentered/Dislocated)"
        interpretation = "Severe dysplasia or dislocation, immediate treatment required"
    
    return {
        "classification": classification,
        "alpha_angle": alpha_angle,
        "beta_angle": beta_angle,
        "femoral_coverage": femoral_coverage,
        "interpretation": interpretation
    }


def run_test_case(calculator: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run a test case for a specific calculator.
    
    Args:
        calculator: Name of the calculator
        test_case: Dictionary containing test inputs
    
    Returns:
        Dictionary with expected outputs
    """
    if calculator == "adrenal_ct_washout":
        return adrenal_ct_washout(
            test_case["unenh"],
            test_case["portal"],
            test_case["delayed"]
        )
    elif calculator == "adrenal_mri_chemical_shift":
        return adrenal_mri_chemical_shift(
            test_case["in_phase"],
            test_case["out_phase"]
        )
    elif calculator == "prostate_volume":
        return prostate_volume_psa_density(
            test_case["length"],
            test_case["height"],
            test_case["width"],
            test_case["psa"]
        )
    elif calculator == "renal_cyst":
        return renal_cyst_bosniak(
            test_case.get("homogeneous", False),
            test_case.get("thin_wall", False),
            test_case.get("no_septa_calc_enhancement", False),
            test_case.get("thickened_walls", False),
            test_case.get("measurable_enhancement", False)
        )
    elif calculator == "spleen_size":
        return spleen_size(
            test_case["length"],
            test_case["age"],
            test_case["sex"]
        )
    elif calculator == "hip_dysplasia":
        return hip_dysplasia_indices(
            test_case["alpha_angle"],
            test_case["beta_angle"],
            test_case["femoral_coverage"]
        )
    else:
        raise ValueError(f"Unknown calculator: {calculator}")


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python verify_calculators.py <calculator_name> [test_case_json]")
        print("\nAvailable calculators:")
        print("  - adrenal_ct_washout")
        print("  - adrenal_mri_chemical_shift")
        print("  - prostate_volume")
        print("  - renal_cyst")
        print("  - spleen_size")
        print("  - hip_dysplasia")
        sys.exit(1)
    
    calculator = sys.argv[1]
    
    if len(sys.argv) > 2:
        # Test case provided as JSON
        test_case = json.loads(sys.argv[2])
        result = run_test_case(calculator, test_case)
        print(json.dumps(result, indent=2))
    else:
        # Run default test cases
        print(f"Running default test cases for {calculator}...")
        # Add default test cases here if needed


if __name__ == "__main__":
    main()
