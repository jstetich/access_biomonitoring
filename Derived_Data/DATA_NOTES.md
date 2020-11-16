# Data Derivation
The `KML` files contained here was extracted from KMZ files in the 
"Original_Data" folder by converting the 'kmz' extension to `zip`, and
unzipping in Windows. We discarded the associated graphic symbols,
which we do not need.


# Data Format Summary
These `KML` files contain principally <Placemark> tags. Each Placemark
contains the following tags:  

*  <name>         - The name of the placemark.  This appears to relate to a sample or a station.
                    It usually corresponds to a code or ID in teh HTML
					
*  <visibility>  

*  <styleUrl>

*  <Snippet maxLines='0'> 

*  <description>  - Contains HTML encoded data (see below)

*  <Point>        - Contains a <coordinates> tag containing a pair of
                    floating point values, representing Longitude and
					Latitude (in that order).

##  HTML Data Format
The <description> tag contains a CDATA block that contains HTML.
The HTML consists of two tables.

The FIRST table provides data on the sampling location.  The rows of 
the table contain the data.  Each row contains two entries, a data name,
an he data contents, each contained in a table cell.  For example, the
first row of the <description> tag for one entry contained the following:
<tr><td>Station:
*  LITTLE ANDROSCOGGIN RIVER - STATION 43</td></tr>

Successive rows of this first table contain the following: 

*  Station

*  Station Number

*  Town

*  County

*  Major Drainage

*  Site TypeSample Type

*  Latitude

*  Longitude

In our experience, the latitude and longitude here matches the latitude
and longitude in the <coordinates> tag.

The Second Table follows a line o bolded text containing "Sample(s):".  
It contains one or more rows providing summary data on samples taken a this sampling
location ("Station" in our parlance.)  The first row of this second table 
provided table ccolumn headings, as follows:
*  Sample ID        (Apparently usually (always?) a number)
*  Sample Date      (In MM/DD/YYYY format) 
*  Statutory Class  (A code designating achieved class:  'A', 'B', 'C', 'NC')
*  Report           (Some samples have associated with them a PDF file containing
                     results of sampling.  If availalbe, this item contains an <a> tag
					 contianing a href to the report.
				C</td><td class='sample4'></td></tr>
				</td></tr>
				<td class='sample4'></td></tr>
				<td class='sample1'>183</td><td class='sample2'>9/4/1986</td><td class='sample2'>C</td><td class='sample4'></td></tr>
				<td class='sample1'>188</td><td class='sample2'>8/20/1987</td><td class='sample2'>C</td><td class='sample4'></td></tr>
				<td class='sample1'>366</td><td class='sample2'>8/25/1992</td><td class='sample2'>C</td><td class='sample4'></td></tr>
				<td class='sample1'>709</td><td class='sample2'>8/19/1998</td><td class='sample2'>C</td><td class='sample4'></td></tr>
				<td class='sample1'>1238</td><td class='sample2'>8/18/2003</td><td class='sample2'>C</td><td class='sample4'></td></tr>
<a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/reports/log_1727.pdf'>View</a></td></tr>
				<td class='sample1'>2209</td><td class='sample2'>8/19/2013</td><td class='sample2'>C</td><td class='sample4'><a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/reports/log_2209.pdf'>View</a></td></tr>
				<td class='sample1'>2662</td><td class='sample2'>8/15/2018</td><td class='sample2'>C</td><td class='sample4'></td></tr>
				</table>
				
After that table, the HTML contains lines containing links to 
DOWNSTREAM PHOTO (<IMG alt='BIOMONITORING DOWNSTREAM WEB PHOTO'....)
UPSTREAM PHOTO   (<IMG alt='BIOMONITORING UPSTREAM WEB PHOTO'....)
View or Print in web browser (the <a href =.... tag immediately preceeds that text)
