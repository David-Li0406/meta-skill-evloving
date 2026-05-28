import 'package:flutter/material.dart';
import '../../utils/logger.dart';
import '../../domain/entities/article.dart';
import '../../domain/entities/faq_item.dart';
import '../../domain/entities/study.dart';
import '../../domain/entities/educational_article.dart';
import '../../domain/repositories/article_repository.dart';

class ScienceHubViewModel extends ChangeNotifier {
  final ArticleRepository _repository;

  ScienceHubViewModel(this._repository);

  String _searchQuery = '';
  String get searchQuery => _searchQuery;
  bool get isSearching => _searchQuery.isNotEmpty;

  Article? _articleOfTheDay;
  Article? get articleOfTheDay => _articleOfTheDay;

  List<Article> _articles = [];
  List<Article> get articles => _articles;

  List<FaqItem> _faqs = [];
  List<FaqItem> get faqs => _faqs;

  String _selectedFaqCategory = 'All';
  String get selectedFaqCategory => _selectedFaqCategory;

  List<FaqItem> get filteredFaqs {
    if (_searchQuery.isNotEmpty) {
      return _faqs
          .where((faq) =>
              faq.question.toLowerCase().contains(_searchQuery.toLowerCase()) ||
              faq.answer.toLowerCase().contains(_searchQuery.toLowerCase()))
          .toList();
    }
    if (_selectedFaqCategory == 'All') return _faqs;
    return _faqs.where((faq) => faq.category == _selectedFaqCategory).toList();
  }

  List<Study> _studies = [];
  List<Study> get studies => _studies;

  String _selectedResearchCategory = 'All';
  String get selectedResearchCategory => _selectedResearchCategory;

  List<Study> get filteredStudies {
    if (_searchQuery.isNotEmpty) {
      return _studies
          .where((study) =>
              study.title.toLowerCase().contains(_searchQuery.toLowerCase()) ||
              study.keyFindings
                  .toLowerCase()
                  .contains(_searchQuery.toLowerCase()))
          .toList();
    }
    if (_selectedResearchCategory == 'All') return _studies;
    return _studies
        .where((study) => study.category == _selectedResearchCategory)
        .toList();
  }

  List<EducationalArticle> _educationalArticles = [];
  List<EducationalArticle> get educationalArticles => _educationalArticles;

  String _selectedEduCategory = 'All';
  String get selectedEduCategory => _selectedEduCategory;

  List<EducationalArticle> get filteredEduArticles {
    if (_searchQuery.isNotEmpty) {
      return _educationalArticles
          .where((article) =>
              article.title
                  .toLowerCase()
                  .contains(_searchQuery.toLowerCase()) ||
              article.summary
                  .toLowerCase()
                  .contains(_searchQuery.toLowerCase()))
          .toList();
    }
    if (_selectedEduCategory == 'All') return _educationalArticles;
    return _educationalArticles
        .where((article) => article.category == _selectedEduCategory)
        .toList();
  }

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  void setFaqCategory(String category) {
    _selectedFaqCategory = category;
    _searchQuery = '';
    notifyListeners();
  }

  void setResearchCategory(String category) {
    _selectedResearchCategory = category;
    _searchQuery = '';
    notifyListeners();
  }

  void setEduCategory(String category) {
    _selectedEduCategory = category;
    _searchQuery = '';
    notifyListeners();
  }

  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  Future<void> loadData() async {
    _isLoading = true;
    notifyListeners();

    try {
      _articleOfTheDay = await _repository.getArticleOfTheDay();
      _articles = await _repository.getArticles();
      _loadFaqs();
      _loadStudies();
      _loadEducationalArticles();
    } catch (e) {
      AppLogger.e('Error loading science hub data', e);
    }

    _isLoading = false;
    notifyListeners();
  }

  void _loadFaqs() {
    _faqs = [
      FaqItem(
        id: 'faq-1',
        question: 'Can I take supplements with my ADHD medication?',
        answer:
            'Most supplements are safe to combine with ADHD medications, but timing and specific interactions matter. **Critical exception: Vitamin C** must be taken 1+ hours BEFORE or 4+ hours AFTER stimulants (Adderall, Vyvanse) as it can reduce medication effectiveness by 30-50%. Caffeine should be used cautiously as it has additive stimulant effects. Always consult your prescribing physician before adding supplements, especially if you take multiple medications.',
        category: 'Safety',
        relatedSupplements: ['Vitamin C', 'Caffeine', 'Magnesium'],
      ),
      FaqItem(
        id: 'faq-2',
        question: 'Why does timing matter for Vitamin C and stimulants?',
        answer:
            'Vitamin C (ascorbic acid) acidifies urine, which increases the excretion rate of amphetamine-based stimulants like Adderall and Vyvanse. This can reduce blood levels of the medication by 30-50%, significantly decreasing effectiveness. To avoid this interaction, take Vitamin C at least 1 hour before your morning dose or wait 4+ hours after. Evening dosing (after medication has worn off) is often the safest approach.',
        category: 'Dosing',
        relatedSupplements: ['Vitamin C'],
      ),
      FaqItem(
        id: 'faq-3',
        question:
            'What\'s the difference between methylated and regular B vitamins?',
        answer:
            'Methylated B vitamins (like methylfolate and methylcobalamin) are "pre-activated" forms that bypass a genetic conversion step. About 40-60% of people have MTHFR gene variants that reduce their ability to convert regular folic acid and B12 into usable forms. Methylated versions are immediately bioavailable and often more effective for neurotransmitter synthesis, especially for dopamine and serotonin production critical in ADHD.',
        category: 'General',
        relatedSupplements: ['B-Complex Vitamins'],
      ),
      FaqItem(
        id: 'faq-4',
        question: 'How long until I notice effects from supplements?',
        answer:
            'Timeline varies by supplement type:\n\n**Immediate (30-90 min):** Caffeine, L-Theanine, Mucuna Pruriens\n**Same day (2-6 hours):** Alpha-GPC, Rhodiola, Ginseng\n**1-2 weeks:** Omega-3, Magnesium, Creatine (requires loading)\n**2-4 weeks:** Ashwagandha, NAC, B-Complex (neurotransmitter support)\n**4-8 weeks:** Curcumin, CoQ10 (cellular/mitochondrial changes)\n\nConsistency is key. Many supplements build effects over time rather than providing immediate results.',
        category: 'General',
        relatedSupplements: ['Omega-3', 'Magnesium', 'Ashwagandha', 'Creatine'],
      ),
      FaqItem(
        id: 'faq-5',
        question: 'Do I need to cycle certain supplements?',
        answer:
            'Yes, some supplements require cycling to prevent tolerance or depletion:\n\n**MUST cycle:**\n• Huperzine A: 5 days on / 2 days off (24+ hour half-life)\n• Mucuna Pruriens: 3-5 days on / 2-3 days off (prevents dopamine depletion)\n\n**Recommended cycling:**\n• Caffeine: Take breaks to prevent tolerance\n• Adaptogens (Rhodiola, Ginseng): 5 days on / 2 days off for some users\n\n**No cycling needed:**\n• Omega-3, Magnesium, B vitamins, Zinc - safe for daily long-term use',
        category: 'Dosing',
        relatedSupplements: ['Huperzine A', 'Mucuna Pruriens', 'Rhodiola'],
      ),
      FaqItem(
        id: 'faq-6',
        question: 'Is it safe to take multiple supplements together?',
        answer:
            'Generally yes, but consider:\n\n**Synergistic combinations (good):**\n• Magnesium + B6 (enhances absorption)\n• Caffeine + L-Theanine (reduces jitters)\n• Omega-3 + Vitamin D (fat-soluble absorption)\n\n**Competitive absorption (separate timing):**\n• Zinc + Copper (compete for absorption)\n• Calcium + Magnesium (take separately)\n• High-dose Vitamin C + Copper (inhibits absorption)\n\n**Avoid combining:**\n• 5-HTP + SSRIs (serotonin syndrome risk)\n• St. John\'s Wort + most medications (extensive interactions)\n\nStart with 1-2 supplements and add gradually to identify what works.',
        category: 'Safety',
        relatedSupplements: ['Magnesium', 'Zinc', '5-HTP', 'Omega-3'],
      ),
      FaqItem(
        id: 'faq-7',
        question: 'Should I take supplements with food or on an empty stomach?',
        answer:
            '**With food (fat-soluble):**\n• Omega-3, CoQ10, Curcumin, Vitamin D - require dietary fat for absorption\n• Vinpocetine, Ginseng - better absorption with meals\n\n**Empty stomach (30 min before meals):**\n• NAC - food reduces absorption by ~30%\n• Mucuna Pruriens - protein competes with L-DOPA\n• Amino acids (L-Tyrosine, 5-HTP) - better absorption alone\n\n**Flexible (with or without food):**\n• B vitamins, Magnesium, Zinc, Creatine\n• Alpha-GPC, Rhodiola, Ashwagandha\n\nIf a supplement causes nausea, take it with food regardless of optimal timing.',
        category: 'Dosing',
        relatedSupplements: ['Omega-3', 'NAC', 'Curcumin', 'Alpha-GPC'],
      ),
      FaqItem(
        id: 'faq-8',
        question:
            'What does "evidence quality" mean in the supplement ratings?',
        answer:
            'Our evidence rankings (0-100) reflect:\n\n**High (80-100):** Multiple high-quality RCTs, meta-analyses, consistent results\n• Example: Vitamin C (88), Melatonin (89), B-Complex (85)\n\n**Moderate (60-79):** Some RCTs, observational studies, mixed results\n• Example: Green Tea Extract (77), Alpha-GPC (78), Ginseng (74)\n\n**Low (40-59):** Limited studies, small sample sizes, inconsistent findings\n• Example: DMAE (42), Valerian (58)\n\nHigher scores indicate stronger scientific backing, but individual response varies. Even high-evidence supplements may not work for everyone.',
        category: 'General',
        relatedSupplements: ['Vitamin C', 'Melatonin', 'B-Complex'],
      ),
      FaqItem(
        id: 'faq-9',
        question: 'Can supplements replace ADHD medication?',
        answer:
            '**No.** Supplements support brain function but do not replace prescription ADHD medications. Research shows:\n\n• Stimulants (Adderall, Vyvanse, Ritalin) have ~70-80% response rates for core ADHD symptoms\n• Supplements typically provide 10-30% improvement in specific areas (focus, mood, sleep)\n• Supplements work best as **adjunct therapy** alongside medication and behavioral strategies\n\nSome people use supplements to:\n• Reduce medication dose (under medical supervision)\n• Manage side effects (sleep, appetite)\n• Support neurotransmitter health long-term\n\nNever stop or reduce medication without consulting your prescribing physician.',
        category: 'General',
        relatedSupplements: [],
      ),
      FaqItem(
        id: 'faq-10',
        question: 'Are there supplements I should avoid with ADHD?',
        answer:
            '**Avoid or use extreme caution:**\n\n• **St. John\'s Wort** - Reduces birth control effectiveness 50%+, extensive drug interactions\n• **Kava Kava** - Liver toxicity risk, banned in several countries\n• **High-dose standalone B6 (>100mg)** - Risk of irreversible nerve damage\n• **DMAE** - Weak evidence, unpredictable effects, may worsen symptoms\n\n**Conditional (medical supervision required):**\n• **5-HTP** - NEVER with SSRIs/SNRIs (serotonin syndrome risk)\n• **Copper** - Most ADHD patients have high copper; only supplement if deficient\n• **Mucuna Pruriens** - Must cycle; risk of dopamine depletion\n\nAlways check "Avoid" category in the Library for detailed warnings.',
        category: 'Safety',
        relatedSupplements: [
          'St. John\'s Wort',
          'Kava Kava',
          'High-dose B6',
          '5-HTP'
        ],
      ),
      FaqItem(
        id: 'faq-11',
        question: 'How do I know if a supplement is working?',
        answer:
            'Track specific metrics:\n\n**Subjective measures:**\n• Focus duration (how long can you work without distraction?)\n• Mental clarity (brain fog vs. sharp thinking)\n• Mood stability (emotional regulation)\n• Sleep quality (time to fall asleep, wake feeling rested)\n\n**Objective measures:**\n• Work output (tasks completed per day)\n• Medication effectiveness (do you need less?)\n• Side effect reduction (appetite, sleep, anxiety)\n\n**Best practice:**\n• Add ONE supplement at a time (2-4 week trial)\n• Keep a daily journal of the above metrics\n• Use the app\'s tracking features\n• If no improvement after 4-6 weeks, discontinue\n\nPlacebo effect is real - objective tracking helps identify true benefits.',
        category: 'General',
        relatedSupplements: [],
      ),
      FaqItem(
        id: 'faq-12',
        question:
            'What\'s the difference between "beneficial" and "conditional" supplements?',
        answer:
            '**Beneficial supplements:**\n• Strong safety profile for most people\n• Supported by research for ADHD/cognitive function\n• Minimal drug interactions\n• Example: Omega-3, Magnesium, B-Complex, Creatine\n\n**Conditional/Cautionary supplements:**\n• Effective BUT have significant risks or limitations\n• Require medical supervision or specific conditions\n• May have drug interactions or side effects\n• Example: Caffeine (additive stimulation), Melatonin (hormone), 5-HTP (SSRI interaction), Copper (often already high in ADHD)\n\nConditional doesn\'t mean "bad" - it means "use carefully with awareness of risks." Many people benefit from conditional supplements under proper guidance.',
        category: 'General',
        relatedSupplements: ['Caffeine', 'Melatonin', '5-HTP', 'Copper'],
      ),
    ];
  }

  void _loadStudies() {
    _studies = [
      Study(
        id: 'study-1',
        title: 'Omega-3 fatty acids for ADHD',
        authors: 'Bloch MH, Qawasmi A.',
        year: 2011,
        pubmedUrl: 'https://pubmed.ncbi.nlm.nih.gov/21961774/',
        category: 'Essential Fatty Acids',
        evidenceQuality: EvidenceQuality.high,
        keyFindings:
            'Meta-analysis showed a small but significant effect of omega-3 fatty acids in improving ADHD symptoms. Higher doses of EPA were associated with greater efficacy.',
        relatedSupplements: ['Omega-3 Fish Oil'],
      ),
      Study(
        id: 'study-2',
        title: 'L-theanine and caffeine synergy',
        authors: 'Owen GN, et al.',
        year: 2008,
        pubmedUrl: 'https://pubmed.ncbi.nlm.nih.gov/18681988/',
        category: 'Nootropics',
        evidenceQuality: EvidenceQuality.high,
        keyFindings:
            'The combination of L-theanine and caffeine significantly improved attention and alertness compared to caffeine alone, while reducing jitteriness.',
        relatedSupplements: ['L-Theanine', 'Caffeine'],
      ),
      Study(
        id: 'study-3',
        title: 'Zinc for ADHD: A systematic review',
        authors: 'Zinc Research Group',
        year: 2015,
        pubmedUrl: 'https://pubmed.ncbi.nlm.nih.gov/21350130/',
        category: 'Vitamins & Minerals',
        evidenceQuality: EvidenceQuality.moderate,
        keyFindings:
            'Zinc supplementation may be beneficial as an adjunct to stimulant therapy, especially in populations with low zinc status.',
        relatedSupplements: ['Zinc'],
      ),
      Study(
        id: 'study-4',
        title: 'Ashwagandha for stress and focus',
        authors: 'Chandrasekhar K, et al.',
        year: 2012,
        pubmedUrl: 'https://pubmed.ncbi.nlm.nih.gov/23439798/',
        category: 'Adaptogens',
        evidenceQuality: EvidenceQuality.high,
        keyFindings:
            'High-concentration full-spectrum Ashwagandha root extract safely and effectively improves an individual\'s resistance towards stress and thereby improves self-assessed quality of life.',
        relatedSupplements: ['Ashwagandha (KSM-66)'],
      ),
      Study(
        id: 'study-5',
        title: 'Magnesium and Vitamin B6 for ADHD',
        authors: 'Mousain-Bosc M, et al.',
        year: 2006,
        pubmedUrl: 'https://pubmed.ncbi.nlm.nih.gov/16846314/',
        category: 'Vitamins & Minerals',
        evidenceQuality: EvidenceQuality.moderate,
        keyFindings:
            'Combined magnesium and B6 supplementation significantly improved ADHD symptoms (hyperactivity, aggressiveness) compared to baseline.',
        relatedSupplements: ['Magnesium Glycinate', 'Vitamin B6'],
      ),
      Study(
        id: 'study-6',
        title: 'Creatine and cognitive performance',
        authors: 'Rae C, et al.',
        year: 2003,
        pubmedUrl: 'https://pubmed.ncbi.nlm.nih.gov/14561278/',
        category: 'Nootropics',
        evidenceQuality: EvidenceQuality.high,
        keyFindings:
            'Oral creatine monohydrate supplementation significantly improved performance on intelligence and working memory tests.',
        relatedSupplements: ['Creatine Monohydrate'],
      ),
      Study(
        id: 'study-7',
        title: 'Rhodiola Rosea for mental fatigue',
        authors: 'Shevtsov VA, et al.',
        year: 2003,
        pubmedUrl: 'https://pubmed.ncbi.nlm.nih.gov/12725561/',
        category: 'Adaptogens',
        evidenceQuality: EvidenceQuality.moderate,
        keyFindings:
            'Rhodiola extract showed anti-fatigue effects and improved task performance under stress.',
        relatedSupplements: ['Rhodiola Rosea'],
      ),
      Study(
        id: 'study-8',
        title: 'NAC and impulse control',
        authors: 'Grant JE, et al.',
        year: 2009,
        pubmedUrl: 'https://pubmed.ncbi.nlm.nih.gov/19541530/',
        category: 'Nootropics',
        evidenceQuality: EvidenceQuality.moderate,
        keyFindings:
            'N-Acetyl Cysteine significantly reduced impulsive behaviors in clinical trials, suggesting benefit for ADHD impulsivity.',
        relatedSupplements: ['N-Acetyl Cysteine (NAC)'],
      ),
    ];
  }

  void _loadEducationalArticles() {
    _educationalArticles = [
      EducationalArticle(
        id: '1',
        title: 'Understanding ADHD Neurotransmitter Deficiencies',
        summary:
            'A deep dive into how dopamine and norepinephrine affect ADHD brains and how supplementation can help.',
        content: '''# Understanding ADHD Neurotransmitter Deficiencies

ADHD is increasingly understood not just as a behavioral disorder, but as a complex interplay of neurotransmitter systems that regulate attention, motivation, and executive function.

## The Dopamine Deficiency Hypothesis
Dopamine is the brain's primary reward and motivation neurotransmitter. In many ADHD brains, there is evidence of lower dopamine receptor density or efficiency. This means that activities requiring sustained effort but offering delayed rewards are difficult to maintain because the brain isn't receiving the typical "dopamine reward" for that effort.

## Norepinephrine and Alertness
Norepinephrine is crucial for alertness and filtering out irrelevant information. When norepinephrine levels are optimized, the "signal-to-noise ratio" in the brain improves, allowing you to focus on a single task while ignoring background distractions.

## How Supplementation Can Help
Nutritional precursors can support the body's natural production of these chemicals:
- **L-Tyrosine:** The direct precursor to dopamine. Taking L-Tyrosine on an empty stomach can help increase the pool of available dopamine during periods of stress.
- **B-Complex:** Specifically B6, B9 (folate), and B12 are critical co-factors in the synthesis of neurotransmitters.
- **Magnesium:** Helps regulate the release and reuptake of neurotransmitters, ensuring the system doesn't become overstimulated.

Understanding these biological foundations helps shift the perspective from a "lack of willpower" to a biological need for neurochemical support.''',
        imageUrl:
            'https://images.unsplash.com/photo-1559757175-0eb30cd8c063?auto=format&fit=crop&q=80&w=800',
        category: 'Neuroscience',
        relatedSupplements: ['L-Tyrosine', 'DL-Phenylalanine', 'B-Complex'],
        keyTakeaways: [
          'ADHD is associated with lower dopamine availability.',
          'Tyrosine is a precursor to dopamine.',
          'B6 is essential for neurotransmitter synthesis.'
        ],
        readTime: '6 min',
        author: 'Dr. Sarah Wilson',
        publishedDate: DateTime(2023, 11, 15),
      ),
      EducationalArticle(
        id: '2',
        title: 'The Gut-Brain Axis: Nutrition and ADHD',
        summary:
            'How your dietary choices and gut microbiome influence focus, mood, and cognitive control.',
        content: '''# The Gut-Brain Axis: Nutrition and ADHD

The saying "you are what you eat" takes on a new meaning when we examine the gut-brain axis—the bidirectional communication line between your digestive system and your brain.

## The "Second Brain"
The gut contains hundreds of millions of neurons, often called the enteric nervous system. Furthermore, an estimated 90% of the body's serotonin is produced in the gut, not the brain.

## Inflammation and Focus
Inflammation in the digestive tract, often caused by food sensitivities or high sugar intake, can trigger systemic inflammation that crosses the blood-brain barrier. This is a common cause of "brain fog" and increased ADHD symptoms.

## Probiotics and Executive Function
Emerging research suggests that specific probiotic strains may help improve neurotransmitter balance and reduce the hyperactive symptoms of ADHD.

## Practical Steps:
1. **Reduce Refined Sugars:** Sugar spikes and crashes are the enemy of focus.
2. **Increase Omega-3s:** These healthy fats reduce brain inflammation.
3. **Hydration:** Even mild dehydration can significantly impair executive function.''',
        imageUrl:
            'https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&q=80&w=800',
        category: 'Nutrition',
        relatedSupplements: ['Probiotics', 'Omega-3', 'Magnesium'],
        keyTakeaways: [
          'High sugar diets can exacerbate ADHD symptoms.',
          'Probiotics may improve executive function.',
          'Inflammation in the gut can lead to "brain fog".'
        ],
        readTime: '8 min',
        author: 'Marcus Chen, CNS',
        publishedDate: DateTime(2023, 12, 05),
      ),
      EducationalArticle(
        id: '3',
        title: 'Morning vs. Evening: Optimizing Supplement Timing',
        summary:
            'Why when you take your supplements matters as much as what you take for ADHD management.',
        content: '''# Morning vs. Evening: Optimizing Supplement Timing

Your body's circadian rhythm significantly affects how you process nutrients. Taking the right supplement at the wrong time can sometimes lead to poor results or sleep disruption.

## The Morning Protocol: Stimulate and Focus
The goal of the morning is to support neurotransmitter production and alertness.
- **Pre-Medication:** L-Tyrosine or DLPA should be taken 30-60 minutes before breakfast on an empty stomach.
- **With Breakfast:** Omega-3s and Vitamin D require fat for absorption. Always take these with a meal.
- **The B-Vitamin Rule:** B-Complex vitamins are energizing and should generally be taken before noon.

## The Evening Protocol: Rest and Repair
The goal of the evening is to reduce cortisol and support restorative sleep.
- **Magnesium Glycinate:** Perhaps the most famous evening supplement. It supports GABA production and helps the nervous system relax.
- **Zinc:** Best taken in the evening to support endocrine health and recovery.
- **L-Theanine:** Can be used in the evening to "quiet the brain" without causing drowsiness.

## The Vitamin C Stimulant Rule
**Warning:** Never take high-dose Vitamin C within 4 hours of taking stimulant medication (Vyvanse, Adderall), as it can interfere with the medication's absorption and effectiveness.''',
        imageUrl:
            'https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&q=80&w=800',
        category: 'Lifestyle',
        relatedSupplements: ['Magnesium Glycinate', 'Omega-3', 'Zinc'],
        keyTakeaways: [
          'Take stimulating supplements (ALCAR, Tyrosine) in the morning.',
          'Fat-soluble nutrients (Omega-3) require a meal with fat.',
          'Magnesium is best taken in the evening for sleep quality.'
        ],
        readTime: '5 min',
        author: 'Elena Rodriguez, RD',
        publishedDate: DateTime(2024, 01, 10),
      ),
      EducationalArticle(
        id: '4',
        title: 'The Methylation Cycle and ADHD',
        summary:
            'Exploring the genetic link between MTHFR mutations, methylation, and neurotransmitter balance.',
        content: '''# The Methylation Cycle and ADHD

Methylation is a fundamental biochemical process that occurs billions of times every second in your body. It is responsible for "turning on" and "turning off" genes, repairing DNA, and crucially, producing neurotransmitters like Dopamine and Serotonin.

## The MTHFR Connection
The MTHFR gene provides instructions for making an enzyme that processes folate. Many individuals with ADHD carry variants (like C677T or A1298C) that reduce this enzyme's efficiency by 30-70%.

## Impacts on Brain Health:
1. **BH4 Production:** Methylation is required to produce BH4, a critical cofactor for making dopamine and norepinephrine.
2. **Homocysteine Clearout:** Poor methylation leads to high homocysteine, which can cause neuroinflammation.
3. **Neurotransmitter Breakdown:** COMT, the enzyme that breaks down dopamine in the prefrontal cortex, also requires methylation to function.

## Supporting the Cycle:
- **Methylated B-Vitamins:** Using Methylfolate (5-MTHF) instead of folic acid.
- **Methyl-B12:** Using Methylcobalamin instead of Cyanocobalamin.
- **TMG/Betaine:** Provides additional methyl groups to support the cycle.''',
        imageUrl:
            'https://images.unsplash.com/photo-1530210124550-912dc1381cb8?auto=format&fit=crop&q=80&w=800',
        category: 'Neuroscience',
        relatedSupplements: ['Methylfolate', 'Methyl-B12', 'TMG'],
        keyTakeaways: [
          'Methylation is critical for neurotransmitter synthesis.',
          'MTHFR variants are common in the ADHD population.',
          'Avoid synthetic folic acid if you have methylation issues.'
        ],
        readTime: '7 min',
        author: 'Dr. Sarah Jenkins',
        publishedDate: DateTime(2024, 01, 15),
      ),
      EducationalArticle(
        id: '5',
        title: 'Building Your First ADHD Supplement Stack',
        summary:
            'A step-by-step guide to starting your journey with evidence-based supplementation.',
        content: '''# Building Your First ADHD Supplement Stack

Starting a supplement protocol can be overwhelming. The "Daily Stack" approach focuses on foundational nutrients first, followed by targeted support.

## Step 1: The Foundation (Core Nutrients)
Before adding advanced nootropics, ensure your brain has the basic building blocks:
- **Omega-3 Fatty Acids (EPA/DHA):** Support brain structure and reduce inflammation.
- **Magnesium:** Foundational for over 300 enzymatic reactions.
- **B-Complex:** The "fuel" for neurotransmitter production.

## Step 2: Targeted Support (The "Nudges")
Once your foundation is solid, look at your specific symptoms:
- **For Energy/Fatigue:** ALCAR or Rhodiola Rosea.
- **For Focus/Clarity:** Bacopa Monnieri or Ginkgo Biloba.
- **For Rebound/Crash:** L-Theanine or NAC.

## Step 3: Safety and Tracking
- **The "One-at-a-Time" Rule:** Never start two new supplements on the same day. Wait 3-5 days between new additions to monitor effects.
- **Consistent Logging:** Use the Daily Stack tracker to log your symptoms and identify what actually works for you.
- **Consult Your Doctor:** Supplements can interact with medications. Always share your stack with your healthcare provider.''',
        imageUrl:
            'https://images.unsplash.com/photo-1584017911766-d451b3d0e843?auto=format&fit=crop&q=80&w=800',
        category: 'Lifestyle',
        relatedSupplements: ['Omega-3', 'Magnesium', 'B-Complex'],
        keyTakeaways: [
          'Start with foundational nutrients before advanced nootropics.',
          'Introduce only one new supplement at a time.',
          'Consistency in tracking is key to finding your ideal stack.'
        ],
        readTime: '6 min',
        author: 'Albie Calvo, Founder',
        publishedDate: DateTime(2024, 01, 20),
      ),
    ];
  }
}
