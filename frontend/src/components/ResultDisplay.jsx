import React from 'react';
import {
  CheckCircle, XCircle, AlertTriangle, Info,
  TrendingUp, FlaskConical, Star, Zap,
} from 'lucide-react';

/* ── helpers ── */
const ProgressBar = ({ value, colorClass }) => (
  <div className="progress-bar-track mt-1">
    <div
      className="progress-bar-fill"
      style={{
        width: `${value}%`,
        background: colorClass === 'green'
          ? 'linear-gradient(90deg,#10b981,#34d399)'
          : 'linear-gradient(90deg,#f43f5e,#fb7185)',
      }}
    />
  </div>
);

/* ── Classification Result ── */
const ClassificationResult = ({ result }) => {
  const isConfirmed = result.prediction === 'CONFIRMED';
  const confirmedPct = ((result.probabilities?.CONFIRMED || 0) * 100).toFixed(1);
  const falsePct = ((result.probabilities?.['FALSE POSITIVE'] || 0) * 100).toFixed(1);
  const confidencePct = (result.confidence * 100).toFixed(1);

  return (
    <div className="card p-6 animate-fade-in space-y-5">

      {/* Header */}
      <h3 className="text-lg font-bold flex items-center gap-2" style={{ color: '#c7d2fe' }}>
        <Info className="w-5 h-5 text-indigo-400" style={{ filter: 'drop-shadow(0 0 6px rgba(129,140,248,0.7))' }} />
        Classification Result
      </h3>

      {/* Main prediction badge */}
      <div
        className="relative rounded-xl p-5 overflow-hidden"
        style={
          isConfirmed
            ? {
              background: 'linear-gradient(135deg, rgba(16,185,129,0.12), rgba(5,150,105,0.08))',
              border: '1px solid rgba(16,185,129,0.35)',
              boxShadow: '0 4px 24px rgba(16,185,129,0.1)',
            }
            : {
              background: 'linear-gradient(135deg, rgba(244,63,94,0.12), rgba(190,18,60,0.08))',
              border: '1px solid rgba(244,63,94,0.35)',
              boxShadow: '0 4px 24px rgba(244,63,94,0.1)',
            }
        }
      >
        {/* glow blob */}
        <div
          className="absolute -top-6 -right-6 w-24 h-24 rounded-full blur-2xl"
          style={{ background: isConfirmed ? 'rgba(16,185,129,0.25)' : 'rgba(244,63,94,0.25)' }}
        />

        <div className="relative flex items-center gap-4">
          <div
            className="w-14 h-14 rounded-xl flex items-center justify-center"
            style={{
              background: isConfirmed ? 'rgba(16,185,129,0.15)' : 'rgba(244,63,94,0.15)',
              border: `1px solid ${isConfirmed ? 'rgba(16,185,129,0.4)' : 'rgba(244,63,94,0.4)'}`,
            }}
          >
            {isConfirmed
              ? <CheckCircle className="w-7 h-7 text-green-400" style={{ filter: 'drop-shadow(0 0 8px rgba(52,211,153,0.8))' }} />
              : <XCircle className="w-7 h-7 text-red-400" style={{ filter: 'drop-shadow(0 0 8px rgba(251,113,133,0.8))' }} />
            }
          </div>
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest" style={{ color: isConfirmed ? '#6ee7b7' : '#fda4af' }}>
              Predicted Class
            </p>
            <p
              className="text-3xl font-black mt-0.5"
              style={{
                color: isConfirmed ? '#34d399' : '#f43f5e',
                textShadow: isConfirmed
                  ? '0 0 20px rgba(52,211,153,0.4)'
                  : '0 0 20px rgba(244,63,94,0.4)',
                letterSpacing: '-0.02em',
              }}
            >
              {result.prediction}
            </p>
          </div>
          {isConfirmed && (
            <Star
              className="ml-auto w-5 h-5 text-yellow-400 animate-pulse-slow"
              style={{ filter: 'drop-shadow(0 0 6px rgba(251,191,36,0.7))' }}
            />
          )}
        </div>
      </div>

      {/* Confidence bar */}
      <div className="stat-box">
        <div className="flex items-center justify-between mb-2">
          <p className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-muted)' }}>
            Model Confidence
          </p>
          <span
            className="text-2xl font-black gradient-text"
            style={{ fontFamily: "'Space Grotesk', sans-serif" }}
          >
            {confidencePct}%
          </span>
        </div>
        <div className="progress-bar-track">
          <div className="progress-bar-fill" style={{ width: `${confidencePct}%` }} />
        </div>
      </div>

      {/* Probability breakdown */}
      <div className="stat-box space-y-3">
        <p className="text-xs font-semibold uppercase tracking-wider mb-1" style={{ color: 'var(--text-muted)' }}>
          Probability Breakdown
        </p>

        <div>
          <div className="flex justify-between items-center">
            <span className="flex items-center gap-1.5 text-sm font-semibold text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_6px_rgba(52,211,153,0.8)]" />
              CONFIRMED
            </span>
            <span className="font-bold text-emerald-300">{confirmedPct}%</span>
          </div>
          <ProgressBar value={confirmedPct} colorClass="green" />
        </div>

        <div>
          <div className="flex justify-between items-center">
            <span className="flex items-center gap-1.5 text-sm font-semibold text-rose-400">
              <span className="w-2 h-2 rounded-full bg-rose-400 shadow-[0_0_6px_rgba(251,113,133,0.8)]" />
              FALSE POSITIVE
            </span>
            <span className="font-bold text-rose-300">{falsePct}%</span>
          </div>
          <ProgressBar value={falsePct} colorClass="red" />
        </div>
      </div>

    </div>
  );
};

/* ── Regression Result ── */
const RegressionResult = ({ result }) => (
  <div className="card p-6 animate-fade-in space-y-5">

    {/* Header */}
    <h3 className="text-lg font-bold flex items-center gap-2" style={{ color: '#c7d2fe' }}>
      <TrendingUp className="w-5 h-5 text-cyan-400" style={{ filter: 'drop-shadow(0 0 6px rgba(34,211,238,0.7))' }} />
      Regression Result
    </h3>

    {/* Main value */}
    <div
      className="relative rounded-xl p-6 overflow-hidden text-center"
      style={{
        background: 'linear-gradient(135deg, rgba(99,102,241,0.12), rgba(6,182,212,0.08))',
        border: '1px solid rgba(99,102,241,0.3)',
        boxShadow: '0 4px 24px rgba(99,102,241,0.1)',
      }}
    >
      <div className="absolute -top-8 left-1/2 -translate-x-1/2 w-28 h-28 rounded-full blur-3xl"
        style={{ background: 'rgba(99,102,241,0.2)' }} />
      <div className="relative">
        <FlaskConical
          className="w-10 h-10 mx-auto mb-2 text-indigo-400 animate-float"
          style={{ filter: 'drop-shadow(0 0 10px rgba(129,140,248,0.7))' }}
        />
        <p className="text-xs font-semibold uppercase tracking-widest mb-1" style={{ color: 'var(--text-muted)' }}>
          Predicted Planetary Radius
        </p>
        <p
          className="text-5xl font-black gradient-text"
          style={{ fontFamily: "'Space Grotesk', sans-serif", letterSpacing: '-0.03em' }}
        >
          {result.prediction?.toFixed(2)}
          <span className="text-lg font-semibold ml-2" style={{ color: 'var(--text-secondary)' }}>
            {result.unit || 'R⊕'}
          </span>
        </p>
      </div>
    </div>

    {/* Confidence interval */}
    <div className="stat-box">
      <p className="text-xs font-semibold uppercase tracking-wider mb-3" style={{ color: 'var(--text-muted)' }}>
        95% Confidence Interval
      </p>
      <div className="flex items-stretch gap-3">
        <div
          className="flex-1 text-center rounded-lg p-3"
          style={{ background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.2)' }}
        >
          <p className="text-xs mb-1" style={{ color: 'var(--text-muted)' }}>Lower Bound</p>
          <p className="text-xl font-black text-emerald-400">{result.confidence_interval?.lower?.toFixed(2)}</p>
          <p className="text-xs text-emerald-600 mt-0.5">R⊕</p>
        </div>

        <div className="flex items-center text-lg" style={{ color: 'rgba(99,102,241,0.5)' }}>→</div>

        <div
          className="flex-1 text-center rounded-lg p-3"
          style={{ background: 'rgba(244,63,94,0.08)', border: '1px solid rgba(244,63,94,0.2)' }}
        >
          <p className="text-xs mb-1" style={{ color: 'var(--text-muted)' }}>Upper Bound</p>
          <p className="text-xl font-black text-rose-400">{result.confidence_interval?.upper?.toFixed(2)}</p>
          <p className="text-xs text-rose-600 mt-0.5">R⊕</p>
        </div>
      </div>
    </div>

    {/* Info note */}
    <div
      className="rounded-xl p-3 flex items-start gap-2"
      style={{ background: 'rgba(6,182,212,0.06)', border: '1px solid rgba(6,182,212,0.18)' }}
    >
      <Zap className="w-4 h-4 mt-0.5 flex-shrink-0 text-cyan-400" />
      <p className="text-xs leading-relaxed" style={{ color: 'rgba(34,211,238,0.8)' }}>
        The confidence interval represents the range within which the true planetary radius is likely to fall with <strong>95% probability</strong>.
      </p>
    </div>

  </div>
);

/* ── Main Export ── */
const ResultDisplay = ({ result, taskType }) => {
  if (!result) return null;
  return taskType === 'classification'
    ? <ClassificationResult result={result} />
    : <RegressionResult result={result} />;
};

export default ResultDisplay;
