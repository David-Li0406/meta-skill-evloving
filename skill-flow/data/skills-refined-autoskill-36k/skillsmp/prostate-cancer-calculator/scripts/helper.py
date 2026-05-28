#!/usr/bin/env python3
"""
Prostate Cancer Clinical Calculator
====================================
Risk stratification, LNI prediction, and salvage RT decision support.

Usage:
    from helper import *
    
    # Or run directly for quick calculations:
    python helper.py --nccn --psa 12 --gg 3 --stage T2b --cores 4/12
"""

import math
import argparse
from typing import List, Tuple, Optional, Dict, Any
# =============================================================================
# NCCN RISK CLASSIFICATION
# =============================================================================

def calculate_nccn_risk(
    psa: float,
    grade_group: int,
    t_stage: str,
    positive_cores: int,
    total_cores: int,
    max_core_involvement: float = 100,
    psa_density: float = 0.2,
    primary_gleason: Optional[int] = None,
    n_stage: str = "N0",
    m_stage: str = "M0"
) -> str:
    """
    Calculate NCCN risk group (8-tier classification).
    
    Args:
        psa: PSA value in ng/mL
        grade_group: ISUP Grade Group (1-5)
        t_stage: Clinical T-stage (T1a, T1b, T1c, T2a, T2b, T2c, T3a, T3b, T4)
        positive_cores: Number of positive biopsy cores
        total_cores: Total number of biopsy cores
        max_core_involvement: Maximum % cancer in any single core
        psa_density: PSA density in ng/mL/g
        primary_gleason: Primary Gleason pattern (for pattern 5 detection)
        n_stage: N0, N1, or Nx
        m_stage: M0, M1a, M1b, M1c
    
    Returns:
        Risk group: "Very Low", "Low", "Favorable Intermediate", 
                    "Unfavorable Intermediate", "High", "Very High",
                    "Regional", or "Metastatic"
    """
    # Metastatic and regional first
    if m_stage != "M0":
        return "Metastatic"
    if n_stage == "N1":
        return "Regional"
    
    # Normalize T-stage
    t_stage = t_stage.upper().replace("C", "").replace("CT", "T")
    
    pct_positive = (positive_cores / total_cores * 100) if total_cores > 0 else 0
    
    # Count intermediate risk factors
    intermediate_factors = sum([
        t_stage in ["T2B", "T2C"],
        grade_group in [2, 3],
        10 <= psa <= 20
    ])
    
    # Count high risk factors
    high_risk_factors = sum([
        t_stage == "T3A",
        grade_group >= 4,
        psa > 20
    ])
    
    # Very High Risk checks
    if t_stage in ["T3B", "T4"]:
        return "Very High"
    if primary_gleason == 5:
        return "Very High"
    if positive_cores > 4 and grade_group >= 4:
        return "Very High"
    if high_risk_factors >= 2:
        return "Very High"
    
    # High Risk (exactly 1 high-risk feature)
    if high_risk_factors == 1:
        return "High"
    
    # Unfavorable Intermediate
    if intermediate_factors >= 2 or grade_group == 3 or pct_positive >= 50:
        return "Unfavorable Intermediate"
    
    # Favorable Intermediate
    if intermediate_factors == 1 and grade_group <= 2 and pct_positive < 50:
        return "Favorable Intermediate"
    
    # Low vs Very Low
    if t_stage in ["T1A", "T1B", "T1C", "T2A"] and grade_group == 1 and psa < 10:
        if (t_stage == "T1C" and positive_cores < 3 and 
            max_core_involvement <= 50 and psa_density < 0.15):
            return "Very Low"
        return "Low"
    
    return "Unable to classify"


# =============================================================================
# EAU RISK CLASSIFICATION
# =============================================================================

def calculate_eau_risk(
    psa: float,
    grade_group: int,
    t_stage: str,
    n_stage: str = "N0"
) -> str:
    """
    Calculate EAU risk group.
    
    Returns:
        "Low", "Intermediate Favorable", "Intermediate Unfavorable",
        "High-Risk Localized", or "High-Risk Locally Advanced"
    """
    t_stage = t_stage.upper().replace("C", "").replace("CT", "T")
    
    # Locally advanced
    if t_stage in ["T3A", "T3B", "T4"] or n_stage == "N1":
        return "High-Risk Locally Advanced"
    
    # High-risk localized
    if grade_group >= 4 or psa > 20 or t_stage == "T2C":
        return "High-Risk Localized"
    
    # Low risk (all criteria must be met)
    if grade_group == 1 and psa < 10 and t_stage in ["T1A", "T1B", "T1C", "T2A"]:
        return "Low"
    
    # Intermediate - favorable vs unfavorable
    if grade_group == 3:
        return "Intermediate Unfavorable"
    if grade_group == 2 and psa >= 10:
        return "Intermediate Unfavorable"
    
    return "Intermediate Favorable"


# =============================================================================
# TNM STAGING (AJCC 8TH EDITION)
# =============================================================================

def calculate_tnm_stage(
    clinical_t: str,
    n_stage: str = "N0",
    m_stage: str = "M0",
    psa: Optional[float] = None,
    grade_group: Optional[int] = None
) -> Dict[str, Any]:
    """
    Assign TNM staging categories per AJCC 8th Edition (2018).

    T Categories (Clinical):
        T1: Not palpable/visible
            T1a: Incidental, <5% of resected tissue
            T1b: Incidental, ≥5% of resected tissue
            T1c: Identified by needle biopsy (elevated PSA)
        T2: Confined to prostate
            T2a: ≤50% of one lobe
            T2b: >50% of one lobe, not both
            T2c: Both lobes
        T3: Extraprostatic extension
            T3a: ECE or microscopic bladder neck invasion
            T3b: Seminal vesicle invasion
        T4: Fixed or invades adjacent structures (external sphincter,
            rectum, bladder, levator muscles, pelvic wall)

    N Categories:
        N0: No regional lymph node metastasis
        N1: Regional lymph node metastasis

    M Categories:
        M0: No distant metastasis
        M1a: Non-regional lymph node metastasis
        M1b: Bone metastasis
        M1c: Other site metastasis (with or without bone)

    Args:
        clinical_t: Clinical T stage (T1a, T1b, T1c, T2a, T2b, T2c, T3a, T3b, T4)
        n_stage: N stage (N0, N1, NX)
        m_stage: M stage (M0, M1, M1a, M1b, M1c)
        psa: PSA level in ng/mL (for prognostic staging)
        grade_group: ISUP Grade Group 1-5 (for prognostic staging)

    Returns:
        Dict with TNM categories, descriptions, and prognostic stage if PSA/GG provided
    """
    # Normalize inputs
    clinical_t = clinical_t.upper().strip()
    # Handle "cT2a" -> "T2A" format
    if clinical_t.startswith("CT"):
        clinical_t = clinical_t[1:]
    elif clinical_t.startswith("C"):
        clinical_t = clinical_t[1:]

    n_stage = n_stage.upper().strip()
    m_stage = m_stage.upper().strip()

    # T stage descriptions
    t_descriptions = {
        "T1": "Tumor not palpable or visible on imaging",
        "T1A": "Incidental histologic finding in ≤5% of tissue resected",
        "T1B": "Incidental histologic finding in >5% of tissue resected",
        "T1C": "Tumor identified by needle biopsy (e.g., due to elevated PSA)",
        "T2": "Tumor confined within prostate",
        "T2A": "Tumor involves ≤50% of one lobe",
        "T2B": "Tumor involves >50% of one lobe but not both lobes",
        "T2C": "Tumor involves both lobes",
        "T3": "Extraprostatic tumor",
        "T3A": "Extraprostatic extension (unilateral or bilateral)",
        "T3B": "Tumor invades seminal vesicle(s)",
        "T4": "Tumor fixed or invades adjacent structures (external sphincter, rectum, bladder, levator muscles, pelvic wall)",
        "TX": "Primary tumor cannot be assessed"
    }

    n_descriptions = {
        "N0": "No regional lymph node metastasis",
        "N1": "Metastasis in regional lymph node(s)",
        "NX": "Regional lymph nodes not assessed"
    }

    m_descriptions = {
        "M0": "No distant metastasis",
        "M1": "Distant metastasis",
        "M1A": "Non-regional lymph node(s)",
        "M1B": "Bone(s)",
        "M1C": "Other site(s) with or without bone disease"
    }

    # Validate T stage
    valid_t = ["T1", "T1A", "T1B", "T1C", "T2", "T2A", "T2B", "T2C", "T3", "T3A", "T3B", "T4", "TX"]
    if clinical_t not in valid_t:
        return {
            'ok': False,
            'error': f"Invalid T stage: {clinical_t}. Valid values: {valid_t}"
        }

    # Validate N stage
    valid_n = ["N0", "N1", "NX"]
    if n_stage not in valid_n:
        return {
            'ok': False,
            'error': f"Invalid N stage: {n_stage}. Valid values: {valid_n}"
        }

    # Validate M stage
    valid_m = ["M0", "M1", "M1A", "M1B", "M1C"]
    if m_stage not in valid_m:
        return {
            'ok': False,
            'error': f"Invalid M stage: {m_stage}. Valid values: {valid_m}"
        }

    result = {
        'ok': True,
        't_stage': clinical_t,
        't_description': t_descriptions.get(clinical_t, "Unknown"),
        'n_stage': n_stage,
        'n_description': n_descriptions.get(n_stage, "Unknown"),
        'm_stage': m_stage,
        'm_description': m_descriptions.get(m_stage, "Unknown"),
        'tnm_summary': f"{clinical_t} {n_stage} {m_stage}"
    }

    # Calculate prognostic stage if PSA and Grade Group provided
    if psa is not None and grade_group is not None:
        prognostic = calculate_ajcc_prognostic_stage(
            clinical_t=clinical_t,
            n_stage=n_stage,
            m_stage=m_stage,
            psa=psa,
            grade_group=grade_group
        )
        result['prognostic_stage'] = prognostic.get('stage')
        result['prognostic_stage_description'] = prognostic.get('description')

    return result


def calculate_ajcc_prognostic_stage(
    clinical_t: str,
    n_stage: str,
    m_stage: str,
    psa: float,
    grade_group: int
) -> Dict[str, Any]:
    """
    Calculate AJCC 8th Edition prognostic stage group for prostate cancer.

    Prognostic Stage Groups:
        Stage I:    cT1a-c/cT2a, N0, M0, PSA <10, Grade Group 1
        Stage IIA:  cT1a-c/cT2a, N0, M0, PSA ≥10<20, Grade Group 1
                    OR cT2b-c, N0, M0, PSA <20, Grade Group 1
        Stage IIB:  cT1-2, N0, M0, PSA <20, Grade Group 2
        Stage IIC:  cT1-2, N0, M0, PSA <20, Grade Group 3-4
        Stage IIIA: cT1-2, N0, M0, PSA ≥20, Grade Group 1-4
        Stage IIIB: cT3-4, N0, M0, Any PSA, Grade Group 1-4
        Stage IIIC: Any T, N0, M0, Any PSA, Grade Group 5
        Stage IVA:  Any T, N1, M0, Any PSA, Any Grade Group
        Stage IVB:  Any T, Any N, M1, Any PSA, Any Grade Group

    Args:
        clinical_t: Clinical T stage
        n_stage: N stage (N0, N1)
        m_stage: M stage (M0, M1, M1a, M1b, M1c)
        psa: PSA level in ng/mL
        grade_group: ISUP Grade Group (1-5)

    Returns:
        Dict with stage, description, and criteria matched
    """
    # Normalize T stage
    clinical_t = clinical_t.upper().strip()
    if clinical_t.startswith("CT"):
        clinical_t = clinical_t[1:]
    elif clinical_t.startswith("C"):
        clinical_t = clinical_t[1:]

    n_stage = n_stage.upper().strip()
    m_stage = m_stage.upper().strip()

    # Input validation
    if psa is None or psa < 0:
        return {'ok': False, 'error': 'PSA must be a non-negative number'}
    if grade_group not in [1, 2, 3, 4, 5]:
        return {'ok': False, 'error': f'Grade Group must be 1-5 (got {grade_group})'}

    # Handle NX - cannot determine prognostic stage without N status
    if n_stage == "NX":
        return {
            'stage': 'Unable to classify',
            'description': 'N stage unknown (NX); AJCC prognostic stage requires definitive N staging',
            'criteria': f'{clinical_t}, NX, {m_stage}, PSA {psa:.1f}, GG{grade_group}'
        }

    # Helper functions
    def is_t1_t2a():
        return clinical_t in ["T1", "T1A", "T1B", "T1C", "T2", "T2A"]

    def is_t2b_c():
        return clinical_t in ["T2B", "T2C"]

    def is_t1_t2():
        return clinical_t in ["T1", "T1A", "T1B", "T1C", "T2", "T2A", "T2B", "T2C"]

    def is_t3_t4():
        return clinical_t in ["T3", "T3A", "T3B", "T4"]

    def is_m1():
        return m_stage in ["M1", "M1A", "M1B", "M1C"]

    # Stage determination (order matters - check from highest to lowest)

    # Stage IVB: Any M1
    if is_m1():
        return {
            'stage': 'IVB',
            'description': 'Metastatic disease',
            'criteria': f'{clinical_t}, {n_stage}, {m_stage}'
        }

    # Stage IVA: N1, M0
    if n_stage == "N1" and not is_m1():
        return {
            'stage': 'IVA',
            'description': 'Regional lymph node involvement',
            'criteria': f'{clinical_t}, N1, M0'
        }

    # From here, N0 and M0 assumed
    if n_stage != "N0" or is_m1():
        return {
            'ok': False,
            'error': 'Invalid combination for non-metastatic staging'
        }

    # Stage IIIC: Grade Group 5
    if grade_group == 5:
        return {
            'stage': 'IIIC',
            'description': 'Grade Group 5 (Gleason 9-10)',
            'criteria': f'{clinical_t}, N0, M0, GG5'
        }

    # Stage IIIB: T3-T4, Grade Group 1-4
    if is_t3_t4() and grade_group <= 4:
        return {
            'stage': 'IIIB',
            'description': 'Locally advanced (extraprostatic or seminal vesicle invasion)',
            'criteria': f'{clinical_t}, N0, M0, GG{grade_group}'
        }

    # Stage IIIA: T1-2, PSA ≥20, Grade Group 1-4
    if is_t1_t2() and psa >= 20 and grade_group <= 4:
        return {
            'stage': 'IIIA',
            'description': 'High PSA (≥20 ng/mL)',
            'criteria': f'{clinical_t}, N0, M0, PSA {psa:.1f}, GG{grade_group}'
        }

    # Stage IIC: T1-2, PSA <20, Grade Group 3-4
    if is_t1_t2() and psa < 20 and grade_group in [3, 4]:
        return {
            'stage': 'IIC',
            'description': 'Intermediate-unfavorable Grade Group',
            'criteria': f'{clinical_t}, N0, M0, PSA {psa:.1f}, GG{grade_group}'
        }

    # Stage IIB: T1-2, PSA <20, Grade Group 2
    if is_t1_t2() and psa < 20 and grade_group == 2:
        return {
            'stage': 'IIB',
            'description': 'Grade Group 2 (Gleason 3+4=7)',
            'criteria': f'{clinical_t}, N0, M0, PSA {psa:.1f}, GG2'
        }

    # Stage IIA: T1-2a with PSA 10-<20 GG1, OR T2b-c with PSA <20 GG1
    if grade_group == 1:
        if is_t1_t2a() and 10 <= psa < 20:
            return {
                'stage': 'IIA',
                'description': 'Intermediate PSA with low-grade cancer',
                'criteria': f'{clinical_t}, N0, M0, PSA {psa:.1f}, GG1'
            }
        if is_t2b_c() and psa < 20:
            return {
                'stage': 'IIA',
                'description': 'Bilateral disease with low-grade cancer',
                'criteria': f'{clinical_t}, N0, M0, PSA {psa:.1f}, GG1'
            }

    # Stage I: T1-2a, PSA <10, Grade Group 1
    if is_t1_t2a() and psa < 10 and grade_group == 1:
        return {
            'stage': 'I',
            'description': 'Localized low-risk disease',
            'criteria': f'{clinical_t}, N0, M0, PSA {psa:.1f}, GG1'
        }

    # Fallback
    return {
        'stage': 'Unable to classify',
        'description': 'Does not fit standard prognostic categories',
        'criteria': f'{clinical_t}, {n_stage}, {m_stage}, PSA {psa:.1f}, GG{grade_group}'
    }


# =============================================================================
# CAPRA SCORES
# =============================================================================

def calculate_capra(
    psa: float,
    primary_gleason: int,
    secondary_gleason: int,
    t_stage: str,
    pct_positive_cores: float,
    age: int
) -> Dict[str, Any]:
    """
    Calculate CAPRA score (0-10 points).
    
    Returns:
        Dict with 'score', 'risk_group', and 'breakdown'
    """
    score = 0
    breakdown = {}
    
    # PSA points
    if psa <= 6:
        breakdown['psa'] = 0
    elif psa <= 10:
        breakdown['psa'] = 1
        score += 1
    elif psa <= 20:
        breakdown['psa'] = 2
        score += 2
    elif psa <= 30:
        breakdown['psa'] = 3
        score += 3
    else:
        breakdown['psa'] = 4
        score += 4
    
    # Gleason pattern points
    if primary_gleason >= 4:
        breakdown['gleason'] = 3
        score += 3
    elif secondary_gleason >= 4:
        breakdown['gleason'] = 1
        score += 1
    else:
        breakdown['gleason'] = 0
    
    # T-stage points
    t_stage = t_stage.upper().replace("C", "").replace("CT", "T")
    if t_stage == "T3A":
        breakdown['t_stage'] = 1
        score += 1
    else:
        breakdown['t_stage'] = 0
    
    # % positive cores
    if pct_positive_cores >= 34:
        breakdown['cores'] = 1
        score += 1
    else:
        breakdown['cores'] = 0
    
    # Age
    if age >= 50:
        breakdown['age'] = 1
        score += 1
    else:
        breakdown['age'] = 0
    
    # Risk group
    if score <= 2:
        risk_group = "Low"
    elif score <= 5:
        risk_group = "Intermediate"
    else:
        risk_group = "High"
    
    return {
        'score': score,
        'risk_group': risk_group,
        'breakdown': breakdown
    }


def calculate_capra_s(
    preop_psa: float,
    path_gleason: str,
    margin_positive: bool,
    ece: bool,
    svi: bool,
    lni: bool
) -> Dict[str, Any]:
    """
    Calculate CAPRA-S score (0-12 points) post-prostatectomy.
    
    Args:
        preop_psa: Pre-operative PSA in ng/mL
        path_gleason: Pathologic Gleason (e.g., "3+3", "3+4", "4+3", "4+4", "4+5")
        margin_positive: Positive surgical margin
        ece: Extracapsular extension
        svi: Seminal vesicle invasion
        lni: Lymph node invasion
    
    Returns:
        Dict with 'score', 'risk_group', and 'breakdown'
    """
    score = 0
    breakdown = {}
    
    # PSA points
    if preop_psa <= 6:
        breakdown['psa'] = 0
    elif preop_psa <= 10:
        breakdown['psa'] = 1
        score += 1
    elif preop_psa <= 20:
        breakdown['psa'] = 2
        score += 2
    else:
        breakdown['psa'] = 3
        score += 3
    
    # Pathologic Gleason
    gleason_map = {
        "3+3": 0, "6": 0,
        "3+4": 1, "7a": 1,
        "4+3": 2, "7b": 2,
        "4+4": 3, "8": 3,
        "4+5": 3, "5+4": 3, "5+3": 3, "3+5": 3,
        "5+5": 3, "9": 3, "10": 3
    }
    gs = path_gleason.replace(" ", "")
    breakdown['gleason'] = gleason_map.get(gs, 0)
    score += breakdown['gleason']
    
    # Margin
    if margin_positive:
        breakdown['margin'] = 2
        score += 2
    else:
        breakdown['margin'] = 0
    
    # ECE
    if ece:
        breakdown['ece'] = 1
        score += 1
    else:
        breakdown['ece'] = 0
    
    # SVI
    if svi:
        breakdown['svi'] = 2
        score += 2
    else:
        breakdown['svi'] = 0
    
    # LNI
    if lni:
        breakdown['lni'] = 1
        score += 1
    else:
        breakdown['lni'] = 0
    
    # Risk group
    if score <= 2:
        risk_group = "Low"
    elif score <= 5:
        risk_group = "Intermediate"
    else:
        risk_group = "High"
    
    return {
        'score': score,
        'risk_group': risk_group,
        'breakdown': breakdown
    }


# =============================================================================
# LNI NOMOGRAMS
# =============================================================================

def briganti_2017_lni(
    psa: float,
    t_stage: str,
    grade_group: int,
    pct_positive_highest: float,
    pct_positive_lowest: float
) -> Dict[str, Any]:
    """
    Briganti 2017 nomogram for LNI prediction.
    Uses published beta coefficients (c-statistic 0.908).
    
    Args:
        psa: PSA in ng/mL
        t_stage: T1, T2, or T3 (simplified)
        grade_group: ISUP Grade Group 1-5
        pct_positive_highest: % cores with highest grade pattern (0-100)
        pct_positive_lowest: % cores with lowest grade pattern (0-100)
    
    Returns:
        Dict with 'probability', 'recommend_eplnd', and 'linear_predictor'
    """
    # Normalize T-stage
    t_stage = t_stage.upper().replace("C", "").replace("CT", "T")
    if t_stage in ["T1A", "T1B", "T1C"]:
        t_stage = "T1"
    elif t_stage in ["T2A", "T2B", "T2C"]:
        t_stage = "T2"
    elif t_stage in ["T3A", "T3B"]:
        t_stage = "T3"
    
    # Indicator variables
    ct2 = 1 if t_stage == "T2" else 0
    ct3 = 1 if t_stage == "T3" else 0
    gg2 = 1 if grade_group == 2 else 0
    gg3 = 1 if grade_group == 3 else 0
    gg4 = 1 if grade_group == 4 else 0
    gg5 = 1 if grade_group == 5 else 0
    
    # Linear predictor
    lp = (-5.8717 
          + (0.0826 * psa)
          + (0.3633 * ct2)
          + (0.9555 * ct3)
          + (0.3293 * gg2)
          + (0.7419 * gg3)
          + (0.8755 * gg4)
          + (1.2809 * gg5)
          + (0.0130 * pct_positive_highest)
          + (0.0113 * pct_positive_lowest))
    
    # Probability
    prob = 1 / (1 + math.exp(-lp))
    prob_pct = prob * 100
    
    return {
        'probability': round(prob_pct, 1),
        'recommend_eplnd': prob_pct >= 7,
        'linear_predictor': round(lp, 4),
        'threshold': 7
    }


def briganti_2012_lni(
    psa: float,
    t_stage: str,
    primary_gleason: int,
    secondary_gleason: int,
    pct_positive_cores: float
) -> Dict[str, Any]:
    """
    Briganti 2012 nomogram approximation.
    Note: Exact coefficients not published; this is a simplified version.
    
    Returns estimated LNI probability.
    """
    # Simplified scoring based on published risk factors
    t_stage = t_stage.upper().replace("C", "").replace("CT", "T")
    
    # Base risk from PSA
    if psa < 10:
        base = 2
    elif psa < 20:
        base = 5
    else:
        base = 10
    
    # Gleason adjustment
    gs = primary_gleason + secondary_gleason
    if gs <= 6:
        gleason_mult = 1.0
    elif gs == 7:
        gleason_mult = 1.5 if primary_gleason == 3 else 2.0
    elif gs == 8:
        gleason_mult = 3.0
    else:
        gleason_mult = 4.0
    
    # T-stage adjustment
    if t_stage in ["T1A", "T1B", "T1C", "T2A"]:
        stage_mult = 1.0
    elif t_stage in ["T2B", "T2C"]:
        stage_mult = 1.5
    else:
        stage_mult = 2.5
    
    # Core adjustment
    core_mult = 1 + (pct_positive_cores / 100)
    
    prob = base * gleason_mult * stage_mult * core_mult
    prob = min(prob, 95)  # Cap at 95%
    
    return {
        'probability': round(prob, 1),
        'recommend_eplnd': prob >= 7,
        'note': 'Approximation - use 2017 version for exact calculation'
    }


def roach_lni(psa: float, gleason: int) -> Dict[str, Any]:
    """
    Roach formula for LNI risk.

    Formula: LNI Risk (%) = (2/3 × PSA) + [(Gleason - 6) × 10]

    Note: Overestimates contemporary LNI by 2.5-16 fold but validated
    for RT field decisions.

    Args:
        psa: PSA in ng/mL
        gleason: Gleason score (6-10)

    Returns:
        Dict with probability (0-100%), recommendation, and notes
    """
    # Validate inputs
    if gleason < 6 or gleason > 10:
        return {
            'ok': False,
            'error': f'Gleason score must be 6-10 for Roach formula (got {gleason})'
        }
    if psa < 0:
        return {
            'ok': False,
            'error': f'PSA must be non-negative (got {psa})'
        }

    prob = (2/3 * psa) + ((gleason - 6) * 10)
    prob = max(0.0, min(prob, 100.0))  # Clamp to valid probability range 0-100%

    return {
        'ok': True,
        'probability': round(prob, 1),
        'recommend_pelvic_rt': prob >= 15,
        'threshold': 15,
        'note': 'Validated for RT field decisions; overestimates surgical LNI'
    }


def yale_lni(psa: float, gleason: int, t_stage: str) -> Dict[str, Any]:
    """
    Yale formula for LNI risk.
    
    Formula: LNI Risk (%) = (Gleason - 5) × [PSA/3 + 1.5 × T]
    where T = 0 (T1c), 1 (T2a), 2 (T2b/c)
    """
    t_stage = t_stage.upper().replace("C", "").replace("CT", "T")
    
    if t_stage in ["T1A", "T1B", "T1C"]:
        t_value = 0
    elif t_stage == "T2A":
        t_value = 1
    else:
        t_value = 2
    
    prob = (gleason - 5) * (psa/3 + 1.5 * t_value)
    prob = max(0, prob)
    
    return {
        'probability': round(prob, 1),
        't_value_used': t_value
    }


def mskcc_lni(
    psa: float,
    grade_group: int,
    t_stage: str
) -> Dict[str, Any]:
    """
    MSKCC/Partin table approximation for LNI.
    
    Note: Full implementation requires lookup tables.
    This provides a simplified estimate.
    """
    t_stage = t_stage.upper().replace("C", "").replace("CT", "T")
    
    # Simplified risk matrix based on published tables
    # PSA categories: 0-2.5, 2.6-4, 4.1-6, 6.1-10, >10
    # GG categories: 1, 2, 3, 4-5
    # Stage categories: T1c, T2a, T2b/c, T3
    
    # Base probability by GG
    gg_base = {1: 1, 2: 3, 3: 8, 4: 15, 5: 25}
    base = gg_base.get(grade_group, 5)
    
    # PSA multiplier
    if psa <= 4:
        psa_mult = 0.5
    elif psa <= 10:
        psa_mult = 1.0
    elif psa <= 20:
        psa_mult = 1.5
    else:
        psa_mult = 2.5
    
    # Stage multiplier
    if t_stage in ["T1A", "T1B", "T1C"]:
        stage_mult = 0.8
    elif t_stage == "T2A":
        stage_mult = 1.0
    elif t_stage in ["T2B", "T2C"]:
        stage_mult = 1.3
    else:
        stage_mult = 2.0
    
    prob = base * psa_mult * stage_mult
    
    return {
        'probability': round(prob, 1),
        'recommend_eplnd': prob >= 7,
        'note': 'Approximation - use official MSKCC calculator for precise values',
        'calculator_url': 'https://www.mskcc.org/nomograms/prostate'
    }


# =============================================================================
# PSADT CALCULATION
# =============================================================================

def calculate_psadt(
    psa_values: List[Tuple[float, float]],
    require_rising: bool = True,
    min_psa: float = 0.20,
    min_values: int = 3,
    min_observation_days: int = 90
) -> Dict[str, Any]:
    """
    Calculate PSA doubling time from serial measurements.

    Clinical requirements (per guidelines):
        - Minimum 3 PSA values
        - ≥3 months (90 days) observation period
        - All values ≥0.20 ng/mL
        - All values rising (PSA₂ > PSA₁)
        - Same laboratory/assay (not validated here)

    Args:
        psa_values: List of (time_in_days, psa_value) tuples
        require_rising: If True, validates all PSA values are rising
        min_psa: Minimum PSA threshold (default 0.20 ng/mL)
        min_values: Minimum number of PSA values required (default 3)
        min_observation_days: Minimum observation period in days (default 90)

    Returns:
        Dict with 'ok' boolean, and either results or 'error' message
    """
    # Validate minimum number of values
    if len(psa_values) < min_values:
        return {
            'ok': False,
            'error': f'Need ≥{min_values} PSA values for PSADT (got {len(psa_values)})'
        }

    # Sort by time
    psa_values = sorted(psa_values, key=lambda x: x[0])

    times = [t for t, _ in psa_values]
    psas = [p for _, p in psa_values]

    # Validate observation period
    observation_days = times[-1] - times[0]
    if observation_days < min_observation_days:
        return {
            'ok': False,
            'error': f'Need ≥{min_observation_days} days observation (got {observation_days:.0f} days)'
        }

    # Validate all PSA > 0
    if any(p <= 0 for p in psas):
        return {
            'ok': False,
            'error': 'All PSA values must be >0'
        }

    # Validate minimum PSA threshold
    if any(p < min_psa for p in psas):
        below_threshold = [p for p in psas if p < min_psa]
        return {
            'ok': False,
            'error': f'All PSA values should be ≥{min_psa} ng/mL (found: {below_threshold})'
        }

    # Check rising trend
    if require_rising:
        for i in range(len(psas) - 1):
            if psas[i+1] <= psas[i]:
                return {
                    'ok': False,
                    'error': f'PSA values must be rising (PSA[{i}]={psas[i]:.2f} ≥ PSA[{i+1}]={psas[i+1]:.2f})'
                }

    # Log transform PSA
    ln_psa = [math.log(p) for p in psas]

    # Linear regression
    n = len(times)
    sum_t = sum(times)
    sum_ln = sum(ln_psa)
    sum_t2 = sum(t**2 for t in times)
    sum_t_ln = sum(t * ln for t, ln in zip(times, ln_psa))

    # Slope calculation
    denominator = n * sum_t2 - sum_t**2
    if denominator == 0:
        return {
            'ok': False,
            'error': 'Cannot calculate slope (all time values identical)'
        }

    slope = (n * sum_t_ln - sum_t * sum_ln) / denominator

    if slope <= 0:
        return {
            'ok': True,
            'psadt_months': float('inf'),
            'psadt_days': float('inf'),
            'interpretation': 'PSA stable or declining',
            'slope': slope,
            'n_values': n,
            'observation_days': observation_days
        }

    # Calculate PSADT
    psadt_days = 0.693 / slope  # ln(2) / slope
    psadt_months = psadt_days / 30.44
    psadt_months_rounded = round(psadt_months, 1)

    # R-squared
    intercept = (sum_ln - slope * sum_t) / n
    ss_res = sum((ln - (slope * t + intercept))**2 for t, ln in zip(times, ln_psa))
    mean_ln = sum_ln / n
    ss_tot = sum((ln - mean_ln)**2 for ln in ln_psa)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

    # Use rounded value for interpretation to ensure consistency
    return {
        'ok': True,
        'psadt_months': psadt_months_rounded,
        'psadt_days': round(psadt_days, 0),
        'slope': round(slope, 6),
        'r_squared': round(r_squared, 3),
        'interpretation': interpret_psadt(psadt_months_rounded)['interpretation'],
        'n_values': n,
        'observation_days': observation_days
    }


def interpret_psadt(psadt_months: float) -> Dict[str, str]:
    """
    Clinical interpretation of PSADT value.
    """
    if psadt_months < 3:
        return {
            'interpretation': 'Extremely high risk',
            'detail': 'PSADT <3 months: PCa mortality ~100%, median survival 5-6 years',
            'recommendation': 'Systemic therapy primary; consider intensified treatment'
        }
    elif psadt_months < 6:
        return {
            'interpretation': 'Very high risk',
            'detail': 'PSADT <6 months: Rapid progression likely',
            'recommendation': 'Consider systemic therapy; if local, intensified approach'
        }
    elif psadt_months < 9:
        return {
            'interpretation': 'High risk',
            'detail': 'PSADT <9 months: Meets EMBARK criteria if PSA ≥1',
            'recommendation': 'Early salvage RT with ADT; consider enzalutamide'
        }
    elif psadt_months < 12:
        return {
            'interpretation': 'Moderate-high risk',
            'detail': 'PSADT <12 months: EAU high-risk BCR',
            'recommendation': 'Salvage RT with ADT recommended'
        }
    elif psadt_months < 15:
        return {
            'interpretation': 'Moderate risk',
            'detail': 'PSADT 12-15 months: Borderline',
            'recommendation': 'Salvage RT; ADT duration per other factors'
        }
    else:
        return {
            'interpretation': 'Favorable',
            'detail': 'PSADT >15 months: Lower risk of progression',
            'recommendation': 'Observation may be appropriate; RT alone if treated'
        }


# =============================================================================
# EAU BCR RISK CLASSIFICATION
# =============================================================================

def eau_bcr_risk(
    psadt_months: float,
    grade_group: int,
    time_to_bcr_months: Optional[float] = None,
    current_psa: Optional[float] = None
) -> Dict[str, Any]:
    """
    EAU biochemical recurrence risk classification (post-RP).

    Low-risk BCR (ALL required):
        - PSADT > 12 months
        - Grade Group 1-3
        - Time to BCR > 18 months (if available)

    High-risk BCR (ANY):
        - PSADT ≤ 12 months
        - Grade Group 4-5

    Args:
        psadt_months: PSA doubling time in months
        grade_group: Pathologic Grade Group (1-5)
        time_to_bcr_months: Time from RP to BCR in months (optional)
        current_psa: Current PSA level in ng/mL (required for EMBARK eligibility)
    """
    high_risk_factors = []
    low_risk_criteria_met = []

    # PSADT assessment
    if psadt_months <= 12:
        high_risk_factors.append(f"PSADT ≤12 months ({psadt_months:.1f})")
    else:
        low_risk_criteria_met.append(f"PSADT >12 months ({psadt_months:.1f})")

    # Grade Group assessment
    if grade_group >= 4:
        high_risk_factors.append(f"Grade Group {grade_group}")
    else:
        low_risk_criteria_met.append(f"Grade Group {grade_group}")

    # Time to BCR (if available)
    if time_to_bcr_months is not None:
        if time_to_bcr_months > 18:
            low_risk_criteria_met.append(f"Time to BCR >18 months ({time_to_bcr_months:.0f})")
        else:
            # Not a high-risk factor per se, but doesn't meet low-risk criterion
            pass

    # Determine classification
    if len(high_risk_factors) > 0:
        risk_group = "High Risk BCR"
    elif len(low_risk_criteria_met) >= 2:  # Need at least PSADT and GG criteria
        risk_group = "Low Risk BCR"
    else:
        risk_group = "Indeterminate"

    # EMBARK eligibility (NEJM 2023): PSADT ≤9 months AND PSA ≥1 ng/mL (post-RP)
    # Both criteria must be met for full eligibility
    embark_psadt_met = psadt_months <= 9
    embark_psa_met = current_psa is not None and current_psa >= 1.0
    embark_eligible = embark_psadt_met and embark_psa_met

    # Build EMBARK note (always provide a meaningful message)
    if current_psa is None:
        embark_note = "EMBARK eligibility requires PSA value (PSADT ≤9mo AND PSA ≥1 ng/mL)"
    elif embark_eligible:
        embark_note = f"EMBARK eligible: PSADT {psadt_months:.1f}mo ≤9 AND PSA {current_psa:.2f} ≥1 ng/mL"
    elif embark_psadt_met:
        embark_note = f"PSADT meets EMBARK ({psadt_months:.1f}mo ≤9), but PSA {current_psa:.2f} <1 ng/mL"
    else:
        embark_note = f"Not EMBARK eligible: PSADT {psadt_months:.1f}mo >9 (requires ≤9mo)"

    return {
        'risk_group': risk_group,
        'high_risk_factors': high_risk_factors,
        'low_risk_criteria': low_risk_criteria_met,
        'embark_eligible': embark_eligible,
        'embark_psadt_met': embark_psadt_met,
        'embark_psa_met': embark_psa_met if current_psa is not None else None,
        'embark_note': embark_note
    }


# =============================================================================
# SALVAGE RT DECISIONS
# =============================================================================

def pelvic_node_recommendation(
    pre_srt_psa: float,
    lni_risk_briganti: Optional[float] = None,
    lni_risk_roach: Optional[float] = None,
    using_adt: bool = True
) -> Dict[str, Any]:
    """
    Recommend whether to include pelvic lymph nodes in salvage RT.
    Based on RTOG 0534/SPPORT evidence.
    """
    reasons_for = []
    reasons_against = []
    
    # PSA threshold from SPPORT
    if pre_srt_psa > 0.35:
        reasons_for.append(f"PSA {pre_srt_psa:.2f} > 0.35 (SPPORT benefit threshold)")
    else:
        reasons_against.append(f"PSA {pre_srt_psa:.2f} ≤ 0.35")
    
    # LNI risk from nomograms
    if lni_risk_roach is not None and lni_risk_roach >= 15:
        reasons_for.append(f"Roach LNI risk {lni_risk_roach:.1f}% ≥ 15%")
    
    if lni_risk_briganti is not None and lni_risk_briganti >= 7:
        reasons_for.append(f"Briganti LNI risk {lni_risk_briganti:.1f}% ≥ 7%")
    
    # ADT use
    if not using_adt:
        reasons_against.append("SPPORT used ADT with pelvic RT")
    
    # Recommendation
    if len(reasons_for) >= 1 and using_adt:
        recommendation = "Include pelvic nodes"
        strength = "Strong" if pre_srt_psa > 0.5 else "Moderate"
    elif len(reasons_for) >= 1:
        recommendation = "Consider pelvic nodes"
        strength = "Conditional"
    else:
        recommendation = "Prostate bed alone may be sufficient"
        strength = "Conditional"
    
    return {
        'recommendation': recommendation,
        'strength': strength,
        'reasons_for_pelvic_nodes': reasons_for,
        'reasons_against': reasons_against,
        'spport_reference': 'RTOG 0534/SPPORT showed benefit with PSA >0.35 ng/mL'
    }


def adt_duration_recommendation(
    pre_srt_psa: float,
    grade_group: int,
    psadt_months: float,
    decipher: Optional[float] = None,
    svi: bool = False,
    lni: bool = False
) -> Dict[str, Any]:
    """
    Recommend ADT duration with salvage RT.
    Based on GETUG-AFU 16, RTOG 9601, and RADICALS-HD.
    """
    high_risk_factors = []
    low_risk_factors = []
    
    # Pre-SRT PSA assessment
    if pre_srt_psa >= 1.5:
        high_risk_factors.append(f"PSA ≥1.5 ({pre_srt_psa:.2f}) - RTOG 9601 strong benefit")
    elif pre_srt_psa >= 0.7:
        high_risk_factors.append(f"PSA 0.7-1.5 ({pre_srt_psa:.2f}) - RTOG 9601 moderate benefit")
    else:
        low_risk_factors.append(f"PSA <0.7 ({pre_srt_psa:.2f}) - potential harm from ADT")
    
    # Grade Group
    if grade_group >= 4:
        high_risk_factors.append(f"Grade Group {grade_group}")
    else:
        low_risk_factors.append(f"Grade Group {grade_group}")
    
    # PSADT
    if psadt_months <= 6:
        high_risk_factors.append(f"PSADT ≤6 months ({psadt_months:.1f})")
    elif psadt_months <= 12:
        high_risk_factors.append(f"PSADT 6-12 months ({psadt_months:.1f})")
    else:
        low_risk_factors.append(f"PSADT >12 months ({psadt_months:.1f})")
    
    # Decipher
    if decipher is not None:
        if decipher >= 0.6:
            high_risk_factors.append(f"Decipher high ({decipher:.2f})")
        elif decipher < 0.45:
            low_risk_factors.append(f"Decipher low ({decipher:.2f})")
    
    # Pathologic factors
    if svi:
        high_risk_factors.append("Seminal vesicle invasion")
    if lni:
        high_risk_factors.append("Lymph node invasion")
    
    # Determine recommendation
    if pre_srt_psa < 0.7 and len(high_risk_factors) <= 1:
        recommendation = "RT alone or observation"
        duration = "0 months"
        rationale = "RTOG 9601: No benefit, potential harm in PSA <0.7"
    elif len(high_risk_factors) >= 3 or pre_srt_psa >= 1.5:
        recommendation = "Long-term ADT"
        duration = "24 months"
        rationale = "RTOG 9601 + RADICALS-HD support long-term ADT"
    elif len(high_risk_factors) >= 1:
        recommendation = "Short-term ADT"
        duration = "4-6 months"
        rationale = "GETUG-AFU 16 shows PFS/MFS benefit"
    else:
        recommendation = "RT alone acceptable"
        duration = "0 months"
        rationale = "Low-risk profile; ADT toxicity may outweigh benefit"
    
    return {
        'recommendation': recommendation,
        'duration': duration,
        'rationale': rationale,
        'high_risk_factors': high_risk_factors,
        'low_risk_factors': low_risk_factors,
        'trials_referenced': ['GETUG-AFU 16', 'RTOG 9601', 'RADICALS-HD']
    }


def spport_eligible(
    t_stage: str,
    gleason: int,
    pre_srt_psa: float,
    n_stage: str = "N0"
) -> Dict[str, bool]:
    """
    Check eligibility for RTOG 0534/SPPORT criteria.
    """
    t_stage = t_stage.upper().replace("C", "").replace("P", "")
    
    eligible = True
    criteria = {}
    
    # pT2-pT3
    criteria['stage'] = t_stage in ["T2", "T2A", "T2B", "T2C", "T3", "T3A", "T3B"]
    if not criteria['stage']:
        eligible = False
    
    # Gleason ≤9
    criteria['gleason'] = gleason <= 9
    if not criteria['gleason']:
        eligible = False
    
    # PSA 0.1-2.0
    criteria['psa'] = 0.1 <= pre_srt_psa <= 2.0
    if not criteria['psa']:
        eligible = False
    
    # N0 or Nx
    criteria['nodes'] = n_stage in ["N0", "NX"]
    if not criteria['nodes']:
        eligible = False
    
    return {
        'eligible': eligible,
        'criteria': criteria
    }


# =============================================================================
# POLISH ABIRATERONE ELIGIBILITY (NFZ 2026 - C.87.a / C.87.b)
# =============================================================================

def check_abiraterone_eligibility_poland(
    # Disease state
    disease_state: str,  # "mHSPC", "mCSPC", "nmCRPC", "mCRPC", "adjuvant_post_RT"

    # Patient characteristics
    has_metastases: bool = False,
    castration_resistant: bool = False,

    # For mHSPC/mCSPC high-risk assessment
    gleason_score: Optional[int] = None,
    bone_metastases_count: Optional[int] = None,
    has_visceral_metastases: bool = False,  # Excluding lymph nodes

    # For nmCRPC
    psadt_months: Optional[float] = None,

    # For adjuvant post-RT
    after_radical_rt: bool = False,
    n_positive: Optional[bool] = None,  # Lymph node involvement
    t_stage: Optional[str] = None,  # T3-4 is a risk factor
    psa_at_diagnosis: Optional[float] = None,  # PSA ≥40 is a risk factor

    # For mCRPC
    symptomatic: bool = False,  # Asymptomatic/oligosymptomatic required for some indications
    post_docetaxel: bool = False,
    adt_failure: bool = False,

    # Treatment history (exclusion criteria)
    prior_novel_hormonal_agent: bool = False,  # Apalutamide, enzalutamide, darolutamid
    prior_abiraterone: bool = False,
    months_since_adt_start: Optional[float] = None
) -> Dict[str, Any]:
    """
    Check eligibility for abiraterone acetate under Polish NFZ reimbursement criteria (2026).

    Based on Attachments C.87.a and C.87.b of the Polish drug reimbursement program.

    Disease states:
        - "mHSPC": Metastatic hormone-sensitive prostate cancer (newly diagnosed, high-risk)
        - "mCSPC": Metastatic castration-sensitive (not meeting C.87.a high-risk criteria)
        - "nmCRPC": Non-metastatic castration-resistant prostate cancer
        - "mCRPC": Metastatic castration-resistant prostate cancer
        - "adjuvant_post_RT": Adjuvant hormonal therapy after radical radiotherapy

    IMPORTANT RESTRICTIONS:
        - Patient can only receive abiraterone under ONE indication (C.87.a OR C.87.b)
        - Cannot use if previously treated with apalutamide, enzalutamide, or darolutamide

    Returns:
        Dict with eligibility status, qualifying indication, and detailed criteria assessment
    """
    result = {
        'eligible': False,
        'indication': None,
        'attachment': None,
        'criteria_met': [],
        'criteria_not_met': [],
        'warnings': [],
        'exclusions': []
    }

    # =========================================================================
    # GLOBAL EXCLUSION CRITERIA
    # =========================================================================

    if prior_abiraterone:
        result['exclusions'].append("Wcześniejsze leczenie abirateronem (można stosować tylko w jednym wskazaniu)")
        result['exclusion_reason'] = "Prior abiraterone treatment"
        return result

    if prior_novel_hormonal_agent:
        result['exclusions'].append(
            "Wcześniejsze leczenie nowoczesnym lekiem hormonalnym (apalutamid, enzalutamid, darolutamid)"
        )
        result['exclusion_reason'] = "Prior novel hormonal agent (apalutamide, enzalutamide, darolutamide)"
        return result

    disease_state = disease_state.lower().strip()

    # =========================================================================
    # ATTACHMENT C.87.a - HIGH-RISK mHSPC, mCRPC (PRE/POST CHEMO)
    # =========================================================================

    # --- C.87.a.1: High-risk newly diagnosed mHSPC ---
    if disease_state == "mhspc":
        if not has_metastases:
            result['criteria_not_met'].append("Brak przerzutów (wymagane przerzuty dla mHSPC)")
            return result

        if castration_resistant:
            result['criteria_not_met'].append("Rak oporny na kastrację (wymagany hormonowrażliwy)")
            return result

        # Check for required data to assess high-risk factors
        missing_data = []
        if gleason_score is None:
            missing_data.append("Gleason")
        if bone_metastases_count is None:
            missing_data.append("liczba przerzutów do kości")
        # has_visceral_metastases is boolean, assumed known (defaults to False)

        if missing_data:
            result['criteria_not_met'].append(
                f"Brak danych wymaganych do oceny wysokiego ryzyka: {', '.join(missing_data)}"
            )
            result['warnings'].append(
                "Nie można ocenić kwalifikacji do C.87.a bez pełnych danych o czynnikach ryzyka"
            )
            return result

        # Count high-risk factors (need ≥2 of 3)
        high_risk_factors = 0
        high_risk_details = []

        # Factor 1: Gleason ≥8
        if gleason_score >= 8:
            high_risk_factors += 1
            high_risk_details.append(f"Gleason ≥8 ({gleason_score})")
        else:
            result['criteria_not_met'].append(f"Gleason <8 ({gleason_score})")

        # Factor 2: ≥3 bone metastases
        if bone_metastases_count >= 3:
            high_risk_factors += 1
            high_risk_details.append(f"≥3 przerzuty do kości ({bone_metastases_count})")
        else:
            result['criteria_not_met'].append(f"<3 przerzuty do kości ({bone_metastases_count})")

        # Factor 3: Visceral metastases (excluding lymph nodes)
        if has_visceral_metastases:
            high_risk_factors += 1
            high_risk_details.append("Przerzuty trzewne (z wyłączeniem węzłów chłonnych)")

        if high_risk_factors >= 2:
            result['eligible'] = True
            result['indication'] = "mHSPC wysokiego ryzyka (nowo rozpoznany)"
            result['indication_en'] = "High-risk newly diagnosed mHSPC"
            result['attachment'] = "C.87.a"
            result['criteria_met'] = high_risk_details
            result['high_risk_factors_count'] = high_risk_factors

            # Check timing requirement (MANDATORY - must start within 3 months of ADT)
            if months_since_adt_start is None:
                result['eligible'] = False
                result['criteria_not_met'].append(
                    "Brak danych o czasie od rozpoczęcia ADT (wymagane: ≤3 miesiące)"
                )
                result['warnings'].append(
                    "Podaj months_since_adt_start - leczenie musi być rozpoczęte w ciągu 3 mies. od ADT"
                )
            elif months_since_adt_start > 3:
                result['eligible'] = False
                result['criteria_not_met'].append(
                    f"Przekroczony limit czasowy: {months_since_adt_start:.1f} mies. od ADT (max. 3 mies.)"
                )
            else:
                result['criteria_met'].append(
                    f"Rozpoczęcie w ciągu 3 mies. od ADT ({months_since_adt_start:.1f} mies.)"
                )
        else:
            result['criteria_not_met'].append(
                f"Wymagane ≥2 z 3 czynników wysokiego ryzyka (spełnione: {high_risk_factors})"
            )
            # Check if eligible under C.87.b (mCSPC without high-risk)
            result['alternative'] = "Rozważ kwalifikację jako mCSPC (zał. C.87.b)"

        return result

    # --- C.87.a.2: mCRPC asymptomatic/oligosymptomatic, pre-chemotherapy ---
    if disease_state == "mcrpc" and not post_docetaxel:
        if not has_metastases:
            result['criteria_not_met'].append("Brak przerzutów (wymagane dla mCRPC)")
            return result

        if not castration_resistant:
            result['criteria_not_met'].append("Rak wrażliwy na kastrację (wymagany CRPC)")
            return result

        if not adt_failure:
            result['criteria_not_met'].append("Wymagane niepowodzenie ADT")
            return result

        if symptomatic:
            result['criteria_not_met'].append(
                "Pacjent objawowy (wymagany bezobjawowy lub skąpoobjawowy)"
            )
            result['warnings'].append(
                "Dla pacjentów objawowych rozważ chemioterapię lub C.87.a.3 po docetakselu"
            )
            return result

        result['eligible'] = True
        result['indication'] = "mCRPC bezobjawowy/skąpoobjawowy, przed chemioterapią"
        result['indication_en'] = "Asymptomatic/oligosymptomatic mCRPC, pre-chemotherapy"
        result['attachment'] = "C.87.a"
        result['criteria_met'] = [
            "Oporny na kastrację",
            "Przerzuty obecne",
            "Niepowodzenie ADT",
            "Bezobjawowy lub skąpoobjawowy",
            "Chemioterapia nie jest jeszcze wskazana klinicznie"
        ]
        return result

    # --- C.87.a.3: mCRPC post-docetaxel (after chemotherapy failure) ---
    if disease_state == "mcrpc" and post_docetaxel:
        if not has_metastases:
            result['criteria_not_met'].append("Brak przerzutów (wymagane dla mCRPC)")
            return result

        if not castration_resistant:
            result['criteria_not_met'].append("Rak wrażliwy na kastrację (wymagany CRPC)")
            return result

        result['eligible'] = True
        result['indication'] = "mCRPC po niepowodzeniu chemioterapii opartej o docetaksel"
        result['indication_en'] = "mCRPC after docetaxel-based chemotherapy failure"
        result['attachment'] = "C.87.a"
        result['criteria_met'] = [
            "Oporny na kastrację",
            "Przerzuty obecne",
            "Po niepowodzeniu chemioterapii opartej o docetaksel (progresja lub nietolerancja)"
        ]
        result['warnings'].append(
            "UWAGA: post_docetaxel=True zakłada niepowodzenie leczenia docetakselem "
            "(progresja biochemiczna/kliniczna lub nietolerancja)"
        )
        return result

    # =========================================================================
    # ATTACHMENT C.87.b - mCSPC, nmCRPC, ADJUVANT POST-RT
    # =========================================================================

    # --- C.87.b.1: mCSPC (not meeting C.87.a high-risk criteria) ---
    if disease_state == "mcspc":
        if not has_metastases:
            result['criteria_not_met'].append("Brak przerzutów (wymagane dla mCSPC)")
            return result

        if castration_resistant:
            result['criteria_not_met'].append("Rak oporny na kastrację (wymagany wrażliwy)")
            return result

        # CRITICAL: mCSPC requires NOT meeting C.87.a high-risk criteria
        # Must verify patient doesn't qualify for C.87.a (≥2 of 3 high-risk factors)
        high_risk_factors = 0
        high_risk_details = []

        if gleason_score is not None and gleason_score >= 8:
            high_risk_factors += 1
            high_risk_details.append(f"Gleason ≥8 ({gleason_score})")
        if bone_metastases_count is not None and bone_metastases_count >= 3:
            high_risk_factors += 1
            high_risk_details.append(f"≥3 przerzuty do kości ({bone_metastases_count})")
        if has_visceral_metastases:
            high_risk_factors += 1
            high_risk_details.append("Przerzuty trzewne")

        if high_risk_factors >= 2:
            result['criteria_not_met'].append(
                f"Spełnia kryteria wysokiego ryzyka C.87.a ({high_risk_factors}/3 czynników)"
            )
            result['criteria_not_met'].extend(high_risk_details)
            result['alternative'] = "Pacjent kwalifikuje się do C.87.a (mHSPC wysokiego ryzyka), nie C.87.b"
            return result

        # Check if we have enough data to confirm NOT high-risk
        if gleason_score is None or bone_metastases_count is None:
            result['warnings'].append(
                "Brak pełnych danych do oceny wysokiego ryzyka - upewnij się, że pacjent nie spełnia kryteriów C.87.a"
            )

        result['eligible'] = True
        result['indication'] = (
            "mCSPC niespełniający kryteriów wysokiego ryzyka C.87.a, "
            "w połączeniu z ADT (samodzielnie lub z 18-tyg. docetakselem)"
        )
        result['indication_en'] = (
            "mCSPC not meeting C.87.a high-risk criteria, "
            "with ADT alone or with 18-week docetaxel"
        )
        result['attachment'] = "C.87.b"
        result['criteria_met'] = [
            "Wrażliwy na kastrację",
            "Przerzuty obecne",
            f"Nie spełnia kryteriów wysokiego ryzyka C.87.a ({high_risk_factors}/3 czynników)"
        ]
        result['treatment_options'] = [
            "ADT + abirateron (monoterapia)",
            "ADT + abirateron + docetaksel (18 tyg.)"
        ]
        return result

    # --- C.87.b.2: nmCRPC high risk of metastasis ---
    if disease_state == "nmcrpc":
        if has_metastases:
            result['criteria_not_met'].append("Przerzuty obecne (wymagany nmCRPC bez przerzutów)")
            return result

        if not castration_resistant:
            result['criteria_not_met'].append("Rak wrażliwy na kastrację (wymagany CRPC)")
            return result

        if psadt_months is None:
            result['criteria_not_met'].append("Brak danych o PSA DT (wymagane PSA DT ≤10 mies.)")
            return result

        if psadt_months > 10:
            result['criteria_not_met'].append(
                f"PSA DT >10 miesięcy ({psadt_months:.1f} mies.) - wymagane ≤10 mies."
            )
            result['warnings'].append(
                "Duże ryzyko przerzutów definiowane jako PSA DT ≤10 miesięcy"
            )
            return result

        result['eligible'] = True
        result['indication'] = "nmCRPC z dużym ryzykiem przerzutów (PSA DT ≤10 mies.)"
        result['indication_en'] = "nmCRPC with high risk of metastasis (PSADT ≤10 months)"
        result['attachment'] = "C.87.b"
        result['criteria_met'] = [
            "Oporny na kastrację",
            "Bez przerzutów (M0)",
            f"PSA DT ≤10 miesięcy ({psadt_months:.1f} mies.) - duże ryzyko przerzutów"
        ]
        return result

    # --- C.87.b.3: Adjuvant after radical RT (high-risk) ---
    if disease_state == "adjuvant_post_rt":
        if not after_radical_rt:
            result['criteria_not_met'].append("Brak radioterapii radykalnej w wywiadzie")
            return result

        # Consistency checks for adjuvant setting
        if has_metastases:
            result['warnings'].append(
                "UWAGA: Wskazano przerzuty (has_metastases=True), "
                "ale leczenie adjuwantowe dotyczy zwykle choroby miejscowej po RT"
            )
        if castration_resistant:
            result['warnings'].append(
                "UWAGA: Wskazano oporność na kastrację (castration_resistant=True), "
                "ale leczenie adjuwantowe dotyczy zwykle choroby hormonowrażliwej"
            )

        # Check high-risk criteria for adjuvant setting
        # Option A: N+ (lymph node involvement)
        if n_positive is True:
            result['eligible'] = True
            result['indication'] = (
                "Uzupełniająca hormonoterapia po RT radykalnej - "
                "grupa wysokiego ryzyka (N+)"
            )
            result['indication_en'] = "Adjuvant after radical RT - high-risk (N+)"
            result['attachment'] = "C.87.b"
            result['criteria_met'] = [
                "Po radioterapii radykalnej",
                "Przerzuty w węzłach chłonnych (N+)"
            ]
            result['max_duration'] = "24 miesiące (2 lata)"
            result['warnings'].append(
                "Maksymalny czas leczenia: 2 lata w skojarzeniu z ADT"
            )
            return result

        # Option B: N- AND ≥2 of 3 factors (T3-4, Gleason 8-10, PSA ≥40)
        if n_positive is False:
            risk_factors = 0
            risk_details = []

            # Factor 1: T3-4
            if t_stage is not None:
                t_upper = t_stage.upper().replace("C", "").replace("P", "")
                if t_upper in ["T3", "T3A", "T3B", "T4"]:
                    risk_factors += 1
                    risk_details.append(f"Cecha T3-4 ({t_stage})")

            # Factor 2: Gleason 8-10
            if gleason_score is not None and gleason_score >= 8:
                risk_factors += 1
                risk_details.append(f"Gleason 8-10 ({gleason_score})")

            # Factor 3: PSA ≥40
            if psa_at_diagnosis is not None and psa_at_diagnosis >= 40:
                risk_factors += 1
                risk_details.append(f"PSA ≥40 ng/mL ({psa_at_diagnosis:.1f})")

            if risk_factors >= 2:
                result['eligible'] = True
                result['indication'] = (
                    "Uzupełniająca hormonoterapia po RT radykalnej - "
                    "grupa wysokiego ryzyka (N-, ≥2 czynniki ryzyka)"
                )
                result['indication_en'] = "Adjuvant after radical RT - high-risk (N-, ≥2 risk factors)"
                result['attachment'] = "C.87.b"
                result['criteria_met'] = [
                    "Po radioterapii radykalnej",
                    "Brak przerzutów w węzłach chłonnych (N-)",
                    f"≥2 z 3 czynników ryzyka spełnione ({risk_factors}/3)"
                ] + risk_details
                result['max_duration'] = "24 miesiące (2 lata)"
                result['warnings'].append(
                    "Maksymalny czas leczenia: 2 lata w skojarzeniu z ADT"
                )
                return result
            else:
                result['criteria_not_met'].append(
                    f"N- wymaga ≥2 z 3 czynników: T3-4, Gleason 8-10, PSA ≥40 "
                    f"(spełnione: {risk_factors}/3)"
                )
                if risk_details:
                    result['criteria_met'] = risk_details
                return result

        # N status unknown
        result['criteria_not_met'].append(
            "Brak danych o statusie węzłów chłonnych (N) - wymagane dla oceny kwalifikacji"
        )
        return result

    # =========================================================================
    # UNKNOWN DISEASE STATE
    # =========================================================================

    result['criteria_not_met'].append(
        f"Nierozpoznany stan choroby: '{disease_state}'. "
        f"Dozwolone (bez rozróżnienia wielkości liter): mhspc, mcspc, nmcrpc, mcrpc, adjuvant_post_rt"
    )
    return result


def format_abiraterone_eligibility_pl(result: Dict[str, Any]) -> str:
    """
    Format abiraterone eligibility result as a Polish-language summary.
    """
    lines = []

    if result.get('exclusion_reason'):
        lines.append("❌ WYKLUCZENIE Z PROGRAMU LEKOWEGO")
        lines.append("-" * 40)
        for excl in result.get('exclusions', []):
            lines.append(f"  • {excl}")
        return "\n".join(lines)

    if result.get('eligible'):
        lines.append("✅ KWALIFIKUJE SIĘ DO PROGRAMU LEKOWEGO")
    else:
        lines.append("❌ NIE KWALIFIKUJE SIĘ DO PROGRAMU LEKOWEGO")

    lines.append("-" * 40)

    if result.get('indication'):
        lines.append(f"Wskazanie: {result['indication']}")

    if result.get('attachment'):
        lines.append(f"Załącznik: {result['attachment']}")

    if result.get('criteria_met'):
        lines.append("\nSpełnione kryteria:")
        for c in result['criteria_met']:
            lines.append(f"  ✓ {c}")

    if result.get('criteria_not_met'):
        lines.append("\nNiespełnione kryteria:")
        for c in result['criteria_not_met']:
            lines.append(f"  ✗ {c}")

    if result.get('warnings'):
        lines.append("\nUwagi:")
        for w in result['warnings']:
            lines.append(f"  ⚠ {w}")

    if result.get('alternative'):
        lines.append(f"\nAlternatywa: {result['alternative']}")

    if result.get('treatment_options'):
        lines.append("\nOpcje leczenia:")
        for opt in result['treatment_options']:
            lines.append(f"  • {opt}")

    if result.get('max_duration'):
        lines.append(f"\nMaksymalny czas leczenia: {result['max_duration']}")

    return "\n".join(lines)


# =============================================================================
# POLISH B.56 PROGRAMME - PROSTATE CANCER DRUG ELIGIBILITY
# =============================================================================

# HRR genes accepted for talazoparib+enzalutamide
HRR_GENES = {"BRCA1", "BRCA2", "ATM", "CDK12", "CHEK2", "PALB2", "RAD51C"}

# Drug dosing reference
B56_DRUG_DOSING = {
    "apalutamide": {"dose": "240 mg", "frequency": "once daily", "with_food": False},
    "darolutamide": {"dose": "600 mg BID (1200 mg/day)", "frequency": "twice daily", "with_food": True},
    "enzalutamide": {"dose": "160 mg", "frequency": "once daily", "with_food": False},
    "olaparib": {"dose": "300 mg BID (600 mg/day)", "frequency": "twice daily", "with_food": False},
    "niraparib_abiraterone": {"dose": "200 mg nira + 1000 mg abi + prednisone 10 mg", "frequency": "once daily", "with_food": False, "note": "MUST use combination tablet"},
    "talazoparib_enzalutamide": {"dose": "0.5 mg tala + 160 mg enza", "frequency": "once daily", "with_food": False},
}


def check_b56_general_criteria(
    histology_confirmed: bool = True,
    age: int = 18,
    ecog: int = 0,
    has_other_malignancy: bool = False,
    has_neuroendocrine: bool = False
) -> Dict[str, Any]:
    """
    Check general B.56 programme criteria that apply to all drugs.

    Returns dict with 'eligible' and 'criteria_not_met' if any general criterion fails.
    """
    issues = []

    if not histology_confirmed:
        issues.append("Wymagane histologiczne potwierdzenie gruczolakoraka stercza")

    if age < 18:
        issues.append(f"Wiek <18 lat ({age})")

    if has_other_malignancy:
        issues.append("Niekontrolowany inny nowotwór złośliwy")

    if has_neuroendocrine:
        issues.append("Rak neuroendokrynny/drobnokomórkowy/przewodowy (wyklucza z programu)")

    return {
        'eligible': len(issues) == 0,
        'criteria_not_met': issues,
        'ecog': ecog
    }


def check_apalutamide_eligibility(
    disease_state: str,  # "mHSPC" or "nmCRPC"
    # General criteria
    ecog: int = 0,
    histology_confirmed: bool = True,
    age: int = 18,
    has_other_malignancy: bool = False,
    has_neuroendocrine: bool = False,
    # Disease-specific
    has_metastases: bool = False,
    testosterone_ng_dl: Optional[float] = None,
    psadt_months: Optional[float] = None,
    psa_value: Optional[float] = None,
    # Prior treatment
    prior_abiraterone: bool = False,
    prior_adt_months_metastatic: Optional[float] = None,
    docetaxel_status: str = "not_applicable",  # "completed", "not_indicated", "not_applicable"
    bone_modifying_agents: bool = False,
    bone_modifying_for_osteoporosis: bool = False,
    # Safety
    seizure_history: bool = False,
    seizure_risk_factors: bool = False
) -> Dict[str, Any]:
    """
    Check eligibility for Apalutamide under B.56 programme.

    Args:
        disease_state: "mHSPC" or "nmCRPC"
        ecog: ECOG performance status (0-4)
        testosterone_ng_dl: Serum testosterone in ng/dL (required for nmCRPC)
        psadt_months: PSA doubling time in months (required for nmCRPC)
        prior_adt_months_metastatic: Months of ADT for metastatic disease (max 6 for mHSPC)
        docetaxel_status: For mHSPC - "completed", "not_indicated" (with rationale), or "not_applicable"
    """
    result = {
        'eligible': False,
        'drug': 'Apalutamide',
        'drug_pl': 'Apalutamid',
        'indication': None,
        'criteria_met': [],
        'criteria_not_met': [],
        'warnings': [],
        'dosing': B56_DRUG_DOSING['apalutamide']
    }

    # Check general criteria
    general = check_b56_general_criteria(histology_confirmed, age, ecog, has_other_malignancy, has_neuroendocrine)
    if not general['eligible']:
        result['criteria_not_met'].extend(general['criteria_not_met'])
        return result

    disease_state = disease_state.lower().strip()

    # Global exclusions
    if prior_abiraterone:
        result['criteria_not_met'].append("Wcześniejsze leczenie abirateronem")
        return result

    if seizure_history or seizure_risk_factors:
        result['criteria_not_met'].append("Drgawki w wywiadzie lub czynniki ryzyka drgawek")
        return result

    if bone_modifying_agents and not bone_modifying_for_osteoporosis:
        result['criteria_not_met'].append("Stosowanie leków modyfikujących metabolizm kości (z wyjątkiem osteoporozy)")
        return result

    # =========================================================================
    # mHSPC
    # =========================================================================
    if disease_state == "mhspc":
        if ecog > 2:
            result['criteria_not_met'].append(f"ECOG {ecog} > 2 (wymagane ECOG 0-2 dla mHSPC)")
            return result

        if not has_metastases:
            result['criteria_not_met'].append("Brak potwierdzonych przerzutów")
            return result

        if prior_adt_months_metastatic is not None and prior_adt_months_metastatic > 6:
            result['criteria_not_met'].append(
                f"ADT dla choroby przerzutowej >{prior_adt_months_metastatic:.1f} mies. (max 6 mies.)"
            )
            return result

        if docetaxel_status not in ["completed", "not_indicated"]:
            result['criteria_not_met'].append(
                "Wymagane: docetaksel ukończony LUB udokumentowana decyzja o pominięciu"
            )
            result['warnings'].append(
                "Podaj docetaxel_status='completed' lub 'not_indicated' z uzasadnieniem"
            )
            return result

        result['eligible'] = True
        result['indication'] = "mHSPC (przerzutowy hormonowrażliwy rak stercza)"
        result['criteria_met'] = [
            f"ECOG {ecog} (0-2)",
            "Potwierdzone przerzuty",
            "Hormonowrażliwy"
        ]
        if prior_adt_months_metastatic is not None:
            result['criteria_met'].append(f"ADT dla mets ≤6 mies. ({prior_adt_months_metastatic:.1f})")
        if docetaxel_status == "completed":
            result['criteria_met'].append("Docetaksel ukończony")
        elif docetaxel_status == "not_indicated":
            result['criteria_met'].append("Docetaksel niestosowany (udokumentowana decyzja)")

        return result

    # =========================================================================
    # nmCRPC
    # =========================================================================
    if disease_state == "nmcrpc":
        if ecog > 1:
            result['criteria_not_met'].append(f"ECOG {ecog} > 1 (wymagane ECOG 0-1 dla nmCRPC)")
            return result

        if has_metastases:
            result['criteria_not_met'].append("Przerzuty obecne (wymagany M0 dla nmCRPC)")
            return result

        # Castration verification
        if testosterone_ng_dl is None:
            result['criteria_not_met'].append("Brak pomiaru testosteronu")
            return result
        if testosterone_ng_dl > 50:
            result['criteria_not_met'].append(
                f"Testosteron {testosterone_ng_dl:.1f} ng/dL > 50 ng/dL (brak kastracji)"
            )
            return result

        # PSADT requirement
        if psadt_months is None:
            result['criteria_not_met'].append("Brak PSA DT (wymagane ≤10 mies.)")
            return result
        if psadt_months > 10:
            result['criteria_not_met'].append(
                f"PSA DT {psadt_months:.1f} mies. > 10 mies."
            )
            return result

        # PSA progression (simplified - assume validated if PSA provided)
        if psa_value is not None and psa_value <= 2:
            result['criteria_not_met'].append(f"PSA {psa_value:.2f} ≤ 2 ng/mL")
            return result

        result['eligible'] = True
        result['indication'] = "nmCRPC (nieprzerzutowy oporny na kastrację rak stercza)"
        result['criteria_met'] = [
            f"ECOG {ecog} (0-1)",
            "M0 (bez przerzutów)",
            f"Testosteron ≤50 ng/dL ({testosterone_ng_dl:.1f})",
            f"PSA DT ≤10 mies. ({psadt_months:.1f})"
        ]
        if psa_value is not None:
            result['criteria_met'].append(f"PSA > 2 ng/mL ({psa_value:.2f})")

        return result

    result['criteria_not_met'].append(
        f"Nierozpoznany stan choroby: '{disease_state}'. Dozwolone: mHSPC, nmCRPC"
    )
    return result


def check_darolutamide_eligibility(
    disease_state: str,  # "mHSPC" or "nmCRPC"
    # General criteria
    ecog: int = 0,
    histology_confirmed: bool = True,
    age: int = 18,
    has_other_malignancy: bool = False,
    has_neuroendocrine: bool = False,
    # Disease-specific
    has_metastases: bool = False,
    testosterone_ng_dl: Optional[float] = None,
    psadt_months: Optional[float] = None,
    psa_value: Optional[float] = None,
    # Prior treatment
    prior_abiraterone: bool = False,
    prior_adt_months_metastatic: Optional[float] = None,
    bone_modifying_agents: bool = False,
    bone_modifying_for_osteoporosis: bool = False,
    # Docetaxel (required for mHSPC)
    can_receive_docetaxel: bool = True
) -> Dict[str, Any]:
    """
    Check eligibility for Darolutamide under B.56 programme.

    Note: In mHSPC, darolutamide REQUIRES docetaxel combination.
    """
    result = {
        'eligible': False,
        'drug': 'Darolutamide',
        'drug_pl': 'Darolutamid',
        'indication': None,
        'criteria_met': [],
        'criteria_not_met': [],
        'warnings': [],
        'dosing': B56_DRUG_DOSING['darolutamide']
    }

    # Check general criteria
    general = check_b56_general_criteria(histology_confirmed, age, ecog, has_other_malignancy, has_neuroendocrine)
    if not general['eligible']:
        result['criteria_not_met'].extend(general['criteria_not_met'])
        return result

    disease_state = disease_state.lower().strip()

    # Global exclusions
    if prior_abiraterone:
        result['criteria_not_met'].append("Wcześniejsze leczenie abirateronem")
        return result

    if bone_modifying_agents and not bone_modifying_for_osteoporosis:
        result['criteria_not_met'].append("Stosowanie leków modyfikujących metabolizm kości (z wyjątkiem osteoporozy)")
        return result

    # =========================================================================
    # mHSPC (requires docetaxel)
    # =========================================================================
    if disease_state == "mhspc":
        if ecog > 2:
            result['criteria_not_met'].append(f"ECOG {ecog} > 2 (wymagane ECOG 0-2 dla mHSPC)")
            return result

        if not has_metastases:
            result['criteria_not_met'].append("Brak potwierdzonych przerzutów")
            return result

        if not can_receive_docetaxel:
            result['criteria_not_met'].append(
                "Darolutamid w mHSPC wymaga leczenia skojarzonego z docetakselem"
            )
            result['warnings'].append("Rozważ apalutamid lub enzalutamid jako alternatywę")
            return result

        if prior_adt_months_metastatic is not None and prior_adt_months_metastatic > 6:
            result['criteria_not_met'].append(
                f"ADT dla choroby przerzutowej >{prior_adt_months_metastatic:.1f} mies. (max 6 mies.)"
            )
            return result

        result['eligible'] = True
        result['indication'] = "mHSPC (przerzutowy hormonowrażliwy) + docetaksel"
        result['criteria_met'] = [
            f"ECOG {ecog} (0-2)",
            "Potwierdzone przerzuty",
            "Hormonowrażliwy",
            "Kwalifikuje się do docetakselu"
        ]
        result['treatment_protocol'] = [
            "Rozpocznij darolutamid",
            "Pierwszy cykl docetakselu w ciągu 6 tygodni",
            "Plan: 6 cykli docetakselu",
            "Kontynuuj darolutamid nawet przy przerwaniu docetakselu"
        ]
        if prior_adt_months_metastatic is not None:
            result['criteria_met'].append(f"ADT dla mets ≤6 mies. ({prior_adt_months_metastatic:.1f})")

        return result

    # =========================================================================
    # nmCRPC
    # =========================================================================
    if disease_state == "nmcrpc":
        if ecog > 1:
            result['criteria_not_met'].append(f"ECOG {ecog} > 1 (wymagane ECOG 0-1 dla nmCRPC)")
            return result

        if has_metastases:
            result['criteria_not_met'].append("Przerzuty obecne (wymagany M0 dla nmCRPC)")
            return result

        if testosterone_ng_dl is None:
            result['criteria_not_met'].append("Brak pomiaru testosteronu")
            return result
        if testosterone_ng_dl > 50:
            result['criteria_not_met'].append(
                f"Testosteron {testosterone_ng_dl:.1f} ng/dL > 50 ng/dL"
            )
            return result

        if psadt_months is None:
            result['criteria_not_met'].append("Brak PSA DT (wymagane ≤10 mies.)")
            return result
        if psadt_months > 10:
            result['criteria_not_met'].append(f"PSA DT {psadt_months:.1f} mies. > 10 mies.")
            return result

        if psa_value is not None and psa_value <= 2:
            result['criteria_not_met'].append(f"PSA {psa_value:.2f} ≤ 2 ng/mL")
            return result

        result['eligible'] = True
        result['indication'] = "nmCRPC (nieprzerzutowy oporny na kastrację)"
        result['criteria_met'] = [
            f"ECOG {ecog} (0-1)",
            "M0 (bez przerzutów)",
            f"Testosteron ≤50 ng/dL ({testosterone_ng_dl:.1f})",
            f"PSA DT ≤10 mies. ({psadt_months:.1f})"
        ]

        return result

    result['criteria_not_met'].append(
        f"Nierozpoznany stan choroby: '{disease_state}'. Dozwolone: mHSPC, nmCRPC"
    )
    return result


def check_enzalutamide_eligibility(
    disease_state: str,  # "mHSPC", "nmCRPC", "mCRPC_pre", "mCRPC_post"
    # General criteria
    ecog: int = 0,
    histology_confirmed: bool = True,
    age: int = 18,
    has_other_malignancy: bool = False,
    has_neuroendocrine: bool = False,
    # Disease-specific
    has_metastases: bool = False,
    testosterone_ng_dl: Optional[float] = None,
    psadt_months: Optional[float] = None,
    psa_value: Optional[float] = None,
    has_psa_progression: bool = False,
    has_radiological_progression: bool = False,
    # Prior treatment
    prior_abiraterone: bool = False,
    prior_adt_months_metastatic: Optional[float] = None,
    docetaxel_status: str = "not_applicable",
    bone_modifying_agents: bool = False,
    bone_modifying_for_osteoporosis: bool = False,
    # Safety
    seizure_history: bool = False,
    seizure_risk_factors: bool = False
) -> Dict[str, Any]:
    """
    Check eligibility for Enzalutamide under B.56 programme.

    Args:
        disease_state: "mHSPC", "nmCRPC", "mCRPC_pre" (pre-docetaxel), "mCRPC_post" (post-docetaxel)
    """
    result = {
        'eligible': False,
        'drug': 'Enzalutamide',
        'drug_pl': 'Enzalutamid',
        'indication': None,
        'criteria_met': [],
        'criteria_not_met': [],
        'warnings': [],
        'dosing': B56_DRUG_DOSING['enzalutamide']
    }

    # Check general criteria
    general = check_b56_general_criteria(histology_confirmed, age, ecog, has_other_malignancy, has_neuroendocrine)
    if not general['eligible']:
        result['criteria_not_met'].extend(general['criteria_not_met'])
        return result

    disease_state = disease_state.lower().strip()

    # Global exclusions
    if prior_abiraterone:
        result['criteria_not_met'].append("Wcześniejsze leczenie abirateronem")
        return result

    if seizure_history or seizure_risk_factors:
        result['criteria_not_met'].append("Drgawki w wywiadzie lub czynniki ryzyka drgawek")
        return result

    if bone_modifying_agents and not bone_modifying_for_osteoporosis:
        result['criteria_not_met'].append("Leki modyfikujące metabolizm kości (z wyjątkiem osteoporozy)")
        return result

    # =========================================================================
    # mHSPC
    # =========================================================================
    if disease_state == "mhspc":
        if ecog > 2:
            result['criteria_not_met'].append(f"ECOG {ecog} > 2")
            return result

        if not has_metastases:
            result['criteria_not_met'].append("Brak przerzutów")
            return result

        if prior_adt_months_metastatic is not None and prior_adt_months_metastatic > 6:
            result['criteria_not_met'].append(
                f"ADT dla mets >{prior_adt_months_metastatic:.1f} mies. (max 6)"
            )
            return result

        result['eligible'] = True
        result['indication'] = "mHSPC (przerzutowy hormonowrażliwy)"
        result['criteria_met'] = [
            f"ECOG {ecog} (0-2)",
            "Potwierdzone przerzuty"
        ]
        return result

    # =========================================================================
    # nmCRPC
    # =========================================================================
    if disease_state == "nmcrpc":
        if ecog > 1:
            result['criteria_not_met'].append(f"ECOG {ecog} > 1")
            return result

        if has_metastases:
            result['criteria_not_met'].append("Przerzuty obecne (wymagany M0)")
            return result

        # Testosterone measurement required
        if testosterone_ng_dl is None:
            result['criteria_not_met'].append("Brak pomiaru testosteronu (wymagane ≤50 ng/dL)")
            return result
        if testosterone_ng_dl > 50:
            result['criteria_not_met'].append(f"Testosteron {testosterone_ng_dl:.1f} > 50 ng/dL")
            return result

        # PSADT required
        if psadt_months is None:
            result['criteria_not_met'].append("Brak PSA DT (wymagane ≤10 mies.)")
            return result
        if psadt_months > 10:
            result['criteria_not_met'].append(f"PSA DT {psadt_months:.1f} > 10 mies.")
            return result

        # PSA >2 check (if provided)
        if psa_value is not None and psa_value <= 2:
            result['criteria_not_met'].append(f"PSA {psa_value:.2f} ≤ 2 ng/mL (wymagane >2)")
            return result

        result['eligible'] = True
        result['indication'] = "nmCRPC (nieprzerzutowy oporny na kastrację)"
        result['criteria_met'] = [
            f"ECOG {ecog} (0-1)",
            "M0",
            f"Testosteron ≤50 ng/dL ({testosterone_ng_dl:.1f})",
            f"PSA DT ≤10 mies. ({psadt_months:.1f})"
        ]
        if psa_value is not None:
            result['criteria_met'].append(f"PSA > 2 ng/mL ({psa_value:.2f})")
        return result

    # =========================================================================
    # mCRPC pre-docetaxel
    # =========================================================================
    if disease_state in ["mcrpc_pre", "mcrpc pre", "mcrpc"]:
        if ecog > 1:
            result['criteria_not_met'].append(f"ECOG {ecog} > 1 (pre-docetaxel wymaga ECOG 0-1)")
            return result

        if not has_metastases:
            result['criteria_not_met'].append("Brak przerzutów (wymagane dla mCRPC)")
            return result

        if testosterone_ng_dl is not None and testosterone_ng_dl > 50:
            result['criteria_not_met'].append(f"Testosteron {testosterone_ng_dl:.1f} > 50 ng/dL")
            return result

        if not has_psa_progression and not has_radiological_progression:
            result['criteria_not_met'].append("Brak progresji PSA ani radiologicznej")
            return result

        result['eligible'] = True
        result['indication'] = "mCRPC przed chemioterapią"
        result['criteria_met'] = [
            f"ECOG {ecog} (0-1)",
            "Przerzuty obecne",
            "Oporny na kastrację"
        ]
        if has_psa_progression:
            result['criteria_met'].append("Progresja PSA")
        if has_radiological_progression:
            result['criteria_met'].append("Progresja radiologiczna")
        return result

    # =========================================================================
    # mCRPC post-docetaxel
    # =========================================================================
    if disease_state in ["mcrpc_post", "mcrpc post"]:
        if ecog > 2:
            result['criteria_not_met'].append(f"ECOG {ecog} > 2")
            return result

        if not has_metastases:
            result['criteria_not_met'].append("Brak przerzutów")
            return result

        if testosterone_ng_dl is not None and testosterone_ng_dl > 50:
            result['criteria_not_met'].append(f"Testosteron {testosterone_ng_dl:.1f} > 50 ng/dL")
            return result

        if not has_psa_progression and not has_radiological_progression:
            result['criteria_not_met'].append("Brak progresji")
            return result

        result['eligible'] = True
        result['indication'] = "mCRPC po docetakselu"
        result['criteria_met'] = [
            f"ECOG {ecog} (0-2)",
            "Przerzuty obecne",
            "Po docetakselu"
        ]
        return result

    result['criteria_not_met'].append(
        f"Nierozpoznany stan: '{disease_state}'. Dozwolone: mHSPC, nmCRPC, mCRPC_pre, mCRPC_post"
    )
    return result


def check_olaparib_eligibility(
    # General criteria
    ecog: int = 0,
    histology_confirmed: bool = True,
    age: int = 18,
    has_other_malignancy: bool = False,
    has_neuroendocrine: bool = False,
    # Disease-specific
    has_metastases: bool = False,
    testosterone_ng_dl: Optional[float] = None,
    has_psa_progression: bool = False,
    has_radiological_progression: bool = False,
    # Mutation status
    brca_mutation: Optional[str] = None,  # "BRCA1", "BRCA2", or None
    mutation_type: str = "unknown",  # "germline", "somatic", "unknown"
    # Prior treatment
    progressed_on_hormonal_therapy: bool = False,
    prior_docetaxel: bool = False,
    prior_cabazitaxel: bool = False,
    # Renal function
    crcl_ml_min: Optional[float] = None
) -> Dict[str, Any]:
    """
    Check eligibility for Olaparib under B.56 programme.

    Olaparib is for mCRPC with BRCA1/2 mutation after progression on hormonal therapy.
    """
    result = {
        'eligible': False,
        'drug': 'Olaparib',
        'drug_pl': 'Olaparib',
        'indication': None,
        'criteria_met': [],
        'criteria_not_met': [],
        'warnings': [],
        'dosing': B56_DRUG_DOSING['olaparib']
    }

    # Check general criteria
    general = check_b56_general_criteria(histology_confirmed, age, ecog, has_other_malignancy, has_neuroendocrine)
    if not general['eligible']:
        result['criteria_not_met'].extend(general['criteria_not_met'])
        return result

    if ecog > 2:
        result['criteria_not_met'].append(f"ECOG {ecog} > 2")
        return result

    # Must be mCRPC
    if not has_metastases:
        result['criteria_not_met'].append("Brak przerzutów (wymagane mCRPC)")
        return result

    if testosterone_ng_dl is not None and testosterone_ng_dl > 50:
        result['criteria_not_met'].append(f"Testosteron {testosterone_ng_dl:.1f} > 50 ng/dL")
        return result

    if not has_psa_progression and not has_radiological_progression:
        result['criteria_not_met'].append("Brak progresji PSA ani radiologicznej")
        return result

    # BRCA mutation required
    if brca_mutation not in ["BRCA1", "BRCA2"]:
        result['criteria_not_met'].append(
            "Wymagana mutacja BRCA1 lub BRCA2 (patogenna/prawdopodobnie patogenna)"
        )
        return result

    # Must have progressed on hormonal therapy
    if not progressed_on_hormonal_therapy:
        result['criteria_not_met'].append(
            "Wymagana progresja po nowej generacji terapii hormonalnej"
        )
        return result

    # Renal function check (REQUIRED for PARP inhibitors)
    if crcl_ml_min is None:
        result['criteria_not_met'].append("Brak wyliczenia CrCl (wymagane >30 mL/min)")
        return result
    if crcl_ml_min <= 30:
        result['criteria_not_met'].append(
            f"CrCl {crcl_ml_min:.0f} mL/min ≤30 (przeciwwskazanie)"
        )
        return result
    elif crcl_ml_min <= 50:
        result['warnings'].append(
            f"CrCl {crcl_ml_min:.0f} mL/min (31-50) - wymagana redukcja dawki per ChPL"
        )

    result['eligible'] = True
    result['indication'] = "mCRPC z mutacją BRCA po progresji na terapii hormonalnej"
    result['criteria_met'] = [
        f"ECOG {ecog} (0-2)",
        "mCRPC (przerzuty + oporność na kastrację)",
        f"Mutacja {brca_mutation} ({mutation_type})",
        "Progresja po nowej generacji terapii hormonalnej"
    ]
    if prior_docetaxel:
        result['criteria_met'].append("Po docetakselu")
    if prior_cabazitaxel:
        result['criteria_met'].append("Po kabazytakselu")
    if crcl_ml_min is not None and crcl_ml_min > 50:
        result['criteria_met'].append(f"CrCl {crcl_ml_min:.0f} mL/min (>50)")

    return result


def check_niraparib_abiraterone_eligibility(
    # General criteria
    ecog: int = 0,
    histology_confirmed: bool = True,
    age: int = 18,
    has_other_malignancy: bool = False,
    has_neuroendocrine: bool = False,
    # Disease-specific
    has_metastases: bool = False,
    testosterone_ng_dl: Optional[float] = None,
    has_psa_progression: bool = False,
    has_radiological_progression: bool = False,
    # Mutation status
    brca_mutation: Optional[str] = None,  # "BRCA1", "BRCA2", or None
    mutation_type: str = "unknown",
    # Prior treatment
    prior_abiraterone: bool = False,
    abiraterone_months: Optional[float] = None,  # If prior, how many months
    abiraterone_progression: bool = False,  # If prior, did progression occur?
    prior_parp_inhibitor: bool = False,
    prior_nonsteroidal_antiandrogen: bool = False,
    chemotherapy_indicated: bool = False,
    # Renal function
    crcl_ml_min: Optional[float] = None
) -> Dict[str, Any]:
    """
    Check eligibility for Niraparib + Abiraterone under B.56 programme.

    For mCRPC with BRCA1/2 mutation in 1st line (no chemo indication).
    """
    result = {
        'eligible': False,
        'drug': 'Niraparib + Abiraterone',
        'drug_pl': 'Niraparib + Abirateron',
        'indication': None,
        'criteria_met': [],
        'criteria_not_met': [],
        'warnings': [],
        'dosing': B56_DRUG_DOSING['niraparib_abiraterone']
    }

    # Check general criteria
    general = check_b56_general_criteria(histology_confirmed, age, ecog, has_other_malignancy, has_neuroendocrine)
    if not general['eligible']:
        result['criteria_not_met'].extend(general['criteria_not_met'])
        return result

    if ecog > 2:
        result['criteria_not_met'].append(f"ECOG {ecog} > 2")
        return result

    # Must be mCRPC
    if not has_metastases:
        result['criteria_not_met'].append("Brak przerzutów (wymagane mCRPC)")
        return result

    if testosterone_ng_dl is not None and testosterone_ng_dl > 50:
        result['criteria_not_met'].append(f"Testosteron {testosterone_ng_dl:.1f} > 50 ng/dL")
        return result

    if not has_psa_progression and not has_radiological_progression:
        result['criteria_not_met'].append("Brak progresji")
        return result

    # BRCA mutation required
    if brca_mutation not in ["BRCA1", "BRCA2"]:
        result['criteria_not_met'].append("Wymagana mutacja BRCA1 lub BRCA2")
        return result

    # No chemotherapy indication
    if chemotherapy_indicated:
        result['criteria_not_met'].append(
            "Chemioterapia jest wskazana (niraparib+abi dla 1. linii bez wskazań do CHT)"
        )
        return result

    # Prior treatment exclusions
    if prior_parp_inhibitor:
        result['criteria_not_met'].append("Wcześniejsze leczenie inhibitorem PARP")
        return result

    if prior_nonsteroidal_antiandrogen:
        result['criteria_not_met'].append("Wcześniejsze leczenie niesteroidowym antyandrogenem")
        return result

    # Abiraterone exception logic
    if prior_abiraterone:
        if abiraterone_months is not None and abiraterone_months > 4:
            result['criteria_not_met'].append(
                f"Abirateron stosowany >{abiraterone_months:.1f} mies. (max 4 mies. dla wyjątku)"
            )
            return result
        if abiraterone_progression:
            result['criteria_not_met'].append(
                "Progresja w trakcie abirateronu (wyklucza wyjątek)"
            )
            return result
        result['warnings'].append(
            "Wyjątek: abirateron rozpoczęty <4 mies. temu bez progresji - może kontynuować"
        )

    # Renal function check (REQUIRED for PARP inhibitors)
    if crcl_ml_min is None:
        result['criteria_not_met'].append("Brak wyliczenia CrCl (wymagane >30 mL/min)")
        return result
    if crcl_ml_min <= 30:
        result['criteria_not_met'].append(f"CrCl {crcl_ml_min:.0f} mL/min ≤30 (przeciwwskazanie)")
        return result
    elif crcl_ml_min <= 50:
        result['warnings'].append(f"CrCl {crcl_ml_min:.0f} mL/min - redukcja dawki")

    result['eligible'] = True
    result['indication'] = "mCRPC z mutacją BRCA, 1. linia (bez wskazań do CHT)"
    result['criteria_met'] = [
        f"ECOG {ecog} (0-2)",
        "mCRPC",
        f"Mutacja {brca_mutation}",
        "Brak wskazań do chemioterapii w 1. linii",
        "Bez wcześniejszego inhibitora PARP",
        "Bez wcześniejszego niesteroidowego antyandrogenu"
    ]
    result['warnings'].append("UWAGA: Stosować WYŁĄCZNIE tabletkę złożoną niraparib+abirateron")

    return result


def check_talazoparib_enzalutamide_eligibility(
    # General criteria
    ecog: int = 0,
    histology_confirmed: bool = True,
    age: int = 18,
    has_other_malignancy: bool = False,
    has_neuroendocrine: bool = False,
    # Disease-specific
    has_metastases: bool = False,
    testosterone_ng_dl: Optional[float] = None,
    has_psa_progression: bool = False,
    has_radiological_progression: bool = False,
    # Mutation status
    hrr_mutations: Optional[List[str]] = None,  # List of mutated HRR genes
    mutation_type: str = "unknown",
    # Prior treatment
    prior_abiraterone: bool = False,
    prior_parp_inhibitor: bool = False,
    prior_nonsteroidal_antiandrogen: bool = False,
    chemotherapy_indicated: bool = False,
    # Renal function
    crcl_ml_min: Optional[float] = None
) -> Dict[str, Any]:
    """
    Check eligibility for Talazoparib + Enzalutamide under B.56 programme.

    For mCRPC with HRR gene mutations in 1st line (no chemo indication).
    """
    result = {
        'eligible': False,
        'drug': 'Talazoparib + Enzalutamide',
        'drug_pl': 'Talazoparib + Enzalutamid',
        'indication': None,
        'criteria_met': [],
        'criteria_not_met': [],
        'warnings': [],
        'dosing': B56_DRUG_DOSING['talazoparib_enzalutamide']
    }

    # Check general criteria
    general = check_b56_general_criteria(histology_confirmed, age, ecog, has_other_malignancy, has_neuroendocrine)
    if not general['eligible']:
        result['criteria_not_met'].extend(general['criteria_not_met'])
        return result

    if ecog > 2:
        result['criteria_not_met'].append(f"ECOG {ecog} > 2")
        return result

    # Must be mCRPC
    if not has_metastases:
        result['criteria_not_met'].append("Brak przerzutów (wymagane mCRPC)")
        return result

    if testosterone_ng_dl is not None and testosterone_ng_dl > 50:
        result['criteria_not_met'].append(f"Testosteron {testosterone_ng_dl:.1f} > 50 ng/dL")
        return result

    if not has_psa_progression and not has_radiological_progression:
        result['criteria_not_met'].append("Brak progresji")
        return result

    # HRR mutation required
    if not hrr_mutations:
        result['criteria_not_met'].append(
            f"Wymagana mutacja HRR: {', '.join(sorted(HRR_GENES))}"
        )
        return result

    valid_mutations = [m for m in hrr_mutations if m.upper() in HRR_GENES]
    if not valid_mutations:
        result['criteria_not_met'].append(
            f"Brak uznawanej mutacji HRR. Podane: {hrr_mutations}. "
            f"Akceptowane: {', '.join(sorted(HRR_GENES))}"
        )
        return result

    # No chemotherapy indication
    if chemotherapy_indicated:
        result['criteria_not_met'].append("Chemioterapia wskazana (tala+enza dla 1. linii bez CHT)")
        return result

    # Prior treatment exclusions
    if prior_abiraterone:
        result['criteria_not_met'].append("Wcześniejszy abirateron")
        return result

    if prior_parp_inhibitor:
        result['criteria_not_met'].append("Wcześniejszy inhibitor PARP")
        return result

    if prior_nonsteroidal_antiandrogen:
        result['criteria_not_met'].append("Wcześniejszy niesteroidowy antyandrogen")
        return result

    # Renal function check (REQUIRED for PARP inhibitors)
    if crcl_ml_min is None:
        result['criteria_not_met'].append("Brak wyliczenia CrCl (wymagane >30 mL/min)")
        return result
    if crcl_ml_min <= 30:
        result['criteria_not_met'].append(f"CrCl {crcl_ml_min:.0f} mL/min ≤30 (przeciwwskazanie)")
        return result
    elif crcl_ml_min <= 50:
        result['warnings'].append(f"CrCl {crcl_ml_min:.0f} mL/min - redukcja dawki talazoparib")

    result['eligible'] = True
    result['indication'] = "mCRPC z mutacją HRR, 1. linia (bez wskazań do CHT)"
    result['criteria_met'] = [
        f"ECOG {ecog} (0-2)",
        "mCRPC",
        f"Mutacja HRR: {', '.join(valid_mutations)}",
        "Brak wskazań do chemioterapii",
        "Bez wcześniejszego abirateronu/PARP/niesteroidowego antyandrogenu"
    ]

    return result


def check_b56_eligibility(
    disease_state: str,
    # Patient characteristics
    ecog: int = 0,
    age: int = 18,
    histology_confirmed: bool = True,
    has_other_malignancy: bool = False,
    has_neuroendocrine: bool = False,
    # Disease state
    has_metastases: bool = False,
    testosterone_ng_dl: Optional[float] = None,
    psadt_months: Optional[float] = None,
    psa_value: Optional[float] = None,
    has_psa_progression: bool = False,
    has_radiological_progression: bool = False,
    # Mutations
    brca_mutation: Optional[str] = None,
    hrr_mutations: Optional[List[str]] = None,
    # Prior treatments
    prior_abiraterone: bool = False,
    prior_parp_inhibitor: bool = False,
    prior_nonsteroidal_antiandrogen: bool = False,
    progressed_on_hormonal_therapy: bool = False,
    can_receive_docetaxel: bool = True,
    chemotherapy_indicated: bool = False,
    # Safety
    seizure_history: bool = False,
    crcl_ml_min: Optional[float] = None
) -> Dict[str, Any]:
    """
    Check eligibility for ALL B.56 programme drugs and return comprehensive results.

    Returns dict with eligibility status for each drug.
    """
    results = {
        'disease_state': disease_state,
        'eligible_drugs': [],
        'ineligible_drugs': [],
        'drug_results': {}
    }

    disease_state_lower = disease_state.lower().strip()

    # Check each drug based on disease state
    drugs_to_check = []

    if disease_state_lower == "mhspc":
        drugs_to_check = ["apalutamide", "darolutamide", "enzalutamide"]
    elif disease_state_lower == "nmcrpc":
        drugs_to_check = ["apalutamide", "darolutamide", "enzalutamide"]
    elif disease_state_lower in ["mcrpc_pre", "mcrpc_post"]:
        drugs_to_check = ["enzalutamide", "olaparib", "niraparib_abiraterone", "talazoparib_enzalutamide"]
    elif disease_state_lower == "mcrpc":
        # Ambiguous - require explicit pre/post specification
        results['error'] = (
            "Stan 'mCRPC' jest niejednoznaczny. Podaj 'mCRPC_pre' (przed chemioterapią) "
            "lub 'mCRPC_post' (po docetakselu) dla prawidłowej kwalifikacji."
        )
        results['hint'] = "mCRPC_pre dla ECOG 0-1, mCRPC_post dla ECOG 0-2 (po docetakselu)"
        return results
    else:
        results['error'] = f"Nierozpoznany stan choroby: {disease_state}"
        results['allowed_states'] = ["mHSPC", "nmCRPC", "mCRPC_pre", "mCRPC_post"]
        return results

    for drug in drugs_to_check:
        if drug == "apalutamide":
            r = check_apalutamide_eligibility(
                disease_state=disease_state,
                ecog=ecog, histology_confirmed=histology_confirmed, age=age,
                has_other_malignancy=has_other_malignancy, has_neuroendocrine=has_neuroendocrine,
                has_metastases=has_metastases, testosterone_ng_dl=testosterone_ng_dl,
                psadt_months=psadt_months, psa_value=psa_value,
                prior_abiraterone=prior_abiraterone,
                seizure_history=seizure_history
            )
        elif drug == "darolutamide":
            r = check_darolutamide_eligibility(
                disease_state=disease_state,
                ecog=ecog, histology_confirmed=histology_confirmed, age=age,
                has_other_malignancy=has_other_malignancy, has_neuroendocrine=has_neuroendocrine,
                has_metastases=has_metastases, testosterone_ng_dl=testosterone_ng_dl,
                psadt_months=psadt_months, psa_value=psa_value,
                prior_abiraterone=prior_abiraterone,
                can_receive_docetaxel=can_receive_docetaxel
            )
        elif drug == "enzalutamide":
            r = check_enzalutamide_eligibility(
                disease_state=disease_state,
                ecog=ecog, histology_confirmed=histology_confirmed, age=age,
                has_other_malignancy=has_other_malignancy, has_neuroendocrine=has_neuroendocrine,
                has_metastases=has_metastases, testosterone_ng_dl=testosterone_ng_dl,
                psadt_months=psadt_months, psa_value=psa_value,
                has_psa_progression=has_psa_progression,
                has_radiological_progression=has_radiological_progression,
                prior_abiraterone=prior_abiraterone,
                seizure_history=seizure_history
            )
        elif drug == "olaparib":
            r = check_olaparib_eligibility(
                ecog=ecog, histology_confirmed=histology_confirmed, age=age,
                has_other_malignancy=has_other_malignancy, has_neuroendocrine=has_neuroendocrine,
                has_metastases=has_metastases, testosterone_ng_dl=testosterone_ng_dl,
                has_psa_progression=has_psa_progression,
                has_radiological_progression=has_radiological_progression,
                brca_mutation=brca_mutation,
                progressed_on_hormonal_therapy=progressed_on_hormonal_therapy,
                crcl_ml_min=crcl_ml_min
            )
        elif drug == "niraparib_abiraterone":
            r = check_niraparib_abiraterone_eligibility(
                ecog=ecog, histology_confirmed=histology_confirmed, age=age,
                has_other_malignancy=has_other_malignancy, has_neuroendocrine=has_neuroendocrine,
                has_metastases=has_metastases, testosterone_ng_dl=testosterone_ng_dl,
                has_psa_progression=has_psa_progression,
                has_radiological_progression=has_radiological_progression,
                brca_mutation=brca_mutation,
                prior_abiraterone=prior_abiraterone,
                prior_parp_inhibitor=prior_parp_inhibitor,
                prior_nonsteroidal_antiandrogen=prior_nonsteroidal_antiandrogen,
                chemotherapy_indicated=chemotherapy_indicated,
                crcl_ml_min=crcl_ml_min
            )
        elif drug == "talazoparib_enzalutamide":
            r = check_talazoparib_enzalutamide_eligibility(
                ecog=ecog, histology_confirmed=histology_confirmed, age=age,
                has_other_malignancy=has_other_malignancy, has_neuroendocrine=has_neuroendocrine,
                has_metastases=has_metastases, testosterone_ng_dl=testosterone_ng_dl,
                has_psa_progression=has_psa_progression,
                has_radiological_progression=has_radiological_progression,
                hrr_mutations=hrr_mutations,
                prior_abiraterone=prior_abiraterone,
                prior_parp_inhibitor=prior_parp_inhibitor,
                prior_nonsteroidal_antiandrogen=prior_nonsteroidal_antiandrogen,
                chemotherapy_indicated=chemotherapy_indicated,
                crcl_ml_min=crcl_ml_min
            )
        else:
            continue

        results['drug_results'][drug] = r
        if r['eligible']:
            results['eligible_drugs'].append(r['drug_pl'])
        else:
            results['ineligible_drugs'].append(r['drug_pl'])

    return results


def format_b56_eligibility_pl(results: Dict[str, Any]) -> str:
    """
    Format B.56 eligibility results as a Polish-language summary.
    """
    lines = []

    lines.append("=" * 50)
    lines.append("PROGRAM LEKOWY B.56 - RAK STERCZA")
    lines.append("=" * 50)
    lines.append(f"\nStan choroby: {results.get('disease_state', 'nieznany').upper()}")

    if results.get('error'):
        lines.append(f"\n❌ BŁĄD: {results['error']}")
        return "\n".join(lines)

    if results.get('eligible_drugs'):
        lines.append(f"\n✅ KWALIFIKUJE SIĘ DO LEKÓW ({len(results['eligible_drugs'])}):")
        for drug in results['eligible_drugs']:
            lines.append(f"   • {drug}")
    else:
        lines.append("\n❌ NIE KWALIFIKUJE SIĘ DO ŻADNEGO LEKU")

    lines.append("\n" + "-" * 50)
    lines.append("SZCZEGÓŁY DLA KAŻDEGO LEKU:")
    lines.append("-" * 50)

    for drug_key, drug_result in results.get('drug_results', {}).items():
        status = "✅" if drug_result['eligible'] else "❌"
        lines.append(f"\n{status} {drug_result['drug_pl']}")

        if drug_result.get('indication'):
            lines.append(f"   Wskazanie: {drug_result['indication']}")

        if drug_result.get('criteria_met'):
            lines.append("   Spełnione:")
            for c in drug_result['criteria_met'][:5]:  # Limit to 5
                lines.append(f"     ✓ {c}")

        if drug_result.get('criteria_not_met'):
            lines.append("   Niespełnione:")
            for c in drug_result['criteria_not_met'][:3]:  # Limit to 3
                lines.append(f"     ✗ {c}")

        if drug_result.get('warnings'):
            lines.append("   Uwagi:")
            for w in drug_result['warnings'][:2]:
                lines.append(f"     ⚠ {w}")

        if drug_result.get('dosing'):
            d = drug_result['dosing']
            lines.append(f"   Dawkowanie: {d['dose']} ({d['frequency']})")

    return "\n".join(lines)


# =============================================================================
# MAIN / CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Prostate Cancer Clinical Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Calculation type')
    
    # NCCN risk
    nccn_parser = subparsers.add_parser('nccn', help='Calculate NCCN risk group')
    nccn_parser.add_argument('--psa', type=float, required=True)
    nccn_parser.add_argument('--gg', type=int, required=True, help='Grade Group 1-5')
    nccn_parser.add_argument('--stage', type=str, required=True, help='T-stage')
    nccn_parser.add_argument('--cores', type=str, required=True, help='positive/total, e.g., 4/12')
    nccn_parser.add_argument('--max-involvement', type=float, default=100)
    nccn_parser.add_argument('--psa-density', type=float, default=0.2)
    
    # Briganti
    briganti_parser = subparsers.add_parser('briganti', help='Calculate Briganti 2017 LNI')
    briganti_parser.add_argument('--psa', type=float, required=True)
    briganti_parser.add_argument('--stage', type=str, required=True)
    briganti_parser.add_argument('--gg', type=int, required=True)
    briganti_parser.add_argument('--pct-high', type=float, required=True)
    briganti_parser.add_argument('--pct-low', type=float, required=True)
    
    # PSADT
    psadt_parser = subparsers.add_parser('psadt', help='Calculate PSADT')
    psadt_parser.add_argument('--values', type=str, required=True,
                              help='Comma-separated day:psa pairs, e.g., "0:0.2,90:0.4,180:0.8"')
    
    # Roach
    roach_parser = subparsers.add_parser('roach', help='Calculate Roach LNI')
    roach_parser.add_argument('--psa', type=float, required=True)
    roach_parser.add_argument('--gleason', type=int, required=True)

    # TNM Staging
    tnm_parser = subparsers.add_parser('tnm', help='Calculate TNM and AJCC prognostic stage')
    tnm_parser.add_argument('--t', type=str, required=True, help='T-stage (T1a, T1b, T1c, T2a, T2b, T2c, T3a, T3b, T4)')
    tnm_parser.add_argument('--n', type=str, default='N0', help='N-stage (N0, N1)')
    tnm_parser.add_argument('--m', type=str, default='M0', help='M-stage (M0, M1, M1a, M1b, M1c)')
    tnm_parser.add_argument('--psa', type=float, help='PSA in ng/mL (for prognostic staging)')
    tnm_parser.add_argument('--gg', type=int, help='Grade Group 1-5 (for prognostic staging)')

    args = parser.parse_args()

    if args.command == 'nccn':
        pos, total = map(int, args.cores.split('/'))
        result = calculate_nccn_risk(
            psa=args.psa,
            grade_group=args.gg,
            t_stage=args.stage,
            positive_cores=pos,
            total_cores=total,
            max_core_involvement=args.max_involvement,
            psa_density=args.psa_density
        )
        print(f"NCCN Risk Group: {result}")
    
    elif args.command == 'briganti':
        result = briganti_2017_lni(
            psa=args.psa,
            t_stage=args.stage,
            grade_group=args.gg,
            pct_positive_highest=args.pct_high,
            pct_positive_lowest=args.pct_low
        )
        print(f"LNI Probability: {result['probability']}%")
        print(f"Recommend ePLND: {'Yes' if result['recommend_eplnd'] else 'No'}")
    
    elif args.command == 'psadt':
        pairs = args.values.split(',')
        psa_values = []
        for pair in pairs:
            day, psa = pair.split(':')
            psa_values.append((float(day), float(psa)))
        result = calculate_psadt(psa_values)
        if result.get('ok'):
            print(f"PSADT: {result['psadt_months']:.1f} months")
            print(f"Interpretation: {result['interpretation']}")
            print(f"R-squared: {result['r_squared']:.3f}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")

    elif args.command == 'roach':
        result = roach_lni(psa=args.psa, gleason=args.gleason)
        if result.get('ok'):
            print(f"LNI Risk: {result['probability']}%")
            print(f"Recommend Pelvic RT: {'Yes' if result['recommend_pelvic_rt'] else 'No'}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")

    elif args.command == 'tnm':
        result = calculate_tnm_stage(
            clinical_t=args.t,
            n_stage=args.n,
            m_stage=args.m,
            psa=args.psa,
            grade_group=args.gg
        )
        if result.get('ok'):
            print(f"TNM: {result['tnm_summary']}")
            print(f"T: {result['t_description']}")
            print(f"N: {result['n_description']}")
            print(f"M: {result['m_description']}")
            if result.get('prognostic_stage'):
                print(f"AJCC Prognostic Stage: {result['prognostic_stage']}")
                print(f"Description: {result['prognostic_stage_description']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
