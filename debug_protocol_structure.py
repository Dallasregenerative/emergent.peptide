#!/usr/bin/env python3
"""
Debug Protocol Structure - Examine what's actually being returned
"""

import requests
import json

def debug_protocol_structure():
    base_url = "https://peptide-wizard-3.preview.emergentagent.com"
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
        
        # Generate protocol
        print("Generating protocol...")
        protocol_response = requests.post(f"{api_url}/generate-functional-protocol/{assessment_id}")
        
        if protocol_response.status_code == 200:
            protocol_result = protocol_response.json()
            protocol_data = protocol_result.get("protocol")
            
            print("\n" + "="*80)
            print("PROTOCOL DATA STRUCTURE:")
            print("="*80)
            
            if protocol_data:
                # Print top-level keys
                print("TOP-LEVEL KEYS:")
                for key in sorted(protocol_data.keys()):
                    value = protocol_data[key]
                    value_type = type(value).__name__
                    if isinstance(value, (dict, list)):
                        size = len(value)
                        print(f"  {key}: {value_type} (size: {size})")
                    else:
                        print(f"  {key}: {value_type}")
                
                # Look for uniform sections specifically
                print("\nUNIFORM SECTIONS CHECK:")
                uniform_sections = [
                    "mechanism_of_action",
                    "detailed_dosing_protocols", 
                    "stacking_combinations",
                    "comprehensive_contraindications",
                    "monitoring_requirements",
                    "evidence_based_support",
                    "outcome_statistics"
                ]
                
                for section in uniform_sections:
                    if section in protocol_data:
                        print(f"  ✅ {section}: FOUND")
                        # Show structure
                        section_data = protocol_data[section]
                        if isinstance(section_data, dict):
                            print(f"     Keys: {list(section_data.keys())}")
                        elif isinstance(section_data, list):
                            print(f"     List length: {len(section_data)}")
                    else:
                        print(f"  ❌ {section}: MISSING")
                
                # Show sample of actual data
                print("\nSAMPLE DATA:")
                for key, value in list(protocol_data.items())[:3]:
                    print(f"\n{key}:")
                    if isinstance(value, dict):
                        for subkey, subvalue in list(value.items())[:3]:
                            print(f"  {subkey}: {str(subvalue)[:100]}...")
                    elif isinstance(value, list):
                        print(f"  List with {len(value)} items")
                        if value:
                            print(f"  First item: {str(value[0])[:100]}...")
                    else:
                        print(f"  {str(value)[:200]}...")
                        
            else:
                print("No protocol data found!")
                
        else:
            print(f"Protocol generation failed: {protocol_response.status_code}")
            print(protocol_response.text)
    else:
        print(f"Assessment creation failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    debug_protocol_structure()