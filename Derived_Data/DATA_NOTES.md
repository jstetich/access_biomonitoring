# Summary of Steps
1.  Identify a Source KML file (`lawb_biomonitoring_station_2019.kml`).

2.  Run  `DataParserStation.py`, to generate statewide CSV files,
    `Biomonitoring_Samples_Parsed.csv` and `Biomonitoring_Stations_Parsed.csv`
    
3.  In GIS, select stations found in the Casco Bay watershed, saved as 
    `CB_Biomonitoting_Stations.csv` and `CB_Invertebrate_Stations.csv`, for all
    biomonitoting stations, and stream invertebrate invertebrate biomonitoring
    stations respectively.
    
4.  Run `SelectedStationDataSelector_all.py`. and
    `SelectedStationDataSelector_inverts.py`.  These scripts differ only in 
    the (hard coded) file names.  They produce `Biomonitoring_Samples_CB.csv`
    and `Invertebrate_Samples_CB.csv`.
    
5.  (Optional) Run `MostRecentDataSelector_all.py`, and
    `MostRecentDataSelector_inverts.py` (again, they differ only by hard coded
    file names). This step produces `Most_Recent_Samples_Casco_Bay.csv` and 
    `Most_Recent_Invert_Samples_Casco_Bay.csv`
    
6.  (Optional) Run `ParameterDataScraper.py` to generate 
    `Invertebrate_Parameters_CB.csv`. This is a large CSV file containing
    the underlying data (invertebrate counts, summaries, etc.) used to generate
    the "A", "B", "C" rankings based on invertebrate biomonitoring. 
    It does not successfully download associated data for all samples, but it
    gets most of them. 

#  KML Source Files
The `KML` file here `lawb_biomonitoring_station_2019.kml`, was extracted from
a KMZ file in the "Original_Data" folder by converting the 'kmz' extension to
`zip`, and unzipping in Windows. We discarded the associated graphic symbols,
which we do not need. See below for the format of the data contained in this
`KML` file.

# List of Output Files
The key output files that will be used for further analysis are the following:
*  `Biomonitoring_Stations_CB.csv`
*  `Invertebrate_Stations_CB.csv`
*  `Biomonitoring_Samples_CB.csv`
*  `Invertebrate_Samples_CB.csv`
*  `Most_Recent_Samples_CB.csv`
*  `Most_Recent_Invert_Samples_CB.csv`

# Explanation of Data Derivation
## Parsed CSV Files
The files `Biomonitoring_Samples_Parsed.csv` and `Biomonitoring_Stations_Parsed.csv`
Were generated from the KML files using a python script,`DataParserStation.py`,
and an associated "helper Class" defined in `htmlParse2Data.py`. 

The `DataParserStation.py` script is a simple script that instantiates 
a data parser, scans through the KML file and generates two CSV files, for
ease of further analysis.  Both input KML file and output CSV file names
are hard coded into the script.  To run `DataParserStation.py`, both the
source `KML` file and the helper python file, `htmlParse2Data.py` must be
in the same directory.

Users should be aware that the identity of some data columns is also hard
coded into the script, so results should be checked carefully for correct
column headers and missing data columns.

We have run the script through Spyder and Idle.  When we double click on
the python file in Windows, it briefly opens a command window, but
does not generate any output.  Running Python scripts directly from the
desktop in Windows is often problematic.

## Casco Bay Watershed Station Lists
We worked in ArcGIS to generate lists of biomonitoring
stations  and invertebrate biomonitoring stations in the Casco Bay Watershed. 
These  file is called `CB_Biomonitoting_Stations.csv` and
`CB_Invertebrate_Stations.csv`.  The process followed the obvious steps,
of importing latitude and longitude data from 
`Biomonitoring_Stations_Parsed.csv` into ArcGIS as an event layer, exporting
the data as a shapefile,  selecting points that overlap the Casco Bay
Watershed, (Filtering to Stream Invertebrate sampling stations if necessary).  The only complex step involvs adding local imperviousness to the data.  That involved
running a spatial merge with the Catchments Data Layer (see below)to extract
estimates of impervious cover in local catchements, and exporting the data
from ArcGIS. We removed unnecessary data colums, and changed the file
extension to ".csv".

## Casco Bay Watershed Sample Data
We generated `Biomonitoring_Samples_CB.csv` and
`Invertebrate_Samples_CB.csv` using python scripts, 
`SelectedStationDataSelector_all.py` and `SelectedStationDataSelector_inverts.py`.
The files contain sample results ONLY from stations within the Casco Bay
Watershed.  The two Python scripts differ only by including different hard
coded input and output file names.

# Most Recent Samples
We use data from the "most recent" samples to show "current" conditions for
each site.  Some of these historic observations, however, are fairly old, and
arguably not relevant for current status.  Further, filtering observations
would be simpler in R, but we had functioning code from 2015, which we updated
for 2020.

We use two Python scripts, including `MostRecentDataSelector_all.py` and
`MostRecentDataSelector_inverts.py` that differ only with regards to hard
coded file names.  The final produced files are
`Most_Recent_Samples_Casco_Bay.csv` and `Most_Recent_Invert_Samples_Casco_Bay.csv`

# Complete Parameter File
`ParameterDataScraper.py` is a python script that guesses at URLs for accessing
the underlying data associated with each biomonitoring sample, based on the
consistent format of links embedded in the KML source files.  To limit demand
on DEP servers, the script only (a) accesses data on invertebrate
biomonitoting stations, (b) incorporates a number of delays before retrying
URLS that do not work. Expect teh script to take a long time (~ 15 minutes)
to run.

The script does not successfully download data for all samples, but it gets
most of them.  It principally misses data for data with Sample ID with the
format "SA-###-YEAR". These appear to all be Algae samples, which currently
have invalid links to underlying data, and presumably, either lack underlying
data or use a different URL format. We have not taken time to add code to
filter those candidate URLs out, which would speed running the script.

The script produces `Invertebrate_Parameters_CB.csv`, which
is a large CSV file containing all the underlying data (invertebrate counts,
summaries, etc.) used to generate the "A", "B", "C" rankings in the KML
files.

# GIS Files
## Biomonitoring Locations
We generated our geospatial data showing stream invertebrate biomonitoring
locations as follows (intermediate geospatial layers are not exposed in the Git archive):

1.  We imported  latitude and longitude data from `Biomonitoring_Stations_Parsed.csv`
    into ArcGIS as an event layer, exporting the data as a shapefile, 
    `DEP_Biomonitoring`

2.  We selected points that overlap the Casco Bay Watershed, using 
    'Select by Location', producing `CB_Biomonitoring`

3.  We then further filtered to select only stream invertebrate sampling
    stations, using "Select by Attributes" to select biomonitoring stations
    with "Sample_Typ" == "Macroinvertebrate", producing the final
    `CB_Inverebrate_Biomonitoring` shapefile included in the GIT archive.

4.  Finally, we exported that files attribute table as a text (comma delimited) file,
    as described above to create the Casco Bay Watershed Station List descrived above.

## Catchments 
Since Maine has no recent high resolution state-wide imperviouscover data, we
reused impervious cover data by catchment area we developed for the 2015
State of the Bay Report.  These data are based on impervious cover estimates from
Maine IF&W, based on a one meter pixel size.  Those estimates are based principally 
on aerial photography from 2007, so they represent on-the-ground conditions
from over a decade ago, but they are the most recent values available.  

Our derived data layer aggregated impervious cover data by (somewhat simplified)
NAD+ V2 catchement areas.  We simplified the NAD+ V2 catchements principally to
remove catchements under 50 Ha, and absorb some small coastal catchments
into adjacent areas that drain to the same coastal bodies of water.

Our notes from 2015 describe preparation of this data sets as follows:

1.	Starting from CascoBayCatchments_Over_50 Shapefile (derived brom NHD2+).  

2.	Copy data to a new file (CascoBayCatchments_Over_50_Imperviousness)  

3.	Add Data column for Area of imperviousness and Percent imperviousness.  

4.	Use ZonalStatisticsAsTable to produce a table that ties polygons to
        imperviousness.  The resulting table counts the impervious area, in square
        meters (because the original imperviousness grid had a resolution of
        one meter).  Sum would give the same answer, since each pixel is 1 m on
        a side.  

5.	Join the Catchment data layer to the results of ZonalStatisticAsTable. 
 
6.	Copy the value from the table for the Impervious Area for each polygon
        into the data column defined in step 2.  Remove the join.  Note that
        areas that contain no impervious cover trigger a ?warning? in this
        step, but the value added to the attribute table is correctly set to zero.  

7.	In the Percent Imperviousness column defined in step 2,
        Calculate percent impervious for each polygon from the catchment area in
        square meters and the impervious area in each.


# KML File Data Format Summary
These `KML` files contain principally <Placemark> tags. Each Placemark
contains the following tags:  

*  <name>         - The name of the placemark.  This appears to relate to a sample or a station.
                    It usually corresponds to a code or ID in the HTML
				
*  <visibility>  

*  <styleUrl>

*  <Snippet maxLines='0'> 

*  <description>  - Contains HTML encoded data (see below)

*  <Point>        - Contains a <coordinates> tag containing a pair of
                    floating point values, representing Longitude and
					Latitude (in that order).

##  HTML Data Format
The <description> tag contains a CDATA block that contains HTML. That
HTML contains all the data (both attributes and locations) that we need.
The HTML consists of two tables.

The FIRST table provides data on the sampling location.  The rows of 
the table contain the data.  Each row contains two entries, a data name,
and the data contents, each contained in a table cell.  For example, the
first row of the <description> tag for one entry contained the following:
<tr><td>Station:
*  LITTLE ANDROSCOGGIN RIVER - STATION 43</td></tr>

Successive rows of this first table contain the following: 

*  Station

*  Station Number

*  Town

*  County

*  Major Drainage

*  Site Type

*  Sample Type

*  Latitude

*  Longitude

In our experience, the latitude and longitude here matches the latitude
and longitude in the <coordinates> tag.  Similarly, the Station Number
in the HTML matches the <name> tag in the Placemark.

The Second Table follows a line of bolded text containing "Sample(s):".  
It contains one or more rows providing summary data on samples taken a this
sampling location ("Station" in our parlance.)  The first row of this
second table provided table column headings.  The contents of this table
have varied from time to time, so you need to check that the contents are as 
expected.

Prior to 2020, the data had the following contents:

*  Sample ID        (Apparently usually (always?) a number)  
*  Sample Date      (In MM/DD/YYYY format)  
*  Statutory Class  (A code designating achieved class:  'A', 'B', 'C', 'NC') 
*  Attained Class  
*  Report           (Some samples have associated with them a PDF file containing
                     results of sampling.  If availalbe, this item contains an <a> tag
		     containing a href to the report.  
*  Final Determination  

In 2020, the Attained Class and Final Determination Columns were missing.

After that table, the HTML contains lines containing links to photographs and a
an HTML version of the data.
DOWNSTREAM PHOTO (<IMG alt='BIOMONITORING DOWNSTREAM WEB PHOTO'....>)
UPSTREAM PHOTO   (<IMG alt='BIOMONITORING UPSTREAM WEB PHOTO'....>)
View or Print in web browser (the <a href =.... tag immediately preceeds that text)

# Data Parsing.
Two Python scripts included here were used to parse the data from KML to CSV files.

htmlparse2Data.py definies an HTML parser class that reads the DEP formatted KML file's
<description> tag.

Data Parser Station generates two CSV files, one listing stations, the other
listing samples, linked to the Stations data by a common "Station Number" key.

# Diving Deeper.
THE DEP KML files frequently contain links to underlying data files giving results
of biomonitoring in great detail.  These secondary links take two forms:  PDF reports
and CSV tabular summaries of individual parameters.  Both CSV and PDF files can
be downloaded from the DEP server using a simple URL request, if you know the appropriate
URL.  The URL format is fairly simple, consisting of a long header, followed by a
sample ID, and last, the ".csv. extension, as follows:

* the URL header: 
  "http://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/"

* A Sample ID Number:   e.g., Sample "314" from Station S-143. (We have a list of 
  Sample ID Numbers now.)

* The Suffix ".csv'

The resulting URL:
<http://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/314.csv>
accesses the CSV file, which can be saved directly, or parsed.

We have developed draft Python scripts to access and parse these CSV files, but
we do not use the raw CSV files in State of Casco Bay, so hey are not included
in the Git archive at this time.





