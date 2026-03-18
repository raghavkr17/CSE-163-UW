"""
hw5.py

Raghav Krishna Ranganathan
CSE 163 THA5 Mapping

Loads Washington census tract geometry and USDA food access data,
merges them, and produces geospatial plots for analysis.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def _no_array_interface(self: object) -> None:
    """
    Disable NumPy array interface for Shapely geometries.

    This prevents NumPy from attempting to treat geometry
    objects as arrays, which can cause compatibility issues
    between Shapely 1.7 and newer NumPy versions.
    """
    raise AttributeError


try:
    from shapely.geometry.base import BaseGeometry
    from shapely.geometry import (
        Point, MultiPoint, LineString, MultiLineString,
        Polygon, MultiPolygon, GeometryCollection
    )

    for _cls in [
        BaseGeometry, Point, MultiPoint, LineString, MultiLineString,
        Polygon, MultiPolygon, GeometryCollection
    ]:
        try:
            _cls.__array_interface__ = property(_no_array_interface)
        except Exception:
            pass
except Exception:
    pass


def load_in_data(census_file: str, food_file: str) -> gpd.GeoDataFrame:
    """
    Load the census shapefile and food access CSV and merge them.

    Parameters:
        census_file: path to the census shapefile
        food_file: path to the food access CSV

    Returns:
        A GeoDataFrame produced by merging on CTIDFP00 and CensusTract.
    """
    census = gpd.read_file(census_file)
    food = pd.read_csv(food_file)

    merged = census.merge(
        food,
        left_on='CTIDFP00',
        right_on='CensusTract',
        how='left'
    )
    return merged


def percentage_food_data(data: gpd.GeoDataFrame) -> float:
    """
    Return the percent of Washington census tracts that have food access data.
    """
    total = len(data)
    with_food = data['County'].notna().sum()
    return (with_food / total) * 100


def plot_map(data: gpd.GeoDataFrame) -> None:
    """
    Plot the shapes of all Washington census tracts to map.png.
    """
    fig, ax = plt.subplots()
    data.plot(ax=ax)
    plt.title("Washington State")
    plt.savefig("map.png")


def plot_population_map(data: gpd.GeoDataFrame) -> None:
    """
    Plot census tract shapes colored by population to population_map.png.

    Tracts without food data will have missing POP2010 and will not be colored.
    """
    fig, ax = plt.subplots()

    data.plot(color='#EEEEEE', ax=ax)

    has_pop = data['POP2010'].notna()
    data.loc[has_pop].plot(
        column='POP2010',
        legend=True,
        ax=ax
    )

    plt.title("Washington Census Tract Populations")
    plt.savefig("population_map.png")


def plot_population_county_map(data: gpd.GeoDataFrame) -> None:
    """
    Aggregate by county and plot county populations to
    county_population_map.png.
    """
    base = data[['County', 'POP2010', 'geometry']].copy()
    base = base[base['County'].notna() & base['POP2010'].notna()]

    county = base.dissolve(by='County', aggfunc='sum')

    fig, ax = plt.subplots()
    data.plot(color='#EEEEEE', ax=ax)
    county.plot(column='POP2010', legend=True, ax=ax)

    plt.title("Washington County Populations")
    plt.savefig("county_population_map.png")


def plot_food_access_by_county(data: gpd.GeoDataFrame) -> None:
    """
    Produce a 2x2 subplot figure of food access ratios by county.
    Saves to county_food_access.png.
    """
    cols = [
        'County', 'geometry', 'POP2010',
        'lapophalf', 'lapop10',
        'lalowihalf', 'lalowi10'
    ]
    county = data[cols].copy()
    county = county[county['County'].notna()].copy()

    numeric_cols = ['POP2010', 'lapophalf',
                    'lapop10', 'lalowihalf', 'lalowi10']
    county[numeric_cols] = county[numeric_cols].fillna(0)

    county = county.dissolve(by='County', aggfunc='sum')

    pop = county['POP2010'].replace(0, pd.NA)
    county['lapophalf_ratio'] = county['lapophalf'] / pop
    county['lapop10_ratio'] = county['lapop10'] / pop
    county['lalowihalf_ratio'] = county['lalowihalf'] / pop
    county['lalowi10_ratio'] = county['lalowi10'] / pop

    county[['lapophalf_ratio', 'lapop10_ratio',
            'lalowihalf_ratio', 'lalowi10_ratio']] = (
        county[['lapophalf_ratio', 'lapop10_ratio',
                'lalowihalf_ratio', 'lalowi10_ratio']].fillna(0)
    )

    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2, figsize=(20, 10))

    county.plot(color='#EEEEEE', ax=ax1)
    county.plot(column='lapophalf_ratio', ax=ax1, legend=True, vmin=0, vmax=1)
    ax1.set_title('Low Access: Half')

    county.plot(color='#EEEEEE', ax=ax2)
    county.plot(column='lapop10_ratio', ax=ax2, legend=True, vmin=0, vmax=1)
    ax2.set_title('Low Access: 10')

    county.plot(color='#EEEEEE', ax=ax3)
    county.plot(column='lalowihalf_ratio', ax=ax3, legend=True, vmin=0, vmax=1)
    ax3.set_title('Low Income + Low Access: Half')

    county.plot(color='#EEEEEE', ax=ax4)
    county.plot(column='lalowi10_ratio', ax=ax4, legend=True, vmin=0, vmax=1)
    ax4.set_title('Low Income + Low Access: 10')

    plt.savefig("county_food_access.png")


def plot_low_access_tracts(data: gpd.GeoDataFrame) -> None:
    """
    Plot low access census tracts to low_access.png.

    Urban uses lapophalf, rural uses lapop10.
    A tract is low access if >= 500 people OR >= 33% of the tract population.
    """
    needed = data.copy()
    for col in ['POP2010', 'lapophalf', 'lapop10', 'Urban']:
        if col not in needed.columns:
            raise KeyError(f"Missing required column: {col}")

    needed[['POP2010', 'lapophalf', 'lapop10']] = (
        needed[['POP2010', 'lapophalf', 'lapop10']].fillna(0)
    )

    pop = needed['POP2010'].replace(0, pd.NA)

    urban_mask = needed['Urban'] == 1
    rural_mask = needed['Urban'] == 0

    urban_low = (
        (needed['lapophalf'] >= 500) |
        ((needed['lapophalf'] / pop) >= 0.33)
    )

    rural_low = (
        (needed['lapop10'] >= 500) |
        ((needed['lapop10'] / pop) >= 0.33)
    )

    low_access = (urban_mask & urban_low) | (rural_mask & rural_low)
    low_access = low_access.fillna(False)

    fig, ax = plt.subplots()

    needed.plot(color='#EEEEEE', ax=ax)

    has_food = needed['County'].notna()
    needed.loc[has_food].plot(color='#AAAAAA', ax=ax)

    needed.loc[low_access].plot(ax=ax)

    plt.title("Low Access Census Tracts")
    plt.savefig("low_access.png")


def main():
    census_file = "food_access/tl_2010_53_tract00/tl_2010_53_tract00.shp"
    food_file = "food_access/food_access.csv"

    data = load_in_data(census_file, food_file)

    print(percentage_food_data(data))

    plot_map(data)
    plot_population_map(data)
    plot_population_county_map(data)
    plot_food_access_by_county(data)
    plot_low_access_tracts(data)


if __name__ == "__main__":
    main()
