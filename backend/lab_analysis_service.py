"""
Lab Analysis Service for PeptideProtocols.ai
Handles lab file upload, OCR processing, biomarker analysis, and risk assessment
"""

import os
import json
import uuid
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import logging
import base64

logger = logging.getLogger(__name__)

class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"  
    HIGH = "high"
    CRITICAL = "critical"

class LabValueStatus(str, Enum):
    NORMAL = "normal"
    LOW = "low"
    HIGH = "high"
    CRITICAL_LOW = "critical_low"
    CRITICAL_HIGH = "critical_high"

class LabAnalysisService:
    """
    Comprehensive lab analysis service for biomarker interpretation and risk assessment
    """
    
    def __init__(self):
        self.reference_ranges = self._load_reference_ranges()
        self.peptide_interactions = self._load_peptide_lab_interactions()
        
    def _load_reference_ranges(self) -> Dict[str, Dict[str, Any]]:
        """Load standard reference ranges for common biomarkers"""
        return {
            # Metabolic Panel
            "glucose": {
                "unit": "mg/dL",
                "normal_range": [70, 99],
                "high_range": [100, 125],
                "critical_high": 126,
                "interpretation": {
                    "normal": "Optimal glucose metabolism",
                    "high": "Prediabetic range - increased diabetes risk",
                    "critical_high": "Diabetic range - requires medical attention"
                }
            },
            "hemoglobin_a1c": {
                "unit": "%",
                "normal_range": [4.0, 5.6],
                "high_range": [5.7, 6.4],
                "critical_high": 6.5,
                "interpretation": {
                    "normal": "Excellent long-term glucose control",
                    "high": "Prediabetic - lifestyle modifications recommended",
                    "critical_high": "Diabetic - medical management required"
                }
            },
            
            # Lipid Panel
            "total_cholesterol": {
                "unit": "mg/dL",
                "normal_range": [0, 199],
                "high_range": [200, 239],
                "critical_high": 240,
                "interpretation": {
                    "normal": "Optimal cholesterol levels",
                    "high": "Borderline high - dietary changes recommended",
                    "critical_high": "High cholesterol - medical evaluation needed"
                }
            },
            "ldl_cholesterol": {
                "unit": "mg/dL", 
                "normal_range": [0, 99],
                "high_range": [100, 159],
                "critical_high": 160,
                "interpretation": {
                    "normal": "Optimal LDL levels",
                    "high": "Above optimal - cardiovascular risk increased",
                    "critical_high": "High LDL - significant cardiovascular risk"
                }
            },
            "hdl_cholesterol": {
                "unit": "mg/dL",
                "normal_range": [40, 200],  # 40+ for men, 50+ for women
                "low_range": [30, 39],
                "critical_low": 30,
                "interpretation": {
                    "normal": "Protective HDL levels",
                    "low": "Low HDL - increased cardiovascular risk",
                    "critical_low": "Very low HDL - significant cardiovascular risk"
                }
            },
            "triglycerides": {
                "unit": "mg/dL",
                "normal_range": [0, 149],
                "high_range": [150, 199],
                "critical_high": 200,
                "interpretation": {
                    "normal": "Optimal triglyceride levels",
                    "high": "Borderline high triglycerides",
                    "critical_high": "High triglycerides - metabolic risk"
                }
            },
            
            # Thyroid Panel
            "tsh": {
                "unit": "mIU/L",
                "normal_range": [0.4, 4.0],
                "low_range": [0.1, 0.39],
                "high_range": [4.1, 10.0],
                "critical_low": 0.1,
                "critical_high": 10.0,
                "interpretation": {
                    "normal": "Normal thyroid function",
                    "low": "Possible hyperthyroidism",
                    "high": "Possible hypothyroidism",
                    "critical_low": "Severe hyperthyroidism - immediate evaluation",
                    "critical_high": "Severe hypothyroidism - medical attention required"
                }
            },
            "free_t4": {
                "unit": "ng/dL", 
                "normal_range": [0.8, 1.8],
                "low_range": [0.5, 0.79],
                "high_range": [1.81, 3.0],
                "interpretation": {
                    "normal": "Normal T4 levels",
                    "low": "Low T4 - possible hypothyroidism",
                    "high": "High T4 - possible hyperthyroidism"
                }
            },
            "free_t3": {
                "unit": "pg/mL",
                "normal_range": [2.3, 4.2],
                "low_range": [1.5, 2.29],
                "high_range": [4.21, 6.0],
                "interpretation": {
                    "normal": "Normal T3 levels",
                    "low": "Low T3 - possible thyroid dysfunction",
                    "high": "High T3 - possible hyperthyroidism"
                }
            },
            
            # Hormone Panel
            "testosterone_total": {
                "unit": "ng/dL",
                "normal_range_male": [300, 1000],
                "normal_range_female": [15, 70],
                "low_range_male": [200, 299],
                "low_range_female": [8, 14],
                "interpretation": {
                    "normal": "Optimal testosterone levels",
                    "low": "Low testosterone - may benefit from optimization",
                    "critical_low": "Very low testosterone - medical evaluation recommended"
                }
            },
            "testosterone_free": {
                "unit": "pg/mL",
                "normal_range_male": [50, 200],
                "normal_range_female": [1.0, 8.5],
                "interpretation": {
                    "normal": "Normal free testosterone",
                    "low": "Low free testosterone - bioavailable hormone deficient"
                }
            },
            
            # Inflammatory Markers
            "crp": {
                "unit": "mg/L",
                "normal_range": [0, 3.0],
                "high_range": [3.1, 10.0],
                "critical_high": 10.0,
                "interpretation": {
                    "normal": "Low inflammation",
                    "high": "Moderate inflammation - cardiovascular risk",
                    "critical_high": "High inflammation - significant health risk"
                }
            },
            
            # Kidney Function
            "creatinine": {
                "unit": "mg/dL",
                "normal_range": [0.6, 1.2],
                "high_range": [1.3, 2.0],
                "critical_high": 2.0,
                "interpretation": {
                    "normal": "Normal kidney function",
                    "high": "Mild kidney dysfunction",
                    "critical_high": "Significant kidney dysfunction - medical attention"
                }
            },
            "bun": {
                "unit": "mg/dL",
                "normal_range": [7, 20],
                "high_range": [21, 40],
                "critical_high": 40,
                "interpretation": {
                    "normal": "Normal kidney function",
                    "high": "Possible kidney or liver dysfunction",
                    "critical_high": "Significant dysfunction - medical evaluation"
                }
            },
            
            # Liver Function
            "alt": {
                "unit": "U/L",
                "normal_range": [7, 40],
                "high_range": [41, 120],
                "critical_high": 120,
                "interpretation": {
                    "normal": "Normal liver function",
                    "high": "Mild liver dysfunction",
                    "critical_high": "Significant liver damage - medical attention"
                }
            },
            "ast": {
                "unit": "U/L",
                "normal_range": [8, 40],
                "high_range": [41, 120],
                "critical_high": 120,
                "interpretation": {
                    "normal": "Normal liver function",
                    "high": "Possible liver or muscle damage",
                    "critical_high": "Significant damage - immediate evaluation"
                }
            },
            
            # Vitamins & Minerals
            "vitamin_d": {
                "unit": "ng/mL",
                "normal_range": [30, 100],
                "low_range": [20, 29],
                "critical_low": 20,
                "interpretation": {
                    "normal": "Optimal vitamin D levels",
                    "low": "Vitamin D insufficiency",
                    "critical_low": "Vitamin D deficiency - supplementation needed"
                }
            },
            "b12": {
                "unit": "pg/mL",
                "normal_range": [300, 900],
                "low_range": [200, 299],
                "critical_low": 200,
                "interpretation": {
                    "normal": "Adequate B12 levels",
                    "low": "B12 insufficiency - supplementation may help",
                    "critical_low": "B12 deficiency - supplementation required"
                }
            }
        }
    
    def _load_peptide_lab_interactions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load peptide-specific lab considerations and contraindications"""
        return {
            "semaglutide": [
                {
                    "lab": "glucose",
                    "interaction": "Monitor closely - may cause hypoglycemia",
                    "adjustment": "Consider reducing diabetes medications"
                },
                {
                    "lab": "hemoglobin_a1c", 
                    "interaction": "Expect improvement in HbA1c levels",
                    "adjustment": "Monitor for over-correction"
                }
            ],
            "tirzepatide": [
                {
                    "lab": "glucose",
                    "interaction": "Strong glucose-lowering effects",
                    "adjustment": "Reduce diabetes medications by 25-50%"
                },
                {
                    "lab": "triglycerides",
                    "interaction": "May significantly improve triglycerides",
                    "adjustment": "Monitor lipid panels for improvements"
                }
            ],
            "cjc_1295": [
                {
                    "lab": "glucose",
                    "interaction": "Growth hormone may increase insulin resistance",
                    "adjustment": "Monitor glucose levels closely"
                },
                {
                    "lab": "free_t4",
                    "interaction": "May enhance thyroid hormone conversion",
                    "adjustment": "Monitor thyroid function"
                }
            ],
            "bpc_157": [
                {
                    "lab": "crp",
                    "interaction": "May reduce inflammatory markers",
                    "adjustment": "Monitor for improvement in inflammation"
                },
                {
                    "lab": "alt",
                    "interaction": "Hepatoprotective effects may improve liver enzymes", 
                    "adjustment": "Monitor liver function improvements"
                }
            ]
        }
    
    def analyze_lab_value(self, lab_name: str, value: float, gender: str = "male") -> Dict[str, Any]:
        """
        Analyze individual lab value and provide interpretation
        """
        lab_name = lab_name.lower().replace(" ", "_").replace("-", "_")
        
        if lab_name not in self.reference_ranges:
            return {
                "status": "unknown",
                "interpretation": "Reference ranges not available for this lab",
                "risk_level": RiskLevel.LOW
            }
        
        ranges = self.reference_ranges[lab_name]
        
        # Handle gender-specific ranges
        if f"normal_range_{gender}" in ranges:
            normal_range = ranges[f"normal_range_{gender}"]
            low_range = ranges.get(f"low_range_{gender}", [0, normal_range[0]-1])
        else:
            normal_range = ranges["normal_range"]
            low_range = ranges.get("low_range", [0, normal_range[0]-1])
        
        high_range = ranges.get("high_range", [normal_range[1]+1, 999999])
        critical_low = ranges.get("critical_low", 0)
        critical_high = ranges.get("critical_high", 999999)
        
        # Determine status
        if value <= critical_low:
            status = LabValueStatus.CRITICAL_LOW
            risk_level = RiskLevel.CRITICAL
        elif value >= critical_high:
            status = LabValueStatus.CRITICAL_HIGH
            risk_level = RiskLevel.CRITICAL
        elif value < normal_range[0]:
            status = LabValueStatus.LOW
            risk_level = RiskLevel.MODERATE if value < low_range[0] else RiskLevel.LOW
        elif value > normal_range[1]:
            status = LabValueStatus.HIGH
            risk_level = RiskLevel.MODERATE if value > high_range[1] else RiskLevel.LOW
        else:
            status = LabValueStatus.NORMAL
            risk_level = RiskLevel.LOW
        
        # Get interpretation
        interpretation_key = status.value
        if "critical" in status.value:
            interpretation_key = status.value
        elif status == LabValueStatus.LOW:
            interpretation_key = "low"
        elif status == LabValueStatus.HIGH:
            interpretation_key = "high"
        else:
            interpretation_key = "normal"
        
        interpretation = ranges["interpretation"].get(interpretation_key, "Value assessed")
        
        return {
            "lab_name": lab_name,
            "value": value,
            "unit": ranges.get("unit", ""),
            "status": status,
            "risk_level": risk_level,
            "interpretation": interpretation,
            "normal_range": normal_range,
            "reference_info": {
                "normal": normal_range,
                "low_concern": low_range if "low_range" in ranges else None,
                "high_concern": high_range if "high_range" in ranges else None
            }
        }
    
    def analyze_full_panel(self, lab_data: Dict[str, float], patient_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze complete lab panel and provide comprehensive assessment
        """
        gender = patient_info.get("gender", "male").lower()
        age = int(patient_info.get("age", 35))
        
        analyzed_labs = {}
        risk_factors = []
        recommendations = []
        peptide_considerations = []
        
        # Analyze each lab value
        for lab_name, value in lab_data.items():
            analysis = self.analyze_lab_value(lab_name, value, gender)
            analyzed_labs[lab_name] = analysis
            
            # Collect risk factors
            if analysis["risk_level"] in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                risk_factors.append({
                    "lab": lab_name,
                    "issue": analysis["interpretation"],
                    "risk_level": analysis["risk_level"]
                })
        
        # Generate specific recommendations
        recommendations = self._generate_recommendations(analyzed_labs, patient_info)
        
        # Assess peptide considerations
        peptide_considerations = self._assess_peptide_safety(analyzed_labs)
        
        # Calculate overall risk score
        overall_risk = self._calculate_overall_risk(analyzed_labs)
        
        return {
            "analysis_id": str(uuid.uuid4()),
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "patient_info": patient_info,
            "lab_results": analyzed_labs,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "peptide_considerations": peptide_considerations,
            "overall_risk": overall_risk,
            "summary": self._generate_summary(analyzed_labs, risk_factors)
        }
    
    def _generate_recommendations(self, analyzed_labs: Dict[str, Any], patient_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations based on lab results"""
        recommendations = []
        
        for lab_name, analysis in analyzed_labs.items():
            if analysis["risk_level"] in [RiskLevel.MODERATE, RiskLevel.HIGH, RiskLevel.CRITICAL]:
                # Glucose recommendations - handle both HIGH and CRITICAL_HIGH
                if lab_name == "glucose" and analysis["status"] in [LabValueStatus.HIGH, LabValueStatus.CRITICAL_HIGH]:
                    priority = "critical" if analysis["status"] == LabValueStatus.CRITICAL_HIGH else "high"
                    recommendations.append({
                        "category": "metabolic",
                        "priority": priority,
                        "recommendation": "Consider metabolic peptides like semaglutide or tirzepatide for glucose optimization",
                        "rationale": "Elevated glucose indicates insulin resistance - GLP-1 agonists highly effective"
                    })
                
                # Testosterone recommendations - handle both LOW and CRITICAL_LOW
                elif lab_name == "testosterone_total" and analysis["status"] in [LabValueStatus.LOW, LabValueStatus.CRITICAL_LOW]:
                    priority = "high" if analysis["status"] == LabValueStatus.CRITICAL_LOW else "moderate"
                    recommendations.append({
                        "category": "hormonal",
                        "priority": priority,
                        "recommendation": "Testosterone optimization may be beneficial - consider comprehensive hormone panel",
                        "rationale": "Low testosterone affects energy, muscle mass, and overall vitality"
                    })
                
                # Vitamin D recommendations - handle both LOW and CRITICAL_LOW
                elif lab_name == "vitamin_d" and analysis["status"] in [LabValueStatus.LOW, LabValueStatus.CRITICAL_LOW]:
                    priority = "high" if analysis["status"] == LabValueStatus.CRITICAL_LOW else "moderate"
                    recommendations.append({
                        "category": "nutritional",
                        "priority": priority, 
                        "recommendation": "Vitamin D3 supplementation (2000-5000 IU daily) recommended",
                        "rationale": "Vitamin D deficiency affects immune function and bone health"
                    })
                
                # CRP recommendations - handle both HIGH and CRITICAL_HIGH
                elif lab_name == "crp" and analysis["status"] in [LabValueStatus.HIGH, LabValueStatus.CRITICAL_HIGH]:
                    priority = "critical" if analysis["status"] == LabValueStatus.CRITICAL_HIGH else "high"
                    recommendations.append({
                        "category": "inflammatory",
                        "priority": priority,
                        "recommendation": "Consider anti-inflammatory peptides like BPC-157 and lifestyle modifications",
                        "rationale": "Elevated CRP indicates systemic inflammation - addressing root cause critical"
                    })
                
                # Hemoglobin A1C recommendations - handle both HIGH and CRITICAL_HIGH
                elif lab_name == "hemoglobin_a1c" and analysis["status"] in [LabValueStatus.HIGH, LabValueStatus.CRITICAL_HIGH]:
                    priority = "critical" if analysis["status"] == LabValueStatus.CRITICAL_HIGH else "high"
                    recommendations.append({
                        "category": "metabolic",
                        "priority": priority,
                        "recommendation": "Diabetes management protocol needed - consider GLP-1 agonists and lifestyle interventions",
                        "rationale": "Elevated HbA1c indicates poor glucose control over 2-3 months"
                    })
                
                # Total Cholesterol recommendations - handle both HIGH and CRITICAL_HIGH
                elif lab_name == "total_cholesterol" and analysis["status"] in [LabValueStatus.HIGH, LabValueStatus.CRITICAL_HIGH]:
                    priority = "high" if analysis["status"] == LabValueStatus.CRITICAL_HIGH else "moderate"
                    recommendations.append({
                        "category": "cardiovascular",
                        "priority": priority,
                        "recommendation": "Cardiovascular risk reduction - consider lifestyle modifications and lipid management",
                        "rationale": "Elevated cholesterol increases cardiovascular disease risk"
                    })
        
        return recommendations
    
    def _assess_peptide_safety(self, analyzed_labs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess safety considerations for peptide therapy based on lab results"""
        considerations = []
        
        # Check for diabetes-related peptide considerations
        if "glucose" in analyzed_labs or "hemoglobin_a1c" in analyzed_labs:
            glucose_analysis = analyzed_labs.get("glucose", {})
            if glucose_analysis.get("status") in [LabValueStatus.HIGH, LabValueStatus.CRITICAL_HIGH]:
                considerations.append({
                    "peptide_class": "GLP-1 agonists",
                    "consideration": "Excellent candidates - may provide significant glucose improvement",
                    "monitoring": "Monitor glucose levels closely during initiation"
                })
        
        # Check liver function for hepatotoxic concerns
        alt_analysis = analyzed_labs.get("alt", {})
        ast_analysis = analyzed_labs.get("ast", {})
        if (alt_analysis.get("status") == LabValueStatus.HIGH or 
            ast_analysis.get("status") == LabValueStatus.HIGH):
            considerations.append({
                "peptide_class": "Growth hormone peptides",
                "consideration": "Use with caution - monitor liver function closely",
                "monitoring": "Repeat liver function tests in 4-6 weeks"
            })
        
        # Check kidney function
        creatinine_analysis = analyzed_labs.get("creatinine", {})
        if creatinine_analysis.get("status") in [LabValueStatus.HIGH, LabValueStatus.CRITICAL_HIGH]:
            considerations.append({
                "peptide_class": "All peptides",
                "consideration": "Kidney function impaired - adjust dosing and monitor closely",
                "monitoring": "Nephrology consultation recommended"
            })
        
        return considerations
    
    def _calculate_overall_risk(self, analyzed_labs: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall health risk based on lab results"""
        risk_score = 0
        critical_count = 0
        high_count = 0
        moderate_count = 0
        
        for analysis in analyzed_labs.values():
            if analysis["risk_level"] == RiskLevel.CRITICAL:
                critical_count += 1
                risk_score += 4
            elif analysis["risk_level"] == RiskLevel.HIGH:
                high_count += 1
                risk_score += 3
            elif analysis["risk_level"] == RiskLevel.MODERATE:
                moderate_count += 1
                risk_score += 2
        
        total_labs = len(analyzed_labs)
        normalized_score = (risk_score / (total_labs * 4)) * 100 if total_labs > 0 else 0
        
        if critical_count > 0:
            overall_level = RiskLevel.CRITICAL
        elif normalized_score > 60:
            overall_level = RiskLevel.HIGH
        elif normalized_score > 30:
            overall_level = RiskLevel.MODERATE
        else:
            overall_level = RiskLevel.LOW
        
        return {
            "overall_risk_level": overall_level,
            "risk_score": round(normalized_score, 1),
            "critical_findings": critical_count,
            "high_risk_findings": high_count,
            "moderate_risk_findings": moderate_count,
            "total_labs_analyzed": total_labs
        }
    
    def _generate_summary(self, analyzed_labs: Dict[str, Any], risk_factors: List[Dict[str, Any]]) -> str:
        """Generate a concise summary of lab analysis"""
        if not risk_factors:
            return "Lab results show no significant abnormalities. Continue current health optimization strategies."
        
        high_risk_count = len([r for r in risk_factors if r["risk_level"] == RiskLevel.CRITICAL])
        moderate_risk_count = len([r for r in risk_factors if r["risk_level"] in [RiskLevel.HIGH, RiskLevel.MODERATE]])
        
        if high_risk_count > 0:
            return f"Critical findings identified in {high_risk_count} lab value(s). Immediate medical attention recommended. Additional {moderate_risk_count} findings require monitoring and intervention."
        elif moderate_risk_count > 0:
            return f"{moderate_risk_count} lab value(s) outside optimal ranges. Targeted interventions recommended to optimize health and reduce long-term risk."
        else:
            return "Minor lab variations noted. Overall health status good with room for optimization."
    
    def extract_lab_data_from_text(self, text_content: str) -> Dict[str, float]:
        """
        Extract lab values from text content using pattern matching
        Basic implementation - in production would use more sophisticated NLP/ML
        """
        extracted_labs = {}
        
        # Common lab value patterns
        patterns = {
            "glucose": r"glucose[:\s]+(\d+(?:\.\d+)?)",
            "hemoglobin_a1c": r"(?:hemoglobin\s+a1c|hba1c|a1c)[:\s]+(\d+(?:\.\d+)?)",
            "total_cholesterol": r"(?:total\s+cholesterol|cholesterol)[:\s]+(\d+(?:\.\d+)?)",
            "ldl_cholesterol": r"ldl[:\s]+(\d+(?:\.\d+)?)",
            "hdl_cholesterol": r"hdl[:\s]+(\d+(?:\.\d+)?)",
            "triglycerides": r"triglycerides?[:\s]+(\d+(?:\.\d+)?)",
            "tsh": r"tsh[:\s]+(\d+(?:\.\d+)?)",
            "free_t4": r"(?:free\s+t4|ft4)[:\s]+(\d+(?:\.\d+)?)",
            "free_t3": r"(?:free\s+t3|ft3)[:\s]+(\d+(?:\.\d+)?)",
            "testosterone_total": r"(?:total\s+testosterone|testosterone)[:\s]+(\d+(?:\.\d+)?)",
            "crp": r"(?:c-reactive\s+protein|crp)[:\s]+(\d+(?:\.\d+)?)",
            "vitamin_d": r"(?:vitamin\s+d|25-oh\s+vitamin\s+d)[:\s]+(\d+(?:\.\d+)?)",
            "creatinine": r"creatinine[:\s]+(\d+(?:\.\d+)?)",
            "alt": r"alt[:\s]+(\d+(?:\.\d+)?)",
            "ast": r"ast[:\s]+(\d+(?:\.\d+)?)"
        }
        
        text_lower = text_content.lower()
        
        for lab_name, pattern in patterns.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                try:
                    extracted_labs[lab_name] = float(matches[0])
                except ValueError:
                    continue
        
        return extracted_labs
    
    def save_lab_analysis(self, analysis_data: Dict[str, Any]) -> str:
        """Save lab analysis results to storage"""
        analysis_id = analysis_data["analysis_id"]
        storage_path = f"/app/backend/lab_analyses/{analysis_id}.json"
        
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        with open(storage_path, 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
        
        logger.info(f"Lab analysis {analysis_id} saved successfully")
        return analysis_id

# Global service instance
lab_analysis_service = LabAnalysisService()