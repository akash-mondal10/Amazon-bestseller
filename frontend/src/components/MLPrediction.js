import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Brain, TrendingUp, Star, Zap } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MLPrediction = () => {
  const [price, setPrice] = useState('14');
  const [year, setYear] = useState('2020');
  const [genre, setGenre] = useState('Fiction');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [modelInfo, setModelInfo] = useState(null);

  const handlePredict = async () => {
    if (!price || !year) return;
    setLoading(true);
    try {
      const response = await axios.post(`${API}/ml/predict`, {
        price: parseFloat(price),
        year: parseInt(year),
        genre: genre
      });
      setPrediction(response.data);
    } catch (error) {
      console.error('Prediction error:', error);
    }
    setLoading(false);
  };

  const fetchModelInfo = async () => {
    try {
      const response = await axios.get(`${API}/ml/info`);
      setModelInfo(response.data);
    } catch (error) {
      console.error('Error fetching model info:', error);
    }
  };

  React.useEffect(() => {
    fetchModelInfo();
  }, []);

  return (
    <Card data-testid="ml-prediction-panel" className="bg-white border border-[#E5E7EB] rounded-lg shadow-sm">
      <CardHeader className="border-b border-[#E5E7EB]">
        <div className="flex items-center gap-3">
          <Brain className="h-6 w-6 text-[#6366F1]" strokeWidth={1.5} />
          <CardTitle className="text-2xl font-bold text-[#030712] tracking-tight">ML Predictions</CardTitle>
        </div>
        <p className="text-sm text-[#4B5563] mt-1">Predict if a book will be a bestseller and its likely rating</p>
      </CardHeader>
      <CardContent className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase tracking-widest text-[#4B5563]">Enter Book Details</h3>

            <div>
              <label className="text-sm font-medium text-[#030712] mb-1 block">Price ($)</label>
              <Input
                data-testid="ml-price-input"
                type="number"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                placeholder="e.g. 14"
                className="bg-white border-[#E5E7EB]"
                min="1"
                max="50"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-[#030712] mb-1 block">Publication Year</label>
              <Input
                data-testid="ml-year-input"
                type="number"
                value={year}
                onChange={(e) => setYear(e.target.value)}
                placeholder="e.g. 2020"
                className="bg-white border-[#E5E7EB]"
                min="2000"
                max="2025"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-[#030712] mb-1 block">Genre</label>
              <Select value={genre} onValueChange={setGenre}>
                <SelectTrigger data-testid="ml-genre-select" className="bg-white border-[#E5E7EB]">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Fiction">Fiction</SelectItem>
                  <SelectItem value="Non Fiction">Non Fiction</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <button
              data-testid="ml-predict-button"
              onClick={handlePredict}
              disabled={loading}
              className="w-full bg-[#6366F1] text-white hover:bg-indigo-700 font-medium px-4 py-3 rounded-md transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <Zap className="h-4 w-4" />
              {loading ? 'Predicting...' : 'Run Prediction'}
            </button>
          </div>

          {/* Results */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold uppercase tracking-widest text-[#4B5563]">Prediction Results</h3>

            {prediction ? (
              <div className="space-y-4">
                {/* Bestseller Prediction */}
                <div data-testid="bestseller-result" className={`p-4 rounded-lg border ${
                  prediction.bestseller_prediction.is_bestseller
                    ? 'bg-green-50 border-green-200'
                    : 'bg-orange-50 border-orange-200'
                }`}>
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className={`h-5 w-5 ${
                      prediction.bestseller_prediction.is_bestseller ? 'text-green-600' : 'text-orange-600'
                    }`} />
                    <span className="font-bold text-[#030712]">Bestseller Prediction</span>
                  </div>
                  <p className={`text-2xl font-black ${
                    prediction.bestseller_prediction.is_bestseller ? 'text-green-700' : 'text-orange-700'
                  }`}>
                    {prediction.bestseller_prediction.is_bestseller ? 'Likely Bestseller' : 'Moderate Potential'}
                  </p>
                  <div className="flex gap-4 mt-2 text-sm">
                    <span className="text-[#4B5563]">
                      Probability: <strong>{(prediction.bestseller_prediction.probability * 100).toFixed(1)}%</strong>
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                      prediction.bestseller_prediction.confidence === 'High' ? 'bg-green-200 text-green-800' :
                      prediction.bestseller_prediction.confidence === 'Medium' ? 'bg-yellow-200 text-yellow-800' :
                      'bg-red-200 text-red-800'
                    }`}>
                      {prediction.bestseller_prediction.confidence} Confidence
                    </span>
                  </div>
                </div>

                {/* Rating Prediction */}
                <div data-testid="rating-result" className="p-4 rounded-lg border bg-blue-50 border-blue-200">
                  <div className="flex items-center gap-2 mb-2">
                    <Star className="h-5 w-5 text-blue-600" />
                    <span className="font-bold text-[#030712]">Rating Prediction</span>
                  </div>
                  <p className="text-2xl font-black text-blue-700">
                    {prediction.rating_prediction.predicted_rating} / 5.0
                  </p>
                  <p className="text-sm text-[#4B5563] mt-1">
                    Category: <strong>{prediction.rating_prediction.rating_category}</strong>
                  </p>
                </div>
              </div>
            ) : (
              <div className="p-8 rounded-lg border border-dashed border-[#E5E7EB] text-center">
                <Brain className="h-12 w-12 text-[#E5E7EB] mx-auto mb-3" />
                <p className="text-sm text-[#4B5563]">Enter book details and click "Run Prediction" to see results</p>
              </div>
            )}

            {/* Model Info */}
            {modelInfo && (
              <div className="p-3 rounded-lg bg-[#F9FAFB] border border-[#E5E7EB]">
                <p className="text-xs font-semibold uppercase tracking-widest text-[#4B5563] mb-2">Model Performance</p>
                <div className="grid grid-cols-2 gap-2 text-xs text-[#4B5563]">
                  <span>Classification Accuracy: <strong>{(modelInfo.classification.metrics.accuracy * 100).toFixed(1)}%</strong></span>
                  <span>Regression R2: <strong>{modelInfo.regression.metrics.r2_score.toFixed(3)}</strong></span>
                </div>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default MLPrediction;
