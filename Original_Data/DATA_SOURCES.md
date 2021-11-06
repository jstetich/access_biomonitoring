# Original KML File Data
Maine's Department of Environmental Protection makes certain data available on-line 
at <https://www.maine.gov/dep/gis/datamaps/>.   Among those data, the site 
exposes GIS data on stream and wetland biomonitoring via a `KML` file, 
`lawb_biomonitoring.kml`.

This file was downloaded by Curtis C. Bohlen on November 14, 2020.  The metadata on
the DEP web site stated the file was current as of (7/16/2020).

## File Structure
This KML file consists principally of <NetworkLink> tags pointing to other 
online resources.  These appear to be KMZ files containing similar
data, organized in different ways for display purposes.

A `KMZ` file is zip archive containing a `KML` file, often with other associated files.
The unzipped `KML` files are in the "Derived_Data" folder.

## Downloaded KMZ files
We work principally with the file found through the following URL:
<https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/lawb_biomonitoring_station.kmz>.

That file is modified and uploaded periodically, so the date of access matters.

We accessed that file on April 17th of 2019 successfully.  In November of 2020,
the file accessed through that URL contained only the "Statutory Class" field 
for individual sample results, and not the "Final Determination".  We have
contacted Maine DEP to alert them to the probem, but continue our analysis with the 
a data accessed in 2019.

