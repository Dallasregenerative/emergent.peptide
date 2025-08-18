"""
Enhanced Collective Learning System for PeptideProtocols.ai
Handles protocol anonymization, rating, feedback, and storage for continuous learning
"""

import hashlib
import uuid
import json
import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from enum import Enum
import logging
from cryptography.fernet import Fernet
import base64
import os

logger = logging.getLogger(__name__)

class ProtocolAccuracy(str, Enum):
    HIGHLY_ACCURATE = "highly_accurate"
    MOSTLY_ACCURATE = "mostly_accurate"
    PARTIALLY_ACCURATE = "partially_accurate"
    NEEDS_IMPROVEMENT = "needs_improvement"

class FeedbackType(str, Enum):
    DOSING_ADJUSTMENT = "dosing_adjustment"
    SAFETY_CONCERN = "safety_concern"
    EFFICACY_IMPROVEMENT = "efficacy_improvement"
    CONTRAINDICATION_MISSING = "contraindication_missing"
    STACKING_SUGGESTION = "stacking_suggestion"
    MONITORING_ADDITION = "monitoring_addition"
    GENERAL_IMPROVEMENT = "general_improvement"

class CollectiveLearningService:
    """
    Service for managing collective learning through anonymized protocol storage
    """
    
    def __init__(self):
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for data anonymization"""
        key_path = "/app/backend/.protocol_encryption_key"
        
        if os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                return key_file.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_path, 'wb') as key_file:
                key_file.write(key)
            os.chmod(key_path, 0o600)  # Restrict permissions
            return key
    
    def generate_protocol_number(self, patient_data: Dict[str, Any]) -> str:
        """
        Generate unique protocol number for anonymization
        Format: PPA-YYYY-XXXXXXXX (PeptideProtocols Anonymized)
        """
        # Create unique identifier from patient data and timestamp
        identifier_data = f"{patient_data.get('first_name', '')}{patient_data.get('last_name', '')}{patient_data.get('date_of_birth', '')}{datetime.now().isoformat()}"
        hash_digest = hashlib.sha256(identifier_data.encode()).hexdigest()[:8]
        
        year = datetime.now().year
        protocol_number = f"PPA-{year}-{hash_digest.upper()}"
        
        return protocol_number
    
    def anonymize_protocol_data(self, protocol_data: Dict[str, Any], patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Anonymize protocol data by removing/encrypting sensitive information
        """
        protocol_number = self.generate_protocol_number(patient_data)
        
        # Create anonymized copy
        anonymized_data = protocol_data.copy()
        
        # Remove direct patient identifiers
        sensitive_fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        for field in sensitive_fields:
            if field in anonymized_data:
                del anonymized_data[field]
        
        # Encrypt date of birth and store protocol mapping
        encrypted_dob = None
        if patient_data.get('date_of_birth'):
            encrypted_dob = self.cipher_suite.encrypt(patient_data['date_of_birth'].encode()).decode()
        
        # Add anonymization metadata
        anonymized_data.update({
            'protocol_number': protocol_number,
            'encrypted_dob': encrypted_dob,
            'anonymized_at': datetime.now(timezone.utc).isoformat(),
            'is_anonymized': True,
            'original_patient_id': None,  # Remove patient ID reference
        })
        
        # Anonymize free-text fields (remove potential identifiers)
        text_fields = ['medical_history', 'current_medications', 'lifestyle_factors', 'goals']
        for field in text_fields:
            if field in anonymized_data:
                anonymized_data[field] = self._anonymize_text(anonymized_data[field])
        
        return anonymized_data
    
    def _anonymize_text(self, text: str) -> str:
        """
        Remove potential identifiers from free text
        """
        if not text:
            return text
        
        # Remove common name patterns (simple approach)
        # In production, this would use more sophisticated NLP
        text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[Name]', text)  # Common name patterns
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)  # SSN patterns
        text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[Phone]', text)  # Phone patterns
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[Email]', text)  # Email patterns
        
        return text
    
    def store_anonymized_protocol(self, anonymized_data: Dict[str, Any], practitioner_feedback: Dict[str, Any] = None) -> str:
        """
        Store anonymized protocol in collective learning database
        """
        protocol_number = anonymized_data['protocol_number']
        
        # Add feedback if provided
        if practitioner_feedback:
            anonymized_data['practitioner_feedback'] = {
                **practitioner_feedback,
                'feedback_date': datetime.now(timezone.utc).isoformat(),
                'feedback_id': str(uuid.uuid4())
            }
        
        # Add metadata for collective learning
        anonymized_data.update({
            'learning_metadata': {
                'created_for_learning': datetime.now(timezone.utc).isoformat(),
                'version': '1.0',
                'learning_status': 'active',
                'reference_count': 0,
                'last_referenced': None
            }
        })
        
        # In a real implementation, this would be stored in MongoDB
        # For now, we'll store in a JSON file as proof of concept
        storage_path = f"/app/backend/collective_learning_protocols/{protocol_number}.json"
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        
        with open(storage_path, 'w') as f:
            json.dump(anonymized_data, f, indent=2, default=str)
        
        logger.info(f"Anonymized protocol {protocol_number} stored for collective learning")
        return protocol_number
    
    def create_practitioner_feedback(self, 
                                   protocol_rating: int,
                                   accuracy_assessment: ProtocolAccuracy,
                                   identified_inaccuracies: List[str],
                                   suggested_improvements: List[Dict[str, Any]],
                                   practitioner_id: str,
                                   additional_notes: str = None) -> Dict[str, Any]:
        """
        Create structured practitioner feedback for protocol
        """
        feedback = {
            'rating': protocol_rating,
            'accuracy_assessment': accuracy_assessment,
            'identified_inaccuracies': identified_inaccuracies,
            'suggested_improvements': suggested_improvements,
            'practitioner_id': practitioner_id,
            'additional_notes': additional_notes,
            'feedback_timestamp': datetime.now(timezone.utc).isoformat(),
            'feedback_version': '1.0'
        }
        
        return feedback
    
    def retrieve_protocol_by_number(self, protocol_number: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve anonymized protocol by protocol number
        """
        try:
            storage_path = f"/app/backend/collective_learning_protocols/{protocol_number}.json"
            
            if not os.path.exists(storage_path):
                return None
            
            with open(storage_path, 'r') as f:
                protocol_data = json.load(f)
            
            # Update reference count and last referenced
            if 'learning_metadata' in protocol_data:
                protocol_data['learning_metadata']['reference_count'] += 1
                protocol_data['learning_metadata']['last_referenced'] = datetime.now(timezone.utc).isoformat()
                
                # Save updated metadata
                with open(storage_path, 'w') as f:
                    json.dump(protocol_data, f, indent=2, default=str)
            
            return protocol_data
            
        except Exception as e:
            logger.error(f"Error retrieving protocol {protocol_number}: {e}")
            return None
    
    def add_protocol_update(self, protocol_number: str, update_data: Dict[str, Any]) -> bool:
        """
        Add update/feedback to existing protocol for continuous learning
        """
        try:
            protocol_data = self.retrieve_protocol_by_number(protocol_number)
            if not protocol_data:
                return False
            
            # Initialize updates array if not exists
            if 'protocol_updates' not in protocol_data:
                protocol_data['protocol_updates'] = []
            
            # Add new update
            update_entry = {
                'update_id': str(uuid.uuid4()),
                'update_timestamp': datetime.now(timezone.utc).isoformat(),
                'update_type': update_data.get('type', 'general'),
                'update_content': update_data,
                'source': update_data.get('source', 'practitioner')
            }
            
            protocol_data['protocol_updates'].append(update_entry)
            
            # Save updated protocol
            storage_path = f"/app/backend/collective_learning_protocols/{protocol_number}.json"
            with open(storage_path, 'w') as f:
                json.dump(protocol_data, f, indent=2, default=str)
            
            logger.info(f"Added update to protocol {protocol_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding update to protocol {protocol_number}: {e}")
            return False
    
    def get_learning_analytics(self) -> Dict[str, Any]:
        """
        Get analytics about collective learning system usage
        """
        try:
            protocols_dir = "/app/backend/collective_learning_protocols"
            if not os.path.exists(protocols_dir):
                return {
                    'total_protocols': 0,
                    'total_feedback_entries': 0,
                    'average_rating': 0,
                    'most_common_improvements': [],
                    'learning_trends': {}
                }
            
            protocol_files = [f for f in os.listdir(protocols_dir) if f.endswith('.json')]
            
            total_protocols = len(protocol_files)
            total_feedback = 0
            ratings = []
            improvement_types = []
            
            for file in protocol_files:
                try:
                    with open(os.path.join(protocols_dir, file), 'r') as f:
                        protocol_data = json.load(f)
                    
                    # Count feedback entries
                    if 'practitioner_feedback' in protocol_data:
                        total_feedback += 1
                        ratings.append(protocol_data['practitioner_feedback']['rating'])
                        
                        # Collect improvement types
                        improvements = protocol_data['practitioner_feedback'].get('suggested_improvements', [])
                        for improvement in improvements:
                            improvement_types.append(improvement.get('type', 'general'))
                    
                    # Count protocol updates
                    if 'protocol_updates' in protocol_data:
                        total_feedback += len(protocol_data['protocol_updates'])
                        
                except Exception as e:
                    logger.error(f"Error processing protocol file {file}: {e}")
                    continue
            
            # Calculate analytics
            average_rating = sum(ratings) / len(ratings) if ratings else 0
            
            # Count improvement types
            improvement_counts = {}
            for imp_type in improvement_types:
                improvement_counts[imp_type] = improvement_counts.get(imp_type, 0) + 1
            
            most_common_improvements = sorted(improvement_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                'total_protocols': total_protocols,
                'total_feedback_entries': total_feedback,
                'average_rating': round(average_rating, 2),
                'most_common_improvements': most_common_improvements,
                'learning_trends': {
                    'protocols_with_feedback': len(ratings),
                    'feedback_participation_rate': round((len(ratings) / total_protocols * 100), 2) if total_protocols > 0 else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating learning analytics: {e}")
            return {}
    
    def search_similar_protocols(self, symptoms: List[str], conditions: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar protocols in collective learning database
        """
        try:
            protocols_dir = "/app/backend/collective_learning_protocols"
            if not os.path.exists(protocols_dir):
                return []
            
            protocol_files = [f for f in os.listdir(protocols_dir) if f.endswith('.json')]
            similar_protocols = []
            
            for file in protocol_files[:limit]:  # Simple implementation - in production would use vector search
                try:
                    with open(os.path.join(protocols_dir, file), 'r') as f:
                        protocol_data = json.load(f)
                    
                    # Simple similarity check (in production would use semantic similarity)
                    protocol_symptoms = protocol_data.get('symptoms', [])
                    protocol_conditions = protocol_data.get('medical_conditions', [])
                    
                    similarity_score = 0
                    for symptom in symptoms:
                        if any(symptom.lower() in ps.lower() for ps in protocol_symptoms):
                            similarity_score += 1
                    
                    for condition in conditions:
                        if any(condition.lower() in pc.lower() for pc in protocol_conditions):
                            similarity_score += 2  # Weight conditions higher
                    
                    if similarity_score > 0:
                        similar_protocols.append({
                            'protocol_number': protocol_data['protocol_number'],
                            'similarity_score': similarity_score,
                            'rating': protocol_data.get('practitioner_feedback', {}).get('rating', 0),
                            'peptides_used': protocol_data.get('recommended_peptides', []),
                            'created_date': protocol_data.get('anonymized_at', '')
                        })
                        
                except Exception as e:
                    logger.error(f"Error processing protocol file {file}: {e}")
                    continue
            
            # Sort by similarity score and rating
            similar_protocols.sort(key=lambda x: (x['similarity_score'], x['rating']), reverse=True)
            return similar_protocols[:limit]
            
        except Exception as e:
            logger.error(f"Error searching similar protocols: {e}")
            return []

# Global instance
collective_learning_service = CollectiveLearningService()