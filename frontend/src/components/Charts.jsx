import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, LineChart, Line, AreaChart, Area } from 'recharts';

const ClassificationChart = ({ probabilities }) => {
  const data = [
    { name: 'CONFIRMED', value: probabilities?.CONFIRMED || 0, color: '#22c55e' },
    { name: 'FALSE POSITIVE', value: probabilities?.['FALSE POSITIVE'] || 0, color: '#ef4444' },
  ];

  return (
    <div className="card p-6 animate-fade-in">
      <h3 className="text-xl font-bold mb-4">Probability Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis type="number" domain={[0, 1]} stroke="#9ca3af" />
          <YAxis type="category" dataKey="name" stroke="#9ca3af" width={100} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
            formatter={(value) => [`${(value * 100).toFixed(1)}%`, 'Probability']}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const RegressionChart = ({ prediction, confidenceInterval }) => {
  // Create data for visualization
  const center = prediction || 2.5;
  const lower = confidenceInterval?.lower || (center - 0.5);
  const upper = confidenceInterval?.upper || (center + 0.5);
  
  const data = [
    { name: 'Lower', value: lower, type: 'CI' },
    { name: 'Prediction', value: center, type: 'Prediction' },
    { name: 'Upper', value: upper, type: 'CI' },
  ];

  return (
    <div className="card p-6 animate-fade-in">
      <h3 className="text-xl font-bold mb-4">Prediction with Confidence Interval</h3>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="name" stroke="#9ca3af" />
          <YAxis stroke="#9ca3af" domain={['auto', 'auto']} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
            formatter={(value) => [`${value.toFixed(2)} Earth radii`, 'Radius']}
          />
          <Area 
            type="monotone" 
            dataKey="value" 
            stroke="#6366f1" 
            fillOpacity={1} 
            fill="url(#colorValue)" 
          />
          <Line type="monotone" dataKey="value" stroke="#8b5cf6" strokeWidth={2} dot={{ fill: '#8b5cf6', strokeWidth: 2 }} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

const Charts = ({ result, taskType }) => {
  if (!result) return null;

  return (
    <div className="space-y-6">
      {taskType === 'classification' ? (
        <ClassificationChart probabilities={result.probabilities} />
      ) : (
        <RegressionChart 
          prediction={result.prediction} 
          confidenceInterval={result.confidence_interval} 
        />
      )}
    </div>
  );
};

export default Charts;
