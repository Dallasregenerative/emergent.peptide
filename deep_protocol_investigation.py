#!/usr/bin/env python3
"""
Deep Protocol Investigation
===========================
This will show the actual protocol content to understand personalization issues
"""

import requests
import json
import sys

class DeepProtocolInvestigator:
    def __init__(self, base_url="https://peptide-wizard-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"

    def investigate_protocols(self):
        print("🔬 DEEP PROTOCOL INVESTIGATION")
        print("=" * 60)
        
        # Very different patients to maximize differences
        patient_a_data = {
            "patient_name": "Emma Wilson",
            "age": 25,
            "gender": "Female",
            "weight": 120,
            "height_feet": 5,
            "height_inches": 2,
            "primary_concerns": ["Weight loss", "Fat burning", "Metabolic enhancement"],
            "health_goals": ["Lose 30 pounds", "Reduce body fat", "Boost metabolism"],
            "current_medications": [],
            "medical_history": [],
            "allergies": []
        }
        
        patient_b_data = {
            "patient_name": "Marcus Thompson",
            "age": 65,
            "gender": "Male", 
            "weight": 220,
            "height_feet": 6,
            "height_inches": 1,
            "primary_concerns": ["Severe joint pain", "Arthritis", "Muscle recovery"],
            "health_goals": ["Eliminate joint pain", "Improve mobility", "Heal injuries"],
            "current_medications": ["Warfarin", "Atorvastatin", "Prednisone", "Insulin"],
            "medical_history": ["Diabetes Type 1", "Heart disease", "Rheumatoid arthritis", "Blood clots"],
            "allergies": ["Sulfa drugs", "Shellfish"]
        }
        
        # Create assessments and generate protocols
        print("Creating assessments...")
        
        # Patient A
        response_a = requests.post(
            f"{self.api_url}/assessment/multi-step",
            json={"step": 1, "assessment_data": patient_a_data}
        )
        assessment_a_id = response_a.json().get("id")
        
        # Patient B  
        response_b = requests.post(
            f"{self.api_url}/assessment/multi-step",
            json={"step": 1, "assessment_data": patient_b_data}
        )
        assessment_b_id = response_b.json().get("id")
        
        print("Generating protocols...")
        
        # Generate protocols
        protocol_a_response = requests.post(f"{self.api_url}/generate-functional-protocol/{assessment_a_id}")
        protocol_a = protocol_a_response.json().get("protocol", {})
        
        protocol_b_response = requests.post(f"{self.api_url}/generate-functional-protocol/{assessment_b_id}")
        protocol_b = protocol_b_response.json().get("protocol", {})
        
        print("\n" + "="*80)
        print("PATIENT A (25F, 120lbs, Weight Loss Focus)")
        print("="*80)
        
        print("\n🧬 PRIMARY PEPTIDES:")
        peptides_a = protocol_a.get("primary_peptides", [])
        for i, peptide in enumerate(peptides_a):
            print(f"  {i+1}. {peptide}")
        
        print("\n💊 DETAILED DOSING:")
        dosing_a = protocol_a.get("detailed_dosing_protocols", {})
        for key, value in dosing_a.items():
            print(f"  {key}: {str(value)[:200]}...")
        
        print("\n⚠️  SAFETY CONSIDERATIONS:")
        safety_a = protocol_a.get("safety_considerations", [])
        for i, safety in enumerate(safety_a):
            print(f"  {i+1}. {safety}")
        
        print("\n🧠 AI ANALYSIS:")
        analysis_a = protocol_a.get("ai_analysis", "")
        print(f"  {analysis_a}")
        
        print("\n📝 PRACTITIONER NOTES:")
        notes_a = protocol_a.get("practitioner_notes", "")
        print(f"  {notes_a}")
        
        print("\n" + "="*80)
        print("PATIENT B (65M, 220lbs, Joint Pain Focus, Multiple Medications)")
        print("="*80)
        
        print("\n🧬 PRIMARY PEPTIDES:")
        peptides_b = protocol_b.get("primary_peptides", [])
        for i, peptide in enumerate(peptides_b):
            print(f"  {i+1}. {peptide}")
        
        print("\n💊 DETAILED DOSING:")
        dosing_b = protocol_b.get("detailed_dosing_protocols", {})
        for key, value in dosing_b.items():
            print(f"  {key}: {str(value)[:200]}...")
        
        print("\n⚠️  SAFETY CONSIDERATIONS:")
        safety_b = protocol_b.get("safety_considerations", [])
        for i, safety in enumerate(safety_b):
            print(f"  {i+1}. {safety}")
        
        print("\n🧠 AI ANALYSIS:")
        analysis_b = protocol_b.get("ai_analysis", "")
        print(f"  {analysis_b}")
        
        print("\n📝 PRACTITIONER NOTES:")
        notes_b = protocol_b.get("practitioner_notes", "")
        print(f"  {notes_b}")
        
        print("\n" + "="*80)
        print("CRITICAL PERSONALIZATION ANALYSIS")
        print("="*80)
        
        # Check if protocols are identical
        identical_peptides = str(peptides_a) == str(peptides_b)
        identical_dosing = str(dosing_a) == str(dosing_b)
        identical_safety = str(safety_a) == str(safety_b)
        identical_analysis = analysis_a == analysis_b
        identical_notes = notes_a == notes_b
        
        print(f"\n❌ IDENTICAL PEPTIDES: {identical_peptides}")
        print(f"❌ IDENTICAL DOSING: {identical_dosing}")
        print(f"❌ IDENTICAL SAFETY: {identical_safety}")
        print(f"❌ IDENTICAL ANALYSIS: {identical_analysis}")
        print(f"❌ IDENTICAL NOTES: {identical_notes}")
        
        total_identical = sum([identical_peptides, identical_dosing, identical_safety, identical_analysis, identical_notes])
        
        print(f"\n🚨 CRITICAL FINDING: {total_identical}/5 protocol sections are IDENTICAL")
        
        if total_identical >= 4:
            print("❌ SEVERE PERSONALIZATION FAILURE - Protocols are essentially the same")
            return False
        elif total_identical >= 2:
            print("⚠️  MODERATE PERSONALIZATION ISSUES - Some sections are identical")
            return False
        else:
            print("✅ GOOD PERSONALIZATION - Protocols are sufficiently different")
            return True

if __name__ == "__main__":
    investigator = DeepProtocolInvestigator()
    success = investigator.investigate_protocols()
    sys.exit(0 if success else 1)