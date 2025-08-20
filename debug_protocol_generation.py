#!/usr/bin/env python3
"""
Test the actual protocol generation structure before Pydantic conversion
"""

import requests
import json

def test_protocol_generation_structure():
    base_url = "https://peptideai-debug.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    # Create assessment
    assessment_data = {
        "step": 1,
        "assessment_data": {
            "patient_name": "Sarah Johnson",
            "age": 35,
            "gender": "Female",
            "weight": 160,
            "height_feet": 5,
            "height_inches": 6,
            "email": "sarah.johnson@example.com",
            "primary_concerns": ["Weight loss resistance", "Metabolic dysfunction"],
            "health_goals": ["Sustainable weight loss", "Improved metabolic health"],
            "current_medications": ["Metformin 500mg twice daily"],
            "medical_history": ["Type 2 diabetes (pre-diabetic)", "Hypothyroidism"],
            "allergies": ["Sulfa drugs"],
            "lifestyle_factors": {
                "exercise_frequency": "2-3 times per week",
                "diet_type": "Low carb attempted"
            }
        }
    }
    
    print("Creating assessment...")
    response = requests.post(f"{api_url}/assessment/multi-step", json=assessment_data)
    
    if response.status_code == 200:
        assessment_result = response.json()
        assessment_id = assessment_result.get("id")
        print(f"Assessment created: {assessment_id}")
        
        # Generate protocol and examine the raw response
        print("Generating protocol...")
        protocol_response = requests.post(f"{api_url}/generate-functional-protocol/{assessment_id}")
        
        if protocol_response.status_code == 200:
            protocol_result = protocol_response.json()
            
            # Save the full response to a file for detailed analysis
            with open('/app/protocol_response_debug.json', 'w') as f:
                json.dump(protocol_result, f, indent=2, default=str)
            
            print("Protocol response saved to protocol_response_debug.json")
            
            # Check if the enhanced structure exists anywhere in the response
            protocol_data = protocol_result.get("protocol", {})
            
            print("\nChecking for enhanced structure in protocol data...")
            
            # Look for any keys that might contain the enhanced structure
            for key, value in protocol_data.items():
                if isinstance(value, dict):
                    print(f"\nChecking dict key '{key}' with {len(value)} items:")
                    for subkey in value.keys():
                        print(f"  - {subkey}")
                        
                        # Check if this might be our enhanced structure
                        if any(section in subkey for section in ["mechanism", "dosing", "stacking", "contraindication", "monitoring", "evidence", "outcome"]):
                            print(f"    *** POTENTIAL ENHANCED SECTION: {subkey} ***")
            
            # Also check the top-level response for any other data
            print(f"\nTop-level response keys: {list(protocol_result.keys())}")
            
            return True
        else:
            print(f"Protocol generation failed: {protocol_response.status_code}")
            print(protocol_response.text)
            return False
    else:
        print(f"Assessment creation failed: {response.status_code}")
        return False

if __name__ == "__main__":
    test_protocol_generation_structure()