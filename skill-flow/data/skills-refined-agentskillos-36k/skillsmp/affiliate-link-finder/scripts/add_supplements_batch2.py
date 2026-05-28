#!/usr/bin/env python3
"""
Script to add 7 new/enhanced supplements for Batch 2
Inserts after the Batch 1 supplements
"""

# The 7 Batch 2 supplements as properly formatted Dart map entries
NEW_SUPPLEMENTS_BATCH2 = '''      {
        "id": "green-tea-extract",
        "name": "Green Tea Extract (EGCG)",
        "category": "Antioxidant",
        "dosage": "250-500mg EGCG",
        "timeOfDay": "morning",
        "benefits": [
          "Focus Enhancement",
          "Neuroprotection",
          "Fat Oxidation"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Standardized to 50% EGCG (epigallocatechin gallate). Contains L-theanine naturally. Avoid high doses on empty stomach.",
        "status": "beneficial",
        "mechanismOfAction":
            "EGCG crosses the blood-brain barrier and modulates dopamine and norepinephrine levels. It inhibits COMT (catechol-O-methyltransferase), the enzyme that breaks down dopamine, extending dopamine availability. Also provides neuroprotection through antioxidant activity and supports mitochondrial function.",
        "detailedBenefits": [
          "Extends dopamine half-life by inhibiting COMT enzyme",
          "Improves sustained attention and reduces mind-wandering",
          "Neuroprotective against oxidative stress and neurodegeneration",
          "Synergizes with L-theanine for calm, focused alertness"
        ],
        "timingRationale":
            "Morning dosing provides focus benefits throughout the day. Contains caffeine (unless decaffeinated), so avoid evening use. Take with food to prevent nausea. Effects peak 1-2 hours after ingestion. Decaffeinated extracts can be taken later in the day if needed.",
        "scientificEvidenceRank": 77,
        "studyLinks": {
          "EGCG and dopamine metabolism":
              "https://pubmed.ncbi.nlm.nih.gov/18296328/",
          "Green tea for cognitive function":
              "https://pubmed.ncbi.nlm.nih.gov/28056735/",
          "COMT inhibition and attention":
              "https://pubmed.ncbi.nlm.nih.gov/21129394/"
        },
        "dosageByWeight": {
          "40-60": "250mg EGCG",
          "60-80": "300-400mg EGCG",
          "80-100": "400-500mg EGCG",
          "100-120": "500mg EGCG"
        },
        "dosageFrequency": "Once or twice daily with meals",
        "dosageWarnings": [
          "Contains caffeine unless decaffeinated (30-50mg per dose)",
          "Take with food to avoid nausea (tannins can upset stomach)",
          "High doses (>800mg EGCG) may affect liver enzymes - monitor",
          "May interact with blood thinners and blood pressure medications"
        ],
        "tldr":
            "Extends dopamine availability by inhibiting COMT; provides neuroprotection and synergizes with L-theanine for focus.",
        "adhdMedInteractions": {
          "Adderall":
              "COMT inhibition may extend dopamine availability, potentially enhancing and prolonging stimulant effects. Monitor for overstimulation.",
          "Vyvanse":
              "May extend the duration of dopamine elevation from lisdexamfetamine; could reduce 'crash' during offset.",
          "Ritalin":
              "Complementary mechanism - methylphenidate blocks reuptake while EGCG blocks breakdown, potentially synergistic."
        }
      },
      {
        "id": "nac",
        "name": "N-Acetyl Cysteine (NAC)",
        "category": "Amino Acid",
        "dosage": "600-1200mg",
        "timeOfDay": "morning",
        "benefits": [
          "Glutathione Production",
          "Oxidative Stress Reduction",
          "Impulse Control"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Precursor to glutathione, the brain's master antioxidant. Modulates glutamate for impulse control. Take on empty stomach for best absorption.",
        "status": "beneficial",
        "mechanismOfAction":
            "NAC is a precursor to glutathione, the brain's primary antioxidant defense system. It also modulates glutamate neurotransmission by restoring cystine-glutamate exchange in the nucleus accumbens, which is implicated in impulse control and compulsive behaviors. Additionally supports mitochondrial function and reduces neuroinflammation.",
        "detailedBenefits": [
          "Increases brain glutathione levels by 30-50% for neuroprotection",
          "Improves impulse control and reduces compulsive behaviors",
          "Protects dopaminergic neurons from oxidative damage",
          "May reduce irritability and emotional dysregulation"
        ],
        "timingRationale":
            "Morning dosing on empty stomach maximizes absorption (food reduces bioavailability by ~30%). Effects build over 2-4 weeks of consistent use. Some people split dose (morning + afternoon) for sustained glutathione production. Avoid evening dosing as it can be mildly energizing.",
        "scientificEvidenceRank": 79,
        "studyLinks": {
          "NAC for impulse control and ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/31109635/",
          "Glutathione and neuroprotection":
              "https://pubmed.ncbi.nlm.nih.gov/29706149/",
          "NAC and glutamate modulation":
              "https://pubmed.ncbi.nlm.nih.gov/23369637/"
        },
        "dosageByWeight": {
          "40-60": "600mg",
          "60-80": "900mg",
          "80-100": "1200mg",
          "100-120": "1200-1800mg"
        },
        "dosageFrequency": "Once or twice daily on empty stomach (30 min before meals)",
        "dosageWarnings": [
          "May cause GI upset - start with lower dose and increase gradually",
          "Can have sulfur smell/taste (normal, not harmful)",
          "Avoid if you have asthma (may trigger bronchospasm in rare cases)",
          "Generally very safe; used in hospitals for acetaminophen overdose"
        ],
        "tldr":
            "Boosts glutathione for neuroprotection and modulates glutamate for improved impulse control and reduced compulsivity.",
        "adhdMedInteractions": {
          "Adderall":
              "Provides antioxidant protection against stimulant-induced oxidative stress; may improve impulse control beyond medication effects.",
          "Vyvanse":
              "Supports long-term brain health during chronic stimulant use; glutamate modulation complements dopamine effects.",
          "Ritalin":
              "Neuroprotective benefits support sustained medication effectiveness; may reduce irritability side effects."
        }
      },
      {
        "id": "huperzine-a",
        "name": "Huperzine A",
        "category": "Nootropic",
        "dosage": "50-200mcg",
        "timeOfDay": "morning",
        "benefits": [
          "Acetylcholine Enhancement",
          "Memory Consolidation",
          "Neuroprotection"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Potent acetylcholinesterase inhibitor. Very long half-life (24+ hours). Start low, cycle use (5 days on, 2 days off recommended).",
        "status": "beneficial",
        "mechanismOfAction":
            "Huperzine A is a reversible acetylcholinesterase inhibitor that prevents the breakdown of acetylcholine, increasing its availability in synapses. It has a very long half-life (24-36 hours) and also provides neuroprotection through NMDA receptor modulation and antioxidant effects. Supports memory formation and learning.",
        "detailedBenefits": [
          "Increases acetylcholine levels by 30-40% for enhanced attention",
          "Improves memory consolidation and recall",
          "Neuroprotective against glutamate excitotoxicity",
          "May enhance neuroplasticity and learning capacity"
        ],
        "timingRationale":
            "Morning dosing recommended due to 24+ hour half-life. Effects are cumulative and long-lasting. Cycling (5 days on, 2 days off) prevents tolerance and allows acetylcholinesterase levels to normalize. Take with or without food. Avoid daily use without breaks.",
        "scientificEvidenceRank": 71,
        "studyLinks": {
          "Huperzine A for cognitive enhancement":
              "https://pubmed.ncbi.nlm.nih.gov/23374481/",
          "Acetylcholinesterase inhibition and memory":
              "https://pubmed.ncbi.nlm.nih.gov/16007238/",
          "Neuroprotective effects":
              "https://pubmed.ncbi.nlm.nih.gov/18611150/"
        },
        "dosageByWeight": {
          "40-60": "50mcg",
          "60-80": "100mcg",
          "80-100": "150mcg",
          "100-120": "200mcg"
        },
        "dosageFrequency": "Once daily in morning, cycle 5 days on / 2 days off",
        "dosageWarnings": [
          "Very long half-life - do NOT take daily without breaks (cycle use)",
          "May cause vivid dreams or insomnia if taken too late in day",
          "Can cause cholinergic side effects (nausea, headache) at high doses",
          "Start with lowest dose and assess tolerance before increasing"
        ],
        "tldr":
            "Potent acetylcholinesterase inhibitor with 24+ hour half-life; enhances memory and attention but requires cycling to prevent tolerance.",
        "adhdMedInteractions": {
          "Adderall":
              "Complementary mechanism - enhances acetylcholine (attention/memory) while stimulants enhance dopamine (motivation/focus).",
          "Vyvanse":
              "May improve memory consolidation and learning during medication-enhanced focus periods.",
          "Ritalin":
              "Supports attention through different neurotransmitter system; may enhance overall cognitive benefits."
        }
      },
      {
        "id": "vinpocetine",
        "name": "Vinpocetine",
        "category": "Nootropic",
        "dosage": "10-20mg",
        "timeOfDay": "morning",
        "benefits": [
          "Cerebral Blood Flow",
          "Mental Clarity",
          "Neuroprotection"
        ],
        "evidenceLevel": "low",
        "notes":
            "Derived from periwinkle plant. Enhances cerebral blood flow and glucose utilization. Take with food for better absorption.",
        "status": "beneficial",
        "mechanismOfAction":
            "Vinpocetine enhances cerebral blood flow by dilating blood vessels in the brain and reducing blood viscosity. It also improves glucose and oxygen utilization in neurons, supports mitochondrial function, and has neuroprotective antioxidant properties. May modulate phosphodiesterase to increase cAMP levels.",
        "detailedBenefits": [
          "Increases cerebral blood flow by 7-30% in research studies",
          "Improves mental clarity and processing speed",
          "Enhances glucose utilization for brain energy",
          "Neuroprotective against ischemia and oxidative stress"
        ],
        "timingRationale":
            "Morning or early afternoon dosing with food maximizes absorption (fat-soluble). Effects are noticeable within 1-2 hours. Avoid evening dosing as increased blood flow and energy can interfere with sleep. Take with meals containing fat for best bioavailability.",
        "scientificEvidenceRank": 63,
        "studyLinks": {
          "Vinpocetine and cerebral blood flow":
              "https://pubmed.ncbi.nlm.nih.gov/12404671/",
          "Cognitive enhancement effects":
              "https://pubmed.ncbi.nlm.nih.gov/12895685/",
          "Neuroprotective mechanisms":
              "https://pubmed.ncbi.nlm.nih.gov/16389715/"
        },
        "dosageByWeight": {
          "40-60": "10mg",
          "60-80": "15mg",
          "80-100": "20mg",
          "100-120": "20-30mg"
        },
        "dosageFrequency": "Once or twice daily with meals",
        "dosageWarnings": [
          "Take with food (fat-soluble, poor absorption on empty stomach)",
          "May lower blood pressure - monitor if on BP medications",
          "Avoid during pregnancy (may affect blood flow to placenta)",
          "Can interact with blood thinners - consult physician"
        ],
        "tldr":
            "Enhances cerebral blood flow and glucose utilization for improved mental clarity and processing speed.",
        "adhdMedInteractions": {
          "Adderall":
              "Improved blood flow may enhance nutrient delivery to support stimulant-driven cognitive demands.",
          "Vyvanse":
              "Better glucose utilization may support sustained energy during long medication duration.",
          "Ritalin":
              "Complementary mechanism - blood flow enhancement supports dopamine-driven focus improvements."
        }
      },
      {
        "id": "mucuna-pruriens",
        "name": "Mucuna Pruriens (L-DOPA)",
        "category": "Amino Acid",
        "dosage": "300-500mg",
        "timeOfDay": "morning",
        "benefits": [
          "Dopamine Precursor",
          "Mood Enhancement",
          "Motivation"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "⚠️ Natural source of L-DOPA (dopamine precursor). Use cautiously - can deplete dopamine with chronic use. Cycle recommended.",
        "status": "beneficial",
        "mechanismOfAction":
            "Mucuna pruriens contains L-DOPA (levodopa), the direct precursor to dopamine. It crosses the blood-brain barrier and is converted to dopamine by aromatic L-amino acid decarboxylase. While this provides immediate dopamine boost, chronic use without cycling can downregulate dopamine receptors and deplete endogenous production. Also contains other neuroprotective compounds.",
        "detailedBenefits": [
          "Rapidly increases dopamine levels (within 30-60 minutes)",
          "Improves motivation, mood, and drive",
          "May enhance focus and mental energy",
          "Contains neuroprotective antioxidants beyond L-DOPA"
        ],
        "timingRationale":
            "Morning dosing on empty stomach maximizes L-DOPA absorption (protein competes for absorption). Effects peak within 1-2 hours. CRITICAL: Cycle use (3-5 days on, 2-3 days off) to prevent receptor downregulation and dopamine depletion. Not for daily long-term use.",
        "scientificEvidenceRank": 69,
        "studyLinks": {
          "Mucuna pruriens and dopamine":
              "https://pubmed.ncbi.nlm.nih.gov/15478206/",
          "L-DOPA for mood and motivation":
              "https://pubmed.ncbi.nlm.nih.gov/24931003/",
          "Neuroprotective effects":
              "https://pubmed.ncbi.nlm.nih.gov/23675006/"
        },
        "dosageByWeight": {
          "40-60": "300mg (15% L-DOPA extract)",
          "60-80": "400mg",
          "80-100": "500mg",
          "100-120": "500-600mg"
        },
        "dosageFrequency": "Once daily on empty stomach, CYCLE 3-5 days on / 2-3 days off",
        "dosageWarnings": [
          "⚠️ MUST CYCLE - chronic daily use depletes dopamine and downregulates receptors",
          "Take on empty stomach (protein blocks L-DOPA absorption)",
          "May cause nausea, especially at higher doses",
          "Avoid with MAO inhibitors or Parkinson's medications",
          "Not recommended for long-term daily use without cycling"
        ],
        "tldr":
            "Natural L-DOPA source for rapid dopamine boost; MUST be cycled to prevent receptor downregulation and depletion.",
        "adhdMedInteractions": {
          "Adderall":
              "⚠️ CAUTION: Combining may cause excessive dopamine and overstimulation. Use on non-medication days or cycle carefully.",
          "Vyvanse":
              "⚠️ CAUTION: Risk of dopamine overload. Consider using on medication-free days or weekends only.",
          "Ritalin":
              "⚠️ CAUTION: Additive dopamine effects may cause jitteriness or anxiety. Monitor carefully if combining."
        }
      },
'''

def main():
    file_path = 'lib/infrastructure/services/seeding_service.dart'
    
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the insertion point (after Curcumin, before Alpha-GPC)
    insertion_index = None
    for i, line in enumerate(lines):
        if '"id": "alpha-gpc"' in line:
            # Go back to find the previous closing brace
            for j in range(i-1, 0, -1):
                if lines[j].strip() == '},':
                    insertion_index = j + 1
                    break
            break
    
    if insertion_index is None:
        print("ERROR: Could not find insertion point")
        return
    
    print(f"Inserting 5 new supplements at line {insertion_index + 1}")
    
    # Insert the new supplements
    lines.insert(insertion_index, NEW_SUPPLEMENTS_BATCH2)
    
    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("✅ Successfully added 5 new supplements!")
    print("New supplements: Green Tea Extract, NAC, Huperzine A, Vinpocetine, Mucuna Pruriens")
    print("Note: Alpha-GPC and 5-HTP will be enhanced separately")

if __name__ == '__main__':
    main()
