"""
hw3.py
Author: Raghav Krishna
Date: 01/27/2026

Analyze and visualize educational attainment data (1920 till 2018).
Includes:
- Compare bachelor's degree by sex
- Average attainment by degree
- Line plot over time
- Bar plot for high school completion
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def compare_bachelors_year(data: pd.DataFrame, year: int) -> pd.Series:
    """Return percentage of males and females with at least a bachelor's in the given year."""
    result = data.loc[(year, ["M", "F"], "bachelor's"), "Total"]
    return result

def mean_min_degrees(
    data: pd.DataFrame,
    start_year: int = None,
    end_year: int = None,
    category: str = "Total"
) -> pd.Series:
    """Return average percentage of each Min degree for the given category and year range."""
    # Slice by year
    years = data.index.get_level_values("Year")
    if start_year is None:
        start_year = years.min()
    if end_year is None:
        end_year = years.max()
    
    filtered = data.loc[(slice(start_year, end_year), "A", slice(None)), category]
    mean_values = filtered.groupby(level="Min degree").mean()
    return mean_values

def line_plot_min_degree(data: pd.DataFrame, min_degree: str) -> None:
    """Plot a line plot of Total percentage over years for the given min_degree."""
    plot_data = data.loc[(slice(None), "A", min_degree), "Total"].reset_index()
    sns.relplot(data=plot_data, x="Year", y="Total", kind="line")
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    plt.title(f"Percentage earning {min_degree} over time")
    plt.savefig("line_plot_min_degree.png", bbox_inches="tight")
    plt.close()

def bar_plot_high_school(data: pd.DataFrame, year: int) -> None:
    """Plot a bar plot comparing Total percentages for F, M, A for high school in the given year."""
    plot_data = data.loc[(year, ["F", "M", "A"], "high school"), "Total"].reset_index()
    sns.catplot(data=plot_data, x="Sex", y="Total", kind="bar")
    plt.xlabel("Sex")
    plt.ylabel("Percentage")
    plt.title(f"High school completion in {year}")
    plt.savefig("bar_plot_high_school.png", bbox_inches="tight")
    plt.close()

def main():
    # Load CSV
    df = pd.read_csv("nces-ed-attainment.csv")
    
    # Replace missing values
    df.replace("---", pd.NA, inplace=True)
    
    # Set MultiIndex
    df.set_index(["Year", "Sex", "Min degree"], inplace=True)
    
    # Convert numeric columns to float
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Call functions
    print(compare_bachelors_year(df, 1980))
    print(mean_min_degrees(df, 2000, 2010, "Total"))
    line_plot_min_degree(df, "bachelor's")
    bar_plot_high_school(df, 2009)

if __name__ == "__main__":
    main()
