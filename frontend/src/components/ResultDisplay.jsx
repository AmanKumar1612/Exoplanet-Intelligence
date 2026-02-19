import React from 'react';
import { CheckCircle, XCircle, AlertTriangle, Info } from 'lucide-react';

const ResultDisplay = ({ result, taskType }) => {
  if (!result) return null;

  if (taskType === 'classification') {
    return (
      <div className="card p-6 animate-fade-in">
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Info className="w-5 h-5 text-indigo-400" />
          Classification Result
        </h3>
        
        <div className="space-y-4">
          {/* Prediction */}
          <div className={`p-4 rounded-lg ${
            result.prediction === 'CONFIRMED' 
              ? 'bg-green-500/20 border border-green-500/30' 
              : 'bg-red-500/20 border border-red-500/30'
          }`}>
            <div className="flex items-center gap-3">
              {result.prediction === 'CONFIRMED' ? (
                <CheckCircle className="w-8 h-8 text-green-400" />
              ) : (
                <XCircle className="w-8 h-8 text-red-400" />
              )}
              <div>
                <p className="text-sm text-gray-400">Predicted Class</p>
                <p className="text-2xl font-bold">{result.prediction}</p>
              </div>
            </div>
          </div>

          {/* Confidence */}
          <div className="p-4 bg-gray-800/50 rounded-lg">
            <p className="text-sm text-gray-400 mb-1">Confidence</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${result.confidence * 100}%` }}
                />
              </div>
              <span className="text-lg font-bold text-indigo-400">
                {(result.confidence * 100).toFixed(1)}%
              </span>
            </div>
          </div>

          {/* Probabilities */}
          <div className="p-4 bg-gray-800/50 rounded-lg">
            <p className="text-sm text-gray-400 mb-3">Probability Scores</p>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-green-400">CONFIRMED</span>
                <span className="font-bold">{(result.probabilities?.CONFIRMED || 0) * 100}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${(result.probabilities?.CONFIRMED || 0) * 100}%` }}
                />
              </div>
              
              <div className="flex items-center justify-between mt-2">
                <span className="text-red-400">FALSE POSITIVE</span>
                <span className="font-bold">{(result.probabilities?.['FALSE POSITIVE'] || 0) * 100}%</span>
              </div>
              <div className="bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-red-500 h-2 rounded-full"
                  style={{ width: `${(result.probabilities?.['FALSE POSITIVE'] || 0) * 100}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Regression result
  return (
    <div className="card p-6 animate-fade-in">
      <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
        <Info className="w-5 h-5 text-indigo-400" />
        Regression Result
      </h3>
      
      <div className="space-y-4">
        {/* Prediction */}
        <div className="p-6 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-lg border border-indigo-500/30">
          <div className="text-center">
            <p className="text-sm text-gray-400 mb-1">Predicted Planetary Radius</p>
            <p className="text-4xl font-bold gradient-text">
              {result.prediction?.toFixed(2)}
              <span className="text-lg ml-2 text-gray-400">{result.unit || 'Earth radii'}</span>
            </p>
          </div>
        </div>

        {/* Confidence Interval */}
        <div className="p-4 bg-gray-800/50 rounded-lg">
          <p className="text-sm text-gray-400 mb-3">95% Confidence Interval</p>
          <div className="flex items-center justify-center gap-4">
            <div className="text-center">
              <p className="text-sm text-gray-500">Lower Bound</p>
              <p className="text-xl font-bold text-green-400">
                {result.confidence_interval?.lower?.toFixed(2)}
              </p>
            </div>
            <div className="text-gray-600">→</div>
            <div className="text-center">
              <p className="text-sm text-gray-500">Upper Bound</p>
              <p className="text-xl font-bold text-red-400">
                {result.confidence_interval?.upper?.toFixed(2)}
              </p>
            </div>
          </div>
        </div>

        {/* Info */}
        <div className="p-3 bg-blue-500/10 rounded-lg border border-blue-500/20">
          <div className="flex items-start gap-2">
            <AlertTriangle className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-blue-300">
              The confidence interval represents the range within which the true planetary radius 
              is likely to fall with 95% probability.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;
