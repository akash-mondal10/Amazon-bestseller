import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Cell } from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PriceRatingChart = ({ selectedYear, selectedGenre }) => {
  const [data, setData] = useState([]);
  const [correlation, setCorrelation] = useState(0);

  useEffect(() => {
    fetchData();
  }, [selectedYear, selectedGenre]);

  const fetchData = async () => {
    try {
      const response = await axios.get(`${API}/price-rating`);
      const chartData = response.data.prices.map((price, index) => ({
        price: price,
        rating: response.data.ratings[index],
        name: response.data.names[index],
        genre: response.data.genres[index]
      }));
      setData(chartData);
      setCorrelation(response.data.correlation);
    } catch (error) {
      console.error('Error fetching price-rating data:', error);
    }
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-[#E5E7EB] rounded-lg shadow-lg">
          <p className="font-semibold text-[#030712] text-sm">{payload[0].payload.name}</p>
          <p className="text-xs text-[#4B5563]">Genre: {payload[0].payload.genre}</p>
          <p className="text-xs text-[#4B5563]">Price: ${payload[0].value}</p>
          <p className="text-xs text-[#4B5563]">Rating: {payload[1].value}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card data-testid="price-rating-chart" className="bg-white border border-[#E5E7EB] rounded-lg shadow-sm card-hover">
      <CardHeader className="border-b border-[#E5E7EB]">
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-bold text-[#030712] tracking-tight">Price vs Rating</CardTitle>
          <span className="text-xs bg-orange-100 text-[#EA580C] px-3 py-1 rounded-full font-semibold">
            Correlation: {correlation.toFixed(3)}
          </span>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        <ResponsiveContainer width="100%" height={350}>
          <ScatterChart margin={{ top: 10, right: 30, left: 0, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
            <XAxis 
              type="number" 
              dataKey="price" 
              name="Price" 
              unit="$"
              tick={{ fill: '#4B5563', fontSize: 11 }}
              label={{ value: 'Price ($)', position: 'insideBottom', offset: -5, fill: '#4B5563' }}
            />
            <YAxis 
              type="number" 
              dataKey="rating" 
              name="Rating"
              tick={{ fill: '#4B5563', fontSize: 11 }}
              label={{ value: 'User Rating', angle: -90, position: 'insideLeft', fill: '#4B5563' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Scatter name="Books" data={data} fill="#EA580C" opacity={0.6}>
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.genre === 'Fiction' ? '#EA580C' : '#2563EB'} 
                />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
        <div className="flex gap-4 justify-center mt-4">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-[#EA580C]"></div>
            <span className="text-xs text-[#4B5563] font-medium">Fiction</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-[#2563EB]"></div>
            <span className="text-xs text-[#4B5563] font-medium">Non Fiction</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PriceRatingChart;
