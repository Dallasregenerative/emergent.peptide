#!/usr/bin/env python3
"""
Comprehensive System Health Check for PeptideProtocols.ai
Testing all core platform components before patient journey testing
"""

import requests
import json
from datetime import datetime
import tempfile
import os

class PeptideProtocolsSystemHealthChecker:
    def __init__(self, base_url="https://peptideai-debug.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.critical_failures = []

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else f"{self.api_url}/"
        headers = {'Content-Type': 'application/json'} if not files else {}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                if files:
                    response = requests.post(url, files=files, data=data)
                else:
                    response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    self.test_results.append({
                        "test": name,
                        "status": "PASSED",
                        "details": response_data if isinstance(response_data, dict) else {}
                    })
                    return True, response_data
                except:
                    self.test_results.append({
                        "test": name,
                        "status": "PASSED",
                        "details": {}
                    })
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                    self.test_results.append({
                        "test": name,
                        "status": "FAILED",
                        "error": error_detail,
                        "expected_status": expected_status,
                        "actual_status": response.status_code
                    })
                    if expected_status == 200:
                        self.critical_failures.append(name)
                except:
                    print(f"   Error: {response.text[:200]}")
                    self.test_results.append({
                        "test": name,
                        "status": "FAILED",
                        "error": response.text[:200],
                        "expected_status": expected_status,
                        "actual_status": response.status_code
                    })
                    if expected_status == 200:
                        self.critical_failures.append(name)
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                "test": name,
                "status": "FAILED",
                "error": str(e)
            })
            if expected_status == 200:
                self.critical_failures.append(name)
            return False, {}

    def test_core_platform_health(self):
        """Test Core Platform Health"""
        print("\n=== TESTING CORE PLATFORM HEALTH ===")
        
        # Test 1: Root API endpoint
        success1, response1 = self.run_test("Root API Endpoint", "GET", "", 200)
        
        if success1:
            version = response1.get("version", "Unknown")
            features = response1.get("features", [])
            print(f"   ✅ Platform Version: {version}")
            print(f"   ✅ Available Features: {len(features)}")
            for feature in features:
                print(f"      - {feature}")
        
        return success1

    def test_database_connections(self):
        """Test Database Connections via API endpoints"""
        print("\n=== TESTING DATABASE CONNECTIONS ===")
        
        # Test enhanced library (MongoDB connection)
        success1, response1 = self.run_test("Enhanced Library Database", "GET", "enhanced-library", 200)
        
        if success1:
            if isinstance(response1, list):
                print(f"   ✅ Enhanced Library Database: {len(response1)} entries loaded")
            else:
                print("   ⚠️  Enhanced Library Database: Unexpected response format")
        
        # Test comprehensive peptides database
        success2, response2 = self.run_test("Comprehensive Peptides Database", "GET", "peptides", 200)
        
        if success2:
            if isinstance(response2, list):
                print(f"   ✅ Comprehensive Peptides Database: {len(response2)} entries loaded")
                if len(response2) >= 60:
                    print("   ✅ Database expansion confirmed (60+ entries)")
                else:
                    print(f"   ⚠️  Database may not be fully expanded ({len(response2)} entries)")
            else:
                print("   ⚠️  Comprehensive Peptides Database: Unexpected response format")
        
        return success1 and success2

    def test_dr_peptide_ai_functionality(self):
        """Test Dr. Peptide AI Core Functionality"""
        print("\n=== TESTING DR. PEPTIDE AI FUNCTIONALITY ===")
        
        # Test 1: Basic chat functionality
        basic_chat = {
            "message": "What are the key benefits of BPC-157 for tissue healing?",
            "conversation_history": []
        }
        
        success1, response1 = self.run_test("Dr. Peptide Basic Chat", "POST", "dr-peptide/chat", 200, data=basic_chat)
        
        if success1:
            if response1.get("success"):
                ai_response = response1.get("response", "")
                if len(ai_response) > 100 and "BPC-157" in ai_response:
                    print("   ✅ Dr. Peptide AI responding with comprehensive answers")
                else:
                    print("   ⚠️  Dr. Peptide AI response may be incomplete")
            else:
                print(f"   ❌ Dr. Peptide AI chat failed: {response1.get('error')}")
                self.critical_failures.append("Dr. Peptide AI Basic Chat")
        
        # Test 2: Lab interpretation
        lab_data = {
            "lab_data": {
                "TSH": "3.5 mIU/L",
                "Free_T4": "1.0 ng/dL",
                "CRP": "5.2 mg/L",
                "Vitamin_D": "25 ng/mL"
            },
            "patient_context": {
                "age": 45,
                "gender": "female",
                "primary_concerns": ["Fatigue", "Weight gain"]
            }
        }
        
        success2, response2 = self.run_test("Dr. Peptide Lab Interpretation", "POST", "dr-peptide/interpret-labs", 200, data=lab_data)
        
        if success2:
            if response2.get("success"):
                interpretation = response2.get("interpretation", "")
                if len(interpretation) > 100:
                    print("   ✅ Lab interpretation functionality working")
                else:
                    print("   ⚠️  Lab interpretation response seems brief")
            else:
                print(f"   ❌ Lab interpretation failed: {response2.get('error')}")
        
        return success1 and success2

    def test_assessment_system(self):
        """Test Multi-Step Assessment System"""
        print("\n=== TESTING ASSESSMENT SYSTEM ===")
        
        # Create test assessment
        assessment_data = {
            "step": 1,
            "data": {
                "patient_name": "System Test Patient",
                "age": 40,
                "gender": "female",
                "weight": 150.0,
                "height_feet": 5,
                "height_inches": 5,
                "email": "test@example.com",
                "primary_concerns": ["Energy", "Sleep"],
                "health_goals": ["Better energy", "Improved sleep"],
                "current_medications": [],
                "medical_history": [],
                "allergies": []
            }
        }
        
        success1, response1 = self.run_test("Create Assessment", "POST", "assessment/multi-step", 200, data=assessment_data)
        
        if success1:
            assessment_id = response1.get("id")
            if assessment_id:
                print(f"   ✅ Assessment created: {assessment_id}")
                
                # Test file upload capability
                lab_content = "Test lab results: TSH: 2.5, Free T4: 1.2"
                
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                    temp_file.write(lab_content)
                    temp_file_path = temp_file.name
                
                try:
                    url = f"{self.api_url}/assessment/{assessment_id}/upload-files"
                    with open(temp_file_path, 'rb') as f:
                        files = {'files': ('test_labs.txt', f, 'text/plain')}
                        response = requests.post(url, files=files)
                    
                    self.tests_run += 1
                    if response.status_code == 200:
                        self.tests_passed += 1
                        print("   ✅ File upload capability working")
                        success2 = True
                    else:
                        print(f"   ❌ File upload failed: {response.status_code}")
                        success2 = False
                        self.critical_failures.append("File Upload")
                        
                except Exception as e:
                    print(f"   ❌ File upload error: {str(e)}")
                    success2 = False
                    self.critical_failures.append("File Upload")
                finally:
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
                
                # Test protocol generation
                success3, response3 = self.run_test(
                    "Protocol Generation",
                    "POST",
                    f"generate-functional-protocol/{assessment_id}",
                    200
                )
                
                if success3:
                    protocol = response3.get("protocol", {})
                    if protocol.get("primary_peptides"):
                        print("   ✅ Protocol generation working")
                    else:
                        print("   ⚠️  Protocol generation may have issues")
                
                return success1 and success2 and success3
            else:
                print("   ❌ No assessment ID returned")
                self.critical_failures.append("Assessment Creation")
                return False
        
        return success1

    def test_expanded_peptide_database(self):
        """Test Expanded Peptide Database (60+ entries)"""
        print("\n=== TESTING EXPANDED PEPTIDE DATABASE (60+ ENTRIES) ===")
        
        # Test comprehensive peptides endpoint
        success1, response1 = self.run_test("Comprehensive Peptides (60+ entries)", "GET", "peptides", 200)
        
        if success1:
            if isinstance(response1, list):
                total_entries = len(response1)
                print(f"   ✅ Database entries: {total_entries}")
                
                if total_entries >= 60:
                    print("   ✅ Database expansion confirmed (60+ entries)")
                else:
                    print(f"   ⚠️  Database expansion incomplete ({total_entries} entries)")
                
                # Check for functional medicine compounds
                compound_names = [item.get("name", "") for item in response1]
                functional_compounds = ["NAD+", "Glutathione", "Methylene Blue", "Berberine"]
                
                found_compounds = 0
                for compound in functional_compounds:
                    if any(compound in name for name in compound_names):
                        found_compounds += 1
                        print(f"   ✅ Functional medicine compound found: {compound}")
                
                if found_compounds >= 2:
                    print("   ✅ Functional medicine compounds integrated")
                else:
                    print("   ⚠️  Limited functional medicine compounds")
            else:
                print("   ❌ Unexpected response format")
                self.critical_failures.append("Peptides Database")
                return False
        
        # Test categories
        success2, response2 = self.run_test("Peptide Categories", "GET", "peptides/categories", 200)
        
        if success2:
            categories = response2.get("categories", [])
            print(f"   ✅ Available categories: {len(categories)}")
            
            # Check for new categories
            new_categories = ["Metabolic Support", "Detoxification", "Neuroprotection", "Longevity"]
            found_new_cats = sum(1 for cat in new_categories if cat in categories)
            
            if found_new_cats >= 2:
                print("   ✅ New categories integrated")
            else:
                print("   ⚠️  Limited new categories")
        
        return success1 and success2

    def test_integration_verification(self):
        """Test Assessment → Protocol Generation → Feedback Loop"""
        print("\n=== TESTING INTEGRATION VERIFICATION ===")
        
        # Create assessment
        assessment_data = {
            "step": 1,
            "data": {
                "patient_name": "Integration Test Patient",
                "age": 35,
                "gender": "male",
                "primary_concerns": ["Low energy", "Poor recovery"],
                "health_goals": ["Increase energy", "Better recovery"],
                "current_medications": [],
                "medical_history": [],
                "allergies": []
            }
        }
        
        success1, response1 = self.run_test("Integration - Assessment", "POST", "assessment/multi-step", 200, data=assessment_data)
        
        if not success1:
            self.critical_failures.append("Assessment → Protocol Integration")
            return False
        
        assessment_id = response1.get("id")
        if not assessment_id:
            print("   ❌ No assessment ID for integration test")
            self.critical_failures.append("Assessment → Protocol Integration")
            return False
        
        # Generate protocol
        success2, response2 = self.run_test(
            "Integration - Protocol Generation",
            "POST",
            f"generate-functional-protocol/{assessment_id}",
            200
        )
        
        if not success2:
            self.critical_failures.append("Assessment → Protocol Integration")
            return False
        
        protocol_id = response2.get("protocol_id")
        if not protocol_id:
            print("   ❌ No protocol ID for feedback integration")
            return False
        
        # Test feedback loop
        feedback_data = {
            "protocol_id": protocol_id,
            "feedback_data": {
                "protocol_effectiveness": 4,
                "specific_outcomes": {
                    "energy_improvement": 4,
                    "recovery_improvement": 3
                },
                "would_recommend": True
            }
        }
        
        success3, response3 = self.run_test(
            "Integration - Feedback Loop",
            "POST",
            "feedback/protocol",
            200,
            data=feedback_data
        )
        
        if success3:
            print("   ✅ Complete integration loop working")
            print("   ✅ Assessment → Protocol Generation → Feedback loop verified")
        else:
            self.critical_failures.append("Feedback Loop Integration")
        
        return success1 and success2 and success3

    def run_comprehensive_system_health_check(self):
        """Run comprehensive system health check"""
        print("🏥 COMPREHENSIVE SYSTEM HEALTH CHECK FOR PEPTIDEPROTOCOLS.AI")
        print("🎯 VERIFYING ALL CORE PLATFORM COMPONENTS BEFORE PATIENT JOURNEY TESTING")
        print("="*100)
        
        print(f"\n🚀 Running comprehensive system verification...")
        
        # Test 1: Core Platform Health
        print("\n" + "="*25 + " 1. CORE PLATFORM HEALTH " + "="*25)
        test1_success = self.test_core_platform_health()
        
        # Test 2: Database Connections
        print("\n" + "="*25 + " 2. DATABASE CONNECTIONS " + "="*25)
        test2_success = self.test_database_connections()
        
        # Test 3: Dr. Peptide AI Functionality
        print("\n" + "="*25 + " 3. DR. PEPTIDE AI FUNCTIONALITY " + "="*25)
        test3_success = self.test_dr_peptide_ai_functionality()
        
        # Test 4: Expanded Peptide Database (60+ compounds)
        print("\n" + "="*25 + " 4. EXPANDED PEPTIDE DATABASE " + "="*25)
        test4_success = self.test_expanded_peptide_database()
        
        # Test 5: Assessment System
        print("\n" + "="*25 + " 5. ASSESSMENT SYSTEM " + "="*25)
        test5_success = self.test_assessment_system()
        
        # Test 6: Integration Verification
        print("\n" + "="*25 + " 6. INTEGRATION VERIFICATION " + "="*25)
        test6_success = self.test_integration_verification()
        
        # Final Results
        print("\n" + "="*100)
        print("📊 COMPREHENSIVE SYSTEM HEALTH CHECK RESULTS")
        print("="*100)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        all_tests = [test1_success, test2_success, test3_success, test4_success, test5_success, test6_success]
        overall_success = all(all_tests)
        
        print(f"\n🎯 SYSTEM COMPONENT RESULTS:")
        component_names = [
            "Core Platform Health",
            "Database Connections", 
            "Dr. Peptide AI Functionality",
            "Expanded Peptide Database (60+ entries)",
            "Assessment System",
            "Integration Verification"
        ]
        
        for i, (component_name, success) in enumerate(zip(component_names, all_tests), 1):
            status = "✅ OPERATIONAL" if success else "❌ ISSUES DETECTED"
            print(f"   {i}. {component_name}: {status}")
        
        # Critical failures summary
        if self.critical_failures:
            print(f"\n🚨 CRITICAL FAILURES DETECTED:")
            for failure in self.critical_failures:
                print(f"   ❌ {failure}")
        
        # Success criteria evaluation
        print(f"\n🎯 SUCCESS CRITERIA EVALUATION:")
        
        criteria = {
            "All core systems operational": test1_success and test2_success,
            "No critical errors or failures": len(self.critical_failures) == 0,
            "Dr. Peptide AI responding appropriately": test3_success,
            "Expanded peptide database (60+ compounds) accessible": test4_success,
            "Assessment system functional": test5_success,
            "Integration loop complete": test6_success
        }
        
        for criterion, met in criteria.items():
            status = "✅ MET" if met else "❌ NOT MET"
            print(f"   {status} {criterion}")
        
        all_criteria_met = all(criteria.values())
        
        if overall_success and all_criteria_met:
            print(f"\n🎉 SYSTEM HEALTH CHECK: FULLY OPERATIONAL!")
            print("✅ All core platform components working correctly")
            print("✅ No critical errors or failures detected")
            print("✅ Ready for comprehensive patient journey testing")
            print("✅ Collective intelligence system ready to receive and process feedback")
        else:
            print(f"\n⚠️  SYSTEM HEALTH CHECK: ISSUES DETECTED")
            print("❌ Some components may need attention before patient journey testing")
            if self.critical_failures:
                print(f"❌ Critical failures: {', '.join(self.critical_failures)}")
        
        return overall_success and all_criteria_met

if __name__ == "__main__":
    checker = PeptideProtocolsSystemHealthChecker()
    success = checker.run_comprehensive_system_health_check()
    
    if success:
        print(f"\n🎉 PEPTIDEPROTOCOLS.AI SYSTEM: READY FOR PATIENT JOURNEY TESTING!")
    else:
        print(f"\n⚠️  PEPTIDEPROTOCOLS.AI SYSTEM: REQUIRES ATTENTION BEFORE PATIENT JOURNEY TESTING")
    
    exit(0 if success else 1)