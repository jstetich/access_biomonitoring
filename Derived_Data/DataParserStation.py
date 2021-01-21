'''
Extracts DEP water quality data from a KML file. (lawb_biomonitoring_station.kml)
The data we want is located in the description tag of each placemark.
This script uses the xml.etree ElementTree module to parse the kml file
and isolate the description tags.  It then uses an instance of
Maine_DEP_HTML_Parser class (defined in the helper module "htmlParse2Dat.py")
to parse the description tag into data that can be saved as a csv data file.

'''
import os
import csv
from pathlib import Path
from htmlParse2Data import Maine_DEP_HTML_Parser
from xml.etree import ElementTree as ET

########################
# Set Up Header Rows
# The header row column order and contents have changed since 2015
# And they changed again in 2020, omitting some necessary data.
# You need to confirm that these data columns are still correct.
########################
StationHeader = ['Station Number', 'Station', 
                 'Town', 'County',
                 'Major Drainage', 'Site Type',
                 'Sample Type',
                 'Latitude', 'Longitude']

SampleHeader =  ['Station Number', 'Sample Type', 'Sample ID', 'Sample Date',
                 'Statutory Class',  'Attained Class',
                 'Report', 'Final Determination']


##########################
#Setup filepaths
##########################
rootdir =  Path(os.getcwd())   # os.getcwd() points to the python file home
print(rootdir.resolve())

StationFileName = 'Biomonitoring_Stations_Parsed.csv'
SampleFileName =  'Biomonitoring_Samples_Parsed.csv'
KMLFileName = 'lawb_biomonitoring_station_2019.kml'


myPath = rootdir               # Allows for indirection if necessary

KMLpath = myPath / KMLFileName
Stationpath  = myPath / StationFileName
Samplepath = myPath /  SampleFileName


#########################
#Open the CSV files that will hold the combined output
#########################
try:
    stationfile = open(Stationpath, 'w')
except:
    print('Could not open Station File')
    stationfile.close()
    raise
try:
    samplefile = open(Samplepath, 'w')
except:
    print('Could not open Sample File')
    samplefile.close()
    raise

# Initialize them as CSV writers
try:
    samplewriter  = csv.DictWriter(samplefile,  SampleHeader,
                                   extrasaction='ignore', delimiter=',',
                                   quotechar='"', lineterminator= '\r',
                                   quoting=csv.QUOTE_MINIMAL)
    stationwriter = csv.DictWriter(stationfile, StationHeader,
                                   extrasaction='ignore', delimiter=',',
                                   quotechar='"', lineterminator= '\r',
                                   quoting=csv.QUOTE_MINIMAL)
except:
    print("Could not open files as CSV")
    samplefile.close()
    stationfile.close()
    raise

try:
    #Write the CSV header rows
    aRow = dict()
    for item in StationHeader:
        aRow[item] = item
    stationwriter.writerow(aRow)
    aRow = dict()
    for item in SampleHeader:
        aRow[item] = item
    samplewriter.writerow(aRow)
    
except:
    print('Could not write the header row')
    samplefile.close()
    stationfile.close()
    raise

##################
#Open the XML File
##################
try:
    kmlfile = open(KMLpath, 'rb')
except:
    print('Could not open KML File')
    kmlfile.close()
    raise

#################
#Create the HTML Parser
#################
parser = Maine_DEP_HTML_Parser()

##################
#Parse the KML File
##################
tree = ET.parse(kmlfile)
root = tree.getroot()
for info in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark/'
                         '{http://www.opengis.net/kml/2.2}description'):
    
    parser.feed(info.text)
   # print('*********************')
   # print(parser.StationData['Station Number'])
    stationwriter.writerow(parser.StationData)
    print(parser.StationData)
    for Data in parser.SampleDataList:
        #print('------------------------')
        #print(Data['Sample ID'])
        samplewriter.writerow(Data)
    parser.close()

   
################
#Final Cleanup
################
samplefile.close()
stationfile.close()
kmlfile.close()


