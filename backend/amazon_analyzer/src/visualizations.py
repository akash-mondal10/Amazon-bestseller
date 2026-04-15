"""Visualization functions for Amazon Bestsellers dataset."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


class DataVisualizer:
    """Create various visualizations for the dataset."""
    
    def __init__(self, df, output_dir=None):
        """Initialize the visualizer.
        
        Args:
            df: pandas DataFrame to visualize
            output_dir: Directory to save plots (optional)
        """
        self.df = df.copy()
        
        if output_dir is None:
            base_dir = Path(__file__).parent.parent
            self.output_dir = base_dir / 'output'
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(exist_ok=True)
    
    def plot_top_authors(self, n=10, save=True):
        """Create bar chart of top authors.
        
        Args:
            n: Number of top authors to display
            save: Whether to save the plot
        """
        plt.figure(figsize=(12, 6))
        author_counts = self.df['Author'].value_counts().head(n)
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, n))
        bars = plt.bar(range(len(author_counts)), author_counts.values, color=colors)
        
        plt.xlabel('Author', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Bestsellers', fontsize=12, fontweight='bold')
        plt.title(f'Top {n} Authors by Number of Bestselling Books', fontsize=14, fontweight='bold', pad=20)
        plt.xticks(range(len(author_counts)), author_counts.index, rotation=45, ha='right')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'top_authors.png', dpi=300, bbox_inches='tight')
            print(f"✓ Saved: top_authors.png")
        
        plt.close()
    
    def plot_genre_distribution(self, save=True):
        """Create bar chart of genre distribution.
        
        Args:
            save: Whether to save the plot
        """
        plt.figure(figsize=(10, 6))
        genre_counts = self.df['Genre'].value_counts()
        
        colors = ['#FF6B6B', '#4ECDC4']
        bars = plt.bar(genre_counts.index, genre_counts.values, color=colors)
        
        plt.xlabel('Genre', fontsize=12, fontweight='bold')
        plt.ylabel('Number of Books', fontsize=12, fontweight='bold')
        plt.title('Distribution of Books by Genre', fontsize=14, fontweight='bold', pad=20)
        
        # Add value labels and percentages
        total = len(self.df)
        for i, bar in enumerate(bars):
            height = bar.get_height()
            pct = (height / total) * 100
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}\n({pct:.1f}%)',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'genre_distribution.png', dpi=300, bbox_inches='tight')
            print(f"✓ Saved: genre_distribution.png")
        
        plt.close()
    
    def plot_year_trends(self, save=True):
        """Create line plot of year-wise trends.
        
        Args:
            save: Whether to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Year-wise Trends Analysis', fontsize=16, fontweight='bold', y=1.00)
        
        yearly_data = self.df.groupby('Year').agg({
            'Name': 'count',
            'User Rating': 'mean',
            'Price': 'mean',
            'Reviews': 'mean'
        }).reset_index()
        
        # Book count trend
        axes[0, 0].plot(yearly_data['Year'], yearly_data['Name'], marker='o', linewidth=2, markersize=8, color='#3498db')
        axes[0, 0].set_xlabel('Year', fontweight='bold')
        axes[0, 0].set_ylabel('Number of Books', fontweight='bold')
        axes[0, 0].set_title('Books Published per Year', fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Average rating trend
        axes[0, 1].plot(yearly_data['Year'], yearly_data['User Rating'], marker='s', linewidth=2, markersize=8, color='#e74c3c')
        axes[0, 1].set_xlabel('Year', fontweight='bold')
        axes[0, 1].set_ylabel('Average Rating', fontweight='bold')
        axes[0, 1].set_title('Average User Rating over Years', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Average price trend
        axes[1, 0].plot(yearly_data['Year'], yearly_data['Price'], marker='^', linewidth=2, markersize=8, color='#2ecc71')
        axes[1, 0].set_xlabel('Year', fontweight='bold')
        axes[1, 0].set_ylabel('Average Price ($)', fontweight='bold')
        axes[1, 0].set_title('Average Book Price over Years', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Average reviews trend
        axes[1, 1].plot(yearly_data['Year'], yearly_data['Reviews'], marker='D', linewidth=2, markersize=8, color='#9b59b6')
        axes[1, 1].set_xlabel('Year', fontweight='bold')
        axes[1, 1].set_ylabel('Average Reviews', fontweight='bold')
        axes[1, 1].set_title('Average Number of Reviews over Years', fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'year_trends.png', dpi=300, bbox_inches='tight')
            print(f"✓ Saved: year_trends.png")
        
        plt.close()
    
    def plot_price_vs_rating(self, save=True):
        """Create scatter plot of price vs rating.
        
        Args:
            save: Whether to save the plot
        """
        plt.figure(figsize=(12, 7))
        
        # Color points by genre
        genres = self.df['Genre'].unique()
        colors = {'Fiction': '#FF6B6B', 'Non Fiction': '#4ECDC4'}
        
        for genre in genres:
            genre_data = self.df[self.df['Genre'] == genre]
            plt.scatter(genre_data['Price'], genre_data['User Rating'],
                       alpha=0.6, s=100, label=genre, color=colors.get(genre, '#95a5a6'))
        
        plt.xlabel('Price ($)', fontsize=12, fontweight='bold')
        plt.ylabel('User Rating', fontsize=12, fontweight='bold')
        plt.title('Price vs User Rating (by Genre)', fontsize=14, fontweight='bold', pad=20)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        # Add correlation coefficient
        corr = self.df['Price'].corr(self.df['User Rating'])
        plt.text(0.05, 0.95, f'Correlation: {corr:.3f}',
                transform=plt.gca().transAxes,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=11, fontweight='bold',
                verticalalignment='top')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'price_vs_rating.png', dpi=300, bbox_inches='tight')
            print(f"✓ Saved: price_vs_rating.png")
        
        plt.close()
    
    def plot_correlation_heatmap(self, save=True):
        """Create correlation heatmap for numeric variables.
        
        Args:
            save: Whether to save the plot
        """
        plt.figure(figsize=(10, 8))
        
        # Select numeric columns
        numeric_cols = ['User Rating', 'Reviews', 'Price', 'Year']
        corr_matrix = self.df[numeric_cols].corr()
        
        # Create heatmap
        sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdYlBu_r',
                   center=0, square=True, linewidths=1,
                   cbar_kws={"shrink": 0.8},
                   annot_kws={'fontsize': 12, 'fontweight': 'bold'})
        
        plt.title('Correlation Matrix of Numeric Variables', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
            print(f"✓ Saved: correlation_heatmap.png")
        
        plt.close()
    
    def plot_rating_distribution(self, save=True):
        """Create histogram of rating distribution.
        
        Args:
            save: Whether to save the plot
        """
        plt.figure(figsize=(10, 6))
        
        plt.hist(self.df['User Rating'], bins=20, color='#3498db', edgecolor='black', alpha=0.7)
        plt.axvline(self.df['User Rating'].mean(), color='red', linestyle='--',
                   linewidth=2, label=f"Mean: {self.df['User Rating'].mean():.2f}")
        plt.axvline(self.df['User Rating'].median(), color='green', linestyle='--',
                   linewidth=2, label=f"Median: {self.df['User Rating'].median():.2f}")
        
        plt.xlabel('User Rating', fontsize=12, fontweight='bold')
        plt.ylabel('Frequency', fontsize=12, fontweight='bold')
        plt.title('Distribution of User Ratings', fontsize=14, fontweight='bold', pad=20)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(self.output_dir / 'rating_distribution.png', dpi=300, bbox_inches='tight')
            print(f"✓ Saved: rating_distribution.png")
        
        plt.close()
    
    def create_all_plots(self):
        """Generate all visualization plots."""
        print("\n📊 Generating visualizations...")
        print("-" * 50)
        
        self.plot_top_authors()
        self.plot_genre_distribution()
        self.plot_year_trends()
        self.plot_price_vs_rating()
        self.plot_correlation_heatmap()
        self.plot_rating_distribution()
        
        print("-" * 50)
        print(f"✓ All plots saved to: {self.output_dir}")
