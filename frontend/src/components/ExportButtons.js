import React, { useState } from 'react';
import { FileSpreadsheet, FileText, Download, Loader2 } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ExportButtons = ({ selectedYear, selectedGenre, searchQuery }) => {
  const [exportingExcel, setExportingExcel] = useState(false);
  const [exportingPdf, setExportingPdf] = useState(false);

  const buildParams = () => {
    const params = new URLSearchParams();
    if (selectedYear && selectedYear !== 'all') params.append('year', selectedYear);
    if (selectedGenre && selectedGenre !== 'all') params.append('genre', selectedGenre);
    if (searchQuery) params.append('search', searchQuery);
    return params.toString();
  };

  const handleExportExcel = async () => {
    setExportingExcel(true);
    try {
      const params = buildParams();
      const url = `${API}/export/excel${params ? '?' + params : ''}`;
      const response = await fetch(url);
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = 'amazon_bestseller_analysis.xlsx';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      console.error('Excel export error:', error);
    }
    setExportingExcel(false);
  };

  const handleExportPdf = async () => {
    setExportingPdf(true);
    try {
      const params = buildParams();
      const url = `${API}/export/pdf${params ? '?' + params : ''}`;
      const response = await fetch(url);
      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = 'amazon_bestseller_report.pdf';
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      console.error('PDF export error:', error);
    }
    setExportingPdf(false);
  };

  return (
    <div className="flex gap-3" data-testid="export-buttons">
      <button
        data-testid="export-excel-btn"
        onClick={handleExportExcel}
        disabled={exportingExcel}
        className="inline-flex items-center gap-2 bg-[#10B981] text-white hover:bg-emerald-700 font-medium px-4 py-2 rounded-md transition-colors text-sm disabled:opacity-50"
      >
        {exportingExcel ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileSpreadsheet className="h-4 w-4" />}
        {exportingExcel ? 'Exporting...' : 'Export Excel'}
      </button>

      <button
        data-testid="export-pdf-btn"
        onClick={handleExportPdf}
        disabled={exportingPdf}
        className="inline-flex items-center gap-2 bg-[#EA580C] text-white hover:bg-orange-700 font-medium px-4 py-2 rounded-md transition-colors text-sm disabled:opacity-50"
      >
        {exportingPdf ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4" />}
        {exportingPdf ? 'Exporting...' : 'Export PDF'}
      </button>
    </div>
  );
};

export default ExportButtons;
