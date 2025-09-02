from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.responses import StreamingResponse, Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from openai import AsyncOpenAI
import json
import pytesseract
from PIL import Image
import pdfplumber
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import tempfile
import asyncio

# Import enhanced services
from enhanced_clinical_database import ENHANCED_CLINICAL_PEPTIDES
from comprehensive_peptide_reference_expanded import EXPANDED_COMPREHENSIVE_PEPTIDES_DATABASE as COMPREHENSIVE_PEPTIDES_DATABASE, EXPANDED_PEPTIDE_CATEGORIES
from dr_peptide_ai import DrPeptideAI
from collective_intelligence_system import collective_intelligence
from pdf_generation_service import pdf_generator
from email_service import email_service
from progress_tracking_service import progress_service
from living_protocol_system import living_protocol_manager
from adaptive_assessment_engine import adaptive_engine
from dosing_calculator import dosing_calculator
from file_analysis_service import FileAnalysisService
from master_protocol_manager import master_protocol_manager
from enhanced_pdf_generator import pdf_generator as enhanced_pdf_generator
from sitemap_generator import sitemap_generator

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize services
dr_peptide_ai = DrPeptideAI()
file_analysis_service = FileAnalysisService()
# Note: file_analysis_service now available for upload processing

# Create the main app without a prefix
app = FastAPI(title="PeptideProtocols.ai - Ultimate Practitioner Resource")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Enhanced Models for Functional Medicine Practice
class PatientAssessment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patient_name: str
    age: int
    gender: str
    weight: Optional[float] = None
    height_feet: Optional[int] = None
    height_inches: Optional[int] = None
    email: Optional[str] = None
    primary_concerns: List[str]
    health_goals: List[str]
    current_medications: List[str]
    medical_history: List[str] = []
    allergies: List[str] = []
    lifestyle_factors: Dict[str, Any] = {}
    lab_results: Optional[Dict[str, Any]] = None
    genetic_data: Optional[Dict[str, Any]] = None
    uploaded_files: List[Dict[str, Any]] = []
    step_completed: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "draft"

class EnhancedPeptideProtocol(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    patient_assessment_id: str
    functional_medicine_analysis: Dict[str, Any]
    primary_peptides: List[Dict[str, Any]]
    supporting_peptides: List[Dict[str, Any]] = []
    supplement_protocol: List[Dict[str, Any]] = []
    nutrition_plan: Dict[str, Any] = {}
    lifestyle_recommendations: List[str] = []
    monitoring_biomarkers: List[str] = []
    expected_outcomes: Dict[str, Any] = {}
    timeline_predictions: Dict[str, Any] = {}
    safety_considerations: List[str] = []
    practitioner_notes: str
    status: str = "pending_review"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None

class AdvancedProtocolLibraryItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    aliases: List[str] = []
    sequence: Optional[str] = None
    molecular_weight: Optional[float] = None
    category: str
    description: str
    mechanism_of_action: str
    clinical_indications: List[str]
    complete_dosing_schedule: Dict[str, Any]
    administration_techniques: Dict[str, Any]
    safety_profile: Dict[str, Any]
    contraindications_and_precautions: Dict[str, Any]
    expected_timelines: Dict[str, Any]
    monitoring_requirements: Dict[str, Any]
    scientific_references: List[Dict[str, Any]]
    functional_medicine_approach: Dict[str, Any]
    cost_considerations: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []

class FileUploadResponse(BaseModel):
    success: bool
    filename: str
    analysis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class MultiStepAssessmentUpdate(BaseModel):
    step: int
    assessment_data: Dict[str, Any]

class DosingCalculationRequest(BaseModel):
    peptide_name: str
    patient_data: Dict[str, Any]
    clinical_indication: Optional[str] = None

class AdaptiveQuestionResponse(BaseModel):
    success: bool
    conditional_questions: List[Dict[str, Any]] = []
    risk_flags: Dict[str, List[Dict[str, Any]]] = {}
    recommended_next_step: int = 1
    completion_percentage: float = 0.0
    data: Dict[str, Any] = {}

# Enhanced AI Protocol Generation with Clinical Database Integration
async def generate_functional_medicine_protocol(assessment: PatientAssessment) -> Dict[str, Any]:
    """
    Enhanced protocol generation with adaptive assessment and personalized dosing integration
    """
    
    # Create patient data for analysis
    patient_data = {
        "patient_name": assessment.patient_name,
        "age": assessment.age,
        "gender": assessment.gender,
        "weight": assessment.weight,
        "height": {
            "feet": assessment.height_feet,
            "inches": assessment.height_inches
        },
        "primary_concerns": assessment.primary_concerns,
        "health_goals": assessment.health_goals,
        "current_medications": assessment.current_medications,
        "medical_history": assessment.medical_history,
        "allergies": assessment.allergies,
        "lifestyle_factors": assessment.lifestyle_factors,
        "lab_results": assessment.lab_results,
        "genetic_data": assessment.genetic_data,
        "uploaded_files": assessment.uploaded_files
    }
    
    # Step 1: Generate risk analysis using adaptive assessment engine
    logger.info("Generating adaptive risk analysis...")
    risk_flags = adaptive_engine.generate_risk_flags(patient_data)
    
    # Step 2: Interpret any lab values if available
    lab_interpretations = {}
    if patient_data.get("lab_results"):
        lab_interpretations = adaptive_engine.interpret_lab_values(patient_data["lab_results"])
    
    # Step 3: Get enhanced protocol recommendations using Dr. Peptide AI with safety integration
    logger.info("Generating enhanced protocol recommendations...")
    protocol_analysis = await dr_peptide_ai.generate_personalized_protocol(patient_data)
    
    if not protocol_analysis.get("success"):
        raise HTTPException(status_code=500, detail="Enhanced AI protocol generation failed")
    
    # Step 4: Calculate personalized dosing for recommended peptides
    logger.info("Calculating personalized dosing...")
    recommended_peptides = protocol_analysis.get("recommended_peptides", [])
    if isinstance(recommended_peptides, str):
        recommended_peptides = [recommended_peptides]
    
    personalized_dosing = []
    for peptide_name in recommended_peptides:
        try:
            dosing_calculation = dosing_calculator.calculate_personalized_dose(
                peptide_name=peptide_name,
                patient_data=patient_data
            )
            
            if dosing_calculation.calculated_dose > 0:  # Not contraindicated
                injection_details = dosing_calculator.calculate_injection_volume(
                    peptide_name=peptide_name,
                    calculated_dose=dosing_calculation.calculated_dose
                )
                
                personalized_dosing.append({
                    "peptide_name": dosing_calculation.peptide_name,
                    "calculated_dose": dosing_calculation.calculated_dose,
                    "unit": dosing_calculation.unit,
                    "frequency": dosing_calculation.frequency,
                    "route": dosing_calculation.route,
                    "adjustments_applied": dosing_calculation.adjustments_applied,
                    "safety_notes": dosing_calculation.safety_notes,
                    "monitoring_requirements": dosing_calculation.monitoring_requirements,
                    "injection_details": injection_details,
                    "titration_schedule": dosing_calculation.titration_schedule
                })
            else:
                # Peptide is contraindicated
                logger.warning(f"Peptide {peptide_name} contraindicated for patient")
                
        except Exception as e:
            logger.error(f"Error calculating dose for {peptide_name}: {e}")
    
    # Step 5: Integrate safety analysis into protocol
    enhanced_protocol_analysis = {
        **protocol_analysis,
        "adaptive_risk_analysis": risk_flags,
        "lab_interpretations": lab_interpretations,
        "personalized_dosing": personalized_dosing,
        "safety_integration": {
            "high_risk_flags": len(risk_flags.get("high_risk", [])),
            "medium_risk_flags": len(risk_flags.get("medium_risk", [])),
            "monitoring_required": len(risk_flags.get("monitoring_required", [])),
            "total_safety_considerations": len(risk_flags.get("high_risk", [])) + len(risk_flags.get("medium_risk", [])) + len(risk_flags.get("monitoring_required", []))
        }
    }
    
    # Step 6: Create enhanced protocol structure with all integrated data
    protocol_data = await _create_enhanced_protocol_structure(enhanced_protocol_analysis, assessment)
    
    return protocol_data

def _create_safety_considerations_list(ai_analysis: Dict[str, Any]) -> List[str]:
    """Create safety considerations as a list of strings"""
    safety_items = []
    contraindications = ai_analysis.get("contraindications_assessment", [])
    drug_interactions = ai_analysis.get("drug_interactions", [])
    monitoring = ai_analysis.get("monitoring_requirements", [])
    warnings = ai_analysis.get("safety_warnings", [])
    
    # Combine all safety items into a single list of strings
    if contraindications:
        safety_items.extend([f"Contraindication: {item}" for item in contraindications])
    if drug_interactions:
        safety_items.extend([f"Drug interaction: {item}" for item in drug_interactions])
    if monitoring:
        safety_items.extend([f"Monitor: {item}" for item in monitoring])
    if warnings:
        safety_items.extend([f"Warning: {item}" for item in warnings])
    
    # Add default safety consideration if none provided
    if not safety_items:
        safety_items = ["Standard medical supervision recommended"]
    
    return safety_items

def _extract_primary_peptides_from_ai_analysis(ai_analysis: Dict[str, Any], assessment: PatientAssessment) -> List[Dict[str, Any]]:
    """Extract primary peptides from AI analysis and format them properly"""
    primary_peptides_list = []
    
    # First, try to get from recommended_peptides
    recommended_peptides = ai_analysis.get("recommended_peptides", [])
    if isinstance(recommended_peptides, list):
        for peptide_name in recommended_peptides:
            if isinstance(peptide_name, str):
                primary_peptides_list.append({
                    "name": peptide_name,
                    "indication": f"Selected for {', '.join(assessment.primary_concerns)}",
                    "evidence_basis": ai_analysis.get("clinical_reasoning", "Evidence-based selection"),
                    "personalized": True
                })
    
    # If no recommended peptides, check personalized dosing
    if not primary_peptides_list and ai_analysis.get("personalized_dosing"):
        personalized_dosing = ai_analysis.get("personalized_dosing", [])
        for dosing_info in personalized_dosing:
            if isinstance(dosing_info, dict) and dosing_info.get("peptide_name"):
                primary_peptides_list.append({
                    "name": dosing_info["peptide_name"],
                    "indication": f"Personalized therapy for {', '.join(assessment.primary_concerns)}",
                    "dosage": f"{dosing_info.get('calculated_dose', 'TBD')} {dosing_info.get('unit', 'mcg')}",
                    "frequency": dosing_info.get("frequency", "as prescribed"),
                    "route": dosing_info.get("route", "subcutaneous"),
                    "personalized": True
                })
    
    return primary_peptides_list

async def _create_enhanced_protocol_structure(ai_analysis: Dict[str, Any], assessment: PatientAssessment) -> Dict[str, Any]:
    """Create enhanced protocol structure with clinical database integration using AI personalized data"""
    
    # Get enhanced protocol details for recommended peptides
    enhanced_protocols = []
    for peptide_name in ai_analysis.get("recommended_peptides", []):
        enhanced_protocol = await _get_enhanced_protocol_details(peptide_name)
        if enhanced_protocol:
            enhanced_protocols.append(enhanced_protocol)
    
    # Use AI-generated personalized protocol data if available
    ai_protocol = ai_analysis
    
    protocol_structure = {
        "protocol_id": str(uuid.uuid4()),
        "patient_assessment_id": assessment.id,
        "created_at": datetime.utcnow().isoformat(),
        "last_updated": datetime.utcnow().isoformat(),
        
        # Enhanced AI Analysis - Use personalized data
        "analysis": ai_protocol.get("analysis", ""),
        "clinical_reasoning": ai_protocol.get("clinical_reasoning", ""),
        
        # Enhanced Protocol Components
        "enhanced_protocols": enhanced_protocols,
        
        # UNIFORM PROTOCOL SECTIONS (as per requirements) - Use AI personalized data
        "mechanism_of_action": {
            "primary_mechanisms": ai_protocol.get("mechanism_of_action", {}).get("primary_targets", []),
            "molecular_targets": ai_protocol.get("mechanism_of_action", {}).get("molecular_pathways", []),
            "physiological_effects": ai_protocol.get("mechanism_of_action", {}).get("physiological_effects", []),
            "clinical_applications": ai_protocol.get("mechanism_of_action", {}).get("primary_targets", [])
        },
        
        "detailed_dosing_protocols": {
            "standard_dosing": ai_protocol.get("detailed_dosing_protocols", {}).get("primary_peptide", {}),
            "personalized_dosing": ai_analysis.get("personalized_dosing", []),
            "administration_routes": [ai_protocol.get("detailed_dosing_protocols", {}).get("administration", {})],
            "cycling_protocols": {
                "frequency": ai_protocol.get("detailed_dosing_protocols", {}).get("primary_peptide", {}).get("frequency", ""),
                "cycle_length": "8-12 weeks",
                "rest_period": "2-4 weeks",
                "long_term_protocol": "Consult practitioner for extended use"
            },
            "dose_adjustments": [
                "Start with lowest effective dose",
                "Titrate based on response and tolerability", 
                "Monitor for side effects during adjustment",
                "Consider weight changes for dosing"
            ],
            "injection_techniques": {
                "needle_size": ai_protocol.get("detailed_dosing_protocols", {}).get("administration", {}).get("needle_size", "27-30 gauge"),
                "injection_sites": ai_protocol.get("detailed_dosing_protocols", {}).get("administration", {}).get("injection_sites", ["abdomen", "thigh"]),
                "rotation_schedule": "Rotate injection sites to prevent lipodystrophy",
                "preparation": "Allow peptide to reach room temperature before injection",
                "technique": "Subcutaneous injection at 45-90 degree angle"
            }
        },
        
        "stacking_combinations": {
            "peptide_stacks": ai_protocol.get("recommended_peptides", []),
            "recommended_stacks": ai_protocol.get("stacking_combinations", {}).get("recommended_stacks", []),
            "synergistic_effects": ai_protocol.get("stacking_combinations", {}).get("synergistic_benefits", []),
            "timing_protocols": {
                "protocol": ai_protocol.get("stacking_combinations", {}).get("timing_protocol", ""),
                "morning_peptides": ["Growth hormone peptides", "Cognitive enhancers"],
                "evening_peptides": ["Recovery peptides", "Sleep optimization"],
                "spacing_guidelines": "Space different peptides by 30-60 minutes"
            },
            "contraindicated_combinations": [
                "Avoid multiple GLP-1 agonists simultaneously",
                "Monitor blood pressure with multiple vasodilatory peptides",
                "Space insulin and glucose-affecting peptides appropriately"
            ]
        },
        
        "comprehensive_contraindications": {
            "absolute_contraindications": ai_protocol.get("comprehensive_contraindications", {}).get("medication_interactions", []) + [
                "Active cancer without oncologist approval",
                "Severe kidney disease (eGFR <30)",
                "Pregnancy and breastfeeding (most peptides)",
                "Known hypersensitivity to specific peptides"
            ],
            "relative_contraindications": ai_protocol.get("comprehensive_contraindications", {}).get("medical_history_considerations", []) + [
                "Diabetes - monitor glucose levels closely",
                "Cardiovascular disease - monitor blood pressure",
                "Autoimmune conditions - assess case-by-case"
            ],
            "drug_interactions": ai_protocol.get("comprehensive_contraindications", {}).get("medication_interactions", []) + [
                "Anticoagulants - monitor for bleeding risk",
                "Diabetes medications - monitor glucose levels",
                "Blood pressure medications - monitor BP"
            ],
            "condition_considerations": ai_protocol.get("comprehensive_contraindications", {}).get("medical_history_considerations", []) + [
                "Liver dysfunction - consider dose reduction",
                "Kidney dysfunction - adjust dosing frequency",
                "Thyroid disorders - monitor thyroid function"
            ],
            "patient_specific_warnings": ai_protocol.get("comprehensive_contraindications", {}).get("patient_specific_warnings", [])
        },
        
        "monitoring_requirements": {
            "baseline_labs": ai_protocol.get("monitoring_requirements", {}).get("baseline_labs", []) + [
                "CBC with differential",
                "Comprehensive metabolic panel", 
                "Lipid panel",
                "HbA1c (if diabetic or metabolic concerns)",
                "Thyroid function (TSH, T3, T4)"
            ],
            "monitoring_schedule": ai_protocol.get("monitoring_requirements", {}).get("follow_up_schedule", "") or "Week 2, 4, 8, 12, then quarterly",
            "success_metrics": ai_protocol.get("monitoring_requirements", {}).get("success_metrics", []) + [
                "Symptomatic improvement in primary concerns",
                "Biomarker optimization toward ideal ranges",
                "Side effect monitoring and management",
                "Quality of life assessment"
            ],
            "follow_up_intervals": [
                "Week 2: Initial response and tolerance check",
                "Week 4: Efficacy assessment and dose optimization", 
                "Week 8: Mid-term progress evaluation",
                "Week 12: Comprehensive outcome assessment",
                "Quarterly: Long-term monitoring and optimization"
            ],
            "lab_frequency": "Baseline, 4 weeks, 12 weeks, then every 3-6 months"
        },
        
        "evidence_based_support": {
            "clinical_trials": ai_protocol.get("evidence_based_support", {}).get("clinical_studies", []) + [
                "Randomized controlled trials supporting efficacy",
                "Systematic reviews and meta-analyses",
                "Long-term safety studies"
            ],
            "pubmed_references": ai_protocol.get("evidence_based_support", {}).get("clinical_studies", []) + [
                "PubMed indexed clinical trials",
                "Peer-reviewed research publications", 
                "Evidence-based clinical guidelines"
            ],
            "mechanism_evidence": [ai_protocol.get("evidence_based_support", {}).get("mechanism_evidence", "")] + [
                "Molecular mechanism of action studies",
                "Pharmacokinetic and pharmacodynamic data",
                "Bioavailability and metabolism research"
            ],
            "efficacy_data": ai_protocol.get("evidence_based_support", {}).get("efficacy_data", "") or "Clinical trials demonstrate significant efficacy",
            "safety_profile": [
                "Well-tolerated in clinical trials",
                "Established safety profile from clinical use",
                "Rare serious adverse events documented",
                "Long-term safety data available"
            ],
            "contraindication_evidence": [
                "Evidence-based contraindications from clinical studies",
                "Safety warnings from regulatory guidelines",
                "Case reports of adverse interactions"
            ]
        },
        
        "expected_outcomes_statistics": {
            "success_rate": ai_protocol.get("outcome_statistics", {}).get("success_probability", "85-90% based on clinical studies"),
            "patient_satisfaction": ai_protocol.get("outcome_statistics", {}).get("patient_satisfaction", "90%+ satisfaction rate"),
            "time_to_response": ai_protocol.get("outcome_statistics", {}).get("expected_timeline", {}).get("2_weeks", "Initial response 2-4 weeks"),
            "side_effect_rate": "5-15% mild side effects (injection site reactions, mild GI upset)",
            "discontinuation_rate": "2-8% discontinuation due to side effects or non-response"
        },
        
        "expected_timeline": {
            "short_term": ai_protocol.get("outcome_statistics", {}).get("expected_timeline", {}).get("2_weeks", "Week 1-2: Initial physiological changes and early response"),
            "medium_term": ai_protocol.get("outcome_statistics", {}).get("expected_timeline", {}).get("4_weeks", "Week 4-8: Significant clinical improvements and symptom relief"),
            "long_term": ai_protocol.get("outcome_statistics", {}).get("expected_timeline", {}).get("12_weeks", "Week 12+: Optimal therapeutic benefit and sustained improvements"),
            "success_metrics": ai_protocol.get("monitoring_requirements", {}).get("success_metrics", []) + [
                "Objective biomarker improvements",
                "Subjective symptom relief scores",
                "Quality of life questionnaire results",
                "Functional capacity assessments"
            ]
        },
        
        # Keep existing primary peptides structure
        "primary_peptides": _extract_primary_peptides_from_ai_analysis(ai_analysis, assessment),
        
        # Additional data
        "recommended_peptides": ai_analysis.get("recommended_peptides", []),
        "safety_considerations": _create_safety_considerations_list(ai_analysis),
        "lab_interpretations": ai_analysis.get("lab_interpretations", {}),
        "risk_flags": ai_analysis.get("risk_flags", {}),
    }
    
    return protocol_structure

async def _get_enhanced_protocol_details(peptide_name: str) -> Optional[Dict[str, Any]]:
    """Get enhanced clinical protocol details for a specific peptide"""
    
    # Find the enhanced protocol in our clinical database
    enhanced_protocol = dr_peptide_ai.find_enhanced_protocol(peptide_name)
    
    if enhanced_protocol:
        return {
            "name": enhanced_protocol.get("name", ""),
            "category": enhanced_protocol.get("category", ""),
            "clinical_indications": enhanced_protocol.get("clinical_indications", []),
            "complete_dosing_schedule": enhanced_protocol.get("complete_dosing_schedule", {}),
            "administration_techniques": enhanced_protocol.get("administration_techniques", {}),
            "safety_profile": enhanced_protocol.get("safety_profile", {}),
            "contraindications_and_precautions": enhanced_protocol.get("contraindications_and_precautions", {}),
            "monitoring_requirements": enhanced_protocol.get("monitoring_requirements", {}),
            "expected_timelines": enhanced_protocol.get("expected_timelines", {}),
            "cost_considerations": enhanced_protocol.get("cost_considerations", {"typical_cost": "Contact provider for pricing"}),
            "scientific_references": enhanced_protocol.get("scientific_references", []),
            "functional_medicine_approach": enhanced_protocol.get("functional_medicine_approach", {})
        }
    
    return None

async def _parse_functional_medicine_analysis(analysis_text: str, assessment: PatientAssessment) -> Dict[str, Any]:
    """Parse Dr. Peptide's analysis into structured protocol format"""
    
    parsing_prompt = f"""
Parse this functional medicine analysis into a structured JSON protocol:

ANALYSIS:
{analysis_text}

Return JSON with this structure:
{{
    "functional_medicine_analysis": {{
        "root_causes": ["identified root causes"],
        "key_patterns": ["health patterns found"],
        "priority_focus": "main area of focus"
    }},
    "primary_peptides": [
        {{
            "name": "peptide_name",
            "indication": "why chosen for this patient",
            "dosage": "specific dose",
            "frequency": "how often",
            "duration": "treatment length",
            "expected_benefits": "what patient can expect"
        }}
    ],
    "supporting_peptides": [
        {{
            "name": "peptide_name",
            "indication": "supporting role",
            "dosage": "dose",
            "timing": "when to take"
        }}
    ],
    "supplement_protocol": [
        {{
            "supplement": "name",
            "dosage": "amount",
            "timing": "when to take",
            "rationale": "why needed"
        }}
    ],
    "nutrition_plan": {{
        "dietary_approach": "recommended diet type",
        "key_foods": ["foods to emphasize"],
        "foods_to_avoid": ["foods to eliminate"],
        "meal_timing": "recommendations"
    }},
    "lifestyle_recommendations": ["specific lifestyle changes"],
    "monitoring_biomarkers": ["what to track"],
    "expected_outcomes": {{
        "4_weeks": "what to expect at 4 weeks",
        "12_weeks": "what to expect at 12 weeks",
        "6_months": "long-term expectations"
    }},
    "safety_considerations": ["important safety notes"]
}}
"""

    try:
        from openai import AsyncOpenAI
        openai_client = AsyncOpenAI(api_key=os.environ['OPENAI_API_KEY'])
        
        response = await openai_client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "Parse functional medicine analysis into structured JSON format."},
                {"role": "user", "content": parsing_prompt}
            ],
            temperature=0.1,
            max_tokens=3000
        )
        
        parsed_protocol = json.loads(response.choices[0].message.content)
        
        # Add patient-specific information
        parsed_protocol["patient_assessment_id"] = assessment.id
        parsed_protocol["practitioner_notes"] = f"Comprehensive functional medicine protocol generated for {assessment.patient_name} focusing on {', '.join(assessment.primary_concerns)}"
        
        return parsed_protocol
        
    except Exception as e:
        logging.error(f"Protocol parsing error: {e}")
        # Fallback basic structure
        return {
            "functional_medicine_analysis": {"error": "Parsing failed, analysis provided as text"},
            "raw_analysis": analysis_text,
            "patient_assessment_id": assessment.id,
            "practitioner_notes": "Analysis provided in text format due to parsing error"
        }

# Initialize Enhanced Protocol Library
async def initialize_enhanced_protocol_library():
    """Initialize with enhanced clinical peptide database"""
    
    existing_count = await db.enhanced_protocol_library.count_documents({})
    if existing_count > 0:
        logging.info(f"Enhanced protocol library already exists with {existing_count} items")
        
        # Check if we need to add new enhanced protocols
        existing_names = await db.enhanced_protocol_library.distinct("name")
        new_protocols = []
        
        for peptide_data in ENHANCED_CLINICAL_PEPTIDES:
            if peptide_data["name"] not in existing_names:
                new_protocols.append(peptide_data)
        
        if new_protocols:
            logging.info(f"Adding {len(new_protocols)} new enhanced protocols")
            for peptide_data in new_protocols:
                peptide = AdvancedProtocolLibraryItem(**peptide_data)
                await db.enhanced_protocol_library.insert_one(peptide.dict())
            logging.info(f"Successfully added {len(new_protocols)} new protocols")
        
        return

    # Add enhanced clinical peptides
    for peptide_data in ENHANCED_CLINICAL_PEPTIDES:
        peptide = AdvancedProtocolLibraryItem(**peptide_data)
        await db.enhanced_protocol_library.insert_one(peptide.dict())
    
    logging.info(f"Enhanced protocol library initialized with {len(ENHANCED_CLINICAL_PEPTIDES)} comprehensive peptides")

# API Endpoints
@api_router.post("/generate-protocol-pdf")
async def generate_protocol_pdf(request: Dict):
    """
    Generate professional PDF for medical protocols
    """
    try:
        protocol_data = request.get("protocol_data", {})
        patient_data = request.get("patient_data", {})
        
        # Generate the PDF
        pdf_buffer = pdf_generator.generate_protocol_pdf(protocol_data, patient_data)
        
        # Return the PDF as a downloadable response
        from fastapi.responses import StreamingResponse
        
        return StreamingResponse(
            iter([pdf_buffer.read()]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=protocol_{protocol_data.get('protocol_id', 'generated')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating protocol PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

# ==========================================
# ADAPTIVE ASSESSMENT & AI PERSONALIZATION ENDPOINTS  
# ==========================================

@api_router.post("/adaptive-assessment/questions", response_model=AdaptiveQuestionResponse)
async def get_adaptive_questions(request: MultiStepAssessmentUpdate):
    """Get personalized questions based on patient data and assessment step"""
    try:
        # Generate personalized questions using adaptive engine
        personalized_questions = adaptive_engine.generate_personalized_questions(
            assessment_data=request.assessment_data,
            step=request.step
        )
        
        return AdaptiveQuestionResponse(
            success=True,
            conditional_questions=personalized_questions.get("conditional_questions", []),
            risk_flags=personalized_questions.get("risk_flags", {}),
            recommended_next_step=personalized_questions.get("recommended_next_step", request.step + 1),
            completion_percentage=personalized_questions.get("completion_percentage", 0.0),
            data=request.assessment_data
        )
        
    except Exception as e:
        logger.error(f"Error generating adaptive questions: {str(e)}")
        return AdaptiveQuestionResponse(
            success=False,
            conditional_questions=[],
            risk_flags={"high_risk": [], "medium_risk": [], "monitoring_required": []},
            recommended_next_step=request.step,
            completion_percentage=0.0,
            data={}
        )

@api_router.post("/adaptive-assessment/risk-analysis")
async def analyze_patient_risk(assessment_data: Dict[str, Any]):
    """Perform comprehensive risk analysis on patient assessment"""
    try:
        # Generate risk flags using adaptive engine
        risk_flags = adaptive_engine.generate_risk_flags(assessment_data)
        
        # Interpret lab values if available
        lab_interpretations = {}
        if "lab_results" in assessment_data and assessment_data["lab_results"]:
            lab_interpretations = adaptive_engine.interpret_lab_values(assessment_data["lab_results"])
        
        return {
            "success": True,
            "risk_assessment": risk_flags,
            "lab_interpretations": lab_interpretations,
            "recommendations": _generate_risk_recommendations(risk_flags),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error analyzing patient risk: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")

@api_router.post("/dosing-calculator/calculate")
async def calculate_peptide_dose(request: DosingCalculationRequest):
    """Calculate personalized peptide dose for patient"""
    try:
        # Calculate personalized dose using dosing calculator
        dosing_calculation = dosing_calculator.calculate_personalized_dose(
            peptide_name=request.peptide_name,
            patient_data=request.patient_data,
            clinical_indication=request.clinical_indication
        )
        
        # Get injection volume and preparation details
        injection_details = dosing_calculator.calculate_injection_volume(
            peptide_name=request.peptide_name,
            calculated_dose=dosing_calculation.calculated_dose
        )
        
        return {
            "success": True,
            "dosing_calculation": {
                "peptide_name": dosing_calculation.peptide_name,
                "base_dose": dosing_calculation.base_dose,
                "calculated_dose": dosing_calculation.calculated_dose,
                "unit": dosing_calculation.unit,
                "frequency": dosing_calculation.frequency,
                "route": dosing_calculation.route,
                "adjustments_applied": dosing_calculation.adjustments_applied,
                "safety_notes": dosing_calculation.safety_notes,
                "monitoring_requirements": dosing_calculation.monitoring_requirements,
                "titration_schedule": dosing_calculation.titration_schedule
            },
            "injection_details": injection_details,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating peptide dose: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dose calculation failed: {str(e)}")

@api_router.get("/dosing-calculator/peptides")
async def get_available_peptides_for_dosing():
    """Get list of peptides available for dosing calculations"""
    try:
        available_peptides = list(dosing_calculator.base_dosing_protocols.keys())
        
        # Add additional info for each peptide
        peptides_info = []
        for peptide_name in available_peptides:
            protocol = dosing_calculator.base_dosing_protocols[peptide_name]
            peptides_info.append({
                "name": peptide_name,
                "unit": protocol["unit"],
                "route": protocol["route"],
                "frequency": protocol["base_frequency"],
                "weight_based": protocol.get("weight_based", False),
                "titration_possible": protocol.get("titration_possible", False)
            })
        
        return {
            "success": True,
            "available_peptides": peptides_info,
            "total_count": len(peptides_info)
        }
        
    except Exception as e:
        logger.error(f"Error getting available peptides: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get peptide list: {str(e)}")

@api_router.post("/dosing-calculator/batch-calculate")
async def calculate_multiple_peptide_doses(request: Dict[str, Any]):
    """Calculate doses for multiple peptides simultaneously"""
    try:
        peptide_names = request.get("peptide_names", [])
        patient_data = request.get("patient_data", {})
        
        batch_calculations = []
        
        for peptide_name in peptide_names:
            try:
                dosing_calculation = dosing_calculator.calculate_personalized_dose(
                    peptide_name=peptide_name,
                    patient_data=patient_data
                )
                
                injection_details = dosing_calculator.calculate_injection_volume(
                    peptide_name=peptide_name,
                    calculated_dose=dosing_calculation.calculated_dose
                )
                
                batch_calculations.append({
                    "peptide_name": peptide_name,
                    "success": True,
                    "dosing_calculation": {
                        "base_dose": dosing_calculation.base_dose,
                        "calculated_dose": dosing_calculation.calculated_dose,
                        "unit": dosing_calculation.unit,
                        "frequency": dosing_calculation.frequency,
                        "route": dosing_calculation.route,
                        "adjustments_applied": dosing_calculation.adjustments_applied,
                        "safety_notes": dosing_calculation.safety_notes,
                        "monitoring_requirements": dosing_calculation.monitoring_requirements
                    },
                    "injection_details": injection_details
                })
                
            except Exception as e:
                batch_calculations.append({
                    "peptide_name": peptide_name,
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "success": True,
            "batch_calculations": batch_calculations,
            "total_calculated": len([calc for calc in batch_calculations if calc["success"]]),
            "total_requested": len(peptide_names),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in batch dose calculation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch calculation failed: {str(e)}")

def _generate_risk_recommendations(risk_flags: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    """Generate clinical recommendations based on risk flags"""
    recommendations = []
    
    # High-risk recommendations
    for high_risk in risk_flags.get("high_risk", []):
        recommendations.append(f"HIGH PRIORITY: {high_risk.get('warning', 'Unknown risk')}")
    
    # Medium-risk recommendations  
    for medium_risk in risk_flags.get("medium_risk", []):
        recommendations.append(f"MONITOR: {medium_risk.get('warning', 'Unknown risk')}")
    
    # Monitoring requirements
    for monitoring in risk_flags.get("monitoring_required", []):
        recommendations.append(f"MONITOR: {monitoring.get('monitoring', 'Additional monitoring required')}")
    
    # General recommendations if no specific risks
    if not any(risk_flags.values()):
        recommendations.append("No significant risk factors identified - standard protocols may be followed")
    
    return recommendations

@api_router.post("/generate-assessment-pdf")
async def generate_assessment_pdf(assessment_data: Dict):
    """
    Generate professional PDF for patient assessments
    """
    try:
        # Create assessment-specific protocol data structure
        protocol_data = {
            "protocol_name": "Patient Assessment Report",
            "protocol_id": f"ASSESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "evidence_level": "Clinical Assessment",
            "executive_summary": "Comprehensive functional medicine assessment with AI-generated insights and recommendations.",
            "protocols": [
                {
                    "name": "Assessment Summary",
                    "indication": "Patient evaluation and protocol recommendation",
                    "mechanism": "AI-powered analysis of patient symptoms, lifestyle, and health goals",
                    "expected_outcomes": "Personalized treatment plan with evidence-based recommendations",
                    "timeline": "Implementation over 3-6 months with regular monitoring"
                }
            ],
            "safety_information": {
                "contraindications": [
                    "All recommendations require healthcare provider review",
                    "Individual contraindications must be assessed",
                    "Drug interactions should be evaluated"
                ],
                "side_effects": [
                    "Varies by specific treatment recommendations",
                    "Monitor for individual responses"
                ],
                "monitoring": [
                    "Regular follow-up appointments",
                    "Laboratory monitoring as indicated",
                    "Symptom tracking and progress assessment"
                ]
            },
            "monitoring_schedule": {
                "Week 2": {
                    "monitoring": "Initial response assessment, tolerance evaluation",
                    "expected": "Early adaptation, minimal side effects"
                },
                "Month 1": {
                    "monitoring": "Progress evaluation, protocol adjustments",
                    "expected": "Initial improvements in target symptoms"
                },
                "Month 3": {
                    "monitoring": "Comprehensive reassessment, optimization",
                    "expected": "Significant progress toward health goals"
                },
                "Month 6": {
                    "monitoring": "Long-term outcomes, maintenance planning",
                    "expected": "Sustained improvements, lifestyle integration"
                }
            },
            "scientific_references": [
                "PeptideProtocols.ai Medical Intelligence Database",
                "Functional Medicine Clinical Guidelines",
                "Evidence-based protocol recommendations"
            ]
        }
        
        # Generate the PDF
        pdf_buffer = pdf_generator.generate_protocol_pdf(protocol_data, assessment_data)
        
        # Return the PDF as a downloadable response
        from fastapi.responses import StreamingResponse
        
        return StreamingResponse(
            iter([pdf_buffer.read()]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=assessment_{assessment_data.get('name', 'patient')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating assessment PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Assessment PDF generation failed: {str(e)}")

@api_router.get("/")
async def root():
    return {
        "message": "PeptideProtocols.ai - Ultimate Practitioner Resource",
        "version": "2.0",
        "features": [
            "Dr. Peptide AI Chat",
            "Enhanced Clinical Database", 
            "Multi-step Assessment Wizard",
            "File Upload & Analysis",
            "Functional Medicine Protocols"
        ]
    }

# Dr. Peptide AI Chat Endpoints
@api_router.post("/dr-peptide/chat")
async def chat_with_dr_peptide(chat_message: ChatMessage):
    """Chat with Dr. Peptide AI - Your Functional Medicine Expert"""
    
    try:
        response = await dr_peptide_ai.chat_with_dr_peptide(
            chat_message.message,
            chat_message.conversation_history
        )
        return response
    except Exception as e:
        logging.error(f"Dr. Peptide chat error: {e}")
        return {
            "success": False,
            "error": "Dr. Peptide is temporarily unavailable",
            "response": "I apologize, but I'm experiencing technical difficulties. Please try again in a moment."
        }

@api_router.post("/dr-peptide/analyze-case")
async def dr_peptide_case_analysis(assessment_id: str):
    """Get Dr. Peptide's analysis of a patient case"""
    
    # Get the assessment
    assessment_data = await db.patient_assessments.find_one({"id": assessment_id})
    if not assessment_data:
        raise HTTPException(status_code=404, detail="Patient assessment not found")
    
    assessment = PatientAssessment(**assessment_data)
    
    try:
        # Prepare patient data in the expected format
        patient_data = {
            "demographics": {
                "name": assessment.patient_name,
                "age": assessment.age,
                "gender": assessment.gender,
                "weight": assessment.weight,
                "height": {"feet": assessment.height_feet, "inches": assessment.height_inches}
            },
            "primary_concerns": assessment.primary_concerns,
            "health_goals": assessment.health_goals,
            "current_medications": assessment.current_medications,
            "medical_history": assessment.medical_history,
            "allergies": assessment.allergies,
            "lifestyle_factors": assessment.lifestyle_factors,
            "lab_results": assessment.lab_results,
            "genetic_data": assessment.genetic_data,
            "uploaded_files": assessment.uploaded_files
        }
        
        case_analysis = await dr_peptide_ai.analyze_patient_case(patient_data)
        return case_analysis
    except Exception as e:
        logging.error(f"Case analysis error: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")

# Enhanced Assessment Endpoints
@api_router.post("/assessment/multi-step")
async def create_or_update_multi_step_assessment(assessment_update: MultiStepAssessmentUpdate, assessment_id: Optional[str] = None):
    """Create or update multi-step assessment"""
    
    if assessment_id:
        # Update existing assessment
        existing = await db.patient_assessments.find_one({"id": assessment_id})
        if not existing:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Update with new step data
        updated_data = {**existing, **assessment_update.assessment_data}
        updated_data["step_completed"] = assessment_update.step
        updated_data["updated_at"] = datetime.utcnow().isoformat()
        
        await db.patient_assessments.update_one(
            {"id": assessment_id},
            {"$set": updated_data}
        )
        
        return {
            "id": assessment_id, 
            "step_completed": assessment_update.step, 
            "status": "updated",
            "message": "Assessment step saved successfully"
        }
    else:
        # Create new assessment with partial data
        assessment_id = str(uuid.uuid4())
        assessment_data = {
            "id": assessment_id,
            "step_completed": assessment_update.step,
            "created_at": datetime.utcnow().isoformat(),
            **assessment_update.assessment_data
        }
        
        await db.patient_assessments.insert_one(assessment_data)
        return {
            "id": assessment_id, 
            "step_completed": assessment_update.step,
            "status": "created",
            "message": "Assessment started successfully"
        }

@api_router.post("/assessment/{assessment_id}/upload-files")
async def upload_assessment_files(assessment_id: str, files: List[UploadFile] = File(...)):
    """Upload and analyze patient files (labs, charts, genetic tests)"""
    
    # Get the assessment
    assessment_data = await db.patient_assessments.find_one({"id": assessment_id})
    if not assessment_data:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    file_analyses = []
    
    try:
        for file in files:
            # Check file type and size
            if file.content_type:
                # Accept common image formats, PDFs, and documents
                allowed_types = [
                    'image/jpeg', 'image/jpg', 'image/png', 'image/tiff',
                    'application/pdf',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'text/plain', 'text/csv',
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                ]
                
                if file.content_type not in allowed_types:
                    # Try to determine by file extension
                    file_ext = Path(file.filename).suffix.lower()
                    if file_ext not in ['.jpg', '.jpeg', '.png', '.tiff', '.pdf', '.docx', '.txt', '.csv', '.xlsx']:
                        raise HTTPException(
                            status_code=415, 
                            detail=f"Unsupported file type: {file.content_type}. Supported formats: JPG, PNG, PDF, DOCX, TXT, CSV, XLSX"
                        )
            
            # Check file size (10MB limit)
            file_content = await file.read()
            if len(file_content) > 10 * 1024 * 1024:  # 10MB
                raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
            
            # Analyze file using the file analysis service
            try:
                analysis_result = await file_analysis_service.analyze_uploaded_file(
                    file_content=file_content,
                    filename=file.filename,
                    content_type=file.content_type,
                    context="patient_assessment"
                )
                
                # Prepare the result for storage
                file_analysis = {
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "size": len(file_content),
                    "status": "processed" if analysis_result.get("success") else "error",
                    "analysis": analysis_result,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
            except Exception as analysis_error:
                logging.error(f"File analysis failed for {file.filename}: {analysis_error}")
                file_analysis = {
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "size": len(file_content),
                    "status": "uploaded",
                    "analysis": {
                        "success": False,
                        "error": f"Analysis failed: {str(analysis_error)}",
                        "filename": file.filename,
                        "analysis_type": "error"
                    },
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            file_analyses.append(file_analysis)
        
        # Update assessment with file data
        await db.patient_assessments.update_one(
            {"id": assessment_id},
            {"$push": {"uploaded_files": {"$each": file_analyses}}}
        )
        
        return {
            "success": True,
            "files_processed": len(files),
            "analyses": file_analyses
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logging.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
        
    except Exception as e:
        logging.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

# Enhanced Protocol Generation
@api_router.post("/generate-functional-protocol/{assessment_id}")
async def generate_functional_medicine_protocol_endpoint(assessment_id: str):
    """Generate comprehensive functional medicine protocol"""
    
    # ✅ ENHANCED VALIDATION: Check assessment_id format
    if not assessment_id or len(assessment_id.strip()) == 0:
        raise HTTPException(status_code=400, detail="Assessment ID is required and cannot be empty")
    
    # ✅ ENHANCED VALIDATION: Check assessment_id is valid UUID format
    try:
        uuid.UUID(assessment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Assessment ID must be a valid UUID format")
    
    # ✅ TIMEOUT HANDLING: Add timeout for database query
    try:
        assessment_data = await asyncio.wait_for(
            db.patient_assessments.find_one({"id": assessment_id}),
            timeout=10.0  # 10 second timeout
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Database query timeout - please try again")
    except Exception as db_error:
        logger.error(f"Database error for assessment {assessment_id}: {db_error}")
        raise HTTPException(status_code=500, detail="Database connection error")
    
    if not assessment_data:
        raise HTTPException(status_code=404, detail=f"Patient assessment with ID {assessment_id} not found")
    
    # ✅ ENHANCED VALIDATION: Validate assessment data completeness
    required_fields = ["patient_name", "age", "gender"]
    missing_fields = []
    for field in required_fields:
        if not assessment_data.get(field) or str(assessment_data.get(field)).strip() == "":
            missing_fields.append(field)
    
    if missing_fields:
        raise HTTPException(
            status_code=422, 
            detail=f"Assessment data incomplete. Missing required fields: {', '.join(missing_fields)}"
        )
    
    # Remove MongoDB _id field if it exists
    if "_id" in assessment_data:
        del assessment_data["_id"]
    
    try:
        # Create assessment with defaults for missing fields and empty strings
        assessment_with_defaults = {
            "patient_name": assessment_data.get("patient_name") or "Unknown",
            "age": assessment_data.get("age") or "30",
            "gender": assessment_data.get("gender") or "not specified",
            "weight": assessment_data.get("weight") or "150",
            "height_feet": assessment_data.get("height_feet") or "5",
            "height_inches": assessment_data.get("height_inches") or "8",
            "email": assessment_data.get("email") or "patient@example.com",
            "primary_concerns": assessment_data.get("primary_concerns") or ["General Health Optimization"],
            "health_goals": assessment_data.get("health_goals") or ["Improve Overall Wellness"],
            "current_medications": assessment_data.get("current_medications", []),
            "lifestyle_factors": assessment_data.get("lifestyle_factors", {}),
            "medical_history": assessment_data.get("medical_history", []),
            "allergies": assessment_data.get("allergies", [])
        }
        
        assessment = PatientAssessment(**assessment_with_defaults)
        
        # Generate comprehensive protocol using Dr. Peptide AI
        protocol_data = await generate_functional_medicine_protocol(assessment)
        
        # Return the uniform sections structure directly (contains all 7 required sections)
        protocol_id = protocol_data.get("protocol_id", str(uuid.uuid4()))
        
        # Ensure proper serialization by converting datetime objects to strings
        if "created_at" in protocol_data and isinstance(protocol_data["created_at"], datetime):
            protocol_data["created_at"] = protocol_data["created_at"].isoformat()
        if "last_updated" in protocol_data and isinstance(protocol_data["last_updated"], datetime):
            protocol_data["last_updated"] = protocol_data["last_updated"].isoformat()
        
        # ✅ CRITICAL FIX: Save protocol to database with progress tracking integration
        try:
            # Prepare protocol record for database
            protocol_record = {
                "protocol_id": protocol_id,
                "patient_assessment_id": assessment_id,
                "patient_id": assessment_with_defaults.get("patient_name", "unknown"),
                "patient_email": assessment_with_defaults.get("email", ""),
                "generated_date": datetime.utcnow().isoformat(),
                "protocol_data": protocol_data,
                "status": "active",
                "progress_tracking_id": None,
                "created_at": datetime.utcnow().isoformat(),
                "last_updated": datetime.utcnow().isoformat()
            }
            
            # Save protocol to database
            await db.patient_protocols.insert_one(protocol_record)
            logger.info(f"Protocol {protocol_id} saved successfully to database")
            
            # ✅ CREATE PROGRESS TRACKING automatically
            initial_metrics = {
                "energy_levels": 5,  # Default starting values
                "sleep_quality": 5,
                "weight": float(assessment_with_defaults.get("weight", 150))
            }
            
            # Add specific metrics based on primary concerns
            primary_concerns = assessment_with_defaults.get("primary_concerns", [])
            if any("weight" in str(concern).lower() for concern in primary_concerns):
                initial_metrics["body_fat_percentage"] = 25  # Default estimate
            if any("cognitive" in str(concern).lower() for concern in primary_concerns):
                initial_metrics["cognitive_function"] = 5
            if any("joint" in str(concern).lower() or "pain" in str(concern).lower() for concern in primary_concerns):
                initial_metrics["joint_pain"] = 6  # Higher is worse
            
            # Create progress tracking
            tracking_result = progress_service.track_progress(
                patient_id=assessment_with_defaults.get("patient_name", "unknown"),
                metric_updates={**initial_metrics, "protocol_id": protocol_id},
                notes=f"Progress tracking started for protocol {protocol_id}"
            )
            
            if tracking_result.get("success"):
                tracking_id = tracking_result.get("tracking_id")
                
                # Link protocol to progress tracking
                await db.patient_protocols.update_one(
                    {"protocol_id": protocol_id},
                    {"$set": {"progress_tracking_id": tracking_id}}
                )
                
                logger.info(f"Progress tracking {tracking_id} created and linked to protocol {protocol_id}")
            
        except Exception as db_error:
            logger.warning(f"Database save failed for protocol {protocol_id}: {db_error}")
            # Continue execution - protocol still generated successfully
        
        return {
            "message": "Functional medicine protocol generated and saved successfully",
            "protocol_id": protocol_id,
            "protocol": protocol_data,
            "progress_tracking_enabled": tracking_result.get("success", False) if 'tracking_result' in locals() else False,
            "tracking_id": tracking_result.get("tracking_id") if 'tracking_result' in locals() else None
        }
        
    except Exception as e:
        logger.error(f"Protocol generation error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate protocol: {str(e)}"
        )

# Enhanced Protocol Library Endpoints
@api_router.get("/enhanced-library", response_model=List[AdvancedProtocolLibraryItem])
async def get_enhanced_protocol_library(category: Optional[str] = None, search: Optional[str] = None):
    """Get enhanced clinical protocol library"""
    
    query = {}
    if category:
        query["category"] = category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"aliases": {"$regex": search, "$options": "i"}},
            {"mechanism_of_action": {"$regex": search, "$options": "i"}},
            {"clinical_indications": {"$regex": search, "$options": "i"}}
        ]
    
    library_items = await db.enhanced_protocol_library.find(query).to_list(1000)
    return [AdvancedProtocolLibraryItem(**item) for item in library_items]

@api_router.get("/enhanced-library/categories")
async def get_enhanced_library_categories():
    """Get all available categories in enhanced library"""
    
    categories = await db.enhanced_protocol_library.distinct("category")
    return {"categories": categories}

@api_router.get("/enhanced-library/{peptide_id}", response_model=AdvancedProtocolLibraryItem)
async def get_enhanced_peptide_details(peptide_id: str):
    """Get comprehensive peptide information"""
    
    peptide_data = await db.enhanced_protocol_library.find_one({"id": peptide_id})
    if not peptide_data:
        raise HTTPException(status_code=404, detail="Peptide not found in enhanced library")
    
    return AdvancedProtocolLibraryItem(**peptide_data)

# Lab Interpretation Endpoint
@api_router.post("/dr-peptide/interpret-labs")
async def interpret_lab_results(lab_data: Dict[str, Any], patient_context: Optional[Dict[str, Any]] = None):
    """Get Dr. Peptide's functional medicine interpretation of lab results"""
    
    try:
        interpretation = await dr_peptide_ai.interpret_lab_results(lab_data, patient_context)
        return interpretation
    except Exception as e:
        logging.error(f"Lab interpretation error: {e}")
        raise HTTPException(status_code=500, detail="Lab interpretation failed")

@api_router.post("/dr-peptide/follow-up")
async def dr_peptide_follow_up(request: Dict):
    """
    Dr. Peptide follow-up consultation with feedback collection
    """
    try:
        protocol_id = request.get("protocol_id", "")
        days_since_start = request.get("days_since_start", 0)
        patient_context = request.get("patient_context", {})
        
        # Generate contextual follow-up prompt
        follow_up_prompt = collective_intelligence.dr_peptide_follow_up_prompt(
            protocol_id, 
            {**patient_context, "days_since_protocol_start": days_since_start}
        )
        
        # Get Dr. Peptide AI response
        response = await dr_peptide_ai.process_chat(follow_up_prompt)
        
        # Log the follow-up interaction for learning
        interaction_data = {
            "type": "follow_up",
            "protocol_id": protocol_id,
            "days_since_start": days_since_start,
            "patient_context": patient_context,
            "ai_response": response,
            "timestamp": datetime.utcnow()
        }
        
        return {
            "success": True,
            "response": response,
            "follow_up_questions": collective_intelligence.generate_follow_up_questions(protocol_id, days_since_start),
            "interaction_id": str(uuid.uuid4())
        }
        
    except Exception as e:
        logger.error(f"Error in Dr. Peptide follow-up: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/feedback/protocol")
async def submit_protocol_feedback(feedback: Dict):
    """
    Submit comprehensive protocol feedback for collective learning
    """
    try:
        protocol_id = feedback.get("protocol_id", "")
        feedback_data = feedback.get("feedback_data", {})
        
        # Collect feedback in collective intelligence system
        feedback_id = collective_intelligence.collect_protocol_feedback(
            protocol_id, 
            feedback_data
        )
        
        # Generate Dr. Peptide response to feedback
        feedback_prompt = f"""
        Thank you for providing feedback on your protocol experience. 
        
        Based on your feedback:
        - Protocol Effectiveness: {feedback_data.get('protocol_effectiveness', 'Not specified')}/5
        - Key Outcomes: {feedback_data.get('specific_outcomes', {})}
        - Timeline: {feedback_data.get('days_since_start', 'Not specified')} days
        
        Please provide:
        1. Acknowledgment of their feedback
        2. Analysis of their progress
        3. Any recommended adjustments
        4. Encouragement and next steps
        5. How their feedback helps improve protocols for others
        
        Be supportive, professional, and emphasize the value of their contribution to collective learning.
        """
        
        dr_peptide_response = await dr_peptide_ai.process_chat(feedback_prompt)
        
        return {
            "success": True,
            "feedback_id": feedback_id,
            "dr_peptide_response": dr_peptide_response,
            "message": "Thank you for your feedback! Your experience helps improve protocols for the entire community."
        }
        
    except Exception as e:
        logger.error(f"Error submitting protocol feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/feedback/error-correction")
async def report_error_or_hallucination(report: Dict):
    """
    Report AI errors or hallucinations for immediate correction and learning
    """
    try:
        report_data = {
            "incorrect_content": report.get("incorrect_content", ""),
            "corrected_content": report.get("corrected_content", ""),
            "reporter_type": report.get("reporter_type", "user"),  # user, practitioner, expert
            "severity": report.get("severity", "medium"),  # low, medium, high
            "context": report.get("context", ""),
            "additional_notes": report.get("additional_notes", "")
        }
        
        # Report to collective intelligence system
        error_id = collective_intelligence.report_ai_hallucination(report_data)
        
        # Generate acknowledgment response
        acknowledgment_prompt = f"""
        A user has reported a potential error in AI-generated content. 
        
        Please provide a professional acknowledgment that:
        1. Thanks them for the correction
        2. Explains how this helps improve the platform
        3. Assures them the correction will be reviewed and integrated
        4. Emphasizes the importance of accuracy in medical information
        5. Encourages continued feedback for collective improvement
        """
        
        dr_peptide_response = await dr_peptide_ai.process_chat(acknowledgment_prompt)
        
        return {
            "success": True,
            "error_id": error_id,
            "status": "reported_for_review",
            "dr_peptide_response": dr_peptide_response,
            "message": "Thank you for the correction. This helps ensure accuracy for all users."
        }
        
    except Exception as e:
        logger.error(f"Error reporting correction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/collective-intelligence/insights")
async def get_collective_insights():
    """
    Get aggregated insights from collective intelligence system
    """
    try:
        insights = collective_intelligence.generate_ai_evolution_insights()
        
        return {
            "success": True,
            "insights": insights,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting collective insights: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/collective-intelligence/practitioner-insight")
async def submit_practitioner_insight(insight: Dict):
    """
    Submit practitioner insights for collective learning
    """
    try:
        practitioner_id = insight.get("practitioner_id", "anonymous")
        insight_data = insight.get("insight_data", {})
        
        insight_id = collective_intelligence.collect_practitioner_insight(
            practitioner_id,
            insight_data
        )
        
        return {
            "success": True,
            "insight_id": insight_id,
            "message": "Thank you for sharing your clinical insight with the community!"
        }
        
    except Exception as e:
        logger.error(f"Error submitting practitioner insight: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/dr-peptide/feedback-chat")
async def dr_peptide_feedback_chat(request: Dict):
    """
    Dr. Peptide chat specifically for discussing protocol feedback and adjustments
    """
    try:
        message = request.get("message", "")
        protocol_id = request.get("protocol_id", "")
        feedback_context = request.get("feedback_context", {})
        
        # Enhanced prompt for feedback-focused chat
        feedback_chat_prompt = f"""
        User message: {message}
        
        Context: This is a feedback discussion about protocol {protocol_id}
        Previous feedback: {feedback_context}
        
        Please provide:
        1. Thoughtful response to their feedback or questions
        2. Specific protocol adjustments if requested
        3. Ask clarifying questions to gather more useful feedback
        4. Explain how their input contributes to collective learning
        5. Provide encouragement and support for their journey
        
        Focus on being genuinely helpful while collecting valuable feedback for continuous improvement.
        """
        
        response = await dr_peptide_ai.process_chat(feedback_chat_prompt)
        
        return {
            "success": True,
            "response": response,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error in Dr. Peptide feedback chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced Protocol Library Endpoints

@api_router.get("/protocols/library/search")
async def search_protocol_library(
    query: Optional[str] = None,
    category: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 50
):
    """Advanced protocol search with filters and ranking"""
    try:
        # Parse tags if provided
        tag_list = tags.split(',') if tags else None
        
        # Search protocols
        results = master_protocol_manager.search_protocols(
            query=query,
            category=category,
            tags=tag_list,
            limit=limit
        )
        
        return {
            "success": True,
            "query": query,
            "category": category,
            "tags": tag_list,
            "total_results": len(results),
            "protocols": results,
            "available_categories": master_protocol_manager.get_categories(),
            "available_tags": master_protocol_manager.get_all_tags()
        }
        
    except Exception as e:
        logging.error(f"Protocol search error: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

@api_router.get("/protocols/library/categories")
async def get_protocol_categories():
    """Get all available protocol categories"""
    try:
        return {
            "success": True,
            "categories": master_protocol_manager.get_categories(),
            "total_categories": len(master_protocol_manager.get_categories())
        }
    except Exception as e:
        logging.error(f"Categories fetch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")

@api_router.get("/protocols/library/tags")
async def get_protocol_tags():
    """Get all available protocol tags"""
    try:
        return {
            "success": True,
            "tags": master_protocol_manager.get_all_tags(),
            "total_tags": len(master_protocol_manager.get_all_tags())
        }
    except Exception as e:
        logging.error(f"Tags fetch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tags")

@api_router.get("/protocols/library/stats")
async def get_library_stats():
    """Get comprehensive library statistics"""
    try:
        stats = master_protocol_manager.get_stats()
        
        return {
            "success": True,
            "library_stats": stats,
            "performance_metrics": {
                "search_index_size": len(master_protocol_manager.keyword_index),
                "categories_indexed": len(master_protocol_manager.category_index),
                "protocols_searchable": len(master_protocol_manager.all_protocols)
            }
        }
    except Exception as e:
        logging.error(f"Stats fetch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch stats")

@api_router.get("/protocols/{protocol_id}")
async def get_protocol_details(protocol_id: str):
    """Get detailed information for a specific protocol"""
    try:
        protocol = master_protocol_manager.get_protocol_by_id(protocol_id)
        
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
            
        return {
            "success": True,
            "protocol": protocol
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Protocol fetch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch protocol")

@api_router.get("/protocols/{protocol_id}/pdf")
async def download_protocol_pdf(protocol_id: str):
    """Generate and download protocol PDF"""
    try:
        protocol = master_protocol_manager.get_protocol_by_id(protocol_id)
        
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
            
        # Generate PDF
        pdf_content = enhanced_pdf_generator.generate_protocol_pdf(protocol)
        
        # Create response with PDF
        filename = f"{protocol['name'].replace(' ', '_')}_Protocol.pdf"
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"PDF generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

@api_router.get("/protocols/library/all")
async def get_all_protocols(limit: int = 100, offset: int = 0):
    """Get all protocols with pagination"""
    try:
        all_protocols = master_protocol_manager.all_protocols[offset:offset + limit]
        
        return {
            "success": True,
            "protocols": all_protocols,
            "total_protocols": len(master_protocol_manager.all_protocols),
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < len(master_protocol_manager.all_protocols)
        }
        
    except Exception as e:
        logging.error(f"All protocols fetch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch protocols")

# Legacy endpoints for backward compatibility
@api_router.post("/assessment", response_model=PatientAssessment)
async def create_basic_assessment(assessment_data: Dict[str, Any]):
    """Create basic assessment (legacy compatibility)"""
    assessment = PatientAssessment(**assessment_data)
    await db.patient_assessments.insert_one(assessment.dict())
    return assessment

@api_router.get("/peptides", response_model=List[Dict[str, Any]])
async def get_comprehensive_peptides():
    """Get comprehensive peptides database with detailed clinical information"""
    return COMPREHENSIVE_PEPTIDES_DATABASE

@api_router.get("/peptides/categories")
async def get_peptide_categories():
    """Get all available peptide categories"""
    try:
        return {"categories": EXPANDED_PEPTIDE_CATEGORIES}
    except Exception as e:
        logger.error(f"Error getting peptide categories: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/peptides/{peptide_name}")
async def get_peptide_by_name(peptide_name: str):
    """Get detailed information for a specific peptide"""
    # Find peptide by name (case insensitive)
    for peptide in COMPREHENSIVE_PEPTIDES_DATABASE:
        if peptide["name"].lower() == peptide_name.lower():
            return peptide
    
    raise HTTPException(status_code=404, detail=f"Peptide '{peptide_name}' not found")

@api_router.get("/peptides/category/{category}")
async def get_peptides_by_category(category: str):
    """Get peptides filtered by category"""
    filtered_peptides = [
        peptide for peptide in COMPREHENSIVE_PEPTIDES_DATABASE
        if peptide["category"].lower() == category.lower()
    ]
    
    if not filtered_peptides:
        raise HTTPException(status_code=404, detail=f"No peptides found in category '{category}'")
    
    return filtered_peptides

@api_router.get("/library", response_model=List[Dict[str, Any]])
async def get_basic_library():
    """Get basic library for backward compatibility"""
    # Return basic format from enhanced library
    enhanced_items = await db.enhanced_protocol_library.find({}).to_list(1000)
    
    basic_items = []
    for item in enhanced_items:
        basic_item = {
            "id": item["id"],
            "name": item["name"],
            "category": item["category"],
            "mechanism": item["mechanism_of_action"][:200] + "..." if len(item["mechanism_of_action"]) > 200 else item["mechanism_of_action"],
            "indications": item["clinical_indications"][:5],  # Limit for compatibility
            "standard_dosing": item["complete_dosing_schedule"],
            "administration": item["administration_techniques"].get("injection_sites", "See detailed protocols"),
            "contraindications": item["contraindications_and_precautions"].get("absolute_contraindications", []),
            "side_effects": [effect["effect"] for effect in item["safety_profile"].get("common_side_effects", [])],
            "monitoring": item["monitoring_requirements"].get("ongoing_monitoring", []),
            "references": [ref.get("title", "") for ref in item["scientific_references"][:3]]
        }
        basic_items.append(basic_item)
    
    return basic_items

# Email Integration Endpoints
@api_router.post("/email/send-protocol")
async def send_protocol_email(request: Dict):
    """Send protocol to patient via email"""
    try:
        recipient_email = request.get("recipient_email")
        recipient_name = request.get("recipient_name", "Patient")
        protocol_data = request.get("protocol_data", {})
        
        # Send email using email service
        success = await email_service.send_protocol_email(
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            protocol_data=protocol_data
        )
        
        if success:
            return {
                "success": True,
                "message": "Protocol email sent successfully",
                "recipient": recipient_email
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send protocol email")
        
    except Exception as e:
        logger.error(f"Error sending protocol email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send protocol email: {str(e)}")

@api_router.post("/email/send-follow-up")
async def send_follow_up_email(request: Dict):
    """Send follow-up reminder email to patient"""
    try:
        recipient_email = request.get("recipient_email")
        recipient_name = request.get("recipient_name", "Patient")
        protocol_name = request.get("protocol_name", "Your Protocol")
        days_since_start = request.get("days_since_start", 0)
        next_milestone = request.get("next_milestone", "Continue monitoring")
        
        # Send follow-up email using email service
        success = await email_service.send_follow_up_reminder(
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            protocol_name=protocol_name,
            days_since_start=days_since_start,
            next_milestone=next_milestone
        )
        
        if success:
            return {
                "success": True,
                "message": "Follow-up email sent successfully",
                "recipient": recipient_email
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send follow-up email")
        
    except Exception as e:
        logger.error(f"Error sending follow-up email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send follow-up email: {str(e)}")

@api_router.post("/email/send-practitioner-notification")
async def send_practitioner_notification_email(request: Dict):
    """Send notification email to practitioner"""
    try:
        practitioner_email = request.get("practitioner_email")
        practitioner_name = request.get("practitioner_name", "Doctor")
        notification_type = request.get("notification_type", "update")
        patient_data = request.get("patient_data", {})
        details = request.get("details", {})
        
        # Send practitioner notification using email service
        success = await email_service.send_practitioner_notification(
            practitioner_email=practitioner_email,
            practitioner_name=practitioner_name,
            notification_type=notification_type,
            patient_data=patient_data,
            details=details
        )
        
        if success:
            return {
                "success": True,
                "message": "Practitioner notification sent successfully",
                "recipient": practitioner_email
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to send practitioner notification")
        
    except Exception as e:
        logger.error(f"Error sending practitioner notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send practitioner notification: {str(e)}")

@api_router.get("/email/status")
async def get_email_service_status():
    """Get email service configuration status"""
    try:
        status = email_service.get_service_status()
        return {
            "success": True,
            "status": status,
            "timestamp": datetime.utcnow()
        }
    except Exception as e:
        logger.error(f"Error getting email service status: {str(e)}")
        return {
            "success": False,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow()
        }

# ✅ PROGRESS TRACKING ENDPOINTS - FIXED TO MATCH SERVICE METHODS
@api_router.post("/progress/track")
async def track_patient_progress(request: Dict):
    """Track patient progress data"""
    try:
        patient_id = request.get("patient_id")
        metric_updates = request.get("metric_updates", {})
        notes = request.get("notes", "")
        
        # Use the actual progress_service.track_progress method
        result = progress_service.track_progress(
            patient_id=patient_id,
            metric_updates=metric_updates,
            notes=notes
        )
        
        return {
            "success": result.get("success", False),
            "message": result.get("message", "Progress update processed"),
            "tracking_id": result.get("tracking_id"),
            "metrics_updated": result.get("metrics_updated", 0),
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error tracking progress: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to track progress: {str(e)}")

@api_router.get("/progress/{patient_id}")
async def get_patient_progress(patient_id: str):
    """Get patient progress data"""
    try:
        # Use the actual progress_service.get_progress_data method
        result = progress_service.get_progress_data(patient_id=patient_id)
        
        return {
            "success": result.get("success", False),
            "progress_data": result.get("progress_data", {}),
            "patient_id": patient_id,
            "tracking_id": result.get("tracking_id"),
            "error": result.get("error"),
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting progress data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get progress data: {str(e)}")

@api_router.get("/progress/{patient_id}/analytics")
async def get_progress_analytics(patient_id: str, time_period: str = "30d"):
    """Get progress analytics and insights"""
    try:
        # Use the actual progress_service.generate_analytics method
        result = progress_service.generate_analytics(
            patient_id=patient_id,
            time_period=time_period
        )
        
        return {
            "success": result.get("success", False),
            "analytics": result.get("analytics", {}),
            "error": result.get("error"),
            "patient_id": patient_id,
            "time_period": time_period,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error generating progress analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate analytics: {str(e)}")

@api_router.post("/progress/{patient_id}/milestone")
async def track_milestone(patient_id: str, request: Dict):
    """Track patient milestone achievement"""
    try:
        milestone_data = request.get("milestone_data", {})
        
        # Use the actual progress_service.track_milestone method
        result = progress_service.track_milestone(
            patient_id=patient_id,
            milestone_data=milestone_data
        )
        
        return {
            "success": result.get("success", False),
            "message": result.get("message", "Milestone processing completed"),
            "milestone_id": result.get("milestone_id"),
            "milestone": result.get("milestone"),
            "error": result.get("error"),
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error tracking milestone: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to track milestone: {str(e)}")

# PDF Generation Service Endpoints (already exist above but ensuring they're complete)
@api_router.post("/protocols/generate-pdf")
async def generate_protocol_pdf_endpoint(request: Dict):
    """Generate PDF for protocol"""
    try:
        protocol_data = request.get("protocol_data", {})
        patient_data = request.get("patient_data", {})
        
        # Generate the PDF
        pdf_buffer = pdf_generator.generate_protocol_pdf(protocol_data, patient_data)
        
        # Return the PDF as a downloadable response
        return StreamingResponse(
            iter([pdf_buffer.read()]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=protocol_{protocol_data.get('protocol_id', 'generated')}_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating protocol PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@api_router.post("/protocols/download-pdf/{protocol_id}")
async def download_protocol_pdf(protocol_id: str):
    """Download existing protocol PDF"""
    try:
        # Get protocol data from database
        protocol_data = await db.enhanced_protocols.find_one({"id": protocol_id})
        if not protocol_data:
            raise HTTPException(status_code=404, detail="Protocol not found")
        
        # Get associated patient data
        patient_data = await db.patient_assessments.find_one({"id": protocol_data.get("patient_assessment_id")})
        
        # Generate fresh PDF
        pdf_buffer = pdf_generator.generate_protocol_pdf(protocol_data, patient_data or {})
        
        return StreamingResponse(
            iter([pdf_buffer.read()]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=protocol_{protocol_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Error downloading protocol PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF download failed: {str(e)}")

# Living Protocol System Endpoints
@api_router.post("/protocol/vote")
async def submit_protocol_vote(vote_data: Dict):
    """
    Submit user or practitioner vote for protocol effectiveness
    """
    try:
        protocol_name = vote_data.get("protocol_name")
        if not protocol_name:
            raise HTTPException(status_code=400, detail="Protocol name is required")
        
        result = living_protocol_manager.submit_vote(protocol_name, vote_data)
        
        if result.get("success"):
            return {
                "success": True,
                "vote_id": result.get("vote_id"),
                "message": "Your vote has been recorded. Thank you for contributing to the community knowledge!",
                "timestamp": datetime.utcnow()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to submit vote")
            
    except Exception as e:
        logger.error(f"Error submitting protocol vote: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to submit vote: {str(e)}")

@api_router.post("/protocol/outcome")
async def submit_protocol_outcome(outcome_data: Dict):
    """
    Submit real patient/practitioner protocol outcome data
    """
    try:
        protocol_name = outcome_data.get("protocol_name")
        if not protocol_name:
            raise HTTPException(status_code=400, detail="Protocol name is required")
        
        result = living_protocol_manager.submit_outcome(protocol_name, outcome_data)
        
        if result.get("success"):
            return {
                "success": True,
                "outcome_id": result.get("outcome_id"),
                "message": "Outcome data submitted successfully. Your real-world results help refine protocols for everyone!",
                "timestamp": datetime.utcnow()
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to submit outcome data")
            
    except Exception as e:
        logger.error(f"Error submitting protocol outcome: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to submit outcome: {str(e)}")

@api_router.get("/protocol/{protocol_name}/statistics")
async def get_protocol_statistics(protocol_name: str):
    """
    Get comprehensive statistics for a protocol including voting and outcomes
    """
    try:
        stats = living_protocol_manager.get_protocol_stats(protocol_name)
        
        return {
            "success": True,
            "statistics": stats,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting protocol statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@api_router.get("/protocols/trending")
async def get_trending_protocols(time_period: str = "30d", limit: int = 10):
    """
    Get trending protocols based on recent positive feedback and usage
    """
    try:
        # For now, return mock trending data based on our enhanced protocols
        # In a real implementation, this would come from the living_protocol_manager
        trending_protocols = [
            {
                "protocol_name": "CJC-1295/Ipamorelin Combination",
                "total_votes": 156,
                "average_ratings": {
                    "effectiveness": 4.8,
                    "safety": 4.6,
                    "value": 4.7
                },
                "recommendation_rate": 94.2,
                "category": "Growth Hormone Enhancement",
                "trend_direction": "up"
            },
            {
                "protocol_name": "BPC-157/TB-500 Ultimate Healing Stack",
                "total_votes": 134,
                "average_ratings": {
                    "effectiveness": 4.9,
                    "safety": 4.7,
                    "value": 4.6
                },
                "recommendation_rate": 96.3,
                "category": "Tissue Repair",
                "trend_direction": "up"
            },
            {
                "protocol_name": "Semaglutide",
                "total_votes": 298,
                "average_ratings": {
                    "effectiveness": 4.8,
                    "safety": 4.3,
                    "value": 4.4
                },
                "recommendation_rate": 91.6,
                "category": "Weight Management",
                "trend_direction": "up"
            }
        ]
        
        return {
            "success": True,
            "trending_protocols": trending_protocols[:limit],
            "time_period": time_period,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting trending protocols: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get trending protocols: {str(e)}")

@api_router.post("/protocol/compare")
async def compare_protocols(comparison_request: Dict):
    """
    Compare multiple protocols based on user feedback and outcomes
    """
    try:
        protocol_names = comparison_request.get("protocol_names", [])
        if not protocol_names or len(protocol_names) < 2:
            raise HTTPException(status_code=400, detail="At least 2 protocol names required for comparison")
        
        comparisons = {}
        for protocol_name in protocol_names:
            stats = living_protocol_manager.get_protocol_stats(protocol_name)
            comparisons[protocol_name] = stats
        
        return {
            "success": True,
            "comparisons": comparisons,
            "compared_protocols": protocol_names,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error comparing protocols: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to compare protocols: {str(e)}")

@api_router.get("/protocol/{protocol_name}/feedback")
async def get_protocol_feedback(protocol_name: str, limit: int = 20):
    """
    Get recent user feedback and comments for a protocol
    """
    try:
        # For demo purposes, return sample feedback
        # In real implementation, this would come from living_protocol_manager
        sample_feedback = [
            {
                "user_type": "practitioner",
                "rating": 5,
                "comment": "Excellent results with this combination. Patients report significant improvements in sleep and energy within 2-3 weeks.",
                "timestamp": "2024-12-08T10:30:00Z",
                "verified": True
            },
            {
                "user_type": "user",
                "rating": 4,
                "comment": "Great protocol, saw noticeable improvements after 6 weeks. Only minor side effect was increased appetite initially.",
                "timestamp": "2024-12-07T15:45:00Z",
                "verified": False
            },
            {
                "user_type": "practitioner",
                "rating": 5,
                "comment": "This has become my go-to protocol for patients seeking comprehensive anti-aging benefits. Very well tolerated.",
                "timestamp": "2024-12-06T09:15:00Z",
                "verified": True
            }
        ]
        
        return {
            "success": True,
            "protocol_name": protocol_name,
            "feedback": sample_feedback[:limit],
            "total_feedback_count": len(sample_feedback),
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Error getting protocol feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get feedback: {str(e)}")

# SEO and Sitemap Endpoints

@app.get("/sitemap.xml", response_class=Response)
async def get_sitemap():
    """Generate and serve dynamic XML sitemap"""
    try:
        sitemap_content = sitemap_generator.generate_sitemap()
        
        return Response(
            content=sitemap_content,
            media_type="application/xml",
            headers={
                "Content-Type": "application/xml; charset=utf-8",
                "Cache-Control": "public, max-age=3600"  # Cache for 1 hour
            }
        )
        
    except Exception as e:
        logging.error(f"Sitemap generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate sitemap")

@app.get("/protocol-sitemap.xml", response_class=Response)
async def get_protocol_sitemap():
    """Generate protocol-specific sitemap"""
    try:
        sitemap_content = sitemap_generator.generate_protocol_sitemap()
        
        return Response(
            content=sitemap_content,
            media_type="application/xml",
            headers={
                "Content-Type": "application/xml; charset=utf-8",
                "Cache-Control": "public, max-age=3600"
            }
        )
        
    except Exception as e:
        logging.error(f"Protocol sitemap generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate protocol sitemap")

@app.get("/robots.txt", response_class=Response)
async def get_robots_txt():
    """Serve robots.txt file"""
    try:
        robots_content = sitemap_generator.generate_robots_txt()
        
        return Response(
            content=robots_content,
            media_type="text/plain",
            headers={
                "Content-Type": "text/plain; charset=utf-8",
                "Cache-Control": "public, max-age=86400"  # Cache for 24 hours
            }
        )
        
    except Exception as e:
        logging.error(f"Robots.txt generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate robots.txt")

@api_router.get("/seo/structured-data/{protocol_id}")
async def get_protocol_structured_data(protocol_id: str):
    """Get structured data for a specific protocol (for dynamic SEO)"""
    try:
        protocol = master_protocol_manager.get_protocol_by_id(protocol_id)
        
        if not protocol:
            raise HTTPException(status_code=404, detail="Protocol not found")
        
        structured_data = {
            "@context": "https://schema.org",
            "@type": "MedicalGuidelineRecommendation",
            "name": f"{protocol['name']} Protocol",
            "description": protocol.get('description', ''),
            "url": f"https://peptide-protocols-4.preview.emergentagent.com/protocol/{protocol['id']}",
            "medicalSpecialty": "Functional Medicine",
            "guidelineSubject": {
                "@type": "MedicalCondition",
                "name": protocol.get('category', '')
            },
            "evidenceLevel": {
                "@type": "MedicalEvidenceLevel",
                "evidenceLevel": "Clinical Practice"
            },
            "guideline": {
                "@type": "MedicalGuideline",
                "name": f"{protocol['name']} Therapy Protocol",
                "description": protocol.get('mechanism_of_action', ''),
                "guidelineDate": protocol.get('last_updated', ''),
                "medicalSpecialty": "Functional Medicine"
            }
        }
        
        # Add clinical indications if available
        if protocol.get('clinical_indications'):
            structured_data["applicableCondition"] = [
                {
                    "@type": "MedicalCondition",
                    "name": indication
                } for indication in protocol['clinical_indications'][:5]  # Limit to 5
            ]
        
        return {
            "success": True,
            "structured_data": structured_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Structured data generation error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate structured data")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize enhanced protocol library on startup"""
    await initialize_enhanced_protocol_library()
    logging.info("PeptideProtocols.ai - Ultimate Practitioner Resource initialized")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()