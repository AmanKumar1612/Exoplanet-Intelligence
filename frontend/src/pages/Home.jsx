import React, { useState } from 'react';
import {
  FlaskConical, GitCompare, Ruler, AlertCircle,
  Sparkles, Globe,
} from 'lucide-react';
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
      const response = taskType === 'classification'
        ? await predictClassification(features)
        : await predictRegression(features);
      setResult(response);
    } catch (err) {
      setError(err.message || 'An error occurred during prediction');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-10">

      {/* ── Hero ── */}
      <div className="text-center pt-4 pb-2 animate-fade-in">
        {/* Pill badge */}
        <div className="inline-flex items-center gap-2 mb-5 px-4 py-1.5 rounded-full text-xs font-semibold"
          style={{
            background: 'rgba(99,102,241,0.1)',
            border: '1px solid rgba(99,102,241,0.3)',
            color: '#a5b4fc',
            letterSpacing: '0.08em',
            boxShadow: '0 0 16px rgba(99,102,241,0.12)',
          }}>
          <Sparkles className="w-3.5 h-3.5" />
          NASA Kepler Mission · ML Powered
          <Globe className="w-3.5 h-3.5" />
        </div>

        <h1
          className="text-5xl font-black gradient-text mb-4 leading-tight"
          style={{ fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}
        >
          Exoplanet Intelligence
          <br />
          <span style={{ fontSize: '0.7em', opacity: 0.85 }}>System</span>
        </h1>
<<<<<<< HEAD
        <p className="text-gray-400 max-w-2xl mx-auto">
          Machine learning powered predictions for exoplanet classification and radius estimation
=======

        <p className="max-w-xl mx-auto text-sm leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
          Machine learning–powered predictions for exoplanet classification and radius estimation
>>>>>>> f533504 (feat: improve UI/CSS with nebula theme, glassmorphism, and animations)
          using NASA Kepler mission data.
        </p>
      </div>

      {/* ── Task Switcher ── */}
      <div className="flex justify-center">
        <div
          className="flex p-1.5 rounded-2xl gap-1"
          style={{
            background: 'rgba(8,11,24,0.7)',
            border: '1px solid rgba(99,102,241,0.2)',
            boxShadow: '0 2px 16px rgba(0,0,0,0.3)',
          }}
        >
          {[
            { type: 'classification', label: 'Classification', Icon: GitCompare },
            { type: 'regression', label: 'Regression', Icon: Ruler },
          ].map(({ type, label, Icon }) => {
            const active = taskType === type;
            return (
              <button
                key={type}
                onClick={() => handleTaskTypeChange(type)}
                className="relative flex items-center gap-2 px-6 py-2.5 rounded-xl font-semibold text-sm transition-all duration-300"
                style={
                  active
                    ? {
                      background: 'linear-gradient(135deg,#6366f1,#8b5cf6)',
                      color: '#fff',
                      boxShadow: '0 4px 16px rgba(99,102,241,0.5)',
                    }
                    : { color: 'var(--text-secondary)' }
                }
              >
                <Icon className="w-4 h-4" />
                {label}
              </button>
            );
          })}
        </div>
      </div>

      {/* ── Task Description ── */}
      <div
        className="max-w-2xl mx-auto rounded-xl p-4 flex items-start gap-3"
        style={{
          background: 'rgba(99,102,241,0.06)',
          border: '1px solid rgba(99,102,241,0.18)',
          boxShadow: '0 2px 16px rgba(99,102,241,0.06)',
        }}
      >
        <div
          className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
          style={{ background: 'rgba(99,102,241,0.15)', border: '1px solid rgba(99,102,241,0.3)' }}
        >
          <FlaskConical className="w-4 h-4 text-indigo-400" />
        </div>
        <div>
          <h3 className="font-bold mb-1" style={{ color: '#c7d2fe' }}>
            {taskType === 'classification' ? 'Exoplanet Classification' : 'Planetary Radius Prediction'}
          </h3>
          <p className="text-sm leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
            {taskType === 'classification'
              ? 'Predict whether an exoplanet candidate is CONFIRMED as a real planet or classified as a FALSE POSITIVE based on transit and stellar properties.'
              : 'Predict the planetary radius in Earth radii based on transit depth, orbital properties, and stellar characteristics.'}
          </p>
        </div>
      </div>

      {/* ── Error ── */}
      {error && (
        <div className="max-w-2xl mx-auto animate-fade-in">
          <div
            className="rounded-xl p-4 flex items-start gap-3"
            style={{ background: 'rgba(244,63,94,0.08)', border: '1px solid rgba(244,63,94,0.3)' }}
          >
            <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-bold text-rose-400">Error</h4>
              <p className="text-sm text-rose-300 mt-0.5">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* ── Main Grid ── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

        {/* Input Form */}
        <div className="card p-6">
          <h2
            className="text-lg font-bold mb-6 flex items-center gap-2"
            style={{ color: '#c7d2fe' }}
          >
            <span
              className="w-7 h-7 rounded-lg flex items-center justify-center text-xs font-black"
              style={{ background: 'rgba(99,102,241,0.2)', border: '1px solid rgba(99,102,241,0.35)', color: '#a5b4fc' }}
            >
              ①
            </span>
            Input Features
          </h2>
          <InputForm taskType={taskType} onSubmit={handleSubmit} isLoading={isLoading} />
        </div>

        {/* Results */}
        <div className="space-y-6">
          {result ? (
            <>
              <ResultDisplay result={result} taskType={taskType} />
              <Charts result={result} taskType={taskType} />
            </>
          ) : (
            <div
              className="card p-8 text-center flex flex-col items-center justify-center"
              style={{ minHeight: '260px' }}
            >
              <div
                className="w-16 h-16 rounded-full flex items-center justify-center mb-4 animate-float"
                style={{
                  background: 'rgba(99,102,241,0.08)',
                  border: '1px solid rgba(99,102,241,0.2)',
                }}
              >
                <FlaskConical className="w-8 h-8" style={{ color: 'rgba(99,102,241,0.5)' }} />
              </div>
              <p className="font-semibold mb-1" style={{ color: 'var(--text-secondary)' }}>Awaiting Prediction</p>
              <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
                Enter exoplanet features and click predict to see results
              </p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Home;
