/**
 * Validation utilities for exoplanet features
 */

/**
 * Validate a single feature value
 * @param {string} key - Feature key
 * @param {any} value - Feature value
 * @param {Array} config - Feature configuration
 * @returns {string|null} Error message or null if valid
 */
export const validateFeature = (key, value, config) => {
  // Find feature config
  const featureConfig = config.find(f => f.key === key);
  if (!featureConfig) {
    return `Unknown feature: ${key}`;
  }

  // Check if empty
  if (value === '' || value === null || value === undefined) {
    if (featureConfig.required) {
      return `${featureConfig.name} is required`;
    }
    return null;
  }

  // Parse to number
  const numValue = parseFloat(value);
  if (isNaN(numValue)) {
    return `${featureConfig.name} must be a number`;
  }

  // Check minimum
  if (featureConfig.min !== undefined && numValue < featureConfig.min) {
    return `${featureConfig.name} must be at least ${featureConfig.min}`;
  }

  // Check maximum
  if (featureConfig.max !== undefined && numValue > featureConfig.max) {
    return `${featureConfig.name} must be at most ${featureConfig.max}`;
  }

  return null;
};

/**
 * Validate all features
 * @param {Object} features - Features object
 * @param {Array} config - Feature configuration
 * @returns {Object} Object with errors for each field
 */
export const validateAllFeatures = (features, config) => {
  const errors = {};
  
  for (const feature of config) {
    const value = features[feature.key];
    const error = validateFeature(feature.key, value, config);
    if (error) {
      errors[feature.key] = error;
    }
  }
  
  return errors;
};

/**
 * Check if features are valid
 * @param {Object} features - Features object
 * @param {Array} config - Feature configuration
 * @returns {boolean} True if valid
 */
export const isValidFeatures = (features, config) => {
  const errors = validateAllFeatures(features, config);
  return Object.keys(errors).length === 0;
};

/**
 * Get default feature values
 * @param {Array} config - Feature configuration
 * @returns {Object} Default values
 */
export const getDefaultFeatures = (config) => {
  return config.reduce((acc, f) => ({ ...acc, [f.key]: f.default }), {});
};

/**
 * Validate a number is within range
 * @param {number} value - Value to check
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {boolean} True if valid
 */
export const isInRange = (value, min, max) => {
  const num = parseFloat(value);
  return !isNaN(num) && num >= min && num <= max;
};

/**
 * Validate numeric input
 * @param {any} value - Value to check
 * @returns {boolean} True if valid number
 */
export const isNumeric = (value) => {
  return value !== '' && !isNaN(parseFloat(value)) && isFinite(value);
};
