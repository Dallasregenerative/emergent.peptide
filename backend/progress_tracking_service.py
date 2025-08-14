"""
Progress Tracking Service for PeptideProtocols.ai
Advanced patient monitoring with outcome tracking and analytics
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import uuid
from dataclasses import dataclass, asdict

@dataclass
class ProgressMetric:
    """Individual progress metric data point"""
    metric_name: str
    value: float
    unit: str
    date: str
    target_value: Optional[float] = None
    normal_range: Optional[Dict[str, float]] = None

@dataclass
class PatientProgress:
    """Comprehensive patient progress tracking"""
    patient_id: str
    protocol_id: str
    start_date: str
    metrics: List[ProgressMetric]
    milestones: List[Dict]
    notes: List[Dict]
    status: str = "active"

class ProgressTrackingService:
    """
    Service for tracking patient progress across multiple metrics
    """
    
    def __init__(self):
        self.patient_progress = {}  # In production, this would be a database
        self.metric_templates = self._initialize_metric_templates()
    
    def _initialize_metric_templates(self) -> Dict:
        """Initialize standard progress metric templates"""
        return {
            "energy_levels": {
                "name": "Energy Levels",
                "unit": "1-10 scale",
                "normal_range": {"min": 7, "max": 10},
                "target_improvement": 2,
                "frequency": "weekly"
            },
            "sleep_quality": {
                "name": "Sleep Quality",
                "unit": "1-10 scale", 
                "normal_range": {"min": 7, "max": 10},
                "target_improvement": 2,
                "frequency": "weekly"
            },
            "weight": {
                "name": "Weight",
                "unit": "lbs",
                "target_change": -15,  # Negative for weight loss
                "frequency": "weekly"
            },
            "body_fat_percentage": {
                "name": "Body Fat Percentage",
                "unit": "%",
                "normal_range": {"male": {"min": 10, "max": 15}, "female": {"min": 16, "max": 24}},
                "frequency": "monthly"
            },
            "hba1c": {
                "name": "HbA1c",
                "unit": "%",
                "normal_range": {"min": 4.0, "max": 5.6},
                "target_value": 5.5,
                "frequency": "quarterly"
            },
            "fasting_glucose": {
                "name": "Fasting Glucose",
                "unit": "mg/dL",
                "normal_range": {"min": 70, "max": 99},
                "frequency": "monthly"
            },
            "blood_pressure_systolic": {
                "name": "Systolic BP",
                "unit": "mmHg",
                "normal_range": {"min": 110, "max": 120},
                "frequency": "weekly"
            },
            "blood_pressure_diastolic": {
                "name": "Diastolic BP", 
                "unit": "mmHg",
                "normal_range": {"min": 70, "max": 80},
                "frequency": "weekly"
            },
            "crp": {
                "name": "C-Reactive Protein",
                "unit": "mg/L",
                "normal_range": {"min": 0, "max": 3.0},
                "target_value": 1.0,
                "frequency": "monthly"
            },
            "testosterone_total": {
                "name": "Total Testosterone",
                "unit": "ng/dL",
                "normal_range": {"male": {"min": 300, "max": 1000}, "female": {"min": 8, "max": 60}},
                "frequency": "quarterly"
            },
            "dhea_s": {
                "name": "DHEA-S",
                "unit": "mcg/dL",
                "normal_range": {"min": 65, "max": 380},
                "frequency": "quarterly"
            },
            "vitamin_d": {
                "name": "Vitamin D 25-OH",
                "unit": "ng/mL",
                "normal_range": {"min": 30, "max": 100},
                "target_value": 50,
                "frequency": "semi-annually"
            },
            "cognitive_function": {
                "name": "Cognitive Function Score",
                "unit": "1-10 scale",
                "normal_range": {"min": 7, "max": 10},
                "target_improvement": 2,
                "frequency": "monthly"
            },
            "joint_pain": {
                "name": "Joint Pain Level", 
                "unit": "1-10 scale",
                "target_value": 2,  # Lower is better
                "frequency": "weekly"
            },
            "recovery_time": {
                "name": "Exercise Recovery Time",
                "unit": "hours",
                "target_improvement": -12,  # Negative for improvement
                "frequency": "weekly"
            }
        }
    
    def create_patient_tracking(self, patient_id: str, protocol_id: str, initial_metrics: Dict) -> str:
        """Create new patient progress tracking"""
        tracking_id = str(uuid.uuid4())
        
        # Initialize progress metrics
        initial_progress_metrics = []
        for metric_name, value in initial_metrics.items():
            if metric_name in self.metric_templates:
                template = self.metric_templates[metric_name]
                initial_progress_metrics.append(
                    ProgressMetric(
                        metric_name=metric_name,
                        value=value,
                        unit=template["unit"],
                        date=datetime.now().isoformat(),
                        target_value=template.get("target_value"),
                        normal_range=template.get("normal_range")
                    )
                )
        
        # Create patient progress tracking
        patient_progress = PatientProgress(
            patient_id=patient_id,
            protocol_id=protocol_id,
            start_date=datetime.now().isoformat(),
            metrics=initial_progress_metrics,
            milestones=[],
            notes=[]
        )
        
        self.patient_progress[tracking_id] = patient_progress
        return tracking_id
    
    def add_progress_entry(self, tracking_id: str, metric_updates: Dict, notes: str = "") -> bool:
        """Add new progress measurements"""
        if tracking_id not in self.patient_progress:
            return False
        
        patient_progress = self.patient_progress[tracking_id]
        current_date = datetime.now().isoformat()
        
        # Add new metric measurements
        for metric_name, value in metric_updates.items():
            if metric_name in self.metric_templates:
                template = self.metric_templates[metric_name]
                new_metric = ProgressMetric(
                    metric_name=metric_name,
                    value=value,
                    unit=template["unit"],
                    date=current_date,
                    target_value=template.get("target_value"),
                    normal_range=template.get("normal_range")
                )
                patient_progress.metrics.append(new_metric)
        
        # Add notes if provided
        if notes:
            patient_progress.notes.append({
                "date": current_date,
                "note": notes,
                "type": "progress_update"
            })
        
        # Check for milestone achievements
        self._check_milestones(tracking_id)
        
        return True
    
    def _check_milestones(self, tracking_id: str):
        """Check if patient has achieved any milestones"""
        patient_progress = self.patient_progress[tracking_id]
        current_metrics = self._get_latest_metrics(tracking_id)
        
        # Define milestone criteria
        milestones_to_check = [
            {
                "name": "Energy Improvement",
                "criteria": lambda metrics: metrics.get("energy_levels", 0) >= 7,
                "description": "Energy levels reached healthy range (7+)"
            },
            {
                "name": "Sleep Quality Achievement",
                "criteria": lambda metrics: metrics.get("sleep_quality", 0) >= 7,
                "description": "Sleep quality reached optimal range (7+)"
            },
            {
                "name": "Weight Loss Milestone",
                "criteria": lambda metrics: self._calculate_weight_change(tracking_id) <= -10,
                "description": "Achieved 10+ lbs weight loss"
            },
            {
                "name": "HbA1c Improvement",
                "criteria": lambda metrics: metrics.get("hba1c", 10) <= 5.6,
                "description": "HbA1c returned to normal range (<5.7%)"
            },
            {
                "name": "Inflammation Reduction",
                "criteria": lambda metrics: metrics.get("crp", 10) <= 3.0,
                "description": "C-Reactive Protein normalized (<3.0 mg/L)"
            }
        ]
        
        for milestone in milestones_to_check:
            # Check if milestone already achieved
            existing_milestones = [m["name"] for m in patient_progress.milestones]
            if milestone["name"] not in existing_milestones:
                if milestone["criteria"](current_metrics):
                    patient_progress.milestones.append({
                        "name": milestone["name"],
                        "description": milestone["description"],
                        "achieved_date": datetime.now().isoformat(),
                        "celebration": True
                    })
    
    def _calculate_weight_change(self, tracking_id: str) -> float:
        """Calculate total weight change from start"""
        patient_progress = self.patient_progress[tracking_id]
        weight_metrics = [m for m in patient_progress.metrics if m.metric_name == "weight"]
        
        if len(weight_metrics) < 2:
            return 0
        
        initial_weight = weight_metrics[0].value
        latest_weight = weight_metrics[-1].value
        return latest_weight - initial_weight
    
    def _get_latest_metrics(self, tracking_id: str) -> Dict[str, float]:
        """Get the most recent value for each metric"""
        patient_progress = self.patient_progress[tracking_id]
        latest_metrics = {}
        
        for metric in patient_progress.metrics:
            # Keep the most recent value for each metric
            if metric.metric_name not in latest_metrics:
                latest_metrics[metric.metric_name] = metric.value
            else:
                # Compare dates and keep the more recent one
                current_date = datetime.fromisoformat(metric.date)
                existing_metric = next(m for m in patient_progress.metrics 
                                     if m.metric_name == metric.metric_name 
                                     and m.value == latest_metrics[metric.metric_name])
                existing_date = datetime.fromisoformat(existing_metric.date)
                
                if current_date > existing_date:
                    latest_metrics[metric.metric_name] = metric.value
        
        return latest_metrics
    
    def get_progress_dashboard_data(self, tracking_id: str) -> Dict:
        """Get comprehensive dashboard data for patient progress"""
        if tracking_id not in self.patient_progress:
            return {}
        
        patient_progress = self.patient_progress[tracking_id]
        
        # Organize metrics by type for charts
        chart_data = self._prepare_chart_data(tracking_id)
        
        # Calculate progress scores
        progress_scores = self._calculate_progress_scores(tracking_id)
        
        # Get upcoming milestones
        upcoming_milestones = self._get_upcoming_milestones(tracking_id)
        
        # Timeline data
        timeline_events = self._create_timeline_events(tracking_id)
        
        return {
            "patient_id": patient_progress.patient_id,
            "protocol_id": patient_progress.protocol_id,
            "start_date": patient_progress.start_date,
            "status": patient_progress.status,
            "chart_data": chart_data,
            "progress_scores": progress_scores,
            "achieved_milestones": patient_progress.milestones,
            "upcoming_milestones": upcoming_milestones,
            "timeline_events": timeline_events,
            "latest_metrics": self._get_latest_metrics(tracking_id),
            "total_days": (datetime.now() - datetime.fromisoformat(patient_progress.start_date)).days,
            "notes_count": len(patient_progress.notes),
            "metrics_count": len(patient_progress.metrics)
        }
    
    def _prepare_chart_data(self, tracking_id: str) -> Dict:
        """Prepare data formatted for chart visualization"""
        patient_progress = self.patient_progress[tracking_id]
        chart_data = {}
        
        # Group metrics by name for time series charts
        metrics_by_name = {}
        for metric in patient_progress.metrics:
            if metric.metric_name not in metrics_by_name:
                metrics_by_name[metric.metric_name] = []
            
            metrics_by_name[metric.metric_name].append({
                "date": metric.date,
                "value": metric.value,
                "unit": metric.unit,
                "target": metric.target_value,
                "normal_min": metric.normal_range.get("min") if metric.normal_range else None,
                "normal_max": metric.normal_range.get("max") if metric.normal_range else None
            })
        
        # Sort by date for each metric
        for metric_name in metrics_by_name:
            metrics_by_name[metric_name].sort(key=lambda x: x["date"])
        
        chart_data["time_series"] = metrics_by_name
        
        # Create progress comparison chart
        latest_metrics = self._get_latest_metrics(tracking_id)
        progress_comparison = []
        
        for metric_name, current_value in latest_metrics.items():
            template = self.metric_templates.get(metric_name, {})
            normal_range = template.get("normal_range", {})
            
            # Determine if metric is in normal range
            in_range = True
            if normal_range:
                if isinstance(normal_range, dict) and "min" in normal_range:
                    in_range = normal_range["min"] <= current_value <= normal_range["max"]
            
            progress_comparison.append({
                "metric": template.get("name", metric_name),
                "current": current_value,
                "unit": template.get("unit", ""),
                "status": "normal" if in_range else "attention",
                "target": template.get("target_value"),
                "normal_range": normal_range
            })
        
        chart_data["progress_comparison"] = progress_comparison
        
        return chart_data
    
    def _calculate_progress_scores(self, tracking_id: str) -> Dict:
        """Calculate overall progress scores"""
        latest_metrics = self._get_latest_metrics(tracking_id)
        patient_progress = self.patient_progress[tracking_id]
        start_date = datetime.fromisoformat(patient_progress.start_date)
        
        # Get initial values for comparison
        initial_metrics = {}
        for metric in patient_progress.metrics:
            if metric.metric_name not in initial_metrics:
                initial_metrics[metric.metric_name] = metric.value
        
        scores = {
            "overall_improvement": 0,
            "symptom_improvement": 0,
            "biomarker_improvement": 0,
            "lifestyle_improvement": 0
        }
        
        # Calculate improvements
        symptom_metrics = ["energy_levels", "sleep_quality", "cognitive_function", "joint_pain"]
        biomarker_metrics = ["hba1c", "crp", "testosterone_total", "dhea_s", "vitamin_d"]
        lifestyle_metrics = ["weight", "body_fat_percentage", "recovery_time"]
        
        # Symptom score (1-10 scale metrics)
        symptom_improvements = []
        for metric in symptom_metrics:
            if metric in latest_metrics and metric in initial_metrics:
                if metric == "joint_pain":  # Lower is better
                    improvement = initial_metrics[metric] - latest_metrics[metric]
                else:  # Higher is better
                    improvement = latest_metrics[metric] - initial_metrics[metric]
                symptom_improvements.append(max(0, improvement))
        
        if symptom_improvements:
            scores["symptom_improvement"] = min(100, (sum(symptom_improvements) / len(symptom_improvements)) * 10)
        
        # Biomarker score (normalized improvements)
        biomarker_improvements = []
        for metric in biomarker_metrics:
            if metric in latest_metrics and metric in initial_metrics:
                template = self.metric_templates[metric]
                if "target_value" in template:
                    initial_distance = abs(initial_metrics[metric] - template["target_value"])
                    current_distance = abs(latest_metrics[metric] - template["target_value"])
                    if initial_distance > 0:
                        improvement = (initial_distance - current_distance) / initial_distance * 100
                        biomarker_improvements.append(max(0, improvement))
        
        if biomarker_improvements:
            scores["biomarker_improvement"] = sum(biomarker_improvements) / len(biomarker_improvements)
        
        # Lifestyle score
        lifestyle_improvements = []
        for metric in lifestyle_metrics:
            if metric in latest_metrics and metric in initial_metrics:
                if metric in ["weight", "body_fat_percentage", "recovery_time"]:  # Lower is better
                    improvement = (initial_metrics[metric] - latest_metrics[metric]) / initial_metrics[metric] * 100
                    lifestyle_improvements.append(max(0, improvement))
        
        if lifestyle_improvements:
            scores["lifestyle_improvement"] = sum(lifestyle_improvements) / len(lifestyle_improvements)
        
        # Overall score
        scores["overall_improvement"] = (
            scores["symptom_improvement"] * 0.4 +
            scores["biomarker_improvement"] * 0.4 +
            scores["lifestyle_improvement"] * 0.2
        )
        
        return scores
    
    def _get_upcoming_milestones(self, tracking_id: str) -> List[Dict]:
        """Get milestones the patient is close to achieving"""
        latest_metrics = self._get_latest_metrics(tracking_id)
        patient_progress = self.patient_progress[tracking_id]
        achieved_milestones = [m["name"] for m in patient_progress.milestones]
        
        upcoming = []
        
        # Check each potential milestone
        if "Energy Improvement" not in achieved_milestones:
            current_energy = latest_metrics.get("energy_levels", 0)
            if current_energy >= 5:  # Close to achievement
                upcoming.append({
                    "name": "Energy Improvement",
                    "description": "Reach energy level of 7+",
                    "current_progress": f"{current_energy}/10",
                    "completion_percentage": min(100, (current_energy / 7) * 100)
                })
        
        if "Weight Loss Milestone" not in achieved_milestones:
            weight_change = self._calculate_weight_change(tracking_id)
            if weight_change <= -5:  # Lost at least 5 lbs
                upcoming.append({
                    "name": "Weight Loss Milestone",
                    "description": "Lose 10+ pounds",
                    "current_progress": f"{abs(weight_change):.1f}/10 lbs",
                    "completion_percentage": min(100, (abs(weight_change) / 10) * 100)
                })
        
        return upcoming
    
    def _create_timeline_events(self, tracking_id: str) -> List[Dict]:
        """Create timeline of significant events and progress"""
        patient_progress = self.patient_progress[tracking_id]
        events = []
        
        # Add start date
        events.append({
            "date": patient_progress.start_date,
            "type": "start",
            "title": "Protocol Started",
            "description": "Began functional medicine protocol"
        })
        
        # Add milestone achievements
        for milestone in patient_progress.milestones:
            events.append({
                "date": milestone["achieved_date"],
                "type": "milestone",
                "title": milestone["name"],
                "description": milestone["description"]
            })
        
        # Add significant metric improvements
        metrics_by_name = {}
        for metric in patient_progress.metrics:
            if metric.metric_name not in metrics_by_name:
                metrics_by_name[metric.metric_name] = []
            metrics_by_name[metric.metric_name].append(metric)
        
        for metric_name, metric_list in metrics_by_name.items():
            if len(metric_list) >= 2:
                metric_list.sort(key=lambda x: x.date)
                initial = metric_list[0]
                latest = metric_list[-1]
                
                # Check for significant improvement
                improvement_threshold = 0.2  # 20% improvement
                if initial.value != 0:
                    change_percent = abs(latest.value - initial.value) / initial.value
                    if change_percent >= improvement_threshold:
                        events.append({
                            "date": latest.date,
                            "type": "improvement",
                            "title": f"{initial.metric_name.replace('_', ' ').title()} Improved",
                            "description": f"Improved from {initial.value} to {latest.value} {initial.unit}"
                        })
        
        # Sort events by date
        events.sort(key=lambda x: x["date"])
        
        return events

# Global progress tracking service
progress_service = ProgressTrackingService()