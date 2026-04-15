# Amazon Bestseller Analyzer

## 📚 Project Overview

A comprehensive, industry-level data analysis project that analyzes Amazon bestselling books dataset using Python, pandas, and modern web technologies. This project demonstrates end-to-end data science skills from data loading and preprocessing to visualization and insight generation.

**Live Dashboard:** Full-stack web application with interactive charts and filters

## ✨ Features

### Data Analysis
- **Data Loading & Preprocessing**: Clean, modular code for handling CSV data
- **Data Quality Checks**: Missing value detection, duplicate removal, data type validation
- **Feature Engineering**: Price categories, rating categories, review volume segmentation
- **Statistical Analysis**: Comprehensive summary statistics, correlation analysis
- **Trend Analysis**: Year-wise trends, genre distribution, author popularity

### Visualizations
- Top 10 Authors (Bar Chart)
- Genre Distribution (Pie Chart)
- Year-wise Trends (Multi-line Chart)
- Price vs Rating Analysis (Scatter Plot)
- Correlation Matrix (Heatmap)
- Rating Distribution (Histogram)

### Interactive Dashboard
- Real-time filtering by year and genre
- Summary statistics cards
- Key insights panel
- Responsive data table
- Modern, clean UI with smooth animations

## 💻 Tech Stack

### Backend
- **Python 3.11**
- **FastAPI**: High-performance REST API
- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib & Seaborn**: Data visualization

### Frontend
- **React 19**: Modern UI library
- **Recharts**: Interactive chart library
- **Tailwind CSS**: Utility-first CSS framework
- **Shadcn/UI**: Beautiful, accessible components
- **Axios**: HTTP client

### Database
- **MongoDB**: For potential data persistence

## 📁 Project Structure

```
/app/
├── backend/
│   ├── amazon_analyzer/
│   │   ├── data/
│   │   │   └── amazon_bestsellers.csv        # Dataset (100+ books)
│   │   ├── src/
│   │   │   ├── data_loader.py                 # Data loading utilities
│   │   │   ├── preprocessing.py               # Data cleaning & preprocessing
│   │   │   ├── analysis.py                    # Statistical analysis
│   │   │   └── visualizations.py              # Matplotlib/Seaborn plots
│   │   ├── output/                        # Generated visualizations
│   │   └── main.py                        # Standalone analysis script
│   ├── server.py                          # FastAPI application
│   ├── requirements.txt                   # Python dependencies
│   └── .env                               # Environment variables
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js                   # Main dashboard
│   │   │   ├── SummaryCards.js                # Statistics cards
│   │   │   ├── TopAuthorsChart.js             # Bar chart
│   │   │   ├── GenreChart.js                  # Pie chart
│   │   │   ├── YearTrendsChart.js             # Line chart
│   │   │   ├── PriceRatingChart.js            # Scatter plot
│   │   │   ├── CorrelationHeatmap.js          # Correlation matrix
│   │   │   ├── BooksTable.js                  # Data table
│   │   │   └── InsightsPanel.js               # Key insights
│   │   ├── App.js                             # Main app component
│   │   └── index.css                          # Global styles
│   ├── package.json                       # Node dependencies
│   └── .env                               # Frontend config
│
└── README.md                              # This file
```

## 🚀 Quick Start

### Option 1: Run Standalone Python Analysis

```bash
# Navigate to the analyzer directory
cd /app/backend/amazon_analyzer

# Run the main analysis script
python main.py
```

This will:
- Load and preprocess the data
- Perform comprehensive analysis
- Generate visualizations (saved in `output/` folder)
- Print key insights to console

### Option 2: Run Full-Stack Application

The application is already running! The backend and frontend are managed by supervisor.

**Backend API**: Available at `/api` endpoint
**Frontend Dashboard**: Main application interface

### Manual Setup (if needed)

#### Backend
```bash
cd /app/backend
pip install -r requirements.txt
sudo supervisorctl restart backend
```

#### Frontend
```bash
cd /app/frontend
yarn install
sudo supervisorctl restart frontend
```

## 📊 Dataset Information

**Source**: Amazon Bestselling Books (2009-2019)

**Columns**:
- `Name`: Book title
- `Author`: Author name
- `User Rating`: Rating out of 5
- `Reviews`: Number of reviews
- `Price`: Book price in USD
- `Year`: Publication year
- `Genre`: Fiction or Non Fiction

**Size**: 100+ books
**Format**: CSV

## 🔍 Key Insights Generated

The analysis automatically generates insights such as:
- Total dataset composition
- Genre distribution patterns
- Rating statistics and trends
- Price analysis
- Most prolific authors
- Correlation patterns between variables
- Review volume analysis

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API information |
| `/api/summary` | GET | Summary statistics |
| `/api/top-authors` | GET | Top N authors |
| `/api/genre-distribution` | GET | Genre breakdown |
| `/api/year-trends` | GET | Year-wise trends |
| `/api/price-rating` | GET | Price vs rating data |
| `/api/correlation` | GET | Correlation matrix |
| `/api/books` | GET | Filtered books data |
| `/api/insights` | GET | Generated insights |
| `/api/filter-options` | GET | Available filters |

## 🎯 Interview Talking Points

### Data Science Skills
1. **Data Preprocessing**: Demonstrated handling of missing values, duplicates, and data type validation
2. **Exploratory Data Analysis**: Comprehensive statistical analysis with multiple dimensions
3. **Feature Engineering**: Created categorical features from continuous variables
4. **Correlation Analysis**: Identified relationships between variables
5. **Insight Generation**: Automated meaningful insight extraction

### Software Engineering Skills
1. **Modular Code**: Clean separation of concerns (loading, preprocessing, analysis, visualization)
2. **API Design**: RESTful API with clear endpoints and response models
3. **Full-Stack Development**: React frontend with Python backend
4. **Code Quality**: Well-commented, properly structured, follows best practices
5. **Documentation**: Comprehensive README with clear instructions

### Technical Highlights
- Used pandas for efficient data manipulation
- Implemented reusable classes for each concern
- Created both static (Matplotlib) and interactive (Recharts) visualizations
- Built responsive, modern UI with Tailwind CSS
- Implemented real-time filtering and data updates

## 📝 Code Quality Features

✓ **Modular Design**: Each component has a single responsibility
✓ **Type Hints**: Clear function signatures and return types
✓ **Error Handling**: Graceful error management
✓ **Documentation**: Docstrings for all classes and functions
✓ **Clean Code**: Meaningful variable names, proper formatting
✓ **DRY Principle**: No code repetition
✓ **Scalability**: Easy to add new analyses or visualizations

## 🔧 Technologies & Libraries

```python
# Core Data Science
pandas==3.0.2
numpy==2.4.4
matplotlib==3.10.8
seaborn==0.13.2

# Web Framework
fastapi==0.110.1
uvicorn==0.25.0

# Utilities
python-dotenv==1.0.1
pydantic==2.6.4
```

```json
// Frontend
"react": "^19.0.0",
"recharts": "^3.6.0",
"tailwindcss": "^3.4.17",
"axios": "^1.8.4",
"lucide-react": "^0.507.0"
```

## 🎯 Future Enhancements

Potential improvements for the project:
1. **Machine Learning**: Predict book success based on features
2. **Time Series Analysis**: Forecast future trends
3. **Sentiment Analysis**: Analyze review text (if available)
4. **Recommendation System**: Suggest books based on preferences
5. **Data Export**: Download analysis results as PDF/Excel
6. **Advanced Filters**: More granular filtering options
7. **Comparison Mode**: Compare books side-by-side
8. **User Authentication**: Save favorite analyses

## 📝 License

This project is open source and available for educational purposes.

## 👤 Author

Created as an industry-level portfolio project demonstrating:
- Python data analysis skills
- Full-stack development capabilities
- Clean code practices
- Professional documentation

---

**Built with ❤️ using Python, React, and modern data science tools**
