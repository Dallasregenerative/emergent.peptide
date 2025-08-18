import React, { useState } from 'react';
import { Search, FileText, Clock, Users, TrendingUp } from 'lucide-react';

const ProtocolReference = () => {
  const [protocolNumber, setProtocolNumber] = useState('');
  const [protocolData, setProtocolData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analytics, setAnalytics] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  const searchProtocol = async () => {
    if (!protocolNumber.trim()) {
      setError('Please enter a protocol number');
      return;
    }

    setLoading(true);
    setError(null);
    setProtocolData(null);

    try {
      const response = await fetch(`${backendUrl}/api/collective-learning/protocol/${protocolNumber.trim()}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Protocol not found. Please check the protocol number.');
        }
        throw new Error('Failed to retrieve protocol');
      }

      const data = await response.json();
      setProtocolData(data.protocol);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadAnalytics = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/collective-learning/analytics`);
      if (response.ok) {
        const data = await response.json();
        setAnalytics(data.analytics);
      }
    } catch (err) {
      console.error('Failed to load analytics:', err);
    }
  };

  React.useEffect(() => {
    loadAnalytics();
  }, []);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      searchProtocol();
    }
  };

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    } catch {
      return 'Unknown';
    }
  };

  return (
    <div className="protocol-reference p-6 max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Protocol Reference System</h2>
          <p className="text-gray-600">Look up anonymized protocols using protocol numbers for reference and updates</p>
        </div>

        <div className="p-6">
          {/* Search Section */}
          <div className="mb-8">
            <div className="flex items-center space-x-4">
              <div className="flex-1">
                <label htmlFor="protocolNumber" className="block text-sm font-medium text-gray-700 mb-2">
                  Protocol Number
                </label>
                <input
                  id="protocolNumber"
                  type="text"
                  value={protocolNumber}
                  onChange={(e) => setProtocolNumber(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Enter protocol number (e.g., PPA-2024-12345678)"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <button
                onClick={searchProtocol}
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium flex items-center space-x-2"
              >
                <Search className="w-5 h-5" />
                <span>{loading ? 'Searching...' : 'Search'}</span>
              </button>
            </div>
          </div>

          {/* Analytics Dashboard */}
          {analytics && (
            <div className="mb-8 grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-600 text-sm font-medium">Total Protocols</p>
                    <p className="text-2xl font-bold text-blue-900">{analytics.total_protocols}</p>
                  </div>
                  <FileText className="w-8 h-8 text-blue-600" />
                </div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-green-600 text-sm font-medium">Feedback Entries</p>
                    <p className="text-2xl font-bold text-green-900">{analytics.total_feedback_entries}</p>
                  </div>
                  <Users className="w-8 h-8 text-green-600" />
                </div>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-yellow-600 text-sm font-medium">Average Rating</p>
                    <p className="text-2xl font-bold text-yellow-900">{analytics.average_rating}/5</p>
                  </div>
                  <TrendingUp className="w-8 h-8 text-yellow-600" />
                </div>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-purple-600 text-sm font-medium">Participation Rate</p>
                    <p className="text-2xl font-bold text-purple-900">{analytics.learning_trends?.feedback_participation_rate || 0}%</p>
                  </div>
                  <Clock className="w-8 h-8 text-purple-600" />
                </div>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="text-red-800 font-medium">Error</div>
              <div className="text-red-700">{error}</div>
            </div>
          )}

          {/* Protocol Display */}
          {protocolData && (
            <div className="space-y-6">
              {/* Protocol Header */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">Protocol {protocolData.protocol_number}</h3>
                    <p className="text-gray-600">Anonymized Protocol Reference</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-500">Anonymized: {formatDate(protocolData.anonymized_at)}</p>
                    {protocolData.learning_metadata && (
                      <p className="text-sm text-gray-500">
                        Referenced: {protocolData.learning_metadata.reference_count} times
                      </p>
                    )}
                  </div>
                </div>
              </div>

              {/* Protocol Content */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Left Column */}
                <div className="space-y-4">
                  {/* Symptoms */}
                  {protocolData.symptoms && protocolData.symptoms.length > 0 && (
                    <div className="bg-white border rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Symptoms Addressed</h4>
                      <div className="space-y-1">
                        {protocolData.symptoms.map((symptom, index) => (
                          <span key={index} className="inline-block bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-sm mr-2 mb-2">
                            {symptom}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Medical Conditions */}
                  {protocolData.medical_conditions && protocolData.medical_conditions.length > 0 && (
                    <div className="bg-white border rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Medical Conditions</h4>
                      <div className="space-y-1">
                        {protocolData.medical_conditions.map((condition, index) => (
                          <span key={index} className="inline-block bg-red-100 text-red-800 px-2 py-1 rounded-full text-sm mr-2 mb-2">
                            {condition}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Recommended Peptides */}
                  {protocolData.recommended_peptides && protocolData.recommended_peptides.length > 0 && (
                    <div className="bg-white border rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Recommended Peptides</h4>
                      <div className="space-y-1">
                        {protocolData.recommended_peptides.map((peptide, index) => (
                          <span key={index} className="inline-block bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm mr-2 mb-2">
                            {peptide}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Right Column */}
                <div className="space-y-4">
                  {/* Protocol Summary */}
                  {protocolData.protocol_summary && (
                    <div className="bg-white border rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Protocol Summary</h4>
                      <p className="text-gray-700 text-sm leading-relaxed">{protocolData.protocol_summary}</p>
                    </div>
                  )}

                  {/* Practitioner Feedback */}
                  {protocolData.practitioner_feedback && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Practitioner Feedback</h4>
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                          <span className="text-sm font-medium">Rating:</span>
                          <div className="flex">
                            {[1, 2, 3, 4, 5].map((star) => (
                              <span
                                key={star}
                                className={`text-lg ${
                                  star <= protocolData.practitioner_feedback.rating ? 'text-yellow-500' : 'text-gray-300'
                                }`}
                              >
                                ★
                              </span>
                            ))}
                          </div>
                          <span className="text-sm text-gray-600">
                            ({protocolData.practitioner_feedback.rating}/5)
                          </span>
                        </div>
                        <div>
                          <span className="text-sm font-medium">Accuracy: </span>
                          <span className="text-sm capitalize">
                            {protocolData.practitioner_feedback.accuracy_assessment?.replace('_', ' ')}
                          </span>
                        </div>
                        {protocolData.practitioner_feedback.additional_notes && (
                          <div>
                            <span className="text-sm font-medium">Notes: </span>
                            <p className="text-sm text-gray-700 mt-1">
                              {protocolData.practitioner_feedback.additional_notes}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Protocol Updates */}
                  {protocolData.protocol_updates && protocolData.protocol_updates.length > 0 && (
                    <div className="bg-white border rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Protocol Updates</h4>
                      <div className="space-y-3">
                        {protocolData.protocol_updates.map((update, index) => (
                          <div key={index} className="bg-gray-50 p-3 rounded">
                            <div className="flex justify-between items-start mb-1">
                              <span className="text-sm font-medium capitalize">
                                {update.update_type?.replace('_', ' ')}
                              </span>
                              <span className="text-xs text-gray-500">
                                {formatDate(update.update_timestamp)}
                              </span>
                            </div>
                            {update.update_content && (
                              <p className="text-sm text-gray-700">{JSON.stringify(update.update_content)}</p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Usage Instructions */}
              <div className="bg-blue-50 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">Using This Protocol Reference</h4>
                <ul className="text-blue-800 text-sm space-y-1">
                  <li>• Use this protocol number when chatting with Dr. Peptide for specific questions</li>
                  <li>• Reference this protocol for patient progress updates</li>
                  <li>• Share the protocol number with patients for their records</li>
                  <li>• All patient identifying information has been removed for privacy</li>
                </ul>
              </div>
            </div>
          )}

          {/* Common Improvements Section */}
          {analytics?.most_common_improvements && analytics.most_common_improvements.length > 0 && (
            <div className="mt-8 bg-white border rounded-lg p-4">
              <h4 className="font-semibold text-gray-900 mb-3">Most Common Improvement Areas</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {analytics.most_common_improvements.map(([type, count], index) => (
                  <div key={index} className="bg-gray-50 p-3 rounded">
                    <div className="text-sm font-medium capitalize text-gray-900">
                      {type.replace('_', ' ')}
                    </div>
                    <div className="text-lg font-bold text-blue-600">{count} protocols</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProtocolReference;