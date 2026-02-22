import React, { useState } from 'react';
import { HelpCircle, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { validateFeature, validateAllFeatures } from '../utils/validation';
import Tooltip from './Tooltip';

const FEATURE_CONFIG = [
  { key: 'koi_prad', name: 'Planetary Radius', unit: 'R⊕', min: 0.1, max: 30, default: 2.0, description: 'Radius of the planet in Earth radii' },
  { key: 'koi_depth', name: 'Transit Depth', unit: 'ppm', min: 0, max: 10000, default: 100, description: 'Depth of the transit in parts per million' },
  { key: 'koi_period', name: 'Orbital Period', unit: 'days', min: 0.1, max: 1000, default: 50, description: 'Time between successive transits' },
  { key: 'koi_srad', name: 'Stellar Radius', unit: 'R☉', min: 0.1, max: 10, default: 1.0, description: 'Radius of the host star in solar radii' },
  { key: 'koi_steff', name: 'Stellar Temperature', unit: 'K', min: 2500, max: 10000, default: 5778, description: 'Effective temperature of the host star' },
  { key: 'koi_smass', name: 'Stellar Mass', unit: 'M☉', min: 0.1, max: 5, default: 1.0, description: 'Mass of the host star in solar masses' },
  { key: 'koi_slogg', name: 'Surface Gravity', unit: 'log(g)', min: 1, max: 5, default: 4.5, description: 'Surface gravity of the host star' },
  { key: 'koi_lum', name: 'Luminosity', unit: 'log(L☉)', min: -3, max: 5, default: 0, description: 'Luminosity of the host star' },
  { key: 'koi_impact', name: 'Impact Parameter', unit: '', min: 0, max: 2, default: 0.5, description: 'Impact parameter of the transit' },
  { key: 'koi_duration', name: 'Transit Duration', unit: 'hours', min: 0.1, max: 50, default: 3, description: 'Duration of the transit' },
  { key: 'koi_dor', name: 'Distance Ratio', unit: 'a/R★', min: 1, max: 200, default: 20, description: 'Planet-star distance ratio (a/R*)' },
  { key: 'koi_model_snr', name: 'Signal-to-Noise', unit: 'SNR', min: 0, max: 500, default: 20, description: 'Model signal-to-noise ratio' },
  { key: 'koi_kepmag', name: 'Kepler Magnitude', unit: 'mag', min: 5, max: 20, default: 14, description: 'Kepler magnitude of the target' },
  { key: 'koi_score', name: 'Disposition Score', unit: '0-1', min: 0, max: 1, default: 0.5, description: 'Probability score for planet disposition' },
  { key: 'koi_qof', name: 'Quality Flag', unit: '0-1', min: 0, max: 1, default: 0.9, description: 'Quality flag for the KOI (usually close to 1)' },
];

const InputForm = ({ taskType, onSubmit, isLoading }) => {
  const [features, setFeatures] = useState(
    FEATURE_CONFIG.reduce((acc, f) => ({ ...acc, [f.key]: f.default }), {})
  );
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const handleChange = (key, value) => {
    setFeatures(prev => ({ ...prev, [key]: value }));
    if (errors[key]) setErrors(prev => ({ ...prev, [key]: null }));
  };

  const handleBlur = (key) => {
    setTouched(prev => ({ ...prev, [key]: true }));
    const error = validateFeature(key, features[key], FEATURE_CONFIG);
    if (error) setErrors(prev => ({ ...prev, [key]: error }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const allErrors = validateAllFeatures(features, FEATURE_CONFIG);
    setErrors(allErrors);
    setTouched(FEATURE_CONFIG.reduce((acc, f) => ({ ...acc, [f.key]: true }), {}));
    if (Object.keys(allErrors).length === 0) onSubmit(features);
  };

  const fieldState = (key) => {
    if (!touched[key]) return 'neutral';
    return errors[key] ? 'error' : 'valid';
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {FEATURE_CONFIG.map((feature, idx) => {
          const state = fieldState(feature.key);
          return (
            <div
              key={feature.key}
              className="animate-fade-in"
              style={{ animationDelay: `${idx * 0.02}s` }}
            >
              {/* Label */}
              <label className="block mb-1.5">
                <div className="flex items-center gap-1.5 text-sm font-semibold" style={{ color: '#c7d2fe' }}>
                  {feature.name}
                  <Tooltip content={feature.description}>
                    <HelpCircle className="w-3.5 h-3.5 cursor-help" style={{ color: 'var(--text-muted)' }} />
                  </Tooltip>
                </div>
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
                  {feature.unit ? `${feature.unit} · ` : ''}Range: {feature.min}–{feature.max}
                </span>
              </label>

              {/* Input wrapper */}
              <div className="relative">
                <input
                  type="number"
                  step="any"
                  value={features[feature.key]}
                  onChange={(e) => handleChange(feature.key, e.target.value)}
                  onBlur={() => handleBlur(feature.key)}
                  className={`input-field pr-10 ${state === 'error' ? 'border-red-500' : state === 'valid' ? 'border-green-500' : ''
                    }`}
                  placeholder={`e.g. ${feature.default}`}
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2">
                  {state === 'valid' && (
                    <CheckCircle
                      className="w-4 h-4 text-emerald-400"
                      style={{ filter: 'drop-shadow(0 0 4px rgba(52,211,153,0.7))' }}
                    />
                  )}
                  {state === 'error' && (
                    <AlertCircle
                      className="w-4 h-4 text-rose-400"
                      style={{ filter: 'drop-shadow(0 0 4px rgba(251,113,133,0.7))' }}
                    />
                  )}
                </span>
              </div>

              {/* Error message */}
              {errors[feature.key] && (
                <p className="mt-1 text-xs text-rose-400">{errors[feature.key]}</p>
              )}
            </div>
          );
        })}
      </div>

      {/* Submit */}
      <div className="flex justify-center pt-4">
        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
          style={{ minWidth: '200px', justifyContent: 'center' }}
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Processing…</span>
            </>
          ) : (
            <>
              <CheckCircle className="w-5 h-5" />
              <span>
                {taskType === 'classification' ? 'Predict Classification' : 'Predict Radius'}
              </span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default InputForm;
