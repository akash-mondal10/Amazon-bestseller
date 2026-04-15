#!/usr/bin/env python3
"""Main script to run the complete Amazon Bestseller Analysis."""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loader import DataLoader
from preprocessing import DataPreprocessor
from analysis import DataAnalyzer
from visualizations import DataVisualizer


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_insights(insights):
    """Print insights in a formatted way."""
    print("\n📌 KEY INSIGHTS:")
    print("-" * 70)
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    print("-" * 70)


def main():
    """Run the complete analysis pipeline."""
    
    print_header("AMAZON BESTSELLER ANALYZER")
    print("\nA comprehensive data analysis project")
    print("Analyzing Amazon bestselling books dataset\n")
    
    # Step 1: Load Data
    print_header("STEP 1: DATA LOADING")
    loader = DataLoader()
    df = loader.load_data()
    
    # Display basic info
    info = loader.get_basic_info()
    print(f"\nDataset Shape: {info['shape']}")
    print(f"Total Records: {info['total_records']}")
    print(f"Columns: {', '.join(info['columns'])}")
    
    # Display sample
    print("\nFirst 5 rows:")
    print(loader.get_sample(5).to_string())
    
    # Step 2: Data Preprocessing
    print_header("STEP 2: DATA PREPROCESSING")
    preprocessor = DataPreprocessor(df)
    
    # Check data quality
    missing = preprocessor.check_missing_values()
    if missing:
        print(f"⚠️  Missing values found: {missing}")
    else:
        print("✓ No missing values detected")
    
    duplicates = preprocessor.check_duplicates()
    if duplicates['count'] > 0:
        print(f"⚠️  Found {duplicates['count']} duplicate rows ({duplicates['percentage']:.2f}%)")
        preprocessor.remove_duplicates()
    else:
        print("✓ No duplicate rows detected")
    
    # Validate and engineer features
    preprocessor.validate_data_types()
    clean_df = preprocessor.feature_engineering()
    
    # Step 3: Exploratory Data Analysis
    print_header("STEP 3: EXPLORATORY DATA ANALYSIS")
    analyzer = DataAnalyzer(clean_df)
    
    # Summary statistics
    print("\n📊 Summary Statistics:")
    summary_stats = analyzer.get_summary_statistics()
    for col, stats in summary_stats.items():
        print(f"\n{col}:")
        print(f"  Mean: {stats['mean']:.2f}")
        print(f"  Median: {stats['median']:.2f}")
        print(f"  Std Dev: {stats['std']:.2f}")
        print(f"  Range: [{stats['min']:.2f}, {stats['max']:.2f}]")
    
    # Top authors
    print("\n📚 Top 10 Authors:")
    top_authors = analyzer.get_top_authors(10)
    for author, count in zip(top_authors['authors'], top_authors['counts']):
        print(f"  {author}: {count} books")
    
    # Genre distribution
    print("\n📖 Genre Distribution:")
    genre_dist = analyzer.get_genre_distribution()
    for genre, count, pct in zip(genre_dist['genres'], genre_dist['counts'], genre_dist['percentages']):
        print(f"  {genre}: {count} books ({pct}%)")
    
    # Correlation analysis
    print("\n🔗 Correlation Analysis:")
    price_rating = analyzer.get_price_rating_analysis()
    print(f"  Price vs Rating Correlation: {price_rating['correlation']:.3f}")
    
    # Step 4: Generate Insights
    print_header("STEP 4: GENERATING INSIGHTS")
    insights = analyzer.generate_insights()
    print_insights(insights)
    
    # Step 5: Create Visualizations
    print_header("STEP 5: CREATING VISUALIZATIONS")
    visualizer = DataVisualizer(clean_df)
    visualizer.create_all_plots()
    
    # Final Summary
    print_header("ANALYSIS COMPLETE")
    print("\n✅ All analyses completed successfully!")
    print(f"\n📁 Output files saved in: {visualizer.output_dir}")
    print("\nGenerated files:")
    print("  - top_authors.png")
    print("  - genre_distribution.png")
    print("  - year_trends.png")
    print("  - price_vs_rating.png")
    print("  - correlation_heatmap.png")
    print("  - rating_distribution.png")
    
    print("\n" + "=" * 70)
    print("  Thank you for using Amazon Bestseller Analyzer!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
