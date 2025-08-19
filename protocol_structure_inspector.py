#!/usr/bin/env python3
"""
Protocol Structure Inspector
============================
Inspect the actual protocol structure being returned to understand the current implementation.
"""

import requests
import json
import sys

def inspect_protocol_structure():
    """Create a test protocol and inspect its structure"""
    base_url = "https://protocol-debug.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("🔍 PROTOCOL STRUCTURE INSPECTION")
    print("=" * 50)
    
    # Step 1: Create assessment
    print("Creating test assessment...")
    assessment_data = {
        "step": 1,
        "assessment_data": {
            "patient_name": "Sarah Johnson",
            "age": 35,
            "gender": "Female",
            "weight": 160,
            "primary_concerns": ["Weight loss", "Low energy", "Poor sleep"],
            "health_goals": ["Lose weight", "Increase energy"],
            "current_medications": [],
            "medical_history": [],
            "allergies": []
        }
    }
    
    try:
        response = requests.post(f"{api_url}/assessment/multi-step", json=assessment_data)
        if response.status_code != 200:
            print(f"❌ Assessment creation failed: {response.status_code}")
            return
        
        assessment_id = response.json().get("id")
        print(f"✅ Assessment created: {assessment_id}")
        
        # Step 2: Generate protocol
        print("Generating protocol...")
        response = requests.post(f"{api_url}/generate-functional-protocol/{assessment_id}")
        if response.status_code != 200:
            print(f"❌ Protocol generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        protocol_result = response.json()
        protocol_data = protocol_result.get("protocol", {})
        
        print(f"✅ Protocol generated successfully")
        print(f"Protocol ID: {protocol_result.get('protocol_id')}")
        
        # Step 3: Inspect structure
        print("\n📋 CURRENT PROTOCOL STRUCTURE:")
        print("=" * 50)
        
        def print_structure(data, indent=0):
            """Recursively print data structure"""
            prefix = "  " * indent
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        print(f"{prefix}{key}: ({type(value).__name__})")
                        if isinstance(value, dict) and len(value) > 0:
                            print_structure(value, indent + 1)
                        elif isinstance(value, list) and len(value) > 0:
                            print(f"{prefix}  [{len(value)} items]")
                            if len(value) > 0 and isinstance(value[0], dict):
                                print(f"{prefix}  Sample item structure:")
                                print_structure(value[0], indent + 2)
                    else:
                        value_preview = str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                        print(f"{prefix}{key}: {value_preview}")
            elif isinstance(data, list):
                print(f"{prefix}[{len(data)} items]")
                if len(data) > 0:
                    print_structure(data[0], indent + 1)
        
        print_structure(protocol_data)
        
        # Step 4: Check for uniform sections specifically
        print("\n🔍 UNIFORM SECTIONS CHECK:")
        print("=" * 50)
        
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
                print(f"✅ {section}: PRESENT")
                section_data = protocol_data[section]
                if isinstance(section_data, dict):
                    print(f"   Keys: {list(section_data.keys())}")
                else:
                    print(f"   Type: {type(section_data)}")
            else:
                print(f"❌ {section}: MISSING")
        
        # Step 5: Show what sections ARE present
        print(f"\n📊 ACTUAL SECTIONS PRESENT:")
        print("=" * 50)
        actual_sections = list(protocol_data.keys()) if isinstance(protocol_data, dict) else []
        for section in actual_sections:
            print(f"   • {section}")
        
        print(f"\nTotal sections: {len(actual_sections)}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    inspect_protocol_structure()