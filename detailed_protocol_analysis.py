#!/usr/bin/env python3
"""
Detailed Protocol Analysis
==========================
This script will generate protocols and show detailed comparison
"""

import requests
import json
import sys
from datetime import datetime

class DetailedProtocolAnalyzer:
    def __init__(self, base_url="https://peptide-protocols-4.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"

    def create_and_analyze_protocols(self):
        print("🔍 DETAILED PROTOCOL ANALYSIS")
        print("=" * 50)
        
        # Patient A: Young female, weight loss focus
        patient_a_data = {
            "patient_name": "Sarah Johnson",
            "age": 28,
            "gender": "Female",
            "weight": 145,
            "height_feet": 5,
            "height_inches": 4,
            "primary_concerns": ["Weight loss", "Low energy", "Metabolic optimization"],
            "health_goals": ["Lose 20 pounds", "Increase energy levels", "Improve metabolism"],
            "current_medications": [],
            "medical_history": [],
            "allergies": []
        }
        
        # Patient B: Older male, joint pain focus
        patient_b_data = {
            "patient_name": "Robert Chen",
            "age": 52,
            "gender": "Male", 
            "weight": 185,
            "height_feet": 5,
            "height_inches": 10,
            "primary_concerns": ["Joint pain", "Recovery from injury", "Inflammation"],
            "health_goals": ["Reduce joint pain", "Improve recovery time", "Increase mobility"],
            "current_medications": ["Lisinopril", "Metformin", "Ibuprofen"],
            "medical_history": ["Hypertension", "Type 2 Diabetes", "Previous knee injury"],
            "allergies": ["Penicillin"]
        }
        
        # Create assessments
        print("\n1. Creating Patient A Assessment...")
        response_a = requests.post(
            f"{self.api_url}/assessment/multi-step",
            json={"step": 1, "assessment_data": patient_a_data}
        )
        
        if response_a.status_code != 200:
            print(f"❌ Failed to create Patient A assessment: {response_a.status_code}")
            return
            
        assessment_a_id = response_a.json().get("id")
        print(f"✅ Patient A Assessment ID: {assessment_a_id}")
        
        print("\n2. Creating Patient B Assessment...")
        response_b = requests.post(
            f"{self.api_url}/assessment/multi-step",
            json={"step": 1, "assessment_data": patient_b_data}
        )
        
        if response_b.status_code != 200:
            print(f"❌ Failed to create Patient B assessment: {response_b.status_code}")
            return
            
        assessment_b_id = response_b.json().get("id")
        print(f"✅ Patient B Assessment ID: {assessment_b_id}")
        
        # Generate protocols
        print("\n3. Generating Protocol for Patient A...")
        protocol_a_response = requests.post(f"{self.api_url}/generate-functional-protocol/{assessment_a_id}")
        
        if protocol_a_response.status_code != 200:
            print(f"❌ Failed to generate Patient A protocol: {protocol_a_response.status_code}")
            print(f"Response: {protocol_a_response.text}")
            return
            
        protocol_a = protocol_a_response.json().get("protocol", {})
        print(f"✅ Patient A Protocol Generated")
        
        print("\n4. Generating Protocol for Patient B...")
        protocol_b_response = requests.post(f"{self.api_url}/generate-functional-protocol/{assessment_b_id}")
        
        if protocol_b_response.status_code != 200:
            print(f"❌ Failed to generate Patient B protocol: {protocol_b_response.status_code}")
            print(f"Response: {protocol_b_response.text}")
            return
            
        protocol_b = protocol_b_response.json().get("protocol", {})
        print(f"✅ Patient B Protocol Generated")
        
        # Detailed Analysis
        print("\n" + "="*60)
        print("DETAILED PROTOCOL COMPARISON")
        print("="*60)
        
        # Primary Peptides Comparison
        print("\n🧬 PRIMARY PEPTIDES COMPARISON:")
        peptides_a = protocol_a.get("primary_peptides", [])
        peptides_b = protocol_b.get("primary_peptides", [])
        
        print(f"Patient A (Weight Loss Focus): {len(peptides_a)} peptides")
        for i, peptide in enumerate(peptides_a[:3]):  # Show first 3
            if isinstance(peptide, dict):
                print(f"  {i+1}. {peptide.get('name', 'Unknown')}")
            else:
                print(f"  {i+1}. {peptide}")
        
        print(f"\nPatient B (Joint Pain Focus): {len(peptides_b)} peptides")
        for i, peptide in enumerate(peptides_b[:3]):  # Show first 3
            if isinstance(peptide, dict):
                print(f"  {i+1}. {peptide.get('name', 'Unknown')}")
            else:
                print(f"  {i+1}. {peptide}")
        
        # Dosing Protocols Comparison
        print("\n💊 DOSING PROTOCOLS COMPARISON:")
        dosing_a = protocol_a.get("detailed_dosing_protocols", {})
        dosing_b = protocol_b.get("detailed_dosing_protocols", {})
        
        print(f"Patient A Dosing Keys: {list(dosing_a.keys())}")
        print(f"Patient B Dosing Keys: {list(dosing_b.keys())}")
        
        # Check for weight-based calculations
        dosing_a_str = str(dosing_a)
        dosing_b_str = str(dosing_b)
        
        weight_mentions_a = dosing_a_str.count("145") + dosing_a_str.count("weight")
        weight_mentions_b = dosing_b_str.count("185") + dosing_b_str.count("weight")
        
        print(f"Patient A weight mentions in dosing: {weight_mentions_a}")
        print(f"Patient B weight mentions in dosing: {weight_mentions_b}")
        
        # Safety Considerations
        print("\n⚠️  SAFETY CONSIDERATIONS COMPARISON:")
        safety_a = protocol_a.get("safety_considerations", [])
        safety_b = protocol_b.get("safety_considerations", [])
        
        print(f"Patient A Safety Items: {len(safety_a)}")
        print(f"Patient B Safety Items: {len(safety_b)}")
        
        # Check for medication-specific safety considerations
        safety_a_str = str(safety_a).lower()
        safety_b_str = str(safety_b).lower()
        
        medication_mentions_b = safety_b_str.count("lisinopril") + safety_b_str.count("metformin") + safety_b_str.count("diabetes")
        print(f"Patient B medication-specific safety mentions: {medication_mentions_b}")
        
        # Clinical Reasoning
        print("\n🧠 CLINICAL REASONING COMPARISON:")
        reasoning_a = protocol_a.get("ai_analysis", "")
        reasoning_b = protocol_b.get("ai_analysis", "")
        
        print(f"Patient A reasoning length: {len(reasoning_a)} characters")
        print(f"Patient B reasoning length: {len(reasoning_b)} characters")
        
        # Check for concern-specific keywords
        reasoning_a_lower = reasoning_a.lower()
        reasoning_b_lower = reasoning_b.lower()
        
        weight_keywords_a = sum(1 for kw in ["weight", "fat", "metabolism", "energy"] if kw in reasoning_a_lower)
        joint_keywords_b = sum(1 for kw in ["joint", "pain", "inflammation", "recovery"] if kw in reasoning_b_lower)
        
        print(f"Patient A weight-related keywords: {weight_keywords_a}")
        print(f"Patient B joint-related keywords: {joint_keywords_b}")
        
        # Overall Assessment
        print("\n" + "="*60)
        print("PERSONALIZATION ASSESSMENT")
        print("="*60)
        
        personalization_indicators = 0
        total_indicators = 6
        
        # 1. Different primary peptides
        if str(peptides_a) != str(peptides_b):
            personalization_indicators += 1
            print("✅ Different primary peptides detected")
        else:
            print("❌ Same primary peptides")
        
        # 2. Weight-based dosing
        if weight_mentions_a > 0 or weight_mentions_b > 0:
            personalization_indicators += 1
            print("✅ Weight-based dosing detected")
        else:
            print("❌ No weight-based dosing detected")
        
        # 3. Different safety considerations
        if str(safety_a) != str(safety_b):
            personalization_indicators += 1
            print("✅ Different safety considerations")
        else:
            print("❌ Same safety considerations")
        
        # 4. Medication-specific safety for Patient B
        if medication_mentions_b > 0:
            personalization_indicators += 1
            print("✅ Medication-specific safety considerations for Patient B")
        else:
            print("❌ No medication-specific safety considerations")
        
        # 5. Concern-specific reasoning
        if weight_keywords_a >= 2 and joint_keywords_b >= 2:
            personalization_indicators += 1
            print("✅ Concern-specific clinical reasoning")
        else:
            print("❌ Generic clinical reasoning")
        
        # 6. Different clinical reasoning
        if reasoning_a != reasoning_b and len(reasoning_a) > 100 and len(reasoning_b) > 100:
            personalization_indicators += 1
            print("✅ Different clinical reasoning content")
        else:
            print("❌ Similar or minimal clinical reasoning")
        
        personalization_score = (personalization_indicators / total_indicators) * 100
        
        print(f"\n🎯 FINAL PERSONALIZATION SCORE: {personalization_score:.1f}%")
        print(f"   ({personalization_indicators}/{total_indicators} indicators met)")
        
        if personalization_score >= 70:
            print("✅ EXCELLENT personalization - protocols are truly customized")
        elif personalization_score >= 50:
            print("⚠️  GOOD personalization - some customization present")
        else:
            print("❌ POOR personalization - protocols appear generic")
        
        return personalization_score >= 50

if __name__ == "__main__":
    analyzer = DetailedProtocolAnalyzer()
    success = analyzer.create_and_analyze_protocols()
    sys.exit(0 if success else 1)