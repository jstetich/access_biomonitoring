'''
Maine DEP data are organized alternately by geographic locations --"Stations" 
in our parlance -- and "Samples."  Each Sample is associated with a station.

This script scans through a CSV file that includes Station ID Codes of
interest, then scans through a (statewide) list of Sample data, and makes a
copy that includes only data on Samples associated with those stations of
interest.

The logic here could constructively be encapsulated in function or class.
'''

#from urllib.request import urlopen
import os
from pathlib import Path
import csv
#import time


#%%
#################################
# Establish file paths for input and output files
# We isolate these calls here to facilitate editing for other uses.
#################################
rootdir =  Path(os.getcwd())   # os.getcwd() points to the python file home
print(rootdir.resolve())
myPath = rootdir               # Allows for indirection if necessary
Stationpath  = myPath / 'Invertebrate_Stations_CB.csv'
Samplepath = myPath /  'Biomonitoring_Samples_Parsed.csv'
Outpath = myPath / 'Invertebrate_Samples_CB.csv'
print(Stationpath.resolve())

#%%
#################################
# Set Up Column Names for reading Sample Data
# This assumes column names don't change.
##################################

Header = ['Station Number', 'Sample Type', 'Sample ID', 'Sample Date',
          'Statutory Class', 'Attained Class', 'Report',
          'Final Determination']

#%%
#########################
# Open three Files
# We do not use the with... form here because errors are informative.
#########################

try:
    stationfile = open(Stationpath, 'rU')
except:
    print( 'Could not open Sample File')
    stationfile.close()
    raise
try:
    samplefile = open(Samplepath, 'rU')
except:
    print( 'Could not open Parameter File')
    stationfile.close()
    samplefile.close()
    raise
try:
    outfile = open(Outpath, 'w')
except:
    print( 'Could not open Output File')
    stationfile.close()
    samplefile.close()
    outfile.close()
    raise
try:
    stationreader = csv.DictReader(stationfile)
    samplereader = csv.DictReader(samplefile)
    outwriter = csv.DictWriter(outfile, Header, delimiter=',', quotechar='"', lineterminator= '\r', quoting=csv.QUOTE_MINIMAL)
    outwriter.writeheader()
except:
    print( "Could not open files as CSV")
    stationfile.close()
    samplefile.close()
    outfile.close()
    raise
#%%
##############################
#Assemble a set of station IDs in Casco Bay
##############################
print( "Processing...")

# note! List comprehension is slick, but hard coding of column name here is
# rather inellegant. If we want to repackage this as a function, we'd need to
# change that.  Note that the only thing we need is a list with a unique
# Station ID.

StationList = [row['Station_Nu'] for row in stationreader]  
StationSet = set(StationList)

# Note that by reading the station numbers in a list comprehension,
# we have traversed the entire stationreader object

#########################
# Scan through the rows in the Sample data and make copies only of those
# that are assocaited with stations in the Casco Bay Station List.
#########################

for row in samplereader:
    #Test if Station is in Station List for Casco Bay
    if row['Station Number'] in StationSet:
        outwriter.writerow(row)
        print( row['Station Number'])
        
print("Processing complete...")

stationfile.close()
samplefile.close()
outfile.close()


