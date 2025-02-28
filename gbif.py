"""
GBIF Functions.

gbif_credentials: Set up GBIF Credentials
gbif_species_key: Get GBIF Species Key
download_gbif: Download GBIF Entries as CSV file (only once)
load_gbif: Load the GBIF data
gbif_monthly: Extract monthly data as gdf
ecoregions: Get ecoregion boundary as gdf
join_ecoregions_monthly: Join ecoregions with monthly gbif data for species
count_monthly_ecoregions: Count the observations in each ecoregion each month
count_yearly_ecoregions: Count the observations in each ecoregion each year
simplify_ecoregions_gdf: Create a simplified GeoDataFrame for plot
hvplot_occurrence: Holoviews map of monthly distribution
"""
def gbif_credentials(reset=False):
    """
    Set up GBIF Credentials.

    Args:
        reset (bool, optional): Reset credials if missing or True. Defaults to False.
    Effects:
        Set Environment Variables.
    """
    import os
    from getpass import getpass

    reset_credentials = reset
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

# gbif_credentials()
      
def gbif_species_key(species_name = 'grus canadensis'):
    """
    Get GBIF Species Key.

    Args:
        species (str, optional): Name of species. Defaults to 'grus canadensis'.
    Returns:
        species_name (str): Name of species from first entry
        species_key (int): GBIF species key
    """
    import pygbif.species as species

    # Query species
    species_info = species.name_lookup(species_name, rank='SPECIES')

    # Get the first result
    first_result = species_info['results'][0]

    # Get the species key (nubKey)
    species_key = first_result['nubKey']

    # Check the result
    return first_result['species'], species_key

# species_name, species_key = gbif_species_key('grus canadensis')

def download_gbif(gbif_dir, species_key, year = 2023, unzip = False, reset = False):
    """
    Download GBIF Entries as CSV file (only once).

    Args:
        gbif_dir (str): _description_
        species_key (_type_): Species key
        year (int, optional): Year. Defaults to 2023.
        unzip (bool, optiona): Unzip CSV if True.
        reset (bool, optional): Reset download key if True.
    Returns:
        gbif_path (str): GBIF data path
    Effects:
        Download data to gbif_dir
    """
    import os
    from glob import glob
    import pygbif.occurrences as occ
    import time
    import zipfile
    
    if unzip:
        gbif_pattern = os.path.join(gbif_dir, '*.csv')
    else:
        gbif_pattern = os.path.join(gbif_dir, '*.zip')

    # Only download once
    if not glob(gbif_pattern):
        if reset:
            del os.environ['GBIF_DOWNLOAD_KEY']
        # Only submit one request
        if not 'GBIF_DOWNLOAD_KEY' in os.environ:
            # Submit query to GBIF
            queries = [
                f"speciesKey = {species_key}",
                "hasCoordinate = TRUE"
            ]
            if not year == None:
                queries.append(f"year = {year}")

            gbif_query = occ.download(queries)
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
            path=gbif_dir)

        if unzip:
            # Unzip GBIF data
            with zipfile.ZipFile(download_info['path']) as download_zip:
                download_zip.extractall(path=gbif_dir)

    # Find the extracted .csv file path (take the first result)
    gbif_path = glob(gbif_pattern)[0]
    
    return gbif_path

# gbif_path = download_gbif(gbif_dir, species_key)

def load_gbif(gbif_path):
    """
    Load the GBIF data.

    Args:
        gbif_path (str): GBIF data path
    Returns:
        gbif_df (df): GBIF DataFrame for selected species
    """
    import pandas as pd
    
    gbif_df = pd.read_csv(
        gbif_path, 
        delimiter='\t',
        index_col='gbifID',
        on_bad_lines='skip',
        usecols=['gbifID', 'month', 'year', 'countryCode', 'stateProvince', 'decimalLatitude', 'decimalLongitude']
    )
    return gbif_df

# gbif_df = load_gbif(gbif_path)
# gbif_df.head()

def gbif_monthly(gbif_df):
    """
    Extract monthly data as gdf

    Args:
        gbif_df (df): GBIF DataFrame for selected species
    Returns:
        monthly_gdf (gdf): GeoDataFrame of monthly data for species 
    """
    import geopandas as gpd

    monthly_gdf = (
        gpd.GeoDataFrame(
            gbif_df, 
            geometry=gpd.points_from_xy(
                gbif_df.decimalLongitude, 
                gbif_df.decimalLatitude), 
            crs="EPSG:4326")
        # Select the desired columns
        [['year', 'month', 'geometry']]
    )
    return monthly_gdf

# monthly_gdf = gbif_monthly(gbif_df)

def ecoregions(data_dir):
    """
    Get ecoregion boundary as gdf.
    
    Ecoregions represent boundaries formed by biotic and abiotic conditions:
    geology, landforms, soils, vegetation, land use, wildlife, climate, and hydrology.
    
    Args:
        data_dir (str): Data directory name
    Returns:
        ecoregions_gdf (gdf): GeoDataFrame of ecoregions
    """
    import os
    import geopandas as gpd

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
    
    return ecoregions_gdf

# ecoregions_gdf = ecoregions(data_dir)
# ecoregions_gdf.plot(edgecolor='black', color='skyblue')
# !find ~/earth-analytics/data/species -name '*.shp'

def join_ecoregions_monthly(ecoregions_gdf, monthly_gdf):
    """
    Join ecoregions with monthly gbif data for species.

    Args:
        ecoregions_gdf (gdf): GeoDataFrame of ecoregions
        monthly_gdf (gdf): GeoDataFrame of monthly data for species
    Returns:
        gbif_ecoregion_gdf (gdf): GeoDataFrame for species
    """
    gbif_ecoregion_gdf = (
        ecoregions_gdf
        # Match the coordinate reference system of the GBIF data and the ecoregions
        # transform geometries to a new coordinate reference system
        .to_crs(monthly_gdf.crs)
        # Find ecoregion for each observation
        # spatial join
        .sjoin(
            monthly_gdf,
            how='inner', 
            predicate='contains')
        # Select the required columns
        [['year', 'month', 'name']]
    )
    return gbif_ecoregion_gdf

# gbif_ecoregion_gdf = gbif_ecoregion(ecoregions_gdf, monthly_gdf)

def count_monthly_ecoregions(gbif_ecoregions_gdf, region_type = 'ecoregion', occurrence_name = 'name'):
    """
    Count the observations in each ecoregion each month.
    
    Args:
        gbif_ecoregions_gdf (gdf): GeoDataFrame with raw occurrences
        region_type (str, optional): Region type. Default 'ecoregion'.
        occurrence_name (str, optional): Occurrence name. Default 'name'.
    Returns:
        occurrence_gdf (gdf): GeoDataFrame with occurrences by region.
    """

    occurrence_gdf = (
        gbif_ecoregions_gdf
        # For each region, for each month...
        .groupby([region_type, 'month'])
        # count the number of occurrences
        .agg(occurrences=(occurrence_name, 'count'))
    )

    # Get rid of rare observations (possible misidentification)
    occurrence_gdf = occurrence_gdf[occurrence_gdf["occurrences"] > 1]

    # Take the mean by region
    mean_occurrences_by_region = (
        occurrence_gdf
        .groupby([region_type])
        .mean()
    )

    # Take the mean by month
    mean_occurrences_by_month = (
        occurrence_gdf
        .groupby(['month'])
        .mean()
    )

    # Normalize by space and time for sampling effort
    # This accounts for the number of active observers in each location and time of year
    occurrence_gdf['norm_occurrences'] = (
        occurrence_gdf
        / mean_occurrences_by_region
        / mean_occurrences_by_month
    )

    return occurrence_gdf

# occurrence_gdf = count_monthly_ecoregions(gbif_ecoregions_gdf, 'ecoregion', 'name')
# occurrence_gdf.reset_index().plot.scatter(x='month', y='norm_occurrences', c='ecoregion', logy=True)

def count_yearly_ecoregions(gbif_ecoregions_gdf, region_type, occurrence_name):
    """
    Count the observations in each ecoregion each year.
    
    Args:
        gbif_ecoregions_gdf (gdf): GeoDataFrame with raw occurrences
        region_type (str, optional): Region type. Default 'ecoregion'.
        occurrence_name (str, optional): Occurrence name. Default 'name'.
    Returns:
        occurrence_gdf (gdf): GeoDataFrame with occurrences by region.
    """

    occurrence_gdf = (
        gbif_ecoregions_gdf
        # For each region, for each month...
        .groupby([region_type, 'year'])
        # count the number of occurrences
        .agg(occurrences=(occurrence_name, 'count'))
    )

    # Get rid of rare observations (possible misidentification)
    occurrence_gdf = occurrence_gdf[occurrence_gdf["occurrences"] > 1]

    # Take the mean by region
    mean_occurrences_by_region = (
        occurrence_gdf
        .groupby([region_type])
        .mean()
    )

    # Take the mean by year
    mean_occurrences_by_year = (
        occurrence_gdf
        .groupby(['year'])
        .mean()
    )

    # Normalize by space and time for sampling effort
    # This accounts for the number of active observers in each location and time of year
    occurrence_gdf['norm_occurrences'] = (
        occurrence_gdf
        / mean_occurrences_by_region
        / mean_occurrences_by_year
    )

    return occurrence_gdf

# occurrence_gdf = count_yearly_ecoregions(gbif_ecoregion_gdf, 'ecoregion', 'name')

def simplify_ecoregions_gdf(ecoregions_gdf):
    """
    Create a simplified GeoDataFrame for plot.

    Streamlining plotting with hvplot by simplifying the geometry, projecting it to a Mercator projection that is compatible with
    geoviews, and cropping off areas in the Arctic.
    
    Args:
        ecoregions_gdf (gdf): GeoDataFrame of ecoregions
    Returns:
        ecoregions_gdf (gdf): GeoDataFrame of ecoregions
    """
    import cartopy
    import cartopy.crs as ccrs

    # Speed up processing
    ecoregions_gdf.geometry = ecoregions_gdf.simplify(
        .1, preserve_topology=False)

    # Change the CRS to Mercator for mapping
    ecoregions_gdf = ecoregions_gdf.to_crs(ccrs.Mercator())
    
    return ecoregions_gdf

# ecoregions_gdf = simplify_ecoregions_gdf(ecoregions_gdf)

def join_occurrence(ecoregions_gdf, occurrence_gdf):
    """
    Join Ecoregions and Occurrence.

    Args:
        ecoregions_gdf (gdf): GeoDataFrame of ecoregions
        occurrence_gdf (gdf): GeoDataFrame of species occurrences
    Returns:
        occurrence_gdf (gdf): GeoDataFrame of species occurrences
    """

    # Join the occurrences with the plotting GeoDataFrame
    occurrence_gdf = ecoregions_gdf.join(occurrence_gdf[['norm_occurrences']])
    return occurrence_gdf

# occurrence_gdf = join_occurrence(ecoregions_gdf, occurrence_gdf)

def hvplot_occurrence(occurrence_gdf, unit='month'):
    """
    Holoviews map of monthly distribution.

    Args:
        occurrence_gdf (gdf): _description_
    Returns:
        occurrence_hvplot (hvplot): Holoviews plot of occurrence over time with slider
    """
    import panel as pn
    import calendar
    import hvplot.pandas
    # CCRS commented out due to bad behavior.
    # import cartopy
    # import cartopy.crs as ccrs

    # Get the plot bounds so they don't change with the slider
    xmin, ymin, xmax, ymax = occurrence_gdf.total_bounds
    
    pn.extension()

    # Define the slider widget
    if unit == 'month':
        options={calendar.month_name[i]: i for i in range(1, 13)}
    else: # 'year'
        options=sorted(
            occurrence_gdf
            .index
            .get_level_values('year')
            .round()
            .unique()
            .astype(int))
#        {i: i for i in range(1970, 2024)}
    slider = pn.widgets.DiscreteSlider(name=unit, options=options)
    
    occurrence_hvplot = occurrence_gdf.hvplot(
        c='norm_occurrences',
        groupby=unit,
        # Use background tiles
        title='Antigone canadensis Sandhill Crane Migration',
        # geo=True, 
        # crs=ccrs.Mercator(), 
        tiles='CartoLight',
        xlim=(xmin, xmax), ylim=(ymin, ymax),
        frame_height=600,
        frame_width=1400,
        colorbar=False,
        widgets={unit: slider},
        widget_location='bottom',
        width=500,
        height=500
    )
    return occurrence_hvplot

# occurrence_hvplot = hvplot_occurrence(occurrence_gdf)
