"""
Advanced Practitioner Tools - Clinical Intelligence Suite
Provides clinical reasoning engine and practice integration features
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import logging
import re

logger = logging.getLogger(__name__)

class AdvancedPractitionerTools:
    def __init__(self):
        # Clinical reasoning templates
        self.differential_diagnosis_patterns = {
            'metabolic_syndrome': {
                'pattern': ['weight gain', 'fatigue', 'insulin resistance', 'elevated glucose'],
                'confidence_threshold': 0.7,
                'primary_consideration': 'Metabolic syndrome with insulin resistance',
                'secondary_considerations': ['PCOS', 'Hypothyroidism', 'Cushing syndrome'],
                'recommended_workup': ['HbA1c', 'Fasting insulin', 'Lipid panel', 'OGTT']
            },
            'hpa_axis_dysfunction': {
                'pattern': ['fatigue', 'stress', 'cortisol', 'sleep issues', 'brain fog'],
                'confidence_threshold': 0.6,
                'primary_consideration': 'HPA axis dysfunction/Adrenal fatigue',
                'secondary_considerations': ['Depression', 'Sleep disorders', 'Chronic fatigue syndrome'],
                'recommended_workup': ['Cortisol rhythm', 'DHEA-S', 'Pregnenolone', 'Sleep study']
            },
            'thyroid_dysfunction': {
                'pattern': ['fatigue', 'weight', 'brain fog', 'cold', 'hair loss'],
                'confidence_threshold': 0.65,
                'primary_consideration': 'Thyroid dysfunction',
                'secondary_considerations': ['Subclinical hypothyroidism', 'Thyroid resistance', 'Hashimoto\'s'],
                'recommended_workup': ['TSH', 'Free T4', 'Free T3', 'Reverse T3', 'TPO antibodies']
            },
            'hormonal_imbalance': {
                'pattern': ['irregular cycles', 'low libido', 'mood changes', 'hot flashes'],
                'confidence_threshold': 0.6,
                'primary_consideration': 'Sex hormone imbalance',
                'secondary_considerations': ['Perimenopause', 'PCOS', 'Testosterone deficiency'],
                'recommended_workup': ['Estradiol', 'Progesterone', 'Testosterone', 'LH', 'FSH']
            }
        }
        
        # ICD-10 and CPT code mappings
        self.icd10_codes = {
            'metabolic_syndrome': 'E88.81',
            'insulin_resistance': 'R73.9',
            'obesity': 'E66.9',
            'fatigue': 'R53.1',
            'hypothyroidism': 'E03.9',
            'testosterone_deficiency': 'E29.1',
            'sleep_disorder': 'G47.9',
            'depression': 'F32.9'
        }
        
        self.cpt_codes = {
            'comprehensive_metabolic_panel': '80053',
            'lipid_panel': '80061',
            'thyroid_function': '84439',
            'testosterone_total': '84403',
            'insulin_level': '83525',
            'cortisol': '82533',
            'vitamin_d': '82306',
            'hba1c': '83036'
        }
        
        # Clinical pearls database
        self.clinical_pearls = {
            'semaglutide': [
                "GLP-1 receptors in the brain may explain cognitive benefits beyond weight loss",
                "Titrate slowly to minimize GI side effects - patient adherence is key",
                "Monitor for delayed gastric emptying which can affect other medication absorption",
                "Consider cardioprotective effects in high-risk patients",
                "Injection site rotation prevents lipodystrophy"
            ],
            'bpc157': [
                "Most effective for acute injuries when started within 24-48 hours",
                "Systemic effects suggest it works beyond local injection sites",
                "May enhance gut barrier function - beneficial for leaky gut syndrome",
                "Consider cycling (4 weeks on, 2 weeks off) for chronic conditions",
                "Monitor for excessive tissue growth with prolonged use"
            ],
            'testosterone_therapy': [
                "Check hematocrit at 3 and 6 months, then annually",
                "Morning testosterone levels most accurate for diagnosis",
                "Consider aromatase inhibitor if estradiol rises >40 pg/mL",
                "Sleep apnea screening before initiation in high-risk patients",
                "Monitor prostate health with PSA and DRE"
            ]
        }
        
        # Prior authorization templates
        self.prior_auth_templates = {
            'semaglutide_weight_loss': {
                'template': '''
PRIOR AUTHORIZATION REQUEST - SEMAGLUTIDE (WEGOVY)

Patient: {patient_name}
DOB: {date_of_birth}
Diagnosis: Obesity (ICD-10: E66.9)

CLINICAL JUSTIFICATION:
- BMI: {bmi} kg/m² (>30 or >27 with comorbidities)
- Failed conventional weight loss interventions
- Comorbidities: {comorbidities}
- Clinical indicators support GLP-1 therapy

SUPPORTING DOCUMENTATION:
- Recent lab work showing metabolic dysfunction
- Documentation of lifestyle intervention failures
- No contraindications to GLP-1 therapy
- Patient understands risks and benefits

Expected outcome: 10-15% weight reduction over 68 weeks
Monitoring plan: Monthly visits, quarterly labs
''',
                'required_fields': ['patient_name', 'date_of_birth', 'bmi', 'comorbidities']
            }
        }

    def generate_clinical_reasoning(self, patient_data: Dict, assessment_data: Dict) -> Dict[str, Any]:
        """Generate comprehensive clinical reasoning and differential diagnosis"""
        try:
            # Extract key clinical features
            age = int(patient_data.get('age', 40))
            gender = patient_data.get('gender', 'Unknown')
            primary_concerns = patient_data.get('primary_concerns', [])
            medical_history = patient_data.get('medical_history', [])
            
            # Convert all text to lowercase for pattern matching
            all_text = ' '.join([
                ' '.join(str(c) for c in primary_concerns),
                ' '.join(str(h) for h in medical_history),
                str(patient_data.get('lifestyle_factors', {}))
            ]).lower()
            
            # Match differential diagnosis patterns
            differential_matches = []
            
            for condition, pattern_data in self.differential_diagnosis_patterns.items():
                pattern_words = pattern_data['pattern']
                matches = sum(1 for word in pattern_words if word in all_text)
                confidence = matches / len(pattern_words)
                
                if confidence >= pattern_data['confidence_threshold']:
                    differential_matches.append({
                        'condition': condition,
                        'confidence': confidence,
                        'primary_consideration': pattern_data['primary_consideration'],
                        'secondary_considerations': pattern_data['secondary_considerations'],
                        'recommended_workup': pattern_data['recommended_workup'],
                        'matched_features': [word for word in pattern_words if word in all_text]
                    })
            
            # Sort by confidence
            differential_matches.sort(key=lambda x: x['confidence'], reverse=True)
            
            # Generate clinical reasoning narrative
            reasoning_narrative = self._generate_reasoning_narrative(
                age, gender, primary_concerns, differential_matches
            )
            
            # Generate clinical pearls
            selected_peptides = assessment_data.get('recommended_peptides', [])
            clinical_pearls = self._get_relevant_clinical_pearls(selected_peptides)
            
            # Generate ICD-10 suggestions
            icd10_suggestions = self._generate_icd10_suggestions(differential_matches)
            
            return {
                'success': True,
                'clinical_reasoning': {
                    'narrative': reasoning_narrative,
                    'differential_diagnosis': differential_matches,
                    'clinical_pearls': clinical_pearls,
                    'icd10_suggestions': icd10_suggestions,
                    'age_gender_considerations': self._get_age_gender_considerations(age, gender),
                    'monitoring_considerations': self._generate_monitoring_considerations(differential_matches)
                },
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating clinical reasoning: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'clinical_reasoning': {}
            }

    def generate_practice_integration_data(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, Any]:
        """Generate data for seamless practice integration"""
        try:
            # Calculate BMI
            weight = float(patient_data.get('weight', 150))
            height_feet = int(patient_data.get('height_feet', 5))
            height_inches = int(patient_data.get('height_inches', 6))
            total_inches = (height_feet * 12) + height_inches
            bmi = (weight * 703) / (total_inches ** 2) if total_inches > 0 else 25
            
            # Generate billing codes
            billing_codes = self._generate_billing_codes(patient_data, protocol_data)
            
            # Generate prior authorization if needed
            prior_auth = self._generate_prior_authorization(patient_data, protocol_data, bmi)
            
            # Generate EHR-compatible data
            ehr_data = self._generate_ehr_data(patient_data, protocol_data)
            
            # Generate documentation templates
            documentation = self._generate_documentation_templates(patient_data, protocol_data)
            
            # Calculate insurance coverage probability
            coverage_analysis = self._analyze_insurance_coverage(protocol_data)
            
            return {
                'success': True,
                'practice_integration': {
                    'billing_codes': billing_codes,
                    'prior_authorization': prior_auth,
                    'ehr_data': ehr_data,
                    'documentation_templates': documentation,
                    'insurance_coverage': coverage_analysis,
                    'workflow_checklist': self._generate_workflow_checklist()
                },
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating practice integration data: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'practice_integration': {}
            }

    def generate_patient_education_plan(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, Any]:
        """Generate personalized patient education materials"""
        try:
            age = int(patient_data.get('age', 40))
            primary_concerns = patient_data.get('primary_concerns', [])
            selected_peptides = protocol_data.get('recommended_peptides', [])
            
            # Generate education modules based on concerns
            education_modules = []
            
            if any('weight' in str(concern).lower() for concern in primary_concerns):
                education_modules.append(self._create_weight_management_module())
            
            if any('fatigue' in str(concern).lower() for concern in primary_concerns):
                education_modules.append(self._create_energy_optimization_module())
                
            if any('brain fog' in str(concern).lower() or 'cognitive' in str(concern).lower() for concern in primary_concerns):
                education_modules.append(self._create_cognitive_health_module())
            
            # Generate peptide-specific education
            peptide_education = {}
            for peptide in selected_peptides:
                peptide_education[peptide] = self._create_peptide_education(peptide)
            
            # Generate lifestyle recommendations
            lifestyle_plan = self._generate_lifestyle_education(patient_data)
            
            # Generate expectation timeline
            expectation_timeline = self._generate_expectation_timeline(selected_peptides)
            
            return {
                'success': True,
                'patient_education': {
                    'education_modules': education_modules,
                    'peptide_education': peptide_education,
                    'lifestyle_plan': lifestyle_plan,
                    'expectation_timeline': expectation_timeline,
                    'personalization_factors': {
                        'age_group': self._get_age_group(age),
                        'primary_focus': self._identify_primary_focus(primary_concerns),
                        'learning_style_recommendations': self._suggest_learning_styles(age)
                    }
                },
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating patient education plan: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'patient_education': {}
            }

    def _generate_reasoning_narrative(self, age: int, gender: str, concerns: List, differentials: List) -> str:
        """Generate clinical reasoning narrative"""
        narrative = f"Clinical Assessment: {age}-year-old {gender.lower()} presenting with "
        narrative += ', '.join(str(c) for c in concerns[:3]) + ". "
        
        if differentials:
            top_differential = differentials[0]
            narrative += f"Primary consideration: {top_differential['primary_consideration']} "
            narrative += f"(confidence: {top_differential['confidence']:.0%}). "
            
            if len(differentials) > 1:
                narrative += "Alternative considerations include "
                narrative += ', '.join(d['primary_consideration'] for d in differentials[1:3])
                narrative += ". "
        
        # Age-specific considerations
        if age > 45:
            narrative += "Age-related hormonal changes may contribute to symptom complex. "
        elif age < 35:
            narrative += "Consider lifestyle and stress factors given patient age. "
        
        return narrative

    def _get_relevant_clinical_pearls(self, peptides: List[str]) -> List[str]:
        """Get relevant clinical pearls for selected peptides"""
        pearls = []
        for peptide in peptides:
            peptide_key = peptide.lower()
            if peptide_key in self.clinical_pearls:
                pearls.extend(self.clinical_pearls[peptide_key][:2])  # Top 2 pearls per peptide
        return pearls

    def _generate_icd10_suggestions(self, differentials: List) -> List[Dict[str, str]]:
        """Generate ICD-10 code suggestions"""
        suggestions = []
        
        for diff in differentials[:3]:  # Top 3 differentials
            condition = diff['condition']
            if condition in ['metabolic_syndrome', 'hpa_axis_dysfunction']:
                if condition == 'metabolic_syndrome':
                    suggestions.append({
                        'code': self.icd10_codes['metabolic_syndrome'],
                        'description': 'Metabolic syndrome',
                        'confidence': diff['confidence']
                    })
                elif condition == 'hpa_axis_dysfunction':
                    suggestions.append({
                        'code': self.icd10_codes['fatigue'],
                        'description': 'Chronic fatigue, unspecified',
                        'confidence': diff['confidence']
                    })
        
        # Add common codes
        suggestions.append({
            'code': self.icd10_codes['obesity'],
            'description': 'Obesity, unspecified',
            'confidence': 0.8
        })
        
        return suggestions

    def _get_age_gender_considerations(self, age: int, gender: str) -> List[str]:
        """Get age and gender specific considerations"""
        considerations = []
        
        if gender.lower() == 'female':
            if age >= 40:
                considerations.append("Consider perimenopause evaluation")
                considerations.append("Screen for PCOS if irregular cycles")
            if age >= 50:
                considerations.append("Postmenopausal hormone optimization")
        
        if gender.lower() == 'male':
            if age >= 35:
                considerations.append("Consider testosterone screening")
                considerations.append("Monitor prostate health")
        
        if age >= 65:
            considerations.append("Enhanced monitoring for elderly patients")
            considerations.append("Consider drug interaction potential")
        
        return considerations

    def _generate_monitoring_considerations(self, differentials: List) -> List[str]:
        """Generate monitoring considerations based on differentials"""
        monitoring = ["Standard vital signs and weight monitoring"]
        
        for diff in differentials:
            condition = diff['condition']
            if condition == 'metabolic_syndrome':
                monitoring.append("Monthly glucose and lipid monitoring")
            elif condition == 'thyroid_dysfunction':
                monitoring.append("Quarterly thyroid function monitoring")
            elif condition == 'hpa_axis_dysfunction':
                monitoring.append("Cortisol rhythm assessment q6 months")
        
        return list(set(monitoring))  # Remove duplicates

    def _generate_billing_codes(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, List]:
        """Generate appropriate billing codes"""
        return {
            'evaluation_management': ['99213', '99214'],  # Office visits
            'laboratory': [
                self.cpt_codes['comprehensive_metabolic_panel'],
                self.cpt_codes['lipid_panel'],
                self.cpt_codes['hba1c']
            ],
            'procedures': [],  # Injection codes if applicable
            'icd10_primary': self.icd10_codes['obesity'],
            'icd10_secondary': [self.icd10_codes['fatigue']]
        }

    def _generate_prior_authorization(self, patient_data: Dict, protocol_data: Dict, bmi: float) -> Dict[str, Any]:
        """Generate prior authorization documentation"""
        peptides = protocol_data.get('recommended_peptides', [])
        
        if any('semaglutide' in peptide.lower() for peptide in peptides):
            return {
                'required': True,
                'medication': 'Semaglutide (Wegovy)',
                'template': 'semaglutide_weight_loss',
                'required_documentation': [
                    'BMI documentation',
                    'Failed diet/exercise documentation',
                    'Comorbidity documentation',
                    'Laboratory results'
                ],
                'approval_probability': self._calculate_approval_probability(bmi, patient_data)
            }
        
        return {'required': False}

    def _generate_ehr_data(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, Any]:
        """Generate EHR-compatible structured data"""
        return {
            'patient_demographics': {
                'age': patient_data.get('age'),
                'gender': patient_data.get('gender'),
                'bmi': self._calculate_bmi(patient_data)
            },
            'chief_complaint': ', '.join(str(c) for c in patient_data.get('primary_concerns', [])),
            'plan': {
                'medications': protocol_data.get('recommended_peptides', []),
                'monitoring': 'Monthly follow-up with lab monitoring',
                'patient_education': 'Provided comprehensive peptide therapy education'
            },
            'next_appointment': (datetime.now() + timedelta(weeks=4)).strftime('%Y-%m-%d')
        }

    def _generate_documentation_templates(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, str]:
        """Generate clinical documentation templates"""
        return {
            'soap_note': self._generate_soap_note_template(patient_data, protocol_data),
            'consent_form': self._generate_consent_template(protocol_data),
            'patient_instructions': self._generate_instruction_template(protocol_data)
        }

    def _analyze_insurance_coverage(self, protocol_data: Dict) -> Dict[str, Any]:
        """Analyze insurance coverage probability"""
        peptides = protocol_data.get('recommended_peptides', [])
        coverage = {}
        
        for peptide in peptides:
            if 'semaglutide' in peptide.lower():
                coverage[peptide] = {
                    'probability': 0.65,
                    'notes': 'Good coverage for diabetes, variable for weight loss',
                    'strategies': ['Try diabetes indication first', 'Prior authorization needed']
                }
            elif 'bpc' in peptide.lower():
                coverage[peptide] = {
                    'probability': 0.05,
                    'notes': 'Rarely covered - compound pharmacy',
                    'strategies': ['Self-pay', 'HSA/FSA eligible']
                }
        
        return coverage

    def _generate_workflow_checklist(self) -> List[Dict[str, Any]]:
        """Generate practice workflow checklist"""
        return [
            {
                'step': 'Patient assessment complete',
                'status': 'pending',
                'required_actions': ['Review history', 'Physical exam', 'Lab review']
            },
            {
                'step': 'Protocol generated',
                'status': 'pending', 
                'required_actions': ['Review recommendations', 'Approve protocol']
            },
            {
                'step': 'Patient education',
                'status': 'pending',
                'required_actions': ['Provide materials', 'Discuss expectations']
            },
            {
                'step': 'Consent obtained',
                'status': 'pending',
                'required_actions': ['Review consent form', 'Patient signature']
            },
            {
                'step': 'Follow-up scheduled',
                'status': 'pending',
                'required_actions': ['Schedule next visit', 'Set lab reminders']
            }
        ]

    def _calculate_bmi(self, patient_data: Dict) -> float:
        """Calculate BMI from patient data"""
        try:
            weight = float(patient_data.get('weight', 150))
            height_feet = int(patient_data.get('height_feet', 5))
            height_inches = int(patient_data.get('height_inches', 6))
            total_inches = (height_feet * 12) + height_inches
            return round((weight * 703) / (total_inches ** 2), 1)
        except:
            return 25.0

    def _calculate_approval_probability(self, bmi: float, patient_data: Dict) -> float:
        """Calculate prior authorization approval probability"""
        base_prob = 0.5
        
        if bmi >= 35:
            base_prob += 0.3
        elif bmi >= 30:
            base_prob += 0.2
        
        # Add for comorbidities
        medical_history = patient_data.get('medical_history', [])
        if medical_history:
            base_prob += 0.15
        
        return min(base_prob, 0.9)

    def _create_weight_management_module(self) -> Dict[str, Any]:
        """Create weight management education module"""
        return {
            'title': 'Understanding Your Weight Management Journey',
            'key_points': [
                'GLP-1 medications work by regulating appetite and blood sugar',
                'Expect gradual, sustainable weight loss of 1-2 pounds per week',
                'Combine medication with healthy eating and regular exercise',
                'Side effects typically improve after the first few weeks'
            ],
            'action_items': [
                'Track daily food intake and physical activity',
                'Monitor weekly weight at the same time of day',
                'Stay hydrated and eat adequate protein'
            ]
        }

    def _create_energy_optimization_module(self) -> Dict[str, Any]:
        """Create energy optimization education module"""
        return {
            'title': 'Optimizing Your Energy Levels',
            'key_points': [
                'Peptide therapy can help restore natural energy production',
                'Energy improvements typically seen within 4-6 weeks',
                'Sleep quality and stress management are crucial',
                'Regular exercise enhances peptide effectiveness'
            ],
            'action_items': [
                'Maintain consistent sleep schedule (7-9 hours)',
                'Practice stress reduction techniques daily',
                'Track energy levels on a 1-10 scale daily'
            ]
        }

    def _create_cognitive_health_module(self) -> Dict[str, Any]:
        """Create cognitive health education module"""
        return {
            'title': 'Supporting Cognitive Function and Mental Clarity',
            'key_points': [
                'Brain fog often relates to inflammation and metabolic dysfunction',
                'Peptides can support neuroprotection and brain health',
                'Cognitive improvements may take 6-8 weeks to fully manifest',
                'Lifestyle factors significantly impact brain function'
            ],
            'action_items': [
                'Engage in daily cognitive stimulation activities',
                'Maintain omega-3 fatty acid intake',
                'Monitor and rate mental clarity daily'
            ]
        }

    def _create_peptide_education(self, peptide: str) -> Dict[str, Any]:
        """Create peptide-specific education"""
        education_data = {
            'Semaglutide': {
                'mechanism': 'GLP-1 receptor agonist that regulates blood sugar and appetite',
                'administration': 'Weekly subcutaneous injection',
                'timeline': 'Effects begin within 1-2 weeks, peak benefits at 16-20 weeks',
                'monitoring': 'Weekly weight checks, monthly follow-ups'
            },
            'BPC-157': {
                'mechanism': 'Promotes tissue repair and reduces inflammation',
                'administration': 'Daily subcutaneous injection', 
                'timeline': 'Initial effects in 3-7 days, full benefits in 4-6 weeks',
                'monitoring': 'Injection site assessment, symptom tracking'
            }
        }
        
        return education_data.get(peptide, {
            'mechanism': 'Consult with provider for specific peptide information',
            'administration': 'As directed by healthcare provider',
            'timeline': 'Individual response may vary',
            'monitoring': 'Regular follow-up as scheduled'
        })

    def _generate_lifestyle_education(self, patient_data: Dict) -> Dict[str, List[str]]:
        """Generate personalized lifestyle recommendations"""
        return {
            'nutrition': [
                'Focus on whole foods with adequate protein',
                'Stay hydrated with 8-10 glasses of water daily',
                'Consider anti-inflammatory foods like fatty fish and leafy greens'
            ],
            'exercise': [
                'Start with 150 minutes of moderate activity per week',
                'Include strength training 2-3 times per week',
                'Listen to your body and progress gradually'
            ],
            'sleep': [
                'Maintain consistent sleep schedule',
                'Create a relaxing bedtime routine',
                'Limit screen time 1 hour before bed'
            ],
            'stress_management': [
                'Practice deep breathing or meditation daily',
                'Consider yoga or tai chi',
                'Maintain social connections and hobbies'
            ]
        }

    def _generate_expectation_timeline(self, peptides: List[str]) -> Dict[str, str]:
        """Generate expectation timeline based on peptides"""
        return {
            'Week 1-2': 'Initial adaptation, possible mild side effects',
            'Week 3-4': 'Early therapeutic effects begin',
            'Week 6-8': 'Significant improvements typically visible',
            'Week 12+': 'Optimal therapeutic benefits achieved',
            'Ongoing': 'Maintenance of benefits with continued therapy'
        }

    def _get_age_group(self, age: int) -> str:
        """Categorize age group for personalized education"""
        if age < 35:
            return 'Young Adult'
        elif age < 50:
            return 'Middle Age'
        elif age < 65:
            return 'Mature Adult'
        else:
            return 'Senior Adult'

    def _identify_primary_focus(self, concerns: List) -> str:
        """Identify primary educational focus"""
        concern_text = ' '.join(str(c).lower() for c in concerns)
        
        if 'weight' in concern_text:
            return 'Weight Management'
        elif 'fatigue' in concern_text or 'energy' in concern_text:
            return 'Energy Optimization'
        elif 'brain fog' in concern_text or 'cognitive' in concern_text:
            return 'Cognitive Health'
        else:
            return 'General Wellness'

    def _suggest_learning_styles(self, age: int) -> List[str]:
        """Suggest appropriate learning styles based on age"""
        if age < 40:
            return ['Video content', 'Interactive apps', 'Online resources']
        elif age < 60:
            return ['Written materials', 'Video content', 'Group sessions']
        else:
            return ['Written materials', 'One-on-one education', 'Large print resources']

    def _generate_soap_note_template(self, patient_data: Dict, protocol_data: Dict) -> str:
        """Generate SOAP note template"""
        return f"""
SUBJECTIVE:
{patient_data.get('age')}-year-old {patient_data.get('gender', 'patient')} presents with chief complaints of {', '.join(str(c) for c in patient_data.get('primary_concerns', []))}.

OBJECTIVE:
Vital signs stable. Weight: {patient_data.get('weight', 'Unknown')} lbs. 
Lab results reviewed and incorporated into treatment planning.

ASSESSMENT:
Primary diagnosis based on clinical presentation and laboratory findings.
Plan for peptide therapy with {', '.join(protocol_data.get('recommended_peptides', []))}.

PLAN:
1. Initiate peptide therapy as outlined in protocol
2. Patient education provided regarding expectations and monitoring
3. Follow-up in 4 weeks
4. Laboratory monitoring as indicated
"""

    def _generate_consent_template(self, protocol_data: Dict) -> str:
        """Generate consent form template"""
        return f"""
INFORMED CONSENT FOR PEPTIDE THERAPY

I understand that I will be receiving treatment with {', '.join(protocol_data.get('recommended_peptides', []))}.

I have been informed of:
- The expected benefits and potential risks
- Alternative treatment options
- The importance of compliance and monitoring
- When to contact my healthcare provider

Patient Signature: _________________ Date: _________________
"""

    def _generate_instruction_template(self, protocol_data: Dict) -> str:
        """Generate patient instruction template"""
        return f"""
PATIENT INSTRUCTIONS

Your prescribed peptide therapy includes: {', '.join(protocol_data.get('recommended_peptides', []))}

ADMINISTRATION:
- Follow injection instructions provided
- Rotate injection sites as directed
- Store medications as instructed

MONITORING:
- Track symptoms and side effects daily
- Weigh yourself weekly at the same time
- Contact office with any concerns

FOLLOW-UP:
- Next appointment scheduled in 4 weeks
- Laboratory tests as ordered
- Emergency contact: [Office Number]
"""

# Global instance
advanced_practitioner_tools = AdvancedPractitionerTools()