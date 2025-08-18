import React from 'react';
import { Clock, Star, Lock } from 'lucide-react';

const ComingSoonBadge = ({ 
  title, 
  description, 
  size = 'default', 
  variant = 'default',
  icon = 'clock',
  className = ''
}) => {
  const icons = {
    clock: Clock,
    star: Star,  
    lock: Lock
  };
  
  const IconComponent = icons[icon] || Clock;
  
  const sizeClasses = {
    small: 'p-3 text-sm',
    default: 'p-4',
    large: 'p-6 text-lg'
  };
  
  const variantClasses = {
    default: 'bg-blue-50 border-blue-200 text-blue-800',
    premium: 'bg-purple-50 border-purple-200 text-purple-800',
    feature: 'bg-green-50 border-green-200 text-green-800',
    lab: 'bg-orange-50 border-orange-200 text-orange-800'
  };

  return (
    <div className={`
      relative border-2 border-dashed rounded-lg 
      ${sizeClasses[size]} 
      ${variantClasses[variant]}
      ${className}
    `}>
      <div className="flex items-center justify-center mb-2">
        <IconComponent className="w-8 h-8 mb-2 opacity-60" />
      </div>
      
      <div className="text-center">
        <h3 className="font-semibold mb-2">{title}</h3>
        <p className="text-sm opacity-80 mb-3">{description}</p>
        
        <div className="inline-flex items-center space-x-2 px-3 py-1 bg-white/50 rounded-full text-xs font-medium">
          <Clock className="w-3 h-3" />
          <span>Coming Soon</span>
        </div>
      </div>
      
      {/* Decorative gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent rounded-lg pointer-events-none" />
    </div>
  );
};

// Preset components for common use cases
export const LabIntegrationComingSoon = ({ className = '' }) => (
  <ComingSoonBadge
    title="Lab Results Integration"
    description="Upload blood work, hormone panels, and genetic data for personalized risk analysis and precision dosing recommendations."
    variant="lab"
    icon="star"
    className={className}
  />
);

export const PatientTrackingComingSoon = ({ className = '' }) => (
  <ComingSoonBadge
    title="Patient Progress Tracking"
    description="Monitor patient symptoms, track biomarkers, and visualize treatment outcomes over time."
    variant="feature"
    icon="clock"
    className={className}
  />
);

export const MessagingComingSoon = ({ className = '' }) => (
  <ComingSoonBadge
    title="Secure Practitioner Messaging"
    description="HIPAA-compliant communication system for patient consultations and protocol adjustments."
    variant="premium"
    icon="lock"
    className={className}
  />
);

export const PDFGenerationComingSoon = ({ className = '' }) => (
  <ComingSoonBadge
    title="Automated PDF Protocols"
    description="Generate comprehensive protocol booklets with detailed instructions, monitoring guidelines, and patient education materials."
    variant="default"
    icon="star"
    className={className}
  />
);

export const EducationCenterComingSoon = ({ className = '' }) => (
  <ComingSoonBadge
    title="Education Center"
    description="Step-by-step injection tutorials, protocol videos, and comprehensive peptide education library."
    variant="feature"
    icon="star"
    className={className}
  />
);

export const DosingCalculatorComingSoon = ({ className = '' }) => (
  <ComingSoonBadge
    title="Precision Dosing Calculator"
    description="Lab-based dosing optimization with real-time adjustments based on biomarkers and patient response."
    variant="lab"
    icon="star"
    className={className}
  />
);

export const NotificationSystemComingSoon = ({ className = '' }) => (
  <ComingSoonBadge
    title="Notification & Alert System"
    description="Real-time alerts for patient updates, protocol milestones, and important safety notifications."
    variant="premium"
    icon="clock"
    className={className}
  />
);

export const StackingCalculatorComingSoon = ({ className = '' }) => (
  <ComingSoonBadge
    title="Peptide Stacking Optimizer"
    description="Interactive calculator for optimal peptide combinations with timing, dosing, and synergy analysis."
    variant="feature"
    icon="star"
    className={className}
  />
);

export default ComingSoonBadge;