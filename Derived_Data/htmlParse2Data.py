'''
Creates an HTML parser class designed to extract data from the HTML associated
with biomonitoring data presented as the 'description' tag of KML files.

 The
Maine_DEP_HTML_Parser class subclasses the abstract HTMLParser class in the standard
HTMLParser module. 

'''


# from xml.etree import ElementTree as ET

from html.parser import HTMLParser


##  The following example text is included here only so that you can run this 
##  file and see what the  Maine_DEP_HTML_Parser class does.

## This example was derived from data accessed in November of 2019. 

testtxt = '''
				<table border='0' padding='0' width='400'>
				<tr><td>Station:</td><td>MEDUXNEKEAG RIVER - STATION 1</td></tr>
				<tr><td>Station Number:</td><td>S-1</td></tr>
				<tr><td>Town:</td><td>HOULTON</td></tr>
				<tr><td>County:</td><td>AROOSTOOK</td></tr>
				<tr><td>Major Drainage:</td><td>ST. JOHN</td></tr>
				<tr><td>Site Type:</td><td>STREAM/RIVER BIOMONITORING</td></tr>
				<tr><td>Sample Type:</td><td>MACROINVERTEBRATE</td></tr>
				<tr><td>Latitude:</td><td>46.18118700</td></tr>
				<tr><td>Longitude:</td><td>-67.80406700</td></tr>
				</table>
				<b>Sample(s):</b>
				<table border='1' padding='0' width='500'>
				<tr><td>Sample ID</td><td>Sample Date</td><td>Statutory Class</td><td>Attained Class</td><td>Report</td><td>Final Determination</td></tr>
				<tr><td><a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/1.csv'>1</a></td><td>8/22/1983</td><td>B</td><td>Yes</td><td></td><td class='sample5'>B</td></tr>
				<tr><td><a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/331.csv'>331</a></td><td>9/11/1991</td><td>B</td><td>Yes</td><td></td><td class='sample5'>A</td></tr>
				<tr><td><a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/754.csv'>754</a></td><td>9/24/1998</td><td>B</td><td>Yes</td><td></td><td class='sample5'>A</td></tr>
				<tr><td><a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/953.csv'>953</a></td><td>8/17/1999</td><td>B</td><td>Yes</td><td></td><td class='sample5'>A</td></tr>
				<tr><td><a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/967.csv'>967</a></td><td>8/24/2000</td><td>B</td><td>Yes</td><td></td><td class='sample5'>A</td></tr>
				<tr><td><a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/1912.csv'>1912</a></td><td>8/19/2004</td><td>B</td><td>Yes</td><td></td><td class='sample5'>B</td></tr>
				</table>
				<br />DOWNSTREAM PHOTO
				<br />2011 downstream site photo
				<p><IMG alt='BIOMONITORING DOWNSTREAM WEB PHOTO' src='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/photos/s001(down)_7-2011.JPG' align=textTop width=400></p>
				<br />UPSTREAM PHOTO
				<br />2011 upstream site photo
				<p><IMG alt='BIOMONITORING UPSTREAM WEB PHOTO' src='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/photos/s001(up)_7-2011.JPG' align=textTop width=400></p>
				<br/>
				<a href='https://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/station_web/S-1M.htm'>View or Print in web browser</a>
				<br/>
'''


# create a subclass and override the handler methods
class Maine_DEP_HTML_Parser(HTMLParser):
    ''' Read data from HTML tables as formated by DEP for display via KMLs
    and store    Station Data as a dictionary, and Sample Data as a list of
    Dictionaries.

    The stored values are suitable for exporting to CSVs.

    The DEP biomonitoring Station data is divided into two tables embeded in
    the "description" tag of each Placemark.

    The first table contains data on the biomonitoring Station.
    It is organized such that each row contans two items, a name (with a 
    following colon), followed by the associated value.

    The second table is a variable length list of samples associated with the
    station. The organization is different, with a single heder row, followed
    by data. The list of items in this second table is standardized as follows:
        
    Sample ID, Sample Date, Statutory Class, Attained Class, Report, Final
    Determination

    The SampleID tag often contains and attribute which is a URL for an
    associated table providing detailed sample information. An Example URL:

    href='http://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/SA-1-2002.csv

    But we don't need to store the whole URL, since it can be assembled
    from its components, if you know the Sample ID.
    '''

    def __init__(self):
        HTMLParser.__init__(self)
        self.tablecount = 0   # this counts top level tables only;
                              # We want to parse tables 1 and 2 differently
        self.rowcount = 0  
        self.itemcount = 0
        self.curDictPair = {'Key': None, 'Value': None}  # initalize empty pair
        self.StationData = dict()
        self.SampleData = dict()
        self.SampleDataList = []

        self.ColNames = ['Sample ID', 'Sample Date',
                         'Statutory Class', 'Attained Class',
                         'Report', 'Final Determination']
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.rowcount = 0
            self.tablecount = self.tablecount + 1
        elif tag == 'tr':
            self.rowcount = self.rowcount + 1
            self.itemcount = 0
            if self.tablecount == 2:
                self.SampleData["Station Number"] = self.StationData["Station Number"]  #record the unique identifier to match samples to sites
                self.SampleData["Sample Type"] = self.StationData["Sample Type"]        #Convenient for looking at the sample file
 
        elif tag == 'td':
            self.itemcount = self.itemcount + 1
        else: pass
    
    def handle_endtag(self, tag):
        if tag == 'table':
            self.rowcount = 0
        if tag == 'tr':
            if self.tablecount == 1:
                self.StationData[self.curDictPair['Key']] = self.curDictPair['Value']
                self.curDictPair['Key'] = None
                self.curDictPair['Value'] = None
            if self.tablecount == 2:
                if self.rowcount > 1:
                    self.SampleDataList.append(self.SampleData)
                    self.SampleData = dict()
            self.itemcount = 0
            
    def handle_data(self, data):
        if self.tablecount == 1:
            if self.itemcount == 1:
                self.curDictPair['Key'] = data.strip().replace(':', '').replace('\r','').replace('\n', '')    #Eliminate the colon at the end of the name.
            if self.itemcount == 2:
                self.curDictPair['Value'] = data.strip()
        if self.tablecount == 2:
            self.SampleData[self.ColNames[self.itemcount - 1]] = data.strip()

    def close(self):
        HTMLParser.close(self)
        self.tablecount = 0   # this counts top level tables only;
                              # for this application, we parse tables 1 and 2
                              # differently
        self.rowcount = 0  
        self.itemcount = 0
        self.curDictPair = {'Key': None, 'Value': None} # initalize empty pair
        self.StationData = dict()
        self.SampleData = dict()
        self.SampleDataList = []

if __name__ == "__main__":
# instantiate the parser and fed it some HTML.  this will need to be repeated
# for every placemark.
    parser = Maine_DEP_HTML_Parser()
    parser.feed(testtxt)
    print('########################################')
    print('Station Data')
    print('########################################')
    print(parser.StationData)
    print('\n\n########################################')
    print('Sample Data')
    print('########################################')
    for Data in parser.SampleDataList:
        print(Data)
    parser.close()
