import React, { useState } from 'react';
import axios from 'axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Search, X } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SearchBar = ({ onSearchResults }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = async (value) => {
    setQuery(value);
    if (value.trim().length < 2) {
      setResults([]);
      setShowResults(false);
      return;
    }
    
    setSearching(true);
    try {
      const response = await axios.get(`${API}/search?q=${encodeURIComponent(value)}&limit=10`);
      setResults(response.data.results);
      setShowResults(true);
    } catch (error) {
      console.error('Search error:', error);
    }
    setSearching(false);
  };

  const clearSearch = () => {
    setQuery('');
    setResults([]);
    setShowResults(false);
  };

  return (
    <div className="relative w-full max-w-md" data-testid="search-bar">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#4B5563]" strokeWidth={1.5} />
        <Input
          data-testid="search-input"
          type="text"
          placeholder="Search books or authors..."
          value={query}
          onChange={(e) => handleSearch(e.target.value)}
          className="pl-10 pr-10 bg-white border-[#E5E7EB] font-medium h-10"
        />
        {query && (
          <button onClick={clearSearch} className="absolute right-3 top-1/2 -translate-y-1/2" data-testid="search-clear">
            <X className="h-4 w-4 text-[#4B5563] hover:text-[#030712]" />
          </button>
        )}
      </div>

      {showResults && results.length > 0 && (
        <Card className="absolute top-12 left-0 right-0 z-50 shadow-lg border border-[#E5E7EB] max-h-80 overflow-y-auto">
          <CardContent className="p-2">
            <p className="text-xs text-[#4B5563] px-3 py-1 font-semibold uppercase tracking-widest">
              {results.length} result{results.length !== 1 ? 's' : ''} found
            </p>
            {results.map((book, index) => (
              <div
                key={index}
                data-testid={`search-result-${index}`}
                className="px-3 py-2 hover:bg-[#F9FAFB] rounded-md cursor-pointer transition-colors"
              >
                <p className="font-semibold text-sm text-[#030712]">{book.Name}</p>
                <div className="flex gap-3 text-xs text-[#4B5563] mt-1">
                  <span>{book.Author}</span>
                  <span className="text-yellow-500">&#9733; {book['User Rating']}</span>
                  <span>${book.Price}</span>
                  <span className={`px-1.5 py-0.5 rounded-full text-[10px] font-semibold ${
                    book.Genre === 'Fiction' ? 'bg-orange-100 text-[#EA580C]' : 'bg-blue-100 text-[#2563EB]'
                  }`}>{book.Genre}</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {showResults && results.length === 0 && query.length >= 2 && !searching && (
        <Card className="absolute top-12 left-0 right-0 z-50 shadow-lg border border-[#E5E7EB]">
          <CardContent className="p-4 text-center text-sm text-[#4B5563]">
            No results found for "{query}"
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SearchBar;
