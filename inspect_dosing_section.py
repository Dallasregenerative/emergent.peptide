#!/usr/bin/env python3
"""
Inspect Dosing Section
======================
Check what's actually in the personalized dosing section.
"""

import requests
import json

def inspect_dosing():
    base_url = "https://peptide-protocols-4.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    # Create assessment
    assessment_data = {
        "step": 1,
        "assessment_data": {
            "patient_name": "Sarah Johnson",
            "age": 35,
            "gender": "Female",
            "weight": 160,
            "primary_concerns": ["Weight loss"],
            "health_goals": ["Lose weight"],
            "current_medications": [],
            "medical_history": [],
            "allergies": []
        }
    }
    
    # Create assessment
    response = requests.post(f"{api_url}/assessment/multi-step", json=assessment_data)
    assessment_id = response.json().get("id")
    
    # Generate protocol
    response = requests.post(f"{api_url}/generate-functional-protocol/{assessment_id}")
    protocol = response.json().get("protocol", {})
    
    # Inspect dosing section
    dosing_section = protocol.get("detailed_dosing_protocols", {})
    print("DETAILED DOSING PROTOCOLS SECTION:")
    print("=" * 50)
    print(json.dumps(dosing_section, indent=2))
    
    # Also check primary peptides for dosing info
    primary_peptides = protocol.get("primary_peptides", [])
    print("\nPRIMARY PEPTIDES SECTION:")
    print("=" * 50)
    print(json.dumps(primary_peptides, indent=2))

if __name__ == "__main__":
    inspect_dosing()