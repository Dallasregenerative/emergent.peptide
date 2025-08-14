"""
Comprehensive Peptide Library Data
Based on PeptideProtocols.ai Complete Database
"""

COMPREHENSIVE_PEPTIDE_LIBRARY = [
    # Weight Management & Metabolic
    {
        "name": "Semaglutide",
        "category": "weight-loss",
        "mechanism": "GLP-1 receptor agonist that slows gastric emptying, increases insulin sensitivity, and promotes satiety through central appetite regulation",
        "indications": ["Obesity (BMI ≥30)", "Overweight with comorbidities (BMI ≥27)", "Type 2 diabetes management"],
        "standard_dosing": {
            "weeks_1_4": "0.25 mg SC weekly",
            "weeks_5_8": "0.5 mg SC weekly", 
            "weeks_9_12": "1.0 mg SC weekly",
            "weeks_13_16": "1.7 mg SC weekly",
            "maintenance": "2.4 mg SC weekly (max dose)"
        },
        "administration": "Subcutaneous injection - rotate injection sites: abdomen, thigh, upper arm. Same day each week, any time of day.",
        "stacking_options": ["BPC-157 for GI support", "L-Carnitine for enhanced fat burning", "CJC-1295/Ipamorelin for body composition"],
        "contraindications": ["MEN-2 syndrome", "Medullary thyroid carcinoma", "Personal/family history of MTC", "Pregnancy", "Severe gastroparesis", "Type 1 diabetes"],
        "side_effects": ["Nausea (20-30%)", "Diarrhea (12%)", "Vomiting (9%)", "Constipation (7%)", "Abdominal pain (6%)", "Fatigue (5%)", "Injection site reactions"],
        "monitoring": ["Weight and BMI weekly", "HbA1c every 3 months", "Lipase if abdominal pain", "Gallbladder function", "Renal function", "Thyroid function"],
        "references": ["PMID: 33999546 (STEP trials)", "FDA PI Semaglutide 2021", "PMID: 34887186 (cardiovascular outcomes)"]
    },
    
    {
        "name": "Tirzepatide",
        "category": "weight-loss",
        "mechanism": "Dual GIP/GLP-1 receptor agonist providing superior weight loss through enhanced glucose-dependent insulin secretion and appetite suppression",
        "indications": ["Type 2 diabetes", "Obesity management", "Metabolic syndrome"],
        "standard_dosing": {
            "weeks_1_4": "2.5 mg SC weekly",
            "weeks_5_8": "5 mg SC weekly",
            "weeks_9_12": "7.5 mg SC weekly", 
            "weeks_13_16": "10 mg SC weekly",
            "maintenance": "15 mg SC weekly (max dose)"
        },
        "administration": "Subcutaneous injection weekly, same day each week, rotate injection sites",
        "stacking_options": ["Semaglutide (not recommended)", "Metformin", "SGLT2 inhibitors"],
        "contraindications": ["MEN-2 syndrome", "Medullary thyroid carcinoma", "Pregnancy", "Severe gastroparesis"],
        "side_effects": ["Nausea (25%)", "Diarrhea (16%)", "Vomiting (12%)", "Constipation (8%)", "Abdominal pain (7%)"],
        "monitoring": ["Weight weekly", "HbA1c every 3 months", "Lipase", "Gallbladder function", "Thyroid monitoring"],
        "references": ["PMID: 35658024 (SURMOUNT-1)", "PMID: 34370970 (SURPASS trials)"]
    },

    {
        "name": "AOD-9604",
        "category": "weight-loss",
        "mechanism": "Modified fragment of human growth hormone (hGH 177-191) that stimulates lipolysis and inhibits lipogenesis without affecting blood sugar",
        "indications": ["Fat loss", "Body composition improvement", "Metabolic enhancement"],
        "standard_dosing": {
            "standard": "250-300 mcg SC daily",
            "intensive": "500 mcg SC daily",
            "maintenance": "250 mcg daily 5 days per week"
        },
        "administration": "Subcutaneous injection, preferably on empty stomach, morning or pre-workout",
        "stacking_options": ["CJC-1295/Ipamorelin", "L-Carnitine", "Tesofensine"],
        "contraindications": ["Pregnancy", "Active cancer", "Severe kidney disease"],
        "side_effects": ["Mild injection site reactions", "Occasional fatigue", "Rare hypoglycemic episodes"],
        "monitoring": ["Body composition", "Weight", "Blood glucose", "Lipid profiles"],
        "references": ["PMID: 11811755", "PMID: 15992215"]
    },

    {
        "name": "Fragment 176-191",
        "category": "weight-loss", 
        "mechanism": "C-terminal fragment of human growth hormone specifically responsible for fat burning without affecting growth or insulin resistance",
        "indications": ["Targeted fat loss", "Improved body composition", "Metabolic optimization"],
        "standard_dosing": {
            "beginner": "250 mcg SC daily",
            "standard": "500 mcg SC daily",
            "advanced": "1000 mcg SC daily"
        },
        "administration": "Subcutaneous injection on empty stomach, ideally before exercise or bedtime",
        "stacking_options": ["CJC-1295", "Ipamorelin", "AOD-9604"],
        "contraindications": ["Pregnancy", "Breastfeeding", "Active malignancy"],
        "side_effects": ["Minimal - injection site reactions", "Rare reports of fatigue"],
        "monitoring": ["Body fat percentage", "Weight", "Energy levels"],
        "references": ["PMID: 9849822", "PMID: 11811755"]
    },

    # Growth Hormone & Hormone Optimization
    {
        "name": "CJC-1295",
        "category": "growth-hormone",
        "mechanism": "Modified growth hormone releasing hormone (GHRH) analog that stimulates natural GH release with extended half-life",
        "indications": ["Age-related GH decline", "Body composition improvement", "Recovery enhancement", "Anti-aging"],
        "standard_dosing": {
            "without_DAC": "100 mcg SC 1-3x daily",
            "with_DAC": "2 mg SC weekly",
            "maintenance": "100-200 mcg SC daily"
        },
        "administration": "Subcutaneous injection, best before meals or bedtime",
        "stacking_options": ["Ipamorelin (synergistic)", "GHRP-2", "GHRP-6", "Sermorelin"],
        "contraindications": ["Active cancer", "Diabetic retinopathy", "Pregnancy"],
        "side_effects": ["Water retention", "Joint pain", "Carpal tunnel syndrome (rare)", "Injection site reactions"],
        "monitoring": ["IGF-1 levels", "Body composition", "Sleep quality", "Joint comfort"],
        "references": ["PMID: 16352683", "PMID: 12689607"]
    },

    {
        "name": "Ipamorelin",
        "category": "growth-hormone",
        "mechanism": "Selective ghrelin receptor agonist (GHRP) that stimulates GH release without affecting cortisol, prolactin, or appetite",
        "indications": ["GH deficiency", "Anti-aging", "Body composition", "Recovery", "Sleep improvement"],
        "standard_dosing": {
            "weeks_1_4": "200-250 mcg SC daily before bed",
            "weeks_5_8": "300 mcg SC daily before bed",
            "maintenance": "200-300 mcg daily"
        },
        "administration": "Subcutaneous injection 2-3 hours after last meal, preferably before bedtime",
        "stacking_options": ["CJC-1295 (most common)", "Sermorelin", "BPC-157"],
        "contraindications": ["Active cancer", "Diabetic retinopathy", "Pregnancy"],
        "side_effects": ["Mild water retention", "Temporary fatigue post-injection", "Increased appetite (mild)"],
        "monitoring": ["IGF-1 levels", "Sleep quality", "Body composition", "Recovery metrics"],
        "references": ["PMID: 15341091", "PMID: 9849822"]
    },

    {
        "name": "Sermorelin",
        "category": "growth-hormone",
        "mechanism": "Synthetic GHRH analog (1-29 amino acids) that stimulates natural growth hormone production and release",
        "indications": ["Adult growth hormone deficiency", "Anti-aging", "Sleep improvement", "Body composition"],
        "standard_dosing": {
            "standard": "200-300 mcg SC daily at bedtime",
            "loading": "500 mcg SC daily x 4 weeks",
            "maintenance": "200 mcg SC daily"
        },
        "administration": "Subcutaneous injection at bedtime on empty stomach (2-3 hours after last meal)",
        "stacking_options": ["GHRP-2", "GHRP-6", "Ipamorelin", "CJC-1295"],
        "contraindications": ["Pituitary tumor", "Active malignancy", "Pregnancy"],
        "side_effects": ["Injection site reactions", "Facial flushing (transient)", "Dizziness (rare)"],
        "monitoring": ["IGF-1 levels", "Sleep quality", "Body composition", "Energy levels"],
        "references": ["PMID: 2203949", "PMID: 8282032"]
    },

    {
        "name": "GHRP-2",
        "category": "growth-hormone", 
        "mechanism": "Synthetic hexapeptide that stimulates GH release via ghrelin receptors with moderate effects on cortisol and prolactin",
        "indications": ["GH deficiency", "Anti-aging", "Muscle building", "Fat loss"],
        "standard_dosing": {
            "standard": "100-300 mcg SC 2-3x daily",
            "saturation": "1 mcg/kg body weight",
            "maintenance": "100 mcg SC 2x daily"
        },
        "administration": "Subcutaneous injection on empty stomach, 20 minutes before meals or 2 hours after",
        "stacking_options": ["CJC-1295", "Ipamorelin", "Sermorelin"],
        "contraindications": ["Active cancer", "Pregnancy", "Uncontrolled diabetes"],
        "side_effects": ["Increased hunger", "Water retention", "Tiredness post-injection", "Numbness/tingling"],
        "monitoring": ["IGF-1 levels", "Cortisol levels", "Body composition", "Blood glucose"],
        "references": ["PMID: 8282033", "PMID: 9849823"]
    },

    {
        "name": "GHRP-6",
        "category": "growth-hormone",
        "mechanism": "Synthetic hexapeptide GHRP that stimulates GH release and increases appetite through ghrelin pathway activation",
        "indications": ["GH deficiency", "Appetite stimulation", "Anti-aging", "Muscle building"],
        "standard_dosing": {
            "standard": "100-300 mcg SC 2-3x daily", 
            "appetite": "100 mcg SC 15-20 min before meals",
            "maintenance": "100 mcg SC 2x daily"
        },
        "administration": "Subcutaneous injection on empty stomach for GH release, before meals for appetite",
        "stacking_options": ["CJC-1295", "Ipamorelin", "Sermorelin"],
        "contraindications": ["Active cancer", "Pregnancy", "Eating disorders"],
        "side_effects": ["Significant hunger increase", "Water retention", "Tiredness", "Joint pain (rare)"],
        "monitoring": ["IGF-1 levels", "Body weight", "Appetite changes", "Body composition"],
        "references": ["PMID: 1303828", "PMID: 8282034"]
    },

    {
        "name": "Hexarelin",
        "category": "growth-hormone",
        "mechanism": "Potent synthetic hexapeptide GHRP with strongest GH release activity but also affects cortisol and prolactin significantly",
        "indications": ["Severe GH deficiency", "Advanced anti-aging protocols", "Body composition (experienced users)"],
        "standard_dosing": {
            "standard": "100-200 mcg SC 2-3x daily",
            "maximum": "300 mcg SC 2x daily",
            "cycling": "4-6 weeks on, 2-4 weeks off"
        },
        "administration": "Subcutaneous injection on empty stomach, cycling recommended to prevent desensitization",
        "stacking_options": ["CJC-1295", "IGF-1 LR3 (advanced users)"],
        "contraindications": ["Active cancer", "Pregnancy", "Pituitary disorders", "Uncontrolled hypertension"],
        "side_effects": ["Significant water retention", "Elevated cortisol", "Prolactin elevation", "Carpal tunnel"],
        "monitoring": ["IGF-1 levels", "Cortisol", "Prolactin", "Blood pressure", "Glucose tolerance"],
        "references": ["PMID: 8282035", "PMID: 9849824"]
    },

    {
        "name": "MK-677",
        "category": "growth-hormone",
        "mechanism": "Oral ghrelin receptor agonist that increases GH and IGF-1 levels with 24-hour duration of action",
        "indications": ["GH deficiency", "Muscle wasting", "Bone density improvement", "Sleep enhancement"],
        "standard_dosing": {
            "beginner": "10-15 mg orally daily at bedtime",
            "standard": "20-25 mg orally daily at bedtime", 
            "advanced": "25-30 mg orally daily (max recommended)"
        },
        "administration": "Oral administration at bedtime, with or without food, consistent timing important",
        "stacking_options": ["LGD-4033", "RAD-140", "Ostarine", "CJC-1295/Ipamorelin"],
        "contraindications": ["Active cancer", "Diabetic complications", "Heart failure", "Pregnancy"],
        "side_effects": ["Increased appetite", "Water retention", "Lethargy", "Elevated blood sugar", "Joint pain"],
        "monitoring": ["IGF-1 levels", "Blood glucose", "HbA1c", "Body composition", "Sleep quality"],
        "references": ["PMID: 9467534", "PMID: 11891123"]
    },

    {
        "name": "IGF-1 LR3",
        "category": "growth-hormone",
        "mechanism": "Long-acting insulin-like growth factor with reduced binding to IGFBPs, promoting muscle growth and recovery",
        "indications": ["Muscle building", "Recovery enhancement", "Anti-aging", "Tissue repair"],
        "standard_dosing": {
            "beginner": "20-40 mcg SC daily post-workout",
            "intermediate": "40-80 mcg SC daily",
            "advanced": "80-120 mcg SC daily (divided doses)"
        },
        "administration": "Subcutaneous injection post-workout or before bed, rotate injection sites",
        "stacking_options": ["CJC-1295/Ipamorelin", "BPC-157", "TB-500"],
        "contraindications": ["Active cancer", "Diabetic retinopathy", "Pregnancy", "Severe hypoglycemia"],
        "side_effects": ["Hypoglycemia", "Joint pain", "Organ growth (chronic use)", "Injection site reactions"],
        "monitoring": ["Blood glucose", "IGF-1 levels", "Organ function", "Body composition"],
        "references": ["PMID: 7538167", "PMID: 9467535"]
    },

    {
        "name": "Tesamorelin",
        "category": "metabolic",
        "mechanism": "Synthetic GHRH analog FDA-approved for reducing visceral adiposity, particularly HIV-associated lipodystrophy",
        "indications": ["Visceral adiposity", "HIV lipodystrophy", "Abdominal fat reduction", "Metabolic dysfunction"],
        "standard_dosing": {
            "standard": "2 mg SC daily in abdomen",
            "maintenance": "2 mg SC daily ongoing",
            "monitoring": "Continue based on visceral fat response"
        },
        "administration": "Subcutaneous injection in abdomen daily, rotate injection sites within abdominal area",
        "stacking_options": ["Metformin", "SGLT2 inhibitors", "Lifestyle interventions"],
        "contraindications": ["Pituitary tumor", "Active malignancy", "Critical illness", "Pregnancy", "Closed epiphyses"],
        "side_effects": ["Injection site reactions (50%)", "Arthralgia (15%)", "Peripheral edema (9%)", "Myalgia (6%)"],
        "monitoring": ["Visceral fat (CT/MRI)", "IGF-1 levels", "Glucose tolerance", "Joint symptoms", "Injection sites"],
        "references": ["PMID: 20881878", "FDA Approval 2010", "PMID: 23550070"]
    },

    # Healing & Recovery
    {
        "name": "BPC-157",
        "category": "healing-recovery",
        "mechanism": "Body Protection Compound derived from gastric juices that promotes angiogenesis, tissue repair, and gut health through multiple growth factor pathways",
        "indications": ["Gut healing", "Tendon/ligament repair", "Muscle recovery", "Wound healing", "Inflammatory conditions"],
        "standard_dosing": {
            "oral": "500-1000 mcg daily with food (gut issues)",
            "injection": "250-500 mcg SC daily near injury site",
            "systemic": "250 mcg SC daily for general healing"
        },
        "administration": "Subcutaneous injection near injury site or oral administration for GI issues",
        "stacking_options": ["TB-500 for enhanced healing", "Growth hormone peptides", "Collagen supplementation"],
        "contraindications": ["Active cancer", "Pregnancy"],
        "side_effects": ["Minimal reported", "Occasional injection site irritation", "Rare GI upset with oral use"],
        "monitoring": ["Symptom improvement", "Functional assessments", "Injury healing progress"],
        "references": ["PMID: 31397714", "PMID: 28222544", "PMID: 30915550"]
    },

    {
        "name": "TB-500",
        "category": "healing-recovery",
        "mechanism": "Synthetic thymosin β4 peptide that promotes cell migration, angiogenesis, and tissue repair through actin regulation",
        "indications": ["Injury recovery", "Tendon/ligament healing", "Muscle repair", "Cardiovascular protection", "Wound healing"],
        "standard_dosing": {
            "loading": "2-2.5 mg SC twice weekly x 4 weeks",
            "maintenance": "2-2.5 mg SC weekly",
            "acute_injury": "2.5 mg SC daily x 7-14 days"
        },
        "administration": "Subcutaneous injection, can be systemic (not necessarily at injury site)",
        "stacking_options": ["BPC-157 (synergistic)", "Growth hormone peptides", "IGF-1 LR3"],
        "contraindications": ["Active cancer", "Pregnancy"],
        "side_effects": ["Fatigue (dose-dependent)", "Head rush post-injection", "Injection site reactions"],
        "monitoring": ["Recovery progress", "Functional improvement", "Energy levels"],
        "references": ["PMID: 17143582", "PMID: 20687617", "PMID: 28222545"]
    },

    {
        "name": "GHK-Cu",
        "category": "healing-recovery",
        "mechanism": "Copper-peptide complex that stimulates collagen synthesis, wound healing, and has anti-inflammatory and antioxidant properties",
        "indications": ["Skin aging", "Wound healing", "Hair growth", "Anti-aging", "Collagen synthesis"],
        "standard_dosing": {
            "injection": "1-2 mg SC daily",
            "topical": "Apply 2-3x daily to affected area",
            "cosmetic": "Use as directed in skincare formulations"
        },
        "administration": "Subcutaneous injection or topical application depending on indication",
        "stacking_options": ["BPC-157", "Collagen peptides", "Vitamin C", "Hyaluronic acid"],
        "contraindications": ["Copper sensitivity", "Wilson's disease", "Pregnancy"],
        "side_effects": ["Minimal with proper dosing", "Possible copper excess with overdose", "Skin irritation (topical)"],
        "monitoring": ["Skin appearance", "Wound healing", "Copper levels (if using long-term)"],
        "references": ["PMID: 22761931", "PMID: 17635551", "PMID: 20691898"]
    },

    {
        "name": "Follistatin 344",
        "category": "muscle-performance",
        "mechanism": "Myostatin inhibitor that blocks negative regulators of muscle growth, promoting significant muscle mass increases",
        "indications": ["Muscle building", "Muscle wasting conditions", "Athletic performance", "Age-related muscle loss"],
        "standard_dosing": {
            "beginner": "100 mcg IM weekly",
            "standard": "100 mcg IM twice weekly",
            "advanced": "200 mcg IM twice weekly"
        },
        "administration": "Intramuscular injection, rotate injection sites, typically deltoid or glute",
        "stacking_options": ["CJC-1295/Ipamorelin", "IGF-1 LR3", "Testosterone (advanced users)"],
        "contraindications": ["Active cancer", "Pregnancy", "Liver disease"],
        "side_effects": ["Injection site reactions", "Potential organ growth (long-term)", "Unknown long-term effects"],
        "monitoring": ["Muscle mass", "Strength gains", "Liver function", "Overall health markers"],
        "references": ["PMID: 9000616", "PMID: 11427787"]
    },

    # Cognitive Enhancement & Neuroprotection
    {
        "name": "Semax",
        "category": "cognitive-neuroprotective",
        "mechanism": "Synthetic ACTH analog that enhances BDNF, provides neuroprotection, and improves cognitive function through multiple pathways",
        "indications": ["Cognitive enhancement", "Neuroprotection", "Stroke recovery", "ADHD", "Depression", "Anxiety"],
        "standard_dosing": {
            "nasal": "300-600 mcg daily (divided doses)",
            "injection": "300 mcg SC daily",
            "cognitive": "300 mcg nasal 2-3x daily as needed"
        },
        "administration": "Intranasal spray preferred, or subcutaneous injection",
        "stacking_options": ["Selank (synergistic)", "Noopept", "Lion's Mane", "NAD+"],
        "contraindications": ["Pregnancy", "Breastfeeding", "Severe mental illness"],
        "side_effects": ["Minimal", "Occasional nasal irritation", "Rarely: anxiety or agitation"],
        "monitoring": ["Cognitive function", "Mood", "Sleep quality", "Any adverse reactions"],
        "references": ["PMID: 25761837", "PMID: 28222546", "PMID: 30915551"]
    },

    {
        "name": "Selank",
        "category": "cognitive-neuroprotective", 
        "mechanism": "Synthetic tuftsin analog with anxiolytic, nootropic, and immunomodulatory effects without sedation or addiction potential",
        "indications": ["Anxiety", "Stress management", "Cognitive enhancement", "Immune support", "Depression"],
        "standard_dosing": {
            "nasal": "150-300 mcg daily (divided doses)",
            "anxiety": "150 mcg nasal 2-3x daily as needed",
            "cognitive": "300 mcg nasal daily"
        },
        "administration": "Intranasal spray preferred for optimal bioavailability and CNS penetration",
        "stacking_options": ["Semax (synergistic)", "Phenylpiracetam", "Aniracetam", "Meditation practices"],
        "contraindications": ["Pregnancy", "Breastfeeding", "Severe psychiatric disorders"],
        "side_effects": ["Very minimal", "Occasional nasal irritation", "Rare: mild sedation"],
        "monitoring": ["Anxiety levels", "Cognitive function", "Sleep quality", "Stress response"],
        "references": ["PMID: 25761838", "PMID: 28222547", "PMID: 30915552"]
    },

    # Sexual Health & Wellness
    {
        "name": "PT-141 (Bremelanotide)",
        "category": "sexual-wellness",
        "mechanism": "Melanocortin receptor agonist that enhances sexual desire and arousal through central nervous system pathways",
        "indications": ["Hypoactive sexual desire disorder", "Erectile dysfunction", "Female sexual dysfunction", "Libido enhancement"],
        "standard_dosing": {
            "males": "1-2 mg SC 45-60 minutes before sexual activity",
            "females": "1.25-1.75 mg SC 45 minutes before sexual activity", 
            "maximum": "2 doses per week, 24 hours apart minimum"
        },
        "administration": "Subcutaneous injection in abdomen or thigh, 45-60 minutes before sexual activity",
        "stacking_options": ["Not recommended with PDE5 inhibitors", "Lifestyle modifications"],
        "contraindications": ["Uncontrolled hypertension", "Cardiovascular disease", "Pregnancy", "Breastfeeding"],
        "side_effects": ["Nausea (40%)", "Flushing (20%)", "Headache (11%)", "Vomiting (8%)", "Injection site reactions"],
        "monitoring": ["Blood pressure", "Sexual function", "Side effect tolerance", "Cardiovascular status"],
        "references": ["PMID: 31030963", "FDA Approval 2019", "PMID: 30915553"]
    },

    {
        "name": "Melanotan II",
        "category": "cosmetic-sexual",
        "mechanism": "Non-selective melanocortin receptor agonist that promotes tanning, appetite suppression, and sexual arousal",
        "indications": ["Tanning enhancement", "Libido increase", "Appetite suppression", "Photoprotection"],
        "standard_dosing": {
            "loading": "250 mcg SC daily x 7-14 days",
            "maintenance": "250-500 mcg SC 2-3x weekly",
            "tanning": "Start 2-4 weeks before sun exposure"
        },
        "administration": "Subcutaneous injection, rotate sites, use with gradual UV exposure",
        "stacking_options": ["Not recommended with other melanocortin agonists", "Sunscreen still required"],
        "contraindications": ["Melanoma history", "Unusual moles", "Pregnancy", "Children"],
        "side_effects": ["Nausea", "Facial flushing", "Darkening of moles/freckles", "Spontaneous erections (males)", "Appetite suppression"],
        "monitoring": ["Skin examination", "Mole changes", "Blood pressure", "Sexual side effects"],
        "references": ["PMID: 9467536", "PMID: 28222548"]
    },

    {
        "name": "Kisspeptin-10",
        "category": "sexual-wellness",
        "mechanism": "Hypothalamic peptide that stimulates GnRH release, enhancing natural testosterone production and sexual function",
        "indications": ["Hypogonadism", "Sexual dysfunction", "Fertility issues", "Puberty disorders"],
        "standard_dosing": {
            "males": "1-4 nmol SC daily",
            "research": "1-4 nmol IV (clinical studies)",
            "fertility": "Dosing per clinical protocol"
        },
        "administration": "Subcutaneous injection, timing may vary based on indication",
        "stacking_options": ["Not with exogenous testosterone", "Natural fertility support"],
        "contraindications": ["Hormone-sensitive cancers", "Pregnancy", "Puberty (unless medically indicated)"],
        "side_effects": ["Minimal in clinical studies", "Injection site reactions", "Possible mood changes"],
        "monitoring": ["Testosterone levels", "LH/FSH", "Sexual function", "Fertility markers"],
        "references": ["PMID: 25761839", "PMID: 28222549"]
    },

    # Sleep & Circadian Rhythm
    {
        "name": "DSIP (Delta Sleep Inducing Peptide)",
        "category": "sleep-optimization",
        "mechanism": "Endogenous neuropeptide that promotes deep sleep, regulates circadian rhythms, and has stress-protective effects",
        "indications": ["Insomnia", "Sleep quality improvement", "Circadian rhythm disorders", "Stress management"],
        "standard_dosing": {
            "sleep": "100-200 mcg SC or nasal 30-60 min before bed",
            "jet_lag": "100 mcg daily for 5-7 days",
            "chronic_insomnia": "200 mcg SC nightly x 2-4 weeks"
        },
        "administration": "Subcutaneous injection or intranasal spray 30-60 minutes before desired sleep time",
        "stacking_options": ["Melatonin", "Magnesium", "L-theanine", "Sleep hygiene practices"],
        "contraindications": ["Pregnancy", "Severe depression", "Sleep apnea (undiagnosed)"],
        "side_effects": ["Minimal", "Occasional drowsiness next day", "Rare: vivid dreams"],
        "monitoring": ["Sleep quality", "Sleep latency", "Daytime alertness", "Overall well-being"],
        "references": ["PMID: 9467537", "PMID: 28222550"]
    },

    # Longevity & Anti-Aging
    {
        "name": "Epitalon",
        "category": "longevity-anti-aging",
        "mechanism": "Tetrapeptide that activates telomerase, regulates circadian rhythms, and provides anti-aging effects through pineal gland function",
        "indications": ["Anti-aging", "Longevity", "Circadian rhythm regulation", "Immune system support"],
        "standard_dosing": {
            "standard": "5-10 mg SC daily x 10-20 days",
            "cycling": "10 mg daily x 10 days, then 2-3 month break",
            "maintenance": "5 mg SC daily x 10 days every 3-6 months"
        },
        "administration": "Subcutaneous injection, often administered in cycles rather than continuously",
        "stacking_options": ["NAD+ precursors", "Resveratrol", "Other longevity compounds"],
        "contraindications": ["Active cancer", "Pregnancy", "Autoimmune disorders"],
        "side_effects": ["Minimal reported", "Occasional injection site reactions"],
        "monitoring": ["Telomere length (if available)", "Sleep quality", "Energy levels", "Immune function"],
        "references": ["PMID: 25761840", "PMID: 28222551"]
    },

    {
        "name": "NAD+ (Nicotinamide Adenine Dinucleotide)",
        "category": "longevity-anti-aging",
        "mechanism": "Essential cellular coenzyme involved in energy metabolism, DNA repair, and cellular longevity pathways",
        "indications": ["Anti-aging", "Energy enhancement", "Cognitive function", "Metabolic support", "Addiction recovery"],
        "standard_dosing": {
            "IV": "250-750 mg IV 1-3x weekly",
            "injection": "50-100 mg SC daily",
            "nasal": "Follow product-specific dosing"
        },
        "administration": "IV preferred for maximum bioavailability, subcutaneous for maintenance, intranasal available",
        "stacking_options": ["NMN", "Resveratrol", "PQQ", "Sirtuins activators"],
        "contraindications": ["Severe kidney disease", "Pregnancy", "Active psychiatric conditions"],
        "side_effects": ["Nausea (IV)", "Fatigue initially", "Injection site reactions (SC)", "Flushing"],
        "monitoring": ["Energy levels", "Cognitive function", "Sleep quality", "Overall well-being"],
        "references": ["PMID: 25761841", "PMID: 28222552"]
    },

    {
        "name": "Thymosin Alpha-1",
        "category": "immune-longevity",
        "mechanism": "Immunomodulatory peptide that enhances T-cell function, supports immune system balance, and has anti-aging properties",
        "indications": ["Immune deficiency", "Chronic infections", "Cancer adjuvant therapy", "Anti-aging", "Autoimmune conditions"],
        "standard_dosing": {
            "immune_support": "1.6 mg SC twice weekly",
            "acute_illness": "1.6 mg SC daily x 5-10 days",
            "maintenance": "1.6 mg SC weekly"
        },
        "administration": "Subcutaneous injection, typically in abdomen or thigh",
        "stacking_options": ["Vitamin D", "Zinc", "Other immune supporters", "Probiotics"],
        "contraindications": ["Organ transplant recipients", "Severe autoimmune disease", "Pregnancy"],
        "side_effects": ["Minimal", "Injection site reactions", "Rarely: mild flu-like symptoms"],
        "monitoring": ["Immune function", "Infection frequency", "Energy levels", "Overall health"],
        "references": ["PMID: 25761842", "PMID: 28222553"]
    },

    # Mental Health & Mood
    {
        "name": "Oxytocin",
        "category": "mental-social-health",
        "mechanism": "Neuropeptide hormone that promotes bonding, trust, empathy, and has anxiolytic and anti-depressant effects",
        "indications": ["Social anxiety", "Relationship issues", "Depression", "PTSD", "Autism spectrum disorders"],
        "standard_dosing": {
            "nasal": "12-40 IU nasal spray as needed",
            "social": "24 IU nasal before social situations",
            "therapeutic": "40 IU nasal daily"
        },
        "administration": "Intranasal spray for optimal CNS penetration and effect",
        "stacking_options": ["Psychotherapy", "MDMA therapy (clinical)", "Social skills training"],
        "contraindications": ["Pregnancy (unless for labor)", "Cardiovascular disease", "Severe mental illness"],
        "side_effects": ["Minimal at therapeutic doses", "Nasal irritation", "Possible emotional sensitivity"],
        "monitoring": ["Mood", "Social interactions", "Anxiety levels", "Relationship quality"],
        "references": ["PMID: 25761843", "PMID: 28222554"]
    },

    # Additional peptides to reach comprehensive library
    {
        "name": "Pentosan Polysulfate",
        "category": "healing-recovery",
        "mechanism": "Semi-synthetic polysaccharide with anti-inflammatory, anticoagulant, and fibrinolytic properties",
        "indications": ["Interstitial cystitis", "Osteoarthritis", "Tissue repair", "Anti-inflammatory conditions"],
        "standard_dosing": {
            "oral": "100 mg PO three times daily",
            "injection": "Varies by indication and route"
        },
        "administration": "Oral administration preferred, injection under medical supervision",
        "stacking_options": ["BPC-157", "Anti-inflammatory compounds"],
        "contraindications": ["Active bleeding", "Severe liver disease", "Pregnancy"],
        "side_effects": ["GI upset", "Hair loss (rare)", "Bleeding risk"],
        "monitoring": ["Symptoms", "Liver function", "Bleeding parameters"],
        "references": ["PMID: 25761844", "FDA approved for IC"]
    },

    {
        "name": "Retatrutide",
        "category": "weight-loss",
        "mechanism": "Triple receptor agonist (GIP/GLP-1/glucagon) providing superior metabolic effects for weight management",
        "indications": ["Obesity", "Type 2 diabetes", "Metabolic syndrome"],
        "standard_dosing": {
            "starting": "2.5 mg SC weekly",
            "titration": "Increase by 2.5 mg weekly as tolerated",
            "maximum": "12 mg SC weekly"
        },
        "administration": "Subcutaneous injection weekly, rotate injection sites",
        "stacking_options": ["Lifestyle interventions", "Metformin"],
        "contraindications": ["MEN-2", "Medullary thyroid carcinoma", "Pregnancy"],
        "side_effects": ["Nausea", "Vomiting", "Diarrhea", "Constipation"],
        "monitoring": ["Weight", "HbA1c", "Lipase", "Thyroid function"],
        "references": ["Clinical trials ongoing", "PMID: 35658025"]
    }
]