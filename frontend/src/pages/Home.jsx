import React, { useState } from 'react';
import { FlaskConical, GitCompare, Ruler, AlertCircle } from 'lucide-react';
import InputForm from '../components/InputForm';
import ResultDisplay from '../components/ResultDisplay';
import Charts from '../components/Charts';
import { predictClassification, predictRegression } from '../services/api';

const Home = () => {
  const [taskType, setTaskType] = useState('classification');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleTaskTypeChange = (newType) => {
    setTaskType(newType);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async (features) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      let response;
      if (taskType === 'classification') {
        response = await predictClassification(features);
      } else {
        response = await predictRegression(features);
      }
      setResult(response);
    } catch (err) {
      setError(err.message || 'An error occurred during prediction');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold gradient-text mb-4">
          Exoplanet Intelligence System
        </h1>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Machine learning-powered predictions for exoplanet classification and radius estimation
          using NASA Kepler mission data.
        </p>
      </div>

      {/* Task Selector */}
      <div className="flex justify-center">
        <div className="bg-gray-800/50 p-2 rounded-xl border border-gray-700">
          <button
            onClick={() => handleTaskTypeChange('classification')}
            className={`px-6 py-3 rounded-lg flex items-center gap-2 transition-all ${
              taskType === 'classification'
                ? 'bg-indigo-500 text-white'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <GitCompare className="w-5 h-5" />
            Classification
          </button>
          <button
            onClick={() => handleTaskTypeChange('regression')}
            className={`px-6 py-3 rounded-lg flex items-center gap-2 transition-all ${
              taskType === 'regression'
                ? 'bg-indigo-500 text-white'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Ruler className="w-5 h-5" />
            Regression
          </button>
        </div>
      </div>

      {/* Task Description */}
      <div className="card p-4 max-w-2xl mx-auto">
        <div className="flex items-start gap-3">
          <FlaskConical className="w-6 h-6 text-indigo-400 flex-shrink-0 mt-1" />
          <div>
            <h3 className="font-semibold text-lg mb-1">
              {taskType === 'classification' ? 'Exoplanet Classification' : 'Planetary Radius Prediction'}
            </h3>
            <p className="text-gray-400 text-sm">
              {taskType === 'classification'
                ? 'Predict whether an exoplanet candidate is CONFIRMED as a real planet or classified as a FALSE POSITIVE based on transit and stellar properties.'
                : 'Predict the planetary radius in Earth radii based on transit depth, orbital properties, and stellar characteristics.'}
            </p>
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="max-w-2xl mx-auto">
          <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold text-red-400">Error</h4>
              <p className="text-red-300 text-sm">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="card p-6">
          <h2 className="text-xl font-bold mb-6">Input Features</h2>
          <InputForm
            taskType={taskType}
            onSubmit={handleSubmit}
            isLoading={isLoading}
          />
        </div>

        {/* Results */}
        <div className="space-y-6">
          {result ? (
            <>
              <ResultDisplay result={result} taskType={taskType} />
              <Charts result={result} taskType={taskType} />
            </>
          ) : (
            <div className="card p-6 text-center py-16">
              <FlaskConical className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">
                Enter the exoplanet features and click predict to see results
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
