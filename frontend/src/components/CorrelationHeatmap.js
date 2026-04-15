import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CorrelationHeatmap = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get(`${API}/correlation`);
      setData(response.data);
    } catch (error) {
      console.error('Error fetching correlation data:', error);
    }
  };

  const getColor = (value) => {
    const absValue = Math.abs(value);
    if (value > 0) {
      const intensity = Math.round(absValue * 255);
      return `rgb(${255}, ${255 - intensity}, ${255 - intensity})`;
    } else {
      const intensity = Math.round(absValue * 255);
      return `rgb(${255 - intensity}, ${255 - intensity}, ${255})`;
    }
  };

  if (!data) return null;

  return (
    <Card data-testid="correlation-heatmap" className="bg-white border border-[#E5E7EB] rounded-lg shadow-sm card-hover">
      <CardHeader className="border-b border-[#E5E7EB]">
        <CardTitle className="text-xl font-bold text-[#030712] tracking-tight">Correlation Matrix</CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <div className="overflow-x-auto">
          <table className="w-full border-collapse">
            <thead>
              <tr>
                <th className="border border-[#E5E7EB] p-3 bg-[#F9FAFB] text-xs uppercase tracking-widest font-semibold text-[#4B5563]"></th>
                {data.columns.map((col, index) => (
                  <th key={index} className="border border-[#E5E7EB] p-3 bg-[#F9FAFB] text-xs uppercase tracking-widest font-semibold text-[#4B5563]">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.matrix.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  <td className="border border-[#E5E7EB] p-3 bg-[#F9FAFB] text-xs uppercase tracking-widest font-semibold text-[#4B5563]">
                    {data.columns[rowIndex]}
                  </td>
                  {row.map((value, colIndex) => (
                    <td
                      key={colIndex}
                      className="border border-[#E5E7EB] p-3 text-center font-bold text-sm"
                      style={{ backgroundColor: getColor(value) }}
                    >
                      {value.toFixed(3)}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-4 flex items-center justify-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-12 h-4 bg-gradient-to-r from-blue-100 to-blue-600"></div>
            <span className="text-xs text-[#4B5563] font-medium">Negative</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-12 h-4 bg-gradient-to-r from-red-100 to-red-600"></div>
            <span className="text-xs text-[#4B5563] font-medium">Positive</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CorrelationHeatmap;
