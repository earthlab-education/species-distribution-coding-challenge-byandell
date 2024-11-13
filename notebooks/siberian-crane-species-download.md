# Access locations and times of Siberian Crane encounters

For this challenge, you the
[Global Biodiversity Information Facility (GBIF)](https://www.gbif.org/).
GBIF is compiled from species observation data all over the world, and
includes everything from museum specimens to photos taken by citizen
scientists in their backyards.

### Set up your code to prepare for download

We need a package called
`pygbif` to access the data, which may not be included in your
environment. 

Import packages that will help you:

- Work with reproducible file paths
- Work with tabular data

```{python}
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
import cartopy
import cartopy.crs as ccrs
import panel as pn
pn.extension()
```

Create data directory in the home folder

```{python}
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
gbif_dir = os.path.join(data_dir, 'gbif_siberian')
gbif_dir
```

```
'/home/jovyan/earth-analytics/data/species/gbif_siberian'
```

### Register and log in to GBIF

You will need a [GBIF account](https://www.gbif.org/) to complete this
challenge. You can use your GitHub account to authenticate with GBIF.
Then, run the following code to save your credentials on your computer.

```{python}
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
```

### Get the species key

```{python}
# Query species
species_info = species.name_lookup('grus leucogeranus', rank='SPECIES')

# Get the first result
first_result = species_info['results'][0]

# Get the species key (nubKey)
species_key = first_result['nubKey']

# Check the result
first_result['species'], species_key
```

```
    ('Grus leucogeranus', 2474961)
```

### Download data from GBIF

This gets _all_ data for Siberian Crane, since it is rare and endangered.
Thus the `year` variable is dropped. Note that we can check progress at
<https://www.gbif.org/user/download>.

```{python}
# Only download once
gbif_pattern = os.path.join(gbif_dir, '*.csv')
if not glob(gbif_pattern):
    # Only submit one request
    if not 'GBIF_DOWNLOAD_KEY' in os.environ:
        # Submit query to GBIF
        gbif_query = occ.download([
            "speciesKey = " + str(species_key),
            "hasCoordinate = TRUE",
            #"year = 2023",
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
```

```
download key is 0020917-241007104925546
GBIF.org (17 October 2024) GBIF Occurrence Download
<https://doi.org/10.15468/dl.4d3k48>
```

```{python}
gbif_path
```

```
    '/home/jovyan/earth-analytics/data/species/gbif_siberian/0002798-241024112534372.csv'
```

### Load the GBIF data into Python

```{python}
gbif_df = pd.read_csv(
    gbif_path, 
    delimiter='\t',
    index_col='gbifID',
    on_bad_lines='skip',
    usecols=['gbifID', 'month', 'year', 'countryCode', 'stateProvince', 'decimalLatitude', 'decimalLongitude']
)
gbif_df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>countryCode</th>
      <th>stateProvince</th>
      <th>decimalLatitude</th>
      <th>decimalLongitude</th>
      <th>month</th>
      <th>year</th>
    </tr>
    <tr>
      <th>gbifID</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>985829831</th>
      <td>IN</td>
      <td>Rajasthan</td>
      <td>27.161905</td>
      <td>77.522800</td>
      <td>2.0</td>
      <td>1991.0</td>
    </tr>
    <tr>
      <th>979229641</th>
      <td>CN</td>
      <td>Jiangxi</td>
      <td>28.870571</td>
      <td>116.433170</td>
      <td>11.0</td>
      <td>1988.0</td>
    </tr>
    <tr>
      <th>978902062</th>
      <td>IR</td>
      <td>Mazandaran</td>
      <td>36.667110</td>
      <td>52.550186</td>
      <td>11.0</td>
      <td>2011.0</td>
    </tr>
    <tr>
      <th>978782158</th>
      <td>IN</td>
      <td>Rajasthan</td>
      <td>27.161905</td>
      <td>77.522800</td>
      <td>1.0</td>
      <td>1991.0</td>
    </tr>
    <tr>
      <th>977810003</th>
      <td>IN</td>
      <td>Rajasthan</td>
      <td>27.161905</td>
      <td>77.522800</td>
      <td>1.0</td>
      <td>1992.0</td>
    </tr>
  </tbody>
</table>
</div>

## Convert GBIF data to a GeoDataFrame by Month




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month</th>
      <th>year</th>
      <th>geometry</th>
    </tr>
    <tr>
      <th>gbifID</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>985829831</th>
      <td>2.0</td>
      <td>1991.0</td>
      <td>POINT (77.5228 27.1619)</td>
    </tr>
    <tr>
      <th>979229641</th>
      <td>11.0</td>
      <td>1988.0</td>
      <td>POINT (116.43317 28.87057)</td>
    </tr>
    <tr>
      <th>978902062</th>
      <td>11.0</td>
      <td>2011.0</td>
      <td>POINT (52.55019 36.66711)</td>
    </tr>
    <tr>
      <th>978782158</th>
      <td>1.0</td>
      <td>1991.0</td>
      <td>POINT (77.5228 27.1619)</td>
    </tr>
    <tr>
      <th>977810003</th>
      <td>1.0</td>
      <td>1992.0</td>
      <td>POINT (77.5228 27.1619)</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1019036144</th>
      <td>6.0</td>
      <td>1983.0</td>
      <td>POINT (-90 43.75)</td>
    </tr>
    <tr>
      <th>1019036117</th>
      <td>6.0</td>
      <td>1983.0</td>
      <td>POINT (-90 43.75)</td>
    </tr>
    <tr>
      <th>1019036092</th>
      <td>6.0</td>
      <td>1983.0</td>
      <td>POINT (-90 43.75)</td>
    </tr>
    <tr>
      <th>1019036069</th>
      <td>6.0</td>
      <td>1983.0</td>
      <td>POINT (-90 43.75)</td>
    </tr>
    <tr>
      <th>1019035937</th>
      <td>6.0</td>
      <td>1983.0</td>
      <td>POINT (-90 43.75)</td>
    </tr>
  </tbody>
</table>
<p>2870 rows × 3 columns</p>
</div>



### Download and save ecoregion boundaries

Ecoregions represent boundaries formed by biotic and abiotic conditions: geology, landforms, soils, vegetation, land use, wildlife, climate, and hydrology.

    /home/jovyan/earth-analytics/data/species/wwf_ecoregions/wwf_ecoregions.shp





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>area</th>
      <th>geometry</th>
    </tr>
    <tr>
      <th>ecoregion</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Adelie Land tundra</td>
      <td>0.038948</td>
      <td>MULTIPOLYGON (((158.7141 -69.60657, 158.71264 ...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Admiralty Islands lowland rain forests</td>
      <td>0.170599</td>
      <td>MULTIPOLYGON (((147.28819 -2.57589, 147.2715 -...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Aegean and Western Turkey sclerophyllous and m...</td>
      <td>13.844952</td>
      <td>MULTIPOLYGON (((26.88659 35.32161, 26.88297 35...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Afghan Mountains semi-desert</td>
      <td>1.355536</td>
      <td>MULTIPOLYGON (((65.48655 34.71401, 65.52872 34...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Ahklun and Kilbuck Upland Tundra</td>
      <td>8.196573</td>
      <td>MULTIPOLYGON (((-160.26404 58.64097, -160.2673...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>842</th>
      <td>Sulawesi lowland rain forests</td>
      <td>9.422097</td>
      <td>MULTIPOLYGON (((117.33111 -7.53306, 117.30525 ...</td>
    </tr>
    <tr>
      <th>843</th>
      <td>East African montane forests</td>
      <td>5.010930</td>
      <td>MULTIPOLYGON (((36.7375 -3.13, 36.7375 -3.1316...</td>
    </tr>
    <tr>
      <th>844</th>
      <td>Eastern Arc forests</td>
      <td>0.890325</td>
      <td>MULTIPOLYGON (((36.38 -8.96583, 36.38 -8.96667...</td>
    </tr>
    <tr>
      <th>845</th>
      <td>Borneo montane rain forests</td>
      <td>9.358407</td>
      <td>MULTIPOLYGON (((112.82394 -0.5066, 112.82298 -...</td>
    </tr>
    <tr>
      <th>846</th>
      <td>Kinabalu montane alpine meadows</td>
      <td>0.352694</td>
      <td>MULTIPOLYGON (((116.52616 6.11011, 116.52734 6...</td>
    </tr>
  </tbody>
</table>
<p>847 rows × 3 columns</p>
</div>



    Stored 'ecoregions_gdf' (GeoDataFrame)
    Stored 'gdf_monthly' (GeoDataFrame)


Identify the ecoregion for each observation




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>month</th>
      <th>year</th>
      <th>name</th>
    </tr>
    <tr>
      <th>ecoregion</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5</th>
      <td>3.0</td>
      <td>2015.0</td>
      <td>Al-Hajar foothill xeric woodlands and shrublands</td>
    </tr>
    <tr>
      <th>5</th>
      <td>7.0</td>
      <td>2014.0</td>
      <td>Al-Hajar foothill xeric woodlands and shrublands</td>
    </tr>
    <tr>
      <th>5</th>
      <td>3.0</td>
      <td>2015.0</td>
      <td>Al-Hajar foothill xeric woodlands and shrublands</td>
    </tr>
    <tr>
      <th>5</th>
      <td>12.0</td>
      <td>2017.0</td>
      <td>Al-Hajar foothill xeric woodlands and shrublands</td>
    </tr>
    <tr>
      <th>8</th>
      <td>12.0</td>
      <td>2011.0</td>
      <td>Alashan Plateau semi-desert</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>802</th>
      <td>2.0</td>
      <td>2023.0</td>
      <td>Yellow Sea saline meadow</td>
    </tr>
    <tr>
      <th>802</th>
      <td>2.0</td>
      <td>2015.0</td>
      <td>Yellow Sea saline meadow</td>
    </tr>
    <tr>
      <th>802</th>
      <td>1.0</td>
      <td>2018.0</td>
      <td>Yellow Sea saline meadow</td>
    </tr>
    <tr>
      <th>802</th>
      <td>1.0</td>
      <td>2018.0</td>
      <td>Yellow Sea saline meadow</td>
    </tr>
    <tr>
      <th>802</th>
      <td>12.0</td>
      <td>2014.0</td>
      <td>Yellow Sea saline meadow</td>
    </tr>
  </tbody>
</table>
<p>2205 rows × 3 columns</p>
</div>



Count the observations in each ecoregion each year and month




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>occurrences</th>
      <th>norm_occurrences</th>
    </tr>
    <tr>
      <th>ecoregion</th>
      <th>month</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5</th>
      <th>3.0</th>
      <td>2</td>
      <td>0.100000</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">24</th>
      <th>5.0</th>
      <td>6</td>
      <td>0.166667</td>
    </tr>
    <tr>
      <th>9.0</th>
      <td>2</td>
      <td>0.166667</td>
    </tr>
    <tr>
      <th>53</th>
      <th>3.0</th>
      <td>9</td>
      <td>0.100000</td>
    </tr>
    <tr>
      <th>74</th>
      <th>1.0</th>
      <td>3</td>
      <td>0.016949</td>
    </tr>
    <tr>
      <th>...</th>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">758</th>
      <th>5.0</th>
      <td>20</td>
      <td>0.141093</td>
    </tr>
    <tr>
      <th>6.0</th>
      <td>16</td>
      <td>0.067725</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">802</th>
      <th>1.0</th>
      <td>4</td>
      <td>0.022599</td>
    </tr>
    <tr>
      <th>2.0</th>
      <td>3</td>
      <td>0.026810</td>
    </tr>
    <tr>
      <th>12.0</th>
      <td>2</td>
      <td>0.013863</td>
    </tr>
  </tbody>
</table>
<p>78 rows × 2 columns</p>
</div>






<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>occurrences</th>
      <th>norm_occurrences</th>
    </tr>
    <tr>
      <th>ecoregion</th>
      <th>year</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5</th>
      <th>2015.0</th>
      <td>2</td>
      <td>0.176471</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">24</th>
      <th>2014.0</th>
      <td>2</td>
      <td>0.156250</td>
    </tr>
    <tr>
      <th>2017.0</th>
      <td>2</td>
      <td>0.066667</td>
    </tr>
    <tr>
      <th>2024.0</th>
      <td>2</td>
      <td>0.137931</td>
    </tr>
    <tr>
      <th>53</th>
      <th>2020.0</th>
      <td>4</td>
      <td>0.062378</td>
    </tr>
    <tr>
      <th>...</th>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>758</th>
      <th>1996.0</th>
      <td>3</td>
      <td>0.084746</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">802</th>
      <th>2014.0</th>
      <td>2</td>
      <td>0.125000</td>
    </tr>
    <tr>
      <th>2015.0</th>
      <td>3</td>
      <td>0.211765</td>
    </tr>
    <tr>
      <th>2018.0</th>
      <td>3</td>
      <td>0.031169</td>
    </tr>
    <tr>
      <th>2023.0</th>
      <td>2</td>
      <td>0.032520</td>
    </tr>
  </tbody>
</table>
<p>135 rows × 2 columns</p>
</div>






    <Axes: xlabel='year', ylabel='norm_occurrences'>




    
![png](siberian-crane-species-download_files/siberian-crane-species-download_33_1.png)
    


Create a simplified GeoDataFrame for plot




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>area</th>
      <th>geometry</th>
    </tr>
    <tr>
      <th>ecoregion</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Adelie Land tundra</td>
      <td>0.038948</td>
      <td>MULTIPOLYGON EMPTY</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Admiralty Islands lowland rain forests</td>
      <td>0.170599</td>
      <td>POLYGON ((16411777.375 -229101.376, 16384825.7...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Aegean and Western Turkey sclerophyllous and m...</td>
      <td>13.844952</td>
      <td>MULTIPOLYGON (((3391149.749 4336064.109, 33846...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Afghan Mountains semi-desert</td>
      <td>1.355536</td>
      <td>MULTIPOLYGON (((7369001.698 4093509.259, 73168...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Ahklun and Kilbuck Upland Tundra</td>
      <td>8.196573</td>
      <td>MULTIPOLYGON (((-17930832.005 8046779.358, -17...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>842</th>
      <td>Sulawesi lowland rain forests</td>
      <td>9.422097</td>
      <td>MULTIPOLYGON (((14113374.546 501721.962, 14128...</td>
    </tr>
    <tr>
      <th>843</th>
      <td>East African montane forests</td>
      <td>5.010930</td>
      <td>MULTIPOLYGON (((4298787.669 -137583.786, 42727...</td>
    </tr>
    <tr>
      <th>844</th>
      <td>Eastern Arc forests</td>
      <td>0.890325</td>
      <td>MULTIPOLYGON (((4267432.68 -493759.165, 428533...</td>
    </tr>
    <tr>
      <th>845</th>
      <td>Borneo montane rain forests</td>
      <td>9.358407</td>
      <td>MULTIPOLYGON (((13126956.393 539092.917, 13136...</td>
    </tr>
    <tr>
      <th>846</th>
      <td>Kinabalu montane alpine meadows</td>
      <td>0.352694</td>
      <td>POLYGON ((12981819.186 696445.445, 12997053.80...</td>
    </tr>
  </tbody>
</table>
<p>847 rows × 3 columns</p>
</div>



    Stored 'gbif_path' (str)
    calendar	 cartopy	 ccrs	 credentials	 data_dir	 ecoregions_dir	 ecoregions_gdf	 ecoregions_path	 ecoregions_url	 
    env_variable	 first_result	 gbif_df	 gbif_dir	 gbif_ecoregion_gdf	 gbif_path	 gbif_pattern	 gdf_monthly	 get_monthly_regional_observations	 
    get_yearly_regional_observations	 getpass	 glob	 gpd	 gv	 hvplot	 occ	 occurrence_month_df	 occurrence_year_df	 
    os	 pathlib	 pd	 pn	 prompt_func	 prompt_text	 reset_credentials	 species	 species_info	 
    species_key	 time	 zipfile	 


Mapping monthly distribution




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>name</th>
      <th>area</th>
      <th>geometry</th>
      <th>norm_occurrences</th>
    </tr>
    <tr>
      <th>ecoregion</th>
      <th>year</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5</th>
      <th>2015.0</th>
      <td>Al-Hajar foothill xeric woodlands and shrublands</td>
      <td>4.099668</td>
      <td>POLYGON ((6264504.021 2842331.306, 6336024.085...</td>
      <td>0.176471</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">24</th>
      <th>2014.0</th>
      <td>Amur meadow steppe</td>
      <td>15.118769</td>
      <td>MULTIPOLYGON (((15067649.194 6001589.024, 1503...</td>
      <td>0.156250</td>
    </tr>
    <tr>
      <th>2017.0</th>
      <td>Amur meadow steppe</td>
      <td>15.118769</td>
      <td>MULTIPOLYGON (((15067649.194 6001589.024, 1503...</td>
      <td>0.066667</td>
    </tr>
    <tr>
      <th>2024.0</th>
      <td>Amur meadow steppe</td>
      <td>15.118769</td>
      <td>MULTIPOLYGON (((15067649.194 6001589.024, 1503...</td>
      <td>0.137931</td>
    </tr>
    <tr>
      <th>53</th>
      <th>2020.0</th>
      <td>Azerbaijan shrub desert and steppe</td>
      <td>6.794797</td>
      <td>POLYGON ((5427403.54 5089371.081, 5512543.361 ...</td>
      <td>0.062378</td>
    </tr>
    <tr>
      <th>...</th>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>758</th>
      <th>1996.0</th>
      <td>Upper Midwest US forest-savanna transition</td>
      <td>15.481685</td>
      <td>MULTIPOLYGON (((-9686382.157 5638236.966, -973...</td>
      <td>0.084746</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">802</th>
      <th>2014.0</th>
      <td>Yellow Sea saline meadow</td>
      <td>0.517810</td>
      <td>POLYGON ((13451648.07 3834357.593, 13303152.21...</td>
      <td>0.125000</td>
    </tr>
    <tr>
      <th>2015.0</th>
      <td>Yellow Sea saline meadow</td>
      <td>0.517810</td>
      <td>POLYGON ((13451648.07 3834357.593, 13303152.21...</td>
      <td>0.211765</td>
    </tr>
    <tr>
      <th>2018.0</th>
      <td>Yellow Sea saline meadow</td>
      <td>0.517810</td>
      <td>POLYGON ((13451648.07 3834357.593, 13303152.21...</td>
      <td>0.031169</td>
    </tr>
    <tr>
      <th>2023.0</th>
      <td>Yellow Sea saline meadow</td>
      <td>0.517810</td>
      <td>POLYGON ((13451648.07 3834357.593, 13303152.21...</td>
      <td>0.032520</td>
    </tr>
  </tbody>
</table>
<p>135 rows × 4 columns</p>
</div>



    Stored 'occurrence_gdf' (GeoDataFrame)





    BokehModel(combine_events=True, render_bundle={'docs_json': {'2b941de9-74b5-45fb-bd4f-44a4b3f3039b': {'version…



                                                   

    WARNING:W-1005 (FIXED_SIZING_MODE): 'fixed' sizing mode requires width and height to be set: figure(id='e565c90b-3e1c-4288-9d47-b6a7701154e7', ...)


    




    BokehModel(combine_events=True, render_bundle={'docs_json': {'5fc56a83-abe9-4ff0-b07f-4c26d84e4750': {'version…


