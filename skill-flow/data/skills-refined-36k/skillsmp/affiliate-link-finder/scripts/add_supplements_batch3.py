#!/usr/bin/env python3
"""
Script to add 4 new conditional/cautionary supplements for Batch 3
These supplements require detailed warnings and usage guidelines
"""

# The 4 new Batch 3 supplements as properly formatted Dart map entries
NEW_SUPPLEMENTS_BATCH3 = '''      {
        "id": "st-johns-wort",
        "name": "St. John's Wort",
        "category": "Herb",
        "dosage": "300mg",
        "timeOfDay": "morning",
        "benefits": [
          "Mild Depression",
          "Mood Support"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "⚠️ CAUTION: Powerful CYP450 enzyme inducer. Interacts with MANY medications including birth control, antidepressants, and blood thinners. NOT recommended for ADHD.",
        "status": "caution",
        "mechanismOfAction":
            "St. John's Wort contains hypericin and hyperforin which modulate serotonin, dopamine, and norepinephrine reuptake. However, it is a potent inducer of CYP450 enzymes (particularly CYP3A4), which dramatically increases the metabolism of many medications, reducing their effectiveness. This makes it incompatible with most pharmaceutical treatments.",
        "detailedBenefits": [
          "May help mild to moderate depression (comparable to SSRIs in some studies)",
          "Modulates multiple neurotransmitter systems",
          "Natural alternative to pharmaceutical antidepressants for some people"
        ],
        "timingRationale":
            "Morning dosing if used. However, NOT RECOMMENDED for people with ADHD due to extensive drug interactions with stimulant medications and other common treatments. Effects build over 2-4 weeks. The CYP450 induction persists for weeks after discontinuation.",
        "scientificEvidenceRank": 65,
        "studyLinks": {
          "St. John's Wort for depression":
              "https://pubmed.ncbi.nlm.nih.gov/18843608/",
          "Drug interactions and CYP450 induction":
              "https://pubmed.ncbi.nlm.nih.gov/15106147/",
          "Contraindications and safety":
              "https://pubmed.ncbi.nlm.nih.gov/24931003/"
        },
        "dosageByWeight": {
          "40-60": "300mg",
          "60-80": "300-600mg",
          "80-100": "600mg",
          "100-120": "600-900mg"
        },
        "dosageFrequency": "Once or twice daily (NOT RECOMMENDED for ADHD patients)",
        "dosageWarnings": [
          "⚠️ CRITICAL: Reduces effectiveness of birth control pills by 50%+",
          "⚠️ Interacts with SSRIs, SNRIs (serotonin syndrome risk)",
          "⚠️ Reduces effectiveness of blood thinners, immunosuppressants, HIV medications",
          "⚠️ May interact with ADHD stimulant medications",
          "Causes photosensitivity - increases sun sensitivity",
          "NOT RECOMMENDED for people on multiple medications"
        ],
        "tldr":
            "Herb for mild depression but EXTENSIVE drug interactions make it unsuitable for most ADHD patients on medications.",
        "adhdMedInteractions": {
          "Adderall":
              "⚠️ NOT RECOMMENDED: May alter stimulant metabolism through CYP450 induction, reducing effectiveness or causing unpredictable effects.",
          "Vyvanse":
              "⚠️ NOT RECOMMENDED: CYP450 induction may affect lisdexamfetamine conversion to active form, altering medication efficacy.",
          "Ritalin":
              "⚠️ CAUTION: Potential interaction through enzyme induction; unpredictable effects on methylphenidate metabolism."
        }
      },
      {
        "id": "valerian-root",
        "name": "Valerian Root",
        "category": "Herb",
        "dosage": "300-600mg",
        "timeOfDay": "evening",
        "benefits": [
          "Sleep Support",
          "Anxiety Reduction"
        ],
        "evidenceLevel": "low",
        "notes":
            "⚠️ CAUTION: Sedating herb for sleep. Can cause morning grogginess. May interact with other sedatives. Not for daytime use.",
        "status": "caution",
        "mechanismOfAction":
            "Valerian root contains valerenic acid which modulates GABA-A receptors, similar to benzodiazepines but much weaker. It increases GABA availability and has mild sedative effects. However, response is highly variable between individuals, and it can cause paradoxical stimulation in some people. Also inhibits CYP450 enzymes.",
        "detailedBenefits": [
          "May reduce sleep latency (time to fall asleep) by 15-20 minutes",
          "Mild anxiolytic effects through GABAergic activity",
          "Non-addictive alternative to prescription sleep aids for some"
        ],
        "timingRationale":
            "Evening only, 30-120 minutes before bed. Highly variable onset time between individuals. Can cause significant morning grogginess or 'hangover' effect. NOT for daytime use. Effects may build over 2-4 weeks of consistent use. Avoid if you need to wake up alert.",
        "scientificEvidenceRank": 58,
        "studyLinks": {
          "Valerian for sleep quality":
              "https://pubmed.ncbi.nlm.nih.gov/16335332/",
          "GABA modulation mechanism":
              "https://pubmed.ncbi.nlm.nih.gov/15650394/",
          "Safety and drug interactions":
              "https://pubmed.ncbi.nlm.nih.gov/17145239/"
        },
        "dosageByWeight": {
          "40-60": "300mg",
          "60-80": "400-500mg",
          "80-100": "500-600mg",
          "100-120": "600mg"
        },
        "dosageFrequency": "Once daily in evening, 30-120 min before bed",
        "dosageWarnings": [
          "⚠️ Can cause significant morning grogginess or 'hangover'",
          "⚠️ May interact with other sedatives, alcohol, benzodiazepines",
          "⚠️ Can cause paradoxical stimulation in some people",
          "Avoid before driving or operating machinery",
          "May inhibit CYP450 enzymes - potential drug interactions",
          "Discontinue 2 weeks before surgery (anesthesia interaction)"
        ],
        "tldr":
            "Sedating herb for sleep support; highly variable effects and can cause morning grogginess.",
        "adhdMedInteractions": {
          "Adderall":
              "May help with stimulant-induced insomnia but can cause morning grogginess that interferes with medication effectiveness.",
          "Vyvanse":
              "Evening use may support sleep after long-acting stimulant wears off, but monitor for next-day sedation.",
          "Ritalin":
              "Can help with sleep onset if stimulants cause insomnia, but variable effects and potential morning impairment."
        }
      },
      {
        "id": "kava-kava",
        "name": "Kava Kava",
        "category": "Herb",
        "dosage": "200-300mg kavalactones",
        "timeOfDay": "evening",
        "benefits": [
          "Anxiety Reduction",
          "Relaxation"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "⚠️ CAUTION: Effective anxiolytic but LIVER TOXICITY RISK. Banned in several countries. Use only high-quality noble kava. Monitor liver enzymes. NOT for long-term use.",
        "status": "caution",
        "mechanismOfAction":
            "Kava's kavalactones modulate GABA-A receptors and block voltage-gated sodium channels, producing anxiolytic and muscle-relaxant effects without sedation at lower doses. However, certain kava preparations (especially those using stems/leaves or non-noble varieties) contain hepatotoxic compounds that can cause severe liver damage. Mechanism of liver toxicity is not fully understood.",
        "detailedBenefits": [
          "Reduces anxiety by 50-60% in clinical trials (comparable to benzodiazepines)",
          "Non-sedating anxiolytic at moderate doses",
          "May improve sleep quality without morning grogginess"
        ],
        "timingRationale":
            "Evening dosing preferred due to relaxation effects. Lower doses can be used during day for anxiety without sedation, but evening use is safer. Effects begin within 30-60 minutes. CRITICAL: Use only noble kava varieties (not tudei kava) and avoid long-term daily use due to liver toxicity risk.",
        "scientificEvidenceRank": 64,
        "studyLinks": {
          "Kava for anxiety disorders":
              "https://pubmed.ncbi.nlm.nih.gov/23235473/",
          "Hepatotoxicity concerns and safety":
              "https://pubmed.ncbi.nlm.nih.gov/17406128/",
          "Mechanism of action":
              "https://pubmed.ncbi.nlm.nih.gov/15639154/"
        },
        "dosageByWeight": {
          "40-60": "150-200mg kavalactones",
          "60-80": "200-250mg kavalactones",
          "80-100": "250-300mg kavalactones",
          "100-120": "300mg kavalactones"
        },
        "dosageFrequency": "Once daily in evening, NOT for long-term daily use",
        "dosageWarnings": [
          "⚠️ CRITICAL: LIVER TOXICITY RISK - monitor liver enzymes if using",
          "⚠️ Use ONLY noble kava varieties (not tudei kava or stem/leaf preparations)",
          "⚠️ Avoid if you have liver disease or take hepatotoxic medications",
          "⚠️ Do NOT combine with alcohol (increases liver toxicity risk)",
          "Can cause skin changes (kava dermopathy) with chronic use",
          "May interact with sedatives, anesthesia, and CYP450-metabolized drugs",
          "Banned in several countries due to safety concerns"
        ],
        "tldr":
            "Potent anxiolytic herb but SERIOUS liver toxicity risk; use only noble varieties and monitor liver function.",
        "adhdMedInteractions": {
          "Adderall":
              "May reduce stimulant-induced anxiety but liver toxicity risk makes it a poor choice for long-term use with medications.",
          "Vyvanse":
              "Can help with evening anxiety after stimulant offset, but hepatotoxicity concerns limit safe use.",
          "Ritalin":
              "Anxiolytic effects may complement stimulant therapy, but liver toxicity risk outweighs benefits for most patients."
        }
      },
      {
        "id": "dmae",
        "name": "DMAE (Dimethylaminoethanol)",
        "category": "Nootropic",
        "dosage": "100-300mg",
        "timeOfDay": "morning",
        "benefits": [
          "Focus",
          "Mood"
        ],
        "evidenceLevel": "low",
        "notes":
            "⚠️ CAUTION: Theoretical choline precursor but limited evidence. May cause overstimulation, insomnia, or headaches. Not well-researched for ADHD.",
        "status": "caution",
        "mechanismOfAction":
            "DMAE is theorized to be a precursor to choline and acetylcholine, but this mechanism is poorly supported by research. It may modulate cholinergic activity through unclear pathways. Some studies suggest it stabilizes cell membranes. However, evidence for cognitive benefits is weak and inconsistent. May cause neural overstimulation in some individuals.",
        "detailedBenefits": [
          "Anecdotal reports of improved focus and mental clarity",
          "May have mild mood-enhancing effects",
          "Theoretical support for acetylcholine production (weak evidence)"
        ],
        "timingRationale":
            "Morning dosing if used, as it can be stimulating and cause insomnia. However, NOT RECOMMENDED due to limited evidence and potential for side effects. Effects are highly variable and unpredictable. Some people experience overstimulation, headaches, or irritability.",
        "scientificEvidenceRank": 42,
        "studyLinks": {
          "DMAE for cognitive function (limited evidence)":
              "https://pubmed.ncbi.nlm.nih.gov/3526687/",
          "Safety concerns and side effects":
              "https://pubmed.ncbi.nlm.nih.gov/6153094/",
          "Mechanism of action (theoretical)":
              "https://pubmed.ncbi.nlm.nih.gov/7301036/"
        },
        "dosageByWeight": {
          "40-60": "100mg",
          "60-80": "150-200mg",
          "80-100": "200-300mg",
          "100-120": "300mg"
        },
        "dosageFrequency": "Once daily in morning (NOT RECOMMENDED)",
        "dosageWarnings": [
          "⚠️ Limited scientific evidence for benefits",
          "⚠️ May cause overstimulation, insomnia, headaches, irritability",
          "⚠️ Can worsen symptoms in some people with ADHD",
          "Avoid if you have bipolar disorder (may trigger mania)",
          "May interact with cholinergic medications",
          "Not recommended during pregnancy or breastfeeding",
          "Better alternatives available (Alpha-GPC, CDP-Choline)"
        ],
        "tldr":
            "Theoretical nootropic with weak evidence and unpredictable effects; better choline sources available.",
        "adhdMedInteractions": {
          "Adderall":
              "⚠️ May cause overstimulation when combined with stimulants; unpredictable effects.",
          "Vyvanse":
              "⚠️ Risk of excessive stimulation; may worsen anxiety or irritability.",
          "Ritalin":
              "⚠️ Potential for additive stimulant effects; not recommended due to limited evidence."
        }
      },
'''

def main():
    file_path = 'lib/infrastructure/services/seeding_service.dart'
    
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the insertion point (look for caffeine which should be in the caution section)
    insertion_index = None
    for i, line in enumerate(lines):
        if '"id": "caffeine"' in line:
            # Go back to find the previous closing brace
            for j in range(i-1, 0, -1):
                if lines[j].strip() == '},':
                    insertion_index = j + 1
                    break
            break
    
    if insertion_index is None:
        print("ERROR: Could not find insertion point (caffeine)")
        print("Searching for alternative insertion point...")
        # Try finding melatonin or any caution status
        for i, line in enumerate(lines):
            if '"status": "caution"' in line:
                # Go back to find the opening brace of this entry
                for j in range(i-1, 0, -1):
                    if lines[j].strip() == '{':
                        # This is the start, now go back one more to find previous closing
                        for k in range(j-1, 0, -1):
                            if lines[k].strip() == '},':
                                insertion_index = k + 1
                                break
                        break
                if insertion_index:
                    break
    
    if insertion_index is None:
        print("ERROR: Could not find insertion point")
        return
    
    print(f"Inserting 4 new conditional supplements at line {insertion_index + 1}")
    
    # Insert the new supplements
    lines.insert(insertion_index, NEW_SUPPLEMENTS_BATCH3)
    
    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("✅ Successfully added 4 new conditional/cautionary supplements!")
    print("New supplements: St. John's Wort, Valerian Root, Kava Kava, DMAE")
    print("Note: Caffeine, Melatonin, Ginseng, Copper, and B6 will be enhanced separately")

if __name__ == '__main__':
    main()
