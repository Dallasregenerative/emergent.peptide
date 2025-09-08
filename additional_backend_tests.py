#!/usr/bin/env python3
"""
Additional Backend Tests
Tests the backend tasks that need retesting according to test_result.md:
- Phase 3 AI Intelligence Upgrade - Evidence-Based Recommendations
- Phase 3 AI Intelligence Upgrade - Cost Analysis Integration  
- Progress Tracking Service
"""

import requests
import json
import sys
from datetime import datetime

class AdditionalBackendTester:
    def __init__(self, base_url="https://peptide-wizard-3.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        
    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
            if details:
                print(f"   {details}")
        else:
            print(f"❌ {name}")
            if details:
                print(f"   {details}")
    
    def make_request(self, method, endpoint, data=None):
        """Make API request with error handling"""
        url = f"{self.api_url}/{endpoint}" if endpoint else f"{self.api_url}/"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            
            return response.status_code, response.json() if response.content else {}
        except Exception as e:
            return 500, {"error": str(e)}
    
    def test_evidence_based_recommendations(self):
        """Test Phase 3 AI Intelligence Upgrade - Evidence-Based Recommendations"""
        print("\n=== TESTING: Evidence-Based Recommendations ===")
        
        # Test 1: Dr. Peptide AI Chat with evidence-based query
        evidence_query = {
            "message": "What is the scientific evidence for BPC-157 in treating inflammatory bowel disease? Please provide specific studies, dosing protocols based on research, and mechanistic explanations with references.",
            "conversation_history": []
        }
        
        status_code, response = self.make_request("POST", "dr-peptide/chat", evidence_query)
        
        if status_code == 200 and response.get("success"):
            ai_response = response.get("response", "")
            
            # Check for evidence-based content
            evidence_keywords = [
                "study", "research", "clinical", "trial", "evidence", 
                "mechanism", "dosing", "protocol", "reference", "pubmed"
            ]
            
            found_keywords = [kw for kw in evidence_keywords if kw.lower() in ai_response.lower()]
            evidence_score = len(found_keywords)
            
            if evidence_score >= 5:
                self.log_test(
                    "Evidence-Based AI Response", 
                    True, 
                    f"Strong evidence integration ({evidence_score}/10 keywords): {found_keywords}"
                )
            else:
                self.log_test(
                    "Evidence-Based AI Response", 
                    False, 
                    f"Limited evidence content ({evidence_score}/10 keywords): {found_keywords}"
                )
            
            # Check response length (comprehensive responses should be substantial)
            if len(ai_response) > 1500:
                self.log_test(
                    "Comprehensive Evidence Response", 
                    True, 
                    f"Detailed response ({len(ai_response)} characters)"
                )
            else:
                self.log_test(
                    "Comprehensive Evidence Response", 
                    False, 
                    f"Brief response ({len(ai_response)} characters)"
                )
                
        else:
            self.log_test(
                "Evidence-Based AI Response", 
                False, 
                f"Status: {status_code}, Error: {response.get('error', 'Unknown')}"
            )
        
        # Test 2: Protocol generation with evidence-based analysis
        # First create an assessment
        assessment_data = {
            "step": 1,
            "data": {
                "patient_name": "Evidence Test Patient",
                "age": 40,
                "gender": "Male",
                "primary_concerns": ["Inflammatory bowel disease", "Chronic inflammation"],
                "health_goals": ["Reduce inflammation", "Heal gut lining"],
                "medical_history": ["Crohn's disease"],
                "current_medications": ["Mesalamine"],
                "allergies": []
            }
        }
        
        status_code2, response2 = self.make_request("POST", "assessment/multi-step", assessment_data)
        
        if status_code2 == 200 and response2.get("id"):
            assessment_id = response2["id"]
            
            # Generate protocol
            status_code3, response3 = self.make_request(
                "POST", 
                f"generate-functional-protocol/{assessment_id}"
            )
            
            if status_code3 == 200:
                protocol = response3.get("protocol", {})
                
                # Check for evidence-based elements in protocol
                scientific_support = protocol.get("scientific_support", {})
                if scientific_support:
                    references = scientific_support.get("key_references", [])
                    evidence_levels = scientific_support.get("evidence_levels", [])
                    
                    if references or evidence_levels:
                        self.log_test(
                            "Evidence-Based Protocol Generation", 
                            True, 
                            f"Scientific support included: {len(references)} references, {len(evidence_levels)} evidence levels"
                        )
                    else:
                        self.log_test(
                            "Evidence-Based Protocol Generation", 
                            False, 
                            "Scientific support section empty"
                        )
                else:
                    self.log_test(
                        "Evidence-Based Protocol Generation", 
                        False, 
                        "No scientific support section in protocol"
                    )
            else:
                self.log_test(
                    "Evidence-Based Protocol Generation", 
                    False, 
                    f"Protocol generation failed: {status_code3}"
                )
        else:
            self.log_test(
                "Evidence-Based Protocol Generation", 
                False, 
                "Failed to create assessment for protocol test"
            )
        
        return status_code == 200 and response.get("success")
    
    def test_cost_analysis_integration(self):
        """Test Phase 3 AI Intelligence Upgrade - Cost Analysis Integration"""
        print("\n=== TESTING: Cost Analysis Integration ===")
        
        # Test 1: AI chat with cost-focused query
        cost_query = {
            "message": "I need a cost-effective peptide protocol for a patient with chronic fatigue on a limited budget. What are the most affordable options, typical monthly costs, and ways to optimize the protocol for cost savings while maintaining effectiveness?",
            "conversation_history": []
        }
        
        status_code, response = self.make_request("POST", "dr-peptide/chat", cost_query)
        
        if status_code == 200 and response.get("success"):
            ai_response = response.get("response", "")
            
            # Check for cost-related content
            cost_keywords = [
                "cost", "price", "affordable", "budget", "expensive", 
                "savings", "economical", "value", "monthly", "insurance"
            ]
            
            found_keywords = [kw for kw in cost_keywords if kw.lower() in ai_response.lower()]
            cost_score = len(found_keywords)
            
            if cost_score >= 3:
                self.log_test(
                    "Cost Analysis AI Response", 
                    True, 
                    f"Cost considerations addressed ({cost_score}/10 keywords): {found_keywords}"
                )
            else:
                self.log_test(
                    "Cost Analysis AI Response", 
                    False, 
                    f"Limited cost analysis ({cost_score}/10 keywords): {found_keywords}"
                )
                
        else:
            self.log_test(
                "Cost Analysis AI Response", 
                False, 
                f"Status: {status_code}, Error: {response.get('error', 'Unknown')}"
            )
        
        # Test 2: Protocol generation with cost analysis
        assessment_data = {
            "step": 1,
            "data": {
                "patient_name": "Budget Test Patient",
                "age": 35,
                "gender": "Female",
                "primary_concerns": ["Chronic fatigue", "Limited budget"],
                "health_goals": ["Increase energy", "Cost-effective treatment"],
                "medical_history": [],
                "current_medications": [],
                "allergies": []
            }
        }
        
        status_code2, response2 = self.make_request("POST", "assessment/multi-step", assessment_data)
        
        if status_code2 == 200 and response2.get("id"):
            assessment_id = response2["id"]
            
            status_code3, response3 = self.make_request(
                "POST", 
                f"generate-functional-protocol/{assessment_id}"
            )
            
            if status_code3 == 200:
                protocol = response3.get("protocol", {})
                
                # Check for cost analysis in protocol
                cost_analysis = protocol.get("cost_analysis", {})
                if cost_analysis:
                    monthly_cost = cost_analysis.get("total_monthly_cost")
                    cost_breakdown = cost_analysis.get("cost_breakdown", [])
                    cost_optimization = cost_analysis.get("cost_optimization", [])
                    
                    if monthly_cost or cost_breakdown or cost_optimization:
                        self.log_test(
                            "Cost Analysis in Protocol", 
                            True, 
                            f"Cost analysis included: monthly cost: {monthly_cost}, breakdown items: {len(cost_breakdown)}, optimizations: {len(cost_optimization)}"
                        )
                    else:
                        self.log_test(
                            "Cost Analysis in Protocol", 
                            False, 
                            "Cost analysis section present but empty"
                        )
                else:
                    self.log_test(
                        "Cost Analysis in Protocol", 
                        False, 
                        "No cost analysis section in protocol"
                    )
            else:
                self.log_test(
                    "Cost Analysis in Protocol", 
                    False, 
                    f"Protocol generation failed: {status_code3}"
                )
        else:
            self.log_test(
                "Cost Analysis in Protocol", 
                False, 
                "Failed to create assessment for cost analysis test"
            )
        
        return status_code == 200 and response.get("success")
    
    def test_progress_tracking_service(self):
        """Test Progress Tracking Service"""
        print("\n=== TESTING: Progress Tracking Service ===")
        
        # Test 1: Track Progress endpoint
        progress_data = {
            "patient_id": "test-patient-123",
            "protocol_id": "test-protocol-456", 
            "progress_data": {
                "week": 2,
                "energy_level": 7,
                "sleep_quality": 6,
                "side_effects": "None reported",
                "compliance": "95%",
                "notes": "Patient reports improved energy and better sleep"
            }
        }
        
        status_code, response = self.make_request("POST", "progress/track", progress_data)
        
        if status_code == 200:
            self.log_test(
                "Track Progress Endpoint", 
                True, 
                f"Progress tracked successfully: {response.get('message', '')}"
            )
        else:
            error_detail = response.get("detail", "Unknown error")
            self.log_test(
                "Track Progress Endpoint", 
                False, 
                f"Status: {status_code}, Error: {error_detail}"
            )
        
        # Test 2: Get Progress endpoint
        status_code2, response2 = self.make_request("GET", "progress/test-patient-123")
        
        if status_code2 == 200:
            self.log_test(
                "Get Progress Endpoint", 
                True, 
                f"Progress data retrieved: {response2.get('message', '')}"
            )
        else:
            error_detail2 = response2.get("detail", "Unknown error")
            self.log_test(
                "Get Progress Endpoint", 
                False, 
                f"Status: {status_code2}, Error: {error_detail2}"
            )
        
        # Test 3: Get Analytics endpoint
        status_code3, response3 = self.make_request("GET", "progress/test-patient-123/analytics")
        
        if status_code3 == 200:
            self.log_test(
                "Get Analytics Endpoint", 
                True, 
                f"Analytics generated: {response3.get('message', '')}"
            )
        else:
            error_detail3 = response3.get("detail", "Unknown error")
            self.log_test(
                "Get Analytics Endpoint", 
                False, 
                f"Status: {status_code3}, Error: {error_detail3}"
            )
        
        # Test 4: Track Milestone endpoint
        milestone_data = {
            "protocol_id": "test-protocol-456",
            "milestone_data": {
                "milestone_type": "energy_improvement",
                "achievement_date": "2025-01-15",
                "description": "Patient achieved target energy level of 8/10",
                "verified_by": "Dr. Smith"
            }
        }
        
        status_code4, response4 = self.make_request("POST", "progress/test-patient-123/milestone", milestone_data)
        
        if status_code4 == 200:
            self.log_test(
                "Track Milestone Endpoint", 
                True, 
                f"Milestone tracked: {response4.get('message', '')}"
            )
        else:
            error_detail4 = response4.get("detail", "Unknown error")
            self.log_test(
                "Track Milestone Endpoint", 
                False, 
                f"Status: {status_code4}, Error: {error_detail4}"
            )
        
        # Overall progress tracking success
        all_endpoints_working = all([
            status_code == 200,
            status_code2 == 200, 
            status_code3 == 200,
            status_code4 == 200
        ])
        
        return all_endpoints_working
    
    def run_all_tests(self):
        """Run all additional backend tests"""
        print("🧪 ADDITIONAL BACKEND TESTS")
        print("=" * 50)
        print("Testing backend tasks that need retesting according to test_result.md")
        
        # Run tests
        test_results = []
        
        test_results.append(self.test_evidence_based_recommendations())
        test_results.append(self.test_cost_analysis_integration())
        test_results.append(self.test_progress_tracking_service())
        
        # Final summary
        print("\n" + "=" * 50)
        print("📊 ADDITIONAL BACKEND TEST SUMMARY")
        print("=" * 50)
        
        success_count = sum(test_results)
        total_tests = len(test_results)
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        
        print(f"Overall Success Rate: {self.tests_passed}/{self.tests_run} ({success_rate:.1f}%)")
        print(f"Major Test Categories: {success_count}/{total_tests} passed")
        
        if success_count == total_tests:
            print("🎉 ALL ADDITIONAL TESTS PASSED!")
        else:
            print("⚠️  SOME ADDITIONAL TESTS FAILED")
            failed_tests = total_tests - success_count
            print(f"❌ {failed_tests} major test categories failed")
        
        return success_count, total_tests, self.tests_passed, self.tests_run

if __name__ == "__main__":
    tester = AdditionalBackendTester()
    success_count, total_tests, tests_passed, tests_run = tester.run_all_tests()
    sys.exit(0 if success_count == total_tests else 1)