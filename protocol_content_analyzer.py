#!/usr/bin/env python3
"""
Detailed Protocol Content Analysis
"""

import requests
import json
from datetime import datetime

def analyze_protocol_content():
    """Analyze the actual protocol content in detail"""
    
    # Use the production URL
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                backend_url = line.split('=')[1].strip()
                break
    
    api_url = f"{backend_url}/api"
    
    print("🔍 DETAILED PROTOCOL CONTENT ANALYSIS")
    print("="*60)
    
    # Create a test assessment
    patient_data = {
        "step": 1,
        "assessment_data": {
            "patient_name": "Test Patient",
            "age": 35,
            "gender": "Female",
            "weight": 160,
            "height_feet": 5,
            "height_inches": 6,
            "email": "test@email.com",
            "primary_concerns": ["Weight management", "Low energy"],
            "health_goals": ["Lose weight", "Increase energy"],
            "current_medications": [],
            "medical_history": [],
            "allergies": [],
            "lifestyle_factors": {
                "exercise_frequency": "3 times per week",
                "sleep_hours": "7 hours",
                "stress_level": "Moderate"
            }
        }
    }
    
    # Create assessment
    response = requests.post(f"{api_url}/assessment/multi-step", json=patient_data, timeout=30)
    if response.status_code != 200:
        print(f"❌ Failed to create assessment: {response.status_code}")
        return
    
    assessment_id = response.json().get('id')
    print(f"✅ Created assessment: {assessment_id}")
    
    # Generate protocol
    print("\n🧬 Generating protocol...")
    response = requests.post(f"{api_url}/generate-functional-protocol/{assessment_id}", timeout=120)
    
    if response.status_code != 200:
        print(f"❌ Failed to generate protocol: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    data = response.json()
    protocol = data.get('protocol', {})
    
    print(f"✅ Generated protocol: {data.get('protocol_id')}")
    
    # Analyze protocol structure
    print(f"\n📋 PROTOCOL STRUCTURE ANALYSIS:")
    print(f"-" * 40)
    
    # Check main sections
    sections = [
        'primary_peptides',
        'functional_medicine_analysis', 
        'safety_considerations',
        'practitioner_notes',
        'cost_analysis',
        'scientific_support',
        'expected_outcomes'
    ]
    
    for section in sections:
        value = protocol.get(section)
        if value:
            if isinstance(value, list):
                print(f"✅ {section}: {len(value)} items")
                if section == 'primary_peptides' and len(value) > 0:
                    print(f"   First peptide: {value[0] if value else 'None'}")
            elif isinstance(value, dict):
                print(f"✅ {section}: {len(value)} keys")
                if len(value) > 0:
                    print(f"   Keys: {list(value.keys())[:3]}...")
            elif isinstance(value, str):
                print(f"✅ {section}: {len(value)} characters")
                if len(value) > 100:
                    print(f"   Preview: {value[:100]}...")
            else:
                print(f"✅ {section}: {type(value)} - {value}")
        else:
            print(f"❌ {section}: Missing or empty")
    
    # Detailed analysis of primary peptides
    primary_peptides = protocol.get('primary_peptides', [])
    if primary_peptides:
        print(f"\n💊 PRIMARY PEPTIDES DETAILED ANALYSIS:")
        print(f"-" * 45)
        
        for i, peptide in enumerate(primary_peptides, 1):
            print(f"\nPeptide {i}:")
            if isinstance(peptide, dict):
                for key, value in peptide.items():
                    if isinstance(value, str) and len(value) > 100:
                        print(f"  {key}: {value[:100]}...")
                    else:
                        print(f"  {key}: {value}")
            else:
                print(f"  Raw data: {peptide}")
    
    # Safety considerations analysis
    safety = protocol.get('safety_considerations', [])
    if safety:
        print(f"\n⚠️  SAFETY CONSIDERATIONS:")
        print(f"-" * 30)
        for i, item in enumerate(safety[:5], 1):  # Show first 5
            print(f"{i}. {item}")
        if len(safety) > 5:
            print(f"... and {len(safety) - 5} more items")
    
    # Clinical reasoning analysis
    clinical_reasoning = protocol.get('practitioner_notes', '') or protocol.get('ai_analysis', '')
    if clinical_reasoning:
        print(f"\n🧠 CLINICAL REASONING:")
        print(f"-" * 25)
        print(f"Length: {len(clinical_reasoning)} characters")
        print(f"Content: {clinical_reasoning[:300]}...")
    
    # Full protocol JSON (truncated)
    print(f"\n📄 FULL PROTOCOL STRUCTURE (First 1000 chars):")
    print(f"-" * 50)
    protocol_json = json.dumps(protocol, indent=2)
    print(protocol_json[:1000] + "..." if len(protocol_json) > 1000 else protocol_json)

if __name__ == "__main__":
    analyze_protocol_content()