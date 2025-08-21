"""
File Analysis Service for PeptideProtocols.ai
Handles analysis of uploaded patient files (labs, charts, genetic tests)
"""

import os
import io
import logging
import json
from typing import Dict, Any, Optional, List
import tempfile
from pathlib import Path
from datetime import datetime

# Import required libraries for file processing
import pytesseract
from PIL import Image
import pdfplumber
from openai import AsyncOpenAI

# Add docx support if available
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# Add lxml support if available  
try:
    import lxml.html
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False

class FileAnalysisService:
    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        self.supported_formats = {
            'pdf': self._analyze_pdf,
            'jpg': self._analyze_image, 
            'jpeg': self._analyze_image,
            'png': self._analyze_image,
            'docx': self._analyze_docx,
            'txt': self._analyze_text,
            'xlsx': self._analyze_excel,
            'csv': self._analyze_csv
        }

    async def analyze_uploaded_file(self, file_content: bytes, filename: str, content_type: str, context: str = "") -> Dict[str, Any]:
        """
        Main entry point for file analysis
        """
        try:
            # Determine file extension
            file_extension = Path(filename).suffix.lower().lstrip('.')
            
            if file_extension not in self.supported_formats:
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_extension}",
                    "filename": filename,
                    "analysis_type": "unsupported"
                }

            # Extract text content based on file type
            extracted_text = await self.supported_formats[file_extension](file_content)
            
            if not extracted_text:
                return {
                    "success": False,
                    "error": "No text could be extracted from file",
                    "filename": filename,
                    "analysis_type": "extraction_failed"
                }

            # Analyze with AI for medical context
            analysis_result = await self._ai_analyze_medical_content(extracted_text, filename, context)
            
            return {
                "success": True,
                "filename": filename,
                "analysis_type": self._determine_analysis_type(extracted_text),
                "extracted_text": extracted_text[:1000],  # First 1000 chars for preview
                "full_analysis": analysis_result,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logging.error(f"File analysis error for {filename}: {e}")
            return {
                "success": False,
                "error": str(e),
                "filename": filename,
                "analysis_type": "error"
            }

    async def _analyze_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF files"""
        try:
            text_content = ""
            with io.BytesIO(file_content) as pdf_file:
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + "\n"
            return text_content
        except Exception as e:
            logging.error(f"PDF analysis error: {e}")
            return ""

    async def _analyze_image(self, file_content: bytes) -> str:
        """Extract text from images using OCR"""
        try:
            # Save to temporary file for pytesseract
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name

            # Open image and perform OCR
            image = Image.open(temp_file_path)
            text = pytesseract.image_to_string(image, config='--psm 6')
            
            # Clean up temp file
            os.unlink(temp_file_path)
            
            return text
        except Exception as e:
            logging.error(f"Image OCR error: {e}")
            return ""

    async def _analyze_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX files"""
        if not DOCX_AVAILABLE:
            return "DOCX support not available"
        
        try:
            with io.BytesIO(file_content) as docx_file:
                doc = Document(docx_file)
                text_content = ""
                for paragraph in doc.paragraphs:
                    text_content += paragraph.text + "\n"
            return text_content
        except Exception as e:
            logging.error(f"DOCX analysis error: {e}")
            return ""

    async def _analyze_text(self, file_content: bytes) -> str:
        """Process plain text files"""
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_content.decode('latin-1')
            except Exception as e:
                logging.error(f"Text decoding error: {e}")
                return ""

    async def _analyze_excel(self, file_content: bytes) -> str:
        """Extract data from Excel files"""
        try:
            import pandas as pd
            with io.BytesIO(file_content) as excel_file:
                # Try to read all sheets
                excel_data = pd.read_excel(excel_file, sheet_name=None)
                text_content = ""
                for sheet_name, df in excel_data.items():
                    text_content += f"Sheet: {sheet_name}\n"
                    text_content += df.to_string(index=False) + "\n\n"
            return text_content
        except ImportError:
            return "Excel analysis requires pandas library"
        except Exception as e:
            logging.error(f"Excel analysis error: {e}")
            return ""

    async def _analyze_csv(self, file_content: bytes) -> str:
        """Process CSV files"""
        try:
            import pandas as pd
            with io.BytesIO(file_content) as csv_file:
                df = pd.read_csv(csv_file)
                return df.to_string(index=False)
        except ImportError:
            # Fallback without pandas
            text = file_content.decode('utf-8')
            return text
        except Exception as e:
            logging.error(f"CSV analysis error: {e}")
            return ""

    def _determine_analysis_type(self, text_content: str) -> str:
        """Determine the type of medical document based on content"""
        text_lower = text_content.lower()
        
        # Lab results indicators
        if any(keyword in text_lower for keyword in ['lab results', 'laboratory', 'blood test', 'cbc', 'chemistry panel', 'lipid panel', 'glucose', 'hemoglobin', 'cholesterol']):
            return "lab_results"
        
        # Genetic test indicators
        elif any(keyword in text_lower for keyword in ['genetic', 'dna', 'snp', 'variant', 'allele', 'gene', 'mutation', 'polymorphism']):
            return "genetic_test"
        
        # Medical chart indicators
        elif any(keyword in text_lower for keyword in ['medical record', 'chart', 'history', 'diagnosis', 'treatment', 'medication', 'physician', 'doctor']):
            return "medical_chart"
        
        # Imaging reports
        elif any(keyword in text_lower for keyword in ['mri', 'ct scan', 'x-ray', 'ultrasound', 'imaging', 'radiology']):
            return "imaging_report"
        
        # General medical document
        elif any(keyword in text_lower for keyword in ['patient', 'medical', 'health', 'clinical']):
            return "medical_document"
        
        else:
            return "general_document"

    async def _ai_analyze_medical_content(self, text_content: str, filename: str, context: str) -> Dict[str, Any]:
        """Use AI to analyze medical content and extract key insights"""
        try:
            analysis_type = self._determine_analysis_type(text_content)
            
            # Create specialized prompt based on document type
            prompt = self._create_analysis_prompt(text_content, analysis_type, filename, context)
            
            messages = [
                {
                    "role": "system", 
                    "content": """You are Dr. Peptide, an expert functional medicine practitioner analyzing medical documents. 
                    Provide comprehensive analysis focusing on:
                    - Key findings and abnormal values
                    - Functional medicine interpretation
                    - Potential peptide therapy opportunities
                    - Root cause implications
                    - Recommended follow-up testing
                    
                    Always maintain patient privacy and provide educational insights."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-5",
                messages=messages,
                temperature=0.2,  # Low temperature for consistent medical analysis
                max_tokens=2000
            )
            
            ai_analysis = response.choices[0].message.content
            
            return {
                "ai_interpretation": ai_analysis,
                "analysis_type": analysis_type,
                "key_findings": self._extract_key_findings(text_content, analysis_type),
                "peptide_opportunities": self._identify_peptide_opportunities(ai_analysis),
                "follow_up_recommendations": self._extract_recommendations(ai_analysis)
            }
            
        except Exception as e:
            logging.error(f"AI analysis error: {e}")
            return {
                "ai_interpretation": "Unable to complete AI analysis due to technical issues.",
                "analysis_type": self._determine_analysis_type(text_content),
                "error": str(e)
            }

    def _create_analysis_prompt(self, text_content: str, analysis_type: str, filename: str, context: str) -> str:
        """Create specialized analysis prompt based on document type"""
        
        base_prompt = f"""
Please analyze this {analysis_type} document: {filename}

DOCUMENT CONTENT:
{text_content[:3000]}  # Limit to first 3000 characters to avoid token limits

CONTEXT: {context}

"""

        if analysis_type == "lab_results":
            specific_prompt = """
As Dr. Peptide, please provide a comprehensive lab analysis including:

1. KEY FINDINGS:
   - Identify any values outside optimal functional ranges
   - Note patterns and relationships between markers
   - Highlight areas of concern

2. FUNCTIONAL MEDICINE INTERPRETATION:
   - What do these results suggest about underlying physiology?
   - Potential nutrient deficiencies or imbalances
   - Root cause implications

3. PEPTIDE THERAPY OPPORTUNITIES:
   - Which peptides could address identified issues?
   - Specific protocols based on these findings
   - Expected improvements

4. FOLLOW-UP RECOMMENDATIONS:
   - Additional testing that would be valuable
   - Monitoring plan
   - Lifestyle interventions

Please use optimal functional ranges, not just standard reference ranges.
"""

        elif analysis_type == "genetic_test":
            specific_prompt = """
As Dr. Peptide, please analyze this genetic data including:

1. KEY GENETIC VARIANTS:
   - Important SNPs and their implications
   - Risk factors identified
   - Metabolic implications

2. PEPTIDE THERAPY RELEVANCE:
   - How genetics might influence peptide selection
   - Personalized dosing considerations
   - Metabolism and clearance factors

3. PERSONALIZED RECOMMENDATIONS:
   - Lifestyle modifications based on genetics
   - Targeted supplementation
   - Peptide protocols optimized for genetic profile

4. RISK MITIGATION:
   - Areas requiring extra monitoring
   - Contraindications based on genetics
"""

        elif analysis_type == "medical_chart":
            specific_prompt = """
As Dr. Peptide, please analyze this medical record including:

1. MEDICAL HISTORY SUMMARY:
   - Key diagnoses and conditions
   - Current medications and treatments
   - Surgical history

2. FUNCTIONAL MEDICINE PERSPECTIVE:
   - Root cause analysis of conditions
   - Interconnections between symptoms
   - Systems-based approach

3. PEPTIDE INTEGRATION OPPORTUNITIES:
   - How peptides could complement current care
   - Potential interactions with medications
   - Safety considerations

4. HOLISTIC RECOMMENDATIONS:
   - Comprehensive treatment approach
   - Lifestyle and nutritional support
   - Monitoring and optimization plan
"""

        else:
            specific_prompt = """
Please provide a general medical analysis of this document including:

1. KEY MEDICAL INFORMATION:
   - Important findings or data
   - Relevant health indicators
   - Areas of concern

2. FUNCTIONAL MEDICINE INSIGHTS:
   - Potential root causes
   - Systems-based interpretation
   - Optimization opportunities

3. PEPTIDE THERAPY RELEVANCE:
   - How this information relates to peptide therapy
   - Potential treatment opportunities
   - Safety considerations

4. RECOMMENDATIONS:
   - Next steps for patient care
   - Additional information needed
   - Integration with current treatment
"""

        return base_prompt + specific_prompt

    def _extract_key_findings(self, text_content: str, analysis_type: str) -> List[str]:
        """Extract key findings based on document type"""
        findings = []
        text_lower = text_content.lower()
        
        if analysis_type == "lab_results":
            # Look for common lab markers and values
            lab_markers = ['glucose', 'cholesterol', 'triglycerides', 'hemoglobin', 'white blood cell', 'creatinine', 'tsh', 'testosterone', 'estrogen', 'cortisol']
            for marker in lab_markers:
                if marker in text_lower:
                    # Try to extract the value (simplified approach)
                    start_idx = text_lower.find(marker)
                    end_idx = min(start_idx + 100, len(text_content))
                    finding_text = text_content[start_idx:end_idx].replace('\n', ' ')
                    findings.append(finding_text)
        
        elif analysis_type == "genetic_test":
            # Look for genetic variants
            if 'snp' in text_lower or 'variant' in text_lower:
                findings.append("Genetic variants identified - requires detailed analysis")
        
        # If no specific findings, add general note
        if not findings:
            findings.append(f"Document contains {analysis_type.replace('_', ' ')} information requiring expert interpretation")
        
        return findings[:5]  # Limit to 5 key findings

    def _identify_peptide_opportunities(self, ai_analysis: str) -> List[str]:
        """Extract peptide opportunities from AI analysis"""
        opportunities = []
        
        # Look for peptide mentions in the analysis
        peptide_names = ['BPC-157', 'TB-500', 'GHK-Cu', 'Thymosin Alpha-1', 'CJC-1295', 'Ipamorelin', 'Selank', 'Epitalon', 'PT-141']
        
        for peptide in peptide_names:
            if peptide.lower() in ai_analysis.lower():
                opportunities.append(f"{peptide} therapy indicated based on analysis")
        
        if not opportunities:
            opportunities.append("Peptide therapy opportunities require detailed consultation")
        
        return opportunities

    def _extract_recommendations(self, ai_analysis: str) -> List[str]:
        """Extract follow-up recommendations from AI analysis"""
        recommendations = []
        
        # Look for common recommendation keywords
        rec_keywords = ['recommend', 'suggest', 'consider', 'follow-up', 'monitor', 'test']
        
        sentences = ai_analysis.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in rec_keywords):
                clean_sentence = sentence.strip()
                if clean_sentence and len(clean_sentence) > 20:
                    recommendations.append(clean_sentence)
        
        if not recommendations:
            recommendations.append("Detailed consultation recommended for personalized recommendations")
        
        return recommendations[:3]  # Limit to 3 recommendations

    async def analyze_multiple_files(self, files_data: List[Dict[str, Any]], context: str = "") -> Dict[str, Any]:
        """Analyze multiple files and provide integrated insights"""
        try:
            individual_analyses = []
            all_text_content = []
            
            # Analyze each file individually
            for file_data in files_data:
                analysis = await self.analyze_uploaded_file(
                    file_data['content'],
                    file_data['filename'],
                    file_data['content_type'],
                    context
                )
                individual_analyses.append(analysis)
                if analysis.get('success'):
                    all_text_content.append(analysis.get('extracted_text', ''))
            
            # Create integrated analysis
            if all_text_content:
                integrated_analysis = await self._create_integrated_analysis(all_text_content, context)
            else:
                integrated_analysis = "No files could be successfully analyzed"
            
            return {
                "success": True,
                "individual_analyses": individual_analyses,
                "integrated_analysis": integrated_analysis,
                "total_files": len(files_data),
                "successful_analyses": sum(1 for a in individual_analyses if a.get('success', False)),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Multiple file analysis error: {e}")
            return {
                "success": False,
                "error": str(e),
                "individual_analyses": [],
                "integrated_analysis": "Analysis failed due to technical issues"
            }

    async def _create_integrated_analysis(self, all_text_content: List[str], context: str) -> str:
        """Create integrated analysis across multiple documents"""
        try:
            combined_content = "\n\n=== DOCUMENT SEPARATOR ===\n\n".join(all_text_content)
            
            prompt = f"""
As Dr. Peptide, please provide an integrated analysis across these multiple patient documents:

CONTEXT: {context}

COMBINED DOCUMENT CONTENT:
{combined_content[:4000]}  # Limit total content

Please provide:

1. INTEGRATED FINDINGS:
   - Key patterns across all documents
   - Correlations and connections
   - Comprehensive health picture

2. PEPTIDE THERAPY STRATEGY:
   - Unified peptide protocol recommendations
   - Prioritized interventions
   - Synergistic approaches

3. COMPREHENSIVE PLAN:
   - Integrated treatment approach
   - Timeline and priorities
   - Monitoring strategy

4. NEXT STEPS:
   - Additional information needed
   - Coordinated care recommendations
   - Patient education priorities

Focus on creating a cohesive, comprehensive treatment strategy.
"""

            messages = [
                {
                    "role": "system",
                    "content": "You are Dr. Peptide providing integrated analysis across multiple patient documents. Focus on creating comprehensive, coordinated treatment strategies."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.3,
                max_tokens=2500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Integrated analysis error: {e}")
            return "Unable to create integrated analysis due to technical issues."