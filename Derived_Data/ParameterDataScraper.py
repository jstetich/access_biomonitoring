'''
Look up water quality data from the DEP website.

Defines a class that scrapes data from on-line CSV files accessed via an HTTP
connection. The class was designed to look up multi-parameter data from the
Maine DEP web site. Some characteristics of the class are specific to that
purpose, but could be generalized.

The DEP data is exposed through a hyperlink presented as part of the data
available via the 'description' tag of DEP's biomonitoring KML files.  A
separate Python script Parses the KML file for Station and Sample IDs.  A
second filters the Sample Data for data associated with Stations of Interest.

This script, and the associated class, takes a list of Sample IDs and
constructs the implied URL to access the underlying raw parameter data.

The URL is constructed in a simple way based on the Sample ID.
This script looks at a CSV file that includes biomonitoring sample IDs of
interest, constructs the relelvant URL, downloads the associated file,
parses it, and writes the data to a growing file that aggregates water quality
data from multiple samples into one large CSV file.

When running this script, the URL fails to download the relevant file from
time to time. Thi appears to be related to the speed of response of the DEP
server. Rather than fixing that here, the script writes the sample codes
associated with the failed lookups to the console.  If you are running this
from an IDE, you can copy text from the console and run a second script to
look those Sample IDs up seperately.
'''

#%%

import os
import csv
import time

from urllib.request import urlopen
from pathlib import Path
from io import StringIO

#%%

###################################
# Constants
###################################
URLPrefix = 'http://www.maine.gov/dep/gis/datamaps/lawb_biomonitoring/results/'
SampleIDHeader = 'Sample ID'


###############
# File links
###############

rootdir =  Path(os.getcwd())   # os.getcwd() points to the python file home
print(rootdir.resolve())

inFileName =  'Invertebrate_Samples_CB.csv'
outFileName = 'Invertebrate_Parameters_CB.csv'
unreadFileName = "Biomonitoring_Samples_Not_Read.csv"

myPath = rootdir               # Allows for indirection if necessary

inpath = myPath / inFileName
outpath  = myPath / outFileName
unreadpath = myPath /  unreadFileName


#%%

class DEP_Raw_Data_Scraper:
    '''
    Scrapes data from on-line CSV data files provided by Maine
    DEP.  The files provide detailed data on biomonitoring samples, including
    all parameters associated with those samples.

    The class scrapes data from on-line CSV files accessed via an HTTP
    connection. The class was designed to look up multi-parameter data from the
    Maine DEP web site.
    '''

##################################
#Set Up Column Names for reading
#This assumes column names don't change.
##################################
    def __init__(self, path, outname):
        '''
        Parameters:
                path == a STRING specifying a path.
                outname == a STRING specifying the name out the output CSVfile
        '''

        self.ColNames = ["EGAD_SEQ","Sample ID","Sample Date","Sample Medium",
                         "Sample Method","Replicates","Sampled By","Test",
                         "Parameter Category","Parameter","Value","Units",
                         "Justification"]
        self.SampleIDName = "Sample ID"
        self.URLPrefix = URLPrefix
        self.myPath = path
        self.outFileName = outname
        self.unread = []
        self.maxtries = 3   # Maximum number of tries to download a CSV before giving up
        self.sleeptime = 2  # Time in seconds to wait between successive tries.  not sure if this makes any difference....
        self.openfilelink(path, outname)
        self.timeout = 2    # time to wait before declaring a timeout error
        self.waittime = 0    # time to wait before each try at accessing data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.parameterfile.close()
        if myScraper.unread:
           print ("Failed to read the following Sample IDs:")
           self.printUnread()

    def openfilelink(self,myPath, outFilename):
        #########################
        #Open the CSV file that will hold the combined output
        #########################
        theoutpath = myPath / outFilename
        try:
           self.parameterfile = open(theoutpath, 'w')
        except:
           print ('Could not open Parameter File')
           raise
        try:
           self.parameterwriter = csv.writer(self.parameterfile,
                                             delimiter=',',
                                             quotechar='"',
                                             lineterminator= '\r',
                                             quoting=csv.QUOTE_MINIMAL)
        except:
           print( "Could not open output file as CSV")
           self.parameterfile.close()
           raise
        try:
           #Write the CSV header row
           self.parameterwriter.writerow(self.ColNames)
        except:
           print( 'Could not write the header row')
           self.parameterfile.close()
           raise

    def accessCSV(self, SampleID):
        '''
        Accesses a CSV file as a URL and returns a urllib2 file-like object.
        '''
        ###############
        #Assemble URI
        ###############
        URIText = self.URLPrefix + SampleID.strip() + ".csv"
        #print(URIText)
        ######################
        #Download the CSV File
        ######################
        try:
           response = urlopen(URIText, None, self.timeout)
           # response.read() returns a bytes object
           # In Python 3, that marks binary bytes, or ascii-only text
           # But for reading into csv, I want a str, so I need to decode
           r = response.read().decode()
           return r
        except Exception as e:
           #print "             *****         ",
           #print e.args,
           #print "             *****         "
           return False

    def scrape(self,SampleNames):
        '''
        Scrapes data from the DEP website
        Calls accessCSV up to self.maxtries times in an attempt to access the
        CSV file. If successful, adds the data from that file to the growing
        parameter CSV file.
        '''
        self.unread = []
        for row in SampleNames:
           time.sleep(self.waittime)
           print ("*****  ", row, "  *****    ",)
           print ("Trying:",)
           #could add code here to extract the header row from the first CSV
           # downloaded
           result = False
           tries = 0
           while not result and tries < self.maxtries:
              tries += 1
              print (tries,)
              result = self.accessCSV(row)
              #print(result[1:500])
              #if tries == 1:
              #   print self.URLPrefix + row.strip() + ".csv"
              if not result:
                 time.sleep(self.sleeptime)
                 if tries == self.maxtries:
                    print ("    Failed")
                    self.unread.append(row)

           ##################
           # Open the response as CSV to parse, and write to output
           ##################
           if result:
               # result is a string, containing
               # the CSV file contents. To work with the csv reader,
               # according to the documentation, we need an interator
               # One way to manage that is with StringIO
              result_flo = StringIO(result, newline = None )
              count = 0
              try:
                 URIReader = csv.DictReader(result_flo)
              except:
                 print ("Could not open URI for Row", row, "as CSV")
                 raise
              for aRow in URIReader:
                  count = count + 1
                  #print(aRow)
                  try:
                    #Assemble the data from the CSV file
                    self.parameterwriter.writerow([aRow[item] for item in self.ColNames])
                  except Exception as e:
                    print ("          Failure writing row", count, "for", row, ".")
                    print ("             *****         ")
                    print (e.args[0])
                    print ("             *****         ")
                    continue

    def printUnread(self):
        for item in self.unread: print(item)


    def recordUnread(self, mypath, myfilename):
        try:
           unreadfile = open(unreadpath, 'w')
           unreadwriter = csv.writer(unreadfile,
                                     delimiter=',',
                                     quotechar='"',
                                     lineterminator= '\r', quoting=csv.QUOTE_MINIMAL)
           #The folowing is almost certainly a problem...
           unreadwriter.writerow(self.SampleIDName)
        except:
           print ('Could not Open the Unread Samples file for writing.')
           unreadfile.close()
           raise

        for item in self.unread: unreadwriter.writerow([item])
        unreadfile.close()

#%%


if __name__ == "__main__":
   # Parse in-file here and assemble scraper list
   # could structure this as another with block, but then I don't know how to
   # provide an informative print of what went wrong....
   try:
      samplefile = open(inpath, 'r')
   except:
      print ('Could not open Sample File')
      raise
   try:
      samplereader = csv.DictReader(samplefile)
   except:
      print ("Could not open Sample File as CSV")
      samplefile.close()
      raise
   for row in samplereader:
      samplenames = [row[SampleIDHeader] for row in samplereader]

   #Now, scrape data associated with those Sample IDs
   with DEP_Raw_Data_Scraper(myPath, outFileName) as myScraper:
     myScraper.scrape(samplenames)
     myScraper.recordUnread(myPath, unreadFileName)

   samplefile.close()
