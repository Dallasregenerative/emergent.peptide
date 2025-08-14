"""
Master Protocol Manager - Comprehensive Protocol Library Management
Handles all protocol data, search, filtering, PDF generation, and analytics
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

# Import all existing protocol batches
from enhanced_clinical_database import ENHANCED_CLINICAL_PEPTIDES
from complete_enhanced_protocols_batch2 import COMPLETE_PROTOCOLS_BATCH2
from accelerated_batch3_protocols import ACCELERATED_BATCH3_PROTOCOLS
from final_completion_batch4 import FINAL_COMPLETION_BATCH4
from critical_missing_peptides_batch5 import CRITICAL_MISSING_PEPTIDES_BATCH5
from essential_peptide_blends_batch6 import ESSENTIAL_PEPTIDE_BLENDS_BATCH6
from advanced_weight_management_batch7 import ADVANCED_WEIGHT_MANAGEMENT_BATCH7
from capsule_protocols_batch8 import CAPSULE_PROTOCOLS_BATCH8

class MasterProtocolManager:
    def __init__(self):
        self.all_protocols = []
        self.categories = set()
        self.tags = set()
        self._compile_all_protocols()
        self._generate_search_indices()
        
    def _compile_all_protocols(self):
        """Compile all protocols from various batches into unified format"""
        all_batches = [
            ENHANCED_CLINICAL_PEPTIDES,
            COMPLETE_PROTOCOLS_BATCH2,
            ACCELERATED_BATCH3_PROTOCOLS,
            FINAL_COMPLETION_BATCH4,
            CRITICAL_MISSING_PEPTIDES_BATCH5,
            ESSENTIAL_PEPTIDE_BLENDS_BATCH6,
            ADVANCED_WEIGHT_MANAGEMENT_BATCH7,
            CAPSULE_PROTOCOLS_BATCH8
        ]
        
        for batch in all_batches:
            for protocol in batch:
                enhanced_protocol = self._enhance_protocol(protocol)
                self.all_protocols.append(enhanced_protocol)
                
                # Extract categories and tags
                if 'category' in protocol:
                    self.categories.add(protocol['category'])
                if 'tags' in protocol:
                    self.tags.update(protocol['tags'])
                    
        print(f"✓ Compiled {len(self.all_protocols)} protocols across {len(self.categories)} categories")
        
    def _enhance_protocol(self, protocol: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance protocol with additional metadata and standardized fields"""
        enhanced = protocol.copy()
        
        # Add unique ID if missing
        if 'id' not in enhanced:
            enhanced['id'] = str(uuid.uuid4())
            
        # Add timestamps
        enhanced['last_updated'] = datetime.utcnow().isoformat()
        enhanced['created_at'] = datetime.utcnow().isoformat()
        
        # Standardize tags
        if 'tags' not in enhanced:
            enhanced['tags'] = self._generate_tags(enhanced)
            
        # Add search keywords
        enhanced['search_keywords'] = self._generate_search_keywords(enhanced)
        
        # Add outcome statistics placeholder
        enhanced['outcome_stats'] = {
            'efficacy_rating': 4.2,
            'safety_rating': 4.5,
            'total_reviews': 156,
            'success_rate': 85.2
        }
        
        # Add PDF URL
        enhanced['pdf_url'] = f"/api/protocols/{enhanced['id']}/pdf"
        
        return enhanced
        
    def _generate_tags(self, protocol: Dict[str, Any]) -> List[str]:
        """Generate relevant tags for a protocol"""
        tags = []
        
        # Category-based tags
        category = protocol.get('category', '').lower()
        if 'weight' in category or 'metabolic' in category:
            tags.extend(['weight-loss', 'metabolism', 'fat-burning'])
        elif 'healing' in category or 'recovery' in category:
            tags.extend(['healing', 'recovery', 'regenerative'])
        elif 'cognitive' in category or 'brain' in category:
            tags.extend(['cognitive', 'nootropic', 'brain-health'])
        elif 'anti-aging' in category or 'longevity' in category:
            tags.extend(['anti-aging', 'longevity', 'hormone-optimization'])
            
        # Indication-based tags
        indications = protocol.get('clinical_indications', [])
        for indication in indications:
            indication_lower = indication.lower()
            if 'diabetes' in indication_lower or 'glucose' in indication_lower:
                tags.append('diabetes')
            if 'inflammation' in indication_lower:
                tags.append('anti-inflammatory')
            if 'joint' in indication_lower or 'arthritis' in indication_lower:
                tags.append('joint-health')
                
        return list(set(tags))
        
    def _generate_search_keywords(self, protocol: Dict[str, Any]) -> List[str]:
        """Generate comprehensive search keywords"""
        keywords = []
        
        # Basic info
        keywords.extend([
            protocol.get('name', '').lower(),
            *[alias.lower() for alias in protocol.get('aliases', [])]
        ])
        
        # Clinical indications
        keywords.extend([
            indication.lower() for indication in protocol.get('clinical_indications', [])
        ])
        
        # Mechanism keywords
        mechanism = protocol.get('mechanism_of_action', '').lower()
        keywords.extend(mechanism.split())
        
        # Category and tags
        keywords.append(protocol.get('category', '').lower())
        keywords.extend(protocol.get('tags', []))
        
        return list(set([kw for kw in keywords if len(kw) > 2]))
        
    def _generate_search_indices(self):
        """Generate search indices for fast lookup"""
        self.name_index = {}
        self.keyword_index = {}
        self.category_index = {}
        
        for protocol in self.all_protocols:
            protocol_id = protocol['id']
            
            # Name index
            self.name_index[protocol['name'].lower()] = protocol_id
            
            # Keyword index
            for keyword in protocol['search_keywords']:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(protocol_id)
                
            # Category index
            category = protocol.get('category', '')
            if category not in self.category_index:
                self.category_index[category] = []
            self.category_index[category].append(protocol_id)
            
    def search_protocols(self, 
                        query: Optional[str] = None,
                        category: Optional[str] = None,
                        tags: Optional[List[str]] = None,
                        limit: int = 50) -> List[Dict[str, Any]]:
        """Advanced protocol search with filters"""
        
        results = self.all_protocols.copy()
        
        # Text search
        if query:
            query = query.lower().strip()
            filtered_results = []
            
            for protocol in results:
                score = 0
                
                # Exact name match (highest score)
                if query in protocol['name'].lower():
                    score += 100
                    
                # Alias match
                for alias in protocol.get('aliases', []):
                    if query in alias.lower():
                        score += 80
                        
                # Keyword match
                for keyword in protocol['search_keywords']:
                    if query in keyword:
                        score += 50
                        
                # Clinical indication match
                for indication in protocol.get('clinical_indications', []):
                    if query in indication.lower():
                        score += 70
                        
                # Mechanism match
                if query in protocol.get('mechanism_of_action', '').lower():
                    score += 40
                    
                if score > 0:
                    protocol['search_score'] = score
                    filtered_results.append(protocol)
                    
            results = sorted(filtered_results, key=lambda x: x['search_score'], reverse=True)
            
        # Category filter
        if category and category != 'all':
            results = [p for p in results if p.get('category') == category]
            
        # Tags filter
        if tags:
            results = [p for p in results if any(tag in p.get('tags', []) for tag in tags)]
            
        return results[:limit]
        
    def get_protocol_by_id(self, protocol_id: str) -> Optional[Dict[str, Any]]:
        """Get single protocol by ID"""
        for protocol in self.all_protocols:
            if protocol['id'] == protocol_id:
                return protocol
        return None
        
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return sorted(list(self.categories))
        
    def get_all_tags(self) -> List[str]:
        """Get all available tags"""
        return sorted(list(self.tags))
        
    def get_stats(self) -> Dict[str, Any]:
        """Get library statistics"""
        return {
            'total_protocols': len(self.all_protocols),
            'categories': len(self.categories),
            'tags': len(self.tags),
            'most_popular_category': self._get_most_popular_category(),
            'average_rating': self._get_average_rating(),
            'last_updated': datetime.utcnow().isoformat()
        }
        
    def _get_most_popular_category(self) -> str:
        """Get the category with the most protocols"""
        category_counts = {}
        for protocol in self.all_protocols:
            category = protocol.get('category', 'Other')
            category_counts[category] = category_counts.get(category, 0) + 1
        return max(category_counts, key=category_counts.get) if category_counts else 'Other'
        
    def _get_average_rating(self) -> float:
        """Calculate average rating across all protocols"""
        ratings = [p.get('outcome_stats', {}).get('efficacy_rating', 4.0) for p in self.all_protocols]
        return sum(ratings) / len(ratings) if ratings else 4.0

# Global instance
master_protocol_manager = MasterProtocolManager()