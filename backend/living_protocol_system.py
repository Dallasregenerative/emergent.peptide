"""
Living Protocol System - User and Practitioner Voting and Feedback
Real-time protocol feedback, outcome tracking, and collaborative intelligence
"""

from datetime import datetime, timedelta
import uuid
from typing import Dict, List, Optional
import logging

class LivingProtocolSystem:
    """
    Manages real-time protocol feedback, voting, and outcome statistics
    Implements "living protocol" learning loop for continuous improvement
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.feedback_collection = self.db.protocol_feedback
        self.voting_collection = self.db.protocol_voting  
        self.outcomes_collection = self.db.protocol_outcomes
        self.user_sessions_collection = self.db.user_sessions
        
    async def submit_protocol_vote(self, protocol_data: Dict) -> Dict:
        """
        Submit user or practitioner vote for protocol effectiveness
        """
        try:
            vote_data = {
                "vote_id": str(uuid.uuid4()),
                "protocol_name": protocol_data.get("protocol_name"),
                "user_type": protocol_data.get("user_type", "user"),  # "user" or "practitioner"
                "user_id": protocol_data.get("user_id", "anonymous"),
                "ratings": {
                    "effectiveness": protocol_data.get("effectiveness_rating", 0),  # 1-5 scale
                    "safety": protocol_data.get("safety_rating", 0),  # 1-5 scale
                    "value": protocol_data.get("value_rating", 0),  # 1-5 scale
                    "would_recommend": protocol_data.get("would_recommend", False)
                },
                "experience_details": {
                    "usage_duration": protocol_data.get("usage_duration", ""),  # e.g. "8 weeks"
                    "dosage_used": protocol_data.get("dosage_used", ""),
                    "side_effects": protocol_data.get("side_effects", []),
                    "benefits_experienced": protocol_data.get("benefits_experienced", []),
                    "improvement_percentage": protocol_data.get("improvement_percentage", 0)
                },
                "comments": protocol_data.get("comments", ""),
                "timestamp": datetime.utcnow(),
                "verified_practitioner": protocol_data.get("verified_practitioner", False)
            }
            
            # Store the vote
            result = await self.voting_collection.insert_one(vote_data)
            
            # Update protocol aggregate statistics
            await self._update_protocol_statistics(vote_data["protocol_name"])
            
            return {
                "success": True,
                "vote_id": vote_data["vote_id"],
                "message": "Vote submitted successfully"
            }
            
        except Exception as e:
            logging.error(f"Error submitting protocol vote: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def submit_protocol_outcome(self, outcome_data: Dict) -> Dict:
        """
        Submit real patient/practitioner protocol outcome data
        """
        try:
            outcome_record = {
                "outcome_id": str(uuid.uuid4()),
                "protocol_name": outcome_data.get("protocol_name"),
                "user_type": outcome_data.get("user_type", "user"),
                "practitioner_id": outcome_data.get("practitioner_id"),
                "patient_demographics": {
                    "age_range": outcome_data.get("age_range", ""),  # e.g. "30-40"
                    "gender": outcome_data.get("gender", ""),
                    "health_conditions": outcome_data.get("health_conditions", [])
                },
                "treatment_details": {
                    "duration_weeks": outcome_data.get("duration_weeks", 0),
                    "dosage_protocol": outcome_data.get("dosage_protocol", ""),
                    "administration_method": outcome_data.get("administration_method", ""),
                    "concurrent_treatments": outcome_data.get("concurrent_treatments", [])
                },
                "outcomes": {
                    "primary_goal_achievement": outcome_data.get("primary_goal_achievement", 0),  # 0-100%
                    "side_effects_severity": outcome_data.get("side_effects_severity", 0),  # 1-5 scale
                    "quality_of_life_improvement": outcome_data.get("quality_of_life_improvement", 0),  # 0-100%
                    "biomarker_improvements": outcome_data.get("biomarker_improvements", {}),
                    "objective_measures": outcome_data.get("objective_measures", {}),  # lab values, body comp, etc.
                },
                "practitioner_notes": outcome_data.get("practitioner_notes", ""),
                "follow_up_status": outcome_data.get("follow_up_status", "ongoing"),
                "timestamp": datetime.utcnow(),
                "verified": outcome_data.get("verified", False)
            }
            
            # Store the outcome data
            result = await self.outcomes_collection.insert_one(outcome_record)
            
            # Update protocol outcome statistics
            await self._update_outcome_statistics(outcome_record["protocol_name"])
            
            return {
                "success": True,
                "outcome_id": outcome_record["outcome_id"],
                "message": "Outcome data submitted successfully"
            }
            
        except Exception as e:
            logging.error(f"Error submitting protocol outcome: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def get_protocol_statistics(self, protocol_name: str) -> Dict:
        """
        Get comprehensive statistics for a protocol
        """
        try:
            # Get voting statistics
            vote_stats = await self._calculate_voting_statistics(protocol_name)
            
            # Get outcome statistics
            outcome_stats = await self._calculate_outcome_statistics(protocol_name)
            
            # Get recent feedback
            recent_feedback = await self._get_recent_feedback(protocol_name, limit=10)
            
            return {
                "protocol_name": protocol_name,
                "voting_statistics": vote_stats,
                "outcome_statistics": outcome_stats,
                "recent_feedback": recent_feedback,
                "last_updated": datetime.utcnow().isoformat(),
                "total_data_points": vote_stats.get("total_votes", 0) + outcome_stats.get("total_outcomes", 0)
            }
            
        except Exception as e:
            logging.error(f"Error getting protocol statistics: {str(e)}")
            return {"error": str(e)}
    
    async def _calculate_voting_statistics(self, protocol_name: str) -> Dict:
        """Calculate voting statistics for a protocol"""
        votes_cursor = self.voting_collection.find({"protocol_name": protocol_name})
        votes = await votes_cursor.to_list(None)
        
        if not votes:
            return {
                "total_votes": 0,
                "average_ratings": {"effectiveness": 0, "safety": 0, "value": 0},
                "recommendation_rate": 0,
                "user_breakdown": {"users": 0, "practitioners": 0}
            }
        
        total_votes = len(votes)
        effectiveness_ratings = [v["ratings"]["effectiveness"] for v in votes if v["ratings"]["effectiveness"] > 0]
        safety_ratings = [v["ratings"]["safety"] for v in votes if v["ratings"]["safety"] > 0]
        value_ratings = [v["ratings"]["value"] for v in votes if v["ratings"]["value"] > 0]
        
        recommendations = sum(1 for v in votes if v["ratings"].get("would_recommend", False))
        users = sum(1 for v in votes if v["user_type"] == "user")
        practitioners = sum(1 for v in votes if v["user_type"] == "practitioner")
        
        return {
            "total_votes": total_votes,
            "average_ratings": {
                "effectiveness": round(sum(effectiveness_ratings) / len(effectiveness_ratings), 2) if effectiveness_ratings else 0,
                "safety": round(sum(safety_ratings) / len(safety_ratings), 2) if safety_ratings else 0,
                "value": round(sum(value_ratings) / len(value_ratings), 2) if value_ratings else 0
            },
            "recommendation_rate": round((recommendations / total_votes) * 100, 1) if total_votes > 0 else 0,
            "user_breakdown": {
                "users": users,
                "practitioners": practitioners
            }
        }
    
    async def _calculate_outcome_statistics(self, protocol_name: str) -> Dict:
        """Calculate outcome statistics for a protocol"""
        outcomes_cursor = self.outcomes_collection.find({"protocol_name": protocol_name})
        outcomes = await outcomes_cursor.to_list(None)
        
        if not outcomes:
            return {
                "total_outcomes": 0,
                "success_rate": 0,
                "average_improvement": 0,
                "side_effect_rate": 0
            }
        
        total_outcomes = len(outcomes)
        successful_outcomes = sum(1 for o in outcomes if o["outcomes"]["primary_goal_achievement"] >= 70)
        improvements = [o["outcomes"]["primary_goal_achievement"] for o in outcomes]
        side_effects = sum(1 for o in outcomes if o["outcomes"]["side_effects_severity"] >= 3)
        
        return {
            "total_outcomes": total_outcomes,
            "success_rate": round((successful_outcomes / total_outcomes) * 100, 1) if total_outcomes > 0 else 0,
            "average_improvement": round(sum(improvements) / len(improvements), 1) if improvements else 0,
            "side_effect_rate": round((side_effects / total_outcomes) * 100, 1) if total_outcomes > 0 else 0
        }
    
    async def _get_recent_feedback(self, protocol_name: str, limit: int = 10) -> List[Dict]:
        """Get recent feedback for a protocol"""
        recent_votes_cursor = self.voting_collection.find(
            {"protocol_name": protocol_name, "comments": {"$ne": ""}},
            {"comments": 1, "ratings": 1, "user_type": 1, "timestamp": 1}
        ).sort("timestamp", -1).limit(limit)
        
        recent_votes = await recent_votes_cursor.to_list(None)
        
        return [
            {
                "comment": vote["comments"],
                "ratings": vote["ratings"],
                "user_type": vote["user_type"],
                "timestamp": vote["timestamp"].isoformat()
            }
            for vote in recent_votes
        ]
    
    async def _update_protocol_statistics(self, protocol_name: str):
        """Update cached protocol statistics"""
        try:
            stats = await self.get_protocol_statistics(protocol_name)
            # This would typically update a cached statistics collection
            # For now, we'll log the update
            logging.info(f"Updated statistics for protocol: {protocol_name}")
        except Exception as e:
            logging.error(f"Error updating protocol statistics: {str(e)}")
    
    async def _update_outcome_statistics(self, protocol_name: str):
        """Update cached outcome statistics"""
        try:
            # Similar to above, this would update cached statistics
            logging.info(f"Updated outcome statistics for protocol: {protocol_name}")
        except Exception as e:
            logging.error(f"Error updating outcome statistics: {str(e)}")
    
    async def get_trending_protocols(self, time_period: str = "30d", limit: int = 10) -> List[Dict]:
        """
        Get trending protocols based on recent activity and positive feedback
        """
        try:
            # Calculate date range
            if time_period == "7d":
                start_date = datetime.utcnow() - timedelta(days=7)
            elif time_period == "30d":
                start_date = datetime.utcnow() - timedelta(days=30)
            elif time_period == "90d":
                start_date = datetime.utcnow() - timedelta(days=90)
            else:
                start_date = datetime.utcnow() - timedelta(days=30)
            
            # Aggregate recent voting data
            pipeline = [
                {"$match": {"timestamp": {"$gte": start_date}}},
                {"$group": {
                    "_id": "$protocol_name",
                    "total_votes": {"$sum": 1},
                    "avg_effectiveness": {"$avg": "$ratings.effectiveness"},
                    "avg_safety": {"$avg": "$ratings.safety"},
                    "avg_value": {"$avg": "$ratings.value"},
                    "recommendations": {"$sum": {"$cond": ["$ratings.would_recommend", 1, 0]}}
                }},
                {"$addFields": {
                    "recommendation_rate": {"$multiply": [{"$divide": ["$recommendations", "$total_votes"]}, 100]},
                    "overall_score": {"$add": ["$avg_effectiveness", "$avg_safety", "$avg_value"]}
                }},
                {"$sort": {"overall_score": -1, "total_votes": -1}},
                {"$limit": limit}
            ]
            
            trending_cursor = self.voting_collection.aggregate(pipeline)
            trending = await trending_cursor.to_list(None)
            
            return [
                {
                    "protocol_name": item["_id"],
                    "total_votes": item["total_votes"],
                    "average_ratings": {
                        "effectiveness": round(item["avg_effectiveness"], 2),
                        "safety": round(item["avg_safety"], 2),
                        "value": round(item["avg_value"], 2)
                    },
                    "recommendation_rate": round(item["recommendation_rate"], 1),
                    "overall_score": round(item["overall_score"], 2)
                }
                for item in trending
            ]
            
        except Exception as e:
            logging.error(f"Error getting trending protocols: {str(e)}")
            return []
    
    async def get_protocol_comparisons(self, protocol_names: List[str]) -> Dict:
        """
        Compare multiple protocols based on user feedback and outcomes
        """
        try:
            comparisons = {}
            
            for protocol_name in protocol_names:
                stats = await self.get_protocol_statistics(protocol_name)
                comparisons[protocol_name] = {
                    "voting_stats": stats.get("voting_statistics", {}),
                    "outcome_stats": stats.get("outcome_statistics", {}),
                    "total_data_points": stats.get("total_data_points", 0)
                }
            
            return {
                "comparisons": comparisons,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error generating protocol comparisons: {str(e)}")
            return {"error": str(e)}

# Synchronous wrapper for integration with existing system
class LivingProtocolManager:
    """
    Synchronous manager for living protocol features
    """
    
    def __init__(self):
        self.feedback_data = {}  # In-memory storage for demo
        self.voting_data = {}
        self.outcome_data = {}
    
    def submit_vote(self, protocol_name: str, vote_data: Dict) -> Dict:
        """Submit a protocol vote"""
        if protocol_name not in self.voting_data:
            self.voting_data[protocol_name] = []
        
        vote_record = {
            "vote_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            **vote_data
        }
        
        self.voting_data[protocol_name].append(vote_record)
        
        return {
            "success": True,
            "vote_id": vote_record["vote_id"],
            "message": "Vote submitted successfully"
        }
    
    def submit_outcome(self, protocol_name: str, outcome_data: Dict) -> Dict:
        """Submit protocol outcome data"""
        if protocol_name not in self.outcome_data:
            self.outcome_data[protocol_name] = []
        
        outcome_record = {
            "outcome_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            **outcome_data
        }
        
        self.outcome_data[protocol_name].append(outcome_record)
        
        return {
            "success": True,
            "outcome_id": outcome_record["outcome_id"],
            "message": "Outcome data submitted successfully"
        }
    
    def get_protocol_stats(self, protocol_name: str) -> Dict:
        """Get protocol statistics"""
        votes = self.voting_data.get(protocol_name, [])
        outcomes = self.outcome_data.get(protocol_name, [])
        
        if not votes and not outcomes:
            return {
                "protocol_name": protocol_name,
                "total_votes": 0,
                "total_outcomes": 0,
                "average_ratings": {"effectiveness": 0, "safety": 0, "value": 0},
                "success_rate": 0,
                "last_updated": datetime.utcnow().isoformat()
            }
        
        # Calculate voting statistics
        if votes:
            effectiveness_ratings = [v.get("effectiveness_rating", 0) for v in votes]
            safety_ratings = [v.get("safety_rating", 0) for v in votes]
            value_ratings = [v.get("value_rating", 0) for v in votes]
            
            avg_effectiveness = sum(effectiveness_ratings) / len(effectiveness_ratings) if effectiveness_ratings else 0
            avg_safety = sum(safety_ratings) / len(safety_ratings) if safety_ratings else 0
            avg_value = sum(value_ratings) / len(value_ratings) if value_ratings else 0
        else:
            avg_effectiveness = avg_safety = avg_value = 0
        
        # Calculate outcome statistics
        if outcomes:
            successful_outcomes = sum(1 for o in outcomes if o.get("primary_goal_achievement", 0) >= 70)
            success_rate = (successful_outcomes / len(outcomes)) * 100
        else:
            success_rate = 0
        
        return {
            "protocol_name": protocol_name,
            "total_votes": len(votes),
            "total_outcomes": len(outcomes),
            "average_ratings": {
                "effectiveness": round(avg_effectiveness, 2),
                "safety": round(avg_safety, 2),
                "value": round(avg_value, 2)
            },
            "success_rate": round(success_rate, 1),
            "total_data_points": len(votes) + len(outcomes),
            "last_updated": datetime.utcnow().isoformat()
        }

# Global instance for use in API endpoints
living_protocol_manager = LivingProtocolManager()