import React, { useState } from 'react';

const DrugInteractionChecker = () => {
  const [medications, setMedications] = useState(['']);
  const [peptides, setPeptides] = useState(['']);
  const [medicalConditions, setMedicalConditions] = useState(['']);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  const addMedicationField = () => {
    setMedications([...medications, '']);
  };

  const addPeptideField = () => {
    setPeptides([...peptides, '']);
  };

  const addConditionField = () => {
    setMedicalConditions([...medicalConditions, '']);
  };

  const removeMedicationField = (index) => {
    const newMedications = medications.filter((_, i) => i !== index);
    setMedications(newMedications.length > 0 ? newMedications : ['']);
  };

  const removePeptideField = (index) => {
    const newPeptides = peptides.filter((_, i) => i !== index);
    setPeptides(newPeptides.length > 0 ? newPeptides : ['']);
  };

  const removeConditionField = (index) => {
    const newConditions = medicalConditions.filter((_, i) => i !== index);
    setMedicalConditions(newConditions.length > 0 ? newConditions : ['']);
  };

  const updateMedication = (index, value) => {
    const newMedications = [...medications];
    newMedications[index] = value;
    setMedications(newMedications);
  };

  const updatePeptide = (index, value) => {
    const newPeptides = [...peptides];
    newPeptides[index] = value;
    setPeptides(newPeptides);
  };

  const updateCondition = (index, value) => {
    const newConditions = [...medicalConditions];
    newConditions[index] = value;
    setMedicalConditions(newConditions);
  };

  const checkInteractions = async () => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch(`${backendUrl}/api/drug-interactions/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          medications: medications.filter(med => med.trim() !== ''),
          peptides: peptides.filter(pep => pep.trim() !== ''),
          medical_conditions: medicalConditions.filter(cond => cond.trim() !== '')
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to check drug interactions');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'contraindicated':
        return 'text-red-800 bg-red-100 border-red-300';
      case 'major':
        return 'text-red-700 bg-red-50 border-red-200';
      case 'moderate':
        return 'text-yellow-700 bg-yellow-50 border-yellow-200';
      case 'minor':
        return 'text-green-700 bg-green-50 border-green-200';
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="drug-interaction-checker p-6 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Drug Interaction Checker</h2>
          <p className="text-gray-600">Check for interactions between medications and peptides</p>
        </div>

        <div className="p-6 space-y-6">
          {/* Medications Section */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Current Medications</h3>
            <div className="space-y-2">
              {medications.map((medication, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={medication}
                    onChange={(e) => updateMedication(index, e.target.value)}
                    placeholder="Enter medication name (e.g., Metformin, Lisinopril)"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {medications.length > 1 && (
                    <button
                      onClick={() => removeMedicationField(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                onClick={addMedicationField}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                + Add Another Medication
              </button>
            </div>
          </div>

          {/* Peptides Section */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Peptides Under Consideration</h3>
            <div className="space-y-2">
              {peptides.map((peptide, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={peptide}
                    onChange={(e) => updatePeptide(index, e.target.value)}
                    placeholder="Enter peptide name (e.g., BPC-157, Semaglutide)"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {peptides.length > 1 && (
                    <button
                      onClick={() => removePeptideField(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                onClick={addPeptideField}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                + Add Another Peptide
              </button>
            </div>
          </div>

          {/* Medical Conditions Section */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3">Medical Conditions</h3>
            <div className="space-y-2">
              {medicalConditions.map((condition, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <input
                    type="text"
                    value={condition}
                    onChange={(e) => updateCondition(index, e.target.value)}
                    placeholder="Enter medical condition (e.g., Diabetes, Heart Disease)"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  {medicalConditions.length > 1 && (
                    <button
                      onClick={() => removeConditionField(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  )}
                </div>
              ))}
              <button
                onClick={addConditionField}
                className="text-blue-600 hover:text-blue-800 font-medium"
              >
                + Add Another Condition
              </button>
            </div>
          </div>

          {/* Check Button */}
          <div className="pt-4">
            <button
              onClick={checkInteractions}
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium"
            >
              {loading ? 'Checking Interactions...' : 'Check for Drug Interactions'}
            </button>
          </div>
        </div>

        {/* Results Section */}
        {(results || error) && (
          <div className="border-t border-gray-200 p-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
                <div className="text-red-800 font-medium">Error</div>
                <div className="text-red-700">{error}</div>
              </div>
            )}

            {results && (
              <div className="space-y-4">
                {/* Summary */}
                <div className={`p-4 rounded-md border ${
                  results.has_major_interactions 
                    ? 'bg-red-50 border-red-200' 
                    : results.total_interactions > 0 
                    ? 'bg-yellow-50 border-yellow-200'
                    : 'bg-green-50 border-green-200'
                }`}>
                  <h3 className="font-semibold text-lg mb-2">
                    {results.total_interactions === 0 ? 'No Interactions Found' : 'Interaction Summary'}
                  </h3>
                  <p className="text-gray-700">{results.summary}</p>
                </div>

                {/* Interactions */}
                {results.interactions && results.interactions.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-lg mb-3">Detailed Interactions</h4>
                    <div className="space-y-3">
                      {results.interactions.map((interaction, index) => (
                        <div
                          key={index}
                          className={`p-4 rounded-md border ${getSeverityColor(interaction.severity)}`}
                        >
                          <div className="flex justify-between items-start mb-2">
                            <h5 className="font-medium">
                              {interaction.drug1} ↔ {interaction.drug2}
                            </h5>
                            <span className="px-2 py-1 text-xs font-medium rounded uppercase">
                              {interaction.severity}
                            </span>
                          </div>
                          <p className="mb-2">{interaction.description}</p>
                          <div className="text-sm">
                            <p><strong>Mechanism:</strong> {interaction.mechanism}</p>
                            <p><strong>Management:</strong> {interaction.management}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Contraindications */}
                {results.contraindications && results.contraindications.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-lg mb-3">Contraindications</h4>
                    <div className="space-y-3">
                      {results.contraindications.map((contraindication, index) => (
                        <div
                          key={index}
                          className={`p-4 rounded-md border ${getSeverityColor(contraindication.severity)}`}
                        >
                          <h5 className="font-medium mb-2">
                            {contraindication.peptide} - {contraindication.condition}
                          </h5>
                          <p className="mb-2">{contraindication.reason}</p>
                          <p className="text-sm"><strong>Recommendation:</strong> {contraindication.recommendation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default DrugInteractionChecker;