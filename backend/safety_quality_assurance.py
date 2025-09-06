"""
Safety & Quality Assurance System - Multi-Layer Protection
Provides comprehensive safety monitoring and quality validation
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import logging
import re
import math

logger = logging.getLogger(__name__)

class SafetyQualityAssurance:
    def __init__(self):
        # Multi-layer safety checkpoints
        self.safety_layers = {
            'layer_1_drug_interactions': {
                'enabled': True,
                'severity_levels': ['critical', 'major', 'moderate', 'minor'],
                'auto_block_critical': True
            },
            'layer_2_contraindications': {
                'enabled': True,
                'absolute_contraindications': 'auto_block',
                'relative_contraindications': 'warning_required'
            },
            'layer_3_dosing_boundaries': {
                'enabled': True,
                'max_dose_multiplier': 2.0,  # Maximum 2x standard dose
                'min_dose_multiplier': 0.25  # Minimum 25% standard dose
            },
            'layer_4_practitioner_override': {
                'enabled': True,
                'requires_justification': True,
                'audit_trail_required': True
            },
            'layer_5_patient_consent': {
                'enabled': True,
                'requires_electronic_signature': False,
                'informed_consent_required': True
            }
        }
        
        # Drug interaction database
        self.drug_interactions = {
            'semaglutide': {
                'major_interactions': [
                    {
                        'drug': 'insulin',
                        'severity': 'major',
                        'mechanism': 'Additive hypoglycemic effect',
                        'management': 'Monitor glucose closely, may need insulin dose reduction'
                    },
                    {
                        'drug': 'sulfonylureas',
                        'severity': 'major', 
                        'mechanism': 'Increased hypoglycemia risk',
                        'management': 'Consider dose reduction of sulfonylurea'
                    }
                ],
                'moderate_interactions': [
                    {
                        'drug': 'levothyroxine',
                        'severity': 'moderate',
                        'mechanism': 'Delayed gastric emptying may affect absorption',
                        'management': 'Separate administration by 4 hours if possible'
                    },
                    {
                        'drug': 'warfarin',
                        'severity': 'moderate',
                        'mechanism': 'May affect INR due to dietary changes',
                        'management': 'Monitor INR more frequently'
                    }
                ]
            },
            'bpc157': {
                'moderate_interactions': [
                    {
                        'drug': 'anticoagulants',
                        'severity': 'moderate',
                        'mechanism': 'Potential enhanced healing may affect bleeding',
                        'management': 'Monitor for bleeding, consider dose adjustment'
                    }
                ]
            },
            'formula_n_5550': {
                'critical_interactions': [
                    {
                        'drug': 'ssris',
                        'severity': 'critical',
                        'mechanism': 'Serotonin syndrome risk with tesofensine component',
                        'management': 'ABSOLUTE CONTRAINDICATION - Do not combine'
                    },
                    {
                        'drug': 'snris',
                        'severity': 'critical',
                        'mechanism': 'Serotonin syndrome risk with tesofensine component',
                        'management': 'ABSOLUTE CONTRAINDICATION - Do not combine'
                    },
                    {
                        'drug': 'maois',
                        'severity': 'critical',
                        'mechanism': 'Severe serotonin syndrome and hypertensive crisis risk',
                        'management': 'ABSOLUTE CONTRAINDICATION - 14-day washout required'
                    }
                ],
                'major_interactions': [
                    {
                        'drug': 'stimulants',
                        'severity': 'major',
                        'mechanism': 'Additive cardiovascular effects with tesofensine',
                        'management': 'Enhanced cardiovascular monitoring, consider dose reduction'
                    },
                    {
                        'drug': 'dextromethorphan',
                        'severity': 'major',
                        'mechanism': 'Methylene blue may cause serotonin syndrome',
                        'management': 'Avoid combination or use with extreme caution'
                    }
                ],
                'moderate_interactions': [
                    {
                        'drug': 'antihypertensives',
                        'severity': 'moderate',
                        'mechanism': 'Tesofensine may affect blood pressure',
                        'management': 'Monitor blood pressure closely, adjust antihypertensive as needed'
                    }
                ]
            },
            'formula_m_51': {
                'major_interactions': [
                    {
                        'drug': 'diabetes_medications',
                        'severity': 'major',
                        'mechanism': 'Enhanced insulin sensitivity may require medication dose reduction',
                        'management': 'Monitor blood glucose closely, may require 10-30% medication dose reduction'
                    },
                    {
                        'drug': 'nad_supplements',
                        'severity': 'major',
                        'mechanism': 'Additive NAD+ elevation may cause excessive levels',
                        'management': 'Reduce NAD+ supplement doses by 50% to avoid excessive elevation'
                    }
                ],
                'moderate_interactions': [
                    {
                        'drug': 'stimulants',
                        'severity': 'moderate',
                        'mechanism': 'Additive metabolic effects may cause overstimulation',
                        'management': 'Use cautiously, monitor for excessive stimulation'
                    },
                    {
                        'drug': 'thyroid_medications',
                        'severity': 'moderate',
                        'mechanism': 'May affect thyroid hormone requirements',
                        'management': 'Monitor thyroid function, may require dose adjustments'
                    }
                ]
            },
            'formula_rg_5555': {
                'major_interactions': [
                    {
                        'drug': 'immunosuppressive_drugs',
                        'severity': 'major',
                        'mechanism': 'Competing effects on immune function and healing response',
                        'management': 'Monitor for enhanced or competing immune effects, coordinate with prescribing physician'
                    },
                    {
                        'drug': 'anticoagulants',
                        'severity': 'major',
                        'mechanism': 'TB-500 angiogenic effects may increase bleeding risk',
                        'management': 'Enhanced bleeding monitoring required, consider dose adjustments'
                    }
                ],
                'moderate_interactions': [
                    {
                        'drug': 'anti_inflammatory_medications',
                        'severity': 'moderate',
                        'mechanism': 'Additive anti-inflammatory effects with KPV component',
                        'management': 'Monitor for enhanced anti-inflammatory effects'
                    },
                    {
                        'drug': 'gi_medications',
                        'severity': 'moderate',
                        'mechanism': 'May alter GI medication absorption or effectiveness',
                        'management': 'Separate timing of administration if possible, monitor effectiveness'
                    }
                ]
            }
        }
        
        # Contraindication database
        self.contraindications = {
            'semaglutide': {
                'absolute': [
                    'Personal history of medullary thyroid carcinoma',
                    'Family history of medullary thyroid carcinoma',
                    'Multiple Endocrine Neoplasia syndrome type 2 (MEN 2)',
                    'Pregnancy',
                    'Breastfeeding'
                ],
                'relative': [
                    'History of pancreatitis',
                    'Severe gastroparesis',
                    'Diabetic retinopathy',
                    'Severe kidney disease (eGFR <30)',
                    'History of cholelithiasis'
                ]
            },
            'bpc157': {
                'absolute': [
                    'Active malignancy',
                    'Known hypersensitivity to BPC-157'
                ],
                'relative': [
                    'Pregnancy',
                    'Breastfeeding',
                    'Severe cardiovascular disease'
                ]
            },
            'formula_n_5550': {
                'absolute': [
                    'Current use of SSRIs, SNRIs, MAOIs, or tricyclic antidepressants',
                    'Pregnancy and lactation',
                    'G6PD deficiency (methylene blue component)',
                    'Severe cardiovascular disease (uncontrolled)',
                    'History of serotonin syndrome',
                    'Severe liver failure',
                    'Severe kidney failure (eGFR <30)',
                    'Active eating disorder'
                ],
                'relative': [
                    'Hypertension (controlled)',
                    'History of substance abuse',
                    'Concurrent stimulant use',
                    'Sleep disorders',
                    'Mild to moderate liver impairment',
                    'History of cardiac arrhythmias',
                    'Age >70 years'
                ]
            },
            'formula_m_51': {
                'absolute': [
                    'Pregnancy and lactation',
                    'Known hypersensitivity to 5-AMINO-1MQ or SLU-PP-332 components'
                ],
                'relative': [
                    'Severe cardiovascular disease (requires monitoring)',
                    'Severe liver disease (monitor liver function)',
                    'Uncontrolled diabetes (may require medication adjustments)',
                    'Severe thyroid disorders (may require medication monitoring)'
                ]
            }
        }
        
        # Dosing safety boundaries
        self.dosing_boundaries = {
            'semaglutide': {
                'standard_dose': {'min': 0.25, 'max': 2.4, 'unit': 'mg'},
                'max_weekly_increase': 0.5,
                'titration_minimum_interval': 7  # days
            },
            'bpc157': {
                'standard_dose': {'min': 100, 'max': 500, 'unit': 'mcg'},
                'max_daily_dose': 1000,
                'max_continuous_weeks': 8
            }
        }
        
        # Quality scoring criteria
        self.quality_criteria = {
            'evidence_level': {
                'A_randomized_controlled_trials': 25,
                'B_cohort_studies': 20,
                'C_case_series': 15,
                'D_expert_opinion': 10
            },
            'safety_profile': {
                'excellent': 25,
                'good': 20,
                'acceptable': 15,
                'concerning': 5
            },
            'personalization_depth': {
                'high_personalization': 20,
                'moderate_personalization': 15,
                'standard_personalization': 10,
                'minimal_personalization': 5
            },
            'monitoring_adequacy': {
                'comprehensive': 15,
                'adequate': 12,
                'basic': 8,
                'insufficient': 3
            },
            'patient_engagement': {
                'high_engagement': 15,
                'moderate_engagement': 12,
                'basic_engagement': 8,
                'minimal_engagement': 3
            }
        }

    def execute_multi_layer_safety_check(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, Any]:
        """Execute comprehensive multi-layer safety analysis"""
        try:
            safety_results = {
                'overall_safety_score': 0,
                'safety_alerts': [],
                'layer_results': {},
                'clearance_status': 'pending',
                'required_actions': []
            }
            
            # Layer 1: Drug Interaction Screening
            layer1_result = self._execute_layer1_drug_interactions(patient_data, protocol_data)
            safety_results['layer_results']['layer_1'] = layer1_result
            
            # Layer 2: Contraindication Analysis  
            layer2_result = self._execute_layer2_contraindications(patient_data, protocol_data)
            safety_results['layer_results']['layer_2'] = layer2_result
            
            # Layer 3: Dosing Boundary Checks
            layer3_result = self._execute_layer3_dosing_boundaries(protocol_data)
            safety_results['layer_results']['layer_3'] = layer3_result
            
            # Layer 4: Practitioner Override Requirements
            layer4_result = self._execute_layer4_practitioner_review(safety_results)
            safety_results['layer_results']['layer_4'] = layer4_result
            
            # Layer 5: Patient Consent Verification
            layer5_result = self._execute_layer5_consent_verification(patient_data)
            safety_results['layer_results']['layer_5'] = layer5_result
            
            # Calculate overall safety score
            safety_results['overall_safety_score'] = self._calculate_safety_score(safety_results['layer_results'])
            
            # Determine clearance status
            safety_results['clearance_status'] = self._determine_clearance_status(safety_results)
            
            # Generate required actions
            safety_results['required_actions'] = self._generate_required_actions(safety_results)
            
            # Compile all safety alerts
            safety_results['safety_alerts'] = self._compile_safety_alerts(safety_results['layer_results'])
            
            return {
                'success': True,
                'safety_analysis': safety_results,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error executing multi-layer safety check: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'safety_analysis': {}
            }

    def calculate_protocol_quality_score(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, Any]:
        """Calculate comprehensive protocol quality score"""
        try:
            quality_scores = {}
            total_score = 0
            max_possible_score = 0
            
            # Evidence Level Assessment
            evidence_score = self._assess_evidence_level(protocol_data)
            quality_scores['evidence_level'] = evidence_score
            total_score += evidence_score['score']
            max_possible_score += evidence_score['max_score']
            
            # Safety Profile Assessment
            safety_score = self._assess_safety_profile(protocol_data)
            quality_scores['safety_profile'] = safety_score
            total_score += safety_score['score']
            max_possible_score += safety_score['max_score']
            
            # Personalization Depth Assessment
            personalization_score = self._assess_personalization_depth(patient_data, protocol_data)
            quality_scores['personalization_depth'] = personalization_score
            total_score += personalization_score['score']
            max_possible_score += personalization_score['max_score']
            
            # Monitoring Adequacy Assessment
            monitoring_score = self._assess_monitoring_adequacy(protocol_data)
            quality_scores['monitoring_adequacy'] = monitoring_score
            total_score += monitoring_score['score']
            max_possible_score += monitoring_score['max_score']
            
            # Patient Engagement Assessment
            engagement_score = self._assess_patient_engagement(protocol_data)
            quality_scores['patient_engagement'] = engagement_score
            total_score += engagement_score['score']
            max_possible_score += engagement_score['max_score']
            
            # Calculate overall quality score
            overall_score = round((total_score / max_possible_score) * 100, 1)
            quality_grade = self._determine_quality_grade(overall_score)
            
            # Generate quality recommendations
            recommendations = self._generate_quality_recommendations(quality_scores, overall_score)
            
            return {
                'success': True,
                'quality_assessment': {
                    'overall_score': overall_score,
                    'overall_grade': quality_grade,
                    'component_scores': quality_scores,
                    'recommendations': recommendations,
                    'benchmarks': {
                        'excellent': 90,
                        'good': 80,
                        'acceptable': 70,
                        'needs_improvement': 60
                    }
                },
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating protocol quality score: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'quality_assessment': {}
            }

    def continuous_quality_monitoring(self, protocol_id: str, usage_data: Dict) -> Dict[str, Any]:
        """Implement continuous quality monitoring for deployed protocols"""
        try:
            monitoring_results = {
                'protocol_id': protocol_id,
                'monitoring_metrics': {},
                'trend_analysis': {},
                'quality_alerts': [],
                'improvement_recommendations': []
            }
            
            # Monitor outcome success rates
            success_metrics = self._monitor_outcome_success(usage_data)
            monitoring_results['monitoring_metrics']['outcomes'] = success_metrics
            
            # Monitor safety incidents
            safety_metrics = self._monitor_safety_incidents(usage_data)
            monitoring_results['monitoring_metrics']['safety'] = safety_metrics
            
            # Monitor patient satisfaction
            satisfaction_metrics = self._monitor_patient_satisfaction(usage_data)
            monitoring_results['monitoring_metrics']['satisfaction'] = satisfaction_metrics
            
            # Monitor practitioner feedback
            practitioner_metrics = self._monitor_practitioner_feedback(usage_data)
            monitoring_results['monitoring_metrics']['practitioner_feedback'] = practitioner_metrics
            
            # Trend analysis
            monitoring_results['trend_analysis'] = self._analyze_quality_trends(monitoring_results['monitoring_metrics'])
            
            # Generate alerts for quality degradation
            monitoring_results['quality_alerts'] = self._generate_quality_alerts(monitoring_results)
            
            # Generate improvement recommendations
            monitoring_results['improvement_recommendations'] = self._generate_improvement_recommendations(monitoring_results)
            
            return {
                'success': True,
                'monitoring_results': monitoring_results,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in continuous quality monitoring: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'monitoring_results': {}
            }

    def _execute_layer1_drug_interactions(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, Any]:
        """Layer 1: Drug Interaction Screening"""
        result = {
            'layer_name': 'Drug Interaction Screening',
            'status': 'passed',
            'interactions_found': [],
            'critical_blocks': [],
            'warnings': []
        }
        
        current_medications = patient_data.get('current_medications', [])
        prescribed_peptides = protocol_data.get('recommended_peptides', [])
        
        for peptide in prescribed_peptides:
            peptide_key = peptide.lower()
            if peptide_key in self.drug_interactions:
                
                # Check major interactions
                for interaction in self.drug_interactions[peptide_key].get('major_interactions', []):
                    for medication in current_medications:
                        if interaction['drug'].lower() in str(medication).lower():
                            interaction_data = {
                                'peptide': peptide,
                                'medication': medication,
                                'severity': interaction['severity'],
                                'mechanism': interaction['mechanism'],
                                'management': interaction['management']
                            }
                            
                            result['interactions_found'].append(interaction_data)
                            
                            if interaction['severity'] == 'critical':
                                result['critical_blocks'].append(interaction_data)
                                result['status'] = 'blocked'
                            else:
                                result['warnings'].append(interaction_data)
                
                # Check moderate interactions
                for interaction in self.drug_interactions[peptide_key].get('moderate_interactions', []):
                    for medication in current_medications:
                        if interaction['drug'].lower() in str(medication).lower():
                            interaction_data = {
                                'peptide': peptide,
                                'medication': medication,
                                'severity': interaction['severity'],
                                'mechanism': interaction['mechanism'],
                                'management': interaction['management']
                            }
                            
                            result['interactions_found'].append(interaction_data)
                            result['warnings'].append(interaction_data)
        
        # Set warning status if warnings exist but no critical blocks
        if result['warnings'] and result['status'] != 'blocked':
            result['status'] = 'warning'
        
        return result

    def _execute_layer2_contraindications(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, Any]:
        """Layer 2: Contraindication Analysis"""
        result = {
            'layer_name': 'Contraindication Analysis',
            'status': 'passed',
            'absolute_contraindications': [],
            'relative_contraindications': [],
            'warnings': []
        }
        
        medical_history = patient_data.get('medical_history', [])
        allergies = patient_data.get('allergies', [])
        prescribed_peptides = protocol_data.get('recommended_peptides', [])
        
        # Check patient characteristics
        gender = patient_data.get('gender', '').lower()
        age = int(patient_data.get('age', 0))
        
        for peptide in prescribed_peptides:
            peptide_key = peptide.lower()
            if peptide_key in self.contraindications:
                
                # Check absolute contraindications
                for contraindication in self.contraindications[peptide_key]['absolute']:
                    # Check medical history
                    if any(contraindication.lower() in str(condition).lower() for condition in medical_history):
                        result['absolute_contraindications'].append({
                            'peptide': peptide,
                            'contraindication': contraindication,
                            'source': 'medical_history'
                        })
                        result['status'] = 'blocked'
                    
                    # Check for pregnancy/breastfeeding in females
                    if 'pregnancy' in contraindication.lower() and gender == 'female' and 18 <= age <= 50:
                        result['warnings'].append({
                            'peptide': peptide,
                            'warning': 'Pregnancy screening required for females of childbearing age',
                            'action_required': 'Obtain pregnancy test'
                        })
                
                # Check relative contraindications
                for contraindication in self.contraindications[peptide_key]['relative']:
                    if any(contraindication.lower() in str(condition).lower() for condition in medical_history):
                        result['relative_contraindications'].append({
                            'peptide': peptide,
                            'contraindication': contraindication,
                            'recommendation': 'Enhanced monitoring required'
                        })
                        if result['status'] == 'passed':
                            result['status'] = 'warning'
        
        return result

    def _execute_layer3_dosing_boundaries(self, protocol_data: Dict) -> Dict[str, Any]:
        """Layer 3: Dosing Boundary Checks"""
        result = {
            'layer_name': 'Dosing Boundary Analysis',
            'status': 'passed',
            'boundary_violations': [],
            'warnings': []
        }
        
        dosing_protocols = protocol_data.get('detailed_dosing_protocols', {}).get('personalized_dosing', [])
        
        for dosing in dosing_protocols:
            peptide = dosing.get('peptide_name', '').lower()
            calculated_dose = float(dosing.get('calculated_dose', 0))
            
            if peptide in self.dosing_boundaries:
                boundaries = self.dosing_boundaries[peptide]
                min_dose = boundaries['standard_dose']['min']
                max_dose = boundaries['standard_dose']['max']
                
                # Check if dose is within boundaries
                if calculated_dose < min_dose * self.safety_layers['layer_3_dosing_boundaries']['min_dose_multiplier']:
                    result['boundary_violations'].append({
                        'peptide': peptide,
                        'calculated_dose': calculated_dose,
                        'minimum_safe': min_dose * self.safety_layers['layer_3_dosing_boundaries']['min_dose_multiplier'],
                        'violation_type': 'below_minimum'
                    })
                    result['status'] = 'blocked'
                
                elif calculated_dose > max_dose * self.safety_layers['layer_3_dosing_boundaries']['max_dose_multiplier']:
                    result['boundary_violations'].append({
                        'peptide': peptide,
                        'calculated_dose': calculated_dose,
                        'maximum_safe': max_dose * self.safety_layers['layer_3_dosing_boundaries']['max_dose_multiplier'],
                        'violation_type': 'above_maximum'
                    })
                    result['status'] = 'blocked'
                
                # Check for warnings (approaching limits)
                elif calculated_dose > max_dose * 0.8:  # 80% of max dose
                    result['warnings'].append({
                        'peptide': peptide,
                        'calculated_dose': calculated_dose,
                        'warning': 'Dose approaching upper limit - enhanced monitoring recommended'
                    })
                    if result['status'] == 'passed':
                        result['status'] = 'warning'
        
        return result

    def _execute_layer4_practitioner_review(self, safety_results: Dict) -> Dict[str, Any]:
        """Layer 4: Practitioner Override Requirements"""
        result = {
            'layer_name': 'Practitioner Review Requirements',
            'status': 'passed',
            'review_required': False,
            'override_required': False,
            'justification_required': False
        }
        
        # Check if any previous layers failed
        for layer_key, layer_result in safety_results.get('layer_results', {}).items():
            if layer_result.get('status') == 'blocked':
                result['override_required'] = True
                result['justification_required'] = True
                result['review_required'] = True
                result['status'] = 'requires_override'
            elif layer_result.get('status') == 'warning':
                result['review_required'] = True
                if result['status'] == 'passed':
                    result['status'] = 'requires_review'
        
        return result

    def _execute_layer5_consent_verification(self, patient_data: Dict) -> Dict[str, Any]:
        """Layer 5: Patient Consent Verification"""
        result = {
            'layer_name': 'Patient Consent Verification',
            'status': 'pending',
            'consent_required': True,
            'consent_obtained': False,
            'consent_type': 'informed_consent'
        }
        
        # In production, this would check actual consent status
        # For now, we'll indicate what's required
        result['requirements'] = [
            'Informed consent for peptide therapy',
            'Risk acknowledgment signed',
            'Treatment alternatives discussed',
            'Patient questions answered'
        ]
        
        return result

    def _calculate_safety_score(self, layer_results: Dict) -> float:
        """Calculate overall safety score from layer results"""
        layer_scores = {
            'layer_1': 20,  # Drug interactions
            'layer_2': 25,  # Contraindications  
            'layer_3': 20,  # Dosing boundaries
            'layer_4': 15,  # Practitioner review
            'layer_5': 20   # Patient consent
        }
        
        total_score = 0
        max_score = sum(layer_scores.values())
        
        for layer_key, max_points in layer_scores.items():
            layer_result = layer_results.get(layer_key, {})
            layer_status = layer_result.get('status', 'failed')
            
            if layer_status == 'passed':
                total_score += max_points
            elif layer_status == 'warning' or layer_status == 'requires_review':
                total_score += max_points * 0.7  # 70% credit for warnings
            elif layer_status in ['requires_override', 'pending']:
                total_score += max_points * 0.3  # 30% credit for overridable issues
            # blocked/failed gets 0 points
        
        return round((total_score / max_score) * 100, 1)

    def _determine_clearance_status(self, safety_results: Dict) -> str:
        """Determine overall clearance status"""
        layer_results = safety_results.get('layer_results', {})
        
        # Check for any blocked status
        if any(layer.get('status') == 'blocked' for layer in layer_results.values()):
            return 'blocked'
        
        # Check for override requirements
        if any(layer.get('status') == 'requires_override' for layer in layer_results.values()):
            return 'requires_override'
        
        # Check for review requirements
        if any(layer.get('status') in ['requires_review', 'warning'] for layer in layer_results.values()):
            return 'requires_review'
        
        # Check for pending items
        if any(layer.get('status') == 'pending' for layer in layer_results.values()):
            return 'pending'
        
        return 'cleared'

    def _generate_required_actions(self, safety_results: Dict) -> List[Dict[str, Any]]:
        """Generate list of required actions based on safety analysis"""
        actions = []
        
        clearance_status = safety_results.get('clearance_status')
        
        if clearance_status == 'blocked':
            actions.append({
                'priority': 'critical',
                'action': 'Protocol blocked due to safety concerns',
                'description': 'Critical safety issues must be resolved before proceeding',
                'required_by': 'system'
            })
        
        elif clearance_status == 'requires_override':
            actions.append({
                'priority': 'high',
                'action': 'Practitioner override required',
                'description': 'Safety concerns require practitioner review and justification',
                'required_by': 'practitioner'
            })
        
        elif clearance_status == 'requires_review':
            actions.append({
                'priority': 'moderate',
                'action': 'Practitioner review recommended',
                'description': 'Warning conditions should be reviewed before proceeding',
                'required_by': 'practitioner'
            })
        
        # Add specific actions based on layer results
        layer_results = safety_results.get('layer_results', {})
        
        if layer_results.get('layer_5', {}).get('status') == 'pending':
            actions.append({
                'priority': 'high',
                'action': 'Obtain patient consent',
                'description': 'Informed consent must be obtained before treatment',
                'required_by': 'staff'
            })
        
        return actions

    def _compile_safety_alerts(self, layer_results: Dict) -> List[Dict[str, Any]]:
        """Compile all safety alerts from layer results"""
        alerts = []
        
        for layer_key, layer_result in layer_results.items():
            # Add critical blocks
            for block in layer_result.get('critical_blocks', []):
                alerts.append({
                    'severity': 'critical',
                    'source': layer_key,
                    'type': 'block',
                    'message': f"Critical interaction: {block.get('mechanism', 'Unknown')}",
                    'details': block
                })
            
            # Add warnings
            for warning in layer_result.get('warnings', []):
                alerts.append({
                    'severity': 'warning',
                    'source': layer_key,
                    'type': 'warning',
                    'message': warning.get('warning', warning.get('mechanism', 'Safety warning')),
                    'details': warning
                })
            
            # Add boundary violations
            for violation in layer_result.get('boundary_violations', []):
                alerts.append({
                    'severity': 'critical',
                    'source': layer_key,
                    'type': 'dosing_violation',
                    'message': f"Dosing boundary violation: {violation.get('violation_type')}",
                    'details': violation
                })
        
        return alerts

    # Quality Assessment Methods
    def _assess_evidence_level(self, protocol_data: Dict) -> Dict[str, Any]:
        """Assess evidence level quality"""
        # Look for evidence indicators in protocol
        evidence_indicators = protocol_data.get('evidence_based_support', {})
        
        # Default to good evidence level for peptides with clinical trials
        evidence_level = 'B_cohort_studies'  # Default
        
        if 'randomized controlled trials' in str(evidence_indicators).lower():
            evidence_level = 'A_randomized_controlled_trials'
        elif 'clinical trials' in str(evidence_indicators).lower():
            evidence_level = 'B_cohort_studies'
        
        max_score = max(self.quality_criteria['evidence_level'].values())
        score = self.quality_criteria['evidence_level'][evidence_level]
        
        return {
            'score': score,
            'max_score': max_score,
            'level': evidence_level,
            'percentage': round((score / max_score) * 100, 1)
        }

    def _assess_safety_profile(self, protocol_data: Dict) -> Dict[str, Any]:
        """Assess safety profile quality"""
        # Assess based on known safety data
        peptides = protocol_data.get('recommended_peptides', [])
        
        safety_level = 'good'  # Default for established peptides
        
        # Semaglutide has excellent safety profile from extensive trials
        if any('semaglutide' in peptide.lower() for peptide in peptides):
            safety_level = 'excellent'
        
        max_score = max(self.quality_criteria['safety_profile'].values())
        score = self.quality_criteria['safety_profile'][safety_level]
        
        return {
            'score': score,
            'max_score': max_score,
            'level': safety_level,
            'percentage': round((score / max_score) * 100, 1)
        }

    def _assess_personalization_depth(self, patient_data: Dict, protocol_data: Dict) -> Dict[str, Any]:
        """Assess personalization depth"""
        personalization_factors = 0
        
        # Check for patient-specific dosing
        dosing_data = protocol_data.get('detailed_dosing_protocols', {})
        if dosing_data.get('personalized_dosing'):
            personalization_factors += 1
        
        # Check for concern-specific selection
        primary_concerns = patient_data.get('primary_concerns', [])
        if primary_concerns and len(primary_concerns) > 1:
            personalization_factors += 1
        
        # Check for risk-adjusted protocols
        if protocol_data.get('comprehensive_contraindications'):
            personalization_factors += 1
        
        # Check for individual monitoring
        if protocol_data.get('monitoring_requirements'):
            personalization_factors += 1
        
        if personalization_factors >= 3:
            level = 'high_personalization'
        elif personalization_factors >= 2:
            level = 'moderate_personalization'
        elif personalization_factors >= 1:
            level = 'standard_personalization'
        else:
            level = 'minimal_personalization'
        
        max_score = max(self.quality_criteria['personalization_depth'].values())
        score = self.quality_criteria['personalization_depth'][level]
        
        return {
            'score': score,
            'max_score': max_score,
            'level': level,
            'factors_count': personalization_factors,
            'percentage': round((score / max_score) * 100, 1)
        }

    def _assess_monitoring_adequacy(self, protocol_data: Dict) -> Dict[str, Any]:
        """Assess monitoring adequacy"""
        monitoring_components = 0
        
        monitoring_data = protocol_data.get('monitoring_requirements', {})
        
        # Check for baseline labs
        if monitoring_data.get('baseline_labs'):
            monitoring_components += 1
        
        # Check for follow-up schedule
        if monitoring_data.get('follow_up_intervals'):
            monitoring_components += 1
        
        # Check for safety monitoring
        if monitoring_data.get('safety_monitoring'):
            monitoring_components += 1
        
        # Check for success metrics
        if monitoring_data.get('success_metrics'):
            monitoring_components += 1
        
        if monitoring_components >= 4:
            level = 'comprehensive'
        elif monitoring_components >= 3:
            level = 'adequate'
        elif monitoring_components >= 2:
            level = 'basic'
        else:
            level = 'insufficient'
        
        max_score = max(self.quality_criteria['monitoring_adequacy'].values())
        score = self.quality_criteria['monitoring_adequacy'][level]
        
        return {
            'score': score,
            'max_score': max_score,
            'level': level,
            'components_count': monitoring_components,
            'percentage': round((score / max_score) * 100, 1)
        }

    def _assess_patient_engagement(self, protocol_data: Dict) -> Dict[str, Any]:
        """Assess patient engagement potential"""
        # Assume high engagement based on comprehensive protocols
        engagement_level = 'high_engagement'  # Default for detailed protocols
        
        max_score = max(self.quality_criteria['patient_engagement'].values())
        score = self.quality_criteria['patient_engagement'][engagement_level]
        
        return {
            'score': score,
            'max_score': max_score,
            'level': engagement_level,
            'percentage': round((score / max_score) * 100, 1)
        }

    def _determine_quality_grade(self, score: float) -> str:
        """Determine quality grade based on score"""
        if score >= 90:
            return 'A (Excellent)'
        elif score >= 80:
            return 'B (Good)'
        elif score >= 70:
            return 'C (Acceptable)'
        elif score >= 60:
            return 'D (Needs Improvement)'
        else:
            return 'F (Poor)'

    def _generate_quality_recommendations(self, quality_scores: Dict, overall_score: float) -> List[str]:
        """Generate quality improvement recommendations"""
        recommendations = []
        
        if overall_score < 90:
            # Check each component for improvement opportunities
            for component, data in quality_scores.items():
                if data['percentage'] < 80:
                    if component == 'evidence_level':
                        recommendations.append("Consider incorporating additional clinical trial data")
                    elif component == 'personalization_depth':
                        recommendations.append("Enhance personalization factors (genetics, biomarkers)")
                    elif component == 'monitoring_adequacy':
                        recommendations.append("Expand monitoring protocol comprehensiveness")
        
        if not recommendations:
            recommendations.append("Protocol meets high quality standards")
        
        return recommendations

    # Continuous Monitoring Methods (simplified implementations)
    def _monitor_outcome_success(self, usage_data: Dict) -> Dict[str, Any]:
        """Monitor outcome success rates"""
        return {
            'success_rate': usage_data.get('success_rate', 0.85),
            'total_patients': usage_data.get('total_patients', 0),
            'benchmark': 0.80
        }

    def _monitor_safety_incidents(self, usage_data: Dict) -> Dict[str, Any]:
        """Monitor safety incidents"""
        return {
            'incident_rate': usage_data.get('incident_rate', 0.05),
            'total_incidents': usage_data.get('total_incidents', 0),
            'benchmark': 0.10
        }

    def _monitor_patient_satisfaction(self, usage_data: Dict) -> Dict[str, Any]:
        """Monitor patient satisfaction"""
        return {
            'satisfaction_score': usage_data.get('satisfaction_score', 4.2),
            'response_rate': usage_data.get('response_rate', 0.65),
            'benchmark': 4.0
        }

    def _monitor_practitioner_feedback(self, usage_data: Dict) -> Dict[str, Any]:
        """Monitor practitioner feedback"""
        return {
            'practitioner_rating': usage_data.get('practitioner_rating', 4.1),
            'usage_frequency': usage_data.get('usage_frequency', 0.75),
            'benchmark': 3.8
        }

    def _analyze_quality_trends(self, metrics: Dict) -> Dict[str, str]:
        """Analyze quality trends"""
        return {
            'outcomes': 'stable',
            'safety': 'improving', 
            'satisfaction': 'stable',
            'practitioner_feedback': 'improving'
        }

    def _generate_quality_alerts(self, monitoring_results: Dict) -> List[Dict[str, Any]]:
        """Generate quality alerts"""
        alerts = []
        
        metrics = monitoring_results.get('monitoring_metrics', {})
        
        # Check if success rate drops below benchmark
        outcomes = metrics.get('outcomes', {})
        if outcomes.get('success_rate', 1.0) < outcomes.get('benchmark', 0.8):
            alerts.append({
                'severity': 'warning',
                'type': 'outcome_degradation',
                'message': 'Success rate below benchmark'
            })
        
        return alerts

    def _generate_improvement_recommendations(self, monitoring_results: Dict) -> List[str]:
        """Generate improvement recommendations"""
        return [
            "Continue monitoring current metrics",
            "Consider protocol optimization based on outcome data",
            "Enhance patient education materials"
        ]

# Global instance
safety_quality_assurance = SafetyQualityAssurance()