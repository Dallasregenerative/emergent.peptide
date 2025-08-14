"""
Per-Peptide Dosing Calculator System
Advanced dosing calculations based on patient characteristics, conditions, and safety parameters
Hospital-grade precision with real-time adjustments
"""

import json
import logging
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

@dataclass
class DosingCalculation:
    """Represents a calculated dose with rationale"""
    peptide_name: str
    base_dose: float
    calculated_dose: float
    unit: str
    frequency: str
    route: str
    adjustments_applied: List[str]
    safety_notes: List[str]
    monitoring_requirements: List[str]
    titration_schedule: Optional[Dict[str, Any]] = None

class PeptideDosingCalculator:
    """
    Advanced per-peptide dosing calculator with patient-specific adjustments
    Integrates safety parameters, contraindications, and clinical guidelines
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_dosing_protocols = self._initialize_base_dosing()
        self.adjustment_factors = self._initialize_adjustment_factors()
        self.safety_limits = self._initialize_safety_limits()
        self.interaction_adjustments = self._initialize_interaction_adjustments()
    
    def _initialize_base_dosing(self) -> Dict[str, Dict[str, Any]]:
        """Initialize base dosing protocols for each peptide"""
        
        return {
            "BPC-157": {
                "base_dose_mcg": 250,
                "unit": "mcg",
                "base_frequency": "twice daily",
                "route": "subcutaneous",
                "weight_based": False,
                "min_dose": 100,
                "max_dose": 500,
                "titration_possible": True,
                "injection_volume_ml": 0.25,
                "concentration_mcg_ml": 1000,
                "administration_timing": "morning and evening",
                "food_interaction": "none"
            },
            
            "TB-500": {
                "base_dose_mg": 2.5,
                "unit": "mg",
                "base_frequency": "twice weekly",
                "route": "subcutaneous",
                "weight_based": False,
                "min_dose": 2.0,
                "max_dose": 10.0,
                "titration_possible": False,
                "injection_volume_ml": 1.0,
                "concentration_mg_ml": 2.5,
                "administration_timing": "any time",
                "food_interaction": "none"
            },
            
            "CJC-1295": {
                "base_dose_mcg_kg": 1.0,
                "unit": "mcg",
                "base_frequency": "daily",
                "route": "subcutaneous",
                "weight_based": True,
                "min_dose_mcg_kg": 0.5,
                "max_dose_mcg_kg": 2.0,
                "titration_possible": True,
                "injection_volume_ml": 0.3,
                "administration_timing": "bedtime",
                "food_interaction": "take on empty stomach"
            },
            
            "Ipamorelin": {
                "base_dose_mcg_kg": 1.0,
                "unit": "mcg",
                "base_frequency": "daily",
                "route": "subcutaneous",
                "weight_based": True,
                "min_dose_mcg_kg": 0.5,
                "max_dose_mcg_kg": 2.0,
                "titration_possible": True,
                "injection_volume_ml": 0.3,
                "administration_timing": "bedtime on empty stomach",
                "food_interaction": "avoid food 2 hours before/after"
            },
            
            "Semaglutide": {
                "starting_dose_mg": 0.25,
                "unit": "mg",
                "base_frequency": "weekly",
                "route": "subcutaneous",
                "weight_based": False,
                "titration_schedule": {
                    "week_1_4": 0.25,
                    "week_5_8": 0.5,
                    "week_9_12": 1.0,
                    "week_13_16": 1.7,
                    "maintenance": 2.4
                },
                "max_dose": 2.4,
                "injection_volume_ml": 0.5,
                "administration_timing": "any time, same day each week",
                "food_interaction": "none"
            },
            
            "Thymosin Alpha-1": {
                "base_dose_mg": 1.5,
                "unit": "mg",
                "base_frequency": "twice weekly",
                "route": "subcutaneous",
                "weight_based": False,
                "min_dose": 1.0,
                "max_dose": 3.0,
                "injection_volume_ml": 0.5,
                "administration_timing": "morning",
                "food_interaction": "none"
            },
            
            "GHK-Cu": {
                "base_dose_mg": 1.0,
                "unit": "mg",
                "base_frequency": "daily",
                "route": "subcutaneous or topical",
                "weight_based": False,
                "min_dose": 0.5,
                "max_dose": 3.0,
                "topical_concentration": "3%",
                "injection_volume_ml": 0.3,
                "administration_timing": "bedtime",
                "food_interaction": "none"
            },
            
            "Epithalon": {
                "base_dose_mg": 10,
                "unit": "mg",
                "base_frequency": "daily for 10 days",
                "route": "subcutaneous",
                "weight_based": False,
                "cycle_protocol": "10 days on, 20 days off",
                "min_dose": 5,
                "max_dose": 20,
                "injection_volume_ml": 0.5,
                "administration_timing": "bedtime",
                "food_interaction": "none"
            },
            
            "PT-141": {
                "base_dose_mg": 1.5,
                "unit": "mg",
                "base_frequency": "as needed",
                "route": "subcutaneous",
                "weight_based": False,
                "max_frequency": "2 doses per week",
                "onset_hours": 4,
                "duration_hours": 12,
                "injection_volume_ml": 0.3,
                "administration_timing": "4 hours before activity",
                "food_interaction": "none"
            },
            
            "Melanotan II": {
                "starting_dose_mcg": 100,
                "maintenance_dose_mcg": 250,
                "unit": "mcg",
                "base_frequency": "every other day",
                "route": "subcutaneous",
                "weight_based": False,
                "titration_days": 7,
                "max_dose": 500,
                "injection_volume_ml": 0.25,
                "administration_timing": "evening",
                "food_interaction": "none"
            },
            
            # Oral/Capsule formulations
            "Epithalon Capsules": {
                "base_dose_mg": 10,
                "unit": "mg",
                "base_frequency": "twice daily for 10 days",
                "route": "oral",
                "cycle_protocol": "10 days on, 20 days off",
                "capsule_strength_mg": 5,
                "capsules_per_dose": 2,
                "administration_timing": "morning and evening on empty stomach",
                "food_interaction": "take 30-60 minutes before meals"
            },
            
            "BPC-157 Capsules": {
                "base_dose_mg": 0.25,
                "unit": "mg",
                "base_frequency": "twice daily",
                "route": "oral",
                "capsule_strength_mg": 0.25,
                "capsules_per_dose": 1,
                "bioavailability_percent": 10,
                "administration_timing": "30 minutes before breakfast and dinner",
                "food_interaction": "best on empty stomach for GI conditions"
            },
            
            "Thymosin Alpha-1 Capsules": {
                "base_dose_mg": 1.0,
                "unit": "mg", 
                "base_frequency": "twice weekly",
                "route": "oral",
                "capsule_strength_mg": 0.5,
                "capsules_per_dose": 2,
                "bioavailability_percent": 6,
                "administration_timing": "morning on empty stomach",
                "food_interaction": "avoid dairy within 2 hours"
            }
        }
    
    def _initialize_adjustment_factors(self) -> Dict[str, Dict[str, float]]:
        """Initialize dosing adjustment factors based on patient characteristics"""
        
        return {
            "age_adjustments": {
                "pediatric": {"multiplier": 0.5, "age_range": [12, 17]},
                "young_adult": {"multiplier": 1.0, "age_range": [18, 39]},
                "middle_age": {"multiplier": 1.0, "age_range": [40, 64]},
                "elderly": {"multiplier": 0.8, "age_range": [65, 74]},
                "geriatric": {"multiplier": 0.6, "age_range": [75, 100]}
            },
            
            "weight_adjustments": {
                "underweight": {"multiplier": 0.8, "bmi_range": [0, 18.4]},
                "normal": {"multiplier": 1.0, "bmi_range": [18.5, 24.9]},
                "overweight": {"multiplier": 1.1, "bmi_range": [25.0, 29.9]},
                "obese": {"multiplier": 1.2, "bmi_range": [30.0, 39.9]},
                "morbidly_obese": {"multiplier": 1.0, "bmi_range": [40.0, 60.0]}  # No increase due to safety
            },
            
            "gender_adjustments": {
                "male": {"multiplier": 1.0},
                "female": {"multiplier": 0.9},  # Generally lower doses for women
                "female_pregnant": {"multiplier": 0.0},  # Contraindicated
                "female_breastfeeding": {"multiplier": 0.0}  # Contraindicated
            },
            
            "condition_adjustments": {
                "diabetes": {"multiplier": 0.9, "monitoring": "enhanced_glucose"},
                "kidney_disease": {"multiplier": 0.7, "monitoring": "renal_function"},
                "liver_disease": {"multiplier": 0.8, "monitoring": "hepatic_function"},
                "cardiovascular_disease": {"multiplier": 0.9, "monitoring": "cardiac"},
                "autoimmune": {"multiplier": 1.0, "monitoring": "immune_markers"},
                "cancer_history": {"multiplier": 0.0, "contraindication": True},
                "active_cancer": {"multiplier": 0.0, "contraindication": True}
            },
            
            "medication_interactions": {
                "insulin": {"multiplier": 0.9, "monitoring": "glucose_daily"},
                "metformin": {"multiplier": 1.0, "monitoring": "glucose_weekly"},
                "corticosteroids": {"multiplier": 0.8, "timing": "separate_4_hours"},
                "anticoagulants": {"multiplier": 1.0, "monitoring": "bleeding_risk"},
                "immunosuppressants": {"multiplier": 0.0, "contraindication": "thymosin_peptides"},
                "ssri": {"multiplier": 0.9, "monitoring": "mood_changes"}
            }
        }
    
    def _initialize_safety_limits(self) -> Dict[str, Dict[str, Any]]:
        """Initialize safety limits and maximum doses for each peptide"""
        
        return {
            "absolute_maximums": {
                "BPC-157": {"daily_max_mcg": 1000, "weekly_max_mcg": 7000},
                "TB-500": {"weekly_max_mg": 10, "monthly_max_mg": 40},
                "CJC-1295": {"daily_max_mcg_kg": 3.0, "absolute_max_mcg": 300},
                "Ipamorelin": {"daily_max_mcg_kg": 3.0, "absolute_max_mcg": 300},
                "Semaglutide": {"weekly_max_mg": 2.4, "titration_required": True},
                "Thymosin Alpha-1": {"weekly_max_mg": 6.0, "daily_max_mg": 3.0},
                "GHK-Cu": {"daily_max_mg": 5.0, "topical_max_percent": 5.0},
                "PT-141": {"weekly_max_doses": 2, "dose_max_mg": 2.0},
                "Melanotan II": {"daily_max_mcg": 1000, "loading_max_days": 14}
            },
            
            "contraindication_overrides": {
                "pregnancy": ["ALL_PEPTIDES"],
                "breastfeeding": ["ALL_PEPTIDES"],
                "active_cancer": ["BPC-157", "TB-500", "GHK-Cu", "Thymosin Alpha-1", "Epithalon"],
                "severe_cardiovascular": ["PT-141", "Melanotan II"],
                "immunosuppressed": ["Thymosin Alpha-1", "TB-500"],
                "severe_kidney_disease": ["ALL_RENALLY_CLEARED"],
                "severe_liver_disease": ["ALL_HEPATICALLY_METABOLIZED"]
            }
        }
    
    def _initialize_interaction_adjustments(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize peptide-drug interaction adjustments"""
        
        return {
            "CJC-1295": [
                {
                    "interacting_drug": "insulin",
                    "adjustment_type": "dose_reduction",
                    "factor": 0.8,
                    "monitoring": "Daily glucose monitoring for first 2 weeks",
                    "timing": "Standard timing acceptable"
                },
                {
                    "interacting_drug": "metformin", 
                    "adjustment_type": "enhanced_monitoring",
                    "factor": 1.0,
                    "monitoring": "Weekly glucose monitoring",
                    "timing": "Standard timing acceptable"
                }
            ],
            
            "PT-141": [
                {
                    "interacting_drug": "sildenafil",
                    "adjustment_type": "contraindication",
                    "factor": 0.0,
                    "monitoring": "Blood pressure monitoring required",
                    "timing": "Separate by minimum 24 hours"
                },
                {
                    "interacting_drug": "tadalafil",
                    "adjustment_type": "contraindication", 
                    "factor": 0.0,
                    "monitoring": "Cardiovascular monitoring required",
                    "timing": "Separate by minimum 48 hours"
                }
            ],
            
            "BPC-157": [
                {
                    "interacting_drug": "prednisone",
                    "adjustment_type": "timing_separation",
                    "factor": 1.0,
                    "monitoring": "Therapeutic response monitoring",
                    "timing": "Separate administration by 4+ hours"
                }
            ]
        }
    
    def calculate_personalized_dose(self, peptide_name: str, patient_data: Dict[str, Any], 
                                  clinical_indication: Optional[str] = None) -> DosingCalculation:
        """
        Calculate personalized dose for a specific peptide and patient
        
        Args:
            peptide_name: Name of the peptide
            patient_data: Patient assessment data
            clinical_indication: Specific clinical indication if applicable
            
        Returns:
            DosingCalculation object with personalized dosing
        """
        try:
            if peptide_name not in self.base_dosing_protocols:
                raise ValueError(f"Peptide '{peptide_name}' not found in dosing protocols")
            
            base_protocol = self.base_dosing_protocols[peptide_name]
            
            # Check for absolute contraindications first
            contraindication_result = self._check_contraindications(peptide_name, patient_data)
            if contraindication_result["contraindicated"]:
                return DosingCalculation(
                    peptide_name=peptide_name,
                    base_dose=0,
                    calculated_dose=0,
                    unit=base_protocol["unit"],
                    frequency="CONTRAINDICATED",
                    route=base_protocol["route"],
                    adjustments_applied=["CONTRAINDICATED"],
                    safety_notes=[contraindication_result["reason"]],
                    monitoring_requirements=["Do not administer"]
                )
            
            # Calculate base dose
            if base_protocol.get("weight_based", False):
                weight_kg = self._convert_weight_to_kg(patient_data.get("weight", 70))
                base_dose = base_protocol.get("base_dose_mcg_kg", 1.0) * weight_kg
            else:
                base_dose = base_protocol.get("base_dose_mcg", base_protocol.get("base_dose_mg", 1.0))
                if "base_dose_mg" in base_protocol:
                    base_dose = base_dose  # Already in mg
                elif "starting_dose_mg" in base_protocol:
                    base_dose = base_protocol["starting_dose_mg"]
                elif "starting_dose_mcg" in base_protocol:
                    base_dose = base_protocol["starting_dose_mcg"] / 1000  # Convert to mg
            
            # Apply adjustment factors
            calculated_dose = base_dose
            adjustments_applied = []
            safety_notes = []
            monitoring_requirements = []
            
            # Age adjustments
            age = patient_data.get("age", 40)
            age_factor = self._get_age_adjustment_factor(age)
            if age_factor != 1.0:
                calculated_dose *= age_factor
                adjustments_applied.append(f"Age adjustment: {age_factor:.1f}x")
                if age >= 75:
                    safety_notes.append("Elderly patient - start with reduced dose and monitor closely")
            
            # Gender adjustments
            gender = patient_data.get("gender", "male").lower()
            pregnancy_status = patient_data.get("pregnancy_status", "")
            if "pregnant" in pregnancy_status.lower() or "breastfeeding" in pregnancy_status.lower():
                gender_factor = 0.0
                safety_notes.append("CONTRAINDICATED in pregnancy/breastfeeding")
            else:
                gender_factor = self.adjustment_factors["gender_adjustments"].get(gender, {}).get("multiplier", 1.0)
                if gender_factor != 1.0:
                    calculated_dose *= gender_factor
                    adjustments_applied.append(f"Gender adjustment: {gender_factor:.1f}x")
            
            # Weight/BMI adjustments (for non-weight-based peptides)
            if not base_protocol.get("weight_based", False):
                bmi = self._calculate_bmi(patient_data)
                weight_factor = self._get_weight_adjustment_factor(bmi)
                if weight_factor != 1.0:
                    calculated_dose *= weight_factor
                    adjustments_applied.append(f"BMI adjustment: {weight_factor:.1f}x")
            
            # Medical condition adjustments
            condition_factor, condition_notes, condition_monitoring = self._apply_condition_adjustments(
                patient_data, peptide_name
            )
            calculated_dose *= condition_factor
            if condition_factor != 1.0:
                adjustments_applied.append(f"Medical condition adjustment: {condition_factor:.1f}x")
            safety_notes.extend(condition_notes)
            monitoring_requirements.extend(condition_monitoring)
            
            # Medication interaction adjustments
            interaction_factor, interaction_notes, interaction_monitoring = self._apply_interaction_adjustments(
                patient_data, peptide_name
            )
            calculated_dose *= interaction_factor
            if interaction_factor != 1.0:
                adjustments_applied.append(f"Drug interaction adjustment: {interaction_factor:.1f}x")
            safety_notes.extend(interaction_notes)
            monitoring_requirements.extend(interaction_monitoring)
            
            # Apply safety limits
            calculated_dose = self._apply_safety_limits(peptide_name, calculated_dose, base_protocol)
            
            # Generate titration schedule if applicable
            titration_schedule = None
            if base_protocol.get("titration_possible", False) or "titration_schedule" in base_protocol:
                titration_schedule = self._generate_titration_schedule(
                    peptide_name, calculated_dose, base_protocol, patient_data
                )
            
            return DosingCalculation(
                peptide_name=peptide_name,
                base_dose=base_dose,
                calculated_dose=round(calculated_dose, 3),
                unit=base_protocol["unit"],
                frequency=base_protocol["base_frequency"],
                route=base_protocol["route"],
                adjustments_applied=adjustments_applied,
                safety_notes=safety_notes,
                monitoring_requirements=monitoring_requirements,
                titration_schedule=titration_schedule
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating dose for {peptide_name}: {e}")
            return DosingCalculation(
                peptide_name=peptide_name,
                base_dose=0,
                calculated_dose=0,
                unit="N/A",
                frequency="ERROR",
                route="N/A",
                adjustments_applied=["Calculation error"],
                safety_notes=[f"Error in dose calculation: {str(e)}"],
                monitoring_requirements=["Consult practitioner"]
            )
    
    def _check_contraindications(self, peptide_name: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for absolute contraindications"""
        
        # Pregnancy/breastfeeding
        pregnancy_status = patient_data.get("pregnancy_status", "").lower()
        if any(status in pregnancy_status for status in ["pregnant", "breastfeeding", "trying to conceive"]):
            return {"contraindicated": True, "reason": f"{peptide_name} is contraindicated during pregnancy/breastfeeding"}
        
        # Active cancer
        cancer_details = patient_data.get("cancer_details", [])
        if isinstance(cancer_details, list):
            cancer_details = " ".join(cancer_details).lower()
        elif isinstance(cancer_details, str):
            cancer_details = cancer_details.lower()
        
        if "currently in treatment" in cancer_details or "active" in cancer_details:
            growth_peptides = ["bpc-157", "tb-500", "ghk-cu", "thymosin alpha-1", "epithalon"]
            if any(growth_peptide in peptide_name.lower() for growth_peptide in growth_peptides):
                return {"contraindicated": True, "reason": f"{peptide_name} may stimulate cell growth and is contraindicated with active cancer"}
        
        # Severe cardiovascular disease
        cardiovascular_details = patient_data.get("cardiovascular_details", [])
        if isinstance(cardiovascular_details, list):
            cv_string = " ".join(cardiovascular_details).lower()
        else:
            cv_string = str(cardiovascular_details).lower()
        
        if "severe" in cv_string or "uncontrolled" in cv_string:
            cv_contraindicated = ["pt-141", "melanotan"]
            if any(cv_peptide in peptide_name.lower() for cv_peptide in cv_contraindicated):
                return {"contraindicated": True, "reason": f"{peptide_name} affects blood pressure and is contraindicated with severe cardiovascular disease"}
        
        return {"contraindicated": False, "reason": ""}
    
    def _convert_weight_to_kg(self, weight_lbs: float) -> float:
        """Convert weight from pounds to kilograms"""
        return weight_lbs / 2.20462
    
    def _calculate_bmi(self, patient_data: Dict[str, Any]) -> float:
        """Calculate BMI from patient data"""
        weight_lbs = patient_data.get("weight", 150)
        height_feet = patient_data.get("height_feet", 5)
        height_inches = patient_data.get("height_inches", 8)
        
        # Convert to metric
        weight_kg = self._convert_weight_to_kg(weight_lbs)
        height_cm = (height_feet * 12 + height_inches) * 2.54
        height_m = height_cm / 100
        
        return weight_kg / (height_m ** 2)
    
    def _get_age_adjustment_factor(self, age: int) -> float:
        """Get age-based dosing adjustment factor"""
        for category, settings in self.adjustment_factors["age_adjustments"].items():
            age_range = settings["age_range"]
            if age_range[0] <= age <= age_range[1]:
                return settings["multiplier"]
        return 1.0
    
    def _get_weight_adjustment_factor(self, bmi: float) -> float:
        """Get weight-based dosing adjustment factor"""
        for category, settings in self.adjustment_factors["weight_adjustments"].items():
            bmi_range = settings["bmi_range"]
            if bmi_range[0] <= bmi <= bmi_range[1]:
                return settings["multiplier"]
        return 1.0
    
    def _apply_condition_adjustments(self, patient_data: Dict[str, Any], peptide_name: str) -> Tuple[float, List[str], List[str]]:
        """Apply medical condition-based adjustments"""
        
        factor = 1.0
        notes = []
        monitoring = []
        
        # Check various condition fields
        all_conditions = []
        for field in ["medical_history", "diabetes_details", "cardiovascular_details", 
                     "autoimmune_details", "organ_function_details"]:
            condition_data = patient_data.get(field, [])
            if isinstance(condition_data, list):
                all_conditions.extend([str(item).lower() for item in condition_data])
            elif condition_data:
                all_conditions.append(str(condition_data).lower())
        
        conditions_string = " ".join(all_conditions)
        
        # Apply condition-specific adjustments
        for condition, adjustment in self.adjustment_factors["condition_adjustments"].items():
            if condition in conditions_string:
                if adjustment.get("contraindication", False):
                    factor = 0.0
                    notes.append(f"Contraindicated due to {condition}")
                else:
                    factor *= adjustment["multiplier"]
                    if "monitoring" in adjustment:
                        monitoring.append(adjustment["monitoring"])
                    notes.append(f"Dose adjusted for {condition}")
        
        return factor, notes, monitoring
    
    def _apply_interaction_adjustments(self, patient_data: Dict[str, Any], peptide_name: str) -> Tuple[float, List[str], List[str]]:
        """Apply drug interaction-based adjustments"""
        
        factor = 1.0
        notes = []
        monitoring = []
        
        current_medications = patient_data.get("current_medications", [])
        if not isinstance(current_medications, list):
            current_medications = [str(current_medications)]
        
        medications_string = " ".join([str(med).lower() for med in current_medications])
        
        # Check for specific interactions
        if peptide_name in self.interaction_adjustments:
            for interaction in self.interaction_adjustments[peptide_name]:
                drug = interaction["interacting_drug"]
                if drug in medications_string:
                    if interaction["adjustment_type"] == "contraindication":
                        factor = 0.0
                        notes.append(f"Contraindicated with {drug}")
                    else:
                        factor *= interaction["factor"]
                        notes.append(f"Adjusted for interaction with {drug}")
                    
                    if "monitoring" in interaction:
                        monitoring.append(interaction["monitoring"])
                    if "timing" in interaction:
                        notes.append(f"Timing: {interaction['timing']}")
        
        # General medication adjustments
        for med, adjustment in self.adjustment_factors["medication_interactions"].items():
            if med in medications_string:
                if adjustment.get("contraindication"):
                    if adjustment["contraindication"] == "thymosin_peptides" and "thymosin" in peptide_name.lower():
                        factor = 0.0
                        notes.append(f"Thymosin peptides contraindicated with {med}")
                else:
                    factor *= adjustment["multiplier"]
                    if "monitoring" in adjustment:
                        monitoring.append(adjustment["monitoring"])
                    if "timing" in adjustment:
                        notes.append(f"Timing: {adjustment['timing']}")
        
        return factor, notes, monitoring
    
    def _apply_safety_limits(self, peptide_name: str, calculated_dose: float, base_protocol: Dict[str, Any]) -> float:
        """Apply safety limits to calculated dose"""
        
        if peptide_name in self.safety_limits["absolute_maximums"]:
            limits = self.safety_limits["absolute_maximums"][peptide_name]
            
            # Check different limit types
            if "daily_max_mcg" in limits and base_protocol["unit"] == "mcg":
                calculated_dose = min(calculated_dose, limits["daily_max_mcg"])
            elif "daily_max_mg" in limits and base_protocol["unit"] == "mg":
                calculated_dose = min(calculated_dose, limits["daily_max_mg"])
            elif "absolute_max_mcg" in limits and base_protocol["unit"] == "mcg":
                calculated_dose = min(calculated_dose, limits["absolute_max_mcg"])
        
        # Apply protocol-specific min/max
        if "min_dose" in base_protocol:
            calculated_dose = max(calculated_dose, base_protocol["min_dose"])
        if "max_dose" in base_protocol:
            calculated_dose = min(calculated_dose, base_protocol["max_dose"])
        
        return calculated_dose
    
    def _generate_titration_schedule(self, peptide_name: str, target_dose: float, 
                                   base_protocol: Dict[str, Any], patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a titration schedule for peptides that require gradual dose escalation"""
        
        if "titration_schedule" in base_protocol:
            # Use predefined titration schedule (e.g., Semaglutide)
            return base_protocol["titration_schedule"]
        
        # Generate custom titration schedule
        titration = {}
        
        # Standard titration: start at 50% target dose, increase weekly
        starting_dose = target_dose * 0.5
        week_2_dose = target_dose * 0.75
        week_3_dose = target_dose
        
        titration = {
            "week_1": {
                "dose": round(starting_dose, 3),
                "frequency": base_protocol["base_frequency"],
                "notes": "Starting dose - monitor for tolerability"
            },
            "week_2": {
                "dose": round(week_2_dose, 3),
                "frequency": base_protocol["base_frequency"], 
                "notes": "Increased dose - continue monitoring"
            },
            "week_3_maintenance": {
                "dose": round(target_dose, 3),
                "frequency": base_protocol["base_frequency"],
                "notes": "Target maintenance dose"
            }
        }
        
        return titration
    
    def calculate_injection_volume(self, peptide_name: str, calculated_dose: float) -> Dict[str, Any]:
        """Calculate injection volume and preparation instructions"""
        
        if peptide_name not in self.base_dosing_protocols:
            return {"error": f"Peptide {peptide_name} not found"}
        
        protocol = self.base_dosing_protocols[peptide_name]
        
        # Calculate volume based on concentration
        if protocol["unit"] == "mcg" and "concentration_mcg_ml" in protocol:
            volume_ml = calculated_dose / protocol["concentration_mcg_ml"]
        elif protocol["unit"] == "mg" and "concentration_mg_ml" in protocol:
            volume_ml = calculated_dose / protocol["concentration_mg_ml"]
        else:
            volume_ml = protocol.get("injection_volume_ml", 0.5)
        
        return {
            "injection_volume_ml": round(volume_ml, 2),
            "needle_size": "27-31 gauge, 0.5 inch",
            "injection_site": "Subcutaneous - abdomen, thigh, or upper arm",
            "preparation": "Allow to reach room temperature before injection",
            "timing": protocol.get("administration_timing", "as directed"),
            "food_interaction": protocol.get("food_interaction", "none")
        }


# Initialize the global dosing calculator
dosing_calculator = PeptideDosingCalculator()