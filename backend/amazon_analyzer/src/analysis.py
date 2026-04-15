"""Data analysis functions for Amazon Bestsellers dataset."""

import pandas as pd
import numpy as np
from collections import Counter


class DataAnalyzer:
    """Perform various analyses on the dataset."""
    
    def __init__(self, df):
        """Initialize the analyzer with a DataFrame.
        
        Args:
            df: pandas DataFrame to analyze
        """
        self.df = df.copy()
    
    def get_summary_statistics(self):
        """Get comprehensive summary statistics.
        
        Returns:
            dict: Summary statistics for all numeric columns
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        summary = {}
        
        for col in numeric_cols:
            summary[col] = {
                'count': int(self.df[col].count()),
                'mean': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'q25': float(self.df[col].quantile(0.25)),
                'q75': float(self.df[col].quantile(0.75))
            }
        
        return summary
    
    def get_top_authors(self, n=10):
        """Get top N authors by book count.
        
        Args:
            n: Number of top authors to return
        
        Returns:
            dict: Top authors with their book counts
        """
        author_counts = self.df['Author'].value_counts().head(n)
        result = {
            'authors': author_counts.index.tolist(),
            'counts': author_counts.values.tolist()
        }
        return result
    
    def get_genre_distribution(self):
        """Get distribution of books by genre.
        
        Returns:
            dict: Genre distribution
        """
        genre_counts = self.df['Genre'].value_counts()
        result = {
            'genres': genre_counts.index.tolist(),
            'counts': genre_counts.values.tolist(),
            'percentages': (genre_counts / len(self.df) * 100).round(2).tolist()
        }
        return result
    
    def get_year_wise_trends(self):
        """Analyze year-wise trends.
        
        Returns:
            dict: Year-wise statistics
        """
        yearly_data = self.df.groupby('Year').agg({
            'Name': 'count',
            'User Rating': 'mean',
            'Price': 'mean',
            'Reviews': 'mean'
        }).reset_index()
        
        yearly_data.columns = ['Year', 'Book_Count', 'Avg_Rating', 'Avg_Price', 'Avg_Reviews']
        
        result = {
            'years': yearly_data['Year'].tolist(),
            'book_counts': yearly_data['Book_Count'].tolist(),
            'avg_ratings': yearly_data['Avg_Rating'].round(2).tolist(),
            'avg_prices': yearly_data['Avg_Price'].round(2).tolist(),
            'avg_reviews': yearly_data['Avg_Reviews'].round(0).astype(int).tolist()
        }
        return result
    
    def get_price_rating_analysis(self):
        """Analyze relationship between price and rating.
        
        Returns:
            dict: Price-rating data points
        """
        result = {
            'prices': self.df['Price'].tolist(),
            'ratings': self.df['User Rating'].tolist(),
            'names': self.df['Name'].tolist(),
            'correlation': float(self.df['Price'].corr(self.df['User Rating']))
        }
        return result
    
    def get_correlation_matrix(self):
        """Calculate correlation matrix for numeric columns.
        
        Returns:
            dict: Correlation matrix data
        """
        numeric_cols = ['User Rating', 'Reviews', 'Price', 'Year']
        available_cols = [col for col in numeric_cols if col in self.df.columns]
        
        corr_matrix = self.df[available_cols].corr()
        
        result = {
            'columns': available_cols,
            'matrix': corr_matrix.values.tolist()
        }
        return result
    
    def get_top_rated_books(self, n=10):
        """Get top N highest rated books.
        
        Args:
            n: Number of books to return
        
        Returns:
            dict: Top rated books
        """
        top_books = self.df.nlargest(n, 'User Rating')[['Name', 'Author', 'User Rating', 'Reviews', 'Genre']]
        return top_books.to_dict('records')
    
    def get_most_reviewed_books(self, n=10):
        """Get top N most reviewed books.
        
        Args:
            n: Number of books to return
        
        Returns:
            dict: Most reviewed books
        """
        most_reviewed = self.df.nlargest(n, 'Reviews')[['Name', 'Author', 'User Rating', 'Reviews', 'Genre']]
        return most_reviewed.to_dict('records')
    
    def get_genre_statistics(self):
        """Get detailed statistics by genre.
        
        Returns:
            dict: Genre-wise statistics
        """
        genre_stats = self.df.groupby('Genre').agg({
            'Name': 'count',
            'User Rating': 'mean',
            'Price': 'mean',
            'Reviews': 'mean'
        }).reset_index()
        
        genre_stats.columns = ['Genre', 'Count', 'Avg_Rating', 'Avg_Price', 'Avg_Reviews']
        return genre_stats.to_dict('records')
    
    def generate_insights(self):
        """Generate meaningful insights from the data.
        
        Returns:
            list: List of insight strings
        """
        insights = []
        
        # Total books
        total_books = len(self.df)
        insights.append(f"Dataset contains {total_books} bestselling books.")
        
        # Genre distribution
        genre_dist = self.df['Genre'].value_counts()
        most_common_genre = genre_dist.index[0]
        genre_pct = (genre_dist.iloc[0] / total_books * 100)
        insights.append(f"{most_common_genre} is the dominant genre, representing {genre_pct:.1f}% of bestsellers.")
        
        # Rating insights
        avg_rating = self.df['User Rating'].mean()
        insights.append(f"Average user rating across all books is {avg_rating:.2f} out of 5.")
        
        high_rated = (self.df['User Rating'] >= 4.7).sum()
        high_rated_pct = (high_rated / total_books * 100)
        insights.append(f"{high_rated_pct:.1f}% of bestsellers have ratings of 4.7 or higher.")
        
        # Price insights
        avg_price = self.df['Price'].mean()
        median_price = self.df['Price'].median()
        insights.append(f"Average book price is ${avg_price:.2f}, with a median of ${median_price:.2f}.")
        
        # Most prolific author
        top_author = self.df['Author'].value_counts().index[0]
        author_count = self.df['Author'].value_counts().iloc[0]
        insights.append(f"{top_author} is the most prolific author with {author_count} bestselling books.")
        
        # Year range
        year_range = f"{int(self.df['Year'].min())}-{int(self.df['Year'].max())}"
        insights.append(f"Dataset spans years {year_range}.")
        
        # Correlation insight
        price_rating_corr = self.df['Price'].corr(self.df['User Rating'])
        if abs(price_rating_corr) < 0.3:
            insights.append(f"Price and rating show weak correlation ({price_rating_corr:.3f}), suggesting price doesn't strongly determine rating.")
        
        # Review volume
        high_review_threshold = self.df['Reviews'].quantile(0.75)
        high_review_books = (self.df['Reviews'] >= high_review_threshold).sum()
        insights.append(f"{high_review_books} books have exceptionally high review counts (top 25%).")
        
        return insights
    
    def get_filtered_data(self, year=None, genre=None):
        """Get filtered dataset based on year and/or genre.
        
        Args:
            year: Year to filter by (optional)
            genre: Genre to filter by (optional)
        
        Returns:
            pandas.DataFrame: Filtered dataset
        """
        filtered_df = self.df.copy()
        
        if year is not None:
            filtered_df = filtered_df[filtered_df['Year'] == year]
        
        if genre is not None:
            filtered_df = filtered_df[filtered_df['Genre'] == genre]
        
        return filtered_df
