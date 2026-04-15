import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const COLORS = ['#EA580C', '#2563EB', '#10B981', '#F59E0B', '#6366F1', '#8B5CF6', '#EC4899', '#14B8A6', '#F97316', '#06B6D4'];

const TopAuthorsChart = ({ selectedYear, selectedGenre }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, [selectedYear, selectedGenre]);

  const fetchData = async () => {
    try {
      const response = await axios.get(`${API}/top-authors?n=10`);
      const chartData = response.data.authors.map((author, index) => ({
        author: author.length > 20 ? author.substring(0, 20) + '...' : author,
        count: response.data.counts[index]
      }));
      setData(chartData);
    } catch (error) {
      console.error('Error fetching top authors:', error);
    }
  };

  return (
    <Card data-testid="top-authors-chart" className="bg-white border border-[#E5E7EB] rounded-lg shadow-sm card-hover">
      <CardHeader className="border-b border-[#E5E7EB]">
        <CardTitle className="text-xl font-bold text-[#030712] tracking-tight">Top 10 Authors</CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
            <XAxis 
              dataKey="author" 
              angle={-45} 
              textAnchor="end" 
              height={100}
              tick={{ fill: '#4B5563', fontSize: 11 }}
            />
            <YAxis tick={{ fill: '#4B5563', fontSize: 11 }} />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#FFFFFF', 
                border: '1px solid #E5E7EB',
                borderRadius: '8px',
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
              }}
            />
            <Bar dataKey="count" radius={[4, 4, 0, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};

export default TopAuthorsChart;
