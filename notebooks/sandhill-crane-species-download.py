# %% [markdown]
# # Access locations and times of Veery encounters
# 
# For this challenge, you will use a database called the [Global
# Biodiversity Information Facility (GBIF)](https://www.gbif.org/). GBIF
# is compiled from species observation data all over the world, and
# includes everything from museum specimens to photos taken by citizen
# scientists in their backyards.
# 
# <link rel="stylesheet" type="text/css" href="./assets/styles.css"><div class="callout callout-style-default callout-titled callout-task"><div class="callout-header"><div class="callout-icon-container"><i class="callout-icon"></i></div><div class="callout-title-container flex-fill">Try It: Explore GBIF</div></div><div class="callout-body-container callout-body"><p>Before your get started, go to the <a
# href="https://www.gbif.org/occurrence/search">GBIF occurrences search
# page</a> and explore the data.</p></div></div>
# 
# > **Contribute to open data**
# >
# > You can get your own observations added to GBIF using
# > [iNaturalist](https://www.inaturalist.org/)!
# 
# ### Set up your code to prepare for download
# 
# We will be getting data from a source called [GBIF (Global Biodiversity
# Information Facility)](https://www.gbif.org/). We need a package called
# `pygbif` to access the data, which may not be included in your
# environment. Install it by running the cell below:

# %%
%%bash
pip install pygbif

# %%
%conda list pygbif

# %% [markdown]
# <link rel="stylesheet" type="text/css" href="./assets/styles.css"><div class="callout callout-style-default callout-titled callout-task"><div class="callout-header"><div class="callout-icon-container"><i class="callout-icon"></i></div><div class="callout-title-container flex-fill">Try It: Import packages</div></div><div class="callout-body-container callout-body"><p>In the imports cell, we’ve included some packages that you will need.
# Add imports for packages that will help you:</p>
# <ol type="1">
# <li>Work with reproducible file paths</li>
# <li>Work with tabular data</li>
# </ol></div></div>

# %%
import time
import zipfile
from getpass import getpass
from glob import glob

import os
import pathlib

from getpass import getpass
from glob import glob

import geopandas as gpd
import pandas as pd

import pygbif.occurrences as occ
import pygbif.species as species

# get month names
import calendar

# libraries for Dynamic mapping
import geoviews as gv
import hvplot.pandas
import cartopy.crs as ccrs
import panel as pn
pn.extension()



# %%
# Create data directory in the home folder
data_dir = os.path.join(
    # Home directory
    pathlib.Path.home(),
    # Earth analytics data directory
    'earth-analytics',
    'data',
    # Project directory
    'species',
)
os.makedirs(data_dir, exist_ok=True)

# Define the directory name for GBIF data
gbif_dir = os.path.join(data_dir, 'gbif_grus')
gbif_dir

# %% [markdown]
# :::
# 
# ### Register and log in to GBIF
# 
# You will need a [GBIF account](https://www.gbif.org/) to complete this
# challenge. You can use your GitHub account to authenticate with GBIF.
# Then, run the following code to save your credentials on your computer.
# 
# > **Warning**
# >
# > Your email address **must** match the email you used to sign up for
# > GBIF!
# 
# > **Tip**
# >
# > If you accidentally enter your credentials wrong, you can set
# > `reset_credentials=True` instead of `reset_credentials=False`.

# %%
reset_credentials = False
# GBIF needs a username, password, and email
credentials = dict(
    GBIF_USER=(input, 'username'),
    GBIF_PWD=(getpass, 'password'),
    GBIF_EMAIL=(input, 'email'),
)
for env_variable, (prompt_func, prompt_text) in credentials.items():
    # Delete credential from environment if requested
    if reset_credentials and (env_variable in os.environ):
        os.environ.pop(env_variable)
    # Ask for credential and save to environment
    if not env_variable in os.environ:
        os.environ[env_variable] = prompt_func(prompt_text)

# %% [markdown]
# ### Get the species key
# 
# > ** Your task**
# >
# > 1.  Replace the `species_name` with the name of the species you want
# >     to look up
# > 2.  Run the code to get the species key

# %%
# Query species
species_info = species.name_lookup('grus canadensis', rank='SPECIES')

# Get the first result
first_result = species_info['results'][0]

# Get the species key (nubKey)
species_key = first_result['nubKey']

# Check the result
first_result['species'], species_key

# %%
species_key

# %% [markdown]
# ### Download data from GBIF
# 
# ::: {.callout-task title=“Submit a request to GBIF”
# 
# 1.  Replace `csv_file_pattern` with a string that will match **any**
#     `.csv` file when used in the `glob` function. HINT: the character
#     `*` represents any number of any values except the file separator
#     (e.g. `/`)
# 
# 2.  Add parameters to the GBIF download function, `occ.download()` to
#     limit your query to:
# 
#     -   observations
#     -   from 2023
#     -   with spatial coordinates.
# 
# 3.  Then, run the download. **This can take a few minutes**. :::
# 
#     -   Can check progress at <https://www.gbif.org/user/download>.

# %%
# Only download once
gbif_pattern = os.path.join(gbif_dir, '*.csv')
if not glob(gbif_pattern):
    # Only submit one request
    if not 'GBIF_DOWNLOAD_KEY' in os.environ:
        # Submit query to GBIF
        gbif_query = occ.download([
            "speciesKey = 2474953",
            "hasCoordinate = TRUE",
            "year = 2023",
        ])
        os.environ['GBIF_DOWNLOAD_KEY'] = gbif_query[0]

    # Wait for the download to build
    download_key = os.environ['GBIF_DOWNLOAD_KEY']
    wait = occ.download_meta(download_key)['status']
    while not wait=='SUCCEEDED':
        wait = occ.download_meta(download_key)['status']
        time.sleep(5)

    # Download GBIF data
    download_info = occ.download_get(
        os.environ['GBIF_DOWNLOAD_KEY'], 
        path=data_dir)

    # Unzip GBIF data
    with zipfile.ZipFile(download_info['path']) as download_zip:
        download_zip.extractall(path=gbif_dir)

# Find the extracted .csv file path (take the first result)
gbif_path = glob(gbif_pattern)[0]

# %% [markdown]
# download key is 0020917-241007104925546
# GBIF.org (17 October 2024) GBIF Occurrence Download https://doi.org/10.15468/dl.4d3k48

# %%
gbif_path = glob(gbif_pattern)[0]
gbif_path

# %% [markdown]
# ### Load the GBIF data into Python
# 
# <link rel="stylesheet" type="text/css" href="./assets/styles.css"><div class="callout callout-style-default callout-titled callout-task"><div class="callout-header"><div class="callout-icon-container"><i class="callout-icon"></i></div><div class="callout-title-container flex-fill">Try It: Load GBIF data</div></div><div class="callout-body-container callout-body"><ol type="1">
# <li>Look at the beginning of the file you downloaded using the code
# below. What do you think the <strong>delimiter</strong> is?</li>
# <li>Run the following code cell. What happens?</li>
# <li>Uncomment and modify the parameters of <code>pd.read_csv()</code>
# below until your data loads successfully and you have only the columns
# you want.</li>
# </ol></div></div>
# 
# You can use the following code to look at the beginning of your file:

# %% [markdown]
# I copied from <https://github.com/lauren-alexandra/lauren-alexandra.github.io/blob/main/willow-flycatcher-distribution/willow-flycatcher-distribution.ipynb>
# and Lauren Gleason

# %%
!head -n 2 $gbif_path 

# %%
# Load the GBIF data
gbif_df = pd.read_csv(
    gbif_path, 
    delimiter='\t',
    index_col='gbifID',
    on_bad_lines='skip',
    usecols=['gbifID', 'month', 'year', 'countryCode', 'stateProvince', 'decimalLatitude', 'decimalLongitude']
)
gbif_df.head()

# %% [markdown]
# ### Canada Breeding Locations

# %%
ac_CA = gbif_df.loc[gbif_df['countryCode'] == 'CA']
ac_CA.value_counts()

# %% [markdown]
# ### US Breeding Locations

# %%
ac_US = gbif_df.loc[gbif_df['countryCode'] == 'US']
ac_US.value_counts()

# %% [markdown]
# ## Convert GBIF data to a GeoDataFrame by Month

# %%
gdf_monthly = (
    gpd.GeoDataFrame(
        gbif_df, 
        geometry=gpd.points_from_xy(
            gbif_df.decimalLongitude, 
            gbif_df.decimalLatitude), 
        crs="EPSG:4326")
    # Select the desired columns
    [['month', 'geometry']]
)

gdf_monthly

# %% [markdown]
# ### Download and save ecoregion boundaries
# 
# Ecoregions represent boundaries formed by biotic and abiotic conditions: geology, landforms, soils, vegetation, land use, wildlife, climate, and hydrology.

# %%
# Set up the ecoregion boundary URL
ecoregions_url = "https://storage.googleapis.com/teow2016/Ecoregions2017.zip"

# Set up a path to save the data on your machine
ecoregions_dir = os.path.join(data_dir, 'wwf_ecoregions')

# Make the ecoregions directory
os.makedirs(ecoregions_dir, exist_ok=True)

# Join ecoregions shapefile path
ecoregions_path = os.path.join(ecoregions_dir, 'wwf_ecoregions.shp')

# Only download once
if not os.path.exists(ecoregions_path):
    ecoregions_gdf = gpd.read_file(ecoregions_url)
    ecoregions_gdf.to_file(ecoregions_path)

# %%
%%bash
find ~/earth-analytics/data/species -name '*.shp'

# %%
# Open up the ecoregions boundaries
ecoregions_gdf = (
    gpd.read_file(ecoregions_path)
    .rename(columns={
        'ECO_NAME': 'name',
        'SHAPE_AREA': 'area'})
    [['name', 'area', 'geometry']]
)

# Name the index so it will match the other data later on
ecoregions_gdf.index.name = 'ecoregion'

# Plot the ecoregions to check download
ecoregions_gdf.plot(edgecolor='black', color='skyblue')

# %%
ecoregions_gdf

# %%
%store ecoregions_gdf gdf_monthly

# %% [markdown]
# Identify the ecoregion for each observation

# %%
gbif_ecoregion_gdf = (
    ecoregions_gdf
    # Match the coordinate reference system of the GBIF data and the ecoregions
    # transform geometries to a new coordinate reference system
    .to_crs(gdf_monthly.crs)
    # Find ecoregion for each observation
    # spatial join
    .sjoin(
        gdf_monthly,
        how='inner', 
        predicate='contains')
    # Select the required columns
    [['month', 'name']]
)
gbif_ecoregion_gdf

# %% [markdown]
# Count the observations in each ecoregion each month

# %%
def get_monthly_regional_observations(df, region_type, occurrence_name):

    occurrence_df = (
        df
        # For each region, for each month...
        .groupby([region_type, 'month'])
        # count the number of occurrences
        .agg(occurrences=(occurrence_name, 'count'))
    )

    # Get rid of rare observations (possible misidentification)
    occurrence_df = occurrence_df[occurrence_df["occurrences"] > 1]

    # Take the mean by region
    mean_occurrences_by_region = (
        occurrence_df
        .groupby([region_type])
        .mean()
    )

    # Take the mean by month
    mean_occurrences_by_month = (
        occurrence_df
        .groupby(['month'])
        .mean()
    )

    # Normalize by space and time for sampling effort
    # This accounts for the number of active observers in each location and time of year
    occurrence_df['norm_occurrences'] = (
        occurrence_df
        / mean_occurrences_by_region
        / mean_occurrences_by_month
    )

    return occurrence_df

# %%
occurrence_df = get_monthly_regional_observations(gbif_ecoregion_gdf, 'ecoregion', 'name')

occurrence_df

# %% [markdown]
# Create a simplified GeoDataFrame for plot

# %%
"""
Streamlining plotting with hvplot by simplifying the geometry, projecting it to a Mercator projection that is compatible with
geoviews, and cropping off areas in the Arctic.
"""

# Speed up processing
ecoregions_gdf.geometry = ecoregions_gdf.simplify(
    .1, preserve_topology=False)

# Change the CRS to Mercator for mapping
ecoregions_gdf = ecoregions_gdf.to_crs(ccrs.Mercator())

ecoregions_gdf

# %%
%store gbif_path
%who

# %% [markdown]
# Mapping monthly distribution

# %%
# Join the occurrences with the plotting GeoDataFrame
occurrence_gdf = ecoregions_gdf.join(occurrence_df)

# Get the plot bounds so they don't change with the slider
xmin, ymin, xmax, ymax = occurrence_gdf.total_bounds

# Define the slider widget
slider = pn.widgets.DiscreteSlider(
    name='month', 
    options={calendar.month_name[i]: i for i in range(1, 13)}
)

occurrence_gdf

# %%
%store occurrence_gdf

# %%
occurrence_gdf.hvplot(
    x='Longitude',
    y='Latitude',
    c='norm_occurrences',
    geo=True, 
    crs=ccrs.Mercator()
    )

# %%
occurrence_gdf.hvplot(
    c='norm_occurrences',
    groupby='month',
    # Use background tiles
    title='Antigone canadensis Sandhill Crane Migration',
    geo=True, crs=ccrs.Mercator(), tiles='CartoLight',
    xlim=(xmin, xmax), ylim=(ymin, ymax),
    frame_height=600,
    colorbar=False,
    widgets={'month': slider},
    widget_location='bottom',
    width=500,
    height=500
)

# %%
occurrence_gdf

# %%
# Plot occurrence by ecoregion and month
migration_plot = (
    occurrence_gdf
    .hvplot(
        c='norm_occurrences',
        groupby='month',
        # Use background tiles
        title='Antigone canadensis Sandhill Crane Migration',
        geo=True, crs=ccrs.Mercator(), tiles='CartoLight',
        xlim=(xmin, xmax), ylim=(ymin, ymax),
        frame_height=600,
        colorbar=False,
        widgets={'month': slider},
        widget_location='bottom',
        width=500,
        height=500
    )
)

# Save the plot
migration_plot.save('sandhill-crane-migration.html', embed=True)

# Show the plot
migration_plot

# %% [markdown]
# April Observations

# %%
occurrence_gdf_complete = occurrence_gdf.reset_index()

april_occ = occurrence_gdf_complete.loc[occurrence_gdf_complete['month'] == 4].sort_values(by=['norm_occurrences'], ascending=False)

april_occ_top_5 = april_occ[0:5]
april_occ_bottom_5 = april_occ[-5:]

# %%
# Top Five Ecoregions

april_occ_top_5

# %%
# Bottom Five Ecoregions

april_occ_bottom_5


