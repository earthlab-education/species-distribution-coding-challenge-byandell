def gbif_credentials(reset=False):
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
      
def gbif_species_key(species = 'grus canadensis'):
    # Query species
    species_info = species.name_lookup(species, rank='SPECIES')

    # Get the first result
    first_result = species_info['results'][0]

    # Get the species key (nubKey)
    species_key = first_result['nubKey']

    # Check the result
    return first_result['species'], species_key

# my_species, species_key = gbif_species_key('grus canadensis')

def download_gbif(data_dir, gbif_dir, species_key, year = 2023):
    # Only download once
    gbif_pattern = os.path.join(gbif_dir, '*.csv')
    if not glob(gbif_pattern):
        # Only submit one request
        if not 'GBIF_DOWNLOAD_KEY' in os.environ:
            # Submit query to GBIF
            gbif_query = occ.download([
                f"speciesKey = {species_key}",
                "hasCoordinate = TRUE",
                f"year = {year}",
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
    
    return gbif_path

# gbif_path = download_gbif(gbif_dir, species_key)

def load_gbif(gbif_path):
    # Load the GBIF data
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
    monthly_gdf = (
        gpd.GeoDataFrame(
            gbif_df, 
            geometry=gpd.points_from_xy(
                gbif_df.decimalLongitude, 
                gbif_df.decimalLatitude), 
            crs="EPSG:4326")
        # Select the desired columns
        [['month', 'geometry']]
    )
    return monthly_gdf

# monthly_gdf = gbif_monthly(gbif_df)

def ecoregions(data_dir):
    """
    
    Ecoregions represent boundaries formed by biotic and abiotic conditions:
    geology, landforms, soils, vegetation, land use, wildlife, climate, and hydrology.
    """

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

def gbif_ecoregion(ecoregions_gdf, monthly_gdf):
    gbif_ecoregion_gdf = (
        ecoregions_gdf
        # Match the coordinate reference system of the GBIF data and the ecoregions
        # transform geometries to a new coordinate reference system
        .to_crs(gdf_monthly.crs)
        # Find ecoregion for each observation
        # spatial join
        .sjoin(
            monthly_gdf,
            how='inner', 
            predicate='contains')
        # Select the required columns
        [['month', 'name']]
    )
    return gbif_ecoregion_gdf

# gbif_ecoregion_gdf = gbif_ecoregion(ecoregions_gdf, monthly_gdf)


def get_monthly_regional_observations(df, region_type, occurrence_name):
    """
    Count the observations in each ecoregion each month.
    """

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

# occurrence_df = get_monthly_regional_observations(gbif_ecoregion_gdf, 'ecoregion', 'name')
# occurrence_df.reset_index().plot.scatter(x='month', y='norm_occurrences', c='ecoregion', logy=True)

def simplify_ecoregions_gdf(ecoregions_gdf):
    """
    Create a simplified GeoDataFrame for plot.

    Streamlining plotting with hvplot by simplifying the geometry, projecting it to a Mercator projection that is compatible with
    geoviews, and cropping off areas in the Arctic.
    """

    # Speed up processing
    ecoregions_gdf.geometry = ecoregions_gdf.simplify(
        .1, preserve_topology=False)

    # Change the CRS to Mercator for mapping
    ecoregions_gdf = ecoregions_gdf.to_crs(ccrs.Mercator())
    
    return ecoregions_gdf

# ecoregions_gdf = simplify_ecoregions_gdf(ecoregions_gdf)

def join_occurrence(ecoregions_gdf, occurrence_df):
    """
    Join Ecoregions and Occurrence.

    Args:
        ecoregions_gdf (_type_): _description_
        occurrence_df (_type_): _description_
    Returns:
        occurrence_gdf (gdf)
    """

    # Join the occurrences with the plotting GeoDataFrame
    occurrence_gdf = ecoregions_gdf.join(occurrence_df[['norm_occurrences']])
    return occurrence_gdf

# occurrence_gdf = join_occurrence(ecoregions_gdf, occurrence_df)

def hvplot_occurrence(occurrence_gdf):
    """
    Mapping monthly distribution.

    Args:
        occurrence_gdf (gdf): _description_
    """

    # Get the plot bounds so they don't change with the slider
    xmin, ymin, xmax, ymax = occurrence_gdf.total_bounds

    # Define the slider widget
    slider = pn.widgets.DiscreteSlider(
        name='month', 
        options={calendar.month_name[i]: i for i in range(1, 13)}
    )
    
    migration_hvplot = occurrence_gdf.hvplot(
        c='norm_occurrences',
        groupby='month',
        # Use background tiles
        title='Antigone canadensis Sandhill Crane Migration',
        #geo=True, 
        # crs=ccrs.Mercator(), 
        tiles='CartoLight',
        xlim=(xmin, xmax), ylim=(ymin, ymax),
        frame_height=600,
        frame_width=1400,
        colorbar=False,
        widgets={'month': slider},
        widget_location='bottom',
        width=500,
        height=500
    )
    return migration_hvplot

# migration_hvplot = hvplot_occurrence(occurrence_gdf)
    
def plot_occurrence(occurrence_gdf):
    # Plot occurrence by ecoregion and month
    migration_plot = (
        occurrence_gdf
        .hvplot(
            c='norm_occurrences',
            groupby='month',
            # Use background tiles
            title='Antigone canadensis Sandhill Crane Migration',
            #geo=True, 
            #crs=ccrs.Mercator(), 
            tiles='CartoLight',
            xlim=(xmin, xmax), ylim=(ymin, ymax),
            frame_height=600,
            frame_width=1400,
            colorbar=False,
            widgets={'month': slider},
            widget_location='bottom'
        )
    )
    return migration_plot

# migration_plot = plot_occurrence(occurrence_gdf)
