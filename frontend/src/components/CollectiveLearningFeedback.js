import React, { useState } from 'react';
import { Star } from 'lucide-react';

const CollectiveLearningFeedback = ({ protocolData, onFeedbackSubmit, onAnonymizationComplete }) => {
  const [feedbackStep, setFeedbackStep] = useState(1);
  const [rating, setRating] = useState(0);
  const [accuracyAssessment, setAccuracyAssessment] = useState('');
  const [inaccuracies, setInaccuracies] = useState(['']);
  const [improvements, setImprovements] = useState([{ type: '', description: '' }]);
  const [additionalNotes, setAdditionalNotes] = useState('');
  const [agreeToAnonymize, setAgreeToAnonymize] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [protocolNumber, setProtocolNumber] = useState('');

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  const accuracyOptions = [
    { value: 'highly_accurate', label: 'Highly Accurate' },
    { value: 'mostly_accurate', label: 'Mostly Accurate' },
    { value: 'partially_accurate', label: 'Partially Accurate' },
    { value: 'needs_improvement', label: 'Needs Improvement' }
  ];

  const improvementTypes = [
    { value: 'dosing_adjustment', label: 'Dosing Adjustment' },
    { value: 'safety_concern', label: 'Safety Concern' },
    { value: 'efficacy_improvement', label: 'Efficacy Improvement' },
    { value: 'contraindication_missing', label: 'Missing Contraindication' },
    { value: 'stacking_suggestion', label: 'Peptide Stacking Suggestion' },
    { value: 'monitoring_addition', label: 'Additional Monitoring' },
    { value: 'general_improvement', label: 'General Improvement' }
  ];

  const addInaccuracy = () => {
    setInaccuracies([...inaccuracies, '']);
  };

  const removeInaccuracy = (index) => {
    const newInaccuracies = inaccuracies.filter((_, i) => i !== index);
    setInaccuracies(newInaccuracies.length > 0 ? newInaccuracies : ['']);
  };

  const updateInaccuracy = (index, value) => {
    const newInaccuracies = [...inaccuracies];
    newInaccuracies[index] = value;
    setInaccuracies(newInaccuracies);
  };

  const addImprovement = () => {
    setImprovements([...improvements, { type: '', description: '' }]);
  };

  const removeImprovement = (index) => {
    const newImprovements = improvements.filter((_, i) => i !== index);
    setImprovements(newImprovements.length > 0 ? newImprovements : [{ type: '', description: '' }]);
  };

  const updateImprovement = (index, field, value) => {
    const newImprovements = [...improvements];
    newImprovements[index][field] = value;
    setImprovements(newImprovements);
  };

  const submitFeedbackOnly = async () => {
    setIsSubmitting(true);

    try {
      const response = await fetch(`${backendUrl}/api/collective-learning/protocol-feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          protocol_rating: rating,
          accuracy_assessment: accuracyAssessment,
          identified_inaccuracies: inaccuracies.filter(item => item.trim() !== ''),
          suggested_improvements: improvements.filter(item => item.type && item.description),
          additional_notes: additionalNotes,
          practitioner_id: 'demo-practitioner'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit feedback');
      }

      const data = await response.json();
      onFeedbackSubmit && onFeedbackSubmit(data);
      setFeedbackStep(4); // Show completion

    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const anonymizeAndStore = async () => {
    setIsSubmitting(true);

    try {
      // First submit feedback
      const feedbackResponse = await fetch(`${backendUrl}/api/collective-learning/protocol-feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          protocol_rating: rating,
          accuracy_assessment: accuracyAssessment,
          identified_inaccuracies: inaccuracies.filter(item => item.trim() !== ''),
          suggested_improvements: improvements.filter(item => item.type && item.description),
          additional_notes: additionalNotes,
          practitioner_id: 'demo-practitioner'
        }),
      });

      if (!feedbackResponse.ok) {
        throw new Error('Failed to submit feedback');
      }

      const feedbackData = await feedbackResponse.json();

      // Then anonymize and store protocol
      const anonymizeResponse = await fetch(`${backendUrl}/api/collective-learning/anonymize-protocol`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          protocol_data: protocolData.protocol,
          patient_data: protocolData.assessment_data,
          practitioner_feedback: feedbackData.feedback
        }),
      });

      if (!anonymizeResponse.ok) {
        throw new Error('Failed to anonymize protocol');
      }

      const anonymizeData = await anonymizeResponse.json();
      setProtocolNumber(anonymizeData.protocol_number);
      
      onAnonymizationComplete && onAnonymizationComplete({
        protocolNumber: anonymizeData.protocol_number,
        feedback: feedbackData.feedback
      });
      
      setFeedbackStep(5); // Show anonymization completion

    } catch (error) {
      console.error('Error in anonymization process:', error);
      alert('Failed to complete anonymization. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStarRating = () => (
    <div className="flex items-center space-x-2">
      <span className="text-sm font-medium text-gray-700">Rate this protocol:</span>
      <div className="flex space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => setRating(star)}
            className={`p-1 rounded transition-colors ${
              star <= rating ? 'text-yellow-500' : 'text-gray-300 hover:text-yellow-400'
            }`}
          >
            <Star className="w-6 h-6 fill-current" />
          </button>
        ))}
      </div>
      <span className="text-sm text-gray-600">
        {rating > 0 ? `${rating}/5 stars` : 'Click to rate'}
      </span>
    </div>
  );

  if (feedbackStep === 1) {
    return (
      <div className="collective-learning-feedback bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Protocol Feedback & Learning</h2>
          <p className="text-gray-600">Help improve our collective knowledge by providing feedback on this protocol.</p>
        </div>

        <div className="space-y-6">
          {/* Rating Section */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Overall Protocol Rating</h3>
            {renderStarRating()}
          </div>

          {/* Accuracy Assessment */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Accuracy Assessment</h3>
            <div className="grid grid-cols-2 gap-3">
              {accuracyOptions.map((option) => (
                <label key={option.value} className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="radio"
                    name="accuracy"
                    value={option.value}
                    checked={accuracyAssessment === option.value}
                    onChange={(e) => setAccuracyAssessment(e.target.value)}
                    className="mr-3"
                  />
                  <span className="text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4 pt-4">
            <button
              onClick={() => setFeedbackStep(2)}
              disabled={!rating || !accuracyAssessment}
              className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
            >
              Continue to Detailed Feedback
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (feedbackStep === 2) {
    return (
      <div className="collective-learning-feedback bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Detailed Feedback</h2>
          <p className="text-gray-600">Identify any inaccuracies and suggest improvements.</p>
        </div>

        <div className="space-y-6">
          {/* Identified Inaccuracies */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Identified Inaccuracies</h3>
            <div className="space-y-3">
              {inaccuracies.map((inaccuracy, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={inaccuracy}
                    onChange={(e) => updateInaccuracy(index, e.target.value)}
                    placeholder="Describe any inaccuracy you identified..."
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {inaccuracies.length > 1 && (
                    <button
                      onClick={() => removeInaccuracy(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                onClick={addInaccuracy}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                + Add Another Inaccuracy
              </button>
            </div>
          </div>

          {/* Suggested Improvements */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Suggested Improvements</h3>
            <div className="space-y-4">
              {improvements.map((improvement, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex items-center space-x-2 mb-3">
                    <select
                      value={improvement.type}
                      onChange={(e) => updateImprovement(index, 'type', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="">Select improvement type...</option>
                      {improvementTypes.map((type) => (
                        <option key={type.value} value={type.value}>
                          {type.label}
                        </option>
                      ))}
                    </select>
                    {improvements.length > 1 && (
                      <button
                        onClick={() => removeImprovement(index)}
                        className="px-3 py-2 text-red-600 hover:text-red-800"
                      >
                        Remove
                      </button>
                    )}
                  </div>
                  <textarea
                    value={improvement.description}
                    onChange={(e) => updateImprovement(index, 'description', e.target.value)}
                    placeholder="Describe the improvement suggestion..."
                    rows="3"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              ))}
              <button
                onClick={addImprovement}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                + Add Another Improvement
              </button>
            </div>
          </div>

          {/* Additional Notes */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Additional Notes</h3>
            <textarea
              value={additionalNotes}
              onChange={(e) => setAdditionalNotes(e.target.value)}
              placeholder="Any additional observations or recommendations..."
              rows="4"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4 pt-4">
            <button
              onClick={() => setFeedbackStep(1)}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 font-medium"
            >
              Back
            </button>
            <button
              onClick={() => setFeedbackStep(3)}
              className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 font-medium"
            >
              Continue to Anonymization Options
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (feedbackStep === 3) {
    return (
      <div className="collective-learning-feedback bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Contribute to Collective Learning</h2>
          <p className="text-gray-600">Help improve future protocols by anonymizing and sharing this case.</p>
        </div>

        <div className="space-y-6">
          {/* Anonymization Benefits */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-blue-900 mb-3">Benefits of Contributing</h3>
            <ul className="space-y-2 text-blue-800">
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Contribute to medical research and knowledge advancement</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Help improve future protocol accuracy for similar cases</span>
              </li>
              <li className="flex items-start">  
                <span className="mr-2">•</span>
                <span>Enhance our collective knowledge base for better patient outcomes</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">•</span>
                <span>Maintain complete privacy through advanced encryption</span>
              </li>
            </ul>
          </div>

          {/* Privacy Protection */}
          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="text-lg font-semibold text-green-900 mb-3">Privacy Protection</h3>
            <div className="text-green-800 space-y-2">
              <p><strong>What gets removed:</strong> Patient name, date of birth, email, phone, address</p>
              <p><strong>What gets encrypted:</strong> Date of birth (for age-related analysis only)</p>
              <p><strong>What gets anonymized:</strong> Free-text entries are scrubbed of identifiers</p>
              <p><strong>Protocol Number:</strong> You'll receive a unique reference number for future use</p>
            </div>
          </div>

          {/* Consent */}
          <div className="border-l-4 border-blue-500 pl-4">
            <label className="flex items-start space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={agreeToAnonymize}
                onChange={(e) => setAgreeToAnonymize(e.target.checked)}
                className="mt-1"
              />
              <div>
                <p className="font-medium text-gray-900">
                  I consent to anonymizing and storing this protocol for collective learning
                </p>
                <p className="text-sm text-gray-600 mt-1">
                  The protocol will be completely anonymized, encrypted, and used only to improve future medical care. 
                  You can reference this protocol later using the protocol number provided.
                </p>
              </div>
            </label>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4 pt-4">
            <button
              onClick={() => setFeedbackStep(2)}
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 font-medium"
            >
              Back
            </button>
            <button
              onClick={submitFeedbackOnly}
              disabled={isSubmitting}
              className="px-6 py-3 border border-blue-600 text-blue-600 rounded-md hover:bg-blue-50 font-medium disabled:opacity-50"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Feedback Only'}
            </button>
            <button
              onClick={anonymizeAndStore}
              disabled={!agreeToAnonymize || isSubmitting}
              className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
            >
              {isSubmitting ? 'Processing...' : 'Anonymize & Contribute to Learning'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (feedbackStep === 4) {
    return (
      <div className="collective-learning-feedback bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto text-center">
        <div className="text-green-600 text-6xl mb-4">✓</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Feedback Submitted Successfully!</h2>
        <p className="text-gray-600 mb-6">
          Thank you for your valuable feedback. Your insights help improve our protocol generation system.
        </p>
        <button
          onClick={() => setFeedbackStep(1)}
          className="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 font-medium"
        >
          Submit Another Feedback
        </button>
      </div>
    );
  }

  if (feedbackStep === 5) {
    return (
      <div className="collective-learning-feedback bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto text-center">
        <div className="text-green-600 text-6xl mb-4">🔒✓</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Protocol Successfully Anonymized!</h2>
        <div className="bg-blue-50 p-4 rounded-lg mb-6">
          <p className="text-lg font-semibold text-blue-900 mb-2">Your Protocol Number:</p>
          <div className="text-2xl font-mono font-bold text-blue-700 bg-white p-3 rounded border">
            {protocolNumber}
          </div>
          <p className="text-sm text-blue-700 mt-2">
            Save this number! Use it to reference this protocol when chatting with Dr. Peptide.
          </p>
        </div>
        <p className="text-gray-600 mb-6">
          Your protocol has been anonymized and added to our collective learning database. 
          This will help improve future protocols for similar cases while maintaining complete privacy.
        </p>
        <div className="flex space-x-4 justify-center">
          <button
            onClick={() => navigator.clipboard.writeText(protocolNumber)}
            className="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700 font-medium"
          >
            Copy Protocol Number
          </button>
          <button
            onClick={() => setFeedbackStep(1)}
            className="border border-gray-300 text-gray-700 py-2 px-6 rounded-md hover:bg-gray-50 font-medium"
          >
            Process Another Protocol
          </button>
        </div>
      </div>
    );
  }

  return null;
};

export default CollectiveLearningFeedback;