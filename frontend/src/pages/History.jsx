import React, { useState, useEffect } from 'react';
import { Clock, Trash2, Search, AlertCircle } from 'lucide-react';
import { getPredictionHistory } from '../services/api';

const History = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await getPredictionHistory(50);
      setPredictions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const filteredPredictions = predictions.filter(p => {
    if (filter === 'all') return true;
    return p.task_type === filter;
  });

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleString();
  };

  const renderPrediction = (prediction) => {
    if (prediction.task_type === 'classification') {
      return (
        <div className="flex items-center gap-2">
          <span className={`px-2 py-1 rounded text-xs font-semibold ${
            prediction.output_result?.prediction === 'CONFIRMED'
              ? 'bg-green-500/20 text-green-400'
              : 'bg-red-500/20 text-red-400'
          }`}>
            {prediction.output_result?.prediction}
          </span>
          <span className="text-gray-500 text-sm">
            {(prediction.output_result?.confidence * 100).toFixed(1)}% confidence
          </span>
        </div>
      );
    } else {
      return (
        <div className="text-indigo-400 font-semibold">
          {prediction.output_result?.prediction?.toFixed(2)} Earth radii
        </div>
      );
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold gradient-text mb-4">
          Prediction History
        </h1>
        <p className="text-gray-400">
          View your past predictions and results
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
          <p className="text-red-300">{error}</p>
        </div>
      )}

      {/* Filters */}
      <div className="flex justify-center gap-4">
        {['all', 'classification', 'regression'].map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg capitalize transition-all ${
              filter === f
                ? 'bg-indigo-500 text-white'
                : 'bg-gray-800 text-gray-400 hover:text-white'
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Predictions List */}
      {filteredPredictions.length === 0 ? (
        <div className="card p-12 text-center">
          <Clock className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">No predictions yet</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredPredictions.map((prediction) => (
            <div key={prediction.id} className="card p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    prediction.task_type === 'classification'
                      ? 'bg-blue-500/20 text-blue-400'
                      : 'bg-purple-500/20 text-purple-400'
                  }`}>
                    {prediction.task_type}
                  </div>
                  {renderPrediction(prediction)}
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>{formatDate(prediction.created_at)}</span>
                  <span className="font-mono text-xs">{prediction.model_name}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
