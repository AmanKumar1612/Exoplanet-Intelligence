-- Exoplanet Intelligence System Database Schema
-- PostgreSQL via Supabase

-- Create predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    task_type VARCHAR(50) NOT NULL CHECK (task_type IN ('classification', 'regression')),
    input_features JSONB NOT NULL,
    output_result JSONB NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on task_type for faster filtering
CREATE INDEX IF NOT EXISTS idx_predictions_task_type ON predictions(task_type);

-- Create index on created_at for faster sorting
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Create policy for public read access
CREATE POLICY "Allow public read access" ON predictions
    FOR SELECT USING (true);

-- Create policy for insert access
CREATE POLICY "Allow insert access" ON predictions
    FOR INSERT WITH CHECK (true);

-- Create policy for update access
CREATE POLICY "Allow update access" ON predictions
    FOR UPDATE USING (true);

-- Create policy for delete access
CREATE POLICY "Allow delete access" ON predictions
    FOR DELETE USING (true);

-- Optional: Create a table for API usage statistics
CREATE TABLE IF NOT EXISTS api_usage (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(100) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    user_agent TEXT,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on endpoint
CREATE INDEX IF NOT EXISTS idx_api_usage_endpoint ON api_usage(endpoint);

-- Create index on created_at
CREATE INDEX IF NOT EXISTS idx_api_usage_created_at ON api_usage(created_at DESC);

-- Enable RLS for api_usage
ALTER TABLE api_usage ENABLE ROW LEVEL SECURITY;

-- Create policy for api_usage
CREATE POLICY "Allow api_usage access" ON api_usage
    FOR ALL USING (true);
