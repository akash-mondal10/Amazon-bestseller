"""Data preprocessing and cleaning functions."""

import pandas as pd
import numpy as np


class DataPreprocessor:
    """Handle data cleaning and preprocessing."""
    
    def __init__(self, df):
        """Initialize the preprocessor with a DataFrame.
        
        Args:
            df: pandas DataFrame to preprocess
        """
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_report = {}
    
    def check_missing_values(self):
        """Check for missing values in the dataset.
        
        Returns:
            dict: Missing value counts per column
        """
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        result = {
            col: {'count': int(missing[col]), 'percentage': float(missing_pct[col])}
            for col in self.df.columns if missing[col] > 0
        }
        
        self.cleaning_report['missing_values'] = result
        return result
    
    def check_duplicates(self):
        """Check for duplicate rows.
        
        Returns:
            dict: Duplicate information
        """
        duplicates = self.df.duplicated().sum()
        duplicate_rows = self.df[self.df.duplicated(keep=False)]
        
        result = {
            'count': int(duplicates),
            'percentage': float((duplicates / len(self.df)) * 100)
        }
        
        self.cleaning_report['duplicates'] = result
        return result
    
    def remove_duplicates(self):
        """Remove duplicate rows from the dataset.
        
        Returns:
            pandas.DataFrame: Cleaned dataframe
        """
        initial_count = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_count - len(self.df)
        
        print(f"✓ Removed {removed} duplicate rows")
        return self.df
    
    def handle_missing_values(self, strategy='drop'):
        """Handle missing values based on strategy.
        
        Args:
            strategy: 'drop' to remove rows with missing values,
                     'fill' to fill with appropriate values
        
        Returns:
            pandas.DataFrame: Cleaned dataframe
        """
        if strategy == 'drop':
            initial_count = len(self.df)
            self.df = self.df.dropna()
            removed = initial_count - len(self.df)
            print(f"✓ Removed {removed} rows with missing values")
        
        elif strategy == 'fill':
            # Fill numeric columns with median
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if self.df[col].isnull().any():
                    median_val = self.df[col].median()
                    self.df[col].fillna(median_val, inplace=True)
            
            # Fill categorical columns with mode
            categorical_cols = self.df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if self.df[col].isnull().any():
                    mode_val = self.df[col].mode()[0]
                    self.df[col].fillna(mode_val, inplace=True)
            
            print("✓ Filled missing values")
        
        return self.df
    
    def validate_data_types(self):
        """Validate and convert data types if needed.
        
        Returns:
            dict: Data type information
        """
        # Ensure numeric columns are numeric
        numeric_columns = ['User Rating', 'Reviews', 'Price', 'Year']
        
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        dtypes = self.df.dtypes.to_dict()
        return {str(k): str(v) for k, v in dtypes.items()}
    
    def feature_engineering(self):
        """Create new features from existing data.
        
        Returns:
            pandas.DataFrame: DataFrame with new features
        """
        # Price category
        self.df['Price_Category'] = pd.cut(
            self.df['Price'],
            bins=[0, 10, 15, 20, float('inf')],
            labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
        )
        
        # Rating category
        self.df['Rating_Category'] = pd.cut(
            self.df['User Rating'],
            bins=[0, 4.0, 4.5, 4.7, 5.0],
            labels=['Good', 'Very Good', 'Excellent', 'Outstanding']
        )
        
        # Review volume category
        self.df['Review_Volume'] = pd.cut(
            self.df['Reviews'],
            bins=[0, 10000, 30000, 60000, float('inf')],
            labels=['Low', 'Medium', 'High', 'Very High']
        )
        
        # Decade
        self.df['Decade'] = (self.df['Year'] // 10) * 10
        
        print("✓ Feature engineering completed")
        return self.df
    
    def get_clean_data(self):
        """Get the cleaned dataset.
        
        Returns:
            pandas.DataFrame: Cleaned dataset
        """
        return self.df
    
    def get_cleaning_summary(self):
        """Get summary of cleaning operations.
        
        Returns:
            dict: Cleaning summary
        """
        summary = {
            'original_rows': len(self.original_df),
            'cleaned_rows': len(self.df),
            'rows_removed': len(self.original_df) - len(self.df),
            'cleaning_report': self.cleaning_report
        }
        return summary
