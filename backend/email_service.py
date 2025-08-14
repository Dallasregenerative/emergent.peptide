"""
Email Integration Service for PeptideProtocols.ai
Professional medical communication system with protocol delivery and follow-up
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr, formatdate
from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from pydantic_settings import BaseSettings
from jinja2 import Environment, FileSystemLoader, Template
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime, timedelta
import json

class EmailSettings(BaseSettings):
    """Email configuration settings"""
    MAIL_USERNAME: str = os.environ.get('MAIL_USERNAME', 'noreply@peptideprotocols.ai')
    MAIL_PASSWORD: str = os.environ.get('MAIL_PASSWORD', '')
    MAIL_FROM: str = os.environ.get('MAIL_FROM', 'noreply@peptideprotocols.ai')
    MAIL_FROM_NAME: str = os.environ.get('MAIL_FROM_NAME', 'PeptideProtocols.ai')
    MAIL_PORT: int = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_SERVER: str = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

class EmailService:
    """
    Professional email service for medical communications
    """
    
    def __init__(self):
        self.settings = EmailSettings()
        self.conf = ConnectionConfig(
            MAIL_USERNAME=self.settings.MAIL_USERNAME,
            MAIL_PASSWORD=self.settings.MAIL_PASSWORD,
            MAIL_FROM=self.settings.MAIL_FROM,
            MAIL_PORT=self.settings.MAIL_PORT,
            MAIL_SERVER=self.settings.MAIL_SERVER,
            MAIL_STARTTLS=self.settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=self.settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=self.settings.USE_CREDENTIALS,
            VALIDATE_CERTS=self.settings.VALIDATE_CERTS
        )
        self.fastmail = FastMail(self.conf)
        self.template_env = Environment(
            loader=FileSystemLoader('email_templates') if os.path.exists('email_templates') else None
        )
    
    async def send_protocol_email(
        self,
        recipient_email: str,
        recipient_name: str,
        protocol_data: Dict,
        practitioner_data: Optional[Dict] = None,
        attach_pdf: Optional[bytes] = None
    ) -> bool:
        """
        Send comprehensive protocol email to patient/practitioner
        """
        try:
            # Generate HTML content
            html_content = self._generate_protocol_email_html(
                protocol_data, 
                recipient_name, 
                practitioner_data
            )
            
            # Generate plain text version
            plain_content = self._generate_protocol_email_text(
                protocol_data, 
                recipient_name, 
                practitioner_data
            )
            
            # Create message
            message = MessageSchema(
                subject=f"Your Personalized Functional Medicine Protocol - {protocol_data.get('protocol_name', 'Custom Protocol')}",
                recipients=[recipient_email],
                body=plain_content,
                html=html_content,
                subtype=MessageType.html,
                attachments=[]
            )
            
            # Add PDF attachment if provided
            if attach_pdf:
                message.attachments.append({
                    "file": attach_pdf,
                    "filename": f"protocol_{datetime.now().strftime('%Y%m%d')}.pdf",
                    "content_type": "application/pdf"
                })
            
            # Send email
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Error sending protocol email: {str(e)}")
            return False
    
    async def send_follow_up_reminder(
        self,
        recipient_email: str,
        recipient_name: str,
        protocol_name: str,
        days_since_start: int,
        next_milestone: Optional[str] = None
    ) -> bool:
        """
        Send automated follow-up reminder emails
        """
        try:
            # Determine follow-up type based on timeline
            if days_since_start <= 14:
                follow_up_type = "initial"
                subject = "How are you feeling? - 2 Week Protocol Check-in"
            elif days_since_start <= 30:
                follow_up_type = "monthly"
                subject = "Monthly Progress Check - Share Your Results"
            elif days_since_start <= 90:
                follow_up_type = "quarterly"
                subject = "3-Month Protocol Review - Time for Optimization"
            else:
                follow_up_type = "long_term"
                subject = "Long-term Follow-up - Maintaining Your Health Journey"
            
            html_content = self._generate_follow_up_email_html(
                recipient_name,
                protocol_name,
                days_since_start,
                follow_up_type,
                next_milestone
            )
            
            plain_content = self._generate_follow_up_email_text(
                recipient_name,
                protocol_name,
                days_since_start,
                follow_up_type,
                next_milestone
            )
            
            message = MessageSchema(
                subject=subject,
                recipients=[recipient_email],
                body=plain_content,
                html=html_content,
                subtype=MessageType.html
            )
            
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Error sending follow-up email: {str(e)}")
            return False
    
    async def send_milestone_achievement(
        self,
        recipient_email: str,
        recipient_name: str,
        milestone_name: str,
        milestone_description: str,
        progress_summary: Dict
    ) -> bool:
        """
        Send congratulatory email for milestone achievements
        """
        try:
            html_content = self._generate_milestone_email_html(
                recipient_name,
                milestone_name,
                milestone_description,
                progress_summary
            )
            
            plain_content = self._generate_milestone_email_text(
                recipient_name,
                milestone_name,
                milestone_description,
                progress_summary
            )
            
            message = MessageSchema(
                subject=f"🎉 Congratulations! You've achieved: {milestone_name}",
                recipients=[recipient_email],
                body=plain_content,
                html=html_content,
                subtype=MessageType.html
            )
            
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Error sending milestone email: {str(e)}")
            return False
    
    async def send_practitioner_notification(
        self,
        practitioner_email: str,
        practitioner_name: str,
        notification_type: str,
        patient_data: Dict,
        details: Dict
    ) -> bool:
        """
        Send notifications to practitioners about patient progress or concerns
        """
        try:
            subject_map = {
                "new_patient": f"New Patient Assessment - {patient_data.get('name', 'Unknown')}",
                "milestone_achieved": f"Patient Milestone - {patient_data.get('name', 'Unknown')} achieved {details.get('milestone')}",
                "side_effect_report": f"URGENT: Side Effect Report - {patient_data.get('name', 'Unknown')}",
                "poor_response": f"Protocol Review Needed - {patient_data.get('name', 'Unknown')}"
            }
            
            html_content = self._generate_practitioner_notification_html(
                practitioner_name,
                notification_type,
                patient_data,
                details
            )
            
            plain_content = self._generate_practitioner_notification_text(
                practitioner_name,
                notification_type,
                patient_data,
                details
            )
            
            message = MessageSchema(
                subject=subject_map.get(notification_type, "Patient Update"),
                recipients=[practitioner_email],
                body=plain_content,
                html=html_content,
                subtype=MessageType.html
            )
            
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Error sending practitioner notification: {str(e)}")
            return False
    
    def _generate_protocol_email_html(
        self, 
        protocol_data: Dict, 
        recipient_name: str, 
        practitioner_data: Optional[Dict]
    ) -> str:
        """Generate HTML email for protocol delivery"""
        
        practitioner_section = ""
        if practitioner_data:
            practitioner_section = f"""
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <h3 style="color: #1f2937; margin-bottom: 10px;">Your Healthcare Provider</h3>
                <p><strong>{practitioner_data.get('name', 'Healthcare Provider')}</strong></p>
                <p>{practitioner_data.get('title', 'Functional Medicine Practitioner')}</p>
                <p>Contact: {practitioner_data.get('contact', 'Through PeptideProtocols.ai')}</p>
            </div>
            """
        
        protocols_html = ""
        for i, protocol in enumerate(protocol_data.get('protocols', []), 1):
            protocols_html += f"""
            <div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: #2563eb; margin-bottom: 15px;">{i}. {protocol.get('name', 'Protocol')}</h3>
                <p><strong>Clinical Indication:</strong> {protocol.get('indication', 'N/A')}</p>
                <p><strong>Mechanism of Action:</strong> {protocol.get('mechanism', 'N/A')}</p>
                
                {f'''
                <div style="background-color: #fef3c7; padding: 15px; border-radius: 6px; margin: 15px 0;">
                    <h4 style="color: #92400e; margin-bottom: 10px;">Dosing Schedule</h4>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li><strong>Dosage:</strong> {protocol.get('dosing', {}).get('dose', 'N/A')}</li>
                        <li><strong>Frequency:</strong> {protocol.get('dosing', {}).get('frequency', 'N/A')}</li>
                        <li><strong>Duration:</strong> {protocol.get('dosing', {}).get('duration', 'N/A')}</li>
                        <li><strong>Route:</strong> {protocol.get('dosing', {}).get('route', 'N/A')}</li>
                        <li><strong>Timing:</strong> {protocol.get('dosing', {}).get('timing', 'N/A')}</li>
                    </ul>
                </div>
                ''' if 'dosing' in protocol else ''}
                
                <p><strong>Expected Outcomes:</strong> {protocol.get('expected_outcomes', 'Varies by individual')}</p>
                <p><strong>Timeline:</strong> {protocol.get('timeline', 'Monitor progress closely')}</p>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Your Personalized Protocol - PeptideProtocols.ai</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1f2937; max-width: 800px; margin: 0 auto; padding: 20px;">
            
            <div style="text-align: center; border-bottom: 3px solid #2563eb; padding-bottom: 20px; margin-bottom: 30px;">
                <h1 style="color: #2563eb; margin-bottom: 10px;">🧬 PeptideProtocols.ai</h1>
                <p style="color: #6b7280; font-size: 16px;">Medical Intelligence Platform</p>
            </div>
            
            <h2 style="color: #1f2937;">Dear {recipient_name},</h2>
            
            <p style="font-size: 16px; line-height: 1.8;">
                Your personalized functional medicine protocol has been generated using our world-class medical intelligence system. 
                This evidence-based approach has been tailored specifically for your health goals and medical profile.
            </p>
            
            {practitioner_section}
            
            <div style="background-color: #dbeafe; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <h3 style="color: #1e40af; margin-bottom: 15px;">📋 Protocol Summary</h3>
                <p><strong>Protocol Name:</strong> {protocol_data.get('protocol_name', 'Custom Functional Medicine Protocol')}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
                <p><strong>Evidence Level:</strong> {protocol_data.get('evidence_level', 'Clinical Guidelines')}</p>
                <p><strong>Protocol ID:</strong> {protocol_data.get('protocol_id', 'N/A')}</p>
            </div>
            
            <h3 style="color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px;">Detailed Recommendations</h3>
            {protocols_html}
            
            <div style="background-color: #fef2f2; padding: 20px; border-radius: 8px; border-left: 4px solid #dc2626; margin: 30px 0;">
                <h3 style="color: #dc2626; margin-bottom: 15px;">⚠️ Important Safety Information</h3>
                <p><strong>This protocol must be reviewed and approved by your healthcare provider before implementation.</strong></p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>All recommendations require medical supervision</li>
                    <li>Individual contraindications must be assessed</li>
                    <li>Drug interactions should be evaluated</li>
                    <li>Regular monitoring and follow-up are essential</li>
                </ul>
            </div>
            
            <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <h3 style="color: #15803d; margin-bottom: 15px;">📈 Next Steps</h3>
                <ol style="margin: 0; padding-left: 20px;">
                    <li>Review this protocol with your healthcare provider</li>
                    <li>Discuss any questions or concerns</li>
                    <li>Begin implementation under medical supervision</li>
                    <li>Track your progress and report outcomes</li>
                    <li>Schedule follow-up appointments as recommended</li>
                </ol>
            </div>
            
            <div style="text-align: center; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 40px;">
                <p style="color: #6b7280; font-size: 14px;">
                    This protocol was generated by PeptideProtocols.ai Medical Intelligence Platform<br>
                    For support, visit our platform or contact your healthcare provider<br>
                    <em>Confidential Medical Information - For Patient and Provider Use Only</em>
                </p>
            </div>
            
        </body>
        </html>
        """
    
    def _generate_protocol_email_text(
        self, 
        protocol_data: Dict, 
        recipient_name: str, 
        practitioner_data: Optional[Dict]
    ) -> str:
        """Generate plain text version of protocol email"""
        
        practitioner_text = ""
        if practitioner_data:
            practitioner_text = f"""
Your Healthcare Provider:
{practitioner_data.get('name', 'Healthcare Provider')}
{practitioner_data.get('title', 'Functional Medicine Practitioner')}
Contact: {practitioner_data.get('contact', 'Through PeptideProtocols.ai')}

"""
        
        protocols_text = ""
        for i, protocol in enumerate(protocol_data.get('protocols', []), 1):
            dosing_text = ""
            if 'dosing' in protocol:
                dosing_text = f"""
Dosing Schedule:
- Dosage: {protocol.get('dosing', {}).get('dose', 'N/A')}
- Frequency: {protocol.get('dosing', {}).get('frequency', 'N/A')}
- Duration: {protocol.get('dosing', {}).get('duration', 'N/A')}
- Route: {protocol.get('dosing', {}).get('route', 'N/A')}
- Timing: {protocol.get('dosing', {}).get('timing', 'N/A')}
"""
            
            protocols_text += f"""
{i}. {protocol.get('name', 'Protocol')}
Clinical Indication: {protocol.get('indication', 'N/A')}
Mechanism of Action: {protocol.get('mechanism', 'N/A')}
{dosing_text}
Expected Outcomes: {protocol.get('expected_outcomes', 'Varies by individual')}
Timeline: {protocol.get('timeline', 'Monitor progress closely')}

"""
        
        return f"""
PEPTIDEPROTOCOLS.AI - PERSONALIZED MEDICAL PROTOCOL
==================================================

Dear {recipient_name},

Your personalized functional medicine protocol has been generated using our world-class medical intelligence system. This evidence-based approach has been tailored specifically for your health goals and medical profile.

{practitioner_text}

PROTOCOL SUMMARY:
Protocol Name: {protocol_data.get('protocol_name', 'Custom Functional Medicine Protocol')}
Generated: {datetime.now().strftime('%B %d, %Y')}
Evidence Level: {protocol_data.get('evidence_level', 'Clinical Guidelines')}
Protocol ID: {protocol_data.get('protocol_id', 'N/A')}

DETAILED RECOMMENDATIONS:
{protocols_text}

IMPORTANT SAFETY INFORMATION:
⚠️  This protocol must be reviewed and approved by your healthcare provider before implementation.
- All recommendations require medical supervision
- Individual contraindications must be assessed
- Drug interactions should be evaluated
- Regular monitoring and follow-up are essential

NEXT STEPS:
1. Review this protocol with your healthcare provider
2. Discuss any questions or concerns
3. Begin implementation under medical supervision
4. Track your progress and report outcomes
5. Schedule follow-up appointments as recommended

---
This protocol was generated by PeptideProtocols.ai Medical Intelligence Platform
For support, visit our platform or contact your healthcare provider
Confidential Medical Information - For Patient and Provider Use Only
"""
    
    def _generate_follow_up_email_html(
        self, 
        recipient_name: str, 
        protocol_name: str, 
        days_since_start: int,
        follow_up_type: str,
        next_milestone: Optional[str]
    ) -> str:
        """Generate HTML follow-up email"""
        
        # Customize content based on follow-up type
        if follow_up_type == "initial":
            main_message = """
            <p>You've been on your protocol for 2 weeks now, and we'd love to hear how you're feeling! 
            This is typically when patients start noticing their first improvements.</p>
            
            <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #15803d;">What to expect at 2 weeks:</h3>
                <ul>
                    <li>Initial energy improvements</li>
                    <li>Better sleep quality</li>
                    <li>Reduced inflammation symptoms</li>
                    <li>Improved tolerance to protocols</li>
                </ul>
            </div>
            """
        elif follow_up_type == "monthly":
            main_message = """
            <p>You've completed one full month on your protocol - congratulations on your commitment to better health! 
            This is an important milestone when we typically see significant improvements.</p>
            
            <div style="background-color: #dbeafe; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #1e40af;">Expected improvements at 1 month:</h3>
                <ul>
                    <li>Sustained energy throughout the day</li>
                    <li>Noticeable weight or body composition changes</li>
                    <li>Improved cognitive function</li>
                    <li>Better stress management</li>
                </ul>
            </div>
            """
        else:
            main_message = f"""
            <p>You've been on your protocol for {days_since_start} days, and your dedication to your health journey 
            is admirable. Long-term consistency is key to achieving optimal results.</p>
            """
        
        milestone_section = ""
        if next_milestone:
            milestone_section = f"""
            <div style="background-color: #fef3c7; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #92400e;">🎯 Next Milestone</h3>
                <p>You're approaching: <strong>{next_milestone}</strong></p>
                <p>Keep up the great work - you're making excellent progress!</p>
            </div>
            """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Protocol Follow-up - PeptideProtocols.ai</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1f2937; max-width: 800px; margin: 0 auto; padding: 20px;">
            
            <div style="text-align: center; border-bottom: 3px solid #2563eb; padding-bottom: 20px; margin-bottom: 30px;">
                <h1 style="color: #2563eb; margin-bottom: 10px;">🧬 PeptideProtocols.ai</h1>
                <p style="color: #6b7280; font-size: 16px;">How are you feeling?</p>
            </div>
            
            <h2 style="color: #1f2937;">Hi {recipient_name}!</h2>
            
            {main_message}
            
            {milestone_section}
            
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #1f2937;">📝 Share Your Progress</h3>
                <p>We'd love to hear about your experience so far. Your feedback helps us improve protocols for everyone:</p>
                <ul>
                    <li>How are your energy levels?</li>
                    <li>Are you experiencing any side effects?</li>
                    <li>Have you noticed improvements in your main concerns?</li>
                    <li>Any questions about your current protocol?</li>
                </ul>
                
                <div style="text-align: center; margin-top: 20px;">
                    <a href="https://peptideprotocols.ai/feedback" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">Share Your Progress</a>
                </div>
            </div>
            
            <div style="text-align: center; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 40px;">
                <p style="color: #6b7280; font-size: 14px;">
                    This follow-up was sent by PeptideProtocols.ai<br>
                    Your health journey matters to us<br>
                    <em>Questions? Chat with Dr. Peptide on our platform</em>
                </p>
            </div>
            
        </body>
        </html>
        """
    
    def _generate_follow_up_email_text(
        self, 
        recipient_name: str, 
        protocol_name: str, 
        days_since_start: int,
        follow_up_type: str,
        next_milestone: Optional[str]
    ) -> str:
        """Generate plain text follow-up email"""
        
        milestone_text = ""
        if next_milestone:
            milestone_text = f"""
NEXT MILESTONE:
🎯 You're approaching: {next_milestone}
Keep up the great work - you're making excellent progress!

"""
        
        return f"""
PEPTIDEPROTOCOLS.AI - PROTOCOL FOLLOW-UP
========================================

Hi {recipient_name}!

You've been on your {protocol_name} protocol for {days_since_start} days, and we'd love to hear how you're feeling!

{milestone_text}

SHARE YOUR PROGRESS:
We'd love to hear about your experience so far. Your feedback helps us improve protocols for everyone:

- How are your energy levels?
- Are you experiencing any side effects?
- Have you noticed improvements in your main concerns?
- Any questions about your current protocol?

Visit https://peptideprotocols.ai/feedback to share your progress.

---
This follow-up was sent by PeptideProtocols.ai
Your health journey matters to us
Questions? Chat with Dr. Peptide on our platform
"""
    
    def _generate_milestone_email_html(
        self, 
        recipient_name: str, 
        milestone_name: str,
        milestone_description: str, 
        progress_summary: Dict
    ) -> str:
        """Generate milestone achievement email HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Milestone Achievement - PeptideProtocols.ai</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1f2937; max-width: 800px; margin: 0 auto; padding: 20px;">
            
            <div style="text-align: center; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 40px 20px; border-radius: 12px; margin-bottom: 30px;">
                <h1 style="margin-bottom: 20px; font-size: 28px;">🎉 Congratulations!</h1>
                <h2 style="margin-bottom: 10px; font-size: 22px;">{milestone_name}</h2>
                <p style="font-size: 18px; margin: 0;">{milestone_description}</p>
            </div>
            
            <h2 style="color: #1f2937;">Dear {recipient_name},</h2>
            
            <p style="font-size: 16px; line-height: 1.8;">
                We're thrilled to celebrate this important milestone with you! Your dedication to your health journey 
                has paid off, and this achievement represents real progress toward your wellness goals.
            </p>
            
            <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin: 20px 0;">
                <h3 style="color: #15803d; margin-bottom: 15px;">📈 Your Progress Summary</h3>
                <p><strong>Overall Improvement:</strong> {progress_summary.get('overall_improvement', 'Excellent progress')}</p>
                <p><strong>Key Achievements:</strong></p>
                <ul>
                    {chr(10).join(f'<li>{achievement}</li>' for achievement in progress_summary.get('achievements', ['Milestone completed successfully']))}
                </ul>
            </div>
            
            <div style="background-color: #dbeafe; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #1e40af;">🎯 What's Next?</h3>
                <p>Building on this success, here are your next steps:</p>
                <ul>
                    <li>Continue your current protocol to maintain progress</li>
                    <li>Share this achievement with your healthcare provider</li>
                    <li>Consider advanced optimization strategies</li>
                    <li>Set new health goals to work toward</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://peptideprotocols.ai/dashboard" style="background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">View Your Progress Dashboard</a>
            </div>
            
            <div style="text-align: center; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 40px;">
                <p style="color: #6b7280; font-size: 14px;">
                    Celebrating your success with PeptideProtocols.ai<br>
                    Your health transformation inspires us<br>
                    <em>Keep up the amazing work!</em>
                </p>
            </div>
            
        </body>
        </html>
        """
    
    def _generate_milestone_email_text(
        self, 
        recipient_name: str, 
        milestone_name: str,
        milestone_description: str, 
        progress_summary: Dict
    ) -> str:
        """Generate milestone achievement email text"""
        return f"""
🎉 CONGRATULATIONS - MILESTONE ACHIEVED!
=======================================

{milestone_name}
{milestone_description}

Dear {recipient_name},

We're thrilled to celebrate this important milestone with you! Your dedication to your health journey has paid off, and this achievement represents real progress toward your wellness goals.

YOUR PROGRESS SUMMARY:
Overall Improvement: {progress_summary.get('overall_improvement', 'Excellent progress')}

Key Achievements:
{chr(10).join(f'- {achievement}' for achievement in progress_summary.get('achievements', ['Milestone completed successfully']))}

WHAT'S NEXT:
Building on this success, here are your next steps:
- Continue your current protocol to maintain progress
- Share this achievement with your healthcare provider
- Consider advanced optimization strategies
- Set new health goals to work toward

Visit https://peptideprotocols.ai/dashboard to view your complete progress.

---
Celebrating your success with PeptideProtocols.ai
Your health transformation inspires us
Keep up the amazing work!
"""
    
    def _generate_practitioner_notification_html(
        self,
        practitioner_name: str,
        notification_type: str,
        patient_data: Dict,
        details: Dict
    ) -> str:
        """Generate practitioner notification email HTML"""
        
        # Customize based on notification type
        if notification_type == "side_effect_report":
            urgency_style = "background-color: #fef2f2; border-left: 4px solid #dc2626;"
            urgency_text = "URGENT ATTENTION REQUIRED"
        elif notification_type == "poor_response":
            urgency_style = "background-color: #fef3c7; border-left: 4px solid #f59e0b;"
            urgency_text = "PROTOCOL REVIEW RECOMMENDED"
        else:
            urgency_style = "background-color: #f0fdf4; border-left: 4px solid #10b981;"
            urgency_text = "PATIENT UPDATE"
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Practitioner Notification - PeptideProtocols.ai</title>
        </head>
        <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1f2937; max-width: 800px; margin: 0 auto; padding: 20px;">
            
            <div style="{urgency_style} padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <h2 style="margin-bottom: 10px;">{urgency_text}</h2>
                <p style="margin: 0;">Patient: {patient_data.get('name', 'Unknown')} - Notification Type: {notification_type.replace('_', ' ').title()}</p>
            </div>
            
            <h2>Dear Dr. {practitioner_name},</h2>
            
            <p>This is an automated notification from PeptideProtocols.ai regarding one of your patients.</p>
            
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>Patient Information</h3>
                <p><strong>Name:</strong> {patient_data.get('name', 'Unknown')}</p>
                <p><strong>Age:</strong> {patient_data.get('age', 'Unknown')}</p>
                <p><strong>Protocol:</strong> {patient_data.get('protocol', 'N/A')}</p>
                <p><strong>Days on Protocol:</strong> {patient_data.get('days_on_protocol', 'Unknown')}</p>
            </div>
            
            <div style="background-color: #dbeafe; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3>Notification Details</h3>
                <p>{details.get('description', 'No additional details available.')}</p>
                
                {f'<p><strong>Reported Issues:</strong> {details.get("issues", "None specified")}</p>' if 'issues' in details else ''}
                {f'<p><strong>Milestone Achieved:</strong> {details.get("milestone", "N/A")}</p>' if 'milestone' in details else ''}
                {f'<p><strong>Progress Score:</strong> {details.get("progress_score", "N/A")}</p>' if 'progress_score' in details else ''}
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://peptideprotocols.ai/practitioner/dashboard" style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">View Patient Dashboard</a>
            </div>
            
            <div style="text-align: center; border-top: 1px solid #e5e7eb; padding-top: 20px; margin-top: 40px;">
                <p style="color: #6b7280; font-size: 14px;">
                    This notification was sent by PeptideProtocols.ai<br>
                    Professional medical communication system<br>
                    <em>For healthcare provider use only</em>
                </p>
            </div>
            
        </body>
        </html>
        """
    
    def _generate_practitioner_notification_text(
        self,
        practitioner_name: str,
        notification_type: str,
        patient_data: Dict,
        details: Dict
    ) -> str:
        """Generate practitioner notification email text"""
        
        return f"""
PRACTITIONER NOTIFICATION - PEPTIDEPROTOCOLS.AI
===============================================

Dear Dr. {practitioner_name},

This is an automated notification regarding one of your patients.

PATIENT INFORMATION:
Name: {patient_data.get('name', 'Unknown')}
Age: {patient_data.get('age', 'Unknown')}
Protocol: {patient_data.get('protocol', 'N/A')}
Days on Protocol: {patient_data.get('days_on_protocol', 'Unknown')}

NOTIFICATION TYPE: {notification_type.replace('_', ' ').title()}

DETAILS:
{details.get('description', 'No additional details available.')}

{f'Reported Issues: {details.get("issues", "None specified")}' if 'issues' in details else ''}
{f'Milestone Achieved: {details.get("milestone", "N/A")}' if 'milestone' in details else ''}
{f'Progress Score: {details.get("progress_score", "N/A")}' if 'progress_score' in details else ''}

Visit https://peptideprotocols.ai/practitioner/dashboard to view complete patient information.

---
This notification was sent by PeptideProtocols.ai
Professional medical communication system
For healthcare provider use only
"""
    
    def get_service_status(self) -> Dict[str, Any]:
        """
        Get email service configuration and status
        """
        try:
            status = {
                "configured": bool(self.settings.MAIL_USERNAME and self.settings.MAIL_PASSWORD),
                "mail_server": self.settings.MAIL_SERVER,
                "mail_port": self.settings.MAIL_PORT,
                "mail_from": self.settings.MAIL_FROM,
                "ssl_enabled": self.settings.MAIL_STARTTLS,
                "service_available": True
            }
            
            # Test basic configuration
            if not self.settings.MAIL_USERNAME:
                status["service_available"] = False
                status["error"] = "Mail username not configured"
            elif not self.settings.MAIL_PASSWORD:
                status["service_available"] = False
                status["error"] = "Mail password not configured"
            
            return status
            
        except Exception as e:
            return {
                "configured": False,
                "service_available": False,
                "error": str(e)
            }

# Global email service instance
email_service = EmailService()