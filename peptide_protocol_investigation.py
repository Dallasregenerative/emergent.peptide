#!/usr/bin/env python3
"""
URGENT DATA INVESTIGATION - Distinguish Between Peptides vs Protocols Count
Backend Testing for PeptideProtocols.ai

CRITICAL INVESTIGATION:
User corrected that they have 60 peptides but 87 protocols. 
The homepage statistics API may be incorrectly counting peptides instead of protocols.

INVESTIGATION OBJECTIVES:
1. Protocol Data Sources Analysis - Check what ENHANCED_CLINICAL_PEPTIDES actually contains
2. Current API Behavior Analysis - Test /api/stats/homepage endpoint 
3. Find Correct Protocol Count Source - Look for protocol library endpoints with 87 protocols
4. Verify Data Structure - Check if protocols are treatment plans using peptides

EXPECTED FINDINGS:
- Peptides: 60 (individual compounds)
- Protocols: 87 (treatment protocols, possibly multiple per peptide)
"""

import asyncio
import aiohttp
import json
import sys
import os
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://peptideai-debug.preview.emergentagent.com/api"

class PeptideProtocolInvestigation:
    def __init__(self):
        self.session = None
        self.results = {
            "investigation_timestamp": datetime.now().isoformat(),
            "data_sources": {},
            "api_endpoints": {},
            "count_analysis": {},
            "findings": [],
            "recommendations": []
        }
    
    async def setup_session(self):
        """Setup HTTP session"""
        self.session = aiohttp.ClientSession()
    
    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
    
    async def test_endpoint(self, endpoint, description):
        """Test a specific API endpoint"""
        try:
            url = f"{BACKEND_URL}{endpoint}"
            print(f"\n🔍 Testing: {description}")
            print(f"   URL: {url}")
            
            async with self.session.get(url) as response:
                status = response.status
                if status == 200:
                    data = await response.json()
                    print(f"   ✅ Status: {status}")
                    return {"success": True, "status": status, "data": data}
                else:
                    text = await response.text()
                    print(f"   ❌ Status: {status}")
                    print(f"   Error: {text[:200]}...")
                    return {"success": False, "status": status, "error": text}
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def investigate_homepage_stats(self):
        """Investigate the homepage statistics API"""
        print("\n" + "="*80)
        print("🎯 CRITICAL INVESTIGATION: Homepage Statistics API")
        print("="*80)
        
        result = await self.test_endpoint("/stats/homepage", "Homepage Statistics")
        
        if result["success"]:
            data = result["data"]
            self.results["api_endpoints"]["homepage_stats"] = data
            
            print(f"\n📊 HOMEPAGE STATISTICS ANALYSIS:")
            print(f"   Protocols Count: {data.get('protocols', 'N/A')}")
            print(f"   Practitioners Count: {data.get('practitioners', 'N/A')}")
            print(f"   Success Rate: {data.get('success_rate', 'N/A')}%")
            print(f"   Total Assessments: {data.get('total_assessments', 'N/A')}")
            
            # Critical finding
            protocols_count = data.get('protocols', 0)
            if protocols_count:
                self.results["findings"].append(f"Homepage API reports {protocols_count} protocols")
                if protocols_count != 87:
                    self.results["findings"].append(f"⚠️  DISCREPANCY: Expected 87 protocols, found {protocols_count}")
        
        return result
    
    async def investigate_enhanced_library(self):
        """Investigate the enhanced protocol library"""
        print("\n" + "="*80)
        print("🔬 INVESTIGATION: Enhanced Protocol Library")
        print("="*80)
        
        result = await self.test_endpoint("/enhanced-library", "Enhanced Protocol Library")
        
        if result["success"]:
            data = result["data"]
            count = len(data) if isinstance(data, list) else 0
            self.results["api_endpoints"]["enhanced_library"] = {
                "count": count,
                "sample_data": data[:3] if isinstance(data, list) and len(data) > 0 else data
            }
            
            print(f"\n📚 ENHANCED LIBRARY ANALYSIS:")
            print(f"   Total Entries: {count}")
            
            if isinstance(data, list) and len(data) > 0:
                print(f"   Sample Entry Structure:")
                sample = data[0]
                for key in sample.keys():
                    print(f"     - {key}: {type(sample[key]).__name__}")
                
                # Check if these are protocols or peptides
                has_protocol_fields = any(field in sample for field in ['complete_dosing_schedule', 'administration_techniques', 'clinical_indications'])
                has_peptide_fields = any(field in sample for field in ['sequence', 'molecular_weight'])
                
                if has_protocol_fields:
                    self.results["findings"].append(f"Enhanced library contains {count} PROTOCOL entries (has dosing schedules)")
                if has_peptide_fields:
                    self.results["findings"].append(f"Enhanced library contains {count} PEPTIDE entries (has sequences)")
        
        return result
    
    async def investigate_peptides_database(self):
        """Investigate the comprehensive peptides database"""
        print("\n" + "="*80)
        print("🧬 INVESTIGATION: Comprehensive Peptides Database")
        print("="*80)
        
        result = await self.test_endpoint("/peptides", "Comprehensive Peptides Database")
        
        if result["success"]:
            data = result["data"]
            count = len(data) if isinstance(data, list) else 0
            self.results["api_endpoints"]["peptides_database"] = {
                "count": count,
                "sample_data": data[:3] if isinstance(data, list) and len(data) > 0 else data
            }
            
            print(f"\n🧪 PEPTIDES DATABASE ANALYSIS:")
            print(f"   Total Entries: {count}")
            
            if isinstance(data, list) and len(data) > 0:
                print(f"   Sample Entry Structure:")
                sample = data[0]
                for key in sample.keys():
                    print(f"     - {key}: {type(sample[key]).__name__}")
                
                # Check if these are protocols or peptides
                has_protocol_fields = any(field in sample for field in ['complete_dosing_schedule', 'administration_techniques'])
                has_peptide_fields = any(field in sample for field in ['sequence', 'molecular_weight'])
                
                if has_protocol_fields:
                    self.results["findings"].append(f"Peptides database contains {count} entries with PROTOCOL information")
                if has_peptide_fields:
                    self.results["findings"].append(f"Peptides database contains {count} entries with PEPTIDE information")
                
                if count == 60:
                    self.results["findings"].append(f"✅ MATCH: Found expected 60 peptides in comprehensive database")
        
        return result
    
    async def investigate_protocols_endpoints(self):
        """Investigate potential protocol-specific endpoints"""
        print("\n" + "="*80)
        print("📋 INVESTIGATION: Protocol-Specific Endpoints")
        print("="*80)
        
        endpoints_to_test = [
            ("/protocols", "Protocols Endpoint"),
            ("/enhanced-library/categories", "Enhanced Library Categories"),
            ("/peptides/categories", "Peptides Categories"),
        ]
        
        for endpoint, description in endpoints_to_test:
            result = await self.test_endpoint(endpoint, description)
            
            if result["success"]:
                data = result["data"]
                if isinstance(data, list):
                    count = len(data)
                    print(f"   📊 Found {count} entries")
                    self.results["api_endpoints"][endpoint.replace("/", "_")] = {"count": count, "data": data}
                elif isinstance(data, dict) and "count" in data:
                    count = data["count"]
                    print(f"   📊 Found {count} entries")
                    self.results["api_endpoints"][endpoint.replace("/", "_")] = data
    
    async def analyze_data_structure_differences(self):
        """Analyze the differences between data sources"""
        print("\n" + "="*80)
        print("🔍 CRITICAL ANALYSIS: Data Structure Differences")
        print("="*80)
        
        # Compare counts from different sources
        homepage_protocols = self.results["api_endpoints"].get("homepage_stats", {}).get("protocols", 0)
        enhanced_library_count = self.results["api_endpoints"].get("enhanced_library", {}).get("count", 0)
        peptides_db_count = self.results["api_endpoints"].get("peptides_database", {}).get("count", 0)
        
        print(f"\n📊 COUNT COMPARISON:")
        print(f"   Homepage Stats 'protocols': {homepage_protocols}")
        print(f"   Enhanced Library entries: {enhanced_library_count}")
        print(f"   Peptides Database entries: {peptides_db_count}")
        
        self.results["count_analysis"] = {
            "homepage_protocols": homepage_protocols,
            "enhanced_library": enhanced_library_count,
            "peptides_database": peptides_db_count,
            "expected_peptides": 60,
            "expected_protocols": 87
        }
        
        # Critical analysis
        if homepage_protocols == enhanced_library_count:
            self.results["findings"].append(f"🔍 FINDING: Homepage 'protocols' count ({homepage_protocols}) matches Enhanced Library count")
            self.results["findings"].append("💡 HYPOTHESIS: Homepage may be counting Enhanced Library entries as 'protocols'")
        
        if peptides_db_count == 60:
            self.results["findings"].append(f"✅ CONFIRMED: Peptides database has expected 60 peptides")
        
        if homepage_protocols != 87:
            self.results["findings"].append(f"❌ DISCREPANCY: Homepage shows {homepage_protocols} protocols, expected 87")
            self.results["recommendations"].append("Need to find the correct data source for 87 protocols")
        
        # Check if Enhanced Library entries are actually protocols
        enhanced_sample = self.results["api_endpoints"].get("enhanced_library", {}).get("sample_data", [])
        if enhanced_sample and isinstance(enhanced_sample, list) and len(enhanced_sample) > 0:
            sample = enhanced_sample[0]
            if 'complete_dosing_schedule' in sample and 'administration_techniques' in sample:
                self.results["findings"].append("✅ CONFIRMED: Enhanced Library contains PROTOCOL data (dosing schedules, administration)")
                self.results["recommendations"].append("Enhanced Library appears to be the protocol source, not just peptides")
    
    async def investigate_protocol_vs_peptide_relationship(self):
        """Investigate the relationship between protocols and peptides"""
        print("\n" + "="*80)
        print("🔗 INVESTIGATION: Protocol vs Peptide Relationship")
        print("="*80)
        
        # Check if protocols are treatment plans using peptides
        enhanced_data = self.results["api_endpoints"].get("enhanced_library", {}).get("sample_data", [])
        peptides_data = self.results["api_endpoints"].get("peptides_database", {}).get("sample_data", [])
        
        if enhanced_data and peptides_data:
            print(f"\n🔬 RELATIONSHIP ANALYSIS:")
            
            # Check if enhanced library has peptide sequences
            enhanced_sample = enhanced_data[0] if isinstance(enhanced_data, list) else enhanced_data
            peptides_sample = peptides_data[0] if isinstance(peptides_data, list) else peptides_data
            
            enhanced_has_sequence = 'sequence' in enhanced_sample
            peptides_has_sequence = 'sequence' in peptides_sample
            
            enhanced_has_protocols = 'complete_dosing_schedule' in enhanced_sample
            peptides_has_protocols = 'complete_dosing_schedule' in peptides_sample
            
            print(f"   Enhanced Library has sequences: {enhanced_has_sequence}")
            print(f"   Enhanced Library has protocols: {enhanced_has_protocols}")
            print(f"   Peptides DB has sequences: {peptides_has_sequence}")
            print(f"   Peptides DB has protocols: {peptides_has_protocols}")
            
            if enhanced_has_sequence and enhanced_has_protocols:
                self.results["findings"].append("🔍 FINDING: Enhanced Library contains BOTH peptide data AND protocol data")
                self.results["findings"].append("💡 HYPOTHESIS: Enhanced Library entries are comprehensive peptide protocols")
            
            if peptides_has_sequence and peptides_has_protocols:
                self.results["findings"].append("🔍 FINDING: Peptides Database also contains BOTH peptide data AND protocol data")
    
    async def search_for_87_protocols_source(self):
        """Search for the data source that would have 87 protocols"""
        print("\n" + "="*80)
        print("🎯 CRITICAL SEARCH: Looking for 87 Protocols Source")
        print("="*80)
        
        # Test additional endpoints that might contain protocols
        additional_endpoints = [
            ("/", "Root endpoint - check features"),
            ("/enhanced-library?category=all", "Enhanced Library with all categories"),
        ]
        
        for endpoint, description in additional_endpoints:
            result = await self.test_endpoint(endpoint, description)
            
            if result["success"]:
                data = result["data"]
                
                # Check root endpoint for feature information
                if endpoint == "/" and "features" in data:
                    print(f"   🎯 System Features: {data['features']}")
                    self.results["data_sources"]["system_features"] = data["features"]
        
        # Hypothesis: Maybe there are multiple protocol types or categories
        print(f"\n💡 HYPOTHESIS TESTING:")
        print(f"   - Enhanced Library ({self.results['count_analysis'].get('enhanced_library', 0)}) might be base protocols")
        print(f"   - There might be additional protocol variations or combinations")
        print(f"   - User mentioned 87 protocols vs 60 peptides - suggests protocols > peptides")
        
        if self.results['count_analysis'].get('enhanced_library', 0) > self.results['count_analysis'].get('peptides_database', 0):
            self.results["findings"].append("🔍 FINDING: Enhanced Library has MORE entries than Peptides Database")
            self.results["findings"].append("💡 HYPOTHESIS: Enhanced Library might include protocol variations or combinations")
    
    async def investigate_server_code_logic(self):
        """Investigate what the server code is actually counting"""
        print("\n" + "="*80)
        print("🔍 CRITICAL CODE ANALYSIS: Server Logic Investigation")
        print("="*80)
        
        print(f"\n📝 SERVER CODE ANALYSIS:")
        print(f"   From server.py line 934: protocol_count = len(ENHANCED_CLINICAL_PEPTIDES)")
        print(f"   This suggests homepage API counts ENHANCED_CLINICAL_PEPTIDES as 'protocols'")
        
        # Compare with our findings
        homepage_count = self.results["count_analysis"].get("homepage_protocols", 0)
        enhanced_count = self.results["count_analysis"].get("enhanced_library", 0)
        
        if homepage_count == enhanced_count:
            self.results["findings"].append("🔍 CONFIRMED: Homepage API counts Enhanced Library as 'protocols'")
            self.results["findings"].append("💡 ROOT CAUSE: server.py line 934 uses len(ENHANCED_CLINICAL_PEPTIDES)")
        
        print(f"\n🎯 CRITICAL QUESTION:")
        print(f"   Are ENHANCED_CLINICAL_PEPTIDES actually protocols or peptides?")
        print(f"   Based on our analysis, they appear to be comprehensive peptide protocols")
        print(f"   But user expects 87 protocols vs {homepage_count} currently shown")
        
        self.results["recommendations"].extend([
            "INVESTIGATE: Check if ENHANCED_CLINICAL_PEPTIDES should be expanded to 87 entries",
            "INVESTIGATE: Check if there are additional protocol sources not being counted",
            "INVESTIGATE: Verify if user's expectation of 87 protocols is correct",
            "CONSIDER: Maybe protocols include combinations, variations, or different dosing protocols"
        ])
    
    async def generate_final_analysis(self):
        """Generate final analysis and recommendations"""
        print("\n" + "="*80)
        print("📋 FINAL ANALYSIS & RECOMMENDATIONS")
        print("="*80)
        
        print(f"\n🔍 KEY FINDINGS:")
        for i, finding in enumerate(self.results["findings"], 1):
            print(f"   {i}. {finding}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(self.results["recommendations"], 1):
            print(f"   {i}. {rec}")
        
        # Critical determination
        homepage_count = self.results["count_analysis"].get("homepage_protocols", 0)
        enhanced_count = self.results["count_analysis"].get("enhanced_library", 0)
        peptides_count = self.results["count_analysis"].get("peptides_database", 0)
        
        print(f"\n🎯 CRITICAL DETERMINATION:")
        
        if homepage_count == enhanced_count and enhanced_count != 87:
            print(f"   ❌ ISSUE CONFIRMED: Homepage API is counting Enhanced Library ({enhanced_count}) as 'protocols'")
            print(f"   ❌ DISCREPANCY: User expects 87 protocols, system shows {homepage_count}")
            print(f"   ✅ PEPTIDES CORRECT: Found {peptides_count} peptides (matches expected 60)")
            
            self.results["recommendations"].extend([
                "URGENT: Investigate server.py line 934: protocol_count = len(ENHANCED_CLINICAL_PEPTIDES)",
                "URGENT: Find the correct data source for 87 protocols",
                "URGENT: Determine if protocols should be treatment combinations or variations",
                "Consider: Enhanced Library might need expansion to reach 87 protocols"
            ])
        
        # Final verdict
        print(f"\n⚖️  FINAL VERDICT:")
        if peptides_count == 60:
            print(f"   ✅ PEPTIDES COUNT: CORRECT ({peptides_count})")
        else:
            print(f"   ❌ PEPTIDES COUNT: INCORRECT (found {peptides_count}, expected 60)")
        
        if homepage_count == 87:
            print(f"   ✅ PROTOCOLS COUNT: CORRECT ({homepage_count})")
        else:
            print(f"   ❌ PROTOCOLS COUNT: INCORRECT (found {homepage_count}, expected 87)")
            print(f"   🔧 ACTION REQUIRED: Fix homepage statistics API to show correct protocol count")
    
    async def run_investigation(self):
        """Run the complete investigation"""
        print("🚨 URGENT DATA INVESTIGATION - Peptides vs Protocols Count")
        print("="*80)
        print("User Correction: 60 peptides but 87 protocols")
        print("Investigating homepage statistics API accuracy")
        print("="*80)
        
        await self.setup_session()
        
        try:
            # Core investigations
            await self.investigate_homepage_stats()
            await self.investigate_enhanced_library()
            await self.investigate_peptides_database()
            await self.investigate_protocols_endpoints()
            
            # Analysis
            await self.analyze_data_structure_differences()
            await self.investigate_protocol_vs_peptide_relationship()
            await self.search_for_87_protocols_source()
            await self.investigate_server_code_logic()
            
            # Final analysis
            await self.generate_final_analysis()
            
        finally:
            await self.cleanup_session()
        
        return self.results

async def main():
    """Main investigation function"""
    investigation = PeptideProtocolInvestigation()
    results = await investigation.run_investigation()
    
    # Save results to file
    with open('/app/peptide_protocol_investigation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Investigation results saved to: /app/peptide_protocol_investigation_results.json")
    
    return results

if __name__ == "__main__":
    results = asyncio.run(main())
    
    # Return appropriate exit code
    critical_issues = [f for f in results["findings"] if "DISCREPANCY" in f or "INCORRECT" in f]
    if critical_issues:
        print(f"\n🚨 CRITICAL ISSUES FOUND: {len(critical_issues)}")
        sys.exit(1)
    else:
        print(f"\n✅ INVESTIGATION COMPLETED SUCCESSFULLY")
        sys.exit(0)