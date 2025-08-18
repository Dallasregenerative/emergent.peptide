import React, { useState } from 'react';
import { Upload, FileText, AlertTriangle, CheckCircle, TrendingUp, Activity } from 'lucide-react';

const LabAnalysis = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [selectedFile, setSelectedFile] = useState(null);
  const [manualValues, setManualValues] = useState({});
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  const commonLabTests = [
    { key: 'glucose', name: 'Glucose', unit: 'mg/dL' },
    { key: 'hemoglobin_a1c', name: 'Hemoglobin A1C', unit: '%' },
    { key: 'total_cholesterol', name: 'Total Cholesterol', unit: 'mg/dL' },
    { key: 'ldl_cholesterol', name: 'LDL Cholesterol', unit: 'mg/dL' },
    { key: 'hdl_cholesterol', name: 'HDL Cholesterol', unit: 'mg/dL' },
    { key: 'triglycerides', name: 'Triglycerides', unit: 'mg/dL' },
    { key: 'tsh', name: 'TSH', unit: 'mIU/L' },
    { key: 'free_t4', name: 'Free T4', unit: 'ng/dL' },
    { key: 'free_t3', name: 'Free T3', unit: 'pg/mL' },
    { key: 'testosterone_total', name: 'Total Testosterone', unit: 'ng/dL' },
    { key: 'crp', name: 'C-Reactive Protein', unit: 'mg/L' },
    { key: 'vitamin_d', name: 'Vitamin D', unit: 'ng/mL' },
    { key: 'creatinine', name: 'Creatinine', unit: 'mg/dL' },
    { key: 'alt', name: 'ALT', unit: 'U/L' },
    { key: 'ast', name: 'AST', unit: 'U/L' }
  ];

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
    }
  };

  const uploadAndAnalyzeFile = async () => {
    if (!selectedFile) {
      setError('Please select a file to upload');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Convert file to base64
      const fileReader = new FileReader();
      fileReader.onload = async (e) => {
        const base64Content = btoa(e.target.result);
        
        const response = await fetch(`${backendUrl}/api/lab-analysis/upload`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            file_content: base64Content,
            file_name: selectedFile.name,
            file_type: selectedFile.type,
            patient_info: {
              gender: 'male', // Would get from form in real implementation
              age: '35'
            }
          }),
        });

        if (!response.ok) {
          throw new Error('Failed to analyze lab file');
        }

        const data = await response.json();
        setAnalysis(data);
        setLoading(false);
      };
      
      fileReader.readAsBinaryString(selectedFile);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const analyzeManualValues = async () => {
    const validValues = Object.entries(manualValues)
      .filter(([_, value]) => value && !isNaN(parseFloat(value)))
      .reduce((acc, [key, value]) => {
        acc[key] = parseFloat(value);
        return acc;
      }, {});

    if (Object.keys(validValues).length === 0) {
      setError('Please enter at least one lab value');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${backendUrl}/api/lab-analysis/analyze-values`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          lab_values: validValues,
          patient_info: {
            gender: 'male', // Would get from form in real implementation
            age: '35'
          }
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze lab values');
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const updateManualValue = (key, value) => {
    setManualValues(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'critical':
        return 'text-red-800 bg-red-100 border-red-300';
      case 'high':
        return 'text-red-700 bg-red-50 border-red-200';
      case 'moderate':
        return 'text-yellow-700 bg-yellow-50 border-yellow-200';
      case 'low':
        return 'text-green-700 bg-green-50 border-green-200';
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'critical_high':
      case 'critical_low':
        return 'text-red-800';
      case 'high':
      case 'low':
        return 'text-yellow-700';
      case 'normal':
        return 'text-green-700';
      default:
        return 'text-gray-700';
    }
  };

  return (
    <div className="lab-analysis max-w-6xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Lab Analysis & Risk Assessment</h2>
          <p className="text-gray-600">Upload lab reports or enter values manually for comprehensive analysis</p>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200">
          <div className="flex space-x-8 px-6">
            <button
              onClick={() => setActiveTab('upload')}
              className={`py-4 px-2 border-b-2 font-medium text-sm ${
                activeTab === 'upload'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Upload className="w-4 h-4 inline mr-2" />
              Upload Lab Report
            </button>
            <button
              onClick={() => setActiveTab('manual')}
              className={`py-4 px-2 border-b-2 font-medium text-sm ${
                activeTab === 'manual'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <FileText className="w-4 h-4 inline mr-2" />
              Manual Entry
            </button>
          </div>
        </div>

        <div className="p-6">
          {activeTab === 'upload' && (
            <div className="space-y-6">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
                <div className="text-center">
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="mt-4">
                    <label htmlFor="file-upload" className="cursor-pointer">
                      <span className="mt-2 block text-sm font-medium text-gray-900">
                        Upload your lab report
                      </span>
                      <span className="mt-1 block text-xs text-gray-500">
                        PDF, TXT, or image files supported
                      </span>
                    </label>
                    <input
                      id="file-upload"
                      type="file"
                      className="hidden"
                      accept=".pdf,.txt,.jpg,.jpeg,.png"
                      onChange={handleFileUpload}
                    />
                  </div>
                </div>
                
                {selectedFile && (
                  <div className="mt-4 text-center">
                    <p className="text-sm text-green-600">
                      Selected: {selectedFile.name}
                    </p>
                  </div>
                )}
              </div>

              <button
                onClick={uploadAndAnalyzeFile}
                disabled={!selectedFile || loading}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
              >
                {loading ? 'Analyzing...' : 'Analyze Lab Report'}
              </button>
            </div>
          )}

          {activeTab === 'manual' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {commonLabTests.map((test) => (
                  <div key={test.key} className="space-y-2">
                    <label htmlFor={test.key} className="block text-sm font-medium text-gray-700">
                      {test.name}
                    </label>
                    <div className="relative">
                      <input
                        id={test.key}
                        type="number"
                        step="0.01"
                        value={manualValues[test.key] || ''}
                        onChange={(e) => updateManualValue(test.key, e.target.value)}
                        placeholder={`Enter ${test.name.toLowerCase()}`}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                      <span className="absolute right-3 top-2 text-sm text-gray-500">{test.unit}</span>
                    </div>
                  </div>
                ))}
              </div>

              <button
                onClick={analyzeManualValues}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
              >
                {loading ? 'Analyzing...' : 'Analyze Lab Values'}
              </button>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="mt-6 bg-red-50 border border-red-200 rounded-md p-4">
              <div className="flex">
                <AlertTriangle className="h-5 w-5 text-red-400" />
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <p className="text-sm text-red-700 mt-1">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Analysis Results */}
          {analysis && (
            <div className="mt-8 space-y-6">
              {/* Overall Risk Summary */}
              <div className={`p-4 rounded-lg border ${getRiskColor(analysis.overall_risk?.overall_risk_level || 'low')}`}>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-lg">Overall Health Assessment</h3>
                    <p className="text-sm mt-1">{analysis.summary}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">
                      {analysis.overall_risk?.risk_score || 0}%
                    </div>
                    <div className="text-xs uppercase tracking-wide">
                      Risk Score
                    </div>
                  </div>
                </div>
              </div>

              {/* Individual Lab Results */}
              {analysis.lab_results && Object.keys(analysis.lab_results).length > 0 && (
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Individual Lab Results</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(analysis.lab_results).map(([labName, result]) => (
                      <div key={labName} className="bg-gray-50 rounded-lg p-4">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-medium text-gray-900">
                            {labName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </h4>
                          <span className={`px-2 py-1 text-xs font-medium rounded uppercase ${getStatusColor(result.status)}`}>
                            {result.status?.replace('_', ' ')}
                          </span>
                        </div>
                        <div className="space-y-1">
                          <p className="text-lg font-semibold">
                            {result.value} {result.unit}
                          </p>
                          <p className="text-sm text-gray-600">{result.interpretation}</p>
                          {result.normal_range && (
                            <p className="text-xs text-gray-500">
                              Normal: {result.normal_range[0]}-{result.normal_range[1]} {result.unit}
                            </p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Risk Factors */}
              {analysis.risk_factors && analysis.risk_factors.length > 0 && (
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Risk Factors Identified</h3>
                  <div className="space-y-3">
                    {analysis.risk_factors.map((factor, index) => (
                      <div key={index} className={`p-4 rounded-lg border ${getRiskColor(factor.risk_level)}`}>
                        <div className="flex items-start">
                          <AlertTriangle className="h-5 w-5 mt-1 mr-3" />
                          <div>
                            <h4 className="font-medium">
                              {factor.lab?.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                            </h4>
                            <p className="text-sm mt-1">{factor.issue}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Recommendations */}
              {analysis.recommendations && analysis.recommendations.length > 0 && (
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Clinical Recommendations</h3>
                  <div className="space-y-3">
                    {analysis.recommendations.map((rec, index) => (
                      <div key={index} className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <div className="flex items-start">
                          <CheckCircle className="h-5 w-5 text-blue-600 mt-1 mr-3" />
                          <div>
                            <h4 className="font-medium text-blue-900 capitalize">{rec.category} Recommendation</h4>
                            <p className="text-blue-800 mt-1">{rec.recommendation}</p>
                            <p className="text-blue-700 text-sm mt-2">{rec.rationale}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Peptide Considerations */}
              {analysis.peptide_considerations && analysis.peptide_considerations.length > 0 && (
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Peptide Therapy Considerations</h3>
                  <div className="space-y-3">
                    {analysis.peptide_considerations.map((consideration, index) => (
                      <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-4">
                        <div className="flex items-start">
                          <Activity className="h-5 w-5 text-green-600 mt-1 mr-3" />
                          <div>
                            <h4 className="font-medium text-green-900">{consideration.peptide_class}</h4>
                            <p className="text-green-800 mt-1">{consideration.consideration}</p>
                            <p className="text-green-700 text-sm mt-2">
                              <strong>Monitoring:</strong> {consideration.monitoring}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LabAnalysis;