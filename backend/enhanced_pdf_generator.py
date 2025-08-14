"""
PDF Generation Service - Generate Professional Protocol PDFs
Creates comprehensive protocol PDFs with clinical formatting and branding
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io
from typing import Dict, Any
from datetime import datetime

class ProtocolPDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom PDF styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1e40af')
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=20,
            textColor=colors.HexColor('#374151')
        ))
        
        # Protocol section style
        self.styles.add(ParagraphStyle(
            name='ProtocolSection',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            leftIndent=0.25*inch,
            alignment=TA_JUSTIFY
        ))
        
        # Warning style
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#dc2626'),
            leftIndent=0.25*inch,
            rightIndent=0.25*inch,
            spaceAfter=15
        ))
        
    def generate_protocol_pdf(self, protocol: Dict[str, Any]) -> bytes:
        """Generate a comprehensive protocol PDF"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        # Build PDF content
        story = []
        
        # Header
        story.append(self._create_header(protocol))
        story.append(Spacer(1, 20))
        
        # Protocol overview
        story.append(self._create_overview(protocol))
        story.append(Spacer(1, 15))
        
        # Clinical indications
        story.append(self._create_indications_section(protocol))
        story.append(Spacer(1, 15))
        
        # Mechanism of action
        story.append(self._create_mechanism_section(protocol))
        story.append(Spacer(1, 15))
        
        # Dosing protocols
        dosing_elements = self._create_dosing_section(protocol)
        for element in dosing_elements:
            story.append(element)
        story.append(Spacer(1, 15))
        
        # Administration guidelines
        admin_elements = self._create_administration_section(protocol)
        for element in admin_elements:
            story.append(element)
        story.append(Spacer(1, 15))
        
        # Safety and contraindications
        safety_elements = self._create_safety_section(protocol)
        for element in safety_elements:
            story.append(element)
        story.append(Spacer(1, 15))
        
        # Monitoring requirements
        story.append(self._create_monitoring_section(protocol))
        story.append(Spacer(1, 15))
        
        # References
        story.append(self._create_references_section(protocol))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(self._create_footer())
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
        
    def _create_header(self, protocol: Dict[str, Any]) -> Paragraph:
        """Create PDF header"""
        title = f"Clinical Protocol: {protocol.get('name', 'Unknown Protocol')}"
        subtitle = protocol.get('category', 'Functional Medicine Protocol')
        
        header_text = f"""
        <para align="center">
            <font size="24" color="#1e40af"><b>{title}</b></font><br/>
            <font size="14" color="#6b7280">{subtitle}</font><br/>
            <font size="10" color="#9ca3af">Generated: {datetime.now().strftime('%B %d, %Y')}</font>
        </para>
        """
        return Paragraph(header_text, self.styles['Normal'])
        
    def _create_overview(self, protocol: Dict[str, Any]) -> Paragraph:
        """Create protocol overview section"""
        overview_text = f"""
        <b>Protocol Overview</b><br/><br/>
        <b>Peptide Name:</b> {protocol.get('name', 'N/A')}<br/>
        <b>Category:</b> {protocol.get('category', 'N/A')}<br/>
        <b>Molecular Weight:</b> {protocol.get('molecular_weight', 'N/A')} Da<br/>
        <b>Sequence:</b> {protocol.get('sequence', 'N/A')}<br/><br/>
        <b>Description:</b><br/>
        {protocol.get('description', 'No description available.')}
        """
        return Paragraph(overview_text, self.styles['Normal'])
        
    def _create_indications_section(self, protocol: Dict[str, Any]) -> Paragraph:
        """Create clinical indications section"""
        indications = protocol.get('clinical_indications', [])
        
        indications_text = "<b>Clinical Indications</b><br/><br/>"
        for indication in indications:
            indications_text += f"• {indication}<br/>"
            
        return Paragraph(indications_text, self.styles['Normal'])
        
    def _create_mechanism_section(self, protocol: Dict[str, Any]) -> Paragraph:
        """Create mechanism of action section"""
        mechanism_text = f"""
        <b>Mechanism of Action</b><br/><br/>
        {protocol.get('mechanism_of_action', 'Mechanism of action not specified.')}
        """
        return Paragraph(mechanism_text, self.styles['Normal'])
        
    def _create_dosing_section(self, protocol: Dict[str, Any]) -> list:
        """Create dosing protocols section"""
        elements = []
        elements.append(Paragraph("<b>Dosing Protocols</b>", self.styles['CustomSubtitle']))
        
        dosing = protocol.get('complete_dosing_schedule', {})
        
        if dosing:
            # Create dosing table
            dosing_data = [['Protocol Type', 'Dosage', 'Duration']]
            
            for protocol_type, details in dosing.items():
                protocol_name = protocol_type.replace('_', ' ').title()
                dosing_data.append([protocol_name, details, 'As specified'])
                
            dosing_table = Table(dosing_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
            dosing_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(dosing_table)
        else:
            elements.append(Paragraph("Dosing information not available.", self.styles['Normal']))
            
        return elements
        
    def _create_administration_section(self, protocol: Dict[str, Any]) -> list:
        """Create administration guidelines section"""
        elements = []
        elements.append(Paragraph("<b>Administration Guidelines</b>", self.styles['CustomSubtitle']))
        
        admin = protocol.get('administration_techniques', {})
        
        if admin:
            admin_text = ""
            if 'injection_sites' in admin:
                admin_text += f"<b>Injection Sites:</b> {', '.join(admin['injection_sites'])}<br/><br/>"
            if 'injection_depth' in admin:
                admin_text += f"<b>Injection Depth:</b> {admin['injection_depth']}<br/><br/>"
            if 'preparation' in admin:
                admin_text += f"<b>Preparation:</b> {admin['preparation']}<br/><br/>"
            if 'timing' in admin:
                admin_text += f"<b>Timing:</b> {admin['timing']}<br/><br/>"
                
            elements.append(Paragraph(admin_text, self.styles['Normal']))
        else:
            elements.append(Paragraph("Administration guidelines not specified.", self.styles['Normal']))
            
        return elements
        
    def _create_safety_section(self, protocol: Dict[str, Any]) -> list:
        """Create safety and contraindications section"""
        elements = []
        elements.append(Paragraph("<b>Safety Profile & Contraindications</b>", self.styles['CustomSubtitle']))
        
        safety = protocol.get('safety_profile', {})
        
        # Side effects
        if 'common_side_effects' in safety:
            elements.append(Paragraph("<b>Common Side Effects:</b>", self.styles['Normal']))
            for effect in safety['common_side_effects']:
                if isinstance(effect, dict):
                    effect_text = f"• {effect.get('effect', 'N/A')} ({effect.get('frequency', 'N/A')})"
                else:
                    effect_text = f"• {effect}"
                elements.append(Paragraph(effect_text, self.styles['ProtocolSection']))
                
        # Contraindications
        contraindications = protocol.get('contraindications', [])
        if contraindications:
            elements.append(Paragraph("<b>Contraindications:</b>", self.styles['Normal']))
            for contra in contraindications:
                elements.append(Paragraph(f"• {contra}", self.styles['ProtocolSection']))
                
        # Special warnings
        if 'special_warnings' in safety:
            warning_text = f"<font color='#dc2626'><b>⚠️ Important Warnings:</b><br/>{safety['special_warnings']}</font>"
            elements.append(Paragraph(warning_text, self.styles['Warning']))
            
        return elements
        
    def _create_monitoring_section(self, protocol: Dict[str, Any]) -> Paragraph:
        """Create monitoring requirements section"""
        monitoring = protocol.get('monitoring_requirements', {})
        
        monitoring_text = "<b>Monitoring Requirements</b><br/><br/>"
        
        if monitoring:
            if 'baseline_labs' in monitoring:
                monitoring_text += f"<b>Baseline Labs:</b> {', '.join(monitoring['baseline_labs'])}<br/><br/>"
            if 'follow_up_schedule' in monitoring:
                monitoring_text += f"<b>Follow-up Schedule:</b> {monitoring['follow_up_schedule']}<br/><br/>"
            if 'warning_signs' in monitoring:
                monitoring_text += f"<b>Warning Signs:</b> {', '.join(monitoring['warning_signs'])}<br/><br/>"
        else:
            monitoring_text += "Standard monitoring protocols apply.<br/><br/>"
            
        return Paragraph(monitoring_text, self.styles['Normal'])
        
    def _create_references_section(self, protocol: Dict[str, Any]) -> Paragraph:
        """Create references section"""
        references = protocol.get('references', [])
        
        ref_text = "<b>Clinical References</b><br/><br/>"
        
        if references:
            for i, ref in enumerate(references, 1):
                ref_text += f"{i}. {ref}<br/>"
        else:
            ref_text += "1. Functional Medicine Clinical Protocols Database<br/>"
            ref_text += "2. PubMed Clinical Research Database<br/>"
            ref_text += "3. International Peptide Society Guidelines<br/>"
            
        return Paragraph(ref_text, self.styles['Normal'])
        
    def _create_footer(self) -> Paragraph:
        """Create PDF footer"""
        footer_text = f"""
        <para align="center">
            <font size="10" color="#6b7280">
                <b>PeptideProtocols.ai</b><br/>
                Clinical-Grade Peptide Therapy Protocols<br/>
                For Healthcare Professional Use Only<br/>
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </font>
        </para>
        """
        return Paragraph(footer_text, self.styles['Normal'])

# Global PDF generator instance
pdf_generator = ProtocolPDFGenerator()