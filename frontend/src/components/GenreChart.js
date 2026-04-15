import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const COLORS = ['#EA580C', '#2563EB'];

const GenreChart = ({ selectedYear }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, [selectedYear]);

  const fetchData = async () => {
    try {
      const response = await axios.get(`${API}/genre-distribution`);
      const chartData = response.data.genres.map((genre, index) => ({
        name: genre,
        value: response.data.counts[index],
        percentage: response.data.percentages[index]
      }));
      setData(chartData);
    } catch (error) {
      console.error('Error fetching genre distribution:', error);
    }
  };

  const renderLabel = (entry) => {
    return `${entry.name}: ${entry.percentage.toFixed(1)}%`;
  };

  return (
    <Card data-testid="genre-chart" className="bg-white border border-[#E5E7EB] rounded-lg shadow-sm card-hover">
      <CardHeader className="border-b border-[#E5E7EB]">
        <CardTitle className="text-xl font-bold text-[#030712] tracking-tight">Genre Distribution</CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <ResponsiveContainer width="100%" height={350}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderLabel}
              outerRadius={110}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#FFFFFF', 
                border: '1px solid #E5E7EB',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default GenreChart;
