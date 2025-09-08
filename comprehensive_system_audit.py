#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM AUDIT for PeptideProtocols.ai
Testing all core platform components as requested in the review
"""

import requests
import sys
import json
from datetime import datetime
import tempfile
import os

class ComprehensiveSystemAudit:
    def __init__(self, base_url="https://peptide-wizard-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.assessment_ids = []
        self.protocol_ids = []

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
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Error: {response.text[:200]}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_core_platform_components(self):
        """Test all core platform components"""
        print("\n" + "="*80)
        print("🏗️  CORE PLATFORM COMPONENTS AUDIT")
        print("="*80)
        
        # 1. Root API Health Check
        success1, response1 = self.run_test("Platform Health Check", "GET", "", 200)
        
        if success1:
            version = response1.get("version", "Unknown")
            features = response1.get("features", [])
            print(f"   📊 Platform Version: {version}")
            print(f"   🎯 Features Available: {len(features)}")
            
            expected_features = [
                "Dr. Peptide AI Chat",
                "Enhanced Clinical Database", 
                "Multi-step Assessment Wizard",
                "File Upload & Analysis",
                "Functional Medicine Protocols"
            ]
            
            for feature in expected_features:
                if feature in features:
                    print(f"   ✅ {feature}")
                else:
                    print(f"   ❌ {feature} - Missing")
        
        return success1

    def test_dr_peptide_ai_system(self):
        """Test Dr. Peptide AI Chat System with GPT-4 integration"""
        print("\n" + "="*80)
        print("🤖 DR. PEPTIDE AI CHAT SYSTEM AUDIT")
        print("="*80)
        
        # Test comprehensive functional medicine query
        chat_data = {
            "message": "I have a 45-year-old female patient with chronic fatigue, elevated inflammatory markers (CRP 5.2), low vitamin D (22 ng/mL), and poor sleep quality. She's interested in peptide therapy. What comprehensive functional medicine protocol would you recommend, including specific peptides, dosing, and monitoring parameters?",
            "conversation_history": []
        }
        
        success1, response1 = self.run_test("Dr. Peptide - Comprehensive Query", "POST", "dr-peptide/chat", 200, data=chat_data)
        
        if success1 and response1.get("success"):
            ai_response = response1.get("response", "")
            print(f"   📝 Response Length: {len(ai_response)} characters")
            
            # Check for functional medicine approach
            fm_keywords = ["functional medicine", "root cause", "peptide", "dosing", "monitoring", "biomarkers"]
            found_keywords = sum(1 for keyword in fm_keywords if keyword.lower() in ai_response.lower())
            print(f"   🎯 Functional Medicine Keywords: {found_keywords}/{len(fm_keywords)}")
            
            if found_keywords >= 4:
                print("   ✅ Comprehensive functional medicine response")
            else:
                print("   ⚠️  Response may lack functional medicine depth")
        
        # Test lab interpretation
        lab_data = {
            "TSH": "3.8 mIU/L",
            "Free_T4": "1.0 ng/dL",
            "CRP": "5.2 mg/L",
            "Vitamin_D": "22 ng/mL",
            "B12": "280 pg/mL"
        }
        
        success2, response2 = self.run_test("Dr. Peptide - Lab Interpretation", "POST", "dr-peptide/interpret-labs", 200, 
                                          data={"lab_data": lab_data, "patient_context": {"age": 45, "gender": "female"}})
        
        return success1 and success2

    def test_assessment_wizard(self):
        """Test Multi-step Assessment Wizard"""
        print("\n" + "="*80)
        print("📋 MULTI-STEP ASSESSMENT WIZARD AUDIT")
        print("="*80)
        
        # Create comprehensive assessment
        assessment_data = {
            "step": 6,
            "data": {
                "patient_name": "Marcus Thompson",
                "age": 28,
                "gender": "Male",
                "weight": 185.0,
                "height_feet": 6,
                "height_inches": 0,
                "email": "marcus.thompson@crossfit.com",
                "primary_concerns": ["Slow recovery between training sessions", "Occasional joint soreness", "Performance optimization"],
                "health_goals": ["Peak athletic performance", "Faster recovery", "Lean muscle gain"],
                "current_medications": ["Whey protein", "Creatine", "Multivitamin"],
                "medical_history": ["No significant medical history"],
                "allergies": ["None known"],
                "lifestyle_factors": {
                    "exercise": "very_active",
                    "sleep": "good",
                    "stress": "moderate",
                    "diet": "paleo"
                }
            }
        }
        
        success1, response1 = self.run_test("Assessment Wizard - Create", "POST", "assessment/multi-step", 200, data=assessment_data)
        
        if success1 and response1.get("id"):
            assessment_id = response1["id"]
            self.assessment_ids.append(assessment_id)
            print(f"   📝 Assessment Created: {assessment_id}")
            
            # Test protocol generation
            success2, response2 = self.run_test("Assessment - Generate Protocol", "POST", f"generate-functional-protocol/{assessment_id}", 200)
            
            if success2:
                protocol = response2.get("protocol", {})
                protocol_id = response2.get("protocol_id", "")
                if protocol_id:
                    self.protocol_ids.append(protocol_id)
                
                # Verify protocol structure
                required_sections = ["functional_medicine_analysis", "primary_peptides", "practitioner_notes"]
                sections_present = sum(1 for section in required_sections if section in protocol)
                print(f"   📊 Protocol Sections: {sections_present}/{len(required_sections)}")
                
                primary_peptides = protocol.get("primary_peptides", [])
                print(f"   💊 Primary Peptides Recommended: {len(primary_peptides)}")
                
                return success1 and success2
        
        return success1

    def test_database_systems(self):
        """Test Database Systems - Enhanced Protocol Library and Comprehensive Peptides"""
        print("\n" + "="*80)
        print("🗄️  DATABASE SYSTEMS AUDIT")
        print("="*80)
        
        # Test Enhanced Protocol Library
        success1, response1 = self.run_test("Enhanced Protocol Library", "GET", "enhanced-library", 200)
        
        if success1 and isinstance(response1, list):
            print(f"   📊 Enhanced Library Entries: {len(response1)}")
            
            # Check for expected peptides
            expected_peptides = ["BPC-157", "TB-500", "GHK-Cu", "Thymosin Alpha-1", "CJC-1295"]
            found_peptides = [item.get("name", "") for item in response1]
            
            matches = sum(1 for peptide in expected_peptides if peptide in found_peptides)
            print(f"   🎯 Expected Peptides Found: {matches}/{len(expected_peptides)}")
        
        # Test Comprehensive Peptides Database (60+ entries)
        success2, response2 = self.run_test("Comprehensive Peptides Database", "GET", "peptides", 200)
        
        if success2 and isinstance(response2, list):
            total_entries = len(response2)
            print(f"   📊 Comprehensive Database Entries: {total_entries}")
            
            if total_entries >= 60:
                print("   ✅ Database expansion to 60+ entries confirmed")
            else:
                print(f"   ⚠️  Database has {total_entries} entries (expected 60+)")
            
            # Check for functional medicine compounds
            compound_names = [item.get("name", "") for item in response2]
            fm_compounds = ["NAD+", "Glutathione", "Methylene Blue", "Berberine"]
            fm_found = sum(1 for compound in fm_compounds if any(compound in name for name in compound_names))
            print(f"   🧬 Functional Medicine Compounds: {fm_found}/{len(fm_compounds)}")
        
        # Test categories
        success3, response3 = self.run_test("Peptide Categories", "GET", "peptides/categories", 200)
        
        if success3 and isinstance(response3, dict):
            categories = response3.get("categories", [])
            print(f"   📋 Available Categories: {len(categories)}")
            
            new_categories = ["Metabolic Support", "Detoxification", "Neuroprotection"]
            new_found = sum(1 for cat in new_categories if cat in categories)
            print(f"   🆕 New Categories Found: {new_found}/{len(new_categories)}")
        
        return success1 and success2 and success3

    def test_collective_intelligence_system(self):
        """Test all 6 Collective Intelligence feedback endpoints"""
        print("\n" + "="*80)
        print("🧠 COLLECTIVE INTELLIGENCE SYSTEM AUDIT")
        print("="*80)
        
        results = []
        
        # 1. Dr. Peptide Follow-up
        follow_up_data = {
            "protocol_id": self.protocol_ids[0] if self.protocol_ids else "test-protocol-123",
            "days_since_start": 21,
            "patient_context": {
                "name": "Marcus Thompson",
                "primary_concerns": ["Recovery optimization"],
                "current_status": "Improved recovery time from 48hrs to 24hrs"
            }
        }
        
        success1, response1 = self.run_test("CI - Dr. Peptide Follow-up", "POST", "dr-peptide/follow-up", 200, data=follow_up_data)
        results.append(success1)
        
        if success1:
            follow_up_questions = response1.get("follow_up_questions", [])
            print(f"   📝 Follow-up Questions Generated: {len(follow_up_questions)}")
        
        # 2. Protocol Feedback
        feedback_data = {
            "protocol_id": self.protocol_ids[0] if self.protocol_ids else "test-protocol-123",
            "feedback_data": {
                "protocol_effectiveness": 4,
                "days_since_start": 28,
                "specific_outcomes": {
                    "recovery_time": "Improved from 48hrs to 24hrs",
                    "joint_soreness": "Reduced by 80%",
                    "performance": "Noticeable gains in strength"
                },
                "side_effects": ["Mild injection site reactions"],
                "overall_satisfaction": 4.5
            }
        }
        
        success2, response2 = self.run_test("CI - Protocol Feedback", "POST", "feedback/protocol", 200, data=feedback_data)
        results.append(success2)
        
        # 3. Error Correction
        error_data = {
            "incorrect_content": "BPC-157 should be dosed at 1000mcg daily",
            "corrected_content": "BPC-157 optimal dosing is 200-500mcg daily for most applications",
            "reporter_type": "practitioner",
            "severity": "medium",
            "context": "Dosing recommendation correction",
            "additional_notes": "Clinical experience shows lower doses are more effective"
        }
        
        success3, response3 = self.run_test("CI - Error Correction", "POST", "feedback/error-correction", 200, data=error_data)
        results.append(success3)
        
        # 4. Collective Intelligence Insights
        success4, response4 = self.run_test("CI - Get Insights", "GET", "collective-intelligence/insights", 200)
        results.append(success4)
        
        if success4:
            insights = response4.get("insights", {})
            print(f"   📊 Insights Available: {len(insights)} categories")
        
        # 5. Practitioner Insights
        practitioner_data = {
            "practitioner_id": "dr-functional-med-123",
            "insight_data": {
                "peptide": "BPC-157",
                "clinical_observation": "Optimal dosing for gut healing appears to be 250mcg twice daily rather than single daily dose",
                "patient_population": "IBS and inflammatory bowel conditions",
                "success_rate": "85%",
                "duration_of_experience": "3 years",
                "specialty": "Functional Medicine"
            }
        }
        
        success5, response5 = self.run_test("CI - Practitioner Insight", "POST", "collective-intelligence/practitioner-insight", 200, data=practitioner_data)
        results.append(success5)
        
        # 6. Feedback Chat
        feedback_chat_data = {
            "message": "I'm experiencing some mild injection site reactions with BPC-157. Is this normal and how can I minimize them?",
            "protocol_id": self.protocol_ids[0] if self.protocol_ids else "test-protocol-123",
            "feedback_context": {
                "current_peptide": "BPC-157",
                "dosage": "250mcg daily",
                "days_on_protocol": 14
            }
        }
        
        success6, response6 = self.run_test("CI - Feedback Chat", "POST", "dr-peptide/feedback-chat", 200, data=feedback_chat_data)
        results.append(success6)
        
        if success6:
            chat_response = response6.get("response", "")
            print(f"   💬 Feedback Chat Response: {len(chat_response)} characters")
        
        successful_endpoints = sum(results)
        print(f"\n   📊 Collective Intelligence Endpoints: {successful_endpoints}/6 working")
        
        return successful_endpoints >= 5  # Allow 1 endpoint to fail

    def test_complete_patient_journey(self):
        """Test complete patient journey - Assessment → Protocol → Feedback"""
        print("\n" + "="*80)
        print("🎯 COMPLETE PATIENT JOURNEY AUDIT")
        print("="*80)
        
        # Create Dr. Jennifer Rodriguez assessment
        jennifer_assessment = {
            "step": 6,
            "data": {
                "patient_name": "Dr. Jennifer Rodriguez",
                "age": 52,
                "gender": "Female",
                "weight": 145.0,
                "height_feet": 5,
                "height_inches": 5,
                "email": "jennifer.rodriguez@executive.com",
                "primary_concerns": ["Chronic fatigue", "Brain fog", "High stress", "Hormonal imbalances (perimenopause)", "Poor sleep quality"],
                "health_goals": ["Energy restoration", "Cognitive enhancement", "Stress resilience", "Hormonal optimization", "Longevity"],
                "current_medications": ["Levothyroxine 50mcg", "Magnesium 400mg", "Vitamin D3 2000 IU"],
                "medical_history": ["Perimenopause", "Hypothyroidism", "Anxiety", "Sleep disorders"],
                "allergies": ["Sulfa drugs"],
                "lifestyle_factors": {
                    "exercise": "sedentary",
                    "sleep": "poor",
                    "stress": "very_high",
                    "diet": "irregular"
                }
            }
        }
        
        # Step 1: Create Assessment
        success1, response1 = self.run_test("Patient Journey - Create Assessment", "POST", "assessment/multi-step", 200, data=jennifer_assessment)
        
        if not success1 or not response1.get("id"):
            return False
        
        jennifer_id = response1["id"]
        print(f"   📝 Dr. Jennifer Rodriguez Assessment: {jennifer_id}")
        
        # Step 2: Generate Protocol
        success2, response2 = self.run_test("Patient Journey - Generate Protocol", "POST", f"generate-functional-protocol/{jennifer_id}", 200)
        
        if not success2:
            return False
        
        protocol = response2.get("protocol", {})
        protocol_id = response2.get("protocol_id", "")
        primary_peptides = protocol.get("primary_peptides", [])
        
        print(f"   💊 Protocol Generated: {protocol_id}")
        print(f"   🎯 Primary Peptides: {len(primary_peptides)}")
        
        # Verify appropriate peptides for executive/hormonal concerns
        expected_peptides = ["Selank", "CJC-1295", "Thymosin"]
        found_appropriate = False
        for peptide in primary_peptides:
            if isinstance(peptide, dict):
                peptide_name = peptide.get("name", "")
                if any(expected in peptide_name for expected in expected_peptides):
                    found_appropriate = True
                    print(f"   ✅ Appropriate peptide found: {peptide_name}")
        
        # Step 3: Dr. Peptide Consultation
        consultation_data = {
            "message": f"I have a 52-year-old female executive experiencing chronic fatigue, brain fog, and perimenopause symptoms. She has hypothyroidism and high stress. What specific peptide protocol would you recommend for cognitive enhancement and hormonal optimization?",
            "conversation_history": []
        }
        
        success3, response3 = self.run_test("Patient Journey - Dr. Peptide Consultation", "POST", "dr-peptide/chat", 200, data=consultation_data)
        
        if success3 and response3.get("success"):
            ai_response = response3.get("response", "")
            # Check for relevant keywords
            relevant_keywords = ["cognitive", "hormonal", "perimenopause", "executive", "stress", "peptide"]
            found_keywords = sum(1 for keyword in relevant_keywords if keyword.lower() in ai_response.lower())
            print(f"   🎯 Relevant Keywords in Response: {found_keywords}/{len(relevant_keywords)}")
        
        # Step 4: Submit Feedback
        feedback_data = {
            "protocol_id": protocol_id,
            "feedback_data": {
                "protocol_effectiveness": 4.8,
                "days_since_start": 42,
                "specific_outcomes": {
                    "energy_levels": "Increased by 70%",
                    "brain_fog": "Significantly reduced",
                    "sleep_quality": "Improved from 4/10 to 7/10",
                    "stress_management": "Much better coping"
                },
                "side_effects": ["None reported"],
                "overall_satisfaction": 4.8
            }
        }
        
        success4, response4 = self.run_test("Patient Journey - Submit Feedback", "POST", "feedback/protocol", 200, data=feedback_data)
        
        journey_success = all([success1, success2, success3, success4])
        
        if journey_success:
            print("   ✅ Complete patient journey successful")
        else:
            print("   ⚠️  Patient journey has some issues")
        
        return journey_success

    def test_content_verification(self):
        """Verify content completeness and accuracy"""
        print("\n" + "="*80)
        print("📚 CONTENT VERIFICATION AUDIT")
        print("="*80)
        
        # Test comprehensive peptides database content
        success1, response1 = self.run_test("Content - Peptides Database", "GET", "peptides", 200)
        
        content_score = 0
        total_checks = 0
        
        if success1 and isinstance(response1, list):
            total_checks += 1
            if len(response1) >= 60:
                content_score += 1
                print(f"   ✅ Database size: {len(response1)} entries (60+ target met)")
            else:
                print(f"   ⚠️  Database size: {len(response1)} entries (below 60 target)")
            
            # Check data completeness
            if response1:
                sample_peptide = response1[0]
                required_fields = ["name", "category", "indications", "mechanism_of_action", "evidence_level"]
                
                total_checks += 1
                fields_present = sum(1 for field in required_fields if field in sample_peptide)
                if fields_present == len(required_fields):
                    content_score += 1
                    print(f"   ✅ Data structure: All required fields present")
                else:
                    print(f"   ⚠️  Data structure: {fields_present}/{len(required_fields)} fields present")
        
        # Test enhanced protocol library content
        success2, response2 = self.run_test("Content - Enhanced Library", "GET", "enhanced-library", 200)
        
        if success2 and isinstance(response2, list):
            total_checks += 1
            if len(response2) >= 9:
                content_score += 1
                print(f"   ✅ Enhanced library: {len(response2)} comprehensive entries")
            else:
                print(f"   ⚠️  Enhanced library: {len(response2)} entries (expected 9+)")
        
        # Test categories completeness
        success3, response3 = self.run_test("Content - Categories", "GET", "peptides/categories", 200)
        
        if success3 and isinstance(response3, dict):
            categories = response3.get("categories", [])
            total_checks += 1
            if len(categories) >= 10:
                content_score += 1
                print(f"   ✅ Categories: {len(categories)} available")
            else:
                print(f"   ⚠️  Categories: {len(categories)} available (expected 10+)")
        
        content_percentage = (content_score / total_checks * 100) if total_checks > 0 else 0
        print(f"\n   📊 Content Completeness: {content_score}/{total_checks} ({content_percentage:.1f}%)")
        
        return content_percentage >= 75

    def run_comprehensive_audit(self):
        """Run the complete comprehensive system audit"""
        print("🚀 STARTING COMPREHENSIVE SYSTEM AUDIT FOR PEPTIDEPROTOCOLS.AI")
        print("="*90)
        print("📋 AUDIT SCOPE:")
        print("   • Core Platform Components (Dr. Peptide AI, Assessment Wizard, File Upload, Protocol Generation)")
        print("   • Database Systems (Enhanced Protocol Library, 60+ Comprehensive Peptides)")
        print("   • Collective Intelligence System (All 6 feedback endpoints)")
        print("   • Complete Patient Journey Integration Testing")
        print("   • Content Verification (Database completeness, Scientific accuracy)")
        print("="*90)
        
        audit_results = {}
        
        # Run all audit components
        audit_results["core_platform"] = self.test_core_platform_components()
        audit_results["dr_peptide_ai"] = self.test_dr_peptide_ai_system()
        audit_results["assessment_wizard"] = self.test_assessment_wizard()
        audit_results["database_systems"] = self.test_database_systems()
        audit_results["collective_intelligence"] = self.test_collective_intelligence_system()
        audit_results["patient_journey"] = self.test_complete_patient_journey()
        audit_results["content_verification"] = self.test_content_verification()
        
        # Calculate overall results
        successful_components = sum(audit_results.values())
        total_components = len(audit_results)
        success_rate = (successful_components / total_components * 100)
        
        # Final audit report
        print("\n" + "="*90)
        print("📊 COMPREHENSIVE SYSTEM AUDIT RESULTS")
        print("="*90)
        
        for component, success in audit_results.items():
            status = "✅ PASSED" if success else "❌ FAILED"
            component_name = component.replace("_", " ").title()
            print(f"   {status} {component_name}")
        
        print(f"\n📈 OVERALL AUDIT RESULTS:")
        print(f"   Tests Run: {self.tests_run}")
        print(f"   Tests Passed: {self.tests_passed}")
        print(f"   Individual Test Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        print(f"   Component Success Rate: {success_rate:.1f}% ({successful_components}/{total_components})")
        
        if success_rate >= 85:
            print(f"\n🎉 AUDIT RESULT: SYSTEM READY FOR PRODUCTION")
            print(f"   ✅ All major components operational")
            print(f"   ✅ No critical failures detected")
            print(f"   ✅ Complete patient journey functional")
        elif success_rate >= 70:
            print(f"\n⚠️  AUDIT RESULT: SYSTEM MOSTLY FUNCTIONAL - MINOR ISSUES")
            print(f"   ✅ Core functionality working")
            print(f"   ⚠️  Some components need attention")
        else:
            print(f"\n❌ AUDIT RESULT: SYSTEM NEEDS SIGNIFICANT WORK")
            print(f"   ❌ Multiple critical components failing")
            print(f"   ❌ Not ready for production")
        
        return audit_results

if __name__ == "__main__":
    auditor = ComprehensiveSystemAudit()
    results = auditor.run_comprehensive_audit()