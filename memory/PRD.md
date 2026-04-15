# Amazon Bestseller Analyzer - PRD

## Original Problem Statement
Create a complete industry-level project called "Amazon Best Seller Analyzer" using Python with CSV dataset, modular code, EDA, visualizations (Matplotlib & Seaborn), insights, interactive dashboard with filters, and professional documentation.

## Architecture
- **Backend**: FastAPI (Python 3.11) serving data from CSV via 9 REST endpoints
- **Frontend**: React 19 + Recharts + Tailwind CSS + Shadcn/UI dashboard
- **Data**: Local CSV (97 Amazon bestselling books)
- **Analysis**: pandas, NumPy, Matplotlib, Seaborn

## User Personas
- Data science job seekers showcasing portfolio
- Students learning full-stack data analysis
- Interviewers evaluating candidates

## Core Requirements (Static)
- CSV data loading and preprocessing
- EDA with summary stats, top authors, genre distribution, year trends, correlations
- Visualizations: bar, pie, line, scatter, heatmap
- Auto-generated insights
- Interactive dashboard with year/genre filters
- Standalone Python script
- Professional README

## What's Been Implemented (April 15, 2026)
- [x] Complete Python analysis modules (data_loader, preprocessing, analysis, visualizations)
- [x] 97-book realistic CSV dataset
- [x] FastAPI backend with 9 API endpoints
- [x] React dashboard with 9 components (cards, charts, table, insights)
- [x] Year and Genre filters
- [x] Standalone main.py script
- [x] README.md and PROJECT_SUMMARY.md
- [x] ZIP file for download (/app/amazon-bestseller-analyzer.zip)

## Prioritized Backlog
### P0 - Done
- All core requirements implemented

### P1 - Nice to Have
- Export analysis to PDF/Excel
- More granular filters (price range, rating range)
- Book search functionality

### P2 - Future
- ML predictions (book success predictor)
- Time series forecasting
- Recommendation engine
- User authentication for saved analyses

## Next Tasks
- User can download via Emergent platform
- Add export functionality if requested
- Expand dataset if needed
