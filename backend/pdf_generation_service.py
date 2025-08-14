"""
PDF Generation Service for PeptideProtocols.ai
Professional medical-grade protocol and assessment PDF generation
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from io import BytesIO
from datetime import datetime
import json

class PeptideProtocolsPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom styles for medical documents"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1f2937')
        ))
        
        # Medical header style
        self.styles.add(ParagraphStyle(
            name='MedicalHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor('#2563eb'),
            borderWidth=1,
            borderColor=colors.HexColor('#e5e7eb'),
            borderPadding=8,
            backgroundColor=colors.HexColor('#f8fafc')
        ))
        
        # Protocol section style
        self.styles.add(ParagraphStyle(
            name='ProtocolSection',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica-Bold'
        ))
        
        # Body text with medical formatting
        self.styles.add(ParagraphStyle(
            name='MedicalBody',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#1f2937')
        ))
        
        # Important notice style
        self.styles.add(ParagraphStyle(
            name='ImportantNotice',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            spaceAfter=10,
            leftIndent=20,
            rightIndent=20,
            borderWidth=1,
            borderColor=colors.HexColor('#dc2626'),
            borderPadding=8,
            backgroundColor=colors.HexColor('#fef2f2'),
            textColor=colors.HexColor('#dc2626')
        ))
        
        # Dosing table style
        self.styles.add(ParagraphStyle(
            name='DosingHeader',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            alignment=TA_CENTER,
            textColor=colors.white
        ))
    
    def generate_protocol_pdf(self, protocol_data, patient_data=None):
        """Generate comprehensive protocol PDF for medical practitioners"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title=f"PeptideProtocols.ai - {protocol_data.get('protocol_name', 'Medical Protocol')}"
        )
        
        # Build the PDF content
        story = []
        
        # Header section
        self._add_header(story, protocol_data, patient_data)
        
        # Executive Summary
        if 'executive_summary' in protocol_data:
            self._add_executive_summary(story, protocol_data['executive_summary'])
        
        # Patient Information
        if patient_data:
            self._add_patient_section(story, patient_data)
        
        # Protocol Details
        self._add_protocol_details(story, protocol_data)
        
        # Safety Information
        self._add_safety_section(story, protocol_data)
        
        # Monitoring Schedule
        if 'monitoring_schedule' in protocol_data:
            self._add_monitoring_schedule(story, protocol_data['monitoring_schedule'])
        
        # Scientific References
        if 'scientific_references' in protocol_data:
            self._add_references(story, protocol_data['scientific_references'])
        
        # Footer disclaimers
        self._add_disclaimers(story)
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_page_header, onLaterPages=self._add_page_header)
        
        buffer.seek(0)
        return buffer
    
    def _add_header(self, story, protocol_data, patient_data):
        """Add professional medical header"""
        # Title
        title = protocol_data.get('protocol_name', 'Functional Medicine Protocol')
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Protocol metadata table
        metadata = [
            ['Generated By:', 'PeptideProtocols.ai Medical Intelligence System'],
            ['Generated On:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
            ['Protocol ID:', protocol_data.get('protocol_id', 'N/A')],
            ['Evidence Level:', protocol_data.get('evidence_level', 'N/A')]
        ]
        
        if patient_data:
            metadata.extend([
                ['Patient Name:', patient_data.get('name', 'Confidential')],
                ['Patient Age:', f"{patient_data.get('age', 'N/A')} years"],
                ['Patient Gender:', patient_data.get('gender', 'N/A')]
            ])
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb'))
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 30))
    
    def _add_executive_summary(self, story, executive_summary):
        """Add executive summary section"""
        story.append(Paragraph("Executive Summary", self.styles['MedicalHeader']))
        story.append(Paragraph(executive_summary, self.styles['MedicalBody']))
        story.append(Spacer(1, 20))
    
    def _add_patient_section(self, story, patient_data):
        """Add patient-specific information"""
        story.append(Paragraph("Patient Information", self.styles['MedicalHeader']))
        
        # Patient details
        patient_info = f"""
        <b>Chief Complaints:</b> {', '.join(patient_data.get('concerns', []))}<br/>
        <b>Medical History:</b> {patient_data.get('medical_history', 'None reported')}<br/>
        <b>Current Medications:</b> {patient_data.get('medications', 'None reported')}<br/>
        <b>Allergies:</b> {patient_data.get('allergies', 'None known')}<br/>
        <b>Lifestyle Factors:</b> {patient_data.get('lifestyle', 'Standard assessment')}
        """
        
        story.append(Paragraph(patient_info, self.styles['MedicalBody']))
        story.append(Spacer(1, 20))
    
    def _add_protocol_details(self, story, protocol_data):
        """Add comprehensive protocol details"""
        story.append(Paragraph("Detailed Protocol Recommendations", self.styles['MedicalHeader']))
        
        # Parse protocol recommendations
        protocols = protocol_data.get('protocols', [])
        
        for i, protocol in enumerate(protocols, 1):
            # Protocol name
            story.append(Paragraph(f"{i}. {protocol.get('name', 'Unknown Protocol')}", 
                                 self.styles['ProtocolSection']))
            
            # Indication and mechanism
            story.append(Paragraph(f"<b>Clinical Indication:</b> {protocol.get('indication', 'N/A')}", 
                                 self.styles['MedicalBody']))
            story.append(Paragraph(f"<b>Mechanism of Action:</b> {protocol.get('mechanism', 'N/A')}", 
                                 self.styles['MedicalBody']))
            
            # Dosing table
            if 'dosing' in protocol:
                dosing_data = [
                    ['Parameter', 'Specification'],
                    ['Dosage', protocol['dosing'].get('dose', 'N/A')],
                    ['Frequency', protocol['dosing'].get('frequency', 'N/A')],
                    ['Duration', protocol['dosing'].get('duration', 'N/A')],
                    ['Route', protocol['dosing'].get('route', 'N/A')],
                    ['Timing', protocol['dosing'].get('timing', 'N/A')]
                ]
                
                dosing_table = Table(dosing_data, colWidths=[2*inch, 3*inch])
                dosing_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb'))
                ]))
                
                story.append(dosing_table)
            
            # Expected outcomes and timeline
            if 'expected_outcomes' in protocol:
                story.append(Paragraph(f"<b>Expected Outcomes:</b> {protocol['expected_outcomes']}", 
                                     self.styles['MedicalBody']))
            
            if 'timeline' in protocol:
                story.append(Paragraph(f"<b>Expected Timeline:</b> {protocol['timeline']}", 
                                     self.styles['MedicalBody']))
            
            story.append(Spacer(1, 15))
    
    def _add_safety_section(self, story, protocol_data):
        """Add safety information and contraindications"""
        story.append(Paragraph("Safety Information & Contraindications", self.styles['MedicalHeader']))
        
        # Important safety notice
        safety_notice = """
        <b>IMPORTANT MEDICAL NOTICE:</b> This protocol is generated by AI-assisted medical intelligence 
        and must be reviewed by a qualified healthcare provider before implementation. Individual patient 
        factors, contraindications, and drug interactions must be carefully considered.
        """
        story.append(Paragraph(safety_notice, self.styles['ImportantNotice']))
        
        # Protocol-specific safety information
        if 'safety_information' in protocol_data:
            safety_info = protocol_data['safety_information']
            
            if 'contraindications' in safety_info:
                story.append(Paragraph("<b>Contraindications:</b>", self.styles['ProtocolSection']))
                for contraindication in safety_info['contraindications']:
                    story.append(Paragraph(f"• {contraindication}", self.styles['MedicalBody']))
            
            if 'side_effects' in safety_info:
                story.append(Paragraph("<b>Potential Side Effects:</b>", self.styles['ProtocolSection']))
                for side_effect in safety_info['side_effects']:
                    story.append(Paragraph(f"• {side_effect}", self.styles['MedicalBody']))
            
            if 'monitoring' in safety_info:
                story.append(Paragraph("<b>Required Monitoring:</b>", self.styles['ProtocolSection']))
                for monitoring in safety_info['monitoring']:
                    story.append(Paragraph(f"• {monitoring}", self.styles['MedicalBody']))
        
        story.append(Spacer(1, 20))
    
    def _add_monitoring_schedule(self, story, monitoring_data):
        """Add monitoring and follow-up schedule"""
        story.append(Paragraph("Monitoring & Follow-up Schedule", self.styles['MedicalHeader']))
        
        # Create monitoring table
        monitoring_table_data = [['Timeline', 'Monitoring Requirements', 'Expected Outcomes']]
        
        for timepoint, details in monitoring_data.items():
            monitoring_table_data.append([
                timepoint,
                details.get('monitoring', 'Standard assessment'),
                details.get('expected', 'Monitor progress')
            ])
        
        monitoring_table = Table(monitoring_table_data, colWidths=[1.5*inch, 3*inch, 2*inch])
        monitoring_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(monitoring_table)
        story.append(Spacer(1, 20))
    
    def _add_references(self, story, references):
        """Add scientific references section"""
        story.append(Paragraph("Scientific References", self.styles['MedicalHeader']))
        
        for i, reference in enumerate(references, 1):
            story.append(Paragraph(f"{i}. {reference}", self.styles['MedicalBody']))
        
        story.append(Spacer(1, 20))
    
    def _add_disclaimers(self, story):
        """Add medical and legal disclaimers"""
        story.append(PageBreak())
        story.append(Paragraph("Medical Disclaimers & Important Information", self.styles['MedicalHeader']))
        
        disclaimer_text = """
        <b>MEDICAL DISCLAIMER:</b><br/>
        This protocol is generated by PeptideProtocols.ai, an AI-assisted medical intelligence system, 
        and is intended for use by qualified healthcare providers only. This information should not be 
        considered as medical advice and must not be used as a substitute for professional medical judgment.<br/><br/>
        
        <b>PRACTITIONER RESPONSIBILITY:</b><br/>
        The healthcare provider must review all recommendations, verify appropriateness for the individual 
        patient, consider contraindications, assess potential drug interactions, and make final clinical 
        decisions based on their professional judgment and the patient's complete clinical picture.<br/><br/>
        
        <b>PATIENT SAFETY:</b><br/>
        All peptide therapies should be prescribed and monitored by qualified healthcare providers with 
        appropriate training in functional medicine and peptide therapy. Regular monitoring and follow-up 
        are essential for patient safety and treatment optimization.<br/><br/>
        
        <b>QUALITY ASSURANCE:</b><br/>
        This protocol is generated based on current scientific literature and clinical best practices. 
        However, medical knowledge continuously evolves, and practitioners should stay current with the 
        latest research and guidelines.<br/><br/>
        
        <b>REGULATORY COMPLIANCE:</b><br/>
        Practitioners must ensure compliance with all applicable local, state, and federal regulations 
        regarding peptide therapy and compounded medications.
        """
        
        story.append(Paragraph(disclaimer_text, self.styles['MedicalBody']))
    
    def _add_page_header(self, canvas, doc):
        """Add header to each page"""
        canvas.saveState()
        
        # Header line
        canvas.setStrokeColor(colors.HexColor('#2563eb'))
        canvas.setLineWidth(2)
        canvas.line(72, 750, 540, 750)
        
        # Header text
        canvas.setFont('Helvetica-Bold', 12)
        canvas.setFillColor(colors.HexColor('#1f2937'))
        canvas.drawString(72, 760, "PeptideProtocols.ai - Medical Intelligence Platform")
        
        # Page number
        canvas.setFont('Helvetica', 10)
        canvas.setFillColor(colors.HexColor('#6b7280'))
        page_num = f"Page {doc.page}"
        canvas.drawRightString(540, 760, page_num)
        
        # Footer
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#9ca3af'))
        canvas.drawString(72, 50, "Confidential Medical Document - For Healthcare Provider Use Only")
        canvas.drawRightString(540, 50, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        canvas.restoreState()

# Global PDF generator instance
pdf_generator = PeptideProtocolsPDFGenerator()