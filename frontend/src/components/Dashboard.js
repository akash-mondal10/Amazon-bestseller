import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { BookOpen, Filter } from 'lucide-react';
import SummaryCards from './SummaryCards';
import TopAuthorsChart from './TopAuthorsChart';
import GenreChart from './GenreChart';
import YearTrendsChart from './YearTrendsChart';
import PriceRatingChart from './PriceRatingChart';
import CorrelationHeatmap from './CorrelationHeatmap';
import BooksTable from './BooksTable';
import InsightsPanel from './InsightsPanel';
import SearchBar from './SearchBar';
import MLPrediction from './MLPrediction';
import ExportButtons from './ExportButtons';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [filterOptions, setFilterOptions] = useState({ years: [], genres: [] });
  const [selectedYear, setSelectedYear] = useState('all');
  const [selectedGenre, setSelectedGenre] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [summaryRes, filterRes] = await Promise.all([
        axios.get(`${API}/summary`),
        axios.get(`${API}/filter-options`)
      ]);
      
      setSummary(summaryRes.data);
      setFilterOptions(filterRes.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#F9FAFB]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-[#EA580C] mx-auto"></div>
          <p className="mt-4 text-lg font-medium text-[#4B5563]">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      {/* Header */}
      <header className="sticky-header py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl sm:text-5xl font-black text-[#030712] tracking-tight leading-none">
                Amazon Bestseller Analyzer
              </h1>
              <p className="mt-2 text-base text-[#4B5563] font-medium leading-relaxed">
                Comprehensive analysis of bestselling books on Amazon
              </p>
            </div>
            <BookOpen className="h-12 w-12 text-[#EA580C]" strokeWidth={2} />
          </div>
          
          {/* Filters */}
          <div className="mt-6 flex flex-wrap gap-4 items-center">
            <div className="flex items-center gap-2">
              <Filter className="h-5 w-5 text-[#4B5563]" strokeWidth={1.5} />
              <span className="text-xs uppercase tracking-widest font-semibold text-[#4B5563]">Filters:</span>
            </div>
            
            <Select value={selectedYear} onValueChange={setSelectedYear}>
              <SelectTrigger data-testid="year-filter-select" className="w-[180px] bg-white border-[#E5E7EB] font-medium">
                <SelectValue placeholder="Select Year" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Years</SelectItem>
                {filterOptions.years.map(year => (
                  <SelectItem key={year} value={year.toString()}>{year}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            
            <Select value={selectedGenre} onValueChange={setSelectedGenre}>
              <SelectTrigger data-testid="genre-filter-select" className="w-[180px] bg-white border-[#E5E7EB] font-medium">
                <SelectValue placeholder="Select Genre" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Genres</SelectItem>
                {filterOptions.genres.map(genre => (
                  <SelectItem key={genre} value={genre}>{genre}</SelectItem>
                ))}
              </SelectContent>
            </Select>

            <div className="flex-1" />
            
            <SearchBar />
            
            <ExportButtons selectedYear={selectedYear} selectedGenre={selectedGenre} />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-6">
          {/* Summary Cards */}
          <SummaryCards summary={summary} />
          
          {/* Insights */}
          <InsightsPanel />
          
          {/* Charts Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* Top Authors - 2 cols */}
            <div className="col-span-1 md:col-span-2">
              <TopAuthorsChart selectedYear={selectedYear} selectedGenre={selectedGenre} />
            </div>
            
            {/* Genre Distribution - 2 cols */}
            <div className="col-span-1 md:col-span-2">
              <GenreChart selectedYear={selectedYear} />
            </div>
            
            {/* Year Trends - 2 cols */}
            <div className="col-span-1 md:col-span-2">
              <YearTrendsChart selectedGenre={selectedGenre} />
            </div>
            
            {/* Price vs Rating - 2 cols */}
            <div className="col-span-1 md:col-span-2">
              <PriceRatingChart selectedYear={selectedYear} selectedGenre={selectedGenre} />
            </div>
            
            {/* Correlation Heatmap - Full width */}
            <div className="col-span-1 md:col-span-4">
              <CorrelationHeatmap />
            </div>
          </div>
          
          {/* ML Predictions */}
          <MLPrediction />
          
          {/* Books Table */}
          <BooksTable selectedYear={selectedYear} selectedGenre={selectedGenre} />
        </div>
      </main>
      
      {/* Footer */}
      <footer className="mt-12 py-6 border-t border-[#E5E7EB]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-[#4B5563]">
          <p>Amazon Bestseller Analyzer © 2024 | Built with React, FastAPI & Python</p>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
