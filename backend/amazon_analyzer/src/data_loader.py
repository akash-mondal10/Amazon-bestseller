"""Data loading and basic operations for Amazon Bestsellers dataset."""

import pandas as pd
import os
from pathlib import Path


class DataLoader:
    """Handle data loading and basic operations."""
    
    def __init__(self, data_path=None):
        """Initialize the DataLoader.
        
        Args:
            data_path: Path to the CSV file. If None, uses default path.
        """
        if data_path is None:
            # Default path relative to this file
            base_dir = Path(__file__).parent.parent
            self.data_path = base_dir / 'data' / 'amazon_bestsellers.csv'
        else:
            self.data_path = Path(data_path)
        
        self.df = None
    
    def load_data(self):
        """Load the CSV data into a pandas DataFrame.
        
        Returns:
            pandas.DataFrame: The loaded dataset
        """
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✓ Data loaded successfully: {len(self.df)} records")
            return self.df
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found at: {self.data_path}")
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def get_basic_info(self):
        """Get basic information about the dataset.
        
        Returns:
            dict: Basic dataset information
        """
        if self.df is None:
            self.load_data()
        
        info = {
            'total_records': len(self.df),
            'columns': list(self.df.columns),
            'shape': self.df.shape,
            'dtypes': self.df.dtypes.to_dict(),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        }
        return info
    
    def get_sample(self, n=5):
        """Get a sample of the dataset.
        
        Args:
            n: Number of rows to return
        
        Returns:
            pandas.DataFrame: Sample data
        """
        if self.df is None:
            self.load_data()
        return self.df.head(n)
    
    def get_column_names(self):
        """Get list of column names.
        
        Returns:
            list: Column names
        """
        if self.df is None:
            self.load_data()
        return list(self.df.columns)
