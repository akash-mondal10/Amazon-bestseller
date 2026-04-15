# Amazon Bestseller Analyzer - PRD

## Original Problem Statement
Create a complete industry-level project called "Amazon Best Seller Analyzer" using Python with CSV dataset, modular code, EDA, visualizations, insights, interactive dashboard, and professional documentation.

## Architecture
- **Backend**: FastAPI (Python 3.11) serving data from CSV via REST endpoints + ML models
- **Frontend**: React 19 + Recharts + Tailwind CSS + Shadcn/UI dashboard
- **Data**: Local CSV (550 Amazon bestselling books)
- **Analysis**: pandas, NumPy, Matplotlib, Seaborn
- **ML**: scikit-learn (Random Forest + Gradient Boosting)
- **Export**: reportlab (PDF), openpyxl (Excel)

## What's Been Implemented

### Phase 1 (April 15, 2026)
- [x] Complete Python analysis modules (data_loader, preprocessing, analysis, visualizations)
- [x] 97-book realistic CSV dataset
- [x] FastAPI backend with 9 API endpoints
- [x] React dashboard with 9 components
- [x] Year and Genre filters
- [x] Standalone main.py script
- [x] README.md and PROJECT_SUMMARY.md

### Phase 2 (April 15, 2026)
- [x] Dataset expanded from 97 to 550 books
- [x] Book search (search bar + /api/search endpoint)
- [x] PDF export (full report with summary, insights, tables, ML info)
- [x] Excel export (5 sheets: Summary, Books Data, Top Authors with chart, Year Trends with chart, Correlation)
- [x] ML Classification: Random Forest Classifier (73.6% accuracy) - predicts bestseller status
- [x] ML Regression: Gradient Boosting Regressor - predicts user rating
- [x] ML Prediction UI panel with form inputs and results display

## Test Results
- Backend: 100% (15/15 tests passed)
- Frontend: 93% (14/15 - 1 minor UI testability issue)

## Prioritized Backlog
### P1 - Nice to Have
- Advanced filtering (price range slider, rating range)
- Book comparison side-by-side
- Data upload (user's own CSV)

### P2 - Future
- Time series forecasting
- NLP sentiment analysis on reviews
- Recommendation engine
- User authentication
