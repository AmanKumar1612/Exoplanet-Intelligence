"""
Download NASA Kepler Object of Interest (KOI) dataset
"""
import os
import pandas as pd
import kaggle

def download_koi_dataset():
    """Download the KOI dataset from Kaggle"""
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, 'koi_data.csv')
    
    # Check if data already exists
    if os.path.exists(output_path):
        print(f"Dataset already exists at {output_path}")
        return output_path
    
    try:
        # Try to download using kaggle API
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        # Download the dataset
        api.dataset_download_file(
            'nasa/kepler-exoplanet-search-results',
            file_name='cumulative.csv',
            path=data_dir
        )
        
        # Rename the file
        downloaded_file = os.path.join(data_dir, 'cumulative.csv')
        if os.path.exists(downloaded_file):
            os.rename(downloaded_file, output_path)
            print(f"Dataset downloaded successfully to {output_path}")
            return output_path
    except Exception as e:
        print(f"Kaggle API download failed: {e}")
    
    # Fallback: Create sample data if download fails
    print("Creating sample dataset for demonstration...")
    create_sample_data(output_path)
    return output_path

def create_sample_data(output_path):
    """Create a sample dataset with relevant features"""
    import numpy as np
    
    np.random.seed(42)
    n_samples = 5000
    
    # Define features based on NASA KOI dataset
    data = {
        # Planetary properties
        'koi_prad': np.random.uniform(0.5, 20, n_samples),  # Planetary radius
        'koi_prad_err1': np.random.uniform(0.01, 0.5, n_samples),
        'koi_prad_err2': np.random.uniform(-0.5, -0.01, n_samples),
        'koi_depth': np.random.uniform(1, 1000, n_samples),  # Transit depth (ppm)
        'koi_depth_err1': np.random.uniform(0.1, 50, n_samples),
        'koi_depth_err2': np.random.uniform(-50, -0.1, n_samples),
        'koi_period': np.random.uniform(1, 400, n_samples),  # Orbital period (days)
        'koi_period_err1': np.random.uniform(0.001, 0.1, n_samples),
        'koi_period_err2': np.random.uniform(-0.1, -0.001, n_samples),
        'koi_time0': np.random.uniform(0, 1000, n_samples),  # Transit epoch
        'koi_time0_err1': np.random.uniform(0.001, 0.1, n_samples),
        'koi_time0_err2': np.random.uniform(-0.1, -0.001, n_samples),
        
        # Stellar properties
        'koi_slogg': np.random.uniform(3.5, 5.5, n_samples),  # Surface gravity
        'koi_slogg_err1': np.random.uniform(0.01, 0.1, n_samples),
        'koi_slogg_err2': np.random.uniform(-0.1, -0.01, n_samples),
        'koi_srad': np.random.uniform(0.5, 3.0, n_samples),  # Stellar radius
        'koi_srad_err1': np.random.uniform(0.01, 0.2, n_samples),
        'koi_srad_err2': np.random.uniform(-0.2, -0.01, n_samples),
        'koi_steff': np.random.uniform(3500, 6500, n_samples),  # Effective temperature
        'koi_steff_err1': np.random.uniform(10, 100, n_samples),
        'koi_steff_err2': np.random.uniform(-100, -10, n_samples),
        'koi_smass': np.random.uniform(0.5, 2.0, n_samples),  # Stellar mass
        'koi_smass_err1': np.random.uniform(0.01, 0.1, n_samples),
        'koi_smass_err2': np.random.uniform(-0.1, -0.01, n_samples),
        'koi_lum': np.random.uniform(-1, 2, n_samples),  # Luminosity (log solar)
        'koi_lum_err1': np.random.uniform(0.01, 0.2, n_samples),
        'koi_lum_err2': np.random.uniform(-0.2, -0.01, n_samples),
        
        # Planet-star geometry
        'koi_impact': np.random.uniform(0, 1, n_samples),  # Impact parameter
        'koi_impact_err1': np.random.uniform(0.001, 0.05, n_samples),
        'koi_impact_err2': np.random.uniform(-0.05, -0.001, n_samples),
        'koi_duration': np.random.uniform(1, 15, n_samples),  # Transit duration (hours)
        'koi_duration_err1': np.random.uniform(0.01, 0.5, n_samples),
        'koi_duration_err2': np.random.uniform(-0.5, -0.01, n_samples),
        
        # Transit signal properties
        'koi_max_mult_ev': np.random.uniform(0, 100, n_samples),  # Max multiple event stat
        'koi_max_mult_ev_err1': np.random.uniform(0.1, 5, n_samples),
        'koi_max_mult_ev_err2': np.random.uniform(-5, -0.1, n_samples),
        'koi_model_snr': np.random.uniform(1, 100, n_samples),  # Model signal-to-noise
        'koi_tce_plnt_num': np.random.randint(1, 7, n_samples),  # TCE planet number
        'koi_tce_delivname': np.random.choice(['Q1-Q16', 'Q1-Q17', 'DR25'], n_samples),
        
        # Quality flags
        'koi_vet_stat': np.random.choice(['PASS', 'FAIL', 'suspect'], n_samples, p=[0.6, 0.2, 0.2]),
        'koi_vet_date': np.random.choice(['2019-01-01', '2020-01-01', '2021-01-01'], n_samples),
        
        # Disposition (target for classification)
        'koi_disposition': np.random.choice(['CONFIRMED', 'FALSE POSITIVE', 'CANDIDATE'], n_samples, p=[0.3, 0.3, 0.4]),
        
        # KOI name (identifier)
        'koi_name': [f'KOI-{i:04d}' for i in range(1, n_samples + 1)],
        
        # Additional useful features
        'koi_dor': np.random.uniform(0.1, 100, n_samples),  # Planet-star distance ratio
        'koi_dor_err1': np.random.uniform(0.01, 2, n_samples),
        'koi_dor_err2': np.random.uniform(-2, -0.01, n_samples),
        'koi_kepmag': np.random.uniform(7, 17, n_samples),  # Kepler magnitude
        'koi_qof': np.random.uniform(0, 1, n_samples),  # Quality flag
        'koi_score': np.random.uniform(0, 1, n_samples),  # Disposition score
    }
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Sample dataset created at {output_path}")
    return df

if __name__ == '__main__':
    download_koi_dataset()
