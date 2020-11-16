# Accessing Maine DEP's Biomonitoring Data

Maine's Department of Environmental Protection makes certain data available on-line 
at <https://www.maine.gov/dep/gis/datamaps/>.   Among those data, the site 
exposes GIS dta on stream biomonitoring via a `KML` file, `lawb_biomonitoring.kml`.

`KML` files are used by (*inter alia*) Google Earth to represente geographic data.
At their heart, `KML` files are a specific flavor of `XML`, and they can be parsed
successfully by tools able to parse KML files.  Unfortunately, KML files are also
very flexible, and the data we are interested in finding can be buried in complex
ways.

1. `KML` files are hierarchical, so that one `KML` file can refer to data embedded
   in other files in the internet.  In fact, the raw `KML` file DEP exposes (above)
   refers to several other files, that contain the actual grographic data.

2. `KML` files often contain embeded data that is itself HTML encoded. The default
   way that ArcGIS creates `KML` files apparently embeds the attribute table for each
   feature in an embedded `HTML` table. When we access the attributes, we need to
   parse an HTML table embeded in a `XML` folder.

3.  Closely related `KMZ` files are zip-encoded `KML` files, generally sipped along
    with related information, such as symbols used to diplay the geographic data.

4.  Some related metadata and associated detailed data is contained in files not
    directly accessed by the KML files, but whose names can be inferred from the 
    attribute data.

The repository contains python code for examining, unpacking, accessing and
organizing data derived from the data provided by DEP, by working our way back 
from file to supporting file.
