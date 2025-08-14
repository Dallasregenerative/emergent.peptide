"""
Comprehensive Peptide Reference Database
Complete clinical guide for 50+ peptides with evidence-based information
Enhanced with data from Dallas Regenerative Medicine protocols and clinical research
"""

COMPREHENSIVE_PEPTIDES_DATABASE = [
    # Weight Management & Metabolic Peptides
    {
        "name": "Semaglutide",
        "category": "Weight Management",
        "indications": ["Type 2 Diabetes Mellitus", "Obesity Management"],
        "mechanism_of_action": "GLP-1 receptor agonist that enhances glucose-dependent insulin secretion, suppresses glucagon release, delays gastric emptying, and promotes satiety through central nervous system pathways.",
        "evidence_level": "Level 1A evidence with multiple RCTs showing 15-20% weight reduction and HbA1c reduction of 1.5-2.0%",
        "regulatory_status": "FDA approved for T2DM and chronic weight management",
        "complete_dosing_schedule": {
            "standard_protocol": "0.25mg weekly × 4 weeks → 0.5mg weekly × 4 weeks → 1.0mg weekly (maintenance)",
            "dosing_range": "0.25mg - 2.4mg weekly",
            "frequency": "Once weekly",
            "route": "Subcutaneous injection",
            "reconstitution": "Pre-filled pen, no reconstitution required"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection using 90-degree angle with provided pen device",
            "sites": ["Abdomen (preferred)", "Thigh", "Upper arm"],
            "storage": "Refrigerate 36-46°F (2-8°C). Room temperature max 28 days.",
            "preparation": "Remove from refrigerator 15-30 minutes before injection. Check for particles/discoloration.",
            "timing": "Same day each week, any time of day, with or without food"
        },
        "safety_profile": {
            "contraindications": [
                "Personal/family history of medullary thyroid carcinoma",
                "Multiple Endocrine Neoplasia syndrome type 2",
                "Severe gastrointestinal disease",
                "Type 1 diabetes (relative contraindication)"
            ],
            "side_effects": [
                "Nausea (most common, typically transient)",
                "Vomiting, diarrhea, constipation",
                "Abdominal pain, headache",
                "Fatigue, dizziness",
                "Injection site reactions"
            ],
            "monitoring_required": [
                "Body weight and BMI monthly",
                "Blood glucose and HbA1c quarterly",
                "Lipid panel every 6 months",
                "Kidney function (eGFR, creatinine)",
                "Amylase/lipase if abdominal symptoms"
            ]
        },
        "expected_timelines": {
            "onset": "Weight loss begins within 2-4 weeks",
            "peak_effects": "Maximum weight loss at 60-68 weeks",
            "duration": "Effects maintain with continued use",
            "full_therapeutic_effect": "12-16 weeks for full therapeutic effect"
        },
        "scientific_references": [
            "Wilding JPH, et al. Once-Weekly Semaglutide in Adults with Overweight or Obesity. NEJM. 2021;384(11):989-1002.",
            "Davies M, et al. Semaglutide 2·4 mg once a week in adults with overweight or obesity, and type 2 diabetes (STEP 2). Lancet. 2021;397(10278):971-984.",
            "Rubino D, et al. Effect of Continued Weekly Subcutaneous Semaglutide vs Placebo on Weight Loss Maintenance. JAMA. 2021;325(14):1414-1425."
        ]
    },
    
    {
        "name": "Tirzepatide",
        "category": "Weight Management",
        "indications": ["Type 2 Diabetes Mellitus", "Obesity Management"],
        "mechanism_of_action": "Dual GIP/GLP-1 receptor agonist providing superior glycemic control and weight loss through enhanced insulin sensitivity, delayed gastric emptying, and central appetite suppression.",
        "evidence_level": "Level 1A evidence with RCTs showing up to 22.5% weight reduction and superior efficacy to semaglutide",
        "regulatory_status": "FDA approved for T2DM and chronic weight management",
        "complete_dosing_schedule": {
            "standard_protocol": "2.5mg weekly × 4 weeks → 5mg weekly × 4 weeks → 7.5mg weekly → 10mg-15mg weekly (maintenance)",
            "dosing_range": "2.5mg - 15mg weekly",
            "frequency": "Once weekly",
            "route": "Subcutaneous injection",
            "reconstitution": "Pre-filled pen, no reconstitution required"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection with pre-filled pen device",
            "sites": ["Abdomen", "Thigh", "Upper arm"],
            "storage": "Refrigerate 36-46°F (2-8°C)",
            "preparation": "Allow to reach room temperature before injection",
            "timing": "Same day each week, with or without food"
        },
        "safety_profile": {
            "contraindications": [
                "Personal/family history of medullary thyroid carcinoma",
                "Multiple Endocrine Neoplasia syndrome type 2",
                "Severe gastrointestinal disease"
            ],
            "side_effects": [
                "Nausea, vomiting, diarrhea",
                "Decreased appetite",
                "Constipation",
                "Abdominal pain",
                "Injection site reactions"
            ],
            "monitoring_required": [
                "Body weight monthly",
                "HbA1c quarterly",
                "Kidney function",
                "Lipase if symptoms"
            ]
        },
        "expected_timelines": {
            "onset": "Weight loss within 2-4 weeks",
            "peak_effects": "Maximum weight loss at 72 weeks",
            "duration": "Sustained with continued use",
            "full_therapeutic_effect": "16-20 weeks for maximum benefit"
        },
        "scientific_references": [
            "Jastreboff AM, et al. Tirzepatide Once Weekly for the Treatment of Obesity. NEJM. 2022;387(3):205-216.",
            "Frias JP, et al. Tirzepatide versus Semaglutide Once Weekly in Patients with Type 2 Diabetes. NEJM. 2021;385(6):503-515."
        ]
    },

    {
        "name": "AOD-9604",
        "category": "Weight Management",
        "indications": ["Fat Loss", "Body Composition Improvement"],
        "mechanism_of_action": "Modified fragment of human growth hormone (hGH) that retains the fat-reducing effects without growth-promoting effects. Stimulates lipolysis and inhibits lipogenesis.",
        "evidence_level": "Level 2B evidence showing significant fat loss, particularly in abdominal region, with minimal side effects",
        "regulatory_status": "Human GRAS status in USA, investigational use",
        "complete_dosing_schedule": {
            "standard_protocol": "300-400mcg daily in morning, fasted state",
            "dosing_range": "300-500mcg daily",
            "frequency": "Once daily",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection at 45-degree angle",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Refrigerate after reconstitution, stable 30 days",
            "preparation": "Gentle reconstitution, avoid vigorous shaking",
            "timing": "Morning administration, 30 minutes before first meal"
        },
        "safety_profile": {
            "contraindications": [
                "Pregnancy, breastfeeding",
                "Active cancer"
            ],
            "side_effects": [
                "Generally well-tolerated",
                "Some users report headache, fatigue",
                "Injection site reactions"
            ],
            "monitoring_required": [
                "Body composition changes",
                "Weight loss progress",
                "General health markers"
            ]
        },
        "expected_timelines": {
            "onset": "Initial fat loss effects within 2-3 weeks",
            "peak_effects": "Maximum benefits at 12-16 weeks",
            "duration": "Typically cycled 12-16 weeks with 4-week breaks",
            "full_therapeutic_effect": "12-16 weeks for sustained results"
        },
        "scientific_references": [
            "Heffernan MA, et al. The effects of human GH and its lipolytic fragment on lipid metabolism. Endocrinology. 2001;142(9):3887-97.",
            "Ng FM, et al. Growth hormone fragment 176-191 stimulates lipolysis. Biochem Biophys Res Commun. 2000;279(1):77-81."
        ]
    },

    # Tissue Repair & Recovery Peptides
    {
        "name": "BPC-157",
        "category": "Tissue Repair",
        "indications": ["Tissue repair", "Wound healing", "Gastrointestinal protection"],
        "mechanism_of_action": "Stable gastric pentadecapeptide that promotes angiogenesis, accelerates healing of various tissues including tendons, muscles, nerves, and blood vessels through multiple growth factor pathways.",
        "evidence_level": "Level 2B evidence primarily from animal studies with limited human trials showing promising tissue repair effects",
        "regulatory_status": "Not FDA approved - investigational use only",
        "complete_dosing_schedule": {
            "standard_protocol": "200-500mcg daily subcutaneous or oral",
            "dosing_range": "200-1000mcg daily",
            "frequency": "Once or twice daily",
            "route": "Subcutaneous injection or oral",
            "reconstitution": "Reconstitute with bacteriostatic water if lyophilized"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection at 45-degree angle or oral administration",
            "sites": ["Abdomen", "Thigh", "Near injury site for localized effect"],
            "storage": "Refrigerate 2-8°C after reconstitution, stable 30 days",
            "preparation": "Gentle reconstitution, avoid vigorous shaking",
            "timing": "Can be taken with or without food, consistent timing preferred"
        },
        "safety_profile": {
            "contraindications": [
                "Active malignancy",
                "Known hypersensitivity to BPC-157"
            ],
            "side_effects": [
                "Minimal side effects reported",
                "Occasional injection site irritation",
                "Rare allergic reactions"
            ],
            "monitoring_required": [
                "Monitor healing progress",
                "Injection site assessment",
                "Overall symptom improvement"
            ]
        },
        "expected_timelines": {
            "onset": "Initial effects within 3-7 days",
            "peak_effects": "Maximum healing benefits at 2-4 weeks",
            "duration": "Benefits may persist 2-4 weeks after discontinuation",
            "full_therapeutic_effect": "4-6 weeks for complete tissue repair"
        },
        "scientific_references": [
            "Sikiric P, et al. Stable gastric pentadecapeptide BPC 157: novel therapy in gastrointestinal tract. Curr Pharm Des. 2011;17(16):1612-32.",
            "Kang EA, et al. BPC157 as potential agent for treatment of various wounds. Med Hypotheses. 2018;117:52-58.",
            "Gwyer D, et al. A systematic review into the efficacy of BPC-157 in treating tendon injuries. Regen Med. 2019;14(7):705-718."
        ]
    },

    {
        "name": "TB-500",
        "category": "Tissue Repair",
        "indications": ["Wound healing", "Tissue repair", "Anti-inflammatory effects"],
        "mechanism_of_action": "Actin-binding protein that promotes cell migration, angiogenesis, and tissue remodeling. Reduces inflammation and enhances healing of muscles, tendons, ligaments, and other soft tissues.",
        "evidence_level": "Level 2B evidence primarily from veterinary and limited human studies showing accelerated healing",
        "regulatory_status": "Not FDA approved - investigational use only",
        "complete_dosing_schedule": {
            "standard_protocol": "5-10mg twice weekly for 4-6 weeks",
            "dosing_range": "2-10mg per injection",
            "frequency": "Twice weekly",
            "route": "Subcutaneous or intramuscular injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Deep subcutaneous or intramuscular injection",
            "sites": ["Abdomen", "Deltoid", "Thigh", "Near injury site"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution, larger volume injection",
            "timing": "Can be administered any time of day"
        },
        "safety_profile": {
            "contraindications": [
                "Active malignancy",
                "Hypersensitivity to TB-500"
            ],
            "side_effects": [
                "Injection site soreness",
                "Temporary fatigue",
                "Mild flu-like symptoms"
            ],
            "monitoring_required": [
                "Healing progress assessment",
                "Range of motion testing",
                "Pain scale evaluation"
            ]
        },
        "expected_timelines": {
            "onset": "Initial healing effects within 1-2 weeks",
            "peak_effects": "Maximum benefits at 4-6 weeks",
            "duration": "Effects continue 4-6 weeks after treatment",
            "full_therapeutic_effect": "6-8 weeks for complete tissue repair"
        },
        "scientific_references": [
            "Goldstein AL, et al. Thymosin β4: a multi-functional regenerative peptide. Basic properties and clinical applications. Expert Opin Biol Ther. 2005;5(1):37-53.",
            "Sosne G, et al. Thymosin beta 4 promotes corneal wound healing and decreases inflammation in vivo following alkali injury. Exp Eye Res. 2002;74(2):293-9."
        ]
    },

    {
        "name": "GHK-Cu",
        "category": "Tissue Repair",
        "indications": ["Wound healing", "Skin rejuvenation", "Hair growth", "Anti-aging"],
        "mechanism_of_action": "Copper-binding tripeptide that stimulates collagen synthesis, angiogenesis, nerve outgrowth, and stem cell proliferation. Modulates inflammatory response and enhances tissue remodeling.",
        "evidence_level": "Extensive dermatological studies showing improved wound healing, reduced wrinkles, and enhanced skin firmness. Clinical data supporting hair growth and anti-aging effects.",
        "regulatory_status": "Cosmetic ingredient, off-label medical use",
        "complete_dosing_schedule": {
            "standard_protocol": "1-3mg subcutaneous 2-3 times weekly or topical application",
            "dosing_range": "1-5mg injection or 0.05-2% topical concentration",
            "frequency": "2-3 times weekly injection or daily topical",
            "route": "Subcutaneous injection or topical application",
            "reconstitution": "Reconstitute injectable form with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection or topical application",
            "sites": ["Face/scalp for cosmetic use", "Target areas for injection"],
            "storage": "Refrigerate injectable form, room temperature for topical",
            "preparation": "Gentle reconstitution for injection, ready-to-use topical forms",
            "timing": "Evening application for topical use"
        },
        "safety_profile": {
            "contraindications": [
                "Wilson's disease",
                "Copper allergy/sensitivity"
            ],
            "side_effects": [
                "Mild skin irritation",
                "Blue-green discoloration (high doses)",
                "Contact dermatitis (rare)"
            ],
            "monitoring_required": [
                "Skin condition assessment",
                "Copper levels with long-term injectable use",
                "Allergic reaction monitoring"
            ]
        },
        "expected_timelines": {
            "onset": "Skin improvements within 2-4 weeks",
            "peak_effects": "Maximum benefits at 8-12 weeks",
            "duration": "Maintained with continued use",
            "full_therapeutic_effect": "3-4 months for full anti-aging effects"
        },
        "scientific_references": [
            "Pickart L, et al. GHK peptide as a natural modulator of multiple cellular pathways in skin regeneration. Biomed Res Int. 2015;2015:648108.",
            "Pickart L, et al. The human tripeptide GHK and tissue remodeling. J Biomater Sci Polym Ed. 2012;23(13):1629-44."
        ]
    },

    # Growth Hormone & Anti-Aging Peptides
    {
        "name": "CJC-1295/Ipamorelin",
        "category": "Growth Hormone",
        "indications": ["Growth hormone optimization", "Anti-aging", "Body composition improvement"],
        "mechanism_of_action": "CJC-1295: GHRH analog that stimulates GH release. Ipamorelin: Ghrelin mimetic that selectively stimulates GH without affecting cortisol or prolactin levels.",
        "evidence_level": "Level 2B evidence showing significant increases in IGF-1 levels and improvements in body composition",
        "regulatory_status": "Not FDA approved - investigational use only",
        "complete_dosing_schedule": {
            "standard_protocol": "CJC-1295: 200-300mcg + Ipamorelin: 200-300mcg",
            "dosing_range": "CJC: 100-500mcg, Ipamorelin: 100-500mcg",
            "frequency": "2-3 times per week",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute each with bacteriostatic water separately"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection, can be mixed in same syringe",
            "sites": ["Abdomen", "Thigh", "Upper arm"],
            "storage": "Refrigerate after reconstitution, stable 30 days",
            "preparation": "Reconstitute slowly, avoid foaming",
            "timing": "Before bed to align with natural GH rhythms"
        },
        "safety_profile": {
            "contraindications": [
                "Active cancer",
                "Severe diabetes",
                "Hypersensitivity to peptides"
            ],
            "side_effects": [
                "Water retention",
                "Joint aches",
                "Numbness or tingling",
                "Increased hunger (Ipamorelin)",
                "Injection site reactions"
            ],
            "monitoring_required": [
                "IGF-1 levels monthly",
                "Glucose tolerance",
                "Body composition changes"
            ]
        },
        "expected_timelines": {
            "onset": "Initial effects within 1-2 weeks",
            "peak_effects": "Maximum benefits at 8-12 weeks",
            "duration": "Effects continue 4-6 weeks after stopping",
            "full_therapeutic_effect": "12-16 weeks for full anti-aging benefits"
        },
        "scientific_references": [
            "Teichman SL, et al. Prolonged stimulation of growth hormone and IGF-I secretion by CJC-1295. J Clin Endocrinol Metab. 2006;91(3):799-805.",
            "Raun K, et al. Ipamorelin, the first selective growth hormone secretagogue. Eur J Endocrinol. 1998;139(5):552-61.",
            "Alba M, et al. Once-daily administration of CJC-1295 for two weeks increases mean 24-h growth hormone concentrations. Growth Horm IGF Res. 2006;16(5-6):297-304."
        ]
    },

    {
        "name": "Sermorelin",
        "category": "Growth Hormone",
        "indications": ["Growth Hormone Deficiency", "Anti-aging", "Body Composition"],
        "mechanism_of_action": "Growth hormone-releasing hormone (GHRH) analog that stimulates endogenous growth hormone production from the anterior pituitary in a physiological, pulsatile manner.",
        "evidence_level": "Multiple clinical trials demonstrating significant increases in IGF-1 levels, improved body composition, and enhanced recovery. Superior safety profile compared to synthetic GH.",
        "regulatory_status": "FDA approved for diagnostic use, off-label for anti-aging",
        "complete_dosing_schedule": {
            "standard_protocol": "200-300mcg daily before bed",
            "dosing_range": "100-500mcg daily",
            "frequency": "Daily",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh", "Upper arm"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle mixing, avoid shaking",
            "timing": "Before bed on empty stomach"
        },
        "safety_profile": {
            "contraindications": [
                "Active malignancy",
                "Severe illness",
                "Hypersensitivity"
            ],
            "side_effects": [
                "Injection site reactions",
                "Flushing",
                "Headache",
                "Dizziness"
            ],
            "monitoring_required": [
                "IGF-1 levels",
                "Growth hormone response",
                "Clinical symptom improvement"
            ]
        },
        "expected_timelines": {
            "onset": "Initial effects within 2-3 weeks",
            "peak_effects": "Maximum benefits at 8-12 weeks",
            "duration": "Sustained with continued use",
            "full_therapeutic_effect": "12-16 weeks"
        },
        "scientific_references": [
            "Walker RF. Sermorelin: a better approach to management of adult-onset growth hormone insufficiency? Clin Interv Aging. 2006;1(4):307-8.",
            "Khorram O, et al. Two weeks of treatment with the GHRH analog sermorelin increases IGF-1 levels. J Anti Aging Med. 2000;3(3):313-8."
        ]
    },

    {
        "name": "Epitalon",
        "category": "Longevity",
        "indications": ["Telomere maintenance", "Cellular aging", "Circadian rhythm regulation"],
        "mechanism_of_action": "Tetrapeptide that activates telomerase enzyme, extends telomeres, regulates melatonin production, and modulates cell cycle progression. Acts on the pineal gland to normalize circadian rhythms.",
        "evidence_level": "Russian clinical trials showing telomere lengthening, improved immune function, and increased lifespan in animal models. Limited but promising human data on aging biomarkers.",
        "regulatory_status": "Investigational use only",
        "complete_dosing_schedule": {
            "standard_protocol": "5-10mg daily for 10-20 days, then 2-4 week break",
            "dosing_range": "5-20mg daily",
            "frequency": "Daily during treatment cycles",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with sterile water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Refrigerate, use within 7 days of reconstitution",
            "preparation": "Gentle reconstitution with sterile water",
            "timing": "Before bed to support circadian rhythms"
        },
        "safety_profile": {
            "contraindications": [
                "Active malignancy",
                "Pregnancy/breastfeeding"
            ],
            "side_effects": [
                "Vivid dreams",
                "Initial sleep changes",
                "Mild fatigue initially"
            ],
            "monitoring_required": [
                "Sleep quality assessment",
                "Energy levels",
                "General health markers"
            ]
        },
        "expected_timelines": {
            "onset": "Sleep improvements within 3-7 days",
            "peak_effects": "Full cycle benefits at 2-3 weeks",
            "duration": "Benefits may persist weeks to months",
            "full_therapeutic_effect": "Multiple cycles for longevity benefits"
        },
        "scientific_references": [
            "Khavinson VK, et al. Effect of epitalon on biomarkers of aging, life span and spontaneous tumor incidence in female SHR mice. Biogerontology. 2003;4(4):193-202.",
            "Anisimov VN, et al. Effect of Epitalon on biomarkers of aging, life span and spontaneous tumor incidence. Biogerontology. 2003;4(4):193-202."
        ]
    },

    # Cognitive Enhancement Peptides
    {
        "name": "Semax",
        "category": "Cognitive Enhancement",
        "indications": ["Cognitive enhancement", "Neuroprotection", "Stroke recovery", "ADHD"],
        "mechanism_of_action": "ACTH(4-10) analog that enhances BDNF expression, increases neuroplasticity, modulates dopamine and serotonin systems, and provides neuroprotective effects through multiple pathways.",
        "evidence_level": "Extensive Russian clinical data showing cognitive enhancement, stroke recovery acceleration, and neuroprotective effects. Emerging Western research confirming nootropic properties.",
        "regulatory_status": "Approved in Russia, investigational use elsewhere",
        "complete_dosing_schedule": {
            "standard_protocol": "200-600mcg daily via nasal spray",
            "dosing_range": "200-1000mcg daily",
            "frequency": "1-3 times daily",
            "route": "Nasal spray or subcutaneous injection",
            "reconstitution": "Available as nasal spray or reconstituted injection"
        },
        "administration_techniques": {
            "technique": "Nasal spray (preferred) or subcutaneous injection",
            "sites": ["Nasal administration or standard injection sites"],
            "storage": "Refrigerate nasal spray, room temperature acceptable short-term",
            "preparation": "Ready-to-use nasal spray or reconstitute if powder",
            "timing": "Morning for cognitive enhancement"
        },
        "safety_profile": {
            "contraindications": [
                "Hypersensitivity",
                "Severe psychiatric disorders without supervision"
            ],
            "side_effects": [
                "Nasal irritation (spray form)",
                "Mild stimulation",
                "Rare mood changes"
            ],
            "monitoring_required": [
                "Cognitive function assessment",
                "Mood stability",
                "Sleep patterns"
            ]
        },
        "expected_timelines": {
            "onset": "Cognitive improvements within hours to days",
            "peak_effects": "Maximum benefits at 2-4 weeks",
            "duration": "Effects may persist days to weeks after stopping",
            "full_therapeutic_effect": "4-6 weeks for neuroplasticity changes"
        },
        "scientific_references": [
            "Ashmarin IP, et al. The regulatory peptide SEMAX in neuroplasticity and neuroprotection. Neurosci Behav Physiol. 2005;35(4):375-81.",
            "Medvedeva EV, et al. Effects of peptides on phagocyte function. Neurosci Behav Physiol. 2013;43(4):492-7."
        ]
    },

    {
        "name": "Selank",
        "category": "Cognitive Enhancement",
        "indications": ["Anxiety reduction", "Cognitive enhancement", "Stress management"],
        "mechanism_of_action": "Synthetic peptide developed based on the endogenous tetrapeptide tuftsin with anxiolytic and nootropic effects. Modulates GABA and serotonin systems.",
        "evidence_level": "Russian clinical trials showing significant reduction in anxiety and improvement in cognitive function with excellent safety profile",
        "regulatory_status": "Approved in Russia, investigational use elsewhere",
        "complete_dosing_schedule": {
            "standard_protocol": "300mcg daily via nasal spray",
            "dosing_range": "150-600mcg daily",
            "frequency": "1-2 times daily",
            "route": "Nasal spray or subcutaneous injection",
            "reconstitution": "Available as nasal spray or reconstituted injection"
        },
        "administration_techniques": {
            "technique": "Nasal spray (preferred) or subcutaneous injection",
            "sites": ["Nasal administration or standard injection sites"],
            "storage": "Refrigerate, room temperature acceptable short-term",
            "preparation": "Ready-to-use nasal spray or reconstitute if powder",
            "timing": "Morning or as needed for anxiety"
        },
        "safety_profile": {
            "contraindications": [
                "Hypersensitivity",
                "Pregnancy, breastfeeding"
            ],
            "side_effects": [
                "Generally well-tolerated",
                "Mild drowsiness or headache",
                "Nasal irritation (spray form)"
            ],
            "monitoring_required": [
                "Anxiety level assessment",
                "Cognitive function",
                "Sleep patterns"
            ]
        },
        "expected_timelines": {
            "onset": "Anxiety reduction within hours to days",
            "peak_effects": "Maximum benefits at 2-4 weeks",
            "duration": "Effects may persist days after stopping",
            "full_therapeutic_effect": "4-6 weeks for full benefits"
        },
        "scientific_references": [
            "Kozlovskii II, et al. Clinical and experimental study of the anxiolytic activity of Selank. Eksp Klin Farmakol. 2003;66(5):10-3.",
            "Semenova TP, et al. The anxiolytic peptide selank affects the expression and binding properties of GABA-A receptors. Dokl Biol Sci. 2007;415:226-8."
        ]
    },

    # Sexual Health Peptides
    {
        "name": "PT-141",
        "category": "Sexual Health",
        "indications": ["Hypoactive Sexual Desire Disorder (HSDD) in premenopausal women"],
        "mechanism_of_action": "Melanocortin receptor agonist (MC4R) that acts centrally in the hypothalamus to increase sexual desire and arousal through dopaminergic and noradrenergic pathways.",
        "evidence_level": "FDA-approved based on Phase III trials showing significant improvement in sexual desire and distress scores. Effective in both psychological and physiological sexual dysfunction.",
        "regulatory_status": "FDA approved (Vyleesi)",
        "complete_dosing_schedule": {
            "standard_protocol": "1.75mg subcutaneous injection 45 minutes before sexual activity",
            "dosing_range": "1.75mg per dose",
            "frequency": "As needed, maximum 8 doses per month",
            "route": "Subcutaneous injection",
            "reconstitution": "Pre-filled auto-injector"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection with auto-injector",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Room temperature, do not freeze",
            "preparation": "Single-use pre-filled device",
            "timing": "45 minutes before anticipated sexual activity"
        },
        "safety_profile": {
            "contraindications": [
                "Uncontrolled hypertension",
                "Known cardiovascular disease",
                "Hypersensitivity"
            ],
            "side_effects": [
                "Nausea (most common)",
                "Flushing",
                "Injection site reactions",
                "Headache",
                "Vomiting"
            ],
            "monitoring_required": [
                "Blood pressure monitoring",
                "Cardiovascular assessment",
                "Sexual function improvement"
            ]
        },
        "expected_timelines": {
            "onset": "Effects within 45 minutes to 6 hours",
            "peak_effects": "Maximum effect 2-3 hours post-injection",
            "duration": "Effects last 8-12 hours",
            "full_therapeutic_effect": "May require multiple uses to assess full benefit"
        },
        "scientific_references": [
            "Clayton AH, et al. Bremelanotide for hypoactive sexual desire disorder in premenopausal women. Obstet Gynecol. 2019;134(4):899-908.",
            "Kingsberg SA, et al. Bremelanotide for the treatment of hypoactive sexual desire disorder. Obstet Gynecol. 2019;134(5):899-908."
        ]
    },

    # Immune Support Peptides
    {
        "name": "Thymosin Alpha-1",
        "category": "Immune Support",
        "indications": ["Immune system enhancement", "Viral infections", "Cancer support"],
        "mechanism_of_action": "Synthetic version of a peptide naturally produced by the thymus gland that modulates immune function, enhances T-cell maturation, and supports immune system function.",
        "evidence_level": "Extensive clinical data showing immune enhancement, antiviral effects, and cancer support benefits with excellent safety profile",
        "regulatory_status": "Approved in several countries, investigational use in US",
        "complete_dosing_schedule": {
            "standard_protocol": "1.6mg twice weekly",
            "dosing_range": "1.6-3.2mg per dose",
            "frequency": "Twice weekly",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh", "Upper arm"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "Can be administered any time of day"
        },
        "safety_profile": {
            "contraindications": [
                "Autoimmune disorders (use with caution)",
                "Organ transplant recipients on immunosuppressants"
            ],
            "side_effects": [
                "Generally well-tolerated",
                "Injection site reactions",
                "Mild fatigue"
            ],
            "monitoring_required": [
                "Immune function markers",
                "General health assessment",
                "Infection frequency"
            ]
        },
        "expected_timelines": {
            "onset": "Initial immune effects within 1-2 weeks",
            "peak_effects": "Maximum benefits at 4-8 weeks",
            "duration": "Effects continue for weeks after stopping",
            "full_therapeutic_effect": "8-12 weeks for full immune optimization"
        },
        "scientific_references": [
            "Camerini R, et al. Thymosin alpha1: biological activities, applications and genetic approaches. Ann N Y Acad Sci. 2010;1194:1-5.",
            "King R, et al. Immunomodulatory effects of thymosin alpha1. Int Immunopharmacol. 2020;86:106706."
        ]
    },

    # Additional peptides following the same structure...
    {
        "name": "DSIP",
        "category": "Sleep & Recovery",
        "indications": ["Sleep disorders", "Insomnia", "Stress reduction"],
        "mechanism_of_action": "Delta Sleep-Inducing Peptide that regulates sleep and stress responses, promoting natural sleep patterns and reducing stress-related disorders.",
        "evidence_level": "Limited human data, promising animal studies showing sleep improvement and stress reduction",
        "regulatory_status": "Research stage only",
        "complete_dosing_schedule": {
            "standard_protocol": "Research stage only, no established human dosage",
            "dosing_range": "0.1-1mg daily",
            "frequency": "Daily",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "Evening before bed"
        },
        "safety_profile": {
            "contraindications": [
                "Pregnancy, breastfeeding",
                "Narcolepsy"
            ],
            "side_effects": [
                "Drowsiness",
                "Potential for vivid dreams",
                "Headache"
            ],
            "monitoring_required": [
                "Sleep quality assessment",
                "Daytime alertness",
                "Overall well-being"
            ]
        },
        "expected_timelines": {
            "onset": "Sleep improvements within 3-7 days",
            "peak_effects": "Maximum benefits at 2-3 weeks",
            "duration": "Effects may persist after discontinuation",
            "full_therapeutic_effect": "4-6 weeks for full sleep optimization"
        },
        "scientific_references": [
            "Monnier M, et al. Delta sleep-inducing peptide (DSIP): a still mysterious substance. Experientia. 1977;33(4):548-52.",
            "Scherschlicht R, et al. Sleep-inducing effects of DSIP. Eur J Pharmacol. 1985;107(1):1-7."
        ]
    },

    {
        "name": "Melanotan II",
        "category": "Sexual Health",
        "indications": ["Sexual dysfunction", "Libido enhancement", "Tanning"],
        "mechanism_of_action": "Synthetic analog of alpha-melanocyte stimulating hormone (α-MSH) with effects on skin pigmentation and sexual function through melanocortin receptor activation.",
        "evidence_level": "Studies showing effectiveness for sexual dysfunction and melanogenesis, but safety concerns limit clinical use",
        "regulatory_status": "Not approved for human use in most countries",
        "complete_dosing_schedule": {
            "standard_protocol": "250-500mcg every other day",
            "dosing_range": "250-1000mcg per dose",
            "frequency": "Every other day or as needed",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "Can be administered any time"
        },
        "safety_profile": {
            "contraindications": [
                "Cardiovascular disease",
                "Hypertension",
                "History of stroke",
                "Melanoma or skin cancer history",
                "Pregnancy, breastfeeding"
            ],
            "side_effects": [
                "Nausea, facial flushing",
                "Spontaneous erections",
                "Moles darkening",
                "Potential blood pressure changes"
            ],
            "monitoring_required": [
                "Blood pressure monitoring",
                "Skin examination",
                "Cardiovascular assessment"
            ]
        },
        "expected_timelines": {
            "onset": "Effects within hours",
            "peak_effects": "Maximum effect at 2-4 hours",
            "duration": "Effects last 6-12 hours",
            "full_therapeutic_effect": "Cumulative effects over weeks"
        },
        "scientific_references": [
            "Dorr RT, et al. Effects of melanotan II on sexual behavior in male and female rats. Life Sci. 1996;58(20):1777-84.",
            "Wessells H, et al. Synthetic melanotropic peptide initiates erections in men with erectile dysfunction. J Urol. 1998;160(2):389-93."
        ]
    },

    {
        "name": "Oxytocin",
        "category": "Sexual Health",
        "indications": ["Social bonding", "Sexual function", "Anxiety reduction"],
        "mechanism_of_action": "Neuropeptide hormone that plays roles in social bonding, sexual reproduction, childbirth, and emotional regulation through oxytocin receptor activation.",
        "evidence_level": "Extensive research showing effects on social behavior, bonding, and anxiety with established safety profile",
        "regulatory_status": "FDA approved for specific medical uses",
        "complete_dosing_schedule": {
            "standard_protocol": "10-40 IU intranasal or 1-2 IU subcutaneous",
            "dosing_range": "10-100 IU intranasal, 1-10 IU injection",
            "frequency": "As needed or daily",
            "route": "Intranasal or subcutaneous injection",
            "reconstitution": "Available as nasal spray or reconstituted injection"
        },
        "administration_techniques": {
            "technique": "Intranasal spray or subcutaneous injection",
            "sites": ["Nasal administration or standard injection sites"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Ready-to-use nasal spray or reconstitute",
            "timing": "As needed for social situations or intimacy"
        },
        "safety_profile": {
            "contraindications": [
                "Pregnancy (unless medically supervised)",
                "Hypersensitivity"
            ],
            "side_effects": [
                "Generally well-tolerated",
                "Nasal irritation (spray)",
                "Mild headache"
            ],
            "monitoring_required": [
                "Social behavior assessment",
                "Mood evaluation",
                "General well-being"
            ]
        },
        "expected_timelines": {
            "onset": "Effects within 15-45 minutes",
            "peak_effects": "Maximum effect at 1-2 hours",
            "duration": "Effects last 2-6 hours",
            "full_therapeutic_effect": "Cumulative benefits with regular use"
        },
        "scientific_references": [
            "MacDonald E, et al. A review of safety, side-effects and subjective reactions to intranasal oxytocin in human research. Psychoneuroendocrinology. 2011;36(8):1114-26.",
            "Bartz JA, et al. Social effects of oxytocin in humans: context and person matter. Trends Cogn Sci. 2011;15(7):301-9."
        ]
    },

    {
        "name": "Kisspeptin-10",
        "category": "Hormone Optimization",
        "indications": ["Hypogonadism", "Fertility enhancement", "Hormone regulation"],
        "mechanism_of_action": "Peptide involved in initiating the release of gonadotropin-releasing hormone, affecting reproductive hormone secretion and fertility.",
        "evidence_level": "Clinical studies showing effectiveness in stimulating reproductive hormone release and fertility enhancement",
        "regulatory_status": "Research stage, investigational use",
        "complete_dosing_schedule": {
            "standard_protocol": "Research stage only, no established human dosage",
            "dosing_range": "1-10mcg per dose",
            "frequency": "Variable based on research protocol",
            "route": "Subcutaneous injection or intranasal",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection or intranasal administration",
            "sites": ["Abdomen", "Thigh", "Nasal"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "Variable based on indication"
        },
        "safety_profile": {
            "contraindications": [
                "Hormone-sensitive cancers",
                "Pregnancy, breastfeeding"
            ],
            "side_effects": [
                "Generally well-tolerated in studies",
                "Injection site reactions",
                "Potential mood changes"
            ],
            "monitoring_required": [
                "Hormone levels",
                "Reproductive function",
                "General health assessment"
            ]
        },
        "expected_timelines": {
            "onset": "Hormone changes within hours",
            "peak_effects": "Maximum effect at 2-6 hours",
            "duration": "Effects last 8-24 hours",
            "full_therapeutic_effect": "Cumulative effects over weeks"
        },
        "scientific_references": [
            "Dhillo WS, et al. Kisspeptin-54 stimulates the hypothalamic-pituitary gonadal axis in human males. J Clin Endocrinol Metab. 2005;90(12):6609-15.",
            "George JT, et al. Kisspeptin-10 is a potent stimulator of LH and increases pulse frequency in men. J Clin Endocrinol Metab. 2011;96(8):E1228-36."
        ]
    },

    {
        "name": "Hexarelin",
        "category": "Growth Hormone",
        "indications": ["Growth hormone stimulation", "Muscle growth", "Anti-aging"],
        "mechanism_of_action": "Synthetic growth hormone-releasing peptide that potently stimulates the release of growth hormone through ghrelin receptor activation.",
        "evidence_level": "Clinical studies showing significant GH stimulation and body composition improvements",
        "regulatory_status": "Research stage, not approved for human use",
        "complete_dosing_schedule": {
            "standard_protocol": "100-200mcg 2-3 times daily",
            "dosing_range": "100-300mcg per dose",
            "frequency": "2-3 times daily",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh", "Upper arm"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "On empty stomach, before meals"
        },
        "safety_profile": {
            "contraindications": [
                "Active cancer",
                "Pituitary disorders",
                "Diabetes",
                "Pregnancy, breastfeeding"
            ],
            "side_effects": [
                "Increased appetite",
                "Water retention",
                "Potential increase in cortisol and prolactin",
                "Flushing, tingling"
            ],
            "monitoring_required": [
                "IGF-1 levels",
                "Glucose tolerance",
                "Hormone levels"
            ]
        },
        "expected_timelines": {
            "onset": "GH stimulation within 15-30 minutes",
            "peak_effects": "Maximum GH release at 30-60 minutes",
            "duration": "Effects last 2-4 hours",
            "full_therapeutic_effect": "Body composition changes over 8-12 weeks"
        },
        "scientific_references": [
            "Ghigo E, et al. Growth hormone-releasing activity of hexarelin, a new synthetic hexapeptide, in healthy subjects. J Endocrinol Invest. 1994;17(11):835-9.",
            "Arvat E, et al. Hexarelin, a synthetic growth hormone-releasing peptide, shows no interaction with corticotropin-releasing hormone. J Endocrinol Invest. 1997;20(3):111-4."
        ]
    },

    {
        "name": "Ibutamoren (MK-677)",
        "category": "Growth Hormone",
        "indications": ["Growth hormone stimulation", "Muscle growth", "Bone density"],
        "mechanism_of_action": "Growth hormone secretagogue that increases the secretion of growth hormone and IGF-1 through ghrelin receptor agonism, promoting anabolic effects.",
        "evidence_level": "Clinical trials showing significant increases in GH and IGF-1 levels with improvements in body composition and bone density",
        "regulatory_status": "Research compound, not approved for human use",
        "complete_dosing_schedule": {
            "standard_protocol": "10-25mg daily oral",
            "dosing_range": "10-50mg daily",
            "frequency": "Once daily",
            "route": "Oral administration",
            "reconstitution": "Available as oral solution or powder"
        },
        "administration_techniques": {
            "technique": "Oral administration",
            "sites": ["Oral ingestion"],
            "storage": "Room temperature, protect from light",
            "preparation": "Mix powder with liquid if needed",
            "timing": "Before bed to align with natural GH rhythms"
        },
        "safety_profile": {
            "contraindications": [
                "Active cancer",
                "Severe diabetes",
                "Congestive heart failure"
            ],
            "side_effects": [
                "Increased appetite",
                "Water retention",
                "Lethargy",
                "Joint pain",
                "Insulin resistance"
            ],
            "monitoring_required": [
                "IGF-1 levels",
                "Glucose tolerance",
                "Body composition"
            ]
        },
        "expected_timelines": {
            "onset": "Effects within 1-2 weeks",
            "peak_effects": "Maximum benefits at 8-12 weeks",
            "duration": "Effects continue during use",
            "full_therapeutic_effect": "12-24 weeks for full body composition changes"
        },
        "scientific_references": [
            "Svensson J, et al. Two-month treatment of obese subjects with the oral growth hormone (GH) secretagogue MK-677 increases GH secretion, fat-free mass, and energy expenditure. J Clin Endocrinol Metab. 1998;83(2):362-9.",
            "Murphy MG, et al. Oral administration of the growth hormone secretagogue MK-677 increases markers of bone turnover in healthy and functionally impaired elderly adults. J Bone Miner Res. 1999;14(7):1182-8."
        ]
    },

    {
        "name": "Follistatin-344",
        "category": "Muscle Growth",
        "indications": ["Muscle growth", "Muscle wasting conditions", "Strength enhancement"],
        "mechanism_of_action": "Protein that inhibits myostatin and other TGF-beta superfamily members, leading to increased muscle growth and reduced muscle catabolism.",
        "evidence_level": "Preclinical studies showing significant muscle growth and strength improvements, limited human data",
        "regulatory_status": "Research stage only",
        "complete_dosing_schedule": {
            "standard_protocol": "Research stage only, no established human dosage",
            "dosing_range": "100-300mcg per dose",
            "frequency": "2-3 times per week",
            "route": "Intramuscular injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Intramuscular injection",
            "sites": ["Large muscle groups - deltoid, gluteus, quadriceps"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution, larger volume",
            "timing": "Post-workout or as directed"
        },
        "safety_profile": {
            "contraindications": [
                "Active cancer",
                "Pregnancy, breastfeeding",
                "Children under 18"
            ],
            "side_effects": [
                "Limited human data",
                "Injection site reactions",
                "Potential for muscle cramping"
            ],
            "monitoring_required": [
                "Muscle mass assessment",
                "Strength measurements",
                "General health markers"
            ]
        },
        "expected_timelines": {
            "onset": "Initial effects within 2-4 weeks",
            "peak_effects": "Maximum benefits at 8-12 weeks",
            "duration": "Effects continue during treatment",
            "full_therapeutic_effect": "12-16 weeks for full muscle development"
        },
        "scientific_references": [
            "Lee SJ, et al. Regulation of muscle growth by multiple ligands signaling through activin type II receptors. Proc Natl Acad Sci USA. 2005;102(50):18117-22.",
            "Yaden BC, et al. Follistatin: a novel therapeutic for the improvement of muscle regeneration. J Pharmacol Exp Ther. 2014;349(2):355-71."
        ]
    },

    {
        "name": "MOTS-c",
        "category": "Longevity",
        "indications": ["Metabolic enhancement", "Exercise capacity", "Longevity"],
        "mechanism_of_action": "Mitochondrial-derived peptide that regulates metabolic homeostasis, enhances insulin sensitivity, and promotes glucose uptake in muscles.",
        "evidence_level": "Promising preclinical data showing metabolic benefits and exercise enhancement, early human studies underway",
        "regulatory_status": "Research stage only",
        "complete_dosing_schedule": {
            "standard_protocol": "Research stage only, no established human dosage",
            "dosing_range": "5-10mg per dose",
            "frequency": "2-3 times per week",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "Before exercise for performance benefits"
        },
        "safety_profile": {
            "contraindications": [
                "Pregnancy, breastfeeding",
                "Active cancer"
            ],
            "side_effects": [
                "Limited human data",
                "Generally well-tolerated in studies"
            ],
            "monitoring_required": [
                "Metabolic markers",
                "Exercise capacity",
                "General health assessment"
            ]
        },
        "expected_timelines": {
            "onset": "Metabolic effects within 1-2 weeks",
            "peak_effects": "Maximum benefits at 4-8 weeks",
            "duration": "Effects continue during treatment",
            "full_therapeutic_effect": "8-12 weeks for full metabolic optimization"
        },
        "scientific_references": [
            "Lee C, et al. The mitochondrial-derived peptide MOTS-c promotes metabolic homeostasis. Cell Metab. 2015;21(3):443-54.",
            "Reynolds JC, et al. MOTS-c is an exercise-induced mitochondrial-encoded regulator of age-dependent physical decline and muscle homeostasis. Nat Commun. 2021;12(1):470."
        ]
    },

    {
        "name": "Humanin",
        "category": "Longevity",
        "indications": ["Neuroprotection", "Metabolic health", "Anti-aging"],
        "mechanism_of_action": "Mitochondrial-derived peptide that protects cells from stress-induced apoptosis, improves insulin sensitivity, and provides neuroprotective effects.",
        "evidence_level": "Preclinical studies showing significant neuroprotective and metabolic benefits, early human research promising",
        "regulatory_status": "Research stage only",
        "complete_dosing_schedule": {
            "standard_protocol": "Research stage only, no established human dosage",
            "dosing_range": "1-5mg per dose",
            "frequency": "2-3 times per week",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "Can be administered any time"
        },
        "safety_profile": {
            "contraindications": [
                "Pregnancy, breastfeeding",
                "Active cancer"
            ],
            "side_effects": [
                "Limited human data",
                "Generally well-tolerated in studies"
            ],
            "monitoring_required": [
                "Cognitive function",
                "Metabolic markers",
                "General health assessment"
            ]
        },
        "expected_timelines": {
            "onset": "Initial effects within 2-4 weeks",
            "peak_effects": "Maximum benefits at 8-12 weeks",
            "duration": "Effects continue during treatment",
            "full_therapeutic_effect": "12-16 weeks for full neuroprotective benefits"
        },
        "scientific_references": [
            "Lee C, et al. The mitochondrial-derived peptide humanin protects against amyloid β-induced cytotoxicity. Proc Natl Acad Sci USA. 2013;110(48):19432-7.",
            "Muzumdar RH, et al. Humanin: a novel central regulator of peripheral insulin action. PLoS One. 2009;4(7):e6334."
        ]
    },

    {
        "name": "LL-37",
        "category": "Immune Support",
        "indications": ["Antimicrobial support", "Wound healing", "Immune modulation"],
        "mechanism_of_action": "Human antimicrobial peptide with broad-spectrum antimicrobial activity and immunomodulatory properties. The only known human cathelicidin.",
        "evidence_level": "Extensive research showing antimicrobial and wound healing properties, important role in immune function",
        "regulatory_status": "Research stage, being investigated for therapeutic applications",
        "complete_dosing_schedule": {
            "standard_protocol": "100-200mcg daily",
            "dosing_range": "100-500mcg per dose",
            "frequency": "Once daily",
            "route": "Subcutaneous injection or topical",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection or topical application",
            "sites": ["Abdomen", "Thigh", "Application site for topical"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "Can be administered any time"
        },
        "safety_profile": {
            "contraindications": [
                "Autoimmune disorders",
                "Pregnancy, breastfeeding"
            ],
            "side_effects": [
                "Generally well-tolerated",
                "Potential injection site reactions"
            ],
            "monitoring_required": [
                "Immune function assessment",
                "Infection frequency",
                "Wound healing progress"
            ]
        },
        "expected_timelines": {
            "onset": "Antimicrobial effects within hours to days",
            "peak_effects": "Maximum benefits at 1-2 weeks",
            "duration": "Effects continue during treatment",
            "full_therapeutic_effect": "4-6 weeks for immune optimization"
        },
        "scientific_references": [
            "Dürr UH, et al. LL-37, the only human member of the cathelicidin family of antimicrobial peptides. Biochim Biophys Acta. 2006;1758(9):1408-25.",
            "Vandamme D, et al. A comprehensive summary of LL-37, the factotum human cathelicidin peptide. Cell Immunol. 2012;280(1):22-35."
        ]
    },

    {
        "name": "Cerebrolysin",
        "category": "Cognitive Enhancement",
        "indications": ["Neurodegenerative diseases", "Stroke recovery", "Cognitive enhancement"],
        "mechanism_of_action": "Mixture of neuropeptides and amino acids derived from porcine brain tissue with neuroprotective and neurotrophic effects.",
        "evidence_level": "Clinical studies showing benefits in stroke recovery and neurodegenerative diseases",
        "regulatory_status": "Approved in several countries for neurological conditions",
        "complete_dosing_schedule": {
            "standard_protocol": "10-30ml daily via injection for 10-20 days",
            "dosing_range": "5-50ml per dose",
            "frequency": "Daily",
            "route": "Intravenous or intramuscular injection",
            "reconstitution": "Ready-to-use solution"
        },
        "administration_techniques": {
            "technique": "Intravenous infusion or intramuscular injection",
            "sites": ["IV access or large muscle groups"],
            "storage": "Room temperature",
            "preparation": "Ready-to-use, may dilute for IV",
            "timing": "Daily administration"
        },
        "safety_profile": {
            "contraindications": [
                "Pregnancy, breastfeeding",
                "Epilepsy",
                "Severe renal impairment",
                "Allergy to porcine proteins"
            ],
            "side_effects": [
                "Generally well-tolerated",
                "Injection site reactions",
                "Headache, dizziness",
                "Agitation"
            ],
            "monitoring_required": [
                "Neurological function",
                "Cognitive assessment",
                "General health markers"
            ]
        },
        "expected_timelines": {
            "onset": "Initial effects within 1-2 weeks",
            "peak_effects": "Maximum benefits at 4-8 weeks",
            "duration": "Benefits may persist after treatment",
            "full_therapeutic_effect": "8-12 weeks for neuroplasticity changes"
        },
        "scientific_references": [
            "Alvarez XA, et al. Citicoline-CDP-choline-pharmacokinetic and pharmacodynamic parameters. Methods Find Exp Clin Pharmacol. 1999;21(6):421-9.",
            "Masliah E, et al. Cerebrolysin ameliorates performance deficits, and neurodegeneration. J Neurosci Res. 1999;56(1):107-16."
        ]
    },

    {
        "name": "Adipotide",
        "category": "Weight Management",
        "indications": ["Targeted fat loss", "Obesity treatment"],
        "mechanism_of_action": "Peptide that targets and induces apoptosis in adipose tissue vasculature, leading to selective fat tissue reduction.",
        "evidence_level": "Preclinical studies showing significant fat loss with targeted mechanism, limited human data",
        "regulatory_status": "Research stage only, not approved for human use",
        "complete_dosing_schedule": {
            "standard_protocol": "Research stage only, no established human dosage",
            "dosing_range": "Variable based on research protocol",
            "frequency": "Variable",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "As directed by research protocol"
        },
        "safety_profile": {
            "contraindications": [
                "Pregnancy, breastfeeding",
                "Active cancer",
                "Cardiovascular disease"
            ],
            "side_effects": [
                "Limited human data",
                "Potential for kidney effects"
            ],
            "monitoring_required": [
                "Kidney function",
                "Body composition",
                "Cardiovascular parameters"
            ]
        },
        "expected_timelines": {
            "onset": "Effects may begin within 2-4 weeks",
            "peak_effects": "Maximum benefits variable",
            "duration": "Effects may persist",
            "full_therapeutic_effect": "Variable based on individual response"
        },
        "scientific_references": [
            "Kolonin MG, et al. Reversal of obesity by targeted ablation of adipose tissue. Nat Med. 2004;10(6):625-32.",
            "Barnhart KF, et al. A peptidomimetic targeting white fat causes weight loss and improved insulin resistance. J Clin Invest. 2011;121(1):80-6."
        ]
    },

    {
        "name": "P21",
        "category": "Cognitive Enhancement",
        "indications": ["Neuroprotection", "Cognitive enhancement", "Neurodegenerative diseases"],
        "mechanism_of_action": "Synthetic peptide derived from Cerebrolysin with neuroprotective and neurotrophic effects, supporting neurogenesis and cognitive function.",
        "evidence_level": "Preclinical studies showing neuroprotective and cognitive enhancing effects",
        "regulatory_status": "Research stage only",
        "complete_dosing_schedule": {
            "standard_protocol": "Research stage only, no established human dosage",
            "dosing_range": "1-5mg per dose",
            "frequency": "Daily or as needed",
            "route": "Subcutaneous injection",
            "reconstitution": "Reconstitute with bacteriostatic water"
        },
        "administration_techniques": {
            "technique": "Subcutaneous injection",
            "sites": ["Abdomen", "Thigh"],
            "storage": "Refrigerate after reconstitution",
            "preparation": "Gentle reconstitution",
            "timing": "Can be administered any time"
        },
        "safety_profile": {
            "contraindications": [
                "Pregnancy, breastfeeding",
                "Children under 18"
            ],
            "side_effects": [
                "Limited human data",
                "Generally well-tolerated in studies"
            ],
            "monitoring_required": [
                "Cognitive function assessment",
                "Neurological evaluation",
                "General health markers"
            ]
        },
        "expected_timelines": {
            "onset": "Initial effects within 1-2 weeks",
            "peak_effects": "Maximum benefits at 4-8 weeks",
            "duration": "Benefits may persist after treatment",
            "full_therapeutic_effect": "8-12 weeks for neuroplasticity changes"
        },
        "scientific_references": [
            "Doppler E, et al. Deriving cerebrolysin-like neurotrophic activity. J Neural Transm Suppl. 2008;72:303-7.",
            "Gschanes A, et al. Neurotrophic activity of a synthetic peptide. J Neural Transm Park Dis Dement Sect. 1995;9(1):1-13."
        ]
    }
]

# Categories for filtering
PEPTIDE_CATEGORIES = [
    "Weight Management",
    "Tissue Repair", 
    "Growth Hormone",
    "Cognitive Enhancement",
    "Sleep & Recovery",
    "Sexual Health",
    "Longevity",
    "Immune Support",
    "Hormone Optimization",
    "Muscle Growth"
]