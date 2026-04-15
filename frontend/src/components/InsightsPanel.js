import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Lightbulb } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const InsightsPanel = () => {
  const [insights, setInsights] = useState([]);

  useEffect(() => {
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    try {
      const response = await axios.get(`${API}/insights`);
      setInsights(response.data.insights);
    } catch (error) {
      console.error('Error fetching insights:', error);
    }
  };

  return (
    <Card data-testid="insights-panel" className="bg-white border border-[#E5E7EB] rounded-lg shadow-sm">
      <CardHeader className="border-b border-[#E5E7EB]">
        <div className="flex items-center gap-3">
          <Lightbulb className="h-6 w-6 text-[#EA580C]" strokeWidth={1.5} />
          <CardTitle className="text-2xl font-bold text-[#030712] tracking-tight">Key Insights</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {insights.map((insight, index) => (
            <div
              key={index}
              data-testid={`insight-item-${index}`}
              className="flex gap-3 p-4 bg-[#F9FAFB] rounded-lg border border-[#E5E7EB]"
            >
              <div className="flex-shrink-0">
                <span className="inline-flex items-center justify-center h-8 w-8 rounded-full bg-[#EA580C] text-white text-sm font-bold">
                  {index + 1}
                </span>
              </div>
              <p className="text-sm text-[#030712] leading-relaxed font-medium">{insight}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default InsightsPanel;
