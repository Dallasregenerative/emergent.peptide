"""
Dr. Peptide AI - Functional Medicine Expert Chatbot
Specialized AI assistant for peptide therapy and functional medicine
"""

import os
import json
import logging
import re
from openai import AsyncOpenAI
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import enhanced clinical data
from enhanced_clinical_database import ENHANCED_CLINICAL_PEPTIDES

class DrPeptideAI:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.system_prompt = self._create_system_prompt()
        
class DrPeptideAI:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.enhanced_protocols = ENHANCED_CLINICAL_PEPTIDES
        self.system_prompt = self._create_enhanced_system_prompt()
        
    def _get_enhanced_protocol_data(self) -> str:
        """Generate comprehensive protocol data from enhanced clinical database"""
        protocol_summaries = []
        
        for protocol in self.enhanced_protocols:
            # Extract key clinical data for AI context with safe access
            try:
                indications = protocol.get('clinical_indications', [])
                dosing = protocol.get('complete_dosing_schedule', {})
                safety = protocol.get('safety_profile', {})
                contraindications = protocol.get('contraindications_and_precautions', {})
                references = protocol.get('scientific_references', [])
                cost = protocol.get('cost_considerations', {})
                functional_med = protocol.get('functional_medicine_approach', {})
                
                summary = f"""
{protocol['name']} ({protocol.get('category', 'Unknown')}):
- Clinical Indications: {', '.join(indications[:5])}{'...' if len(indications) > 5 else ''}
- Dosing: {list(dosing.values())[0] if dosing else 'Dosing data available'}
- Safety: {len(safety.get('common_side_effects', []))} documented side effects
- Contraindications: {len(contraindications.get('absolute_contraindications', []))} absolute contraindications
- References: {len(references)} peer-reviewed studies
- Cost: {cost.get('typical_cost', 'Cost data available')}
- Functional Medicine: {functional_med.get('root_cause_focus', 'Functional approach available')}"""
                
                protocol_summaries.append(summary)
                
            except Exception as e:
                # Skip protocols with data issues
                logging.warning(f"Error processing protocol {protocol.get('name', 'Unknown')}: {e}")
                continue
            
        return "\n".join(protocol_summaries)
            
    def find_enhanced_protocol(self, peptide_name: str) -> Optional[Dict[str, Any]]:
        """Find enhanced protocol data by peptide name (fuzzy matching)"""
        peptide_lower = peptide_name.lower()
        
        for protocol in self.enhanced_protocols:
            # Check main name
            if peptide_lower in protocol['name'].lower():
                return protocol
            
            # Check aliases
            for alias in protocol.get('aliases', []):
                if peptide_lower in alias.lower():
                    return protocol
                    
        return None
        
    def get_protocol_summary(self, protocol: Dict[str, Any]) -> str:
        """Generate comprehensive protocol summary for AI context"""
        if not protocol:
            return ""
            
        try:
            # Extract key data points for AI with safe access
            name = protocol.get('name', 'Unknown')
            category = protocol.get('category', 'Unknown')
            indications = protocol.get('clinical_indications', [])
            dosing = protocol.get('complete_dosing_schedule', {})
            admin = protocol.get('administration_techniques', {})
            safety = protocol.get('safety_profile', {})
            contraindications = protocol.get('contraindications_and_precautions', {})
            monitoring = protocol.get('monitoring_requirements', {})
            timelines = protocol.get('expected_timelines', {})
            cost = protocol.get('cost_considerations', {})
            references = protocol.get('scientific_references', [])
            functional_med = protocol.get('functional_medicine_approach', {})

            # Build summary safely
            summary = f"""
ENHANCED PROTOCOL DATA FOR {name}:

**Clinical Profile:**
- Category: {category}
- Clinical Indications: {indications[:3] if indications else ['General therapeutic use']}
- Molecular Weight: {protocol.get('molecular_weight', 'Not specified')} Da

**Dosing Protocols:**
{json.dumps(dosing, indent=2) if dosing else 'Standard dosing protocols available'}

**Safety Profile:**
- Common Side Effects: {[f"{se.get('effect', 'Unknown')} ({se.get('frequency', 'Unknown')})" for se in safety.get('common_side_effects', [])][:3]}
- Contraindications: {contraindications.get('absolute_contraindications', [])[:3]}

**Administration:**
{json.dumps(admin, indent=2) if admin else 'Standard administration techniques available'}

**Monitoring Requirements:**
{json.dumps(monitoring, indent=2) if monitoring else 'Standard monitoring protocols available'}

**Expected Outcomes:**
{json.dumps(timelines, indent=2) if timelines else 'Typical therapeutic timelines available'}

**Cost Analysis:**
{json.dumps(cost, indent=2) if cost else 'Cost information available upon request'}

**Scientific References:**
{len(references)} peer-reviewed studies available

**Functional Medicine Approach:**
{json.dumps(functional_med, indent=2) if functional_med else 'Functional medicine protocols available'}
"""
            return summary
            
        except Exception as e:
            logging.warning(f"Error generating protocol summary for {protocol.get('name', 'Unknown')}: {e}")
            return f"Enhanced protocol data available for {protocol.get('name', 'Unknown Protocol')}"
        
    def _create_enhanced_system_prompt(self) -> str:
        """Create optimized system prompt with comprehensive clinical standards within token limits"""
        
        return f"""
You are Dr. Peptide, board-certified peptide specialist with 20+ years clinical experience. Generate hospital-grade protocols with comprehensive safety analysis.

🏥 **CLINICAL SAFETY REQUIREMENTS:**

**CONTRAINDICATION SCREENING:**
- Cancer: BPC-157, TB-500, GHK-Cu, Thymosin Alpha-1, Epithalon contraindicated
- Pregnancy/Lactation: All peptides contraindicated
- Autoimmune: TB-500 caution with lupus, RA, MS
- CVD: PT-141/Melanotan contraindicated with uncontrolled hypertension
- Pituitary: GH peptides contraindicated with acromegaly

**DRUG INTERACTIONS & MONITORING:**
- Diabetes meds (insulin, metformin) + GH peptides: "Monitor glucose daily x2 weeks, check HbA1c at 3 months"
- Corticosteroids + BPC-157: "Separate by 4+ hours, monitor therapeutic response"
- Immunosuppressants (cyclosporine, tacrolimus) + Thymosin: "HIGH RISK - Avoid without specialist approval"
- ED medications (sildenafil, tadalafil) + PT-141: "CRITICAL - Severe hypotension risk, separate by 24+ hours"
- SSRIs (fluoxetine, sertraline) + Selank/Semax: "Monitor for serotonin syndrome, start lowest dose"
- Anticoagulants + peptides: "Monitor INR closely, assess bleeding risk"

MANDATORY INTERACTION CHECK: List ALL current medications and provide specific interaction analysis for each recommended peptide.

**DOSING WITH SAFETY CALCULATIONS:**
- Weight-based: "250mcg = 3.57mcg/kg for 70kg patient"
- Age >75: Reduce dose 25% 
- Kidney/liver disease: Reduce 25-50%
- BPC-157 max: 500mcg/day, TB-500 max: 10mg/week

**ADMINISTRATION PROTOCOLS:**
- Injection: 27-gauge, 0.5-inch, 45° subcutaneous
- Site rotation: Week 1 abdomen, Week 2 thigh, Week 3 deltoid
- Storage: Refrigerate 36-46°F, stable 28 days

**MONITORING SCHEDULES:**
- Baseline: CBC, CMP, inflammatory markers
- Week 2: Clinical assessment, injection site exam
- Week 8: Labs + efficacy evaluation

**EVIDENCE & COST:**
- Citations: "Sikiric et al. (2020): 65% improvement, n=120"
- Monthly costs: "BPC-157: $53-73, TB-500: $85-120"
- Safety level: "EXCELLENT (90-100), GOOD (75-89), CAUTION (<75)"

🎯 **RESPONSE STRUCTURE:**
1. Safety screening with contraindications
2. Drug interaction analysis
3. Weight-adjusted dosing calculations  
4. Administration and monitoring protocols
5. Evidence-based outcomes and costs
6. Safety score (0-100) with recommendations

Generate precise clinical protocols matching major medical center documentation standards.
"""

    async def chat_with_dr_peptide(self, message: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Enhanced chat interface with intelligent protocol integration
        """
        try:
            # Analyze message for peptide references
            relevant_protocols = self._extract_relevant_protocols(message)
            
            # Prepare conversation context
            if conversation_history is None:
                conversation_history = []
                
            # Build enhanced context with protocol data
            enhanced_context = ""
            if relevant_protocols:
                enhanced_context = "\n\n**RELEVANT ENHANCED PROTOCOLS FOR THIS QUERY:**\n"
                for protocol in relevant_protocols[:3]:  # Limit to top 3 most relevant
                    enhanced_context += self.get_protocol_summary(protocol)
                    enhanced_context += "\n" + "="*50 + "\n"
                
            # Build messages for OpenAI
            messages = [
                {"role": "system", "content": self.system_prompt + enhanced_context}
            ]
            
            # Add conversation history
            for msg in conversation_history[-8:]:  # Keep last 8 messages for context (reduced due to larger system prompt)
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Get AI response with enhanced parameters
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.6,  # Slightly lower for more consistent medical advice
                max_tokens=2000,  # Increased for more comprehensive responses
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": ai_response,
                "enhanced_protocols_used": [p['name'] for p in relevant_protocols] if relevant_protocols else [],
                "timestamp": datetime.utcnow().isoformat(),
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logging.error(f"Enhanced Dr. Peptide chat error: {e}")
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, but I'm experiencing technical difficulties accessing my enhanced clinical database right now. Please try again in a moment, or consult with a healthcare provider for immediate assistance.",
                "timestamp": datetime.utcnow().isoformat()
            }
            
    def _extract_relevant_protocols(self, message: str) -> List[Dict[str, Any]]:
        """Extract relevant enhanced protocols based on message content"""
        relevant_protocols = []
        message_lower = message.lower()
        
        # Common peptide-related keywords and their categories
        keywords_to_category = {
            # Weight management keywords
            'weight loss': 'Weight Management',
            'obesity': 'Weight Management', 
            'fat loss': 'Weight Management',
            'semaglutide': 'Weight Management',
            'tirzepatide': 'Weight Management',
            'glp-1': 'Weight Management',
            'ozempic': 'Weight Management',
            'wegovy': 'Weight Management',
            
            # Cognitive keywords
            'memory': 'Cognitive Enhancement',
            'cognition': 'Cognitive Enhancement',
            'brain': 'Cognitive Enhancement',
            'focus': 'Cognitive Enhancement',
            'nootropic': 'Cognitive Enhancement',
            'dementia': 'Cognitive Enhancement',
            'alzheimer': 'Cognitive Enhancement',
            
            # Growth hormone keywords
            'growth hormone': 'Growth Hormone Enhancement',
            'anti-aging': 'Growth Hormone Enhancement',
            'longevity': 'Growth Hormone Enhancement',
            'muscle': 'Growth Hormone Enhancement',
            'recovery': 'Growth Hormone Enhancement',
            
            # Healing keywords
            'healing': 'Tissue Repair',
            'injury': 'Tissue Repair',
            'pain': 'Tissue Repair',
            'inflammation': 'Tissue Repair',
            'gut': 'Tissue Repair'
        }
        
        # Find protocols by direct name mention
        for protocol in self.enhanced_protocols:
            if protocol['name'].lower() in message_lower:
                relevant_protocols.append(protocol)
                continue
                
            # Check aliases
            for alias in protocol.get('aliases', []):
                if alias.lower() in message_lower:
                    relevant_protocols.append(protocol)
                    break
        
        # If no direct matches, find by category/keywords
        if not relevant_protocols:
            for keyword, category in keywords_to_category.items():
                if keyword in message_lower:
                    category_protocols = [p for p in self.enhanced_protocols if p['category'] == category]
                    relevant_protocols.extend(category_protocols[:2])  # Add top 2 from category
                    
        return relevant_protocols[:3]  # Return top 3 most relevant

    async def generate_personalized_protocol(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized protocol using enhanced clinical database"""
        try:
            # Create advanced clinical-grade prompt with comprehensive reasoning
            protocol_prompt = f"""
You are Dr. Peptide, a board-certified functional medicine physician with 20+ years of clinical experience specializing in peptide therapy. Generate a comprehensive clinical protocol that demonstrates deep medical reasoning and evidence-based decision making.

PATIENT ASSESSMENT DATA:
{json.dumps(patient_data, indent=2)}

🏥 **CLINICAL EXCELLENCE REQUIREMENTS:**

**PATHOPHYSIOLOGY ANALYSIS:**
- Analyze the root causes of patient's conditions at cellular/molecular level
- Identify metabolic dysfunction patterns, inflammatory pathways, hormonal imbalances
- Explain how peptides will address specific pathophysiological mechanisms
- Include systems thinking approach (gut-brain axis, HPA axis, mitochondrial function)

**COMPREHENSIVE MEDICATION ANALYSIS (MANDATORY):**
- Review ALL current medications: {patient_data.get('current_medications', [])}
- Identify specific drug interactions with each recommended peptide
- Provide detailed interaction severity: High Risk, Medium Risk, Low Risk, No Interaction
- Include specific monitoring requirements for each interaction
- Timing considerations (e.g., separate administration by X hours)

**EVIDENCE-BASED PEPTIDE SELECTION:**
- Reference specific clinical studies for each peptide recommendation (format: "Author et al. (Year): X% improvement, n=XX, p<0.001")
- Explain mechanism of action at receptor/cellular level
- Justify dosing based on published pharmacokinetic data
- Include contraindication analysis with clinical reasoning

**PRECISION DOSING PROTOCOLS:**
- Calculate exact weight-based dosing: "250 mcg BPC-157 = 3.57 mcg/kg for 70kg patient, optimized for moderate tissue damage severity"
- Age-based adjustments: "Reduced 25% for age >65 due to decreased renal clearance"
- Individual risk factors: "Increased monitoring frequency given history of hypertension"
- Administration specifics: "27-gauge 0.5-inch needle, 45° subcutaneous angle, rotate injection sites weekly"

**CLINICAL MONITORING PROTOCOLS:**
- Baseline requirements: "CBC with differential, CMP including liver function, inflammatory markers (CRP <1.0 mg/L target), peptide-specific biomarkers"
- Structured follow-up: "Week 2: clinical assessment + injection site exam, Week 4: symptom scales + functional measures, Week 8: comprehensive lab review + protocol optimization"
- Safety parameters: "Monitor for peptide-specific adverse events, drug interactions, efficacy milestones"

**MECHANISM OF ACTION EXPLANATIONS:**
- Cellular pathways: "BPC-157 activates VEGF-mediated angiogenesis and upregulates collagen synthesis via TGF-β1 pathway"
- Receptor interactions: "Ipamorelin selective binding to GHSR-1a receptors without cortisol/prolactin elevation"
- Pharmacokinetics: "Peak plasma levels at 30-60 minutes, elimination half-life 2-4 hours, optimal dosing window analysis"

**OUTCOME PREDICTIONS WITH TIMELINES:**
- Molecular response: "Cellular repair cascade initiation within 24-48 hours"
- Clinical milestones: "≥30% symptom improvement by week 2, ≥50% by week 4, sustained benefits by week 8"
- Biomarker changes: "CRP reduction to <1.0 mg/L, IGF-1 optimization to age-appropriate range"

**FUNCTIONAL MEDICINE INTEGRATION:**
- Root cause analysis: Address underlying triggers (gut permeability, chronic stress, toxin exposure)
- Synergistic interventions: Nutrition protocols, targeted supplementation, lifestyle modifications
- Systems optimization: Sleep quality enhancement, stress resilience building, detoxification support

Generate comprehensive JSON response with this enhanced structure:
{{
    "clinical_reasoning": "Hospital-grade analysis with evidence-based protocol selection rationale",
    "root_causes": ["Primary pathophysiology", "Secondary factors", "Systemic dysfunction"],
    "recommended_peptides": ["Primary peptide", "Supporting peptide", "Optional peptide"],
    "primary_peptides": [
        {{
            "name": "Primary peptide (e.g., BPC-157)",
            "clinical_indication": "Specific indication with ICD-10 (e.g., Chronic tendinopathy M76.9)",
            "evidence_basis": "Study reference (e.g., Sikiric 2020: 65% improvement, n=120, p<0.001)",
            "personalized_dosing": "Weight-based calculation (e.g., 250 mcg = 3.57 mcg/kg for 70kg)",
            "frequency": "Precise timing (e.g., Twice daily: 8AM ±30min, 8PM ±30min, empty stomach)",
            "duration": "Evidence timeline (e.g., 6-week course, 4-week assessment point)",
            "administration": "Clinical protocol (e.g., 27G 0.5-inch needle, 45° subcutaneous, site rotation: Week 1-abdomen, Week 2-thigh, Week 3-deltoid)",
            "storage": "Stability (e.g., Refrigerate 36-46°F, stable 28 days post-reconstitution)",
            "expected_benefits": "Measurable endpoints (e.g., ≥50% WOMAC pain reduction by week 4)",
            "onset_timeline": "Milestones (e.g., Cellular response: 24-48h, Initial relief: days 3-7, Maximum effect: weeks 4-6)",
            "monitoring": "Schedule (e.g., Baseline: CBC/CMP/CRP. Week 2: clinical assessment. Week 8: lab re-evaluation)",
            "safety": "Contraindications (e.g., Compatible with levothyroxine, monitor for injection site reactions)",
            "cost": "Breakdown (e.g., BPC-157 5mg: $45, supplies: $8, monthly: $53, annual: $636 + $600 monitoring)"
        }}
    ],
    "supporting_peptides": [
        {{
            "name": "Supporting peptide (e.g., Thymosin Alpha-1)",
            "rationale": "Combination evidence (e.g., Enhanced recovery with immune modulation)",
            "dosing": "Patient-specific (e.g., 1.6mg twice weekly)",
            "timing": "Coordination (e.g., Monday/Thursday evenings)",
            "benefits": "Combined effects (e.g., Enhanced tissue repair, faster healing)",
            "cost": "Monthly estimate (e.g., $71 total)"
        }}
    ],
    "safety_analysis": {{
        "contraindications": ["Active malignancy excluded", "Pregnancy excluded", "Autoimmune screening completed"],
        "drug_interactions": [
            {{
                "medication": "Current medication name",
                "interaction_severity": "High/Medium/Low/None",
                "clinical_significance": "Specific interaction details",
                "monitoring_requirements": "Specific monitoring needed",
                "timing_adjustments": "Separation timing if needed"
            }}
        ],
        "monitoring": ["Baseline labs: CBC/CMP/CRP", "Injection site assessments", "Drug interaction monitoring", "Follow-up at weeks 2, 4, 8"],
        "warnings": ["Discontinue if allergic reaction", "Report injection site reactions", "Specific drug interaction warnings", "Emergency protocols provided"]
    }},
    "cost_analysis": {{
        "monthly": "Primary peptides: $45-65, Supporting: $65-85, Monitoring: $50, Total: $160-200",
        "annual": "Peptides: $1320-1800, Labs: $600, Visits: $900, Total: $2820-3300",
        "options": "HSA/FSA eligible, bulk purchase discounts available"
    }},
    "timeline_expectations": {{
        "weeks_0-2": ["Injection routine established", "Initial cellular response"],
        "weeks_3-6": ["≥50% symptom improvement", "Functional enhancement"],
        "months_2-6": ["Sustained improvement", "Return to baseline function"]
    }},
    "evidence_summary": "Level II RCT evidence, meta-analysis showing significant improvement (p<0.001)",
    "patient_education": ["Injection technique", "Storage protocols", "Symptom tracking", "Emergency recognition"]
}}

Focus on safety first, personalization based on patient factors, and evidence-based recommendations using our enhanced clinical protocols.
"""

            # Get relevant protocols for context
            relevant_protocols = self._extract_relevant_protocols_for_case(patient_data)
            
            # Add enhanced protocol context
            enhanced_context = ""
            if relevant_protocols:
                enhanced_context = "\n\nRELEVANT ENHANCED PROTOCOLS FOR THIS CASE:\n"
                for protocol in relevant_protocols[:4]:  # Top 4 most relevant
                    enhanced_context += self.get_protocol_summary(protocol)
                    enhanced_context += "\n" + "="*30 + "\n"

            messages = [
                {"role": "system", "content": f"""You are Dr. Peptide, a board-certified functional medicine physician specializing in peptide therapy with 20+ years clinical experience. You must generate hospital-grade clinical protocols that meet medical center standards for documentation and precision.

MANDATORY CLINICAL STANDARDS:
- Provide exact dosing with weight-based calculations
- Include detailed administration protocols with specific injection techniques
- Specify comprehensive monitoring schedules with laboratory requirements
- Conduct thorough safety analysis with contraindication assessment
- Include evidence-based rationale with specific study citations
- Provide detailed cost analysis with transparent pricing
- Ensure all protocols meet hospital clinical documentation standards

COMPREHENSIVE SAFETY REQUIREMENTS:
- Cancer screening: All growth-promoting peptides (BPC-157, TB-500, GHK-Cu) contraindicated with active cancer
- Pregnancy/lactation: All peptides contraindicated in pregnancy/breastfeeding
- Drug interactions: Assess interactions with corticosteroids, diabetes meds, immunosuppressants, ED medications
- Organ function: Adjust dosing for kidney/liver disease, elderly patients (>75 years)
- Cardiovascular: PT-141/Melanotan contraindicated with uncontrolled CVD/hypertension

CLINICAL EXPERTISE AREAS:
- Board certification in functional medicine with peptide therapy subspecialty
- Access to comprehensive enhanced clinical protocols with peer-reviewed evidence
- Hospital-grade clinical decision support system capabilities
- Real-time contraindication and drug interaction analysis
- Evidence-based dosing algorithms and safety monitoring protocols

PROTOCOL PRECISION REQUIREMENTS:
- Dosing: Exact mcg/mg with patient-specific calculations
- Administration: Step-by-step injection protocols with site rotation
- Monitoring: Structured follow-up with specific laboratory schedules
- Safety: Comprehensive contraindication and interaction analysis
- Evidence: Specific study references with outcome data
- Cost: Detailed monthly and annual cost projections with optimization strategies

Your protocols must demonstrate the clinical depth and precision expected from a leading peptide therapy specialist at a major medical center.

{enhanced_context}

Generate protocols that match the clinical detail and precision found in peer-reviewed medical literature and clinical practice guidelines at top-tier medical institutions."""},
                {"role": "user", "content": protocol_prompt}
            ]

            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Higher token limit model
                messages=messages,
                temperature=0.1,  # Very low temperature for maximum clinical precision
                max_tokens=4000,  # Increased token limit for comprehensive protocols
            )

            ai_response = response.choices[0].message.content
            
            # Try to parse as JSON, fallback to text analysis
            try:
                protocol_data = json.loads(ai_response)
                protocol_data["success"] = True
                
                # Perform comprehensive safety analysis on generated protocol
                if 'primary_peptides' in protocol_data:
                    peptides_for_safety = []
                    for peptide in protocol_data['primary_peptides']:
                        if isinstance(peptide, dict):
                            peptides_for_safety.append(peptide)
                        elif isinstance(peptide, str):
                            peptides_for_safety.append({"name": peptide})
                    
                    # Run safety checks
                    contraindications = self.check_contraindications(patient_data, peptides_for_safety)
                    interactions = self.check_drug_interactions(peptides_for_safety, patient_data)
                    dosage_issues = self.validate_dosages(peptides_for_safety, patient_data)
                    
                    # Add safety analysis to protocol
                    protocol_data["comprehensive_safety_analysis"] = {
                        "contraindications_found": contraindications,
                        "drug_interactions": interactions,
                        "dosage_validation": dosage_issues,
                        "safety_score": self._calculate_safety_score(contraindications, interactions, dosage_issues)
                    }
                    
                    # Add safety warnings if critical issues found
                    critical_issues = [c for c in contraindications if c.get('severity') == 'high']
                    critical_interactions = [i for i in interactions if i.get('severity') == 'high']
                    
                    if critical_issues or critical_interactions:
                        protocol_data["safety_warnings"] = [
                            "⚠️ CRITICAL SAFETY ALERT: High-risk contraindications or interactions identified",
                            "This protocol requires immediate practitioner review before implementation",
                            "Do not proceed without specialist consultation"
                        ]
                
            except json.JSONDecodeError:
                # Fallback to text-based analysis
                protocol_data = {
                    "success": True,
                    "analysis": ai_response,
                    "clinical_reasoning": "Comprehensive functional medicine analysis provided",
                    "recommended_peptides": self._extract_peptide_names(ai_response),
                    "root_causes": ["Analysis provided in text format"],
                    "primary_peptides": [],
                    "supporting_peptides": [],
                    "contraindications_assessment": [],
                    "monitoring_requirements": [],
                    "safety_warnings": ["Standard medical supervision required"],
                    "estimated_monthly_cost": "Variable based on protocol"
                }

            return protocol_data

        except Exception as e:
            logging.error(f"Enhanced protocol generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "analysis": "Enhanced protocol generation temporarily unavailable"
            }
            
    def _extract_relevant_protocols_for_case(self, patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract relevant protocols based on comprehensive patient data"""
        relevant_protocols = []
        
        # Extract all text from patient data
        all_text = ""
        for key, value in patient_data.items():
            if isinstance(value, (str, list, dict)):
                all_text += f" {json.dumps(value) if not isinstance(value, str) else value}"
        
        all_text_lower = all_text.lower()
        
        # Category mapping based on patient concerns
        concern_mappings = {
            'weight': 'Weight Management',
            'diabetes': 'Weight Management',
            'obesity': 'Weight Management',
            'fat': 'Weight Management',
            'glucose': 'Weight Management',
            
            'memory': 'Cognitive Enhancement',
            'brain': 'Cognitive Enhancement', 
            'focus': 'Cognitive Enhancement',
            'concentration': 'Cognitive Enhancement',
            'cognitive': 'Cognitive Enhancement',
            'dementia': 'Cognitive Enhancement',
            
            'muscle': 'Growth Hormone Enhancement',
            'energy': 'Growth Hormone Enhancement',
            'aging': 'Growth Hormone Enhancement',
            'recovery': 'Growth Hormone Enhancement',
            'sleep': 'Growth Hormone Enhancement',
            
            'pain': 'Tissue Repair',
            'injury': 'Tissue Repair',
            'inflammation': 'Tissue Repair',
            'healing': 'Tissue Repair',
            'joint': 'Tissue Repair',
            'gut': 'Tissue Repair'
        }
        
        # Find relevant categories
        relevant_categories = set()
        for concern, category in concern_mappings.items():
            if concern in all_text_lower:
                relevant_categories.add(category)
        
        # Get protocols from relevant categories
        for protocol in self.enhanced_protocols:
            if protocol['category'] in relevant_categories:
                relevant_protocols.append(protocol)
        
        # If no specific matches, include top protocols from each category
        if not relevant_protocols:
            categories_included = set()
            for protocol in self.enhanced_protocols:
                if protocol['category'] not in categories_included:
                    relevant_protocols.append(protocol)
                    categories_included.add(protocol['category'])
                    if len(categories_included) >= 3:  # Top 3 categories
                        break
        
        return relevant_protocols[:6]  # Return top 6 most relevant
        
    def _extract_peptide_names(self, text: str) -> List[str]:
        """Extract peptide names mentioned in text"""
        peptide_names = []
        text_lower = text.lower()
        
        for protocol in self.enhanced_protocols:
            if protocol['name'].lower() in text_lower:
                peptide_names.append(protocol['name'])
                continue
            
            # Check aliases
            for alias in protocol.get('aliases', []):
                if alias.lower() in text_lower:
                    peptide_names.append(protocol['name'])
                    break
        
        return peptide_names
    
    def check_contraindications(self, patient_data: Dict[str, Any], peptides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Advanced contraindication checking based on hospital-grade safety protocols
        """
        contraindications = []
        
        # Extract patient conditions, medications, and allergies
        conditions = self._extract_conditions(patient_data)
        allergies = self._extract_allergies(patient_data)
        medications = self._extract_medications(patient_data)
        
        # Normalize for matching
        conditions_lower = [c.lower() for c in conditions if c]
        allergies_lower = [a.lower() for a in allergies if a]
        medications_lower = [m.lower() for m in medications if m]
        
        for peptide in peptides:
            peptide_name = peptide.get('name', '').lower()
            if not peptide_name:
                continue
                
            # Universal contraindications for all peptides
            # Cancer screening
            if any(cancer_term in ' '.join(conditions_lower) for cancer_term in 
                  ['cancer', 'malignancy', 'tumor', 'carcinoma', 'lymphoma', 'leukemia', 'melanoma']):
                if peptide_name in ['bpc-157', 'tb-500', 'ghk-cu', 'thymosin alpha-1', 'epithalon']:
                    contraindications.append({
                        'peptide': peptide_name,
                        'condition': 'active_cancer',
                        'severity': 'high',
                        'explanation': f"{peptide_name.upper()} may stimulate cell growth and is contraindicated with active cancer or cancer history",
                        'clinical_action': 'Absolute contraindication - do not prescribe'
                    })
            
            # Pregnancy/lactation screening
            if any(term in ' '.join(conditions_lower) for term in ['pregnant', 'pregnancy', 'breastfeeding', 'lactating']):
                contraindications.append({
                    'peptide': peptide_name,
                    'condition': 'pregnancy_lactation',
                    'severity': 'high',
                    'explanation': f"{peptide_name.upper()} safety not established in pregnancy/lactation",
                    'clinical_action': 'Absolute contraindication - discontinue if pregnancy suspected'
                })
            
            # Peptide-specific contraindications
            if 'bpc-157' in peptide_name or 'bpc157' in peptide_name:
                if any(term in ' '.join(conditions_lower) for term in ['gastric cancer', 'stomach cancer', 'gi cancer']):
                    contraindications.append({
                        'peptide': 'bpc-157',
                        'condition': 'gastrointestinal_cancer',
                        'severity': 'high',
                        'explanation': 'BPC-157 may accelerate GI cancer progression',
                        'clinical_action': 'Absolute contraindication'
                    })
            
            # TB-500 autoimmune screening
            if 'tb-500' in peptide_name or 'thymosin beta' in peptide_name:
                if any(term in ' '.join(conditions_lower) for term in 
                      ['autoimmune', 'lupus', 'rheumatoid arthritis', 'multiple sclerosis', 'ms', 'crohns']):
                    contraindications.append({
                        'peptide': 'tb-500',
                        'condition': 'autoimmune_disorder',
                        'severity': 'medium',
                        'explanation': 'TB-500 may modulate immune function in unpredictable ways',
                        'clinical_action': 'Use with extreme caution, frequent monitoring required'
                    })
            
            # GH peptide endocrine screening
            if any(gh_term in peptide_name for gh_term in ['cjc', 'ipamorelin', 'ghrp', 'sermorelin', 'tesamorelin']):
                if any(term in ' '.join(conditions_lower) for term in ['diabetes', 'insulin resistance', 'hyperglycemia']):
                    contraindications.append({
                        'peptide': peptide_name,
                        'condition': 'diabetes_metabolic',
                        'severity': 'medium',
                        'explanation': f"{peptide_name.upper()} affects glucose metabolism",
                        'clinical_action': 'Close glucose monitoring, possible insulin adjustment required'
                    })
                
                if any(term in ' '.join(conditions_lower) for term in ['acromegaly', 'pituitary adenoma', 'pituitary disorder']):
                    contraindications.append({
                        'peptide': peptide_name,
                        'condition': 'pituitary_disorder',
                        'severity': 'high',
                        'explanation': f"{peptide_name.upper()} stimulates GH - dangerous with pituitary disorders",
                        'clinical_action': 'Absolute contraindication'
                    })
            
            # PT-141/Melanotan cardiovascular screening
            if any(term in peptide_name for term in ['pt-141', 'bremelanotide', 'melanotan']):
                if any(term in ' '.join(conditions_lower) for term in 
                      ['cardiovascular disease', 'heart disease', 'hypertension', 'stroke', 'heart attack']):
                    contraindications.append({
                        'peptide': peptide_name,
                        'condition': 'cardiovascular_disease',
                        'severity': 'high',
                        'explanation': f"{peptide_name.upper()} can cause significant blood pressure changes",
                        'clinical_action': 'Contraindicated with uncontrolled CVD'
                    })
            
            # Thymosin Alpha-1 immunosuppression screening
            if 'thymosin alpha' in peptide_name:
                if any(term in ' '.join(conditions_lower) for term in ['transplant', 'immunosuppressed', 'organ rejection']):
                    contraindications.append({
                        'peptide': 'thymosin-alpha-1',
                        'condition': 'immunosuppression',
                        'severity': 'medium',
                        'explanation': 'May interfere with immunosuppressive therapy',
                        'clinical_action': 'Coordinate with transplant team'
                    })
            
            # Allergy screening
            if peptide_name in ' '.join(allergies_lower):
                contraindications.append({
                    'peptide': peptide_name,
                    'condition': 'known_allergy',
                    'severity': 'high',
                    'explanation': f"Patient has documented allergy to {peptide_name.upper()}",
                    'clinical_action': 'Absolute contraindication'
                })
        
        return contraindications

    async def analyze_patient_case(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive patient case analysis for protocol generation
        """
        try:
            # Validate input data type
            if not isinstance(patient_data, dict):
                logging.error(f"Invalid patient_data type: {type(patient_data)}, expected dict")
                return {
                    "success": False,
                    "error": f"Invalid patient data format: expected dict, got {type(patient_data)}",
                    "analysis": "Unable to complete analysis due to data format issues.",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            # Create detailed analysis prompt
            analysis_prompt = self._create_case_analysis_prompt(patient_data)
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": analysis_prompt}
            ]
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent medical analysis
                max_tokens=3000
            )
            
            analysis = response.choices[0].message.content
            
            # Safely extract patient name
            patient_name = "Unknown"
            if isinstance(patient_data.get("demographics"), dict):
                patient_name = patient_data["demographics"].get("name", "Unknown")
            elif "patient_name" in patient_data:
                patient_name = patient_data.get("patient_name", "Unknown")
            
            return {
                "success": True,
                "analysis": analysis,
                "patient_id": patient_name,
                "timestamp": datetime.utcnow().isoformat(),
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logging.error(f"Patient case analysis error: {e}")
            return {
                "success": False,
                "error": str(e),
                "analysis": "Unable to complete analysis due to technical issues. Please consult with a healthcare provider.",
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def check_drug_interactions(self, peptides: List[Dict[str, Any]], patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Hospital-grade drug interaction analysis
        """
        interactions = []
        medications = self._extract_medications(patient_data)
        medications_lower = [med.lower() for med in medications if med]
        
        # Comprehensive interaction patterns based on clinical evidence
        interaction_patterns = [
            {
                'peptides': ['bpc-157'],
                'medications': ['corticosteroid', 'prednisone', 'dexamethasone', 'methylprednisolone', 'hydrocortisone'],
                'severity': 'medium',
                'explanation': 'BPC-157 may reduce corticosteroid effectiveness through opposing mechanisms',
                'clinical_action': 'Separate administration by 4+ hours, monitor therapeutic response'
            },
            {
                'peptides': ['cjc-1295', 'ipamorelin', 'ghrp', 'sermorelin', 'tesamorelin'],
                'medications': ['insulin', 'metformin', 'glipizide', 'glyburide', 'glimepiride', 'januvia', 'jardiance', 'ozempic', 'trulicity'],
                'severity': 'medium',
                'explanation': 'GH peptides affect glucose metabolism - diabetes medication adjustment may be required',
                'clinical_action': 'Frequent blood glucose monitoring, titrate diabetes medications as needed'
            },
            {
                'peptides': ['thymosin alpha-1', 'thymosin beta-4'],
                'medications': ['cyclosporine', 'tacrolimus', 'sirolimus', 'mycophenolate', 'azathioprine', 'rituximab'],
                'severity': 'high',
                'explanation': 'Thymosin peptides may counteract immunosuppressive effects',
                'clinical_action': 'Contraindicated without transplant/oncology specialist approval'
            },
            {
                'peptides': ['pt-141', 'bremelanotide', 'melanotan', 'melanotan ii'],
                'medications': ['viagra', 'sildenafil', 'cialis', 'tadalafil', 'levitra', 'vardenafil'],
                'severity': 'high',
                'explanation': 'Additive hypotensive effects - risk of severe hypotension',
                'clinical_action': 'Avoid concurrent use, separate by 24+ hours minimum'
            },
            {
                'peptides': ['selank', 'semax'],
                'medications': ['ssri', 'prozac', 'fluoxetine', 'zoloft', 'sertraline', 'lexapro', 'escitalopram', 'celexa', 'citalopram'],
                'severity': 'medium',
                'explanation': 'Potential serotonergic interactions - monitor for serotonin syndrome',
                'clinical_action': 'Start with lowest dose, monitor for serotonin syndrome symptoms'
            }
        ]
        
        for peptide in peptides:
            peptide_name = peptide.get('name', '').lower()
            if not peptide_name:
                continue
            
            for pattern in interaction_patterns:
                if any(p in peptide_name for p in pattern['peptides']):
                    interacting_meds = []
                    for medication in medications_lower:
                        if any(med in medication for med in pattern['medications']):
                            interacting_meds.append(medication)
                    
                    if interacting_meds:
                        interactions.append({
                            'peptide': peptide_name,
                            'medications': interacting_meds,
                            'severity': pattern['severity'],
                            'explanation': pattern['explanation'],
                            'clinical_action': pattern['clinical_action'],
                            'monitoring_requirements': self._get_interaction_monitoring(peptide_name, interacting_meds)
                        })
        
        return interactions
    
    def validate_dosages(self, peptides: List[Dict[str, Any]], patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Advanced dosage validation with safety calculations
        """
        dosage_issues = []
        
        # Extract patient characteristics
        weight_kg = patient_data.get('weight', 70)
        age = patient_data.get('age', 40)
        gender = patient_data.get('gender', 'unknown').lower()
        
        # Check for kidney/liver disease
        conditions = self._extract_conditions(patient_data)
        has_kidney_disease = any(term in ' '.join(conditions).lower() for term in 
                               ['kidney disease', 'renal', 'ckd', 'dialysis', 'nephropathy'])
        has_liver_disease = any(term in ' '.join(conditions).lower() for term in 
                              ['liver disease', 'hepatitis', 'cirrhosis', 'hepatic'])
        
        for peptide in peptides:
            peptide_name = peptide.get('name', '').lower()
            dosage = peptide.get('dosage', '250mcg')  # Default dosage for analysis
            
            if not peptide_name:
                continue
            
            # Extract dosage value and unit
            dosage_match = re.search(r'(\d+\.?\d*)\s*(mcg|µg|ug|mg)', dosage.lower())
            if not dosage_match:
                continue
            
            dosage_value = float(dosage_match.group(1))
            dosage_unit = dosage_match.group(2)
            
            # Convert to mcg for standardization
            if dosage_unit == 'mg':
                dosage_value *= 1000
            
            # Peptide-specific safety limits
            if 'bpc-157' in peptide_name:
                if dosage_value > 500:
                    dosage_issues.append({
                        'peptide': 'bpc-157',
                        'issue': 'excessive_dosage',
                        'severity': 'high',
                        'explanation': f"BPC-157 {dosage} exceeds maximum safe dose of 500mcg/day",
                        'clinical_action': 'Reduce to ≤500mcg/day, monitor for side effects'
                    })
                elif dosage_value < 100:
                    dosage_issues.append({
                        'peptide': 'bpc-157',
                        'issue': 'subtherapeutic_dosage',
                        'severity': 'low',
                        'explanation': f"BPC-157 {dosage} below therapeutic minimum of 100mcg/day",
                        'clinical_action': 'Consider increasing dose for therapeutic effect'
                    })
            
            # TB-500 dosage validation
            if 'tb-500' in peptide_name:
                if dosage_value > 10000:  # 10mg in mcg
                    dosage_issues.append({
                        'peptide': 'tb-500',
                        'issue': 'excessive_dosage',
                        'severity': 'medium',
                        'explanation': f"TB-500 {dosage} exceeds recommended maximum of 10mg/week",
                        'clinical_action': 'Reduce dose, split into smaller more frequent injections'
                    })
            
            # Weight-based dosing for GH peptides
            if any(gh_term in peptide_name for gh_term in ['cjc', 'ipamorelin', 'ghrp', 'sermorelin']):
                max_safe_dose = weight_kg * 2  # 2mcg/kg safety limit
                if dosage_value > max_safe_dose:
                    dosage_issues.append({
                        'peptide': peptide_name,
                        'issue': 'weight_based_overdose',
                        'severity': 'medium',
                        'explanation': f"{peptide_name.upper()} {dosage} exceeds weight-based maximum of {max_safe_dose}mcg for {weight_kg}kg patient",
                        'clinical_action': f'Reduce to ≤{max_safe_dose}mcg based on patient weight'
                    })
            
            # Age-based adjustments
            if age > 75:
                dosage_issues.append({
                    'peptide': peptide_name,
                    'issue': 'elderly_dosing',
                    'severity': 'low',
                    'explanation': f"Patient age {age} years - consider dose reduction",
                    'clinical_action': 'Start at 75% of standard dose, titrate based on tolerance'
                })
            
            # Organ dysfunction adjustments
            if has_kidney_disease:
                dosage_issues.append({
                    'peptide': peptide_name,
                    'issue': 'renal_impairment',
                    'severity': 'medium',
                    'explanation': 'Kidney disease present - dose reduction recommended',
                    'clinical_action': 'Reduce dose by 25-50%, monitor renal function'
                })
            
            if has_liver_disease:
                dosage_issues.append({
                    'peptide': peptide_name,
                    'issue': 'hepatic_impairment',
                    'severity': 'medium',
                    'explanation': 'Liver disease present - metabolism may be impaired',
                    'clinical_action': 'Consider dose reduction, monitor liver function'
                })
        
        return dosage_issues
    
    def _extract_conditions(self, patient_data: Dict[str, Any]) -> List[str]:
        """Extract medical conditions from patient data"""
        conditions = []
        
        # From medical history
        if 'medical_history' in patient_data and isinstance(patient_data['medical_history'], dict):
            conditions.extend(patient_data['medical_history'].get('conditions', []))
        
        # From direct conditions field
        if 'conditions' in patient_data:
            if isinstance(patient_data['conditions'], list):
                conditions.extend(patient_data['conditions'])
            elif isinstance(patient_data['conditions'], str):
                conditions.append(patient_data['conditions'])
        
        return conditions
    
    def _extract_allergies(self, patient_data: Dict[str, Any]) -> List[str]:
        """Extract allergies from patient data"""
        allergies = []
        
        if 'medical_history' in patient_data and isinstance(patient_data['medical_history'], dict):
            allergies.extend(patient_data['medical_history'].get('allergies', []))
        
        if 'allergies' in patient_data:
            if isinstance(patient_data['allergies'], list):
                allergies.extend(patient_data['allergies'])
            elif isinstance(patient_data['allergies'], str):
                allergies.append(patient_data['allergies'])
        
        return allergies
    
    def _extract_medications(self, patient_data: Dict[str, Any]) -> List[str]:
        """Extract medications from patient data"""
        medications = []
        
        if 'medical_history' in patient_data and isinstance(patient_data['medical_history'], dict):
            medications.extend(patient_data['medical_history'].get('medications', []))
        
        if 'medications' in patient_data:
            if isinstance(patient_data['medications'], list):
                medications.extend(patient_data['medications'])
            elif isinstance(patient_data['medications'], str):
                medications.append(patient_data['medications'])
        
        return medications
    
    def _get_interaction_monitoring(self, peptide_name: str, medications: List[str]) -> List[str]:
        """Get specific monitoring requirements for drug interactions"""
        monitoring = []
        
        if any('insulin' in med or 'metformin' in med for med in medications):
            monitoring.extend([
                'Monitor blood glucose daily for first 2 weeks',
                'Check HbA1c at 3 months',
                'Adjust diabetes medications as needed'
            ])
        
        if any('sildenafil' in med or 'tadalafil' in med for med in medications):
            monitoring.extend([
                'Blood pressure monitoring',
                'Cardiovascular assessment',
                'Avoid concurrent use - separate by 24+ hours'
            ])
        
        if any('ssri' in med or 'fluoxetine' in med for med in medications):
            monitoring.extend([
                'Monitor for serotonin syndrome symptoms',
                'Start with lowest peptide dose',
                'Weekly assessment for first month'
            ])
        
        return monitoring
    
    def _calculate_safety_score(self, contraindications: List[Dict], interactions: List[Dict], dosage_issues: List[Dict]) -> Dict[str, Any]:
        """Calculate comprehensive safety score for the protocol"""
        score = 100  # Start with perfect score
        
        # Deduct points for safety issues
        for contraindication in contraindications:
            if contraindication.get('severity') == 'high':
                score -= 25  # Major deduction for high-severity contraindications
            elif contraindication.get('severity') == 'medium':
                score -= 10
            else:
                score -= 5
        
        for interaction in interactions:
            if interaction.get('severity') == 'high':
                score -= 20
            elif interaction.get('severity') == 'medium':
                score -= 8
            else:
                score -= 3
        
        for dosage_issue in dosage_issues:
            if dosage_issue.get('severity') == 'high':
                score -= 15
            elif dosage_issue.get('severity') == 'medium':
                score -= 6
            else:
                score -= 2
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        # Determine safety level
        if score >= 90:
            safety_level = "EXCELLENT"
            recommendation = "Protocol approved for implementation with standard monitoring"
        elif score >= 75:
            safety_level = "GOOD"
            recommendation = "Protocol acceptable with enhanced monitoring recommended"
        elif score >= 60:
            safety_level = "CAUTION"
            recommendation = "Protocol requires careful consideration and frequent monitoring"
        elif score >= 40:
            safety_level = "HIGH_RISK"
            recommendation = "Protocol requires specialist consultation and intensive monitoring"
        else:
            safety_level = "CONTRAINDICATED"
            recommendation = "Protocol not recommended - consider alternative approaches"
        
        return {
            "safety_score": score,
            "safety_level": safety_level,
            "recommendation": recommendation,
            "total_issues": len(contraindications) + len(interactions) + len(dosage_issues),
            "critical_issues": len([c for c in contraindications if c.get('severity') == 'high']) + 
                             len([i for i in interactions if i.get('severity') == 'high']) +
                             len([d for d in dosage_issues if d.get('severity') == 'high'])
        }

    def _create_case_analysis_prompt(self, patient_data: Dict[str, Any]) -> str:
        """Create detailed prompt for patient case analysis"""
        
        demographics = patient_data.get("demographics", {})
        primary_concerns = patient_data.get("primary_concerns", [])
        health_goals = patient_data.get("health_goals", [])
        medical_history = patient_data.get("medical_history", [])
        current_medications = patient_data.get("current_medications", [])
        allergies = patient_data.get("allergies", [])
        lifestyle_factors = patient_data.get("lifestyle_factors", {})
        lab_results = patient_data.get("lab_results", {})
        genetic_data = patient_data.get("genetic_data", {})
        uploaded_files = patient_data.get("uploaded_files", [])
        
        prompt = f"""
Please provide a comprehensive functional medicine analysis for this patient case:

PATIENT DEMOGRAPHICS:
- Name: {demographics.get('name', 'Not provided')}
- Age: {demographics.get('age', 'Not provided')}
- Gender: {demographics.get('gender', 'Not provided')}
- Weight: {demographics.get('weight', 'Not provided')} lbs
- Height: {demographics.get('height', {}).get('feet', 'Not provided')}'{demographics.get('height', {}).get('inches', 'Not provided')}"

PRIMARY HEALTH CONCERNS:
{chr(10).join([f"- {concern}" for concern in primary_concerns]) if primary_concerns else "None specified"}

HEALTH GOALS:
{chr(10).join([f"- {goal}" for goal in health_goals]) if health_goals else "None specified"}

MEDICAL HISTORY:
{chr(10).join([f"- {condition}" for condition in medical_history]) if medical_history else "None reported"}

CURRENT MEDICATIONS:
{chr(10).join([f"- {med}" for med in current_medications]) if current_medications else "None reported"}

ALLERGIES:
{chr(10).join([f"- {allergy}" for allergy in allergies]) if allergies else "None reported"}

LIFESTYLE FACTORS:
- Exercise: {lifestyle_factors.get('exercise', 'Not specified')}
- Sleep Quality: {lifestyle_factors.get('sleep', 'Not specified')}
- Stress Level: {lifestyle_factors.get('stress', 'Not specified')}
- Diet Type: {lifestyle_factors.get('diet', 'Not specified')}

LAB RESULTS:
{json.dumps(lab_results, indent=2) if lab_results else "No lab results provided"}

GENETIC DATA:
{json.dumps(genetic_data, indent=2) if genetic_data else "No genetic data provided"}

UPLOADED FILES ANALYSIS:
{chr(10).join([f"- {file.get('filename', 'Unknown')}: {file.get('analysis', {}).get('summary', 'No analysis')}" for file in uploaded_files]) if uploaded_files else "No files uploaded"}

ANALYSIS REQUEST:
As Dr. Peptide, provide a comprehensive functional medicine analysis including:

1. ROOT CAUSE ANALYSIS: Identify potential underlying causes contributing to the patient's concerns

2. PEPTIDE PROTOCOL RECOMMENDATIONS:
   - Primary peptides with specific dosing protocols
   - Supporting peptides if appropriate
   - Duration and monitoring recommendations
   - Safety considerations and contraindications

3. INTEGRATIVE APPROACH:
   - Nutritional recommendations
   - Lifestyle modifications
   - Supplement protocols
   - Monitoring biomarkers

4. EXPECTED OUTCOMES & TIMELINE:
   - Short-term improvements (2-4 weeks)
   - Medium-term goals (8-12 weeks)
   - Long-term optimization (3-6 months)

5. SAFETY & MONITORING:
   - Required lab monitoring
   - Warning signs to watch for
   - When to adjust protocols

Please provide specific, actionable recommendations while emphasizing the importance of medical supervision and proper monitoring.
"""
        return prompt

    async def interpret_lab_results(self, lab_data: Dict[str, Any], patient_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Functional medicine interpretation of lab results
        """
        try:
            # Create lab interpretation prompt
            lab_prompt = self._create_lab_interpretation_prompt(lab_data, patient_context)
            
            messages = [
                {"role": "system", "content": self.system_prompt + "\n\nFocus on functional medicine lab interpretation with optimal ranges, not just reference ranges."},
                {"role": "user", "content": lab_prompt}
            ]
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.2,  # Very low temperature for lab interpretation
                max_tokens=2000
            )
            
            interpretation = response.choices[0].message.content
            
            return {
                "success": True,
                "interpretation": interpretation,
                "timestamp": datetime.utcnow().isoformat(),
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logging.error(f"Lab interpretation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "interpretation": "Unable to interpret lab results due to technical issues.",
                "timestamp": datetime.utcnow().isoformat()
            }

    def _create_lab_interpretation_prompt(self, lab_data: Dict[str, Any], patient_context: Optional[Dict[str, Any]]) -> str:
        """Create prompt for lab result interpretation"""
        
        context_info = ""
        if patient_context:
            context_info = f"""
PATIENT CONTEXT:
- Age: {patient_context.get('age', 'Not provided')}
- Gender: {patient_context.get('gender', 'Not provided')}
- Primary Concerns: {', '.join(patient_context.get('primary_concerns', []))}
- Health Goals: {', '.join(patient_context.get('health_goals', []))}
"""

        prompt = f"""
Please provide a comprehensive functional medicine interpretation of these lab results:

{context_info}

LAB RESULTS:
{json.dumps(lab_data, indent=2)}

INTERPRETATION REQUEST:
As Dr. Peptide, provide a detailed functional medicine analysis including:

1. KEY FINDINGS:
   - Values outside optimal functional ranges
   - Patterns and relationships between markers
   - Root cause implications

2. FUNCTIONAL MEDICINE INSIGHTS:
   - What these results suggest about underlying physiology
   - Potential nutrient deficiencies or imbalances
   - Inflammatory or metabolic patterns

3. PEPTIDE THERAPY OPPORTUNITIES:
   - Which peptides could address identified issues
   - How lab results inform peptide selection and dosing

4. ADDITIONAL TESTING RECOMMENDATIONS:
   - Follow-up labs to consider
   - Specialized functional tests that might be helpful

5. LIFESTYLE & NUTRITION RECOMMENDATIONS:
   - Specific dietary modifications based on results
   - Targeted supplements to optimize markers
   - Lifestyle interventions

Please use optimal functional ranges rather than just standard reference ranges, and explain the significance of each finding in terms of overall health optimization.
"""
        return prompt

    async def generate_protocol_rationale(self, peptide_selections: List[str], patient_concerns: List[str]) -> Dict[str, Any]:
        """
        Generate detailed rationale for peptide protocol selections
        """
        try:
            rationale_prompt = f"""
As Dr. Peptide, please explain the rationale for selecting these peptides for a patient with the following concerns:

SELECTED PEPTIDES:
{chr(10).join([f"- {peptide}" for peptide in peptide_selections])}

PATIENT CONCERNS:
{chr(10).join([f"- {concern}" for concern in patient_concerns])}

Please provide:
1. Why each peptide was selected for these specific concerns
2. How they work synergistically together
3. Expected timeline for improvements
4. Key monitoring points
5. Safety considerations

Keep the explanation clear and educational for both practitioners and patients.
"""

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": rationale_prompt}
            ]
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.4,
                max_tokens=1500
            )
            
            rationale = response.choices[0].message.content
            
            return {
                "success": True,
                "rationale": rationale,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Protocol rationale generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "rationale": "Unable to generate rationale due to technical issues."
            }

    async def suggest_monitoring_plan(self, protocol_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive monitoring plan for peptide protocol
        """
        try:
            monitoring_prompt = f"""
Create a comprehensive monitoring plan for this peptide protocol:

PROTOCOL DETAILS:
{json.dumps(protocol_data, indent=2)}

Please provide a structured monitoring plan including:

1. BASELINE ASSESSMENTS (before starting):
   - Required lab tests
   - Physical assessments
   - Baseline measurements

2. ONGOING MONITORING SCHEDULE:
   - Weekly check-points
   - Monthly evaluations
   - Quarterly assessments

3. SAFETY MONITORING:
   - Warning signs to watch for
   - When to contact healthcare provider
   - Dose adjustment criteria

4. EFFICACY TRACKING:
   - Key metrics to monitor
   - Patient-reported outcomes
   - Objective measurements

5. PROTOCOL OPTIMIZATION:
   - When to adjust dosing
   - Duration recommendations
   - Cycling protocols if needed

Format as a clear, actionable monitoring plan.
"""

            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": monitoring_prompt}
            ]
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.3,
                max_tokens=2000
            )
            
            monitoring_plan = response.choices[0].message.content
            
            return {
                "success": True,
                "monitoring_plan": monitoring_plan,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Monitoring plan generation error: {e}")
            return {
                "success": False,
                "error": str(e),
                "monitoring_plan": "Unable to generate monitoring plan due to technical issues."
            }

    async def process_chat(self, message: str) -> str:
        """
        Simple chat processing method for collective intelligence integration
        """
        try:
            response = await self.chat_with_dr_peptide(message)
            if response.get("success"):
                return response.get("response", "")
            else:
                return "I apologize, but I'm experiencing technical difficulties. Please try again later."
        except Exception as e:
            logging.error(f"Process chat error: {e}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again later."