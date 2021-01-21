
"""
Scans through a list of water quality samples, each associated with specific
Stations, and selects the most recent sample for each Station.  The latest
Sample provides the most recent information on local conditions, which we can
show in a map of figure.

This is simpler to do in R, and 
"""

import os
import csv
from pathlib import Path

import datetime as dt  # will use both the dt.datetime and dt.date modules

#################################
#Set Up Column Names for reading
##################################
Header = ['Station Number', 'Sample Type', 'Sample ID', 'Sample Date',
          'Statutory Class', 'Final Determination', 'Attained Class', 'Report']


##############################
# File Referneces
##############################

SampleFileName = 'Biomonitoring_Samples_CB.csv'
OutFileName = 'Most_Recent_Samples_CB.csv'

rootdir =  Path(os.getcwd())   # os.getcwd() points to the python file home
myPath = rootdir               # Allows for indirection if necessary
Samplepath = myPath /  SampleFileName
Outpath = myPath / OutFileName

#########################
#Open two Files
#########################
try:
    samplefile = open(Samplepath, 'r')
except:
    print( 'Could not open Parameter File')
    samplefile.close()
    raise
try:
    outfile = open(Outpath, 'w')
except:
    print( 'Could not open Output File')
    samplefile.close()
    outfile.close()
    raise
try:
    samplereader = csv.DictReader(samplefile)
    outwriter = csv.DictWriter(outfile, Header, delimiter=',', quotechar='"', lineterminator= '\r', quoting=csv.QUOTE_MINIMAL)
    outwriter.writeheader()
except:
    print( "Could not open files as CSV")
    samplefile.close()
    outfile.close()
    raise

##############################
# Scan File row by row, and select the latest record
# This method assumes the input file is sorted by Station Number
# but is scans appropriately for dates and sample times
##############################
aformat = '%m/%d/%Y'
curStationNum = ""
latestbugs = dict()
latestalgae = dict()
latestwet = dict()
curAlgaeDate = dt.datetime.strptime('1/01/1980', aformat).date()  # prior to any samples
curBugsDate = dt.datetime.strptime('1/01/1980', aformat).date()  # prior to any samples
curWetDate = dt.datetime.strptime('1/01/1980', aformat).date()  # prior to any samples
print( 'Processing...')
for row in samplereader:
    date = dt.datetime.strptime(row['Sample Date'], aformat).date()
    if row['Station Number'] == curStationNum:
        # we're still processing the current station
        # priority we need to check if we're looking at a more recent date and 
        # if so, update the stored date and row
        # one problem is that the most recent sample may or may not have an
        #  associated Class determination. Here I want the most recent sample
        # with a related class determination.
        if (row['Sample Type'] == 'ALGAE' and
            row['Final Determination'] and
            row['Final Determination'] != '--'):
            if date > curAlgaeDate:
                latestalgae = row
                curAlgeaDate = date
        elif (row['Sample Type'] == 'MACROINVERTEBRATE' and 
              row['Final Determination'] and 
              row['Final Determination'] != '--'):
            if date > curBugsDate:
                latestbugs = row
                curBugsDate = date
        elif (row['Sample Type'] == 'WETLAND' and 
              row['Final Determination'] and 
              row['Final Determination'] != '--'):
             if date > curWetDate:
                latestwet = row
                curWetDate = date
        else:
            pass
    else:   # We're onto a new Station
            # output results, if any, and start up the next station
            # note that this wil NOT be called for the last record,
            # since at EOF, we're not reading a new row.
        if latestbugs:  #Check if we have a bugs record for this station at all
            outwriter.writerow(latestbugs)
            latestbugs = dict()
        if latestalgae:  #Check if we have an algae record for this station at all
            outwriter.writerow(latestalgae)
            latestalgae = dict()
        if latestwet:  #Check if we have a wetland record for this station at all
            outwriter.writerow(latestwet)
            latestwet = dict()    
        curStationNum = row['Station Number']  # Record the neew station number
        if (row['Sample Type'] == 'ALGAE' and
            row['Final Determination'] and
            row['Final Determination'] != '--'):
            curAlgaeDate = date
            latestalgae = row
        elif (row['Sample Type'] == 'MACROINVERTEBRATE' and 
              row['Final Determination'] and 
              row['Final Determination'] != '--'):
            curBugsDate = date
            latestbugs = row
        elif (row['Sample Type'] == 'WETLAND' and 
              row['Final Determination'] and 
              row['Final Determination'] != '--'):
            curWetDate = date
            latestbugs = row

#One last pass through to write out the last station's data, if any
if latestbugs:  #Check if we have a bugs record for this station at all
    outwriter.writerow(latestbugs)
if latestalgae:  #Check if we have an algae record for this station at all
    outwriter.writerow(latestalgae)
if latestwet:  #Check if we have an algae record for this station at all
    outwriter.writerow(latestwet)

print( 'Processing complete.')

samplefile.close()
outfile.close()


