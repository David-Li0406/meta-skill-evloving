#!/usr/bin/env python3
"""
Script to add 6 new fully standardized supplements to seeding_service.dart
Inserts after B-Complex and before Alpha-GPC
"""

# The 6 new supplements as properly formatted Dart map entries
NEW_SUPPLEMENTS = '''      {
        "id": "rhodiola-rosea",
        "name": "Rhodiola Rosea",
        "category": "Adaptogen",
        "dosage": "200-400mg",
        "timeOfDay": "morning",
        "benefits": [
          "Mental Fatigue Reduction",
          "Stress Resilience",
          "Sustained Attention"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Standardized to 3% rosavins and 1% salidroside. Adaptogen that reduces mental fatigue without sedation.",
        "status": "beneficial",
        "mechanismOfAction":
            "Rhodiola modulates the HPA (hypothalamic-pituitary-adrenal) axis to improve stress resilience. It increases availability of serotonin and dopamine in the prefrontal cortex by inhibiting monoamine oxidase (MAO) enzymes. Also enhances ATP synthesis and reduces cortisol during chronic stress.",
        "detailedBenefits": [
          "Reduces mental fatigue during sustained cognitive tasks by 20-30%",
          "Improves stress-induced attention deficits",
          "Enhances working memory under pressure",
          "Supports dopamine and serotonin availability without depletion"
        ],
        "timingRationale":
            "Morning or early afternoon dosing recommended. Effects begin within 30 minutes and peak at 1-2 hours. Avoid evening use as it can be mildly stimulating and may interfere with sleep.",
        "scientificEvidenceRank": 76,
        "studyLinks": {
          "Rhodiola for mental fatigue":
              "https://pubmed.ncbi.nlm.nih.gov/19016404/",
          "Adaptogenic effects on stress":
              "https://pubmed.ncbi.nlm.nih.gov/11410073/",
          "Cognitive enhancement in fatigue":
              "https://pubmed.ncbi.nlm.nih.gov/20378318/"
        },
        "dosageByWeight": {
          "40-60": "200mg",
          "60-80": "300mg",
          "80-100": "400mg",
          "100-120": "400-500mg"
        },
        "dosageFrequency": "Once or twice daily (morning and early afternoon)",
        "dosageWarnings": [
          "May be mildly stimulating - avoid evening dosing",
          "Start with lower dose to assess tolerance",
          "Avoid with bipolar disorder (may trigger manic episodes)",
          "Generally well-tolerated with minimal side effects"
        ],
        "tldr":
            "Adaptogen that reduces mental fatigue and enhances stress resilience by modulating dopamine and serotonin.",
        "adhdMedInteractions": {
          "Adderall":
              "May help reduce stimulant-induced stress response and support sustained focus during medication offset.",
          "Vyvanse":
              "Complements stimulant action by supporting stress resilience and reducing mental fatigue.",
          "Ritalin":
              "May enhance cognitive benefits while reducing stress-related side effects of stimulant medications."
        }
      },
      {
        "id": "ashwagandha",
        "name": "Ashwagandha (KSM-66)",
        "category": "Adaptogen",
        "dosage": "300-600mg",
        "timeOfDay": "evening",
        "benefits": [
          "Stress Reduction",
          "Anxiety Management",
          "Sleep Quality"
        ],
        "evidenceLevel": "high",
        "notes":
            "KSM-66 or Sensoril extracts preferred. Reduces cortisol and anxiety. Best for evening use due to calming effects.",
        "status": "beneficial",
        "mechanismOfAction":
            "Ashwagandha's withanolides modulate GABAergic signaling to reduce anxiety and promote relaxation. It lowers cortisol levels by regulating the HPA axis. Also enhances BDNF (brain-derived neurotrophic factor) which supports neuroplasticity and stress resilience.",
        "detailedBenefits": [
          "Reduces cortisol levels by 23-28% in chronic stress",
          "Improves sleep quality and reduces sleep latency",
          "Reduces anxiety symptoms by 40-50% in clinical trials",
          "Supports executive function recovery after stressful periods"
        ],
        "timingRationale":
            "Evening dosing (1-2 hours before bed) is optimal for most people due to calming effects. Some may tolerate morning dosing for daytime anxiety, but it can cause drowsiness. Effects build over 2-4 weeks of consistent use.",
        "scientificEvidenceRank": 82,
        "studyLinks": {
          "Ashwagandha for stress and anxiety":
              "https://pubmed.ncbi.nlm.nih.gov/23439798/",
          "Cortisol reduction in chronic stress":
              "https://pubmed.ncbi.nlm.nih.gov/31517876/",
          "Sleep quality improvement":
              "https://pubmed.ncbi.nlm.nih.gov/31728244/"
        },
        "dosageByWeight": {
          "40-60": "300mg",
          "60-80": "400-500mg",
          "80-100": "500-600mg",
          "100-120": "600mg"
        },
        "dosageFrequency": "Once daily in the evening, or split into morning/evening doses",
        "dosageWarnings": [
          "May cause drowsiness - avoid driving after taking",
          "Can lower blood pressure and blood sugar - monitor if on medications",
          "Avoid during pregnancy (may stimulate uterine contractions)",
          "May interact with thyroid medications (can increase T4 levels)"
        ],
        "tldr":
            "Powerful adaptogen that reduces cortisol and anxiety; best for evening use to support sleep and stress recovery.",
        "adhdMedInteractions": {
          "Adderall":
              "Helps mitigate stimulant-induced anxiety and supports sleep quality which is often disrupted by stimulants.",
          "Vyvanse":
              "Reduces evening anxiety and supports recovery from daytime stimulant use; may improve sleep onset.",
          "Ritalin":
              "Complements stimulant therapy by managing stress response and supporting evening wind-down."
        }
      },
      {
        "id": "vitamin-c",
        "name": "Vitamin C (Ascorbic Acid)",
        "category": "Vitamin",
        "dosage": "500-1000mg",
        "timeOfDay": "morning",
        "benefits": [
          "Antioxidant Protection",
          "Dopamine Synthesis",
          "Immune Support"
        ],
        "evidenceLevel": "high",
        "notes":
            "⚠️ TIMING CRITICAL: Take 1+ hours BEFORE or 4+ hours AFTER stimulant medications. Acidifies urine which increases stimulant excretion.",
        "status": "beneficial",
        "mechanismOfAction":
            "Vitamin C is a cofactor for dopamine beta-hydroxylase, the enzyme that converts dopamine to norepinephrine. It also protects catecholamines from oxidation and supports adrenal function. However, it acidifies urine which significantly increases the excretion rate of amphetamine-based stimulants.",
        "detailedBenefits": [
          "Essential cofactor for dopamine-to-norepinephrine conversion",
          "Protects neurotransmitters from oxidative degradation",
          "Supports adrenal health during chronic stress",
          "Powerful antioxidant for brain tissue protection"
        ],
        "timingRationale":
            "CRITICAL: Vitamin C acidifies urine, which increases amphetamine excretion by up to 50%. Take at least 1 hour BEFORE stimulant medication, or wait 4+ hours after. Evening dosing (after medication has worn off) is safest for those on stimulants.",
        "scientificEvidenceRank": 88,
        "studyLinks": {
          "Vitamin C and dopamine synthesis":
              "https://pubmed.ncbi.nlm.nih.gov/7002348/",
          "Urinary pH and amphetamine excretion":
              "https://pubmed.ncbi.nlm.nih.gov/7361718/",
          "Antioxidant effects in brain":
              "https://pubmed.ncbi.nlm.nih.gov/15350981/"
        },
        "dosageByWeight": {
          "40-60": "500mg",
          "60-80": "750mg",
          "80-100": "1000mg",
          "100-120": "1000-1500mg"
        },
        "dosageFrequency": "Once or twice daily, timing separated from stimulant medications",
        "dosageWarnings": [
          "⚠️ CRITICAL: Reduces effectiveness of Adderall/Vyvanse if taken together",
          "Take 1+ hours BEFORE or 4+ hours AFTER stimulant medications",
          "High doses (>2000mg) may cause GI upset or diarrhea",
          "Generally very safe; excess is excreted in urine"
        ],
        "tldr":
            "Essential for dopamine synthesis but MUST be timed carefully - acidifies urine and reduces stimulant effectiveness.",
        "adhdMedInteractions": {
          "Adderall":
              "⚠️ REDUCES EFFECTIVENESS by 30-50% if taken together. Acidifies urine, increasing amphetamine excretion. Separate by 1+ hours before or 4+ hours after.",
          "Vyvanse":
              "⚠️ REDUCES EFFECTIVENESS. Same mechanism as Adderall - increases excretion rate. Timing separation is critical.",
          "Ritalin":
              "Minimal interaction (methylphenidate excretion less pH-dependent). Can be taken together, but separation still recommended."
        }
      },
      {
        "id": "acetyl-l-carnitine",
        "name": "Acetyl-L-Carnitine (ALCAR)",
        "category": "Amino Acid",
        "dosage": "500-1500mg",
        "timeOfDay": "morning",
        "benefits": [
          "Mental Energy",
          "Acetylcholine Production",
          "Mitochondrial Function"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Crosses blood-brain barrier easily. Supports acetylcholine synthesis and mitochondrial energy production.",
        "status": "beneficial",
        "mechanismOfAction":
            "ALCAR is the acetylated form of L-carnitine that crosses the blood-brain barrier. It donates acetyl groups for acetylcholine synthesis (key neurotransmitter for attention and memory). Also transports fatty acids into mitochondria for ATP production and has neuroprotective antioxidant properties.",
        "detailedBenefits": [
          "Enhances acetylcholine synthesis for improved attention",
          "Supports mitochondrial energy production in neurons",
          "Improves mental fatigue and processing speed",
          "Neuroprotective effects against oxidative stress"
        ],
        "timingRationale":
            "Morning dosing on an empty stomach maximizes absorption. Effects are noticeable within 30-60 minutes. Avoid evening dosing as it can be energizing and may interfere with sleep. Can be taken with or without food, but absorption is slightly better on empty stomach.",
        "scientificEvidenceRank": 72,
        "studyLinks": {
          "ALCAR for cognitive function":
              "https://pubmed.ncbi.nlm.nih.gov/28178168/",
          "Acetylcholine synthesis and memory":
              "https://pubmed.ncbi.nlm.nih.gov/8739001/",
          "Mitochondrial support in aging":
              "https://pubmed.ncbi.nlm.nih.gov/18065594/"
        },
        "dosageByWeight": {
          "40-60": "500mg",
          "60-80": "750-1000mg",
          "80-100": "1000-1500mg",
          "100-120": "1500-2000mg"
        },
        "dosageFrequency": "Once or twice daily (morning, or morning + early afternoon)",
        "dosageWarnings": [
          "May be stimulating - avoid evening dosing",
          "Can cause fishy body odor in some people (rare)",
          "May lower seizure threshold in susceptible individuals",
          "Generally well-tolerated; start with lower dose"
        ],
        "tldr":
            "Supports acetylcholine synthesis and mitochondrial energy; improves mental clarity and reduces fatigue.",
        "adhdMedInteractions": {
          "Adderall":
              "Complements stimulant action by supporting acetylcholine (attention) and mitochondrial energy (sustained focus).",
          "Vyvanse":
              "May enhance cognitive benefits and reduce mental fatigue during medication offset.",
          "Ritalin":
              "Supports attention through complementary neurotransmitter system (acetylcholine vs dopamine)."
        }
      },
      {
        "id": "creatine",
        "name": "Creatine Monohydrate",
        "category": "Amino Acid",
        "dosage": "5g",
        "timeOfDay": "any",
        "benefits": [
          "Brain Energy",
          "Working Memory",
          "Mental Fatigue Resistance"
        ],
        "evidenceLevel": "high",
        "notes":
            "Monohydrate form is most researched. Supports ATP regeneration in brain cells. Particularly effective for sleep-deprived individuals.",
        "status": "beneficial",
        "mechanismOfAction":
            "Creatine phosphate serves as a rapid ATP buffer in cells with high energy demands (brain, muscles). It donates phosphate groups to regenerate ATP from ADP, providing immediate energy for cognitive tasks. Brain creatine levels correlate with working memory performance and mental fatigue resistance.",
        "detailedBenefits": [
          "Improves working memory by 10-20% in research trials",
          "Reduces mental fatigue during sustained cognitive tasks",
          "Particularly effective during sleep deprivation",
          "Supports neuroprotection and brain energy reserves"
        ],
        "timingRationale":
            "Timing is flexible - creatine works through saturation (loading brain stores over 2-4 weeks). Can be taken any time of day with or without food. Some prefer post-workout or with meals for better absorption, but consistency matters more than timing.",
        "scientificEvidenceRank": 84,
        "studyLinks": {
          "Creatine for cognitive function":
              "https://pubmed.ncbi.nlm.nih.gov/29704637/",
          "Working memory improvement":
              "https://pubmed.ncbi.nlm.nih.gov/14600563/",
          "Mental fatigue and sleep deprivation":
              "https://pubmed.ncbi.nlm.nih.gov/17828627/"
        },
        "dosageByWeight": {
          "40-60": "3-5g",
          "60-80": "5g",
          "80-100": "5-7g",
          "100-120": "7-10g"
        },
        "dosageFrequency": "Once daily, any time (consistency more important than timing)",
        "dosageWarnings": [
          "May cause mild water retention (1-2 lbs)",
          "Drink adequate water (creatine pulls water into cells)",
          "Loading phase (20g/day for 5 days) optional but not necessary",
          "Extremely safe; one of the most researched supplements"
        ],
        "tldr":
            "Supports brain ATP regeneration; improves working memory and reduces mental fatigue, especially during sleep deprivation.",
        "adhdMedInteractions": {
          "Adderall":
              "Supports brain energy reserves which may enhance sustained focus and reduce mental fatigue during medication offset.",
          "Vyvanse":
              "Complements stimulant action by providing cellular energy substrate; may improve working memory beyond stimulant effects alone.",
          "Ritalin":
              "Provides energy support for high-demand cognitive tasks; works through complementary mechanism (ATP vs dopamine)."
        }
      },
      {
        "id": "curcumin",
        "name": "Curcumin (Turmeric Extract)",
        "category": "Antioxidant",
        "dosage": "500-1000mg",
        "timeOfDay": "any",
        "benefits": [
          "Anti-Inflammatory",
          "Neuroprotection",
          "Mood Support"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Must be formulated for bioavailability (with piperine/black pepper or liposomal). Powerful anti-inflammatory for brain health.",
        "status": "beneficial",
        "mechanismOfAction":
            "Curcumin is a potent anti-inflammatory that crosses the blood-brain barrier. It inhibits NF-κB (inflammatory pathway), increases BDNF (neuroplasticity), and modulates monoamine neurotransmitters. Also has antioxidant properties that protect neurons from oxidative stress. Note: Poor bioavailability unless enhanced with piperine or liposomal delivery.",
        "detailedBenefits": [
          "Reduces neuroinflammation linked to ADHD symptoms",
          "Increases BDNF for neuroplasticity and learning",
          "Mild mood-enhancing effects (MAO inhibition)",
          "Neuroprotective against oxidative stress and aging"
        ],
        "timingRationale":
            "Flexible timing - can be taken with meals for better absorption. Fat-soluble, so taking with dietary fat enhances uptake. Divided doses (morning + evening) may maintain more stable blood levels. Effects are cumulative over weeks, not immediate.",
        "scientificEvidenceRank": 74,
        "studyLinks": {
          "Curcumin and BDNF":
              "https://pubmed.ncbi.nlm.nih.gov/23832433/",
          "Anti-inflammatory effects in brain":
              "https://pubmed.ncbi.nlm.nih.gov/17569207/",
          "Bioavailability enhancement with piperine":
              "https://pubmed.ncbi.nlm.nih.gov/9619120/"
        },
        "dosageByWeight": {
          "40-60": "500mg",
          "60-80": "750mg",
          "80-100": "1000mg",
          "100-120": "1000-1500mg"
        },
        "dosageFrequency": "Once or twice daily with meals containing fat",
        "dosageWarnings": [
          "MUST be enhanced for bioavailability (piperine, liposomal, or phytosome)",
          "May interact with blood thinners (mild anticoagulant effect)",
          "Can cause GI upset in some people - take with food",
          "Avoid high doses if you have gallbladder issues"
        ],
        "tldr":
            "Powerful anti-inflammatory and neuroprotective compound; must be formulated for absorption (with piperine or liposomal).",
        "adhdMedInteractions": {
          "Adderall":
              "Anti-inflammatory effects may support long-term brain health during chronic stimulant use; BDNF increase supports neuroplasticity.",
          "Vyvanse":
              "Neuroprotective properties may mitigate oxidative stress from stimulants; mood support can complement medication effects.",
          "Ritalin":
              "Supports brain health and reduces inflammation; may enhance long-term cognitive benefits of stimulant therapy."
        }
      },
'''

def main():
    file_path = 'lib/infrastructure/services/seeding_service.dart'
    
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the insertion point (after B-Complex closing brace, before Alpha-GPC)
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
    
    print(f"Inserting 6 new supplements at line {insertion_index + 1}")
    
    # Insert the new supplements
    lines.insert(insertion_index, NEW_SUPPLEMENTS)
    
    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print("✅ Successfully added 6 new supplements!")
    print("New supplements: Rhodiola, Ashwagandha, Vitamin C, ALCAR, Creatine, Curcumin")

if __name__ == '__main__':
    main()
