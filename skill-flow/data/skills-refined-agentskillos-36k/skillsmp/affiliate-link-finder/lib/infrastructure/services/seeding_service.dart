import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/foundation.dart';
import '../../utils/logger.dart';

class SeedingService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  Future<void> seedSupplements() async {
    final List<Map<String, dynamic>> supplements = [
      {
        "id": "omega-3",
        "name": "Omega-3 Fish Oil",
        "category": "Essential Fatty Acids",
        "dosage": "1000mg",
        "timeOfDay": "morning",
        "benefits": ["Focus", "Brain Health", "Mood"],
        "evidenceLevel": "high",
        "notes": "Take with food for better absorption",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Increases cell membrane permeability, enhances dopamine receptor density, and reduces neuroinflammation.",
        "detailedBenefits": [
          "Improves working memory by 15% in clinical trials",
          "Reduces impulsivity and emotional dysregulation",
          "Supports long-term neuroprotection"
        ],
        "timingRationale":
            "Fat-soluble nutrients require dietary fat for absorption. Taking with the largest meal (often breakfast or dinner) ensures maximum uptake.",
        "scientificEvidenceRank": 92,
        "studyLinks": {
          "Omega-3 fatty acids for ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/21961774/",
          "EPA vs DHA efficacy comparision":
              "https://pubmed.ncbi.nlm.nih.gov/31336652/"
        },
        "dosageByWeight": {
          "40-60": "500-1000mg",
          "60-80": "1000-2000mg",
          "80-100": "2000-3000mg",
          "100-120": "3000-4000mg"
        },
        "dosageFrequency": "Take once daily with a fatty meal",
        "dosageWarnings": [
          "Consult physician if taking anti-coagulants (blood thinners)",
          "Stop taking 2 weeks before scheduled surgeries",
          "High doses (>3g) may increase bleeding risk in some individuals"
        ],
        "tldr":
            "Essential fatty acids that improve dopamine receptor density and reduce brain inflammation.",
        "adhdMedInteractions": {
          "Adderall":
              "Omega-3 supports the dopamine system and may enhance the long-term effectiveness of stimulant medications.",
          "Vyvanse":
              "Supports brain health and helps smooth out potential side effects of stimulants.",
          "Ritalin":
              "Helps maintain cell membrane health vital for proper neurotransmitter transport."
        }
      },
      {
        "id": "l-theanine",
        "name": "L-Theanine",
        "category": "Nootropic",
        "dosage": "200mg",
        "timeOfDay": "morning",
        "benefits": ["Calm Focus", "Anxiety Reduction"],
        "evidenceLevel": "moderate",
        "notes": "Synergizes well with caffeine",
        "status": "beneficial",
        "focusLevel": 5,
        "mechanismOfAction":
            "Increases alpha brain wave activity (associated with relaxed alertness) and boosts GABA levels without sedation.",
        "detailedBenefits": [
          "Reduces jitteriness from stimulant medications",
          "Improves selective attention during stressful tasks",
          "Promotes relaxation without drowsiness"
        ],
        "timingRationale":
            "Best taken 30-60 minutes before focus work. Its half-life is ~3 hours, so re-dosing might be needed for long days.",
        "scientificEvidenceRank": 78,
        "studyLinks": {
          "L-theanine and caffeine synergy":
              "https://pubmed.ncbi.nlm.nih.gov/18681988/",
          "Effects on stress and cognition":
              "https://pubmed.ncbi.nlm.nih.gov/31623400/"
        },
        "adhdMedInteractions": {
          "Adderall":
              "L-Theanine can help mitigate stimulant-induced jitteriness and anxiety without reducing focus.",
          "Vyvanse":
              "Synergistic effect: promotes calm focus and may smooth out the offset 'crash' of long-acting stimulants.",
          "Ritalin":
              "Reduces irritability and helps with wind-down at the end of the day."
        },
        "dosageByWeight": {
          "40-60": "100-200mg",
          "60-80": "200mg",
          "80-100": "200-400mg",
          "100-120": "400mg"
        },
        "tldr":
            "Promotes 'calm focus' by increasing alpha brain waves and smoothing out stimulant side effects."
      },
      {
        "id": "magnesium",
        "name": "Magnesium Glycinate",
        "category": "Mineral",
        "dosage": "200mg",
        "timeOfDay": "evening",
        "benefits": ["Sleep Quality", "Muscle Relaxation", "Stress Reduction"],
        "evidenceLevel": "high",
        "notes":
            "Glycinate form preferred for better absorption and minimal GI side effects",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Acts as a natural NMDA receptor antagonist, promoting GABA activity and regulating the HPA axis. Glycinate form has superior bioavailability (80-90%) and minimal GI side effects compared to oxide or citrate forms.",
        "detailedBenefits": [
          "Improves sleep latency by 17 minutes in clinical trials",
          "Reduces cortisol levels and anxiety symptoms by 30%",
          "Supports healthy dopamine regulation and prevents stimulant tolerance",
          "Reduces muscle tension and physical restlessness"
        ],
        "timingRationale":
            "Evening dosing supports natural melatonin production and muscle relaxation before sleep. Glycinate's calming effect makes it ideal for bedtime, 1-2 hours before sleep for optimal absorption.",
        "scientificEvidenceRank": 88,
        "studyLinks": {
          "Magnesium supplementation for ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/24065783/",
          "Sleep quality improvement":
              "https://pubmed.ncbi.nlm.nih.gov/23853635/",
          "Magnesium and stress reduction":
              "https://pubmed.ncbi.nlm.nih.gov/28654669/"
        },
        "dosageByWeight": {
          "40-60": "150mg",
          "60-80": "200mg",
          "80-100": "300mg",
          "100-120": "400mg"
        },
        "dosageFrequency": "Once daily, preferably 1-2 hours before bed",
        "dosageWarnings": [
          "Start with 100mg to assess tolerance",
          "High doses (>400mg) may cause digestive discomfort",
          "Consult physician if you have kidney disease or impaired renal function",
          "Take 4+ hours after stimulant medication for optimal absorption"
        ],
        "tldr":
            "Highly bioavailable magnesium that improves sleep quality and reduces anxiety without morning grogginess.",
        "adhdMedInteractions": {
          "Adderall":
              "May help reduce muscle tension and improve sleep quality disrupted by stimulants. Take 4+ hours after medication to avoid absorption interference.",
          "Vyvanse":
              "Supports relaxation during evening comedown from long-acting stimulants. Helps prevent magnesium depletion from chronic stimulant use.",
          "Ritalin":
              "No significant interaction; beneficial for sleep support and reducing evening irritability."
        },
        "contraindications": [
          "People with kidney disease or impaired renal function",
          "Those taking magnesium-containing antacids concurrently",
          "Individuals with myasthenia gravis"
        ],
        "sideEffects": [
          "Loose stools if dose exceeds tolerance (typically >500mg)",
          "Rare: mild drowsiness if taken during the day",
          "Very rare: nausea if taken on empty stomach"
        ]
      },
      {
        "id": "vitamin-d",
        "name": "Vitamin D3",
        "category": "Vitamin",
        "dosage": "2000 IU",
        "timeOfDay": "morning",
        "benefits": ["Executive Function", "Impulse Control", "Mood Stability"],
        "evidenceLevel": "high",
        "notes":
            "Works synergistically with magnesium. Get blood levels tested (optimal: 40-60 ng/mL).",
        "status": "beneficial",
        "focusLevel": 3,
        "mechanismOfAction":
            "Acts as a neurosteroid hormone regulating synthesis of serotonin and dopamine via tyrosine hydroxylase activation. Crucial for nerve growth factor (NGF) and brain-derived neurotrophic factor (BDNF) production.",
        "detailedBenefits": [
          "Correcting deficiency can improve attention scores by 25-30%",
          "Supports overall mood stability and seasonal resilience (especially winter)",
          "Enhances structural neuroplasticity and synaptic function",
          "Reduces inflammation linked to ADHD symptoms"
        ],
        "timingRationale":
            "Vitamin D can suppress melatonin production, so it should be taken in the morning with a fatty meal to align with circadian rhythm and maximize absorption (fat-soluble vitamin).",
        "scientificEvidenceRank": 90,
        "studyLinks": {
          "Vitamin D and ADHD symptoms":
              "https://pubmed.ncbi.nlm.nih.gov/29457224/",
          "Neurosteroid effects of Vitamin D":
              "https://pubmed.ncbi.nlm.nih.gov/28582844/",
          "Vitamin D deficiency in ADHD children":
              "https://pubmed.ncbi.nlm.nih.gov/30415156/"
        },
        "dosageByWeight": {
          "40-60": "1000-2000 IU",
          "60-80": "2000-3000 IU",
          "80-100": "3000-4000 IU",
          "100-120": "4000-5000 IU"
        },
        "dosageFrequency":
            "Once daily with a fatty meal (breakfast recommended)",
        "dosageWarnings": [
          "Get blood levels tested before supplementing (test 25-OH Vitamin D)",
          "Do not exceed 10,000 IU daily without medical supervision",
          "High doses (>5000 IU) require monitoring for hypercalcemia",
          "Always take with vitamin K2 if dosing above 4000 IU to prevent calcium dysregulation"
        ],
        "tldr":
            "Essential neurosteroid that regulates dopamine and serotonin; deficiency strongly linked to ADHD symptoms.",
        "adhdMedInteractions": {
          "Adderall":
              "Vitamin D supports dopamine synthesis pathways, potentially enhancing long-term medication effectiveness. No direct interaction.",
          "Vyvanse":
              "May improve mood stability and reduce seasonal effectiveness variations. Take in morning with medication.",
          "Ritalin":
              "Supports overall neurotransmitter health. No contraindications; synergistic for cognitive function."
        },
        "contraindications": [
          "People with hypercalcemia or hyperparathyroidism",
          "Those with sarcoidosis or other granulomatous diseases",
          "Individuals taking high-dose calcium supplements without medical guidance"
        ],
        "sideEffects": [
          "Rare: nausea or constipation at very high doses (>10,000 IU)",
          "Hypercalcemia symptoms if overdosed (fatigue, confusion, excessive thirst)",
          "Generally well-tolerated at recommended doses"
        ]
      },
      {
        "id": "bacopa-monnieri",
        "name": "Bacopa Monnieri",
        "category": "Herb",
        "dosage": "300mg",
        "timeOfDay": "morning",
        "benefits": [
          "Memory Enhancement",
          "Anxiety Reduction",
          "Learning Speed"
        ],
        "evidenceLevel": "high",
        "notes":
            "Use standardized extract (50% bacosides). Takes 8-12 weeks for full cognitive benefits.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Enhances dendritic branching and synaptic communication through bacosides A and B. Modulates serotonin and dopamine while reducing cortisol. Acts as an adaptogen to buffer stress-induced cognitive decline.",
        "detailedBenefits": [
          "Improves memory consolidation and recall by 20-30% after 12 weeks",
          "Reduces anxiety without sedation (comparable to lorazepam in studies)",
          "Enhances learning speed and information processing",
          "Neuroprotective effects against oxidative stress"
        ],
        "timingRationale":
            "Morning dosing allows cumulative effects to build throughout the day. Effects are delayed (8-12 weeks) but long-lasting. Take with food to enhance absorption of fat-soluble bacosides.",
        "scientificEvidenceRank": 85,
        "studyLinks": {
          "Bacopa for cognitive enhancement":
              "https://pubmed.ncbi.nlm.nih.gov/23772955/",
          "Memory improvement in healthy adults":
              "https://pubmed.ncbi.nlm.nih.gov/18611150/",
          "Bacopa and ADHD symptoms":
              "https://pubmed.ncbi.nlm.nih.gov/24252493/"
        },
        "dosageByWeight": {
          "40-60": "200-300mg",
          "60-80": "300mg",
          "80-100": "300-450mg",
          "100-120": "450mg"
        },
        "dosageFrequency":
            "Once or twice daily with food (morning, or split AM/PM)",
        "dosageWarnings": [
          "Takes 8-12 weeks for full effects - be patient",
          "May cause mild GI upset initially (take with food)",
          "Avoid if you have bradycardia (slow heart rate)",
          "May interact with thyroid medications - consult physician"
        ],
        "tldr":
            "Ayurvedic herb that enhances memory and learning while reducing anxiety; requires 8-12 weeks for full benefits.",
        "adhdMedInteractions": {
          "Adderall":
              "Complementary for memory and learning. Bacopa's anxiolytic effects may help with stimulant-induced anxiety. No contraindications.",
          "Vyvanse":
              "May enhance cognitive benefits of medication while reducing stress. Safe combination for most users.",
          "Ritalin":
              "Synergistic for learning and memory tasks. Bacopa's calming effects balance stimulant activation."
        },
        "contraindications": [
          "People with bradycardia or heart rhythm disorders",
          "Those taking thyroid hormone medications (may alter levels)",
          "Individuals with urinary tract obstructions",
          "Pregnant or breastfeeding women (insufficient safety data)"
        ],
        "sideEffects": [
          "Mild GI upset or nausea (5-10% of users, usually resolves)",
          "Rare: fatigue or increased bowel movements",
          "Very rare: dry mouth or muscle fatigue",
          "Generally well-tolerated with food"
        ]
      },
      {
        "id": "zinc",
        "name": "Zinc (Picolinate or Glycinate)",
        "category": "Mineral",
        "dosage": "15mg",
        "timeOfDay": "any",
        "benefits": ["Impulse Control", "Attention", "Dopamine Metabolism"],
        "evidenceLevel": "moderate",
        "notes":
            "Most effective if deficient. Picolinate or glycinate forms preferred for absorption. Works synergistically with Omega-3s.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Essential cofactor for dopamine transporter (DAT) regulation and tyrosine hydroxylase activity. Modulates NMDA receptors and supports melatonin synthesis. Critical for over 300 enzymatic reactions.",
        "detailedBenefits": [
          "Reduces hyperactivity and impulsivity in zinc-deficient individuals by 30%",
          "Enhances the effectiveness of stimulant medications (lower doses may be needed)",
          "Supports immune function and gut health (important for ADHD comorbidities)",
          "Improves sleep quality through melatonin regulation"
        ],
        "timingRationale":
            "Can cause nausea on an empty stomach. Take with a solid meal, preferably lunch or dinner. Avoid taking with calcium or iron supplements (competes for absorption).",
        "scientificEvidenceRank": 78,
        "studyLinks": {
          "Zinc sulfate in ADHD treatment":
              "https://pubmed.ncbi.nlm.nih.gov/14687872/",
          "Zinc co-treatment with stimulants":
              "https://pubmed.ncbi.nlm.nih.gov/21309642/",
          "Zinc deficiency and ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/21545780/"
        },
        "dosageByWeight": {
          "40-60": "10-15mg",
          "60-80": "15-20mg",
          "80-100": "20-30mg",
          "100-120": "30-40mg"
        },
        "dosageFrequency": "Once daily with food (lunch or dinner)",
        "dosageWarnings": [
          "Do not exceed 40mg daily without medical supervision",
          "Long-term use (>50mg) can cause copper deficiency - supplement copper if needed",
          "Get serum zinc levels tested before supplementing (optimal: 80-120 μg/dL)",
          "Take 2+ hours apart from calcium, iron, or antibiotics"
        ],
        "tldr":
            "Essential mineral for dopamine regulation; deficiency common in ADHD and reduces medication effectiveness.",
        "adhdMedInteractions": {
          "Adderall":
              "Zinc enhances dopamine transporter function, potentially allowing for lower stimulant doses. May improve medication response in zinc-deficient individuals.",
          "Vyvanse":
              "Supports dopamine metabolism and may reduce tolerance development. Synergistic effect for impulse control.",
          "Ritalin":
              "Improves methylphenidate response in children with low zinc levels. Consider testing before supplementing."
        },
        "contraindications": [
          "People with Wilson's disease (copper metabolism disorder)",
          "Those taking penicillamine or other copper-chelating drugs",
          "Individuals with chronic kidney disease (without medical supervision)"
        ],
        "sideEffects": [
          "Nausea if taken on empty stomach (common)",
          "Metallic taste in mouth (occasional)",
          "Copper deficiency if high doses used long-term (>50mg for months)",
          "Rare: stomach cramps or diarrhea"
        ]
      },
      {
        "id": "ginkgo-biloba",
        "name": "Ginkgo Biloba",
        "category": "Herb",
        "dosage": "120mg",
        "timeOfDay": "morning",
        "benefits": ["Cerebral Blood Flow", "Concentration", "Mental Clarity"],
        "evidenceLevel": "moderate",
        "notes":
            "Use standardized extract (24% ginkgo flavonoids, 6% terpene lactones). More effective for inattentive type ADHD.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Increases cerebral blood flow and oxygen delivery to the brain. Acts as a potent antioxidant (flavonoids) and platelet-activating factor (PAF) antagonist. Modulates neurotransmitter systems including dopamine and norepinephrine.",
        "detailedBenefits": [
          "Improves attention and concentration in inattentive-type ADHD",
          "Enhances cerebral blood flow by 15-20%",
          "Reduces mental fatigue and brain fog",
          "Antioxidant neuroprotection against age-related cognitive decline"
        ],
        "timingRationale":
            "Morning dosing aligns with peak cognitive demands. Takes 4-6 weeks for noticeable cognitive benefits. Split dosing (AM/PM) may improve consistency of effects.",
        "scientificEvidenceRank": 72,
        "studyLinks": {
          "Ginkgo for ADHD symptoms":
              "https://pubmed.ncbi.nlm.nih.gov/11386498/",
          "Cognitive enhancement in healthy adults":
              "https://pubmed.ncbi.nlm.nih.gov/20590480/",
          "Cerebral blood flow effects":
              "https://pubmed.ncbi.nlm.nih.gov/12605619/"
        },
        "dosageByWeight": {
          "40-60": "120mg",
          "60-80": "120-240mg",
          "80-100": "240mg",
          "100-120": "240mg"
        },
        "dosageFrequency":
            "Once or twice daily with food (morning, or split AM/PM)",
        "dosageWarnings": [
          "AVOID if taking blood thinners (warfarin, aspirin, etc.) - increases bleeding risk",
          "Stop 2 weeks before surgery due to anticoagulant effects",
          "May cause headaches at higher doses (>240mg)",
          "Avoid if you have bleeding disorders or seizure history"
        ],
        "tldr":
            "Ancient herb that boosts cerebral blood flow and concentration; particularly effective for inattentive-type ADHD.",
        "adhdMedInteractions": {
          "Adderall":
              "May enhance focus benefits through improved cerebral circulation. Monitor for headaches. No direct contraindications.",
          "Vyvanse":
              "Complementary for sustained attention. Ginkgo's blood flow benefits may support medication effectiveness.",
          "Ritalin":
              "Safe combination. May help with concentration and reduce mental fatigue during medication offset."
        },
        "contraindications": [
          "People taking anticoagulants (warfarin, heparin, aspirin)",
          "Those with bleeding disorders or scheduled for surgery",
          "Individuals with seizure disorders (may lower seizure threshold)",
          "Pregnant or breastfeeding women"
        ],
        "sideEffects": [
          "Mild headache (5-10% of users, usually dose-dependent)",
          "GI upset or nausea if taken on empty stomach",
          "Rare: dizziness or allergic skin reactions",
          "Very rare: increased bleeding or bruising (stop immediately)"
        ]
      },
      {
        "id": "iron",
        "name": "Iron (Ferrous Bisglycinate)",
        "category": "Mineral",
        "dosage": "18mg",
        "timeOfDay": "any",
        "benefits": [
          "Dopamine Synthesis",
          "Oxygen Transport",
          "Energy Production"
        ],
        "evidenceLevel": "high",
        "notes":
            "⚠️ ONLY supplement if blood test confirms deficiency (ferritin <30 ng/mL). Excess iron is toxic. Bisglycinate form preferred for absorption and minimal GI upset.",
        "status": "beneficial",
        "focusLevel": 3,
        "mechanismOfAction":
            "Essential cofactor for tyrosine hydroxylase (rate-limiting enzyme in dopamine synthesis). Critical for oxygen transport via hemoglobin and myoglobin. Supports mitochondrial energy production and neurotransmitter metabolism.",
        "detailedBenefits": [
          "Correcting deficiency improves ADHD symptoms by 30-40%",
          "Supports dopamine and norepinephrine production",
          "Enhances cognitive function and reduces fatigue",
          "Improves response to stimulant medications in deficient individuals"
        ],
        "timingRationale":
            "Take on empty stomach for best absorption, or with vitamin C to enhance uptake. Avoid taking with calcium, coffee, or tea (reduces absorption). Evening dosing may reduce GI upset.",
        "scientificEvidenceRank": 82,
        "studyLinks": {
          "Iron deficiency and ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/22664333/",
          "Iron supplementation effects":
              "https://pubmed.ncbi.nlm.nih.gov/18275431/",
          "Ferritin levels in ADHD children":
              "https://pubmed.ncbi.nlm.nih.gov/15687461/"
        },
        "dosageByWeight": {
          "40-60": "10-18mg",
          "60-80": "18-27mg",
          "80-100": "27-45mg",
          "100-120": "45-65mg"
        },
        "dosageFrequency": "Once daily on empty stomach or with vitamin C",
        "dosageWarnings": [
          "⚠️ CRITICAL: Get blood test (serum ferritin) before supplementing",
          "Do NOT supplement if ferritin >30 ng/mL (excess iron is toxic)",
          "Keep out of reach of children (iron poisoning risk)",
          "Retest ferritin every 3 months while supplementing",
          "Stop if experiencing constipation, nausea, or dark stools"
        ],
        "tldr":
            "Essential for dopamine synthesis; ONLY supplement if blood test confirms deficiency (excess iron is harmful).",
        "adhdMedInteractions": {
          "Adderall":
              "Iron deficiency reduces medication effectiveness. Correcting deficiency may allow for lower stimulant doses. Take iron 2+ hours apart from medication.",
          "Vyvanse":
              "Low iron impairs dopamine synthesis needed for medication to work. Supplementation improves response in deficient individuals.",
          "Ritalin":
              "Iron is critical for dopamine pathways. Deficiency linked to poor medication response. Always test before supplementing."
        },
        "contraindications": [
          "People with hemochromatosis or iron overload disorders",
          "Those with normal or high ferritin levels (>30 ng/mL)",
          "Individuals with inflammatory bowel disease (without medical supervision)",
          "Anyone not tested for iron deficiency"
        ],
        "sideEffects": [
          "Common: constipation, dark stools, mild nausea",
          "Reduce dose or switch to bisglycinate form if GI upset occurs",
          "Rare: severe nausea or vomiting (stop immediately)",
          "Overdose risk: keep away from children"
        ]
      },
      {
        "id": "citicoline",
        "name": "Citicoline (CDP-Choline)",
        "category": "Nootropic",
        "dosage": "250mg",
        "timeOfDay": "morning",
        "benefits": ["Mental Clarity", "Sustained Attention", "Memory"],
        "evidenceLevel": "high",
        "notes":
            "Cognizin® brand is most researched. Boosts brain energy with minimal side effects.",
        "status": "beneficial",
        "focusLevel": 5,
        "mechanismOfAction":
            "Precursor to both acetylcholine (learning/memory) and phosphatidylcholine (cell membrane repair). Increases dopamine receptor density and enhances mitochondrial ATP production in the brain.",
        "detailedBenefits": [
          "Improves sustained attention and focus by 15-20% in clinical trials",
          "Enhances working memory and processing speed",
          "Supports brain energy metabolism and reduces mental fatigue",
          "Neuroprotective effects against oxidative stress"
        ],
        "timingRationale":
            "Morning dosing aligns with peak cognitive demands. Can be taken with or without food. Effects are cumulative over 4-6 weeks, with acute benefits within 1-2 hours.",
        "scientificEvidenceRank": 82,
        "studyLinks": {
          "Citicoline for attention and focus":
              "https://pubmed.ncbi.nlm.nih.gov/26179181/",
          "CDP-Choline and dopamine release":
              "https://pubmed.ncbi.nlm.nih.gov/18816480/",
          "Cognitive enhancement in adolescents":
              "https://pubmed.ncbi.nlm.nih.gov/25933483/"
        },
        "dosageByWeight": {
          "40-60": "200-250mg",
          "60-80": "250-300mg",
          "80-100": "300-500mg",
          "100-120": "500mg"
        },
        "dosageFrequency":
            "Once or twice daily (morning, or morning + early afternoon)",
        "dosageWarnings": [
          "Start with 250mg to assess tolerance",
          "Doses above 500mg may cause headaches in some individuals",
          "Take earlier in the day if it affects sleep (rare)",
          "Generally well-tolerated with minimal side effects"
        ],
        "tldr":
            "Premium nootropic that boosts brain energy, dopamine, and acetylcholine for sustained focus and mental clarity.",
        "adhdMedInteractions": {
          "Adderall":
              "Synergistic for cognitive enhancement. Citicoline supports dopamine pathways and may reduce tolerance development. No contraindications.",
          "Vyvanse":
              "Complements stimulant effects by supporting acetylcholine (learning) and brain energy. May enhance working memory benefits.",
          "Ritalin":
              "Safe combination. Citicoline provides neuroprotection and supports long-term cognitive health alongside stimulant use."
        },
        "contraindications": [
          "People with bipolar disorder (may trigger manic episodes in rare cases)",
          "Those taking anticholinergic medications",
          "Pregnant or breastfeeding women (insufficient safety data)"
        ],
        "sideEffects": [
          "Rare: mild headache (usually resolves with lower dose)",
          "Occasional: digestive upset if taken on empty stomach",
          "Very rare: insomnia if taken late in the day",
          "Generally one of the safest nootropics available"
        ]
      },
      {
        "id": "lions-mane",
        "name": "Lion's Mane Mushroom",
        "category": "Mushroom",
        "dosage": "1000mg",
        "timeOfDay": "morning",
        "benefits": ["Neurogenesis", "Cognitive Function", "Neuroprotection"],
        "evidenceLevel": "moderate",
        "notes":
            "Stimulates nerve growth factor (NGF) and brain-derived neurotrophic factor (BDNF). Effects build over 4-8 weeks.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Stimulates synthesis of nerve growth factor (NGF) and BDNF through hericenones and erinacines. Promotes neurogenesis, myelination, and synaptic plasticity. Supports hippocampal function critical for memory.",
        "detailedBenefits": [
          "Enhances neuroplasticity and cognitive flexibility",
          "Supports focus and mental clarity without stimulation",
          "Neuroprotective against cognitive decline",
          "May improve mood and reduce anxiety through NGF pathways"
        ],
        "timingRationale":
            "Morning dosing supports daytime cognitive function. Effects are cumulative over 4-8 weeks. Can be taken with or without food, though absorption may be enhanced with fats.",
        "scientificEvidenceRank": 70,
        "studyLinks": {
          "Lion's Mane and cognitive function":
              "https://pubmed.ncbi.nlm.nih.gov/31881712/",
          "NGF stimulation effects":
              "https://pubmed.ncbi.nlm.nih.gov/23510212/",
          "Neuroprotective properties":
              "https://pubmed.ncbi.nlm.nih.gov/24266378/"
        },
        "dosageByWeight": {
          "40-60": "500-1000mg",
          "60-80": "1000mg",
          "80-100": "1000-1500mg",
          "100-120": "1500-2000mg"
        },
        "dosageFrequency":
            "Once or twice daily with food (morning, or split AM/PM)",
        "dosageWarnings": [
          "Start with 500mg to assess tolerance",
          "Effects are cumulative - allow 4-8 weeks for full benefits",
          "May cause mild GI upset initially (take with food)",
          "Consult physician if you have mushroom allergies"
        ],
        "tldr":
            "Medicinal mushroom that stimulates nerve growth factor for enhanced neuroplasticity and cognitive function.",
        "adhdMedInteractions": {
          "Adderall":
              "Complementary for cognitive enhancement and neuroprotection. Lion's Mane supports brain health alongside stimulant use. No contraindications.",
          "Vyvanse":
              "May enhance long-term cognitive benefits and support neuroplasticity. Safe combination.",
          "Ritalin":
              "Synergistic for focus and mental clarity. Lion's Mane provides neuroprotective benefits during chronic stimulant use."
        },
        "contraindications": [
          "People with mushroom allergies (rare but possible)",
          "Those with bleeding disorders (theoretical risk, monitor)",
          "Pregnant or breastfeeding women (insufficient safety data)"
        ],
        "sideEffects": [
          "Rare: mild GI upset or skin rash (allergic reaction)",
          "Very rare: respiratory difficulty (stop immediately if occurs)",
          "Generally well-tolerated with minimal side effects"
        ]
      },
      {
        "id": "phosphatidylserine",
        "name": "Phosphatidylserine (PS)",
        "category": "Lipid",
        "dosage": "100mg",
        "timeOfDay": "any",
        "benefits": ["Working Memory", "Attention", "Cognitive Processing"],
        "evidenceLevel": "high",
        "notes":
            "Phospholipid essential for cell membrane function. Soy-free (sunflower-derived) preferred for allergen concerns.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Critical phospholipid component of neuronal cell membranes. Supports neurotransmitter receptor function, particularly acetylcholine. Modulates cortisol response and supports healthy HPA axis function. Enhances glucose metabolism in the brain.",
        "detailedBenefits": [
          "Improves working memory and information processing by 15-20%",
          "Enhances attention and reduces distractibility in ADHD",
          "Reduces cortisol levels and stress-induced cognitive impairment",
          "Supports age-related cognitive maintenance"
        ],
        "timingRationale":
            "Can be taken any time of day with food for optimal absorption (fat-soluble). Some prefer evening dosing for cortisol-lowering effects, but morning works well for cognitive support.",
        "scientificEvidenceRank": 80,
        "studyLinks": {
          "Phosphatidylserine for ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/24424348/",
          "Cognitive function improvement":
              "https://pubmed.ncbi.nlm.nih.gov/25933483/",
          "Cortisol modulation effects":
              "https://pubmed.ncbi.nlm.nih.gov/18296328/"
        },
        "dosageByWeight": {
          "40-60": "100mg",
          "60-80": "100-200mg",
          "80-100": "200-300mg",
          "100-120": "300mg"
        },
        "dosageFrequency":
            "Once or twice daily with fatty meals (morning and/or evening)",
        "dosageWarnings": [
          "Start with 100mg to assess tolerance",
          "Take with food containing fat for optimal absorption",
          "May cause mild insomnia if taken late (rare)",
          "Choose sunflower-derived PS if you have soy allergies"
        ],
        "tldr":
            "Essential brain phospholipid that enhances working memory, attention, and stress resilience in ADHD.",
        "adhdMedInteractions": {
          "Adderall":
              "Synergistic for cognitive function. PS supports cell membrane health critical for neurotransmitter signaling. May reduce cortisol elevation from stimulants.",
          "Vyvanse":
              "Complementary for working memory and attention. PS may help buffer stress response during medication use.",
          "Ritalin":
              "Safe combination. PS supports the cellular mechanisms that stimulants rely on for effectiveness."
        },
        "contraindications": [
          "People with soy allergies (use sunflower-derived PS)",
          "Those taking anticholinergic medications (theoretical interaction)",
          "Pregnant or breastfeeding women (insufficient safety data)"
        ],
        "sideEffects": [
          "Rare: mild GI upset or insomnia (if taken late)",
          "Very rare: headache at high doses (>300mg)",
          "Generally well-tolerated with minimal side effects"
        ]
      },
      {
        "id": "saffron",
        "name": "Saffron (Crocus Sativus)",
        "category": "Herb",
        "dosage": "30mg",
        "timeOfDay": "morning",
        "benefits": ["Impulsivity Reduction", "Mood Stability", "Attention"],
        "evidenceLevel": "moderate",
        "notes":
            "Use standardized extract (safranal 2%, crocin 30%). Emerging evidence shows comparable efficacy to methylphenidate in some studies.",
        "status": "beneficial",
        "focusLevel": 5,
        "mechanismOfAction":
            "Modulates serotonin, dopamine, and norepinephrine through crocin and safranal compounds. Acts as a mild NMDA receptor antagonist and enhances BDNF expression. Anti-inflammatory effects support neuronal health.",
        "detailedBenefits": [
          "Reduces impulsivity and hyperactivity comparable to low-dose methylphenidate",
          "Improves mood and reduces anxiety without sedation",
          "Enhances attention span and reduces distractibility",
          "Neuroprotective and anti-inflammatory properties"
        ],
        "timingRationale":
            "Morning dosing aligns with peak symptom periods. Effects build over 6-8 weeks. Can be taken with or without food, though absorption may be enhanced with fats.",
        "scientificEvidenceRank": 68,
        "studyLinks": {
          "Saffron vs methylphenidate for ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/30895760/",
          "Saffron for ADHD symptoms":
              "https://pubmed.ncbi.nlm.nih.gov/31453656/",
          "Mood and cognitive effects":
              "https://pubmed.ncbi.nlm.nih.gov/28527220/"
        },
        "dosageByWeight": {
          "40-60": "15-30mg",
          "60-80": "30mg",
          "80-100": "30mg",
          "100-120": "30mg"
        },
        "dosageFrequency": "Once or twice daily (morning, or split AM/PM)",
        "dosageWarnings": [
          "Do not exceed 30mg daily (higher doses may cause side effects)",
          "Takes 6-8 weeks for full therapeutic effects",
          "Avoid during pregnancy (may stimulate uterine contractions)",
          "May interact with blood pressure medications"
        ],
        "tldr":
            "Emerging ADHD treatment with mood-stabilizing effects; some studies show efficacy comparable to low-dose stimulants.",
        "adhdMedInteractions": {
          "Adderall":
              "May provide complementary mood support. No known contraindications, but monitor for additive effects on mood.",
          "Vyvanse":
              "Saffron's mood-stabilizing effects may complement stimulant therapy. Safe combination for most users.",
          "Ritalin":
              "Some studies suggest saffron alone has comparable efficacy to low-dose methylphenidate. Can be used together under medical supervision."
        },
        "contraindications": [
          "Pregnant or breastfeeding women (may cause uterine contractions)",
          "People with bipolar disorder (may trigger manic episodes)",
          "Those taking blood pressure medications (may enhance effects)",
          "Individuals with bleeding disorders (theoretical risk)"
        ],
        "sideEffects": [
          "Rare: mild nausea or headache at higher doses (>30mg)",
          "Very rare: dizziness or dry mouth",
          "Generally well-tolerated at recommended doses",
          "No significant side effects in most clinical trials"
        ]
      },
      {
        "id": "pycnogenol",
        "name": "Pycnogenol (Pine Bark Extract)",
        "category": "Antioxidant",
        "dosage": "1mg/kg",
        "timeOfDay": "morning",
        "benefits": [
          "Attention",
          "Hyperactivity Reduction",
          "Oxidative Stress"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Standardized French maritime pine bark extract. Requires 8-12 weeks for full cognitive benefits.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Potent antioxidant containing proanthocyanidins that cross the blood-brain barrier. Enhances nitric oxide production for improved cerebral blood flow. Modulates dopamine and norepinephrine metabolism while reducing oxidative stress.",
        "detailedBenefits": [
          "Reduces hyperactivity and improves attention by 20-30% in clinical trials",
          "Enhances antioxidant capacity and reduces neuroinflammation",
          "Improves concentration and visual-motor coordination",
          "May reduce need for stimulant medication in some cases"
        ],
        "timingRationale":
            "Morning dosing supports daytime cognitive function. Effects are cumulative over 8-12 weeks. Take with food to enhance absorption and reduce GI upset.",
        "scientificEvidenceRank": 75,
        "studyLinks": {
          "Pycnogenol for ADHD in children":
              "https://pubmed.ncbi.nlm.nih.gov/16499493/",
          "Attention and hyperactivity improvement":
              "https://pubmed.ncbi.nlm.nih.gov/17063641/",
          "Antioxidant effects on cognition":
              "https://pubmed.ncbi.nlm.nih.gov/22214254/"
        },
        "dosageByWeight": {
          "40-60": "40-60mg",
          "60-80": "60-80mg",
          "80-100": "80-100mg",
          "100-120": "100-120mg"
        },
        "dosageFrequency":
            "Once or twice daily with food (morning, or split AM/PM)",
        "dosageWarnings": [
          "Calculate dose as 1mg per kg of body weight",
          "Takes 8-12 weeks for full therapeutic effects",
          "May enhance effects of blood thinners (monitor if on anticoagulants)",
          "Start with half dose to assess tolerance"
        ],
        "tldr":
            "Powerful antioxidant from pine bark that reduces hyperactivity and improves attention through enhanced blood flow.",
        "adhdMedInteractions": {
          "Adderall":
              "Complementary antioxidant support. May help reduce oxidative stress from chronic stimulant use. No contraindications.",
          "Vyvanse":
              "Synergistic for attention and focus. Pycnogenol's blood flow benefits may enhance medication effectiveness.",
          "Ritalin":
              "Some studies suggest Pycnogenol may reduce need for medication in mild cases. Can be used together safely."
        },
        "contraindications": [
          "People taking blood thinners (may enhance anticoagulant effects)",
          "Those with autoimmune conditions (may stimulate immune system)",
          "Individuals scheduled for surgery (stop 2 weeks prior)",
          "Pregnant or breastfeeding women (insufficient safety data)"
        ],
        "sideEffects": [
          "Rare: mild GI upset, nausea, or headache",
          "Very rare: dizziness or mouth ulcers",
          "Generally well-tolerated with minimal side effects",
          "No serious adverse events in clinical trials"
        ]
      },
      {
        "id": "probiotics",
        "name": "Probiotics (Multi-Strain)",
        "category": "Probiotic",
        "dosage": "10-20 billion CFU",
        "timeOfDay": "morning",
        "benefits": ["Gut-Brain Axis", "Mood Regulation", "Immune Support"],
        "evidenceLevel": "moderate",
        "notes":
            "Focus on Lactobacillus and Bifidobacterium strains. Supports microbiome diversity and neurotransmitter production (serotonin, GABA, dopamine).",
        "status": "beneficial",
        "focusLevel": 3,
        "mechanismOfAction":
            "Modulates gut-brain axis through vagus nerve signaling and neurotransmitter production. Beneficial bacteria produce GABA, serotonin precursors, and short-chain fatty acids that influence brain function. Reduces inflammation and supports immune regulation.",
        "detailedBenefits": [
          "Improves mood and reduces anxiety through gut-brain communication",
          "Supports production of neurotransmitters (90% of serotonin made in gut)",
          "Reduces inflammation linked to ADHD symptoms",
          "Enhances nutrient absorption critical for brain health"
        ],
        "timingRationale":
            "Morning dosing on empty stomach (30 min before food) maximizes survival through stomach acid. Consistent daily use builds healthy microbiome over 4-8 weeks.",
        "scientificEvidenceRank": 65,
        "studyLinks": {
          "Probiotics and ADHD symptoms":
              "https://pubmed.ncbi.nlm.nih.gov/31665527/",
          "Gut-brain axis in neurodevelopment":
              "https://pubmed.ncbi.nlm.nih.gov/30356668/",
          "Microbiome and mental health":
              "https://pubmed.ncbi.nlm.nih.gov/31758907/"
        },
        "dosageByWeight": {
          "40-60": "10 billion CFU",
          "60-80": "15 billion CFU",
          "80-100": "20 billion CFU",
          "100-120": "25 billion CFU"
        },
        "dosageFrequency":
            "Once daily on empty stomach (30 min before breakfast)",
        "dosageWarnings": [
          "Start with lower dose (5 billion CFU) to assess tolerance",
          "May cause temporary bloating or gas (usually resolves in 1-2 weeks)",
          "Refrigerate to maintain potency (check product requirements)",
          "Choose multi-strain formulas with Lactobacillus and Bifidobacterium"
        ],
        "tldr":
            "Beneficial bacteria that support gut-brain communication, mood regulation, and neurotransmitter production.",
        "adhdMedInteractions": {
          "Adderall":
              "Supports gut health which may be affected by stimulants. Probiotics help maintain healthy digestion and nutrient absorption. No contraindications.",
          "Vyvanse":
              "May help with GI side effects common with stimulants. Supports overall health and neurotransmitter balance.",
          "Ritalin":
              "Complementary for gut health and mood support. Safe combination with no known interactions."
        },
        "contraindications": [
          "People with severely compromised immune systems (consult physician)",
          "Those with central venous catheters or serious illness",
          "Individuals with short bowel syndrome (rare risk of infection)",
          "Generally safe for most people"
        ],
        "sideEffects": [
          "Common initially: mild bloating, gas, or digestive changes (1-2 weeks)",
          "Rare: allergic reaction to specific strains",
          "Very rare: infection in immunocompromised individuals",
          "Generally well-tolerated with minimal side effects"
        ]
      },
      {
        "id": "red-dye-40",
        "name": "Red Dye 40 (Allura Red AC / E129)",
        "category": "Artificial Color",
        "description":
            "Synthetic petroleum-based food dye linked to significant behavioral problems in ADHD. One of the 'Southampton Six' requiring warning labels in the EU.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Artificial dyes have been shown to trigger histamine release and may interfere with zinc metabolism. Zinc is a critical cofactor for neurotransmitter synthesis; its depletion can directly worsen hyperactivity and impulsivity in ADHD-sensitive individuals.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Consumption should be eliminated to avoid behavioral flares.",
        "scientificEvidenceRank": 75,
        "studyLinks": {
          "Food additives and hyperactivity (Southampton)":
              "https://pubmed.ncbi.nlm.nih.gov/17825405/",
          "Artificial colors and ADHD meta-analysis":
              "https://pubmed.ncbi.nlm.nih.gov/22331014/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Linked to increased hyperactivity in sensitive children",
          "May cause allergic reactions or skin sensitivity",
          "Listed as Allura Red AC or E129 on international labels",
          "Common in bright red snacks, cereals, and soft drinks"
        ],
        "tldr":
            "Synthetic red dye with high clinical evidence for worsening ADHD hyperactivity and impulsivity.",
        "adhdMedInteractions": {
          "Adderall":
              "CRITICAL: May counter-act the focus benefits of medication by increasing distractibility and restlessness.",
          "Vyvanse":
              "Avoid: Can trigger behavioral flares that mask medication efficacy.",
          "Ritalin":
              "Compromises impulse control, directly opposing the therapeutic goals of stimulant treatment."
        }
      },
      {
        "id": "high-fructose-corn-syrup",
        "name": "High Fructose Corn Syrup (HFCS)",
        "category": "Sweetener",
        "description":
            "Highly processed sweetener that causes rapid blood sugar spikes and crashes, worsening ADHD symptoms. Found in sodas, processed foods, and many packaged snacks.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "HFCS induces rapid insulin release leading to significant blood sugar fluctuations. The subsequent hypoglycemic 'crash' can temporarily deplete neurotransmitter reserves and cause intense brain fog, irritability, and worsened impulsivity in ADHD individuals.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Consumption leads to neuro-energetic instability.",
        "scientificEvidenceRank": 70,
        "studyLinks": {
          "Sugar consumption and ADHD behavior":
              "https://pubmed.ncbi.nlm.nih.gov/21129940/",
          "Sucrose vs HFCS in cognitive health":
              "https://pubmed.ncbi.nlm.nih.gov/16507461/"
        },
        "dosageByWeight": {
          "40-60": "0g (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Causes rapid blood sugar spikes followed by crashes",
          "Increases brain fog and difficulty concentrating",
          "Can lead to significant mood volatility",
          "Linked to systemic inflammation and metabolic stress"
        ],
        "tldr":
            "Processed sweetener causing blood sugar crashes and brain fog; avoid for stable energy and focus.",
        "adhdMedInteractions": {
          "Adderall":
              "WORSENS CRASH: Blood sugar drops from HFCS can exacerbate the afternoon 'crash' of stimulant medications.",
          "Vyvanse":
              "May cause erratic energy levels that make medication focus feel inconsistent.",
          "Ritalin":
              "Directly opposes the calming of hyperactivity due to blood sugar spikes."
        }
      },
      {
        "id": "sodium-benzoate",
        "name": "Sodium Benzoate (E211)",
        "category": "Preservative",
        "description":
            "Common preservative in soft drinks and processed foods that may increase hyperactivity when combined with artificial colors. Particularly problematic for children with ADHD.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Sodium benzoate (E211) can cross the blood-brain barrier and has been shown to increase hyperactivity in its own right. It may interfere with mitochondrial function and potentially induce oxidative stress in the hippocampus.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Preservative with recognized behavioral impact.",
        "scientificEvidenceRank": 68,
        "studyLinks": {
          "Sodium benzoate and hyperactivity (Lancet)":
              "https://pubmed.ncbi.nlm.nih.gov/17825405/",
          "Cellular impact of food preservatives":
              "https://pubmed.ncbi.nlm.nih.gov/22331014/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Significantly amplifies the hyperactivity effects of synthetic food dyes",
          "May cause allergic flares or skin irritation in sensitive people",
          "Listed as Sodium Benzoate or E211",
          "Check for 'sodium benzoate' in sodas and condiments"
        ],
        "tldr":
            "Preservative linked to hyperactivity, especially when consumed with dyes; eliminate to reduce restlessness.",
        "adhdMedInteractions": {
          "Adderall":
              "May increase motor hyperactivity and reduce 'calm' focus window.",
          "Vyvanse":
              "Avoid: Can trigger erratic behavioral responses that interfere with medication effect.",
          "Ritalin":
              "Directly opposes the therapeutic target of reducing hyperactivity."
        }
      },
      {
        "id": "l-tyrosine",
        "name": "L-Tyrosine",
        "category": "Amino Acid",
        "dosage": "500mg",
        "timeOfDay": "morning",
        "benefits": ["Dopamine Precursor", "Stress Resilience", "Acute Focus"],
        "evidenceLevel": "moderate",
        "notes":
            "Building block for dopamine, norepinephrine, and epinephrine. Best for acute stress situations rather than chronic daily use due to tolerance.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Converts to L-DOPA via tyrosine hydroxylase enzyme, then to dopamine. Supports catecholamine synthesis under stress conditions when demand exceeds supply.",
        "detailedBenefits": [
          "Improves cognitive performance under acute stress",
          "Supports dopamine production when depleted",
          "May enhance working memory during demanding tasks",
          "Provides building blocks for stress hormone synthesis"
        ],
        "timingRationale":
            "Take on empty stomach before demanding tasks for maximum absorption. Competes with other amino acids for transport, so avoid taking with protein meals.",
        "scientificEvidenceRank": 65,
        "studyLinks": {
          "Tyrosine for cognitive performance":
              "https://pubmed.ncbi.nlm.nih.gov/25797188/",
          "Stress and working memory":
              "https://pubmed.ncbi.nlm.nih.gov/10688423/"
        },
        "dosageByWeight": {
          "40-60": "500-1000mg",
          "60-80": "1000-1500mg",
          "80-100": "1500-2000mg",
          "100-120": "2000mg"
        },
        "dosageFrequency":
            "Once or split doses before demanding tasks (not daily)",
        "dosageWarnings": [
          "Take on empty stomach for best absorption",
          "Tolerance develops within 6 weeks with daily use",
          "Not recommended for chronic daily supplementation",
          "Take separately from ADHD stimulants (competes for absorption)"
        ],
        "tldr":
            "Dopamine precursor amino acid; best for acute stress situations rather than daily use due to tolerance.",
        "adhdMedInteractions": {
          "Adderall":
              "Take 2+ hours apart from medication (competes for absorption). Works synergistically with iron and B6 (cofactors for conversion).",
          "Vyvanse":
              "Separate timing from medication. May provide additional dopamine support during high-stress periods.",
          "Ritalin":
              "Avoid taking simultaneously. Best used on days off medication or hours apart."
        },
        "contraindications": [
          "People with hyperthyroidism (tyrosine is a thyroid hormone precursor)",
          "Those taking MAO inhibitors",
          "Individuals with melanoma (theoretical risk)",
          "Pregnant or breastfeeding women"
        ],
        "sideEffects": [
          "Rare: headache or nausea at high doses",
          "Possible: irritability or anxiety if overstimulated",
          "Tolerance develops quickly with daily use",
          "Generally safe at recommended doses"
        ]
      },
      {
        "id": "b-complex",
        "name": "Vitamin B Complex (Methylated)",
        "category": "Vitamin",
        "dosage": "50mg",
        "timeOfDay": "morning",
        "benefits": [
          "Neurotransmitter Synthesis",
          "Energy Production",
          "Methylation Support"
        ],
        "evidenceLevel": "high",
        "notes":
            "Methylated form (methylfolate, methylcobalamin) preferred. Essential cofactors for dopamine production.",
        "status": "beneficial",
        "focusLevel": 3,
        "mechanismOfAction":
            "B vitamins serve as essential cofactors for enzymes involved in dopamine, norepinephrine, and serotonin synthesis. Methylated forms (L-methylfolate, methylcobalamin) bypass genetic polymorphisms (MTHFR) that impair folate metabolism in 40-60% of the population.",
        "detailedBenefits": [
          "B6 (P5P) converts L-DOPA to dopamine via aromatic L-amino acid decarboxylase",
          "B9 (methylfolate) supports BH4 synthesis, required for tyrosine hydroxylase",
          "B12 (methylcobalamin) maintains myelin and supports methylation cycles",
          "Reduces homocysteine levels which can impair cognitive function"
        ],
        "timingRationale":
            "Morning dosing aligns with peak dopamine synthesis needs. B vitamins are water-soluble and absorbed quickly (30-60 min). Avoid evening dosing as B vitamins can be energizing and may interfere with sleep.",
        "scientificEvidenceRank": 85,
        "studyLinks": {
          "B vitamins and ADHD symptoms":
              "https://pubmed.ncbi.nlm.nih.gov/27521327/",
          "Methylfolate in ADHD with MTHFR polymorphism":
              "https://pubmed.ncbi.nlm.nih.gov/24284437/",
          "B6 and neurotransmitter synthesis":
              "https://pubmed.ncbi.nlm.nih.gov/18950248/"
        },
        "dosageByWeight": {
          "40-60": "25-50mg B-complex",
          "60-80": "50mg B-complex",
          "80-100": "50-100mg B-complex",
          "100-120": "100mg B-complex"
        },
        "dosageFrequency": "Once daily with breakfast",
        "dosageWarnings": [
          "High-dose B6 (\u003e100mg long-term) may cause peripheral neuropathy",
          "Niacin (B3) may cause flushing; use 'flush-free' forms if sensitive",
          "Methylated forms preferred for those with MTHFR mutations"
        ],
        "tldr":
            "Essential cofactors for neurotransmitter synthesis; methylated forms support dopamine production and bypass genetic limitations.",
        "adhdMedInteractions": {
          "Adderall":
              "B vitamins support the synthesis pathways that stimulants depend on; may enhance medication effectiveness over time.",
          "Vyvanse":
              "Supports conversion of lisdexamfetamine to active d-amphetamine; helps maintain neurotransmitter reserves.",
          "Ritalin":
              "Methylfolate supports BH4 synthesis which is required for dopamine production that methylphenidate enhances."
        }
      },
      {
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
        "focusLevel": 5,
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
        },
        "contraindications": [
          "People with bipolar disorder (may trigger manic episodes)",
          "Those taking MAO inhibitors",
          "Pregnant or breastfeeding women (insufficient safety data)"
        ],
        "sideEffects": [
          "Rare: mild jitteriness or overstimulation",
          "Possible: dry mouth or dizziness",
          "Very rare: agitation in bipolar individuals",
          "Generally well-tolerated at recommended doses"
        ]
      },
      {
        "id": "ashwagandha",
        "name": "Ashwagandha (KSM-66)",
        "category": "Adaptogen",
        "dosage": "300-600mg",
        "timeOfDay": "evening",
        "benefits": ["Stress Reduction", "Anxiety Management", "Sleep Quality"],
        "evidenceLevel": "high",
        "notes":
            "KSM-66 or Sensoril extracts preferred. Reduces cortisol and anxiety. Best for evening use due to calming effects.",
        "status": "beneficial",
        "focusLevel": 3,
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
        "dosageFrequency":
            "Once daily in the evening, or split into morning/evening doses",
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
        "focusLevel": 3,
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
        "dosageFrequency":
            "Once or twice daily, timing separated from stimulant medications",
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
          "Inattentive-Type ADHD"
        ],
        "evidenceLevel": "high",
        "notes":
            "Crosses blood-brain barrier to enhance mitochondrial energy and increase dopamine. Significant benefit specifically for inattentive subtype ADHD.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "ALCAR is the acetylated form of L-carnitine that crosses the blood-brain barrier. It donates acetyl groups for acetylcholine synthesis (key neurotransmitter for attention and memory). Also transports fatty acids into mitochondria for ATP production and provides neuroprotective benefits.",
        "detailedBenefits": [
          "Enhances acetylcholine synthesis for improved attention",
          "Reduces inattentive-type symptoms by 20-30% in trials",
          "Supports mitochondrial energy production in neurons",
          "Improves mental fatigue and processing speed"
        ],
        "timingRationale":
            "Morning dosing on an empty stomach maximizes absorption. Effects are noticeable within 30-60 minutes. Avoid evening dosing as it can be energizing and may interfere with sleep.",
        "scientificEvidenceRank": 78,
        "studyLinks": {
          "ALCAR for ADHD inattentive type":
              "https://pubmed.ncbi.nlm.nih.gov/17444943/",
          "ALCAR for cognitive function":
              "https://pubmed.ncbi.nlm.nih.gov/28178168/",
          "Mitochondrial support in aging":
              "https://pubmed.ncbi.nlm.nih.gov/18065594/"
        },
        "dosageByWeight": {
          "40-60": "500-1000mg",
          "60-80": "750-1000mg",
          "80-100": "1000-1500mg",
          "100-120": "1500-2000mg"
        },
        "dosageFrequency":
            "Once or twice daily (morning, or morning + early afternoon)",
        "dosageWarnings": [
          "Most effective for inattentive-type ADHD specifically",
          "May be stimulating - avoid evening dosing",
          "High doses (>2000mg) may cause fishy body odor (rare)",
          "Start with 500mg to assess cognitive tolerance"
        ],
        "tldr":
            "Supports brain energy and acetylcholine; particularly researched for the inattentive subtype of ADHD.",
        "adhdMedInteractions": {
          "Adderall":
              "Complements stimulant action by supporting acetylcholine (attention) and mitochondrial energy (sustained focus).",
          "Vyvanse":
              "May enhance cognitive benefits and reduce mental fatigue during medication offset.",
          "Ritalin":
              "Supports attention through complementary neurotransmitter system (acetylcholine vs dopamine)."
        },
        "contraindications": [
          "People with seizure disorders (theoretical risk)",
          "Those with thyroid hormone issues (may increase thyroid activity)",
          "Individuals with fishy body odor (TMAU condition)"
        ],
        "sideEffects": [
          "Occasional: fishy body odor at high doses (>2000mg)",
          "Rare: mild GI upset or nausea",
          "Possible: increased energy/restlessness",
          "Generally well-tolerated at recommended doses"
        ]
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
        "focusLevel": 3,
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
        "dosageFrequency":
            "Once daily, any time (consistency more important than timing)",
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
        "benefits": ["Anti-Inflammatory", "Neuroprotection", "Mood Support"],
        "evidenceLevel": "moderate",
        "notes":
            "Must be formulated for bioavailability (with piperine/black pepper or liposomal). Powerful anti-inflammatory for brain health.",
        "status": "beneficial",
        "focusLevel": 3,
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
          "Curcumin and BDNF": "https://pubmed.ncbi.nlm.nih.gov/23832433/",
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
      {
        "id": "green-tea-extract",
        "name": "Green Tea Extract (EGCG)",
        "category": "Antioxidant",
        "dosage": "250-500mg EGCG",
        "timeOfDay": "morning",
        "benefits": ["Focus Enhancement", "Neuroprotection", "Fat Oxidation"],
        "evidenceLevel": "moderate",
        "notes":
            "Standardized to 50% EGCG (epigallocatechin gallate). Contains L-theanine naturally. Avoid high doses on empty stomach.",
        "status": "beneficial",
        "focusLevel": 3,
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
        "focusLevel": 3,
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
        "dosageFrequency":
            "Once or twice daily on empty stomach (30 min before meals)",
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
        },
        "contraindications": [
          "People with asthma (may trigger bronchospasm in rare cases)",
          "Those with bleeding disorders (theoretical risk)",
          "Pregnant or breastfeeding women (consult physician)"
        ],
        "sideEffects": [
          "Common: sulfur smell/taste (normal, not harmful)",
          "Occasional: mild nausea or GI upset (take with food)",
          "Rare: skin rash or allergic reaction",
          "Generally safe and well-tolerated"
        ]
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
        "focusLevel": 3,
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
          "Neuroprotective effects": "https://pubmed.ncbi.nlm.nih.gov/18611150/"
        },
        "dosageByWeight": {
          "40-60": "50mcg",
          "60-80": "100mcg",
          "80-100": "150mcg",
          "100-120": "200mcg"
        },
        "dosageFrequency":
            "Once daily in morning, cycle 5 days on / 2 days off",
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
        "focusLevel": 3,
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
        "benefits": ["Dopamine Precursor", "Mood Enhancement", "Motivation"],
        "evidenceLevel": "moderate",
        "notes":
            "⚠️ Natural source of L-DOPA (dopamine precursor). Use cautiously - can deplete dopamine with chronic use. Cycle recommended.",
        "status": "beneficial",
        "focusLevel": 2,
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
          "Neuroprotective effects": "https://pubmed.ncbi.nlm.nih.gov/23675006/"
        },
        "dosageByWeight": {
          "40-60": "300mg (15% L-DOPA extract)",
          "60-80": "400mg",
          "80-100": "500mg",
          "100-120": "500-600mg"
        },
        "dosageFrequency":
            "Once daily on empty stomach, CYCLE 3-5 days on / 2-3 days off",
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
      {
        "id": "alpha-gpc",
        "name": "Alpha-GPC",
        "category": "Nootropic",
        "dosage": "300-600mg",
        "timeOfDay": "morning",
        "benefits": [
          "Working Memory",
          "Acetylcholine Production",
          "Mental Clarity"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Premium choline source, highly bioavailable. Supports working memory and attention. Crosses blood-brain barrier efficiently.",
        "status": "beneficial",
        "focusLevel": 5,
        "mechanismOfAction":
            "Alpha-GPC (L-alpha glycerylphosphorylcholine) is a highly bioavailable choline compound that crosses the blood-brain barrier efficiently. It serves as a precursor to acetylcholine, the neurotransmitter critical for attention, memory, and learning. Also increases growth hormone release and supports cell membrane phospholipid synthesis.",
        "detailedBenefits": [
          "Increases acetylcholine levels by 40-50% within 1-3 hours",
          "Improves working memory and recall in clinical trials",
          "Enhances focus and mental clarity during cognitive tasks",
          "Supports neuroplasticity and learning capacity"
        ],
        "timingRationale":
            "Morning or pre-cognitive task dosing is optimal. Effects peak within 1-3 hours. Can be taken with or without food. Some people split dose (morning + afternoon) for sustained acetylcholine support. Avoid evening dosing as it may interfere with sleep in sensitive individuals.",
        "scientificEvidenceRank": 78,
        "studyLinks": {
          "Alpha-GPC for cognitive enhancement":
              "https://pubmed.ncbi.nlm.nih.gov/12637119/",
          "Working memory and attention":
              "https://pubmed.ncbi.nlm.nih.gov/21156470/",
          "Acetylcholine synthesis mechanism":
              "https://pubmed.ncbi.nlm.nih.gov/14675803/"
        },
        "dosageByWeight": {
          "40-60": "300mg",
          "60-80": "400-500mg",
          "80-100": "500-600mg",
          "100-120": "600mg"
        },
        "dosageFrequency":
            "Once or twice daily (morning, or morning + afternoon)",
        "dosageWarnings": [
          "Generally very safe with minimal side effects",
          "May cause headaches in some people (sign of excess acetylcholine)",
          "Can cause GI upset at high doses - take with food if needed",
          "More expensive than other choline sources but better bioavailability"
        ],
        "tldr":
            "Premium, highly bioavailable choline source for acetylcholine synthesis; improves working memory and attention.",
        "adhdMedInteractions": {
          "Adderall":
              "Complementary mechanism - supports acetylcholine (attention/memory) while stimulants enhance dopamine (motivation/focus).",
          "Vyvanse":
              "May enhance cognitive benefits and support sustained attention during long medication duration.",
          "Ritalin":
              "Supports attention through different neurotransmitter system; may improve overall cognitive performance."
        }
      },
      {
        "id": "panax-ginseng",
        "name": "Panax Ginseng (Korean Ginseng)",
        "category": "Adaptogen",
        "dosage": "200-400mg",
        "timeOfDay": "morning",
        "benefits": [
          "Sustained Attention",
          "Mental Fatigue Reduction",
          "Dopaminergic Support"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Use standardized extract (4-7% ginsenosides). Contains ginsenosides that modulate dopamine and acetylcholine. Adaptogen for cognitive stamina.",
        "status": "beneficial",
        "focusLevel": 3,
        "mechanismOfAction":
            "Panax ginseng contains ginsenosides that modulate neurotransmission and the HPA axis. It has been shown to increase dopamine and acetylcholine levels in the hippocampus and prefrontal cortex. Ginsenosides (especially Rg1 and Rb1) act as partial agonists for dopamine receptors and promote neuronal supervivencia and dendritic growth.",
        "detailedBenefits": [
          "Improves sustained attention during long cognitive tasks",
          "Reduces mental fatigue and subjective 'brain fog'",
          "Modulates dopamine and acetylcholine for better executive function",
          "Supports HPA axis resilience against chronic stress"
        ],
        "timingRationale":
            "Morning dosing is recommended to support daytime focus and energy. Effects are cumulative but acute improvements in attention are often noticed within 30-90 minutes. Avoid evening use as it can be mildly stimulating and may interfere with sleep.",
        "scientificEvidenceRank": 74,
        "studyLinks": {
          "Ginseng and cognitive performance in ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/22082268/",
          "Neurotransmitter modulation mechanisms":
              "https://pubmed.ncbi.nlm.nih.gov/23439798/",
          "Systematic review of cognitive effects":
              "https://pubmed.ncbi.nlm.nih.gov/20123133/"
        },
        "dosageByWeight": {
          "40-60": "200mg",
          "60-80": "300mg",
          "80-100": "400mg",
          "100-120": "400-500mg"
        },
        "dosageFrequency": "Once daily in the morning",
        "dosageWarnings": [
          "May be mildly stimulating - avoid evening dosing",
          "Can lower blood sugar - monitor if on diabetic medications",
          "May interact with blood thinners (warfarin/aspirin)",
          "Generally well-tolerated; occasional insomnia at high doses"
        ],
        "tldr":
            "Adaptogen that improves sustained attention and reduces mental fatigue through dopaminergic and cholinergic support.",
        "adhdMedInteractions": {
          "Adderall":
              "May complement stimulant action for sustained focus; supports neurotransmitter reserves for later in the day.",
          "Vyvanse":
              "Supports daytime cognitive stamina and may help reduce late-afternoon mental fatigue.",
          "Ritalin":
              "Complementary cholinergic and dopaminergic support helps optimize attention and executive function."
        }
      },
      {
        "id": "maritime-pine-bark",
        "name": "Maritime Pine Bark Extract",
        "category": "Antioxidant",
        "dosage": "1mg/kg",
        "timeOfDay": "morning",
        "benefits": ["Hyperactivity Reduction", "Attention", "Blood Flow"],
        "evidenceLevel": "moderate",
        "notes":
            "Similar to Pycnogenol. Standardized maritime pine bark extract containing proanthocyanidins. Requires 8-12 weeks for full cognitive benefits.",
        "status": "beneficial",
        "focusLevel": 4,
        "mechanismOfAction":
            "Potent antioxidant containing proanthocyanidins that cross the blood-brain barrier. Enhances nitric oxide production for improved cerebral blood flow. Modulates dopamine and norepinephrine metabolism while reducing oxidative stress.",
        "detailedBenefits": [
          "Reduces hyperactivity and improves attention by 20-30% in clinical trials",
          "Enhances antioxidant capacity and reduces neuroinflammation",
          "Improves concentration and visual-motor coordination",
          "Supports cerebral blood flow and oxygen delivery"
        ],
        "timingRationale":
            "Morning dosing supports daytime cognitive function. Effects are cumulative over 8-12 weeks. Take with food to enhance absorption and reduce GI upset.",
        "scientificEvidenceRank": 73,
        "studyLinks": {
          "Pine bark extract for ADHD in children":
              "https://pubmed.ncbi.nlm.nih.gov/16499493/",
          "Attention and hyperactivity improvement":
              "https://pubmed.ncbi.nlm.nih.gov/17063641/",
          "Antioxidant effects on cognition":
              "https://pubmed.ncbi.nlm.nih.gov/22214254/"
        },
        "dosageByWeight": {
          "40-60": "40-60mg",
          "60-80": "60-80mg",
          "80-100": "80-100mg",
          "100-120": "100-120mg"
        },
        "dosageFrequency":
            "Once or twice daily with food (morning, or split AM/PM)",
        "dosageWarnings": [
          "Calculate dose as 1mg per kg of body weight",
          "Takes 8-12 weeks for full therapeutic effects",
          "May enhance effects of blood thinners (monitor if on anticoagulants)",
          "Generally well-tolerated at recommended doses"
        ],
        "tldr":
            "Antioxidant-rich extract that reduces hyperactivity and improves attention through enhanced blood flow.",
        "adhdMedInteractions": {
          "Adderall":
              "Generally safe; antioxidant effect may protect neurons from oxidative stress while supporting blood flow.",
          "Vyvanse":
              "Complements stimulant action by supporting cerebral circulation and providing neuroprotection.",
          "Ritalin":
              "Safe combination; may enhance focus benefits through improved blood flow."
        }
      },
      {
        "id": "phosphatidylcholine",
        "name": "Phosphatidylcholine (PC)",
        "category": "Lipid",
        "dosage": "1200mg",
        "timeOfDay": "any",
        "benefits": [
          "Cell Membrane Support",
          "Acetylcholine Production",
          "Neuronal Structure"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "A major phospholipid and source of choline. Essential for building and maintaining neuronal membranes.",
        "status": "beneficial",
        "focusLevel": 3,
        "mechanismOfAction":
            "Phosphatidylcholine is a vital phospholipid component of all cell membranes, particularly enriched in the brain. It provides choline for the synthesis of acetylcholine, the primary neurotransmitter for learning and memory. It also supports membrane fluidity and neurotransmitter receptor function.",
        "detailedBenefits": [
          "Provides precursor for acetylcholine (vital for memory/focus)",
          "Supports structural integrity of neuronal membranes",
          "Enhances cerebral metabolic activity",
          "Supports liver health and lipid transport"
        ],
        "timingRationale":
            "Can be taken any time of day. Take with a meal containing some fat for optimal absorption, as it is a lipid-soluble nutrient.",
        "scientificEvidenceRank": 65,
        "studyLinks": {
          "Choline and cognitive function":
              "https://pubmed.ncbi.nlm.nih.gov/22071706/",
          "Phospholipids in brain health":
              "https://pubmed.ncbi.nlm.nih.gov/30606018/"
        },
        "dosageByWeight": {
          "40-60": "600-1200mg",
          "60-80": "1200-2400mg",
          "80-100": "2400-3600mg",
          "100-120": "3600-4800mg"
        },
        "dosageFrequency": "One to two times daily with food",
        "dosageWarnings": [
          "High doses (>5g) may cause fishy body odor, sweating, or nausea",
          "Consult physician if taking cholinergic medications",
          "Soy-derived (choose sunflower PC if you have soy allergies)"
        ],
        "tldr":
            "Cell membrane phospholipid supporting neuronal structure and acetylcholine production.",
        "adhdMedInteractions": {
          "Adderall":
              "Supports the cholinergic system alongside stimulant-driven dopamine release; may have mild synergistic effects on focus.",
          "Vyvanse":
              "Generally safe and supportive of cognitive baseline; no direct interactions with medication metabolism.",
          "Ritalin":
              "Compatible combination; PC supports the structural foundation for neurotransmitter signaling."
        }
      },
      {
        "id": "vitamin-e",
        "name": "Vitamin E (Mixed Tocopherols)",
        "category": "Vitamin",
        "dosage": "200 IU",
        "timeOfDay": "any",
        "benefits": ["Antioxidant", "Membrane Protection", "Omega-3 Support"],
        "evidenceLevel": "moderate",
        "notes":
            "Mixed tocopherols preferred. Protects omega-3 fats from oxidation and supports brain membrane health.",
        "status": "beneficial",
        "focusLevel": 2,
        "mechanismOfAction":
            "Vitamin E is the primary fat-soluble antioxidant in brain cell membranes, shielding them from lipid peroxidation. It works synergistically with Omega-3 fatty acids, preventing them from oxidizing and losing their neuroprotective properties. It also supports cognitive function by reducing neuroinflammation.",
        "detailedBenefits": [
          "Protects neuronal membrane lipids from oxidative damage",
          "Synergistically stabilizes Omega-3 fatty acids in the brain",
          "Supports long-term cognitive maintenance and neuroprotection",
          "Reduces oxidative stress markers in the central nervous system"
        ],
        "timingRationale":
            "Water-soluble vitamins are easily excreted, but Vitamin E is fat-soluble and should be taken with a meal containing some fat for optimal absorption. Morning or evening use is generally fine.",
        "scientificEvidenceRank": 60,
        "studyLinks": {
          "Vitamin E and cognitive performance":
              "https://pubmed.ncbi.nlm.nih.gov/24337199/",
          "Antioxidant protection in brain":
              "https://pubmed.ncbi.nlm.nih.gov/11264871/"
        },
        "dosageByWeight": {
          "40-60": "100-200 IU",
          "60-80": "200-400 IU",
          "80-100": "400 IU",
          "100-120": "400-800 IU"
        },
        "dosageFrequency": "Once daily with a fatty meal",
        "dosageWarnings": [
          "High doses (>800 IU) may increase bleeding risk especially if on blood thinners",
          "Use mixed tocopherols (alpha, beta, gamma, delta) for full spectrum benefits",
          "Generally very safe at recommended doses"
        ],
        "tldr":
            "Fat-soluble antioxidant that protects brain membranes; works synergistically with omega-3s.",
        "adhdMedInteractions": {
          "Adderall":
              "Safe and supportive; helps mitigate oxidative stress without affecting medication metabolism.",
          "Vyvanse":
              "Compatible; provides foundational neuroprotection for the aging brain.",
          "Ritalin":
              "Generally safe; no direct interactions with methylphenidate."
        }
      },
      {
        "id": "coq10",
        "name": "Coenzyme Q10 (Ubiquinol)",
        "category": "Antioxidant",
        "dosage": "100-200mg",
        "timeOfDay": "morning",
        "benefits": [
          "Mitochondrial Energy",
          "Brain Cell Energy",
          "Antioxidant Protection"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Ubiquinol form preferred for better absorption. Supports ATP production in mitochondria.",
        "status": "beneficial",
        "focusLevel": 3,
        "mechanismOfAction":
            "CoQ10 is a critical component of the electron transport chain in mitochondria, facilitating ATP (cellular energy) production. The ubiquinol form is the reduced, active antioxidant form that protects cell membranes from oxidative damage. Brain cells have high energy demands and are particularly vulnerable to mitochondrial dysfunction.",
        "detailedBenefits": [
          "Enhances mitochondrial ATP production in neurons",
          "Protects dopaminergic neurons from oxidative stress",
          "May improve mental fatigue and processing speed",
          "Supports cardiovascular health (important for brain blood flow)"
        ],
        "timingRationale":
            "Morning dosing with a fatty meal maximizes absorption (CoQ10 is fat-soluble). Supports daytime energy production when cognitive demands are highest. Avoid evening dosing as it may be energizing.",
        "scientificEvidenceRank": 68,
        "studyLinks": {
          "CoQ10 and cognitive function":
              "https://pubmed.ncbi.nlm.nih.gov/31806905/",
          "Mitochondrial dysfunction in ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/28093713/",
          "Ubiquinol vs ubiquinone bioavailability":
              "https://pubmed.ncbi.nlm.nih.gov/17287847/"
        },
        "dosageByWeight": {
          "40-60": "50-100mg",
          "60-80": "100-150mg",
          "80-100": "150-200mg",
          "100-120": "200-300mg"
        },
        "dosageFrequency": "Once daily with a fatty meal (breakfast or lunch)",
        "dosageWarnings": [
          "May interact with blood thinners (warfarin) - consult physician",
          "Can lower blood pressure - monitor if on BP medications",
          "Ubiquinol form is more expensive but better absorbed",
          "Generally very safe; side effects rare at recommended doses"
        ],
        "tldr":
            "Supports mitochondrial energy production and provides antioxidant protection for high-energy brain cells.",
        "adhdMedInteractions": {
          "Adderall":
              "May help mitigate oxidative stress from chronic stimulant use; supports cellular energy for sustained focus.",
          "Vyvanse":
              "Supports mitochondrial function which may reduce stimulant-related fatigue during medication offset.",
          "Ritalin":
              "Provides antioxidant protection for dopaminergic neurons; may support long-term brain health with stimulant use."
        }
      },
      {
        "id": "vitamin-a",
        "name": "Vitamin A (Retinol)",
        "category": "Vitamin",
        "dosage": "2500 IU",
        "timeOfDay": "any",
        "benefits": [
          "Neuroplasticity",
          "Dopamine Receptor Function",
          "Gene Expression"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "Essential for neurodevelopment and dopamine receptor sensitivity. Avoid megadoses.",
        "status": "beneficial",
        "focusLevel": 2,
        "mechanismOfAction":
            "Retinoic acid, a derivative of Vitamin A, is a potent signaling molecule in the brain that regulates gene expression. It is critical for the induction of dopamine receptors and supporting overall neuroplasticity. Proper levels are essential for neurodevelopment and hippocampal function.",
        "detailedBenefits": [
          "Supports induction and sensitivity of dopamine receptors",
          "Crucial for hippocampal neurogenesis and memory",
          "Regulates gene expression essential for neurodevelopment",
          "Acts as a powerful antioxidant to protect visual processing pathways"
        ],
        "timingRationale":
            "As a fat-soluble vitamin, it must be taken with a meal containing some dietary fat to reach the bloodstream. Timing is flexible, though most include it with their largest meal.",
        "scientificEvidenceRank": 62,
        "studyLinks": {
          "Retinoic acid and dopamine receptors":
              "https://pubmed.ncbi.nlm.nih.gov/11547055/",
          "Vitamin A in hippocampal plasticit":
              "https://pubmed.ncbi.nlm.nih.gov/17502394/"
        },
        "dosageByWeight": {
          "40-60": "1000-2000 IU",
          "60-80": "2000-3000 IU",
          "80-100": "3000-5000 IU",
          "100-120": "5000 IU"
        },
        "dosageFrequency": "Once daily with a fatty meal",
        "dosageWarnings": [
          "⚠️ AVOID megadoses: Toxic above 10,000 IU daily long-term (polar bear liver effect)",
          "Pregnant women should consult physician (risk of birth defects at high doses)",
          "Beta-carotene is a safer precursor for those at risk of toxicity"
        ],
        "tldr":
            "Fat-soluble vitamin supporting neuroplasticity and dopamine receptor function; avoid megadoses.",
        "adhdMedInteractions": {
          "Adderall":
              "Provides foundational support for dopamine receptors that medication targets; generally safe.",
          "Vyvanse":
              "No known direct interaction; supports overall neuronal signaling health.",
          "Ritalin":
              "Compatible; aids in maintaining receptor sensitivity over time."
        }
      },
      {
        "id": "st-johns-wort",
        "name": "St. John's Wort",
        "category": "Herb",
        "dosage": "300mg",
        "timeOfDay": "morning",
        "benefits": ["Mild Depression", "Mood Support"],
        "evidenceLevel": "moderate",
        "notes":
            "⚠️ CAUTION: Powerful CYP450 enzyme inducer. Interacts with MANY medications including birth control, antidepressants, and blood thinners. NOT recommended for ADHD.",
        "status": "caution",
        "focusLevel": 2,
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
        "dosageFrequency":
            "Once or twice daily (NOT RECOMMENDED for ADHD patients)",
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
        "benefits": ["Sleep Support", "Anxiety Reduction"],
        "evidenceLevel": "low",
        "notes":
            "⚠️ CAUTION: Sedating herb for sleep. Can cause morning grogginess. May interact with other sedatives. Not for daytime use.",
        "status": "caution",
        "focusLevel": 2,
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
        "benefits": ["Anxiety Reduction", "Relaxation"],
        "evidenceLevel": "moderate",
        "notes":
            "⚠️ CAUTION: Effective anxiolytic but LIVER TOXICITY RISK. Banned in several countries. Use only high-quality noble kava. Monitor liver enzymes. NOT for long-term use.",
        "status": "caution",
        "focusLevel": 2,
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
          "Mechanism of action": "https://pubmed.ncbi.nlm.nih.gov/15639154/"
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
        "benefits": ["Focus", "Mood"],
        "evidenceLevel": "low",
        "notes":
            "⚠️ CAUTION: Theoretical choline precursor but limited evidence. May cause overstimulation, insomnia, or headaches. Not well-researched for ADHD.",
        "status": "caution",
        "focusLevel": 2,
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
      {
        "id": "caffeine",
        "name": "Caffeine (with L-Theanine)",
        "category": "Stimulant",
        "dosage": "50-100mg",
        "timeOfDay": "morning",
        "benefits": ["Alertness", "Focus", "Reaction Time"],
        "evidenceLevel": "high",
        "notes":
            "⚠️ MUST combine with L-Theanine (2:1 ratio) for ADHD to minimize jitters and anxiety. Alone may worsen impulsivity.",
        "status": "caution",
        "focusLevel": 5,
        "mechanismOfAction":
            "Caffeine is an adenosine receptor antagonist that prevents adenosine from binding to its receptors, thereby increasing alertness and wakefulness. It also indirectly increases dopamine and norepinephrine levels. When combined with L-Theanine, the 'jittery' side effects are mitigated through GABAergic modulation, creating a synergy that improves sustained attention without overstimulation.",
        "detailedBenefits": [
          "Reduces sleepiness and improves subjective alertness",
          "Enhances reaction time and processing speed",
          "Improves sustained attention when combined with L-Theanine",
          "Temporarily increases dopamine availability in the striatum"
        ],
        "timingRationale":
            "Morning use is best for alertness. Avoid use after 2:00 PM to prevent interference with sleep architecture (Caffeine has a ~5-6 hour half-life). Effects peak within 30-60 minutes. Use carefully with prescription stimulants to avoid tachycardia or excessive anxiety.",
        "scientificEvidenceRank": 82,
        "studyLinks": {
          "Caffeine and L-Theanine synergy":
              "https://pubmed.ncbi.nlm.nih.gov/18681988/",
          "Caffeine effects on ADHD symptoms":
              "https://pubmed.ncbi.nlm.nih.gov/21437156/",
          "Adenosine and dopamine interactions":
              "https://pubmed.ncbi.nlm.nih.gov/11283318/"
        },
        "dosageByWeight": {
          "40-60": "50mg + 100mg L-Theanine",
          "60-80": "50-100mg + 100-200mg L-Theanine",
          "80-100": "100mg + 200mg L-Theanine",
          "100-120": "100-150mg + 200-300mg L-Theanine"
        },
        "dosageFrequency": "Once or twice daily (before 2 PM)",
        "dosageWarnings": [
          "⚠️ May increase heart rate and blood pressure",
          "⚠️ Can worsen anxiety, jitters, and sleep latency",
          "⚠️ Tolerance builds quickly; regular breaks are recommended",
          "⚠️ Avoid if sensitive to stimulants or have heart conditions"
        ],
        "tldr":
            "Must be paired with L-Theanine to mitigate jitters; provides temporary alertness and focus but use with caution with ADHD medications.",
        "adhdMedInteractions": {
          "Adderall":
              "⚠️ ADDITIVE EFFECT: Significant risk of overstimulation, tachycardia, and anxiety. Consult your provider before combining.",
          "Vyvanse":
              "⚠️ ADDITIVE EFFECT: May increase heart rate and worsen 'crash' during medication offset.",
          "Ritalin":
              "⚠️ CAUTION: Both increase dopamine and norepinephrine; potential for excessive jitters or blood pressure spikes."
        }
      },
      {
        "id": "melatonin",
        "name": "Melatonin",
        "category": "Hormone",
        "dosage": "0.3-3mg",
        "timeOfDay": "evening",
        "benefits": ["Sleep Latency", "Sleep Quality", "Circadian Rhythm"],
        "evidenceLevel": "high",
        "notes":
            "⚠️ Use only for sleep. Use lowest effective dose (0.3-1mg often better than high doses). Does not treat attention symptoms.",
        "status": "caution",
        "focusLevel": 2,
        "mechanismOfAction":
            "Melatonin is a hormone naturally produced by the pineal gland in response to darkness. It signals to the HPA axis and suprachiasmatic nucleus that it is time for sleep. ADHD is frequently associated with a delayed melatonin onset; exogenous supplementation helps reset the circadian rhythm and reduces sleep latency (time to fall asleep).",
        "detailedBenefits": [
          "Reduces sleep latency by 15-30 minutes on average",
          "Helps synchronize the circadian rhythm in cases of delayed sleep phase",
          "Improves overall sleep quality and duration",
          "May reduce evening restlessness and 'tired but wired' feelings"
        ],
        "timingRationale":
            "Take 30-60 minutes before desired bedtime. Dim lights after taking to support natural production. Avoid 'screen time' (blue light) which suppresses melatonin. For circadian rhythm resetting, take at a consistent time every evening. Not for daytime use.",
        "scientificEvidenceRank": 89,
        "studyLinks": {
          "Melatonin for sleep in ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/30635432/",
          "Circadian rhythm and ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/30107544/",
          "Low dose vs high dose melatonin":
              "https://pubmed.ncbi.nlm.nih.gov/11600521/"
        },
        "dosageByWeight": {
          "40-60": "0.3-0.5mg",
          "60-80": "0.5-1mg",
          "80-100": "1-2mg",
          "100-120": "3mg"
        },
        "dosageFrequency": "Once daily, 30-60 min before bed",
        "dosageWarnings": [
          "⚠️ May cause morning grogginess if dose is too high",
          "⚠️ Can cause vivid dreams or nightmares in some individuals",
          "⚠️ May interact with blood pressure and diabetes medications",
          "⚠️ Long-term daily use in children should be medically supervised",
          "Not recommended for pregnant or breastfeeding women"
        ],
        "tldr":
            "Hormone that helps reset circadian rhythm and reduce sleep latency; highly effective for ADHD-related sleep issues at low doses.",
        "adhdMedInteractions": {
          "Adderall":
              "Helps mitigate stimulant-induced insomnia. Generally safe but monitor for next-day sedation.",
          "Vyvanse":
              "Useful for overcoming late-evening stimulant residual effects; supports normal sleep patterns.",
          "Ritalin":
              "Effective for reducing sleep latency if methylphenidate interferes with falling asleep."
        }
      },
      {
        "id": "5-htp",
        "name": "5-HTP (5-Hydroxytryptophan)",
        "category": "Amino Acid",
        "dosage": "50-100mg",
        "timeOfDay": "evening",
        "benefits": ["Mood Stability", "Sleep Quality", "Serotonin Support"],
        "evidenceLevel": "moderate",
        "notes":
            "⚠️ CRITICAL: Serotonin precursor. AVOID with SSRIs, SNRIs, or other serotonergic medications (risk of Serotonin Syndrome).",
        "status": "beneficial",
        "focusLevel": 2,
        "mechanismOfAction":
            "5-HTP is the immediate precursor to serotonin (5-HT). Unlike tryptophan, it crosses the blood-brain barrier very efficiently and does not require a transport molecule. It is directly decarboxylated into serotonin, which regulates mood, sleep, and impulse control. Serotonin is also a precursor to melatonin, supporting natural sleep architecture.",
        "detailedBenefits": [
          "Improves evening mood and reduces emotional dysregulation",
          "Enhances sleep quality by increasing natural melatonin production",
          "May reduce impulsive behaviors and carbohydrate cravings",
          "Supports emotional resilience in ADHD patients with comorbid anxiety"
        ],
        "timingRationale":
            "Evening dosing is optimal because serotonin supports melatonin production and can have a calming effect. Effects are often noticed within 1-2 hours for sleep. Dose should be 50-100mg; higher doses increase risk of nausea and side effects without much added benefit for most. Take with a small carb snack for best absorption.",
        "scientificEvidenceRank": 72,
        "studyLinks": {
          "5-HTP for depression and mood":
              "https://pubmed.ncbi.nlm.nih.gov/15146197/",
          "Serotonin and impulse control":
              "https://pubmed.ncbi.nlm.nih.gov/20561551/",
          "Safety and interaction with SSRIs":
              "https://pubmed.ncbi.nlm.nih.gov/22129819/"
        },
        "dosageByWeight": {
          "40-60": "50mg",
          "60-80": "50-100mg",
          "80-100": "100mg",
          "100-120": "100-200mg"
        },
        "dosageFrequency": "Once daily in the evening",
        "dosageWarnings": [
          "⚠️ AVOID if taking SSRIs, SNRIs, MAOIs, or other antidepressants",
          "⚠️ Risk of Serotonin Syndrome (high fever, agitation, confusion)",
          "⚠️ May cause nausea or GI upset - take with food if needed",
          "Not for long-term daily use without supervision; cycle breaks recommended"
        ],
        "tldr":
            "Serotonin precursor that supports mood and sleep; highly effective but dangerous if combined with specific antidepressants.",
        "adhdMedInteractions": {
          "Adderall":
              "⚠️ USE CAUTION: Adderall also has minor serotonergic activity. Monitor for overstimulation or mood changes.",
          "Vyvanse":
              "⚠️ USE CAUTION: Potential for additive effects on mood. Consult provider if combining.",
          "Ritalin":
              "Generally low interaction risk, but monitor for changes in mood or sleep architecture."
        }
      },
      {
        "id": "copper",
        "name": "Copper",
        "category": "Mineral",
        "dosage": "1-2mg",
        "timeOfDay": "morning",
        "benefits": [
          "Dopamine Synthesis",
          "Energy Production",
          "Iron Metabolism"
        ],
        "evidenceLevel": "moderate",
        "notes":
            "⚠️ CAUTION: Only supplement if you take high-dose Zinc (Zn:Cu ratio of 15:1). Typical ADHD patients often have HIGH copper and LOW zinc.",
        "status": "caution",
        "focusLevel": 2,
        "mechanismOfAction":
            "Copper is a required cofactor for dopamine beta-hydroxylase, the enzyme that converts dopamine into norepinephrine. It is also essential for mitochondrial energy production (cytochrome c oxidase) and iron metabolism. However, copper and zinc compete for absorption; chronic high zinc intake can cause copper deficiency, and elevated copper-to-zinc ratios are a biomarker frequently observed in ADHD populations.",
        "detailedBenefits": [
          "Supports the conversion of dopamine to norepinephrine",
          "Essential for mitochondrial ATP (energy) production",
          "Required for iron absorption and hemoglobin synthesis",
          "Supports connective tissue and neurotransmitter balance"
        ],
        "timingRationale":
            "Take in the morning with food to minimize potential GI upset. If taking Zinc, separate doses or use a combined formula that maintains the 15:1 Zinc-to-Copper ratio. Copper absorption is inhibited by high doses of Vitamin C; separate these by at least 2 hours.",
        "scientificEvidenceRank": 61,
        "studyLinks": {
          "Copper/Zinc ratios in ADHD populations":
              "https://pubmed.ncbi.nlm.nih.gov/21350130/",
          "Copper role in dopamine metabolism":
              "https://pubmed.ncbi.nlm.nih.gov/11252112/",
          "Mineral competition for absorption":
              "https://pubmed.ncbi.nlm.nih.gov/11110860/"
        },
        "dosageByWeight": {
          "40-60": "0.5-1mg",
          "60-80": "1mg",
          "80-100": "1-2mg",
          "100-120": "2mg"
        },
        "dosageFrequency": "Once daily, preferably with food",
        "dosageWarnings": [
          "⚠️ High doses can be toxic and cause oxidative stress",
          "⚠️ May cause nausea, vomiting, or stomach pain if taken on empty stomach",
          "⚠️ DO NOT supplement if you already have high copper levels (common in ADHD)",
          "⚠️ Long-term high-dose use can interfere with zinc and vitamin C status"
        ],
        "tldr":
            "Essential mineral for norepinephrine synthesis; only supplement if zinc intake is high, as copper/zinc balance is critical for ADHD management.",
        "adhdMedInteractions": {
          "Adderall":
              "Generally low interaction, but ensures adequate norepinephrine reserves for medication efficacy.",
          "Vyvanse":
              "Supports neurotransmitter synthesis required for medication to functional optimally.",
          "Ritalin":
              "Ensures mineral cofactors are available for dopamine/norepinephrine pathways."
        }
      },
      {
        "id": "b6-high-dose",
        "name": "Vitamin B6 (High-Dose Standalone)",
        "category": "Vitamin",
        "dosage": "25-50mg",
        "timeOfDay": "morning",
        "benefits": [
          "Neurotransmitter Synthesis",
          "Dopamine Support",
          "Energy Metabolism"
        ],
        "evidenceLevel": "high",
        "notes":
            "⚠️ CRITICAL: High standalone doses (>100mg/day) long-term can cause IRREVERSIBLE peripheral neuropathy (nerve damage). Best used in Magnesium+B6 combinations.",
        "status": "caution",
        "focusLevel": 2,
        "mechanismOfAction":
            "Pyridoxine (Vitamin B6) is a critical cofactor for over 100 enzymatic reactions, most notably the conversion of L-DOPA to dopamine and 5-HTP to serotonin. It is essential for amino acid metabolism and the creation of heme. However, excessive levels of pyridoxine can inhibit natural B6 metabolism and damage sensory neurons, leading to peripheral neuropathy characterized by numbness and tingling.",
        "detailedBenefits": [
          "Cofactor for the synthesis of dopamine, serotonin, and GABA",
          "Essential for mitochondrial energy production and iron metabolism",
          "Supports homocysteine metabolism for cardiovascular health",
          "May reduce PMS-related mood symptoms in some individuals"
        ],
        "timingRationale":
            "Take in the morning with food to support daytime neurotransmitter synthesis. Avoid evening use as high doses can cause vivid dreams or insomnia in sensitive individuals. Do not exceed 100mg total daily intake from all sources combined (Tolerable Upper Intake Level).",
        "scientificEvidenceRank": 76,
        "studyLinks": {
          "Vitamin B6 and neurotransmitter synthesis":
              "https://pubmed.ncbi.nlm.nih.gov/20126403/",
          "B6 toxicity and peripheral neuropathy":
              "https://pubmed.ncbi.nlm.nih.gov/22116704/",
          "B6 and Magnesium synergy for ADHD":
              "https://pubmed.ncbi.nlm.nih.gov/16846314/"
        },
        "dosageByWeight": {
          "40-60": "10-25mg",
          "60-80": "25mg",
          "80-100": "50mg",
          "100-120": "50-100mg"
        },
        "dosageFrequency": "Once daily with food",
        "dosageWarnings": [
          "⚠️ AVOID exceeding 100mg/day from all sources combined",
          "⚠️ DISCONTINUE immediately if you experience numbness, tingling, or nerve pain",
          "⚠️ Long-term use of standalone high doses carries greater risk than B-complex",
          "⚠️ May interfere with the metabolism of certain anti-seizure medications"
        ],
        "tldr":
            "Essential cofactor for dopamine and serotonin synthesis, but high standalone doses carry a risk of nerve damage; best used in balanced formulas.",
        "adhdMedInteractions": {
          "Adderall":
              "Supports the synthesis of dopamine required for medication to function effectively.",
          "Vyvanse":
              "Essential cofactor for the conversion pathways utilized by the medication.",
          "Ritalin":
              "Ensures adequate neurotransmitter precursors are available for dopamine/norepinephrine pathways."
        }
      },
      {
        "id": "yellow-5",
        "name": "Yellow 5 (Tartrazine / E102)",
        "category": "Artificial Color",
        "description":
            "Synthetic coal-tar dye linked to increased hyperactivity and asthma flares. Requires 'may have an adverse effect on activity and attention in children' warning in the EU.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Tartrazine can induce histamine release and depletes body stores of zinc and vitamin B6. Since B6 is a crucial cofactor for dopamine synthesis, its depletion can lead to neurochemical imbalances and behavioral disruption.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Eliminating from diet is recommended for symptom control.",
        "scientificEvidenceRank": 73,
        "studyLinks": {
          "Southampton study on additives":
              "https://pubmed.ncbi.nlm.nih.gov/17825405/",
          "Zinc depletion and tartrazine":
              "https://pubmed.ncbi.nlm.nih.gov/7930261/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Known to trigger hives and asthma in sensitive individuals",
          "Significant correlation with impulsivity in ADHD children",
          "Listed as Tartrazine or E102",
          "Common in pickles, mustard, cereals, and neon-colored snacks"
        ],
        "tldr":
            "Artificial yellow dye linked to hyperactivity and zinc/B6 depletion; avoid to maintain neurotransmitter balance.",
        "adhdMedInteractions": {
          "Adderall":
              "Can increase irritability and restlessness, counteracting medication's calming effect.",
          "Vyvanse":
              "May trigger mood swings and behavioral flares that reduce the duration of perceived focus.",
          "Ritalin":
              "Avoid: Directly increases the hyperactivity that methylphenidate aims to control."
        }
      },
      {
        "id": "yellow-6",
        "name": "Yellow 6 (Sunset Yellow / E110)",
        "category": "Artificial Color",
        "description":
            "Azo dye shown to increase hyperactive behavior and potentially contribute to adrenal gland tumors in animal studies.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Mimics the effects of a neuro-excitatory toxin in sensitive individuals, triggering hypersensitivity reactions that present as ADHD symptoms like restlessness and poor concentration.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Should be eliminated from an ADHD-friendly diet.",
        "scientificEvidenceRank": 72,
        "studyLinks": {
          "Hyperactivity in 3-year-olds and 8/9-year-olds":
              "https://pubmed.ncbi.nlm.nih.gov/17825405/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Azo dye with high correlation to school-age hyperactivity",
          "Listed as Sunset Yellow FCF or E110",
          "Common in orange sodas, baked goods, and cheese snacks"
        ],
        "tldr":
            "Orange food dye that increases hyperactivity; highly recommended to avoid in ADHD patients.",
        "adhdMedInteractions": {
          "Adderall":
              "May exacerbate 'comedown' irritability and increase physical restlessness.",
          "Vyvanse":
              "Can interfere with sustained attention performance by introducing internal distractibility.",
          "Ritalin":
              "Counter-productive: adds to the motor hyperactivity that medication is intended to suppress."
        }
      },
      {
        "id": "red-3",
        "name": "Red 3 (Erythrosine / E127)",
        "category": "Artificial Color",
        "description":
            "Synthetic cherry-pink dye associated with thyroid disruption and significant behavioral changes in ADHD patients. Banned in many countries for food use.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Erythrosine can interfere with iodine metabolism and thyroid function. Thyroid imbalances are closely linked to cognitive dysfunction, anxiety, and restlessness, which can severely exacerbate existing ADHD symptoms.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Consumption is linked to hormonal and behavioral disruption.",
        "scientificEvidenceRank": 70,
        "studyLinks": {
          "Artificial dyes and thyroid function":
              "https://pubmed.ncbi.nlm.nih.gov/24584102/",
          "Behavioral effects of Red 3":
              "https://pubmed.ncbi.nlm.nih.gov/7161718/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Banned by FDA for use in cosmetics/drugs due to cancer risk in rats",
          "Significant impact on behavioral stability in sensitive individuals",
          "Listed as Erythrosine or E127",
          "Often found in maraschino cherries and some baked goods"
        ],
        "tldr":
            "Red dye with thyroid-disrupting potential that worsens ADHD restlessness; eliminate from diet.",
        "adhdMedInteractions": {
          "Adderall":
              "Can increase physical tension and anxiety, masking the therapeutic effects of medication.",
          "Vyvanse":
              "Avoid: Behavioral side effects may mimic medication 'overdose'.",
          "Ritalin":
              "Directly opposes the calming effect of methylphenidate on motor hyperactivity."
        }
      },
      {
        "id": "blue-1",
        "name": "Blue 1 (Brilliant Blue / E133)",
        "category": "Artificial Color",
        "description":
            "Petroleum-derived blue dye that can cross the blood-brain barrier. Linked to hyperactivity and allergic reactions.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Unlike many other dyes, Blue 1 can cross the blood-brain barrier and has been shown to inhibit neuro-signaling in certain contexts. It triggers inflammatory responses that can manifest as increased impulsivity and mood instability.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Should be removed from ADHD nutritional plans.",
        "scientificEvidenceRank": 68,
        "studyLinks": {
          "Blue 1 and blood-brain barrier":
              "https://pubmed.ncbi.nlm.nih.gov/15531024/",
          "FDA report on food dyes and behavior":
              "https://www.fda.gov/media/100000/download"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Can cross the blood-brain barrier directly",
          "Associated with allergic reactions and behavioral flares",
          "Listed as Brilliant Blue FCF or E133",
          "Found in blue-colored beverages, candy, and ice cream"
        ],
        "tldr":
            "Blue dye that crosses the blood-brain barrier and serves as a behavioral trigger for many ADHD patients.",
        "adhdMedInteractions": {
          "Adderall":
              "May trigger sudden drops in focus and increases in irritability.",
          "Vyvanse": "Avoid: Linked to 'brain fog' and behavioral instability.",
          "Ritalin":
              "Exacerbates impulsivity and reduces the quality of task salience."
        }
      },
      {
        "id": "blue-2",
        "name": "Blue 2 (Indigo Carmine / E132)",
        "category": "Artificial Color",
        "description":
            "Synthetic color associated with hyperactivity and potential neurotoxicity in animal studies.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Blue 2 triggers neuro-inflammatory pathways in sensitive individuals, leading to a state of 'hyper-arousal' that directly mirrors ADHD hyperactivity symptoms.",
        "detailedBenefits": <String>[],
        "timingRationale": "AVOID: Exclusion from diet is highly recommended.",
        "scientificEvidenceRank": 67,
        "studyLinks": {
          "Indigo Carmine and behavioral toxicity":
              "https://pubmed.ncbi.nlm.nih.gov/6582312/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Linked to brain tumors in some older animal studies with high intake",
          "Consistent trigger for ADHD hyperactivity in clinical reports",
          "Listed as Indigo Carmine or E132",
          "Common in candy, beverages, and pet foods"
        ],
        "tldr":
            "Synthetic blue dye associated with behavioral hyper-arousal and restlessness.",
        "adhdMedInteractions": {
          "Adderall": "Can trigger anxiety and heart-rate spikes.",
          "Vyvanse":
              "Avoid: Increases distractibility and decreases cognitive endurance.",
          "Ritalin": "Counteracts the impulse control benefits of medication."
        }
      },
      {
        "id": "carmoisine",
        "name": "Carmoisine (Azorubine / E122)",
        "category": "Artificial Color",
        "description":
            "One of the primary 'Southampton Six' azo dyes with established links to hyperactivity in school-age children.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Similar to other azo dyes, it triggers histamine release which acts as a central nervous system irritant in ADHD patients, causing decreased focus and increased physical motion.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Removing from diet reduces cumulative behavioral load.",
        "scientificEvidenceRank": 71,
        "studyLinks": {
          "Southampton Study (Lancet)":
              "https://pubmed.ncbi.nlm.nih.gov/17825405/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "One of the 'Southampton Six' requiring mandatory EU warnings",
          "Strongly associated with inattention and hyperactivity",
          "Listed as Azorubine or E122",
          "Common in jams, red desserts, and jellies"
        ],
        "tldr":
            "Azo red dye from the Southampton study with proven hyperactivity links.",
        "adhdMedInteractions": {
          "Adderall": "Avoid: Can cause irritability and emotional volatility.",
          "Vyvanse":
              "Triggers focus 'dips' that look like medication wearing off early.",
          "Ritalin":
              "Directly opposes the hyperactivity suppression of medication."
        }
      },
      {
        "id": "quinoline-yellow",
        "name": "Quinoline Yellow (E104)",
        "category": "Artificial Color",
        "description":
            "Synthetic yellow dye that significantly increased Global Hyperactivity scores in large-scale clinical trials.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Causes central nervous system excitation and can induce allergic-like responses that disrupt prefrontal cortex function (the area responsible for executive control).",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Elimination from diet reduces behavioral interference.",
        "scientificEvidenceRank": 69,
        "studyLinks": {
          "EFSA reassessment of Quinoline Yellow":
              "https://www.efsa.europa.eu/en/efsajournal/pub/1329"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "One of the 'Southampton Six' behavioral triggers",
          "Frequently combined with sodium benzoate (amplifies effect)",
          "Listed as Quinoline Yellow or E104",
          "Common in smoked fish and some citrus-flavored drinks"
        ],
        "tldr":
            "Yellow dye that disrupts executive function and increases hyperactivity scores.",
        "adhdMedInteractions": {
          "Adderall":
              "Can trigger restlessness and 'body jitters' that mimic over-medication.",
          "Vyvanse": "Avoid: Reduces the quality of sustained focus.",
          "Ritalin":
              "Opposes medication goals for calming hyperactive behaviors."
        }
      },
      {
        "id": "allura-red",
        "name": "Allura Red AC (E129)",
        "category": "Artificial Color",
        "description":
            "The most common red food dye (Red 40 in USA), proven to increase hyperactivity in school-age children across international studies.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Triggers the release of pro-inflammatory cytokines and histamine in the brain, leading to a state of cognitive arousal that manifests as impulsivity and poor concentration.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Highly recommended for elimination in ADHD patients.",
        "scientificEvidenceRank": 74,
        "studyLinks": {
          "Meta-analysis of food dyes and behavior":
              "https://pubmed.ncbi.nlm.nih.gov/22331014/",
          "Southampton Study Results":
              "https://pubmed.ncbi.nlm.nih.gov/17825405/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "The single most prevalent behavioral trigger dye in the Western diet",
          "Often hidden in white or non-red foods as a 'color enhancer'",
          "Listed as Allura Red AC, Red 40, or E129",
          "Ubiquitous in soft drinks, candy, and colorful cereals"
        ],
        "tldr":
            "The most common behavioral trigger dye; avoid to reduce impulsivity and ADHD flares.",
        "adhdMedInteractions": {
          "Adderall":
              "Avoid: Can cause extreme emotional sensitivity and volatility.",
          "Vyvanse":
              "Can trigger sudden focus drops and increased distractibility.",
          "Ritalin":
              "Opposes the impulse control and motor calming effects of medication."
        }
      },
      {
        "id": "aspartame",
        "name": "Aspartame (E951)",
        "category": "Artificial Sweetener",
        "description":
            "Synthetic sweetener that may interfere with amino acid balance and neurotransmitter synthesis in sensitive individuals.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Aspartame contains phenylalanine, which can compete with other large neutral amino acids (like tyrosine) for transport across the blood-brain barrier. High levels may interfere with the synthesis of dopamine and serotonin, potentially worsening mood and focus in ADHD individuals.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: May cause neurochemical instability and brain fog.",
        "scientificEvidenceRank": 58,
        "studyLinks": {
          "Aspartame and neurobehavioral effects":
              "https://pubmed.ncbi.nlm.nih.gov/28198205/",
          "Phenylalanine and large neutral amino acids":
              "https://pubmed.ncbi.nlm.nih.gov/17684524/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "May trigger migraines or brain fog in sensitive individuals",
          "Interferes with the amino acid balance used for dopamine synthesis",
          "Listed as Aspartame or E951",
          "Found in diet sodas, sugar-free gum, and low-calorie snacks"
        ],
        "tldr":
            "Artificial sweetener that can disrupt neurotransmitter precursors; avoid to maintain cognitive clarity.",
        "adhdMedInteractions": {
          "Adderall":
              "May subtly reduce medication effectiveness by competing with dopamine precursors.",
          "Vyvanse":
              "Avoid: Individual reports of 'brain fog' and mood swings when combined.",
          "Ritalin":
              "Can exacerbate irritability and reduce the quality of task salience."
        }
      },
      {
        "id": "sucralose",
        "name": "Sucralose",
        "category": "Artificial Sweetener",
        "description":
            "Artificial sweetener that may disrupt the gut microbiome and potentially trigger neuro-inflammatory responses.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Sucralose has been shown to significantly alter the gut microbiome and may increase intestinal permeability. Since the gut-brain axis is critical for ADHD management, chronic gut disruption can lead to systemic inflammation and indirect behavioral worsening.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Long-term gut health is foundational for ADHD focus.",
        "scientificEvidenceRank": 55,
        "studyLinks": {
          "Sucralose and the gut microbiome":
              "https://pubmed.ncbi.nlm.nih.gov/30138244/",
          "Artificial sweeteners and systemic inflammation":
              "https://pubmed.ncbi.nlm.nih.gov/31201202/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "May cause digestive upset or bloating in some individuals",
          "Disrupts beneficial bacteria needed for neurotransmitter health",
          "Frequently found in 'Sugar-Free' processed products",
          "Can trigger anecdotal reports of worsening brain fog"
        ],
        "tldr":
            "Artificial sweetener that may disrupt the gut-brain axis; avoid for optimal digestive and cognitive health.",
        "adhdMedInteractions": {
          "Adderall":
              "Safe combination, but gut health disruption can reduce long-term resilience.",
          "Vyvanse":
              "Possible GI irritation; supports avoidance for better nutrient absorption.",
          "Ritalin":
              "No known direct interaction; avoid for systemic baseline health."
        }
      },
      {
        "id": "msg",
        "name": "Monosodium Glutamate (MSG / E621)",
        "category": "Flavor Enhancer",
        "description":
            "Flavor enhancer that acts as an excitotoxin in sensitive individuals, potentially overstimulating neuronal pathways.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "MSG provides highly concentrated glutamate, the brain's primary excitatory neurotransmitter. In sensitive ADHD individuals, this can lead to neuronal 'hyperexcitability,' manifesting as increased restlessness, anxiety, and difficulty controlling motor impulses.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: May cause acute behavioral flares in sensitive people.",
        "scientificEvidenceRank": 52,
        "studyLinks": {
          "MSG and behavioral hyperactivity":
              "https://pubmed.ncbi.nlm.nih.gov/15531024/",
          "Excitotoxicity in sensitive populations":
              "https://pubmed.ncbi.nlm.nih.gov/22331014/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Excitotoxin that can trigger 'brain jitters' and headaches",
          "Significantly exacerbates restlessness in susceptible individuals",
          "Listed as MSG, Monosodium Glutamate, or E621",
          "Found in fast food, many chips, and savory processed snacks"
        ],
        "tldr":
            "Flavor enhancer that can overstimulate the brain and worsen motor restlessness; eliminate from diet.",
        "adhdMedInteractions": {
          "Adderall":
              "May increase overstimulation and jitteriness when combined.",
          "Vyvanse":
              "Avoid: Can cause erratic focus spikes followed by crashes.",
          "Ritalin": "Opposes the calming effects on motor impulsivity."
        }
      },
      {
        "id": "bht",
        "name": "Butylated Hydroxytoluene (BHT / E321)",
        "category": "Preservative",
        "description":
            "Synthetic preservative linked to oxidative stress and potential behavioral disruption in animal studies.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "BHT can induce oxidative stress markers in the brain and has been linked to behavioral toxicity at high levels. It may interfere with the neuroprotective effects of antioxidants and lipids like omega-3.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Preservative with recognized neuro-inflammatory potential.",
        "scientificEvidenceRank": 60,
        "studyLinks": {
          "BHT and neuro-inflammatory markers":
              "https://pubmed.ncbi.nlm.nih.gov/15531024/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Synthetic preservative with high oxidative potential",
          "Linked to behavioral toxicity in sensitive animal models",
          "Check labels for BHT or E321 in dry goods",
          "Common in cereals, snack packaging, and chewing gum"
        ],
        "tldr":
            "Preservative with potential neurotoxic effects; avoid for overall cognitive maintenance.",
        "adhdMedInteractions": {
          "Adderall":
              "No direct metabolism interaction, but adds to systemic oxidative load.",
          "Vyvanse":
              "Generally compatible, but avoid for long-term brain health.",
          "Ritalin": "Compatible combination, but supports non-toxic diet."
        }
      },
      {
        "id": "potassium-benzoate",
        "name": "Potassium Benzoate (E212)",
        "category": "Preservative",
        "description":
            "Preservative similar to sodium benzoate that amplifies hyperactivity, especially when paired with dyes.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Like sodium benzoate, it can increase motor hyperactivity and may contribute to systemic inflammation and mitochondrial stress, particularly when consumed with synthetic dyes.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Consumption is linked to behavioral disruption.",
        "scientificEvidenceRank": 66,
        "studyLinks": {
          "Sodium benzoate and behavior (Southampton)":
              "https://pubmed.ncbi.nlm.nih.gov/17825405/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Shares hyperactive-inducing potential with sodium benzoate",
          "Most problematic when paired with synthetic food dyes",
          "Listed as Potassium Benzoate or E212",
          "Common in soft drinks, fruit juices, and dressings"
        ],
        "tldr":
            "Preservative that amplifies hyperactivity effects; eliminate from diet to reduce restlessness.",
        "adhdMedInteractions": {
          "Adderall":
              "Can increase restlessness and reduce medication focus duration.",
          "Vyvanse":
              "Triggers behavioral spikes that mask medication stability.",
          "Ritalin":
              "Directly opposes the calming therapeutic goal of medication."
        }
      },
      {
        "id": "refined-sugar",
        "name": "Refined Sugar (High Intake)",
        "category": "Dietary Factor",
        "description":
            "Chronic excessive intake of refined sugars that destabilizes blood glucose and downregulates dopamine signaling.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Frequent intake of refined sugar causes rapid glucose spikes followed by insulin-driven crashes. This glycemic instability leads to dopamine receptor downregulation over time and causes acute brain fog, irritability, and attention deficits during sugar 'crashes.'",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Glycemic stability is critical for ADHD management.",
        "scientificEvidenceRank": 63,
        "studyLinks": {
          "Refined sugar and ADHD behaviors":
              "https://pubmed.ncbi.nlm.nih.gov/21129940/",
          "Dopamine receptor downregulation":
              "https://pubmed.ncbi.nlm.nih.gov/16507461/"
        },
        "dosageByWeight": {
          "40-60": "0g (AVOID)",
          "60-80": "0g (AVOID)",
          "80-100": "0g (AVOID)",
          "100-120": "0g (AVOID)"
        },
        "dosageFrequency": "Eliminate processed sugars; use low-glycemic foods",
        "dosageWarnings": [
          "Causes rapid spikes and subsequent brain fog crashes",
          "Long-term excess can reduce the density of dopamine receptors",
          "Check for 'hidden' sugars in savory processed foods",
          "Directly worsens hyperactivity and mood volatility"
        ],
        "tldr":
            "Sugar destabilizes dopamine signaling and causes focus-killing crashes; eliminate to maintain steady attention.",
        "adhdMedInteractions": {
          "Adderall":
              "Worsens the 'comedown' and decreases the efficiency of dopamine signaling.",
          "Vyvanse":
              "Causes energy fluctuations that make medication feel inconsistent.",
          "Ritalin":
              "Opposes medication goals for calming and focus maintenance."
        }
      },
      {
        "id": "trans-fats",
        "name": "Trans Fats (Partially Hydrogenated Oils)",
        "category": "Dietary Fat",
        "description":
            "Harmful synthetic fats that incorporate into brain membranes and interfere with essential fatty acid function.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Trans fats can physically incorporate into neuronal cell membranes, reducing their fluidity. This interference blunts the function of critical proteins like the dopamine transporter and neurotransmitter receptors, directly impairing cognitive processing and signal transduction.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Interferes with the foundation of neuronal signaling.",
        "scientificEvidenceRank": 76,
        "studyLinks": {
          "Trans fats and neuronal membrane fluidity":
              "https://pubmed.ncbi.nlm.nih.gov/21129940/"
        },
        "dosageByWeight": {
          "40-60": "0g (AVOID)",
          "60-80": "0g (AVOID)",
          "80-100": "0g (AVOID)",
          "100-120": "0g (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Directly interferes with the neuroprotective benefits of Omega-3",
          "Pro-inflammatory and disrupts neuronal membrane integrity",
          "Listed as 'partially hydrogenated oils' on many labels",
          "Found in fried foods, some margarines, and processed baked goods"
        ],
        "tldr":
            "Synthetic fats that harden brain cell membranes and block dopamine signaling; avoid completely.",
        "adhdMedInteractions": {
          "Adderall":
              "Reduces the baseline efficacy of the dopaminergic system.",
          "Vyvanse":
              "May contribute to 'foggy' focus and poor cognitive endurance.",
          "Ritalin":
              "Blunts the signal-to-noise ratio in the prefrontal cortex."
        }
      },
      {
        "id": "alcohol",
        "name": "Alcohol",
        "category": "Substance",
        "description":
            "CNS depressant that disrupts dopamine regulation, depletes essential brain nutrients, and ruins sleep quality.",
        "status": "avoid",
        "focusLevel": 1,
        "mechanismOfAction":
            "Alcohol disrupts the fine-tuning of the dopamine system and causes rebound anxiety. It significantly impairs the prefrontal cortex (executive function) and depletes B-vitamins and magnesium, which are essential cofactors for neurotransmitter synthesis. It also ruins REM sleep architecture, vital for cognitive recovery.",
        "detailedBenefits": <String>[],
        "timingRationale":
            "AVOID: Consumption disrupts neurodevelopment and cognitive recovery.",
        "scientificEvidenceRank": 80,
        "studyLinks": {
          "Alcohol and dopamine dysregulation":
              "https://pubmed.ncbi.nlm.nih.gov/28198205/"
        },
        "dosageByWeight": {
          "40-60": "0mg (AVOID)",
          "60-80": "0mg (AVOID)",
          "80-100": "0mg (AVOID)",
          "100-120": "0mg (AVOID)"
        },
        "dosageFrequency": "Eliminate from diet",
        "dosageWarnings": [
          "Depletes B-vitamins and Magnesium critical for ADHD focus",
          "Severely disrupts sleep architecture (no recovery focus)",
          "May significantly interact with ADHD medications",
          "Reduces executive function for 24-48 hours after consumption"
        ],
        "tldr":
            "Depletes vitamins and ruins sleep/dopamine balance; check liquid supplements for alcohol content.",
        "adhdMedInteractions": {
          "Adderall":
              "DANGEROUS: Masks intoxication levels and increases cardiovascular strain.",
          "Vyvanse":
              "High risk of heart rate spikes and extreme next-day anxiety.",
          "Ritalin":
              "Can create a dangerous state of both sedation and stimulation (cocaine-like effect in some metabolism pathways)."
        }
      },
    ];

    try {
      AppLogger.i(
          'Starting seeding process for ${supplements.length} items...');
      final batch = _firestore.batch();

      for (var supplement in supplements) {
        final docRef = _firestore
            .collection('supplements')
            .doc(supplement['id'] as String);
        batch.set(docRef, supplement);
      }

      if (kDebugMode) {
        AppLogger.d('Committing seeding batch...');
      }
      await batch.commit();
      if (kDebugMode) {
        AppLogger.i('Successfully seeded ${supplements.length} supplements');
      }
    } catch (e) {
      AppLogger.e('CRITICAL FAILURE in SeedingService', e);
      if (kDebugMode) {
        AppLogger.e('Error seeding supplements', e);
      }
      rethrow;
    }
  }

  Future<void> createTestUser(String email, String password) async {
    try {
      final auth = FirebaseAuth.instance;
      UserCredential credential;

      try {
        credential = await auth.createUserWithEmailAndPassword(
          email: email,
          password: password,
        );
      } catch (e) {
        // User likely already exists, sign in instead
        credential = await auth.signInWithEmailAndPassword(
          email: email,
          password: password,
        );
      }

      final uid = credential.user!.uid;

      // Create/Update user document in Firestore
      await _firestore.collection('users').doc(uid).set({
        'id': uid,
        'email': email,
        'displayName': 'Test User',
        'createdAt': DateTime.now().toIso8601String(),
        'hasCompletedOnboarding': true,
        'unlockedAchievements': <String>[],
      });
      AppLogger.i('Test user configured successfully: $email');
    } catch (e) {
      AppLogger.e('Failed to configure test user', e);
    }
  }
}
