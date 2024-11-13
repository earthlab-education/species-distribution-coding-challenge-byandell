# Access locations and times of Veery encounters

For this challenge, you will use a database called the [Global
Biodiversity Information Facility (GBIF)](https://www.gbif.org/). GBIF
is compiled from species observation data all over the world, and
includes everything from museum specimens to photos taken by citizen
scientists in their backyards.

<link rel="stylesheet" type="text/css" href="./assets/styles.css"><div class="callout callout-style-default callout-titled callout-task"><div class="callout-header"><div class="callout-icon-container"><i class="callout-icon"></i></div><div class="callout-title-container flex-fill">Try It: Explore GBIF</div></div><div class="callout-body-container callout-body"><p>Before your get started, go to the <a
href="https://www.gbif.org/occurrence/search">GBIF occurrences search
page</a> and explore the data.</p></div></div>

> **Contribute to open data**
>
> You can get your own observations added to GBIF using
> [iNaturalist](https://www.inaturalist.org/)!

### Set up your code to prepare for download

We will be getting data from a source called [GBIF (Global Biodiversity
Information Facility)](https://www.gbif.org/). We need a package called
`pygbif` to access the data, which may not be included in your
environment. Install it by running the cell below:

<link rel="stylesheet" type="text/css" href="./assets/styles.css"><div class="callout callout-style-default callout-titled callout-task"><div class="callout-header"><div class="callout-icon-container"><i class="callout-icon"></i></div><div class="callout-title-container flex-fill">Try It: Import packages</div></div><div class="callout-body-container callout-body"><p>In the imports cell, we’ve included some packages that you will need.
Add imports for packages that will help you:</p>
<ol type="1">
<li>Work with reproducible file paths</li>
<li>Work with tabular data</li>
</ol></div></div>

    /opt/conda/lib/python3.11/site-packages/dask/dataframe/__init__.py:42: FutureWarning: 
    Dask dataframe query planning is disabled because dask-expr is not installed.
    
    You can install it with `pip install dask[dataframe]` or `conda install dask`.
    This will raise in a future version.
    
      warnings.warn(msg, FutureWarning)



<script type="esms-options">{"shimMode": true}</script><style>*[data-root-id],
*[data-root-id] > * {
  box-sizing: border-box;
  font-family: var(--jp-ui-font-family);
  font-size: var(--jp-ui-font-size1);
  color: var(--vscode-editor-foreground, var(--jp-ui-font-color1));
}

/* Override VSCode background color */
.cell-output-ipywidget-background:has(
    > .cell-output-ipywidget-background > .lm-Widget > *[data-root-id]
  ),
.cell-output-ipywidget-background:has(> .lm-Widget > *[data-root-id]) {
  background-color: transparent !important;
}
</style>







<div id='p1011'>
  <div id="d4deb318-44cc-4e9b-b41e-1dde069212ba" data-root-id="p1011" style="display: contents;"></div>
</div>
<script type="application/javascript">(function(root) {
  var docs_json = {"1a37f9ce-0f50-40e7-9130-04d9231f472b":{"version":"3.5.2","title":"Bokeh Application","roots":[{"type":"object","name":"panel.models.browser.BrowserInfo","id":"p1011"},{"type":"object","name":"panel.models.comm_manager.CommManager","id":"p1012","attributes":{"plot_id":"p1011","comm_id":"0cca1c2d449b4591a8fd724f8b4231fd","client_comm_id":"a5aeef464a63414a9d73f8eec9150dd4"}}],"defs":[{"type":"model","name":"ReactiveHTML1"},{"type":"model","name":"FlexBox1","properties":[{"name":"align_content","kind":"Any","default":"flex-start"},{"name":"align_items","kind":"Any","default":"flex-start"},{"name":"flex_direction","kind":"Any","default":"row"},{"name":"flex_wrap","kind":"Any","default":"wrap"},{"name":"gap","kind":"Any","default":""},{"name":"justify_content","kind":"Any","default":"flex-start"}]},{"type":"model","name":"FloatPanel1","properties":[{"name":"config","kind":"Any","default":{"type":"map"}},{"name":"contained","kind":"Any","default":true},{"name":"position","kind":"Any","default":"right-top"},{"name":"offsetx","kind":"Any","default":null},{"name":"offsety","kind":"Any","default":null},{"name":"theme","kind":"Any","default":"primary"},{"name":"status","kind":"Any","default":"normalized"}]},{"type":"model","name":"GridStack1","properties":[{"name":"mode","kind":"Any","default":"warn"},{"name":"ncols","kind":"Any","default":null},{"name":"nrows","kind":"Any","default":null},{"name":"allow_resize","kind":"Any","default":true},{"name":"allow_drag","kind":"Any","default":true},{"name":"state","kind":"Any","default":[]}]},{"type":"model","name":"drag1","properties":[{"name":"slider_width","kind":"Any","default":5},{"name":"slider_color","kind":"Any","default":"black"},{"name":"value","kind":"Any","default":50}]},{"type":"model","name":"click1","properties":[{"name":"terminal_output","kind":"Any","default":""},{"name":"debug_name","kind":"Any","default":""},{"name":"clears","kind":"Any","default":0}]},{"type":"model","name":"FastWrapper1","properties":[{"name":"object","kind":"Any","default":null},{"name":"style","kind":"Any","default":null}]},{"type":"model","name":"NotificationAreaBase1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0}]},{"type":"model","name":"NotificationArea1","properties":[{"name":"js_events","kind":"Any","default":{"type":"map"}},{"name":"notifications","kind":"Any","default":[]},{"name":"position","kind":"Any","default":"bottom-right"},{"name":"_clear","kind":"Any","default":0},{"name":"types","kind":"Any","default":[{"type":"map","entries":[["type","warning"],["background","#ffc107"],["icon",{"type":"map","entries":[["className","fas fa-exclamation-triangle"],["tagName","i"],["color","white"]]}]]},{"type":"map","entries":[["type","info"],["background","#007bff"],["icon",{"type":"map","entries":[["className","fas fa-info-circle"],["tagName","i"],["color","white"]]}]]}]}]},{"type":"model","name":"Notification","properties":[{"name":"background","kind":"Any","default":null},{"name":"duration","kind":"Any","default":3000},{"name":"icon","kind":"Any","default":null},{"name":"message","kind":"Any","default":""},{"name":"notification_type","kind":"Any","default":null},{"name":"_destroyed","kind":"Any","default":false}]},{"type":"model","name":"TemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"BootstrapTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"TemplateEditor1","properties":[{"name":"layout","kind":"Any","default":[]}]},{"type":"model","name":"MaterialTemplateActions1","properties":[{"name":"open_modal","kind":"Any","default":0},{"name":"close_modal","kind":"Any","default":0}]},{"type":"model","name":"ReactiveESM1"},{"type":"model","name":"JSComponent1"},{"type":"model","name":"ReactComponent1"},{"type":"model","name":"AnyWidgetComponent1"},{"type":"model","name":"request_value1","properties":[{"name":"fill","kind":"Any","default":"none"},{"name":"_synced","kind":"Any","default":null},{"name":"_request_sync","kind":"Any","default":0}]}]}};
  var render_items = [{"docid":"1a37f9ce-0f50-40e7-9130-04d9231f472b","roots":{"p1011":"d4deb318-44cc-4e9b-b41e-1dde069212ba"},"root_ids":["p1011"]}];
  var docs = Object.values(docs_json)
  if (!docs) {
    return
  }
  const py_version = docs[0].version.replace('rc', '-rc.').replace('.dev', '-dev.')
  async function embed_document(root) {
    var Bokeh = get_bokeh(root)
    await Bokeh.embed.embed_items_notebook(docs_json, render_items);
    for (const render_item of render_items) {
      for (const root_id of render_item.root_ids) {
	const id_el = document.getElementById(root_id)
	if (id_el.children.length && id_el.children[0].hasAttribute('data-root-id')) {
	  const root_el = id_el.children[0]
	  root_el.id = root_el.id + '-rendered'
	  for (const child of root_el.children) {
            // Ensure JupyterLab does not capture keyboard shortcuts
            // see: https://jupyterlab.readthedocs.io/en/4.1.x/extension/notebook.html#keyboard-interaction-model
	    child.setAttribute('data-lm-suppress-shortcuts', 'true')
	  }
	}
      }
    }
  }
  function get_bokeh(root) {
    if (root.Bokeh === undefined) {
      return null
    } else if (root.Bokeh.version !== py_version) {
      if (root.Bokeh.versions === undefined || !root.Bokeh.versions.has(py_version)) {
	return null
      }
      return root.Bokeh.versions.get(py_version);
    } else if (root.Bokeh.version === py_version) {
      return root.Bokeh
    }
    return null
  }
  function is_loaded(root) {
    var Bokeh = get_bokeh(root)
    return (Bokeh != null && Bokeh.Panel !== undefined)
  }
  if (is_loaded(root)) {
    embed_document(root);
  } else {
    var attempts = 0;
    var timer = setInterval(function(root) {
      if (is_loaded(root)) {
        clearInterval(timer);
        embed_document(root);
      } else if (document.readyState == "complete") {
        attempts++;
        if (attempts > 200) {
          clearInterval(timer);
	  var Bokeh = get_bokeh(root)
	  if (Bokeh == null || Bokeh.Panel == null) {
            console.warn("Panel: ERROR: Unable to run Panel code because Bokeh or Panel library is missing");
	  } else {
	    console.warn("Panel: WARNING: Attempting to render but not all required libraries could be resolved.")
	    embed_document(root)
	  }
        }
      }
    }, 25, root)
  }
})(window);</script>



<script type="esms-options">{"shimMode": true}</script><style>*[data-root-id],
*[data-root-id] > * {
  box-sizing: border-box;
  font-family: var(--jp-ui-font-family);
  font-size: var(--jp-ui-font-size1);
  color: var(--vscode-editor-foreground, var(--jp-ui-font-color1));
}

/* Override VSCode background color */
.cell-output-ipywidget-background:has(
    > .cell-output-ipywidget-background > .lm-Widget > *[data-root-id]
  ),
.cell-output-ipywidget-background:has(> .lm-Widget > *[data-root-id]) {
  background-color: transparent !important;
}
</style>









    '/home/jovyan/earth-analytics/data/species/gbif_siberian'



:::

### Register and log in to GBIF

You will need a [GBIF account](https://www.gbif.org/) to complete this
challenge. You can use your GitHub account to authenticate with GBIF.
Then, run the following code to save your credentials on your computer.

> **Warning**
>
> Your email address **must** match the email you used to sign up for
> GBIF!

> **Tip**
>
> If you accidentally enter your credentials wrong, you can set
> `reset_credentials=True` instead of `reset_credentials=False`.

### Get the species key

> ** Your task**
>
> 1.  Replace the `species_name` with the name of the species you want
>     to look up
> 2.  Run the code to get the species key




    ('Grus leucogeranus', 2474961)






    2474961



### Download data from GBIF

::: {.callout-task title=“Submit a request to GBIF”

1.  Replace `csv_file_pattern` with a string that will match **any**
    `.csv` file when used in the `glob` function. HINT: the character
    `*` represents any number of any values except the file separator
    (e.g. `/`)

2.  Add parameters to the GBIF download function, `occ.download()` to
    limit your query to:

    -   observations
    -   from 2023
    -   with spatial coordinates.

3.  Then, run the download. **This can take a few minutes**. :::

    -   Can check progress at <https://www.gbif.org/user/download>.




    'speciesKey =2474961'



download key is 0020917-241007104925546
GBIF.org (17 October 2024) GBIF Occurrence Download https://doi.org/10.15468/dl.4d3k48




    '/home/jovyan/earth-analytics/data/species/gbif_siberian/0002798-241024112534372.csv'



### Load the GBIF data into Python

<link rel="stylesheet" type="text/css" href="./assets/styles.css"><div class="callout callout-style-default callout-titled callout-task"><div class="callout-header"><div class="callout-icon-container"><i class="callout-icon"></i></div><div class="callout-title-container flex-fill">Try It: Load GBIF data</div></div><div class="callout-body-container callout-body"><ol type="1">
<li>Look at the beginning of the file you downloaded using the code
below. What do you think the <strong>delimiter</strong> is?</li>
<li>Run the following code cell. What happens?</li>
<li>Uncomment and modify the parameters of <code>pd.read_csv()</code>
below until your data loads successfully and you have only the columns
you want.</li>
</ol></div></div>

You can use the following code to look at the beginning of your file:

I copied from <https://github.com/lauren-alexandra/lauren-alexandra.github.io/blob/main/willow-flycatcher-distribution/willow-flycatcher-distribution.ipynb>
and Lauren Gleason

    gbifID	datasetKey	occurrenceID	kingdom	phylum	class	order	family	genus	species	infraspecificEpithet	taxonRank	scientificName	verbatimScientificName	verbatimScientificNameAuthorship	countryCode	locality	stateProvince	occurrenceStatus	individualCount	publishingOrgKey	decimalLatitude	decimalLongitude	coordinateUncertaintyInMeters	coordinatePrecision	elevation	elevationAccuracy	depth	depthAccuracy	eventDate	day	month	year	taxonKey	speciesKey	basisOfRecord	institutionCode	collectionCode	catalogNumber	recordNumber	identifiedBy	dateIdentified	license	rightsHolder	recordedBy	typeStatus	establishmentMeans	lastInterpreted	mediaType	issue
    985829831	4fa7b334-ce0d-4e88-aaae-2e0c138d049e	URN:catalog:CLO:EBIRD:OBS131267733	Animalia	Chordata	Aves	Gruiformes	Gruidae	Grus	Grus leucogeranus		SPECIES	Leucogeranus leucogeranus (Pallas, 1773)	Leucogeranus leucogeranus		IN	Bharatpur--Keoladeo Ghana NP	Rajasthan	PRESENT	7	e2e717bf-551a-4917-bdc9-4fa0f342c530	27.161905	77.5228							1991-02-03	3	2	1991	9531123	2474961	HUMAN_OBSERVATION	CLO	EBIRD	OBS131267733				CC_BY_4_0		obsr280577			2024-04-17T08:23:51.075Z		CONTINENT_DERIVED_FROM_COORDINATES;TAXON_MATCH_TAXON_CONCEPT_ID_IGNORED





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


