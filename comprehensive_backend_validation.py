#!/usr/bin/env python3
"""
COMPREHENSIVE BACKEND VALIDATION FOR PHASE 3
============================================

This test validates all backend systems for the Phase 3 final validation,
focusing on the working systems and documenting the specific issues found.
"""

import requests
import json
import sys
from datetime import datetime

class ComprehensiveBackendValidator:
    def __init__(self, base_url="https://medprotocol-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.results = {}
        
    def test_enhanced_dr_peptide_ai(self):
        """Test Enhanced Dr. Peptide AI System"""
        print("🧠 Testing Enhanced Dr. Peptide AI System...")
        
        test_query = {
            "message": "What peptides would you recommend for a 45-year-old with chronic fatigue, cognitive decline, and metabolic issues? Please include specific dosing and safety considerations.",
            "conversation_history": []
        }
        
        try:
            response = requests.post(f"{self.api_url}/dr-peptide/chat", json=test_query)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    ai_response = data.get("response", "")
                    response_length = len(ai_response)
                    
                    # Check for clinical database integration
                    clinical_keywords = ["BPC-157", "CJC-1295", "Selank", "dosing", "safety", "monitoring"]
                    keywords_found = sum(1 for keyword in clinical_keywords if keyword.lower() in ai_response.lower())
                    
                    print(f"   ✅ Dr. Peptide AI working: {response_length} chars, {keywords_found}/6 clinical keywords")
                    self.results["dr_peptide_ai"] = {
                        "status": "working",
                        "response_length": response_length,
                        "clinical_integration": f"{keywords_found}/6"
                    }
                    return True
                else:
                    print(f"   ❌ Dr. Peptide AI failed: {data.get('error')}")
                    self.results["dr_peptide_ai"] = {"status": "failed", "error": data.get('error')}
                    return False
            else:
                print(f"   ❌ Dr. Peptide AI API error: {response.status_code}")
                self.results["dr_peptide_ai"] = {"status": "api_error", "status_code": response.status_code}
                return False
        except Exception as e:
            print(f"   ❌ Dr. Peptide AI exception: {e}")
            self.results["dr_peptide_ai"] = {"status": "exception", "error": str(e)}
            return False
    
    def test_enhanced_protocol_library(self):
        """Test Enhanced Protocol Library"""
        print("📚 Testing Enhanced Protocol Library...")
        
        try:
            response = requests.get(f"{self.api_url}/enhanced-library")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    protocol_count = len(data)
                    
                    # Check for expected protocols
                    protocol_names = [item.get("name", "") for item in data]
                    expected_protocols = ["BPC-157", "TB-500", "CJC-1295", "Selank"]
                    found_protocols = sum(1 for protocol in expected_protocols if protocol in protocol_names)
                    
                    print(f"   ✅ Enhanced Library working: {protocol_count} protocols, {found_protocols}/4 expected found")
                    self.results["enhanced_library"] = {
                        "status": "working",
                        "protocol_count": protocol_count,
                        "expected_protocols": f"{found_protocols}/4"
                    }
                    return True
                else:
                    print(f"   ❌ Enhanced Library wrong format: {type(data)}")
                    self.results["enhanced_library"] = {"status": "wrong_format", "type": str(type(data))}
                    return False
            else:
                print(f"   ❌ Enhanced Library API error: {response.status_code}")
                self.results["enhanced_library"] = {"status": "api_error", "status_code": response.status_code}
                return False
        except Exception as e:
            print(f"   ❌ Enhanced Library exception: {e}")
            self.results["enhanced_library"] = {"status": "exception", "error": str(e)}
            return False
    
    def test_comprehensive_peptides_database(self):
        """Test Comprehensive Peptides Database (60+ entries)"""
        print("🗄️  Testing Comprehensive Peptides Database...")
        
        try:
            response = requests.get(f"{self.api_url}/peptides")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    peptide_count = len(data)
                    
                    # Check for functional medicine compounds
                    peptide_names = [item.get("name", "") for item in data]
                    fm_compounds = ["NAD+", "Glutathione", "Berberine", "Curcumin"]
                    found_compounds = sum(1 for compound in fm_compounds if any(compound in name for name in peptide_names))
                    
                    print(f"   ✅ Comprehensive Database working: {peptide_count} entries, {found_compounds}/4 FM compounds")
                    self.results["comprehensive_database"] = {
                        "status": "working",
                        "peptide_count": peptide_count,
                        "fm_compounds": f"{found_compounds}/4"
                    }
                    return True
                else:
                    print(f"   ❌ Comprehensive Database wrong format: {type(data)}")
                    self.results["comprehensive_database"] = {"status": "wrong_format", "type": str(type(data))}
                    return False
            else:
                print(f"   ❌ Comprehensive Database API error: {response.status_code}")
                self.results["comprehensive_database"] = {"status": "api_error", "status_code": response.status_code}
                return False
        except Exception as e:
            print(f"   ❌ Comprehensive Database exception: {e}")
            self.results["comprehensive_database"] = {"status": "exception", "error": str(e)}
            return False
    
    def test_assessment_system(self):
        """Test Multi-Step Assessment System"""
        print("📋 Testing Multi-Step Assessment System...")
        
        test_assessment = {
            "step": 1,
            "data": {
                "patient_name": "Test Patient",
                "age": 35,
                "gender": "Female",
                "primary_concerns": ["Fatigue", "Stress"],
                "health_goals": ["Better energy", "Stress management"],
                "current_medications": [],
                "medical_history": [],
                "allergies": []
            }
        }
        
        try:
            response = requests.post(f"{self.api_url}/assessment/multi-step", json=test_assessment)
            if response.status_code == 200:
                data = response.json()
                assessment_id = data.get("id")
                if assessment_id:
                    print(f"   ✅ Assessment System working: Created ID {assessment_id}")
                    self.results["assessment_system"] = {
                        "status": "working",
                        "assessment_id": assessment_id
                    }
                    return True
                else:
                    print(f"   ❌ Assessment System no ID returned")
                    self.results["assessment_system"] = {"status": "no_id", "response": data}
                    return False
            else:
                print(f"   ❌ Assessment System API error: {response.status_code}")
                self.results["assessment_system"] = {"status": "api_error", "status_code": response.status_code}
                return False
        except Exception as e:
            print(f"   ❌ Assessment System exception: {e}")
            self.results["assessment_system"] = {"status": "exception", "error": str(e)}
            return False
    
    def test_protocol_generation(self):
        """Test Protocol Generation System (Known Issue)"""
        print("💊 Testing Protocol Generation System...")
        
        # First create an assessment
        test_assessment = {
            "step": 1,
            "data": {
                "patient_name": "Protocol Test Patient",
                "age": 40,
                "gender": "Male",
                "primary_concerns": ["Energy"],
                "health_goals": ["Better energy"],
                "current_medications": [],
                "medical_history": [],
                "allergies": []
            }
        }
        
        try:
            # Create assessment
            response1 = requests.post(f"{self.api_url}/assessment/multi-step", json=test_assessment)
            if response1.status_code != 200:
                print(f"   ❌ Protocol Generation: Assessment creation failed")
                self.results["protocol_generation"] = {"status": "assessment_failed"}
                return False
            
            assessment_id = response1.json().get("id")
            
            # Try protocol generation
            response2 = requests.post(f"{self.api_url}/generate-functional-protocol/{assessment_id}")
            if response2.status_code == 200:
                data = response2.json()
                protocol_id = data.get("protocol_id")
                print(f"   ✅ Protocol Generation working: Created protocol {protocol_id}")
                self.results["protocol_generation"] = {
                    "status": "working",
                    "protocol_id": protocol_id
                }
                return True
            else:
                error_data = response2.json()
                error_detail = error_data.get("detail", "")
                
                # Analyze specific errors
                if "safety_considerations" in error_detail and "list_type" in error_detail:
                    print(f"   ❌ Protocol Generation: KNOWN BUG - safety_considerations validation error")
                    print(f"      Issue: Expected List[str] but got Dict")
                    self.results["protocol_generation"] = {
                        "status": "validation_error",
                        "issue": "safety_considerations should be List[str] not Dict",
                        "error": error_detail
                    }
                elif "practitioner_notes" in error_detail:
                    print(f"   ❌ Protocol Generation: KNOWN BUG - practitioner_notes missing")
                    self.results["protocol_generation"] = {
                        "status": "validation_error", 
                        "issue": "practitioner_notes field missing",
                        "error": error_detail
                    }
                else:
                    print(f"   ❌ Protocol Generation: Other error - {error_detail}")
                    self.results["protocol_generation"] = {
                        "status": "other_error",
                        "error": error_detail
                    }
                return False
        except Exception as e:
            print(f"   ❌ Protocol Generation exception: {e}")
            self.results["protocol_generation"] = {"status": "exception", "error": str(e)}
            return False
    
    def test_collective_intelligence_system(self):
        """Test Collective Intelligence System"""
        print("🤝 Testing Collective Intelligence System...")
        
        try:
            response = requests.get(f"{self.api_url}/collective-intelligence/insights")
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    insights = data.get("insights", {})
                    print(f"   ✅ Collective Intelligence working: {len(insights)} insight categories")
                    self.results["collective_intelligence"] = {
                        "status": "working",
                        "insight_categories": len(insights)
                    }
                    return True
                else:
                    print(f"   ❌ Collective Intelligence failed: {data}")
                    self.results["collective_intelligence"] = {"status": "failed", "response": data}
                    return False
            else:
                print(f"   ❌ Collective Intelligence API error: {response.status_code}")
                self.results["collective_intelligence"] = {"status": "api_error", "status_code": response.status_code}
                return False
        except Exception as e:
            print(f"   ❌ Collective Intelligence exception: {e}")
            self.results["collective_intelligence"] = {"status": "exception", "error": str(e)}
            return False
    
    def test_email_integration(self):
        """Test Email Integration System"""
        print("📧 Testing Email Integration System...")
        
        try:
            response = requests.get(f"{self.api_url}/email/status")
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", {})
                configured = status.get("configured", False)
                service_available = status.get("service_available", False)
                
                if configured and service_available:
                    print(f"   ✅ Email Integration fully working")
                    self.results["email_integration"] = {"status": "working"}
                    return True
                else:
                    print(f"   ⚠️  Email Integration not configured (expected)")
                    print(f"      Configured: {configured}, Available: {service_available}")
                    self.results["email_integration"] = {
                        "status": "not_configured",
                        "configured": configured,
                        "service_available": service_available,
                        "note": "Mail password not configured - expected"
                    }
                    return False
            else:
                print(f"   ❌ Email Integration API error: {response.status_code}")
                self.results["email_integration"] = {"status": "api_error", "status_code": response.status_code}
                return False
        except Exception as e:
            print(f"   ❌ Email Integration exception: {e}")
            self.results["email_integration"] = {"status": "exception", "error": str(e)}
            return False
    
    def test_progress_tracking(self):
        """Test Progress Tracking System"""
        print("📈 Testing Progress Tracking System...")
        
        test_data = {
            "patient_id": "test-patient-123",
            "protocol_id": "test-protocol-456",
            "progress_data": {"week": 1, "status": "improving"}
        }
        
        try:
            response = requests.post(f"{self.api_url}/progress/track", json=test_data)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"   ✅ Progress Tracking working")
                    self.results["progress_tracking"] = {"status": "working"}
                    return True
                else:
                    print(f"   ❌ Progress Tracking failed: {data}")
                    self.results["progress_tracking"] = {"status": "failed", "response": data}
                    return False
            else:
                error_data = response.json()
                error_detail = error_data.get("detail", "")
                
                if "has no attribute" in error_detail:
                    print(f"   ❌ Progress Tracking: KNOWN BUG - Missing methods")
                    print(f"      Issue: ProgressTrackingService missing track_progress method")
                    self.results["progress_tracking"] = {
                        "status": "missing_methods",
                        "issue": "ProgressTrackingService object has no attribute 'track_progress'",
                        "error": error_detail
                    }
                else:
                    print(f"   ❌ Progress Tracking other error: {error_detail}")
                    self.results["progress_tracking"] = {"status": "other_error", "error": error_detail}
                return False
        except Exception as e:
            print(f"   ❌ Progress Tracking exception: {e}")
            self.results["progress_tracking"] = {"status": "exception", "error": str(e)}
            return False
    
    def run_comprehensive_validation(self):
        """Run all backend validation tests"""
        print("🚀 COMPREHENSIVE BACKEND VALIDATION FOR PHASE 3")
        print("="*60)
        
        tests = [
            ("Enhanced Dr. Peptide AI", self.test_enhanced_dr_peptide_ai),
            ("Enhanced Protocol Library", self.test_enhanced_protocol_library),
            ("Comprehensive Peptides Database", self.test_comprehensive_peptides_database),
            ("Assessment System", self.test_assessment_system),
            ("Protocol Generation", self.test_protocol_generation),
            ("Collective Intelligence", self.test_collective_intelligence_system),
            ("Email Integration", self.test_email_integration),
            ("Progress Tracking", self.test_progress_tracking)
        ]
        
        working_systems = 0
        total_systems = len(tests)
        
        for test_name, test_func in tests:
            if test_func():
                working_systems += 1
        
        print(f"\n📊 COMPREHENSIVE VALIDATION RESULTS")
        print("="*60)
        print(f"Working Systems: {working_systems}/{total_systems}")
        print(f"Success Rate: {(working_systems/total_systems)*100:.1f}%")
        
        print(f"\n✅ WORKING SYSTEMS:")
        for system, result in self.results.items():
            if result.get("status") == "working":
                print(f"   ✅ {system.replace('_', ' ').title()}")
        
        print(f"\n❌ SYSTEMS WITH ISSUES:")
        for system, result in self.results.items():
            if result.get("status") != "working":
                status = result.get("status", "unknown")
                issue = result.get("issue", result.get("error", ""))
                print(f"   ❌ {system.replace('_', ' ').title()}: {status}")
                if issue:
                    print(f"      Issue: {issue}")
        
        return self.results

if __name__ == "__main__":
    validator = ComprehensiveBackendValidator()
    results = validator.run_comprehensive_validation()
    
    # Print JSON results for parsing
    print(f"\n📋 DETAILED RESULTS (JSON):")
    print(json.dumps(results, indent=2))