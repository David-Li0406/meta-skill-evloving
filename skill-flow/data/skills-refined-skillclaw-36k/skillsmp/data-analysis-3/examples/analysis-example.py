"""
Data Analysis Example

This example demonstrates common data analysis workflows using pandas,
including loading data, exploration, transformation, and visualization.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_sample_data() -> pd.DataFrame:
    """Create sample data for demonstration."""
    np.random.seed(42)
    n_samples = 100
    
    data = {
        'id': range(1, n_samples + 1),
        'category': np.random.choice(['A', 'B', 'C'], n_samples),
        'value': np.random.normal(100, 15, n_samples),
        'quantity': np.random.randint(1, 50, n_samples),
        'date': pd.date_range('2024-01-01', periods=n_samples, freq='D'),
    }
    
    # Add some missing values
    df = pd.DataFrame(data)
    df.loc[np.random.choice(df.index, 5), 'value'] = np.nan
    
    return df


def explore_data(df: pd.DataFrame) -> None:
    """Perform basic data exploration."""
    print("=" * 50)
    print("DATA EXPLORATION")
    print("=" * 50)
    
    # Basic info
    print(f"\nShape: {df.shape}")
    print(f"\nColumn types:\n{df.dtypes}")
    
    # Preview
    print(f"\nFirst 5 rows:\n{df.head()}")
    
    # Summary statistics
    print(f"\nSummary statistics:\n{df.describe()}")
    
    # Missing values
    print(f"\nMissing values:\n{df.isnull().sum()}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data by handling missing values."""
    print("\n" + "=" * 50)
    print("DATA CLEANING")
    print("=" * 50)
    
    # Make a copy
    df_clean = df.copy()
    
    # Fill missing values with median
    median_value = df_clean['value'].median()
    df_clean['value'] = df_clean['value'].fillna(median_value)
    
    print(f"Filled {df['value'].isnull().sum()} missing values with median: {median_value:.2f}")
    print(f"Missing values after cleaning: {df_clean.isnull().sum().sum()}")
    
    return df_clean


def analyze_data(df: pd.DataFrame) -> dict:
    """Perform statistical analysis."""
    print("\n" + "=" * 50)
    print("STATISTICAL ANALYSIS")
    print("=" * 50)
    
    # Descriptive statistics
    stats = {
        'mean_value': df['value'].mean(),
        'median_value': df['value'].median(),
        'std_value': df['value'].std(),
        'total_quantity': df['quantity'].sum(),
    }
    
    print(f"\nMean value: {stats['mean_value']:.2f}")
    print(f"Median value: {stats['median_value']:.2f}")
    print(f"Std deviation: {stats['std_value']:.2f}")
    print(f"Total quantity: {stats['total_quantity']}")
    
    # Group analysis
    print("\nGroup statistics:")
    group_stats = df.groupby('category').agg({
        'value': ['mean', 'std'],
        'quantity': 'sum'
    })
    print(group_stats)
    
    return stats


def visualize_data(df: pd.DataFrame) -> None:
    """Create visualizations."""
    print("\n" + "=" * 50)
    print("VISUALIZATION")
    print("=" * 50)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Histogram of values
    axes[0, 0].hist(df['value'], bins=20, edgecolor='black', alpha=0.7)
    axes[0, 0].set_title('Distribution of Values')
    axes[0, 0].set_xlabel('Value')
    axes[0, 0].set_ylabel('Frequency')
    
    # Bar chart by category
    category_counts = df['category'].value_counts()
    axes[0, 1].bar(category_counts.index, category_counts.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    axes[0, 1].set_title('Count by Category')
    axes[0, 1].set_xlabel('Category')
    axes[0, 1].set_ylabel('Count')
    
    # Box plot
    df.boxplot(column='value', by='category', ax=axes[1, 0])
    axes[1, 0].set_title('Value Distribution by Category')
    axes[1, 0].set_xlabel('Category')
    axes[1, 0].set_ylabel('Value')
    plt.suptitle('')  # Remove automatic title
    
    # Scatter plot
    axes[1, 1].scatter(df['quantity'], df['value'], alpha=0.6, c=df['category'].astype('category').cat.codes)
    axes[1, 1].set_title('Value vs Quantity')
    axes[1, 1].set_xlabel('Quantity')
    axes[1, 1].set_ylabel('Value')
    
    plt.tight_layout()
    plt.savefig('analysis_output.png', dpi=150)
    print("Saved visualization to 'analysis_output.png'")


def main():
    """Run the complete analysis workflow."""
    # Step 1: Create/Load data
    df = create_sample_data()
    
    # Step 2: Explore data
    explore_data(df)
    
    # Step 3: Clean data
    df_clean = clean_data(df)
    
    # Step 4: Analyze data
    stats = analyze_data(df_clean)
    
    # Step 5: Visualize data
    visualize_data(df_clean)
    
    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE")
    print("=" * 50)


if __name__ == '__main__':
    main()

