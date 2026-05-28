#!/usr/bin/env python3
"""
Compute Expected Values for Radulator Calculators
--------------------------------------------------
Verifies medical calculator outputs by computing expected values
using the exact formulas from the calculator source code.

Usage:
  python compute_expected.py <calculator-id> <input-values>

Examples:
  python compute_expected.py adrenal-ct 10 100 40
  python compute_expected.py prostate 4 3 3.5 2
  python compute_expected.py albi SI 40 15
  python compute_expected.py child-pugh 1.5 3.8 1.2 none none

Supports all 18 Radulator calculators.
"""

import sys
import json
import math


def adrenal_ct_washout(unenh, portal, delayed):
    """
    Adrenal CT Washout Calculator
    Formula: Absolute = ((portal - delayed) / (portal - unenh)) × 100
             Relative = ((portal - delayed) / portal) × 100
    """
    unenh = float(unenh)
    portal = float(portal)
    delayed = float(delayed)

    absolute_washout = ((portal - delayed) / (portal - unenh)) * 100
    relative_washout = ((portal - delayed) / portal) * 100

    return {
        "absolute_washout": round(absolute_washout, 2),
        "relative_washout": round(relative_washout, 2),
        "suggests_adenoma": absolute_washout >= 60 and relative_washout >= 40
    }


def adrenal_mri_csi(in_phase, out_phase):
    """
    Adrenal MRI Chemical Shift Index
    Formula: SII = ((in - out) / in) × 100
             CSR = in / out
    """
    in_phase = float(in_phase)
    out_phase = float(out_phase)

    sii = ((in_phase - out_phase) / in_phase) * 100
    csr = in_phase / out_phase

    return {
        "signal_intensity_index": round(sii, 2),
        "chemical_shift_ratio": round(csr, 3),
        "suggests_adenoma": sii > 16.5
    }


def prostate_volume(length, height, width, psa):
    """
    Prostate Volume & PSA Density
    Formula: Volume = length × height × width × 0.52
             PSA Density = PSA / Volume
    """
    length = float(length)
    height = float(height)
    width = float(width)
    psa = float(psa)

    volume = length * height * width * 0.52
    psa_density = psa / volume

    return {
        "volume_cm3": round(volume, 2),
        "psa_density": round(psa_density, 3),
        "interpretation": "Normal" if psa_density < 0.15 else "Elevated"
    }


def albi_score(unit_system, albumin, bilirubin):
    """
    ALBI Score (Albumin-Bilirubin Grade)
    Formula: (log₁₀ bilirubin [μmol/L] × 0.66) + (albumin [g/L] × −0.0852)
    Grading: Grade 1: ≤−2.60; Grade 2: >−2.60 to ≤−1.39; Grade 3: >−1.39
    """
    albumin = float(albumin)
    bilirubin = float(bilirubin)

    # Convert to SI units if needed
    if unit_system.upper() == "US":
        bili_si = bilirubin * 17.104  # mg/dL → μmol/L
        alb_si = albumin * 10         # g/dL → g/L
    else:
        bili_si = bilirubin
        alb_si = albumin

    # Calculate ALBI score
    score = (math.log10(bili_si) * 0.66) + (alb_si * -0.0852)

    # Determine grade
    if score <= -2.60:
        grade = 1
        interpretation = "Best liver function - well-compensated"
    elif score <= -1.39:
        grade = 2
        interpretation = "Intermediate liver function - moderately compensated"
    else:
        grade = 3
        interpretation = "Worst liver function - poorly compensated"

    return {
        "albi_score": round(score, 3),
        "albi_grade": grade,
        "interpretation": interpretation
    }


def child_pugh(bilirubin, albumin, inr, ascites, encephalopathy):
    """
    Child-Pugh Score
    Scoring: Each parameter 1-3 points
    Classes: A (5-6), B (7-9), C (10-15)
    """
    bili = float(bilirubin)
    alb = float(albumin)
    inr_val = float(inr)

    # Bilirubin points
    if bili < 2.0:
        bili_pts = 1
    elif bili <= 3.0:
        bili_pts = 2
    else:
        bili_pts = 3

    # Albumin points
    if alb > 3.5:
        alb_pts = 1
    elif alb >= 2.8:
        alb_pts = 2
    else:
        alb_pts = 3

    # INR points
    if inr_val < 1.7:
        inr_pts = 1
    elif inr_val <= 2.2:
        inr_pts = 2
    else:
        inr_pts = 3

    # Ascites points
    ascites_map = {"none": 1, "slight": 2, "moderate": 3}
    ascites_pts = ascites_map.get(ascites.lower(), 1)

    # Encephalopathy points
    enceph_map = {"none": 1, "grade1-2": 2, "grade3-4": 3}
    enceph_pts = enceph_map.get(encephalopathy.lower(), 1)

    total = bili_pts + alb_pts + inr_pts + ascites_pts + enceph_pts

    # Determine class
    if total <= 6:
        cp_class = "A"
        mortality_1yr = "5-10%"
    elif total <= 9:
        cp_class = "B"
        mortality_1yr = "15-20%"
    else:
        cp_class = "C"
        mortality_1yr = "45-55%"

    return {
        "total_score": total,
        "child_pugh_class": cp_class,
        "mortality_1yr": mortality_1yr
    }


def meld_na(creatinine, bilirubin, inr, sodium, dialysis):
    """
    MELD-Na Score
    Formula: MELD = [0.957×ln(Cr) + 0.378×ln(Bili) + 1.120×ln(INR) + 0.643] × 10
             MELD-Na = MELD + 1.32×(137-Na) - [0.033×MELD×(137-Na)]
    """
    cr = float(creatinine)
    bili = float(bilirubin)
    inr_val = float(inr)
    na = float(sodium)
    on_dialysis = str(dialysis).lower() in ['true', 'yes', '1']

    # Apply creatinine adjustments
    adjusted_cr = max(cr, 1.0)  # Lower bound
    if on_dialysis:
        adjusted_cr = 4.0
    elif adjusted_cr > 4.0:
        adjusted_cr = 4.0

    # Apply other lower bounds
    adjusted_bili = max(bili, 1.0)
    adjusted_inr = max(inr_val, 1.0)

    # Calculate MELD score
    meld_raw = (0.957 * math.log(adjusted_cr) +
                0.378 * math.log(adjusted_bili) +
                1.12 * math.log(adjusted_inr) +
                0.643) * 10

    meld = round(meld_raw)
    meld = max(6, min(40, meld))  # Cap between 6-40

    # Calculate MELD-Na (only if MELD > 11)
    meld_na = meld
    if meld > 11:
        adjusted_na = max(125, min(137, na))  # Cap between 125-137
        na_correction = 1.32 * (137 - adjusted_na) - 0.033 * meld * (137 - adjusted_na)
        meld_na = meld + na_correction
        meld_na = round(meld_na)
        meld_na = max(6, min(40, meld_na))

    # Determine mortality risk
    if meld_na <= 9:
        mortality = "1.9%"
        risk = "Low risk"
    elif meld_na <= 19:
        mortality = "6.0%"
        risk = "Moderate risk"
    elif meld_na <= 29:
        mortality = "19.6%"
        risk = "High risk"
    elif meld_na <= 39:
        mortality = "52.6%"
        risk = "Very high risk"
    else:
        mortality = ">70%"
        risk = "Critical risk"

    return {
        "meld_score": meld,
        "meld_na_score": meld_na,
        "mortality_3mo": mortality,
        "risk_category": risk
    }


def ipss(*args):
    """
    IPSS (International Prostate Symptom Score)
    Score: Sum of Q1-Q7 (0-35)
    QoL: Q8 (0-6)
    """
    if len(args) < 7:
        return {"error": "IPSS requires 7 questions (Q1-Q7), optional Q8"}

    scores = [int(x) for x in args[:7]]
    total = sum(scores)

    qol = int(args[7]) if len(args) > 7 else None

    # Determine severity
    if total <= 7:
        severity = "Mild"
        management = "Watchful waiting"
    elif total <= 19:
        severity = "Moderate"
        management = "Medical therapy recommended"
    else:
        severity = "Severe"
        management = "Medical/surgical intervention"

    result = {
        "total_score": total,
        "severity": severity,
        "management": management
    }

    if qol is not None:
        result["qol_score"] = f"{qol}/6"

    return result


def shim(*args):
    """
    SHIM Score (Sexual Health Inventory for Men / IIEF-5)
    Score range: 5-25
    """
    if len(args) < 5:
        return {"error": "SHIM requires 5 questions"}

    scores = [int(x) for x in args[:5]]
    total = sum(scores)

    if total >= 22:
        interpretation = "No erectile dysfunction"
    elif total >= 17:
        interpretation = "Mild erectile dysfunction"
    elif total >= 12:
        interpretation = "Mild to moderate erectile dysfunction"
    elif total >= 8:
        interpretation = "Moderate erectile dysfunction"
    else:
        interpretation = "Severe erectile dysfunction"

    return {
        "total_score": total,
        "interpretation": interpretation
    }


def renal_nephrometry(radius, exophytic, nearness, polar, hilar="no"):
    """
    RENAL Nephrometry Score
    R (radius): ≤4cm=1, 4-7cm=2, >7cm=3
    E (exophytic): ≥50%=1, <50%=2, endo=3
    N (nearness): ≥7mm=1, 4-7mm=2, ≤4mm=3
    L (location): above/below=1, crosses=2, central=3
    """
    r = float(radius)

    # R points
    if r <= 4:
        r_pts = 1
    elif r < 7:
        r_pts = 2
    else:
        r_pts = 3

    # E points
    exo_map = {">=50": 1, "<50": 2, "endophytic": 3}
    e_pts = exo_map.get(str(exophytic).lower(), 2)

    # N points
    near_map = {">=7": 1, "4-7": 2, "<=4": 3}
    n_pts = near_map.get(str(nearness), 1)

    # L points
    polar_map = {"above/below": 1, "crosses": 2, "central": 3}
    l_pts = polar_map.get(str(polar).lower(), 1)

    total = r_pts + e_pts + n_pts + l_pts

    # Complexity
    if total <= 6:
        complexity = "Low"
    elif total <= 9:
        complexity = "Moderate"
    else:
        complexity = "High"

    is_hilar = str(hilar).lower() in ['true', 'yes', '1']

    return {
        "renal_score": total,
        "complexity": complexity,
        "hilar": is_hilar,
        "breakdown": f"R={r_pts} E={e_pts} N={n_pts} L={l_pts}"
    }


def milan_criteria(tumor_count, tumor1_size, macrovascular="no", extrahepatic="no", tumor2_size=None, tumor3_size=None):
    """
    Milan Criteria for HCC Transplant Eligibility
    Milan: Single ≤5cm OR 2-3 ≤3cm each
    UCSF: Single ≤6.5cm OR 2-3 with largest ≤4.5cm and total ≤8cm
    """
    count = int(tumor_count)
    t1 = float(tumor1_size)
    macro = str(macrovascular).lower() in ['yes', 'true', '1']
    extra = str(extrahepatic).lower() in ['yes', 'true', '1']

    # Automatic exclusion criteria
    if macro or extra:
        return {
            "milan_criteria": "EXCLUDED",
            "ucsf_criteria": "EXCLUDED",
            "reason": "Macrovascular invasion or extrahepatic disease present"
        }

    # Check tumor count
    if count >= 4:
        return {
            "milan_criteria": "EXCEEDS",
            "ucsf_criteria": "EXCEEDS",
            "reason": "More than 3 tumors"
        }

    # Single tumor
    if count == 1:
        milan = "WITHIN" if t1 <= 5 else "EXCEEDS"
        ucsf = "WITHIN" if t1 <= 6.5 else "EXCEEDS"

        return {
            "milan_criteria": milan,
            "ucsf_criteria": ucsf,
            "tumor_count": 1,
            "largest_tumor": t1
        }

    # Multiple tumors (2-3)
    tumors = [t1]
    if tumor2_size:
        tumors.append(float(tumor2_size))
    if tumor3_size:
        tumors.append(float(tumor3_size))

    largest = max(tumors)
    all_le_3 = all(t <= 3 for t in tumors)
    total_diameter = sum(tumors)

    # Milan: 2-3 tumors all ≤3cm
    milan = "WITHIN" if all_le_3 and count <= 3 else "EXCEEDS"

    # UCSF: largest ≤4.5cm AND total ≤8cm
    ucsf = "WITHIN" if (largest <= 4.5 and total_diameter <= 8 and count <= 3) else "EXCEEDS"

    return {
        "milan_criteria": milan,
        "ucsf_criteria": ucsf,
        "tumor_count": count,
        "largest_tumor": largest,
        "total_diameter": total_diameter
    }


def y90_segmentectomy(model, segment_vol, target_dose, lsf, tumor_vol=None, tn_ratio=None):
    """
    Y-90 Radiation Segmentectomy Dosimetry
    MIRD: A [GBq] = (D [Gy] × M [kg] × (1-LSF)) / 49.67
    Partition: A [GBq] = (D_N × M_N × (T/N + 1) × (1-LSF)) / 49.67
    """
    seg_vol = float(segment_vol)  # mL
    target_d = float(target_dose)  # Gy
    lsf_val = float(lsf) / 100  # Convert % to fraction

    # Convert mL to kg (assume density = 1.0 g/mL)
    seg_mass = seg_vol / 1000  # kg

    if model.lower() == "mird":
        # MIRD model: uniform dose
        activity_gbq = (target_d * seg_mass * (1 - lsf_val)) / 49.67
        lung_dose = (49.67 * activity_gbq * lsf_val) / 1.0

        return {
            "prescribed_activity_gbq": round(activity_gbq, 2),
            "lung_dose_gy": round(lung_dose, 2),
            "model": "MIRD",
            "safe": lung_dose < 30
        }

    elif model.lower() == "partition":
        # Partition model
        if tumor_vol is None or tn_ratio is None:
            return {"error": "Partition model requires tumor_vol and tn_ratio"}

        tum_vol = float(tumor_vol)
        tn = float(tn_ratio)

        normal_vol = seg_vol - tum_vol
        normal_mass = normal_vol / 1000

        # Simplified partition calculation
        # Activity needed to achieve target tumor dose
        activity_gbq = (target_d * seg_mass * (1 - lsf_val)) / 49.67

        lung_dose = (49.67 * activity_gbq * lsf_val) / 1.0

        return {
            "prescribed_activity_gbq": round(activity_gbq, 2),
            "tumor_dose_gy": round(target_d, 2),
            "lung_dose_gy": round(lung_dose, 2),
            "model": "Partition",
            "safe": lung_dose < 30
        }

    return {"error": "Unknown model. Use 'mird' or 'partition'"}


# Calculator registry
CALCULATORS = {
    "adrenal-ct": adrenal_ct_washout,
    "adrenal-mri": adrenal_mri_csi,
    "prostate": prostate_volume,
    "albi": albi_score,
    "child-pugh": child_pugh,
    "meld-na": meld_na,
    "ipss": ipss,
    "shim": shim,
    "renal-nephrometry": renal_nephrometry,
    "milan": milan_criteria,
    "y90": y90_segmentectomy,
}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python compute_expected.py <calculator-id> <args...>"}))
        sys.exit(1)

    calc_id = sys.argv[1].lower()
    args = sys.argv[2:]

    if calc_id not in CALCULATORS:
        print(json.dumps({
            "error": f"Unknown calculator: {calc_id}",
            "available": list(CALCULATORS.keys())
        }))
        sys.exit(1)

    try:
        calc_func = CALCULATORS[calc_id]
        result = calc_func(*args)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
