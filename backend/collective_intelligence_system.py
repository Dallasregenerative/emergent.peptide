"""
Collective Intelligence & Continuous Learning System
Real-world feedback integration for protocol evolution and safety
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

class CollectiveIntelligenceSystem:
    """
    Manages the collective learning and feedback system that continuously
    evolves the platform's medical intelligence through real-world outcomes
    """
    
    def __init__(self):
        self.feedback_database = {}
        self.protocol_outcomes = {}
        self.practitioner_insights = {}
        self.learning_patterns = {}
        
    # POST-PROTOCOL FEEDBACK COLLECTION
    
    def collect_protocol_feedback(self, protocol_id: str, feedback_data: Dict) -> str:
        """
        Collect comprehensive feedback on protocol effectiveness
        
        feedback_data structure:
        {
            "patient_id": "anonymous_hash",
            "practitioner_id": "dr_id_optional", 
            "protocol_effectiveness": 1-5,
            "specific_outcomes": {
                "energy_improvement": 1-5,
                "sleep_quality": 1-5,
                "weight_loss": "actual_lbs",
                "side_effects": ["list", "of", "effects"],
                "biomarker_changes": {"hba1c": "before_after"}
            },
            "timeline_feedback": {
                "week_2": {"energy": 3, "sleep": 2},
                "month_1": {"energy": 4, "sleep": 3},
                "month_3": {"energy": 5, "sleep": 4}
            },
            "protocol_modifications": [
                {
                    "change": "Reduced BPC-157 dose by 50%",
                    "reason": "Mild injection site reaction",
                    "outcome": "Better tolerance, maintained efficacy"
                }
            ],
            "practitioner_notes": "Free text clinical observations",
            "would_recommend": True/False,
            "suggested_improvements": "Free text suggestions"
        }
        """
        feedback_id = str(uuid.uuid4())
        
        # Store feedback with timestamp
        self.feedback_database[feedback_id] = {
            "protocol_id": protocol_id,
            "feedback_data": feedback_data,
            "timestamp": datetime.now(),
            "processed": False,
            "learning_extracted": False
        }
        
        # Trigger immediate learning if critical feedback
        if feedback_data.get("side_effects") or feedback_data.get("protocol_effectiveness", 0) < 2:
            self._trigger_immediate_learning(protocol_id, feedback_data)
            
        return feedback_id
    
    def _trigger_immediate_learning(self, protocol_id: str, feedback_data: Dict):
        """
        Immediate learning trigger for safety concerns or poor outcomes
        """
        # Flag for immediate review by AI and practitioner network
        alert = {
            "type": "safety_concern" if feedback_data.get("side_effects") else "poor_outcome",
            "protocol_id": protocol_id,
            "feedback": feedback_data,
            "requires_review": True,
            "timestamp": datetime.now()
        }
        
        # This would trigger notifications to practitioner network
        # and update AI training data immediately
        return alert
    
    # DR. PEPTIDE FOLLOW-UP SYSTEM
    
    def generate_follow_up_questions(self, protocol_id: str, days_since_start: int) -> List[str]:
        """
        Generate contextual follow-up questions based on protocol and timeline
        """
        base_questions = []
        
        if days_since_start <= 14:
            base_questions = [
                "How are you tolerating the initial protocol? Any side effects?",
                "Have you noticed any changes in energy levels or sleep quality?",
                "Are you having any difficulties with the administration methods?",
                "Any concerns or questions about the current protocol?"
            ]
        elif days_since_start <= 30:
            base_questions = [
                "What improvements have you noticed in the first month?",
                "How effective has the protocol been for your main concerns?",
                "Have any side effects resolved or new ones appeared?",
                "Would you like any adjustments to dosing or timing?",
                "How are your biomarkers responding if you've had lab work?"
            ]
        elif days_since_start <= 90:
            base_questions = [
                "How would you rate the overall effectiveness at 3 months?",
                "Which aspects of the protocol have been most/least effective?",
                "Any suggestions for improvements based on your experience?",
                "Are you ready to transition to maintenance protocols?",
                "What feedback would help other patients with similar conditions?"
            ]
        
        return base_questions
    
    def dr_peptide_follow_up_prompt(self, protocol_id: str, patient_context: Dict) -> str:
        """
        Generate Dr. Peptide follow-up consultation prompt
        """
        days_since_start = patient_context.get("days_since_protocol_start", 0)
        
        follow_up_prompt = f"""
        Dr. Peptide Follow-Up Consultation:
        
        Patient Context: {patient_context.get('original_concerns', 'Previous protocol recipient')}
        Protocol Started: {days_since_start} days ago
        
        Please provide a warm, professional follow-up that includes:
        
        1. **Progress Check**: Ask about improvements in their main concerns
        2. **Safety Review**: Inquire about any side effects or tolerance issues
        3. **Protocol Optimization**: Offer adjustments based on their response
        4. **Feedback Collection**: Ask for specific feedback that helps the collective intelligence
        5. **Next Steps**: Provide guidance on continuation or modifications
        
        Key Questions to Cover:
        {chr(10).join(f"- {q}" for q in self.generate_follow_up_questions(protocol_id, days_since_start))}
        
        Approach: Be encouraging, scientifically rigorous, and genuinely interested in their journey. 
        This feedback helps improve protocols for the entire community.
        """
        
        return follow_up_prompt
    
    # COLLECTIVE LEARNING ENGINE
    
    def analyze_protocol_patterns(self, condition_type: str, min_feedback_count: int = 5) -> Dict:
        """
        Analyze patterns in protocol effectiveness for continuous learning
        """
        relevant_feedback = []
        
        for feedback_id, feedback_entry in self.feedback_database.items():
            feedback_data = feedback_entry["feedback_data"]
            if (feedback_data.get("condition_type") == condition_type and 
                len(feedback_data.get("specific_outcomes", {})) > 0):
                relevant_feedback.append(feedback_data)
        
        if len(relevant_feedback) < min_feedback_count:
            return {"status": "insufficient_data", "count": len(relevant_feedback)}
        
        # Analyze patterns
        patterns = {
            "most_effective_protocols": self._identify_top_protocols(relevant_feedback),
            "common_side_effects": self._analyze_side_effects(relevant_feedback),
            "optimal_dosing_patterns": self._analyze_dosing_patterns(relevant_feedback),
            "timeline_insights": self._analyze_timeline_patterns(relevant_feedback),
            "biomarker_improvements": self._analyze_biomarker_changes(relevant_feedback)
        }
        
        return patterns
    
    def _identify_top_protocols(self, feedback_list: List[Dict]) -> Dict:
        """Identify most successful protocol combinations"""
        protocol_scores = {}
        
        for feedback in feedback_list:
            protocol_key = feedback.get("protocol_summary", "unknown")
            effectiveness = feedback.get("protocol_effectiveness", 0)
            
            if protocol_key not in protocol_scores:
                protocol_scores[protocol_key] = []
            protocol_scores[protocol_key].append(effectiveness)
        
        # Calculate average effectiveness
        top_protocols = {}
        for protocol, scores in protocol_scores.items():
            if len(scores) >= 3:  # Minimum sample size
                avg_score = sum(scores) / len(scores)
                top_protocols[protocol] = {
                    "average_effectiveness": avg_score,
                    "sample_size": len(scores),
                    "confidence": "high" if len(scores) >= 10 else "moderate"
                }
        
        return dict(sorted(top_protocols.items(), 
                          key=lambda x: x[1]["average_effectiveness"], 
                          reverse=True))
    
    def _analyze_side_effects(self, feedback_list: List[Dict]) -> Dict:
        """Analyze side effect patterns for safety optimization"""
        side_effect_patterns = {}
        
        for feedback in feedback_list:
            effects = feedback.get("specific_outcomes", {}).get("side_effects", [])
            protocol_components = feedback.get("protocol_components", [])
            
            for effect in effects:
                if effect not in side_effect_patterns:
                    side_effect_patterns[effect] = {
                        "frequency": 0,
                        "associated_compounds": {},
                        "severity_reports": []
                    }
                
                side_effect_patterns[effect]["frequency"] += 1
                
                # Track which compounds might be associated
                for compound in protocol_components:
                    if compound not in side_effect_patterns[effect]["associated_compounds"]:
                        side_effect_patterns[effect]["associated_compounds"][compound] = 0
                    side_effect_patterns[effect]["associated_compounds"][compound] += 1
        
        return side_effect_patterns
    
    # PRACTITIONER NETWORK INTEGRATION
    
    def collect_practitioner_insight(self, practitioner_id: str, insight_data: Dict) -> str:
        """
        Collect insights from expert practitioners for collective intelligence
        """
        insight_id = str(uuid.uuid4())
        
        self.practitioner_insights[insight_id] = {
            "practitioner_id": practitioner_id,
            "insight_data": insight_data,
            "timestamp": datetime.now(),
            "validated": False,
            "impact_score": 0
        }
        
        return insight_id
    
    def validate_practitioner_insight(self, insight_id: str, validation_data: Dict):
        """
        Validate practitioner insights through outcome data
        """
        if insight_id in self.practitioner_insights:
            insight = self.practitioner_insights[insight_id]
            
            # Calculate impact score based on validation
            impact_score = self._calculate_insight_impact(validation_data)
            
            insight.update({
                "validated": True,
                "validation_data": validation_data,
                "impact_score": impact_score
            })
    
    # ERROR CORRECTION & LEARNING
    
    def report_ai_hallucination(self, report_data: Dict) -> str:
        """
        Report and learn from AI hallucinations or errors
        """
        error_id = str(uuid.uuid4())
        
        error_report = {
            "error_id": error_id,
            "type": "hallucination",
            "reported_content": report_data.get("incorrect_content"),
            "correct_information": report_data.get("corrected_content"),
            "reporter_credentials": report_data.get("reporter_type"),  # practitioner, patient, etc.
            "severity": report_data.get("severity", "medium"),
            "timestamp": datetime.now(),
            "learning_applied": False
        }
        
        # Immediate flagging for high severity errors
        if error_report["severity"] == "high":
            self._trigger_immediate_correction(error_report)
        
        return error_id
    
    def _trigger_immediate_correction(self, error_report: Dict):
        """
        Immediately flag high-severity errors for correction
        """
        # This would trigger:
        # 1. Immediate review by medical team
        # 2. Temporary flagging of related protocols
        # 3. Update to AI training data
        # 4. Notification to affected users if needed
        pass
    
    # CONTINUOUS EVOLUTION ENGINE
    
    def generate_ai_evolution_insights(self) -> Dict:
        """
        Generate insights for continuous AI model improvement
        """
        evolution_data = {
            "successful_patterns": self._extract_successful_patterns(),
            "failure_patterns": self._extract_failure_patterns(),
            "practitioner_corrections": self._extract_practitioner_corrections(),
            "emerging_treatments": self._identify_emerging_treatments(),
            "safety_insights": self._extract_safety_insights()
        }
        
        return evolution_data
    
    def _extract_successful_patterns(self) -> Dict:
        """Extract patterns from highly successful protocols"""
        successful_protocols = []
        
        for feedback_id, feedback_entry in self.feedback_database.items():
            feedback_data = feedback_entry["feedback_data"]
            if feedback_data.get("protocol_effectiveness", 0) >= 4:
                successful_protocols.append(feedback_data)
        
        # Analyze common elements in successful protocols
        return self._analyze_common_elements(successful_protocols)
    
    def _extract_failure_patterns(self) -> Dict:
        """Extract patterns from unsuccessful protocols for learning"""
        failed_protocols = []
        
        for feedback_id, feedback_entry in self.feedback_database.items():
            feedback_data = feedback_entry["feedback_data"]
            if feedback_data.get("protocol_effectiveness", 0) <= 2:
                failed_protocols.append(feedback_data)
        
        return self._analyze_failure_elements(failed_protocols)
    
    # REAL-TIME PROTOCOL OPTIMIZATION
    
    def optimize_protocol_real_time(self, base_protocol: Dict, patient_profile: Dict) -> Dict:
        """
        Optimize protocol in real-time based on collective learning
        """
        optimizations = []
        
        # Check against successful patterns
        successful_patterns = self._extract_successful_patterns()
        
        # Check against failure patterns to avoid
        failure_patterns = self._extract_failure_patterns()
        
        # Apply practitioner insights
        relevant_insights = self._get_relevant_practitioner_insights(patient_profile)
        
        # Generate optimized protocol
        optimized_protocol = self._apply_optimizations(
            base_protocol, 
            successful_patterns, 
            failure_patterns, 
            relevant_insights
        )
        
        return optimized_protocol
    
    # FEEDBACK INTERFACE METHODS
    
    def create_feedback_session(self, protocol_id: str, session_type: str = "follow_up") -> Dict:
        """
        Create structured feedback session
        """
        session_id = str(uuid.uuid4())
        
        session = {
            "session_id": session_id,
            "protocol_id": protocol_id,
            "session_type": session_type,
            "questions": self._generate_session_questions(session_type),
            "created": datetime.now(),
            "completed": False
        }
        
        return session
    
    def _generate_session_questions(self, session_type: str) -> List[Dict]:
        """Generate appropriate questions based on session type"""
        
        if session_type == "immediate_follow_up":
            return [
                {
                    "id": "tolerance",
                    "question": "How are you tolerating the protocol so far?",
                    "type": "scale_1_5",
                    "required": True
                },
                {
                    "id": "side_effects",
                    "question": "Have you experienced any side effects?",
                    "type": "multiple_choice_with_other",
                    "options": ["None", "Mild fatigue", "Injection site reaction", "Nausea", "Other"]
                }
            ]
        
        elif session_type == "outcome_assessment":
            return [
                {
                    "id": "overall_effectiveness",
                    "question": "How effective has the protocol been overall?",
                    "type": "scale_1_5",
                    "required": True
                },
                {
                    "id": "specific_improvements",
                    "question": "Which areas have improved the most?",
                    "type": "multiple_select",
                    "options": ["Energy", "Sleep", "Weight", "Mood", "Cognitive function", "Physical recovery"]
                },
                {
                    "id": "biomarker_changes",
                    "question": "Have you had lab work showing improvements?",
                    "type": "yes_no_details"
                }
            ]
        
        return []

    def _analyze_common_elements(self, protocols: List[Dict]) -> Dict:
        """Analyze common elements in successful protocols"""
        if not protocols:
            return {"status": "no_data"}
        
        common_elements = {
            "peptide_combinations": {},
            "dosing_patterns": {},
            "duration_patterns": {},
            "patient_demographics": {}
        }
        
        # Simple analysis of common patterns
        for protocol in protocols:
            # Track peptide combinations
            peptides = protocol.get("peptides_used", [])
            if peptides:
                peptide_key = ",".join(sorted(peptides))
                common_elements["peptide_combinations"][peptide_key] = common_elements["peptide_combinations"].get(peptide_key, 0) + 1
        
        return common_elements
    
    def _analyze_failure_elements(self, protocols: List[Dict]) -> Dict:
        """Analyze elements in failed protocols"""
        if not protocols:
            return {"status": "no_data"}
        
        failure_elements = {
            "common_issues": {},
            "problematic_combinations": {},
            "dosing_issues": {}
        }
        
        # Simple analysis of failure patterns
        for protocol in protocols:
            issues = protocol.get("reported_issues", [])
            for issue in issues:
                failure_elements["common_issues"][issue] = failure_elements["common_issues"].get(issue, 0) + 1
        
        return failure_elements
    
    def _analyze_dosing_patterns(self, feedback_list: List[Dict]) -> Dict:
        """Analyze optimal dosing patterns from feedback"""
        dosing_patterns = {}
        
        for feedback in feedback_list:
            modifications = feedback.get("protocol_modifications", [])
            for mod in modifications:
                if "dose" in mod.get("change", "").lower():
                    change_type = "dose_reduction" if "reduced" in mod.get("change", "").lower() else "dose_increase"
                    outcome = mod.get("outcome", "unknown")
                    
                    if change_type not in dosing_patterns:
                        dosing_patterns[change_type] = {"positive": 0, "negative": 0, "neutral": 0}
                    
                    if "better" in outcome.lower() or "improved" in outcome.lower():
                        dosing_patterns[change_type]["positive"] += 1
                    elif "worse" in outcome.lower():
                        dosing_patterns[change_type]["negative"] += 1
                    else:
                        dosing_patterns[change_type]["neutral"] += 1
        
        return dosing_patterns
    
    def _analyze_timeline_patterns(self, feedback_list: List[Dict]) -> Dict:
        """Analyze timeline patterns for improvements"""
        timeline_patterns = {
            "week_2": {"improvements": 0, "total_reports": 0},
            "month_1": {"improvements": 0, "total_reports": 0},
            "month_3": {"improvements": 0, "total_reports": 0}
        }
        
        for feedback in feedback_list:
            timeline_feedback = feedback.get("timeline_feedback", {})
            for timepoint, data in timeline_feedback.items():
                if timepoint in timeline_patterns:
                    timeline_patterns[timepoint]["total_reports"] += 1
                    # Consider improvement if any metric is > 3
                    if any(value > 3 for value in data.values() if isinstance(value, (int, float))):
                        timeline_patterns[timepoint]["improvements"] += 1
        
        return timeline_patterns
    
    def _analyze_biomarker_changes(self, feedback_list: List[Dict]) -> Dict:
        """Analyze biomarker improvement patterns"""
        biomarker_changes = {}
        
        for feedback in feedback_list:
            biomarker_data = feedback.get("specific_outcomes", {}).get("biomarker_changes", {})
            for biomarker, change in biomarker_data.items():
                if biomarker not in biomarker_changes:
                    biomarker_changes[biomarker] = {"improvements": 0, "total_reports": 0}
                
                biomarker_changes[biomarker]["total_reports"] += 1
                # Simple heuristic for improvement detection
                if "improved" in str(change).lower() or "better" in str(change).lower():
                    biomarker_changes[biomarker]["improvements"] += 1
        
        return biomarker_changes
    
    def _calculate_insight_impact(self, validation_data: Dict) -> float:
        """Calculate impact score for practitioner insights"""
        # Simple scoring based on validation data
        base_score = 1.0
        
        # Increase score based on positive outcomes
        if validation_data.get("positive_outcomes", 0) > 0:
            base_score += validation_data["positive_outcomes"] * 0.1
        
        # Increase score based on sample size
        sample_size = validation_data.get("sample_size", 1)
        if sample_size > 10:
            base_score += 0.5
        elif sample_size > 50:
            base_score += 1.0
        
        return min(base_score, 5.0)  # Cap at 5.0
    
    def _extract_practitioner_corrections(self) -> Dict:
        """Extract patterns from practitioner corrections"""
        corrections = {
            "dosing_corrections": 0,
            "safety_corrections": 0,
            "protocol_corrections": 0,
            "total_corrections": len(self.practitioner_insights)
        }
        
        for insight_id, insight in self.practitioner_insights.items():
            insight_type = insight.get("insight_data", {}).get("insight_type", "")
            if "dosing" in insight_type:
                corrections["dosing_corrections"] += 1
            elif "safety" in insight_type:
                corrections["safety_corrections"] += 1
            else:
                corrections["protocol_corrections"] += 1
        
        return corrections
    
    def _identify_emerging_treatments(self) -> Dict:
        """Identify emerging treatment patterns"""
        emerging = {
            "new_combinations": [],
            "novel_applications": [],
            "trending_peptides": {}
        }
        
        # Simple analysis of trending patterns
        for feedback_id, feedback_entry in self.feedback_database.items():
            feedback_data = feedback_entry["feedback_data"]
            if feedback_data.get("protocol_effectiveness", 0) >= 4:
                peptides = feedback_data.get("peptides_used", [])
                for peptide in peptides:
                    emerging["trending_peptides"][peptide] = emerging["trending_peptides"].get(peptide, 0) + 1
        
        return emerging
    
    def _extract_safety_insights(self) -> Dict:
        """Extract safety insights from feedback"""
        safety_insights = {
            "common_side_effects": {},
            "safety_improvements": {},
            "risk_factors": {}
        }
        
        for feedback_id, feedback_entry in self.feedback_database.items():
            feedback_data = feedback_entry["feedback_data"]
            side_effects = feedback_data.get("specific_outcomes", {}).get("side_effects", [])
            
            for effect in side_effects:
                safety_insights["common_side_effects"][effect] = safety_insights["common_side_effects"].get(effect, 0) + 1
        
        return safety_insights
    
    def _get_relevant_practitioner_insights(self, patient_profile: Dict) -> List[Dict]:
        """Get practitioner insights relevant to patient profile"""
        relevant_insights = []
        
        patient_concerns = patient_profile.get("primary_concerns", [])
        patient_conditions = patient_profile.get("medical_history", [])
        
        for insight_id, insight in self.practitioner_insights.items():
            insight_data = insight.get("insight_data", {})
            
            # Simple relevance matching
            if any(concern.lower() in insight_data.get("condition", "").lower() for concern in patient_concerns):
                relevant_insights.append(insight_data)
            elif any(condition.lower() in insight_data.get("condition", "").lower() for condition in patient_conditions):
                relevant_insights.append(insight_data)
        
        return relevant_insights
    
    def _apply_optimizations(self, base_protocol: Dict, successful_patterns: Dict, failure_patterns: Dict, relevant_insights: List[Dict]) -> Dict:
        """Apply optimizations to base protocol"""
        optimized_protocol = base_protocol.copy()
        
        # Apply insights from successful patterns
        if successful_patterns.get("peptide_combinations"):
            most_successful = max(successful_patterns["peptide_combinations"].items(), key=lambda x: x[1], default=(None, 0))
            if most_successful[0]:
                optimized_protocol["recommended_combination"] = most_successful[0].split(",")
        
        # Apply practitioner insights
        for insight in relevant_insights:
            if insight.get("confidence_level") == "high":
                optimized_protocol["practitioner_recommendations"] = optimized_protocol.get("practitioner_recommendations", [])
                optimized_protocol["practitioner_recommendations"].append(insight.get("insight", ""))
        
        return optimized_protocol

# Global instance for collective intelligence
collective_intelligence = CollectiveIntelligenceSystem()