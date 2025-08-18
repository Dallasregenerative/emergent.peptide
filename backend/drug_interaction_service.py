"""
Drug Interaction Service for PeptideProtocols.ai
Provides drug interaction checking functionality for practitioners
"""

import json
from typing import List, Dict, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class InteractionSeverity(str, Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CONTRAINDICATED = "contraindicated"

class DrugInteractionService:
    """
    Drug interaction service with built-in database of common drug interactions
    Focuses on peptide therapy interactions and common medications
    """
    
    def __init__(self):
        self.interaction_database = self._initialize_interaction_database()
        self.peptide_interactions = self._initialize_peptide_interactions()
        
    def _initialize_interaction_database(self) -> Dict:
        """Initialize comprehensive drug interaction database"""
        return {
            # Common medication interactions
            "metformin": {
                "interactions": [
                    {
                        "drug": "insulin",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "May increase risk of hypoglycemia. Monitor blood glucose closely.",
                        "mechanism": "Additive glucose-lowering effects",
                        "management": "Monitor blood glucose, adjust doses as needed"
                    },
                    {
                        "drug": "contrast_agents",
                        "severity": InteractionSeverity.MAJOR,
                        "description": "Increased risk of lactic acidosis with iodinated contrast agents.",
                        "mechanism": "Impaired renal function may reduce metformin clearance",
                        "management": "Discontinue metformin 48 hours before contrast procedures"
                    }
                ]
            },
            "warfarin": {
                "interactions": [
                    {
                        "drug": "aspirin",
                        "severity": InteractionSeverity.MAJOR,
                        "description": "Significantly increased bleeding risk.",
                        "mechanism": "Dual anticoagulant and antiplatelet effects",
                        "management": "Avoid combination or use with extreme caution and frequent monitoring"
                    },
                    {
                        "drug": "acetaminophen",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "May increase anticoagulant effect with prolonged use.",
                        "mechanism": "Inhibition of warfarin metabolism",
                        "management": "Monitor INR more frequently with prolonged acetaminophen use"
                    }
                ]
            },
            "lisinopril": {
                "interactions": [
                    {
                        "drug": "potassium_supplements",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Increased risk of hyperkalemia.",
                        "mechanism": "ACE inhibitors reduce potassium excretion",
                        "management": "Monitor serum potassium levels regularly"
                    },
                    {
                        "drug": "lithium",
                        "severity": InteractionSeverity.MAJOR,
                        "description": "Increased lithium levels and toxicity risk.",
                        "mechanism": "Reduced renal lithium clearance",
                        "management": "Monitor lithium levels closely, consider dose reduction"
                    }
                ]
            },
            "simvastatin": {
                "interactions": [
                    {
                        "drug": "gemfibrozil",
                        "severity": InteractionSeverity.CONTRAINDICATED,
                        "description": "Severe rhabdomyolysis risk.",
                        "mechanism": "Inhibition of statin metabolism",
                        "management": "Avoid combination, use alternative statin or fibrate"
                    },
                    {
                        "drug": "amlodipine",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Increased statin exposure and myopathy risk.",
                        "mechanism": "CYP3A4 inhibition",
                        "management": "Limit simvastatin dose to 20mg daily"
                    }
                ]
            },
            "levothyroxine": {
                "interactions": [
                    {
                        "drug": "calcium_carbonate",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Reduced levothyroxine absorption.",
                        "mechanism": "Calcium binding reduces drug availability",
                        "management": "Separate administration by at least 4 hours"
                    },
                    {
                        "drug": "iron_supplements",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Reduced levothyroxine absorption.",
                        "mechanism": "Iron chelation reduces bioavailability",
                        "management": "Separate administration by at least 4 hours"
                    }
                ]
            },
            "sertraline": {
                "interactions": [
                    {
                        "drug": "tramadol",
                        "severity": InteractionSeverity.MAJOR,
                        "description": "Increased risk of serotonin syndrome.",
                        "mechanism": "Excessive serotonergic activity",
                        "management": "Avoid combination or monitor closely for serotonin syndrome symptoms"
                    },
                    {
                        "drug": "nsaids",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Increased bleeding risk.",
                        "mechanism": "Additive effects on platelet function",
                        "management": "Monitor for signs of bleeding, consider gastroprotection"
                    }
                ]
            }
        }
    
    def _initialize_peptide_interactions(self) -> Dict:
        """Initialize peptide-specific drug interactions database"""
        return {
            "semaglutide": {
                "interactions": [
                    {
                        "drug": "insulin",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Increased hypoglycemia risk when used together.",
                        "mechanism": "Additive glucose-lowering effects",
                        "management": "Reduce insulin dose by 10-25%, monitor blood glucose closely"
                    },
                    {
                        "drug": "sulfonylureas",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Enhanced hypoglycemic effect.",
                        "mechanism": "Dual mechanisms of glucose reduction",
                        "management": "Consider sulfonylurea dose reduction, monitor glucose"
                    },
                    {
                        "drug": "oral_medications",
                        "severity": InteractionSeverity.MINOR,
                        "description": "Delayed gastric emptying may affect oral drug absorption.",
                        "mechanism": "GLP-1 receptor agonist slows gastric motility",
                        "management": "Monitor efficacy of time-sensitive oral medications"
                    }
                ]
            },
            "tirzepatide": {
                "interactions": [
                    {
                        "drug": "insulin",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Significant hypoglycemia risk with combination.",
                        "mechanism": "Dual glucose-lowering mechanisms",
                        "management": "Reduce insulin dose by 25-50%, frequent glucose monitoring"
                    },
                    {
                        "drug": "metformin",
                        "severity": InteractionSeverity.MINOR,
                        "description": "Generally safe combination with enhanced glucose control.",
                        "mechanism": "Complementary mechanisms of action",
                        "management": "Standard monitoring, may allow metformin dose optimization"
                    }
                ]
            },
            "bpc_157": {
                "interactions": [
                    {
                        "drug": "anticoagulants",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "May enhance healing and potentially affect bleeding time.",
                        "mechanism": "Enhanced tissue repair may affect coagulation",
                        "management": "Monitor coagulation parameters with concurrent anticoagulant use"
                    },
                    {
                        "drug": "nsaids",
                        "severity": InteractionSeverity.MINOR,
                        "description": "BPC-157 may help mitigate NSAID-induced GI damage.",
                        "mechanism": "Gastroprotective and healing properties",
                        "management": "Potential beneficial interaction, monitor for GI symptoms"
                    }
                ]
            },
            "tb_500": {
                "interactions": [
                    {
                        "drug": "corticosteroids",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Corticosteroids may reduce healing effects of TB-500.",
                        "mechanism": "Opposing effects on tissue repair and inflammation",
                        "management": "Consider timing of administration, monitor healing response"
                    }
                ]
            },
            "cjc_1295": {
                "interactions": [
                    {
                        "drug": "diabetes_medications",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Growth hormone effects may alter glucose metabolism.",
                        "mechanism": "GH can increase insulin resistance",
                        "management": "Monitor blood glucose, may need diabetes medication adjustment"
                    },
                    {
                        "drug": "thyroid_hormones",
                        "severity": InteractionSeverity.MINOR,
                        "description": "Growth hormone may enhance thyroid hormone effects.",
                        "mechanism": "Metabolic enhancement",
                        "management": "Monitor thyroid function tests periodically"
                    }
                ]
            },
            "ipamorelin": {
                "interactions": [
                    {
                        "drug": "cortisol_medications",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "May interact with cortisol regulation.",
                        "mechanism": "Growth hormone effects on HPA axis",
                        "management": "Monitor cortisol levels, assess adrenal function"
                    }
                ]
            },
            "selank": {
                "interactions": [
                    {
                        "drug": "benzodiazepines",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Potential additive anxiolytic effects.",
                        "mechanism": "Both act on GABA system",
                        "management": "Start with lower Selank doses, monitor for excessive sedation"
                    },
                    {
                        "drug": "ssri_antidepressants",
                        "severity": InteractionSeverity.MINOR,
                        "description": "May enhance mood-stabilizing effects.",
                        "mechanism": "Complementary neurotransmitter effects",
                        "management": "Monitor mood and anxiety levels"
                    }
                ]
            },
            "pt_141": {
                "interactions": [
                    {
                        "drug": "antihypertensives",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "PT-141 may cause hypotension, especially with BP medications.",
                        "mechanism": "Melanocortin receptor effects on blood pressure",
                        "management": "Monitor blood pressure closely, consider medication timing"
                    },
                    {
                        "drug": "pde5_inhibitors",
                        "severity": InteractionSeverity.MAJOR,
                        "description": "Increased risk of dangerous hypotension.",
                        "mechanism": "Additive vasodilatory effects",
                        "management": "Avoid concurrent use or use with extreme caution and monitoring"
                    }
                ]
            },
            "sermorelin": {
                "interactions": [
                    {
                        "drug": "growth_hormone",
                        "severity": InteractionSeverity.MODERATE,
                        "description": "Redundant and potentially excessive GH stimulation.",
                        "mechanism": "Dual GH pathway activation",
                        "management": "Avoid concurrent use, choose one approach"
                    }
                ]
            }
        }
    
    def check_drug_interactions(self, medications: List[str], peptides: List[str] = None) -> Dict:
        """
        Check for drug interactions among medications and peptides
        
        Args:
            medications: List of medication names
            peptides: List of peptide names
            
        Returns:
            Dict containing interaction results
        """
        if not medications and not peptides:
            return {
                "interactions": [],
                "total_interactions": 0,
                "highest_severity": None,
                "has_major_interactions": False,
                "summary": "No medications or peptides provided for analysis."
            }
        
        # Normalize medication names
        normalized_meds = [med.lower().strip() for med in medications]
        normalized_peptides = [pep.lower().strip() for pep in (peptides or [])]
        
        all_substances = normalized_meds + normalized_peptides
        interactions = []
        
        # Check medication-medication interactions
        for i, med1 in enumerate(normalized_meds):
            for med2 in normalized_meds[i+1:]:
                interaction = self._find_interaction(med1, med2, "medication")
                if interaction:
                    interactions.append(interaction)
        
        # Check peptide-medication interactions
        for peptide in normalized_peptides:
            for med in normalized_meds:
                interaction = self._find_peptide_medication_interaction(peptide, med)
                if interaction:
                    interactions.append(interaction)
        
        # Check peptide-peptide interactions
        for i, pep1 in enumerate(normalized_peptides):
            for pep2 in normalized_peptides[i+1:]:
                interaction = self._find_peptide_interaction(pep1, pep2)
                if interaction:
                    interactions.append(interaction)
        
        # Sort by severity
        severity_order = {
            InteractionSeverity.CONTRAINDICATED: 4,
            InteractionSeverity.MAJOR: 3,
            InteractionSeverity.MODERATE: 2,
            InteractionSeverity.MINOR: 1
        }
        
        interactions.sort(key=lambda x: severity_order.get(x["severity"], 0), reverse=True)
        
        return {
            "interactions": interactions,
            "total_interactions": len(interactions),
            "highest_severity": interactions[0]["severity"] if interactions else None,
            "has_major_interactions": any(i["severity"] in [InteractionSeverity.MAJOR, InteractionSeverity.CONTRAINDICATED] 
                                        for i in interactions),
            "summary": self._generate_interaction_summary(interactions)
        }
    
    def _find_interaction(self, drug1: str, drug2: str, interaction_type: str) -> Optional[Dict]:
        """Find interaction between two regular medications"""
        # Check if drug1 has interactions with drug2
        if drug1 in self.interaction_database:
            for interaction in self.interaction_database[drug1]["interactions"]:
                if interaction["drug"] == drug2:
                    return {
                        "drug1": drug1,
                        "drug2": drug2,
                        "severity": interaction["severity"],
                        "description": interaction["description"],
                        "mechanism": interaction["mechanism"],
                        "management": interaction["management"],
                        "type": interaction_type
                    }
        
        # Check reverse direction
        if drug2 in self.interaction_database:
            for interaction in self.interaction_database[drug2]["interactions"]:
                if interaction["drug"] == drug1:
                    return {
                        "drug1": drug2,
                        "drug2": drug1,
                        "severity": interaction["severity"],
                        "description": interaction["description"],
                        "mechanism": interaction["mechanism"],
                        "management": interaction["management"],
                        "type": interaction_type
                    }
        
        return None
    
    def _find_peptide_medication_interaction(self, peptide: str, medication: str) -> Optional[Dict]:
        """Find interaction between peptide and medication"""
        if peptide in self.peptide_interactions:
            for interaction in self.peptide_interactions[peptide]["interactions"]:
                if self._medication_matches(interaction["drug"], medication):
                    return {
                        "drug1": peptide,
                        "drug2": medication,
                        "severity": interaction["severity"],
                        "description": interaction["description"],
                        "mechanism": interaction["mechanism"],
                        "management": interaction["management"],
                        "type": "peptide-medication"
                    }
        
        return None
    
    def _find_peptide_interaction(self, peptide1: str, peptide2: str) -> Optional[Dict]:
        """Find interaction between two peptides"""
        # Most peptides don't have direct interactions, but check for specific cases
        growth_hormone_peptides = ["cjc_1295", "ipamorelin", "sermorelin", "ghrp_2", "ghrp_6"]
        
        if peptide1 in growth_hormone_peptides and peptide2 in growth_hormone_peptides:
            if peptide1 != peptide2:
                return {
                    "drug1": peptide1,
                    "drug2": peptide2,
                    "severity": InteractionSeverity.MINOR,
                    "description": "Potential additive growth hormone effects.",
                    "mechanism": "Both peptides stimulate growth hormone release",
                    "management": "Monitor for excessive GH effects, consider using only one at a time",
                    "type": "peptide-peptide"
                }
        
        return None
    
    def _medication_matches(self, interaction_drug: str, medication: str) -> bool:
        """Check if medication matches interaction drug pattern"""
        # Handle medication classes
        medication_classes = {
            "insulin": ["insulin", "humalog", "novolog", "lantus", "levemir"],
            "sulfonylureas": ["glipizide", "glyburide", "glimepiride"],
            "nsaids": ["ibuprofen", "naproxen", "celecoxib", "diclofenac"],
            "anticoagulants": ["warfarin", "heparin", "rivaroxaban", "apixaban"],
            "diabetes_medications": ["metformin", "glipizide", "insulin", "pioglitazone"],
            "antihypertensives": ["lisinopril", "amlodipine", "metoprolol", "losartan"],
            "pde5_inhibitors": ["sildenafil", "tadalafil", "vardenafil"],
            "ssri_antidepressants": ["sertraline", "fluoxetine", "citalopram", "escitalopram"],
            "benzodiazepines": ["lorazepam", "alprazolam", "clonazepam", "diazepam"]
        }
        
        if interaction_drug in medication_classes:
            return medication in medication_classes[interaction_drug]
        
        return interaction_drug == medication
    
    def _generate_interaction_summary(self, interactions: List[Dict]) -> str:
        """Generate a summary of interactions found"""
        if not interactions:
            return "No significant drug interactions found."
        
        major_count = len([i for i in interactions if i["severity"] in [InteractionSeverity.MAJOR, InteractionSeverity.CONTRAINDICATED]])
        moderate_count = len([i for i in interactions if i["severity"] == InteractionSeverity.MODERATE])
        minor_count = len([i for i in interactions if i["severity"] == InteractionSeverity.MINOR])
        
        summary_parts = []
        if major_count > 0:
            summary_parts.append(f"{major_count} major interaction(s)")
        if moderate_count > 0:
            summary_parts.append(f"{moderate_count} moderate interaction(s)")
        if minor_count > 0:
            summary_parts.append(f"{minor_count} minor interaction(s)")
        
        return f"Found {', '.join(summary_parts)}. Review all interactions before prescribing."
    
    def get_peptide_contraindications(self, peptide: str, medical_conditions: List[str]) -> List[Dict]:
        """Get contraindications for specific peptide based on medical conditions"""
        contraindications = []
        peptide = peptide.lower().strip()
        
        # Define condition-based contraindications
        condition_contraindications = {
            "cancer": {
                "peptides": ["bpc_157", "tb_500", "cjc_1295", "ipamorelin", "sermorelin"],
                "reason": "Growth factors may potentially stimulate tumor growth",
                "severity": InteractionSeverity.CONTRAINDICATED
            },
            "pregnancy": {
                "peptides": ["pt_141", "semaglutide", "tirzepatide", "aod_9604"],
                "reason": "Safety not established in pregnancy",
                "severity": InteractionSeverity.CONTRAINDICATED
            },
            "severe_heart_disease": {
                "peptides": ["pt_141", "cjc_1295"],
                "reason": "Cardiovascular effects may worsen heart conditions",
                "severity": InteractionSeverity.MAJOR
            },
            "uncontrolled_diabetes": {
                "peptides": ["cjc_1295", "ipamorelin", "sermorelin"],
                "reason": "Growth hormone effects may worsen glucose control",
                "severity": InteractionSeverity.MODERATE
            }
        }
        
        normalized_conditions = [condition.lower().strip() for condition in medical_conditions]
        
        for condition in normalized_conditions:
            if condition in condition_contraindications:
                contraindication = condition_contraindications[condition]
                if peptide in contraindication["peptides"]:
                    contraindications.append({
                        "condition": condition,
                        "peptide": peptide,
                        "severity": contraindication["severity"], 
                        "reason": contraindication["reason"],
                        "recommendation": "Avoid use or use only under close medical supervision"
                    })
        
        return contraindications

# Global instance
drug_interaction_service = DrugInteractionService()