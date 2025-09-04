"""
Clinical Decision Support System - Real-Time Intelligence
Provides interactive monitoring dashboard and evidence-based decision trees
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import logging

logger = logging.getLogger(__name__)

class ClinicalDecisionSupport:
    def __init__(self):
        # Critical alert thresholds
        self.critical_thresholds = {
            'weight_loss_rate': 3.0,  # lbs per week
            'blood_pressure_systolic': 180,
            'blood_pressure_diastolic': 110,
            'heart_rate': 120,
            'glucose_fasting': 250,
            'temperature': 101.5
        }
        
        # Warning thresholds
        self.warning_thresholds = {
            'weight_loss_rate': 2.0,
            'blood_pressure_systolic': 160,
            'blood_pressure_diastolic': 100,
            'nausea_severity': 7,
            'injection_site_reaction': 5,
            'fatigue_level': 8
        }
        
        # Evidence-based decision trees
        self.decision_trees = {
            'severe_nausea': {
                'condition': 'nausea_severity > 7 for > 3 days',
                'interventions': [
                    {'action': 'reduce_semaglutide_dose', 'reduction': 0.5, 'evidence': 'STEP-1 trial protocol'},
                    {'action': 'prescribe_ondansetron', 'dose': '4mg PRN', 'evidence': 'Clinical guideline'},
                    {'action': 'dietary_modification', 'type': 'small_frequent_meals', 'evidence': 'Expert consensus'},
                    {'action': 'schedule_followup', 'timeframe': '48 hours', 'evidence': 'Safety protocol'}
                ],
                'escalation': 'Consider IV hydration if severe dehydration'
            },
            'rapid_weight_loss': {
                'condition': 'weight_loss > 2 lbs/week for 2 consecutive weeks',
                'interventions': [
                    {'action': 'reduce_dose', 'reduction': 0.25, 'evidence': 'Obesity medicine guidelines'},
                    {'action': 'nutritional_counseling', 'focus': 'adequate_protein', 'evidence': 'Clinical practice'},
                    {'action': 'monitor_muscle_mass', 'method': 'DEXA scan', 'evidence': 'Body composition research'}
                ],
                'escalation': 'Consider dose hold if >3 lbs/week'
            },
            'injection_site_reaction': {
                'condition': 'reaction_severity > 5 or duration > 48 hours',
                'interventions': [
                    {'action': 'rotate_injection_sites', 'frequency': 'each_injection', 'evidence': 'Manufacturer guidelines'},
                    {'action': 'ice_application', 'duration': '10 minutes pre/post', 'evidence': 'Clinical practice'},
                    {'action': 'topical_antihistamine', 'type': 'diphenhydramine cream', 'evidence': 'Dermatology guidelines'}
                ],
                'escalation': 'Consider allergy evaluation if systemic symptoms'
            },
            'thyroid_concerns': {
                'condition': 'TSH > 4.5 or symptoms of hypothyroidism',
                'interventions': [
                    {'action': 'thyroid_panel', 'tests': 'TSH, Free T4, Free T3', 'evidence': 'Endocrine guidelines'},
                    {'action': 'levothyroxine_adjustment', 'increase': '12.5-25mcg', 'evidence': 'ATA guidelines'},
                    {'action': 'recheck_timing', 'timeframe': '6 weeks', 'evidence': 'Pharmacokinetic data'}
                ],
                'escalation': 'Endocrinology referral if TSH >10'
            }
        }
        
        # Monitoring protocols by risk level
        self.monitoring_protocols = {
            'low_risk': {
                'frequency': 'monthly',
                'parameters': ['weight', 'vital_signs', 'symptom_assessment'],
                'labs': 'quarterly'
            },
            'moderate_risk': {
                'frequency': 'bi-weekly', 
                'parameters': ['weight', 'vital_signs', 'symptom_assessment', 'injection_sites'],
                'labs': 'monthly'
            },
            'high_risk': {
                'frequency': 'weekly',
                'parameters': ['weight', 'vital_signs', 'symptom_assessment', 'injection_sites', 'glucose'],
                'labs': 'bi-weekly'
            }
        }

    def generate_smart_alerts(self, patient_data: Dict, current_metrics: Dict) -> Dict[str, Any]:
        """Generate intelligent alerts based on current patient metrics"""
        try:
            alerts = {
                'critical': [],
                'warning': [],
                'informational': [],
                'recommendations': []
            }
            
            # Check critical thresholds
            for metric, threshold in self.critical_thresholds.items():
                if metric in current_metrics:
                    value = float(current_metrics[metric])
                    if self._exceeds_threshold(metric, value, threshold, 'critical'):
                        alert = self._create_critical_alert(metric, value, threshold)
                        alerts['critical'].append(alert)
            
            # Check warning thresholds  
            for metric, threshold in self.warning_thresholds.items():
                if metric in current_metrics:
                    value = float(current_metrics[metric])
                    if self._exceeds_threshold(metric, value, threshold, 'warning'):
                        alert = self._create_warning_alert(metric, value, threshold)
                        alerts['warning'].append(alert)
            
            # Generate trend-based alerts
            trend_alerts = self._analyze_trends(patient_data, current_metrics)
            alerts['informational'].extend(trend_alerts)
            
            # Generate recommendations
            recommendations = self._generate_smart_recommendations(patient_data, current_metrics, alerts)
            alerts['recommendations'] = recommendations
            
            # Add alert metadata
            alerts['generated_at'] = datetime.utcnow().isoformat()
            alerts['patient_id'] = patient_data.get('patient_name', 'unknown')
            alerts['alert_count'] = {
                'critical': len(alerts['critical']),
                'warning': len(alerts['warning']),
                'informational': len(alerts['informational'])
            }
            
            return {
                'success': True,
                'alerts': alerts
            }
            
        except Exception as e:
            logger.error(f"Error generating smart alerts: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'alerts': {}
            }

    def execute_decision_tree(self, condition: str, patient_data: Dict, current_metrics: Dict) -> Dict[str, Any]:
        """Execute evidence-based decision tree for specific condition"""
        try:
            if condition not in self.decision_trees:
                return {
                    'success': False,
                    'error': f"Decision tree not found for condition: {condition}"
                }
            
            tree = self.decision_trees[condition]
            
            # Evaluate condition
            condition_met = self._evaluate_condition(tree['condition'], current_metrics)
            
            if not condition_met:
                return {
                    'success': True,
                    'condition_met': False,
                    'message': f"Condition '{condition}' not currently met"
                }
            
            # Execute interventions
            interventions = tree['interventions']
            action_plan = []
            
            for intervention in interventions:
                action_item = {
                    'action': intervention['action'],
                    'details': self._format_intervention_details(intervention),
                    'evidence_level': intervention.get('evidence', 'Clinical practice'),
                    'priority': self._determine_intervention_priority(intervention),
                    'timeline': self._determine_intervention_timeline(intervention)
                }
                action_plan.append(action_item)
            
            # Check for escalation criteria
            escalation_needed = self._check_escalation_criteria(condition, current_metrics)
            escalation_plan = tree.get('escalation') if escalation_needed else None
            
            return {
                'success': True,
                'condition_met': True,
                'condition': condition,
                'action_plan': action_plan,
                'escalation_needed': escalation_needed,
                'escalation_plan': escalation_plan,
                'evidence_based': True,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error executing decision tree: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def generate_monitoring_dashboard(self, patient_data: Dict, risk_level: str) -> Dict[str, Any]:
        """Generate personalized monitoring dashboard"""
        try:
            # Get monitoring protocol for risk level
            protocol = self.monitoring_protocols.get(risk_level.lower(), self.monitoring_protocols['moderate_risk'])
            
            # Generate dashboard components
            dashboard = {
                'patient_overview': {
                    'name': patient_data.get('patient_name', 'Unknown'),
                    'age': patient_data.get('age', 'Unknown'),
                    'risk_level': risk_level,
                    'monitoring_frequency': protocol['frequency'],
                    'next_visit': self._calculate_next_visit(protocol['frequency'])
                },
                'vital_monitoring': {
                    'parameters': protocol['parameters'],
                    'frequency': protocol['frequency'],
                    'alert_thresholds': self._get_patient_specific_thresholds(patient_data)
                },
                'lab_monitoring': {
                    'frequency': protocol['labs'],
                    'required_tests': self._get_required_labs(patient_data),
                    'next_lab_date': self._calculate_next_lab_date(protocol['labs'])
                },
                'safety_checklist': self._generate_safety_checklist(patient_data),
                'progress_tracking': {
                    'key_metrics': self._identify_key_metrics(patient_data),
                    'target_ranges': self._define_target_ranges(patient_data),
                    'improvement_timeline': self._generate_improvement_timeline(patient_data)
                }
            }
            
            return {
                'success': True,
                'dashboard': dashboard,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating monitoring dashboard: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'dashboard': {}
            }

    def _exceeds_threshold(self, metric: str, value: float, threshold: float, alert_type: str) -> bool:
        """Check if metric exceeds threshold based on metric type"""
        # Weight loss rate should not exceed threshold
        if 'weight_loss' in metric:
            return value > threshold
        # Blood pressure and other vitals
        elif metric in ['blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 'temperature']:
            return value > threshold
        # Severity scales (higher is worse)
        elif 'severity' in metric or 'level' in metric:
            return value > threshold
        else:
            return value > threshold

    def _create_critical_alert(self, metric: str, value: float, threshold: float) -> Dict[str, Any]:
        """Create critical alert with specific actions"""
        alert_messages = {
            'weight_loss_rate': f"CRITICAL: Rapid weight loss detected ({value} lbs/week). Immediate intervention required.",
            'blood_pressure_systolic': f"CRITICAL: Severe hypertension ({value} mmHg). Emergency evaluation needed.",
            'glucose_fasting': f"CRITICAL: Severe hyperglycemia ({value} mg/dL). Immediate medical attention required."
        }
        
        return {
            'type': 'critical',
            'metric': metric,
            'value': value,
            'threshold': threshold,
            'message': alert_messages.get(metric, f"CRITICAL: {metric} value {value} exceeds safe threshold {threshold}"),
            'immediate_actions': self._get_immediate_actions(metric),
            'timestamp': datetime.utcnow().isoformat(),
            'requires_physician_contact': True
        }

    def _create_warning_alert(self, metric: str, value: float, threshold: float) -> Dict[str, Any]:
        """Create warning alert with monitoring recommendations"""
        alert_messages = {
            'nausea_severity': f"WARNING: Severe nausea reported (level {value}/10). Intervention recommended.",
            'injection_site_reaction': f"WARNING: Significant injection site reaction (level {value}/10). Monitor closely.",
            'weight_loss_rate': f"WARNING: Above target weight loss rate ({value} lbs/week). Consider dose adjustment."
        }
        
        return {
            'type': 'warning',
            'metric': metric,
            'value': value,
            'threshold': threshold,
            'message': alert_messages.get(metric, f"WARNING: {metric} value {value} exceeds target threshold {threshold}"),
            'recommended_actions': self._get_recommended_actions(metric),
            'timestamp': datetime.utcnow().isoformat(),
            'requires_monitoring': True
        }

    def _analyze_trends(self, patient_data: Dict, current_metrics: Dict) -> List[Dict[str, Any]]:
        """Analyze metric trends and generate informational alerts"""
        trends = []
        
        # Positive trends
        if 'energy_levels' in current_metrics and float(current_metrics['energy_levels']) > 7:
            trends.append({
                'type': 'positive_trend',
                'message': f"Excellent energy improvement (level {current_metrics['energy_levels']}/10)",
                'recommendation': 'Current protocol appears optimal - continue monitoring'
            })
        
        if 'weight' in current_metrics:
            trends.append({
                'type': 'progress_update',
                'message': f"Current weight: {current_metrics['weight']} lbs",
                'recommendation': 'Track weekly for optimal monitoring'
            })
        
        return trends

    def _generate_smart_recommendations(self, patient_data: Dict, current_metrics: Dict, alerts: Dict) -> List[Dict[str, Any]]:
        """Generate intelligent recommendations based on patient status"""
        recommendations = []
        
        # Based on critical alerts
        if alerts['critical']:
            recommendations.append({
                'priority': 'critical',
                'category': 'safety',
                'recommendation': 'Immediate physician contact required due to critical alerts',
                'timeframe': 'immediate'
            })
        
        # Based on warning alerts
        if alerts['warning']:
            recommendations.append({
                'priority': 'high',
                'category': 'monitoring',
                'recommendation': 'Enhanced monitoring protocol recommended',
                'timeframe': '24-48 hours'
            })
        
        # Optimization recommendations
        if 'energy_levels' in current_metrics:
            energy = float(current_metrics['energy_levels'])
            if energy < 5:
                recommendations.append({
                    'priority': 'moderate',
                    'category': 'optimization',
                    'recommendation': 'Consider dose adjustment or additional support therapies',
                    'timeframe': 'next visit'
                })
        
        return recommendations

    def _evaluate_condition(self, condition: str, metrics: Dict) -> bool:
        """Evaluate if decision tree condition is met"""
        # Simplified condition evaluation - in production would be more sophisticated
        if 'nausea_severity > 7' in condition:
            return metrics.get('nausea_severity', 0) > 7
        elif 'weight_loss > 2 lbs/week' in condition:
            return metrics.get('weight_loss_rate', 0) > 2
        elif 'reaction_severity > 5' in condition:
            return metrics.get('injection_site_reaction', 0) > 5
        elif 'TSH > 4.5' in condition:
            return metrics.get('tsh', 0) > 4.5
        
        return False

    def _format_intervention_details(self, intervention: Dict) -> str:
        """Format intervention details for display"""
        details = []
        for key, value in intervention.items():
            if key not in ['action', 'evidence']:
                details.append(f"{key}: {value}")
        return '; '.join(details)

    def _determine_intervention_priority(self, intervention: Dict) -> str:
        """Determine intervention priority"""
        if 'reduce' in intervention.get('action', '').lower():
            return 'high'
        elif 'monitor' in intervention.get('action', '').lower():
            return 'moderate'
        else:
            return 'standard'

    def _determine_intervention_timeline(self, intervention: Dict) -> str:
        """Determine intervention timeline"""
        if 'immediate' in str(intervention).lower():
            return 'immediate'
        elif 'hour' in str(intervention).lower():
            return '24-48 hours'
        else:
            return 'next visit'

    def _check_escalation_criteria(self, condition: str, metrics: Dict) -> bool:
        """Check if escalation criteria are met"""
        # Simplified escalation logic
        if condition == 'severe_nausea':
            return metrics.get('nausea_severity', 0) > 8
        elif condition == 'rapid_weight_loss':
            return metrics.get('weight_loss_rate', 0) > 3
        
        return False

    def _calculate_next_visit(self, frequency: str) -> str:
        """Calculate next visit date based on frequency"""
        if frequency == 'weekly':
            next_date = datetime.now() + timedelta(weeks=1)
        elif frequency == 'bi-weekly':
            next_date = datetime.now() + timedelta(weeks=2)
        else:  # monthly
            next_date = datetime.now() + timedelta(weeks=4)
        
        return next_date.strftime("%Y-%m-%d")

    def _get_patient_specific_thresholds(self, patient_data: Dict) -> Dict[str, float]:
        """Get patient-specific alert thresholds"""
        # Customize thresholds based on patient factors
        age = int(patient_data.get('age', 40))
        
        thresholds = self.warning_thresholds.copy()
        
        # Adjust for age
        if age > 65:
            thresholds['blood_pressure_systolic'] = 150  # Less aggressive for elderly
            
        return thresholds

    def _get_required_labs(self, patient_data: Dict) -> List[str]:
        """Get required lab tests based on patient profile"""
        base_labs = ['CBC', 'CMP', 'HbA1c', 'Lipids']
        
        # Add specific labs based on conditions
        if 'thyroid' in str(patient_data.get('medical_history', [])).lower():
            base_labs.extend(['TSH', 'Free T4'])
            
        if any('diabetes' in str(concern).lower() for concern in patient_data.get('primary_concerns', [])):
            base_labs.append('Fructosamine')
            
        return base_labs

    def _calculate_next_lab_date(self, frequency: str) -> str:
        """Calculate next lab date"""
        if frequency == 'monthly':
            next_date = datetime.now() + timedelta(weeks=4)
        elif frequency == 'bi-weekly':
            next_date = datetime.now() + timedelta(weeks=2)
        else:  # quarterly
            next_date = datetime.now() + timedelta(weeks=12)
            
        return next_date.strftime("%Y-%m-%d")

    def _generate_safety_checklist(self, patient_data: Dict) -> List[Dict[str, Any]]:
        """Generate patient-specific safety checklist"""
        checklist = [
            {
                'item': 'Injection site rotation',
                'frequency': 'Each injection',
                'importance': 'high'
            },
            {
                'item': 'Nausea/vomiting assessment',
                'frequency': 'Daily for first 2 weeks',
                'importance': 'high'
            },
            {
                'item': 'Weight monitoring', 
                'frequency': 'Weekly',
                'importance': 'moderate'
            }
        ]
        
        # Add condition-specific items
        if 'thyroid' in str(patient_data.get('medical_history', [])).lower():
            checklist.append({
                'item': 'Thyroid symptom monitoring',
                'frequency': 'Weekly',
                'importance': 'high'
            })
            
        return checklist

    def _identify_key_metrics(self, patient_data: Dict) -> List[str]:
        """Identify key metrics to track based on primary concerns"""
        concerns = patient_data.get('primary_concerns', [])
        metrics = ['weight', 'energy_levels']
        
        for concern in concerns:
            concern_str = str(concern).lower()
            if 'fatigue' in concern_str:
                metrics.append('energy_levels')
            if 'sleep' in concern_str:
                metrics.append('sleep_quality')
            if 'brain fog' in concern_str:
                metrics.append('cognitive_function')
                
        return list(set(metrics))  # Remove duplicates

    def _define_target_ranges(self, patient_data: Dict) -> Dict[str, str]:
        """Define target ranges for key metrics"""
        return {
            'weight': 'Gradual loss 1-2 lbs/week',
            'energy_levels': 'Target: 7-8/10',
            'sleep_quality': 'Target: 7-8/10', 
            'cognitive_function': 'Target: 7-8/10',
            'nausea_severity': 'Target: <3/10'
        }

    def _generate_improvement_timeline(self, patient_data: Dict) -> Dict[str, str]:
        """Generate expected improvement timeline"""
        return {
            'Week 1-2': 'Appetite changes, initial side effects',
            'Week 3-4': 'Early weight loss, energy stabilization',
            'Week 6-8': 'Significant improvements visible',
            'Week 12+': 'Optimal therapeutic effects'
        }

    def _get_immediate_actions(self, metric: str) -> List[str]:
        """Get immediate actions for critical alerts"""
        actions = {
            'weight_loss_rate': [
                'Hold current peptide dose',
                'Contact physician immediately', 
                'Increase caloric intake',
                'Monitor for dehydration'
            ],
            'blood_pressure_systolic': [
                'Recheck BP in 5 minutes',
                'Contact physician/ED immediately',
                'Have patient rest in sitting position',
                'Prepare for emergency transport if needed'
            ]
        }
        return actions.get(metric, ['Contact physician immediately'])

    def _get_recommended_actions(self, metric: str) -> List[str]:
        """Get recommended actions for warning alerts"""
        actions = {
            'nausea_severity': [
                'Consider dose reduction',
                'Implement dietary modifications',
                'Consider anti-nausea medication',
                'Schedule follow-up within 48 hours'
            ],
            'injection_site_reaction': [
                'Rotate injection sites',
                'Apply ice before/after injection',
                'Consider topical antihistamine',
                'Monitor for worsening'
            ]
        }
        return actions.get(metric, ['Monitor closely', 'Contact if worsening'])

# Global instance
clinical_decision_support = ClinicalDecisionSupport()