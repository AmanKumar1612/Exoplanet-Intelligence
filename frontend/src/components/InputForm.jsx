import React, { useState } from 'react';
import { HelpCircle, AlertCircle, CheckCircle } from 'lucide-react';
import { validateFeature, validateAllFeatures } from '../utils/validation';
import Tooltip from './Tooltip';

const FEATURE_CONFIG = [
  { key: 'koi_prad', name: 'Planetary Radius', unit: 'Earth radii', min: 0.1, max: 30, default: 2.0, description: 'Radius of the planet in Earth radii' },
  { key: 'koi_depth', name: 'Transit Depth', unit: 'ppm', min: 0, max: 10000, default: 100, description: 'Depth of the transit in parts per million' },
  { key: 'koi_period', name: 'Orbital Period', unit: 'days', min: 0.1, max: 1000, default: 50, description: 'Time between successive transits' },
  { key: 'koi_srad', name: 'Stellar Radius', unit: 'Solar radii', min: 0.1, max: 10, default: 1.0, description: 'Radius of the host star in solar radii' },
  { key: 'koi_steff', name: 'Stellar Temperature', unit: 'Kelvin', min: 2500, max: 10000, default: 5778, description: 'Effective temperature of the host star' },
  { key: 'koi_smass', name: 'Stellar Mass', unit: 'Solar masses', min: 0.1, max: 5, default: 1.0, description: 'Mass of the host star in solar masses' },
  { key: 'koi_slogg', name: 'Surface Gravity', unit: 'log(g)', min: 1, max: 5, default: 4.5, description: 'Surface gravity of the host star' },
  { key: 'koi_lum', name: 'Luminosity', unit: 'log(L☉)', min: -3, max: 5, default: 0, description: 'Luminosity of the host star' },
  { key: 'koi_impact', name: 'Impact Parameter', unit: '', min: 0, max: 2, default: 0.5, description: 'Impact parameter of the transit' },
  { key: 'koi_duration', name: 'Transit Duration', unit: 'hours', min: 0.1, max: 50, default: 3, description: 'Duration of the transit' },
  { key: 'koi_dor', name: 'Distance Ratio', unit: '', min: 1, max: 200, default: 20, description: 'Planet-star distance ratio (a/R*)' },
  { key: 'koi_model_snr', name: 'Signal-to-Noise', unit: '', min: 0, max: 500, default: 20, description: 'Model signal-to-noise ratio' },
  { key: 'koi_kepmag', name: 'Kepler Magnitude', unit: 'mag', min: 5, max: 20, default: 14, description: 'Kepler magnitude of the target' },
  { key: 'koi_score', name: 'Disposition Score', unit: '', min: 0, max: 1, default: 0.5, description: 'Probability score for planet disposition' },
  { key: 'koi_qof', name: 'Quality Flag', unit: '', min: 0, max: 1, default: 0.9, description: 'Quality flag for the KOI (usually close to 1)' },
];

const InputForm = ({ taskType, onSubmit, isLoading }) => {
  const [features, setFeatures] = useState(
    FEATURE_CONFIG.reduce((acc, f) => ({ ...acc, [f.key]: f.default }), {})
  );
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const handleChange = (key, value) => {
    setFeatures(prev => ({ ...prev, [key]: value }));

    // Clear error when user types
    if (errors[key]) {
      setErrors(prev => ({ ...prev, [key]: null }));
    }
  };

  const handleBlur = (key) => {
    setTouched(prev => ({ ...prev, [key]: true }));
    const error = validateFeature(key, features[key], FEATURE_CONFIG);
    if (error) {
      setErrors(prev => ({ ...prev, [key]: error }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate all features
    const allErrors = validateAllFeatures(features, FEATURE_CONFIG);
    setErrors(allErrors);
    setTouched(FEATURE_CONFIG.reduce((acc, f) => ({ ...acc, [f.key]: true }), {}));

    if (Object.keys(allErrors).length === 0) {
      onSubmit(features);
    }
  };

  const getFieldClass = (key) => {
    if (!touched[key]) return 'input-field';
    return errors[key] ? 'input-field border-red-500' : 'input-field border-green-500';
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {FEATURE_CONFIG.map((feature) => (
          <div key={feature.key} className="relative">
            <label className="block text-sm font-medium text-gray-300 mb-2">
              <div className="flex items-center gap-2">
                {feature.name}
                <Tooltip content={feature.description}>
                  <HelpCircle className="w-4 h-4 text-gray-500 cursor-help" />
                </Tooltip>
              </div>
              <span className="text-xs text-gray-500">
                {feature.unit ? `(${feature.unit})` : ''} • Range: {feature.min} - {feature.max}
              </span>
            </label>

            <div className="relative">
              <input
                type="number"
                step="any"
                value={features[feature.key]}
                onChange={(e) => handleChange(feature.key, e.target.value)}
                onBlur={() => handleBlur(feature.key)}
                className={getFieldClass(feature.key)}
                placeholder={`Enter ${feature.name.toLowerCase()}`}
              />

              {touched[feature.key] && !errors[feature.key] && (
                <CheckCircle className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-green-500" />
              )}

              {errors[feature.key] && (
                <AlertCircle className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-red-500" />
              )}
            </div>

            {errors[feature.key] && (
              <p className="mt-1 text-sm text-red-500">{errors[feature.key]}</p>
            )}
          </div>
        ))}
      </div>

      <div className="flex justify-center mt-8">
        <button
          type="submit"
          disabled={isLoading}
          className={`btn-primary flex items-center gap-2 ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Processing...
            </>
          ) : (
            <>
              <CheckCircle className="w-5 h-5" />
              {taskType === 'classification' ? 'Predict Classification' : 'Predict Radius'}
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default InputForm;
