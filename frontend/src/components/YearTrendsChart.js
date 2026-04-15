import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const YearTrendsChart = ({ selectedGenre }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, [selectedGenre]);

  const fetchData = async () => {
    try {
      const response = await axios.get(`${API}/year-trends`);
      const chartData = response.data.years.map((year, index) => ({
        year: year,
        books: response.data.book_counts[index],
        rating: response.data.avg_ratings[index],
        price: response.data.avg_prices[index]
      }));
      setData(chartData);
    } catch (error) {
      console.error('Error fetching year trends:', error);
    }
  };

  return (
    <Card data-testid="year-trends-chart" className="bg-white border border-[#E5E7EB] rounded-lg shadow-sm card-hover">
      <CardHeader className="border-b border-[#E5E7EB]">
        <CardTitle className="text-xl font-bold text-[#030712] tracking-tight">Year-wise Trends</CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
            <XAxis dataKey="year" tick={{ fill: '#4B5563', fontSize: 11 }} />
            <YAxis yAxisId="left" tick={{ fill: '#4B5563', fontSize: 11 }} />
            <YAxis yAxisId="right" orientation="right" tick={{ fill: '#4B5563', fontSize: 11 }} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#FFFFFF', 
                border: '1px solid #E5E7EB',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Legend verticalAlign="top" height={36} />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="books" 
              stroke="#EA580C" 
              strokeWidth={3}
              dot={{ fill: '#EA580C', r: 5 }}
              name="Book Count"
            />
            <Line 
              yAxisId="right"
              type="monotone" 
              dataKey="rating" 
              stroke="#2563EB" 
              strokeWidth={3}
              dot={{ fill: '#2563EB', r: 5 }}
              name="Avg Rating"
            />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default YearTrendsChart;
