"""
Adaptive Assessment Engine
AI-powered conditional branching logic for personalized intake
Based on patient demographics, conditions, and risk factors
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ConditionalBranch:
    """Represents a conditional branch in the assessment flow"""
    condition: str
    field_name: str
    question_type: str  # 'select', 'input', 'multiselect', 'yes_no'
    question_text: str
    options: List[str] = None
    validation_rules: Dict[str, Any] = None
    required: bool = True
    dependency_fields: List[str] = None

class AdaptiveAssessmentEngine:
    """
    Advanced assessment engine with conditional branching logic
    Personalizes intake flow based on patient characteristics
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conditional_branches = self._initialize_conditional_branches()
        self.risk_flag_rules = self._initialize_risk_flag_rules()
        self.lab_interpretation_rules = self._initialize_lab_rules()
    
    def _initialize_conditional_branches(self) -> Dict[str, List[ConditionalBranch]]:
        """Initialize conditional branching logic based on patient characteristics"""
        
        return {
            "gender_specific": [
                # Female-specific questions
                ConditionalBranch(
                    condition="gender == 'female' and age >= 12 and age <= 55",
                    field_name="pregnancy_status",
                    question_type="select",
                    question_text="Are you currently pregnant, trying to conceive, or breastfeeding?",
                    options=["Not pregnant/not breastfeeding", "Pregnant", "Trying to conceive", "Breastfeeding", "Not sure"],
                    required=True
                ),
                ConditionalBranch(
                    condition="gender == 'female' and age >= 35",
                    field_name="menopause_status",
                    question_type="select",
                    question_text="What is your current menopause status?",
                    options=["Premenopausal", "Perimenopausal", "Postmenopausal", "Surgical menopause"],
                    required=True
                ),
                ConditionalBranch(
                    condition="gender == 'female' and 'hormonal imbalance' in primary_concerns",
                    field_name="hormone_symptoms",
                    question_type="multiselect",
                    question_text="Which hormone-related symptoms are you experiencing?",
                    options=["Hot flashes", "Night sweats", "Mood swings", "Low libido", "Irregular periods", "Fatigue", "Weight gain"],
                    required=True
                ),
                # Male-specific questions
                ConditionalBranch(
                    condition="gender == 'male' and age >= 40",
                    field_name="testosterone_symptoms",
                    question_type="multiselect",
                    question_text="Are you experiencing any of these symptoms that might indicate low testosterone?",
                    options=["Low energy", "Decreased libido", "Muscle loss", "Weight gain", "Mood changes", "Sleep issues", "Erectile dysfunction"],
                    required=False
                )
            ],
            
            "age_specific": [
                # Pediatric considerations (unlikely but comprehensive)
                ConditionalBranch(
                    condition="age < 18",
                    field_name="guardian_consent",
                    question_type="yes_no",
                    question_text="Do you have guardian consent for this assessment?",
                    required=True
                ),
                # Elderly considerations
                ConditionalBranch(
                    condition="age >= 65",
                    field_name="elderly_concerns",
                    question_type="multiselect",
                    question_text="Are you experiencing any age-related health concerns?",
                    options=["Cognitive decline", "Falls/balance issues", "Multiple medications", "Chronic pain", "Social isolation", "Mobility issues"],
                    required=False
                ),
                ConditionalBranch(
                    condition="age >= 75",
                    field_name="frailty_assessment",
                    question_type="select",
                    question_text="How would you describe your overall physical condition?",
                    options=["Very active/robust", "Moderately active", "Somewhat limited", "Significantly limited", "Frail/requires assistance"],
                    required=True
                )
            ],
            
            "medical_condition_specific": [
                # Diabetes management
                ConditionalBranch(
                    condition="'diabetes' in medical_history or 'metformin' in current_medications",
                    field_name="diabetes_details",
                    question_type="multiselect",
                    question_text="Please provide more details about your diabetes management:",
                    options=["Type 1 diabetes", "Type 2 diabetes", "Gestational diabetes", "Prediabetes", "Well controlled", "Poorly controlled", "Recent changes in medications"],
                    required=True
                ),
                ConditionalBranch(
                    condition="'diabetes' in medical_history",
                    field_name="recent_hba1c",
                    question_type="input",
                    question_text="What was your most recent HbA1c result? (if known)",
                    validation_rules={"min": 4.0, "max": 15.0, "type": "float"},
                    required=False
                ),
                
                # Cardiovascular conditions
                ConditionalBranch(
                    condition="'hypertension' in medical_history or 'heart disease' in medical_history",
                    field_name="cardiovascular_details",
                    question_type="multiselect",
                    question_text="Please specify your cardiovascular conditions:",
                    options=["Hypertension", "Coronary artery disease", "Heart failure", "Arrhythmias", "Stroke history", "High cholesterol", "Blood clotting disorders"],
                    required=True
                ),
                
                # Cancer history
                ConditionalBranch(
                    condition="'cancer' in medical_history",
                    field_name="cancer_details",
                    question_type="multiselect",
                    question_text="Please provide cancer history details (this affects peptide safety):",
                    options=["Currently in treatment", "In remission < 2 years", "In remission 2-5 years", "In remission > 5 years", "Family history only", "Multiple cancers"],
                    required=True
                ),
                
                # Autoimmune conditions
                ConditionalBranch(
                    condition="'autoimmune' in medical_history or 'lupus' in medical_history or 'rheumatoid' in medical_history",
                    field_name="autoimmune_details",
                    question_type="multiselect",
                    question_text="Please specify your autoimmune condition(s):",
                    options=["Rheumatoid arthritis", "Lupus", "Multiple sclerosis", "Crohn's disease", "Ulcerative colitis", "Hashimoto's", "Type 1 diabetes", "Other"],
                    required=True
                ),
                
                # Kidney/liver disease
                ConditionalBranch(
                    condition="'kidney' in medical_history or 'liver' in medical_history or 'renal' in medical_history or 'hepatic' in medical_history",
                    field_name="organ_function_details",
                    question_type="multiselect",
                    question_text="Please specify any kidney or liver conditions:",
                    options=["Chronic kidney disease", "Dialysis", "Liver disease", "Hepatitis", "Cirrhosis", "Recent abnormal kidney function", "Recent abnormal liver function"],
                    required=True
                )
            ],
            
            "medication_specific": [
                # Blood thinners
                ConditionalBranch(
                    condition="'warfarin' in current_medications or 'coumadin' in current_medications or 'eliquis' in current_medications",
                    field_name="anticoagulation_details",
                    question_type="multiselect",
                    question_text="You're taking blood thinning medications. Please specify:",
                    options=["Warfarin/Coumadin", "Eliquis", "Xarelto", "Pradaxa", "Aspirin (daily)", "Recent INR values normal", "Recent bleeding episodes"],
                    required=True
                ),
                
                # Immunosuppressants
                ConditionalBranch(
                    condition="'cyclosporine' in current_medications or 'tacrolimus' in current_medications or 'methotrexate' in current_medications",
                    field_name="immunosuppression_details",
                    question_type="multiselect",
                    question_text="You're taking immunosuppressive medications. Please specify:",
                    options=["Organ transplant recipient", "Autoimmune disease treatment", "Cancer treatment", "Recent infections", "Live with immunocompromised persons"],
                    required=True
                ),
                
                # Psychiatric medications
                ConditionalBranch(
                    condition="'ssri' in current_medications or 'prozac' in current_medications or 'zoloft' in current_medications",
                    field_name="psychiatric_medication_details",
                    question_type="multiselect",
                    question_text="You're taking psychiatric medications. Please specify:",
                    options=["SSRIs", "SNRIs", "MAOIs", "Tricyclics", "Mood stabilizers", "Antipsychotics", "Recent dose changes"],
                    required=True
                )
            ],
            
            "lifestyle_risk_factors": [
                # High-risk activities
                ConditionalBranch(
                    condition="'athlete' in lifestyle_factors.values() or 'competitive sports' in health_goals",
                    field_name="athletic_details",
                    question_type="multiselect",
                    question_text="Please specify your athletic activities and goals:",
                    options=["Professional athlete", "Competitive amateur", "Bodybuilding", "Endurance sports", "Contact sports", "Performance enhancement goals"],
                    required=True
                ),
                
                # Substance use screening
                ConditionalBranch(
                    condition="age >= 18",
                    field_name="substance_use",
                    question_type="multiselect",
                    question_text="Please indicate any substance use (affects peptide metabolism):",
                    options=["Social alcohol use", "Regular alcohol use", "Tobacco/nicotine", "Marijuana", "Performance enhancing drugs", "None of the above"],
                    required=False
                )
            ]
        }
    
    def _initialize_risk_flag_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize risk flagging rules for patient safety"""
        
        return {
            "high_risk_flags": {
                "cancer_active": {
                    "conditions": ["'currently in treatment' in cancer_details", "'in remission < 2 years' in cancer_details"],
                    "contraindicated_peptides": ["BPC-157", "TB-500", "GHK-Cu", "Thymosin Alpha-1", "Epithalon"],
                    "warning": "CRITICAL: Active or recent cancer history - growth-promoting peptides contraindicated",
                    "action": "require_oncology_clearance"
                },
                "pregnancy": {
                    "conditions": ["pregnancy_status in ['Pregnant', 'Trying to conceive', 'Breastfeeding']"],
                    "contraindicated_peptides": ["ALL_PEPTIDES"],
                    "warning": "CRITICAL: Pregnancy/breastfeeding - all peptides contraindicated",
                    "action": "absolute_contraindication"
                },
                "severe_immunocompromise": {
                    "conditions": ["'organ transplant' in immunosuppression_details"],
                    "contraindicated_peptides": ["Thymosin Alpha-1", "Thymosin Beta-4"],
                    "warning": "HIGH RISK: Immunosuppressed - immune-modulating peptides require specialist approval",
                    "action": "require_specialist_approval"
                }
            },
            
            "medium_risk_flags": {
                "cardiovascular_risk": {
                    "conditions": ["'heart disease' in cardiovascular_details", "'stroke history' in cardiovascular_details"],
                    "contraindicated_peptides": ["PT-141", "Melanotan II"],
                    "warning": "CAUTION: Cardiovascular conditions - avoid peptides affecting blood pressure",
                    "action": "require_monitoring"
                },
                "diabetes_interaction": {
                    "conditions": ["'diabetes' in diabetes_details", "'insulin' in current_medications"],
                    "interaction_peptides": ["CJC-1295", "Ipamorelin", "Sermorelin"],
                    "warning": "MONITOR: Diabetes medications may require adjustment with GH peptides",
                    "action": "enhanced_glucose_monitoring"
                },
                "elderly_patient": {
                    "conditions": ["age >= 75", "'frail' in frailty_assessment"],
                    "dose_adjustments": "ALL_PEPTIDES",
                    "warning": "ADJUST: Elderly patient - consider 25-50% dose reduction",
                    "action": "dose_adjustment_required"
                }
            },
            
            "monitoring_requirements": {
                "liver_function": {
                    "conditions": ["'liver disease' in organ_function_details", "'hepatitis' in organ_function_details"],
                    "monitoring": "Monthly liver function tests for first 3 months",
                    "peptides_affected": "ALL_METABOLIZED_PEPTIDES"
                },
                "kidney_function": {
                    "conditions": ["'kidney disease' in organ_function_details", "'dialysis' in organ_function_details"],
                    "monitoring": "Monthly creatinine and BUN for first 3 months",
                    "peptides_affected": "ALL_RENALLY_CLEARED_PEPTIDES"
                }
            }
        }
    
    def _initialize_lab_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize lab interpretation rules for clinical decision making"""
        
        return {
            "hba1c_interpretation": {
                "normal": {"range": [4.0, 5.6], "action": "no_additional_monitoring"},
                "prediabetic": {"range": [5.7, 6.4], "action": "monthly_glucose_monitoring"},
                "diabetic": {"range": [6.5, 15.0], "action": "weekly_glucose_monitoring_with_gh_peptides"}
            },
            
            "testosterone_interpretation": {
                "male_low": {"range": [0, 300], "action": "consider_testosterone_optimization"},
                "male_normal": {"range": [300, 1000], "action": "standard_protocols"},
                "male_high": {"range": [1000, 2000], "action": "monitor_for_aromatization"}
            },
            
            "liver_function_interpretation": {
                "alt_elevated": {"threshold": 40, "action": "avoid_hepatically_metabolized_peptides"},
                "ast_elevated": {"threshold": 40, "action": "baseline_liver_monitoring"},
                "bilirubin_elevated": {"threshold": 1.2, "action": "hepatology_consultation"}
            },
            
            "kidney_function_interpretation": {
                "creatinine_elevated": {"threshold": 1.3, "action": "dose_reduction_renally_cleared"},
                "bun_elevated": {"threshold": 20, "action": "enhanced_hydration_protocols"},
                "gfr_reduced": {"threshold": 60, "action": "nephrology_consultation"}
            }
        }
    
    def evaluate_conditional_branches(self, assessment_data: Dict[str, Any]) -> List[ConditionalBranch]:
        """
        Evaluate which conditional branches should be presented to the patient
        
        Args:
            assessment_data: Current assessment data from patient
            
        Returns:
            List of ConditionalBranch objects that should be presented
        """
        applicable_branches = []
        
        try:
            # Convert assessment data to lowercase for easier matching
            assessment_lower = self._normalize_assessment_data(assessment_data)
            
            # Evaluate each category of conditional branches
            for category, branches in self.conditional_branches.items():
                for branch in branches:
                    if self._evaluate_condition(branch.condition, assessment_lower):
                        applicable_branches.append(branch)
                        self.logger.info(f"Conditional branch triggered: {branch.field_name} for condition: {branch.condition}")
            
            return applicable_branches
            
        except Exception as e:
            self.logger.error(f"Error evaluating conditional branches: {e}")
            return []
    
    def _normalize_assessment_data(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize assessment data for condition evaluation"""
        
        normalized = {}
        
        for key, value in assessment_data.items():
            if isinstance(value, str):
                normalized[key] = value.lower()
            elif isinstance(value, list):
                normalized[key] = [str(item).lower() if item else '' for item in value]
            elif isinstance(value, dict):
                normalized[key] = {k: str(v).lower() if v else '' for k, v in value.items()}
            else:
                normalized[key] = value
        
        return normalized
    
    def _evaluate_condition(self, condition: str, assessment_data: Dict[str, Any]) -> bool:
        """
        Safely evaluate a condition string against assessment data
        
        Args:
            condition: String condition to evaluate
            assessment_data: Normalized assessment data
            
        Returns:
            Boolean result of condition evaluation
        """
        try:
            # Create a safe evaluation environment
            safe_dict = {
                'age': assessment_data.get('age', 0),
                'gender': assessment_data.get('gender', ''),
                'weight': assessment_data.get('weight', 0),
                'primary_concerns': assessment_data.get('primary_concerns', []),
                'health_goals': assessment_data.get('health_goals', []),
                'current_medications': assessment_data.get('current_medications', []),
                'medical_history': assessment_data.get('medical_history', []),
                'lifestyle_factors': assessment_data.get('lifestyle_factors', {}),
                'pregnancy_status': assessment_data.get('pregnancy_status', ''),
                'diabetes_details': assessment_data.get('diabetes_details', []),
                'cancer_details': assessment_data.get('cancer_details', []),
                'cardiovascular_details': assessment_data.get('cardiovascular_details', []),
                'autoimmune_details': assessment_data.get('autoimmune_details', []),
                'immunosuppression_details': assessment_data.get('immunosuppression_details', []),
                'organ_function_details': assessment_data.get('organ_function_details', []),
                'frailty_assessment': assessment_data.get('frailty_assessment', '')
            }
            
            # Use eval with restricted environment for condition evaluation
            return eval(condition, {"__builtins__": {}}, safe_dict)
            
        except Exception as e:
            self.logger.error(f"Error evaluating condition '{condition}': {e}")
            return False
    
    def generate_risk_flags(self, assessment_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate risk flags based on patient assessment data
        
        Args:
            assessment_data: Patient assessment data
            
        Returns:
            Dictionary containing categorized risk flags
        """
        risk_flags = {
            "high_risk": [],
            "medium_risk": [],
            "monitoring_required": []
        }
        
        try:
            assessment_lower = self._normalize_assessment_data(assessment_data)
            
            # Evaluate high risk flags
            for flag_name, flag_config in self.risk_flag_rules["high_risk_flags"].items():
                for condition in flag_config["conditions"]:
                    if self._evaluate_condition(condition, assessment_lower):
                        risk_flags["high_risk"].append({
                            "flag": flag_name,
                            "warning": flag_config["warning"],
                            "action": flag_config["action"],
                            "contraindicated_peptides": flag_config.get("contraindicated_peptides", [])
                        })
            
            # Evaluate medium risk flags
            for flag_name, flag_config in self.risk_flag_rules["medium_risk_flags"].items():
                for condition in flag_config["conditions"]:
                    if self._evaluate_condition(condition, assessment_lower):
                        risk_flags["medium_risk"].append({
                            "flag": flag_name,
                            "warning": flag_config["warning"],
                            "action": flag_config["action"],
                            "affected_peptides": flag_config.get("interaction_peptides", flag_config.get("dose_adjustments", []))
                        })
            
            # Evaluate monitoring requirements
            for requirement_name, requirement_config in self.risk_flag_rules["monitoring_requirements"].items():
                for condition in requirement_config["conditions"]:
                    if self._evaluate_condition(condition, assessment_lower):
                        risk_flags["monitoring_required"].append({
                            "requirement": requirement_name,
                            "monitoring": requirement_config["monitoring"],
                            "peptides_affected": requirement_config["peptides_affected"]
                        })
            
            return risk_flags
            
        except Exception as e:
            self.logger.error(f"Error generating risk flags: {e}")
            return risk_flags
    
    def interpret_lab_values(self, lab_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpret uploaded lab values and generate clinical recommendations
        
        Args:
            lab_data: Dictionary of lab values
            
        Returns:
            Dictionary containing interpretations and recommendations
        """
        interpretations = {
            "critical_values": [],
            "abnormal_values": [],
            "recommendations": [],
            "peptide_adjustments": []
        }
        
        try:
            # HbA1c interpretation
            if "hba1c" in lab_data:
                hba1c_value = float(lab_data["hba1c"])
                hba1c_rules = self.lab_interpretation_rules["hba1c_interpretation"]
                
                if hba1c_value >= 6.5:
                    interpretations["abnormal_values"].append({
                        "test": "HbA1c",
                        "value": hba1c_value,
                        "interpretation": "Diabetic range",
                        "action": hba1c_rules["diabetic"]["action"]
                    })
                elif hba1c_value >= 5.7:
                    interpretations["abnormal_values"].append({
                        "test": "HbA1c", 
                        "value": hba1c_value,
                        "interpretation": "Prediabetic range",
                        "action": hba1c_rules["prediabetic"]["action"]
                    })
            
            # Liver function interpretation
            if "alt" in lab_data:
                alt_value = float(lab_data["alt"])
                alt_threshold = self.lab_interpretation_rules["liver_function_interpretation"]["alt_elevated"]["threshold"]
                
                if alt_value > alt_threshold:
                    interpretations["abnormal_values"].append({
                        "test": "ALT",
                        "value": alt_value,
                        "interpretation": "Elevated liver enzymes",
                        "action": "avoid_hepatically_metabolized_peptides"
                    })
            
            # Kidney function interpretation
            if "creatinine" in lab_data:
                creatinine_value = float(lab_data["creatinine"])
                creatinine_threshold = self.lab_interpretation_rules["kidney_function_interpretation"]["creatinine_elevated"]["threshold"]
                
                if creatinine_value > creatinine_threshold:
                    interpretations["abnormal_values"].append({
                        "test": "Creatinine",
                        "value": creatinine_value,
                        "interpretation": "Elevated creatinine - possible kidney dysfunction",
                        "action": "dose_reduction_renally_cleared"
                    })
            
            # Generate specific recommendations based on interpretations
            for abnormal in interpretations["abnormal_values"]:
                if abnormal["action"] == "weekly_glucose_monitoring_with_gh_peptides":
                    interpretations["recommendations"].append(
                        "Weekly glucose monitoring required if using GH-stimulating peptides (CJC-1295, Ipamorelin, Sermorelin)"
                    )
                    interpretations["peptide_adjustments"].append({
                        "peptides": ["CJC-1295", "Ipamorelin", "Sermorelin"],
                        "adjustment": "Enhanced glucose monitoring required",
                        "frequency": "Weekly for first 4 weeks, then biweekly"
                    })
                
                elif abnormal["action"] == "avoid_hepatically_metabolized_peptides":
                    interpretations["recommendations"].append(
                        "Elevated liver enzymes detected - avoid peptides with significant hepatic metabolism"
                    )
                    interpretations["peptide_adjustments"].append({
                        "peptides": ["Oral formulations", "High-dose protocols"],
                        "adjustment": "Use injectable forms and standard doses only",
                        "monitoring": "Monthly liver function tests"
                    })
            
            return interpretations
            
        except Exception as e:
            self.logger.error(f"Error interpreting lab values: {e}")
            return interpretations
    
    def generate_personalized_questions(self, assessment_data: Dict[str, Any], step: int) -> Dict[str, Any]:
        """
        Generate personalized questions for a given assessment step
        
        Args:
            assessment_data: Current assessment data
            step: Current step in assessment
            
        Returns:
            Dictionary containing personalized questions and flow control
        """
        try:
            applicable_branches = self.evaluate_conditional_branches(assessment_data)
            risk_flags = self.generate_risk_flags(assessment_data)
            
            # Filter branches for current step
            step_branches = [branch for branch in applicable_branches if self._should_show_in_step(branch, step)]
            
            return {
                "conditional_questions": [
                    {
                        "field_name": branch.field_name,
                        "question_type": branch.question_type,
                        "question_text": branch.question_text,
                        "options": branch.options,
                        "required": branch.required,
                        "validation_rules": branch.validation_rules
                    }
                    for branch in step_branches
                ],
                "risk_flags": risk_flags,
                "recommended_next_step": self._calculate_next_step(assessment_data, risk_flags),
                "completion_percentage": self._calculate_completion_percentage(assessment_data, applicable_branches)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating personalized questions: {e}")
            return {"conditional_questions": [], "risk_flags": {"high_risk": [], "medium_risk": [], "monitoring_required": []}}
    
    def _should_show_in_step(self, branch: ConditionalBranch, step: int) -> bool:
        """Determine if a conditional branch should be shown in a specific step"""
        
        # Map conditional branches to appropriate steps
        step_mapping = {
            1: ["gender_specific", "age_specific"],
            3: ["medical_condition_specific", "medication_specific"],
            4: ["lifestyle_risk_factors"],
            5: ["lab_specific", "genetic_specific"]
        }
        
        for branch_step, categories in step_mapping.items():
            if step == branch_step:
                # Check if this branch belongs to categories for this step
                for category in self.conditional_branches.keys():
                    if category in categories and branch in self.conditional_branches[category]:
                        return True
        
        return False
    
    def _calculate_next_step(self, assessment_data: Dict[str, Any], risk_flags: Dict[str, List]) -> int:
        """Calculate the recommended next step based on current data and risk flags"""
        
        current_step = assessment_data.get("step_completed", 1)
        
        # If high-risk flags are present, may need additional safety steps
        if risk_flags["high_risk"]:
            return min(current_step + 1, 6)  # Standard flow but with additional safety checks
        
        return min(current_step + 1, 6)
    
    def _calculate_completion_percentage(self, assessment_data: Dict[str, Any], applicable_branches: List[ConditionalBranch]) -> float:
        """Calculate assessment completion percentage"""
        
        base_fields = ["patient_name", "age", "gender", "weight", "primary_concerns", "health_goals"]
        completed_base = sum(1 for field in base_fields if assessment_data.get(field))
        
        # Add conditional field completion
        applicable_fields = [branch.field_name for branch in applicable_branches if branch.required]
        completed_conditional = sum(1 for field in applicable_fields if assessment_data.get(field))
        
        total_required = len(base_fields) + len(applicable_fields)
        total_completed = completed_base + completed_conditional
        
        return (total_completed / total_required * 100) if total_required > 0 else 0


# Initialize the global adaptive assessment engine
adaptive_engine = AdaptiveAssessmentEngine()