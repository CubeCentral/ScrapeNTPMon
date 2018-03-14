#!/usr/bin/python3
#
#   Description:
#   Python program to scrape the monitoring data from www.pool.ntp.org and place it into a sorted, indexed, comma separated value file.
#   The data is received from the monitoring site, added to the file, which is then re-indexed and cleared of duplicates.
#
#   The Number of Rows to fetch from the monitoring site will vary depending upon how often this process is run.
#   When it is run frequently, the number may be lower.  When it is run once a day, a value around the default of 80 is suggested.
#   If, at the end of the program, many rows are marked as Duplicate and are dropped, consider lowering this number.
#
#   The monitoring site will not return more than 4000 rows in any single query, which corresponds to approximately two months worth of monitoring data.
#
#   Author and Contact:
#   Written and Tested by **CubeCentral Labs** at cubecentralATgmailDOTcom
#
#   License:
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Review the GNU General Public License at <http://www.gnu.org/licenses/>
#
#   IMPORTANT NOTICE:
#   This program was written *without* the permission or direction of anyone, especially those at pool.ntp.org.
#   The use of this program should be done with consideration to their website and their infrastructure.
#   If they request that this program not be used against their website, then by all means CEASE RUNNING IT!
#   **CubeCentral Labs** will not be held responsible for the use or misuse of this program and strongly 
#   encourages everyone to use this program carefully, lightly, and respectfully.  Comments and questions are welcome.
#
#   Version 3.01
#
#

import sys, os
import pandas as pd
import argparse
from pathlib import Path
import ipaddress


# Set up command-line option parsing
parser = argparse.ArgumentParser(description="Scrape the monitoring data from www.pool.ntp.org and place it into a sorted, indexed, comma separated value file.  The data is received from the monitoring site, added to the file, which is then re-indexed and cleared of duplicates.  The Number of Rows to fetch from the monitoring site will vary depending upon how often this process is run.  When it is run frequently, this number may be lower.  When it is run once a day, a value around the default of 80 is suggested.  If, at the end of the program, many rows are marked as Duplicate and dropped, consider lowering this number.  The monitoring site will not return more than 4000 rows in any single query, which corresponds to approximately two months worth of monitoring data.")
parser.add_argument("IPaddress",help="the IP Address of NTP Pool Server data to lookup.  Must be either an IPv4 or IPv6 address and not a hostname.",type=str)
parser.add_argument("-r", help="the number of rows of data to fetch from monitoring site.  Default is 80.", default=80,type=int, metavar='rows')
parser.add_argument("-o", help="the path and filename for the writeable result data file.  Default is ./scrapentpmon.csv", default='./scrapentpmon.csv',type=str, metavar='filename')
parser.add_argument("-d", help="include a header line in the data file describing the fields.  Default is no header line.",default=False,action="store_true")
parser.add_argument("-q", action="store_true",help="quiet operation.  Do not output any messages. This includes any errors or warnings.  Use with care.", default=False)
parser.add_argument('-v', action='version', version='%(prog)s 3.01')
args = parser.parse_args()


IncludeHeader = args.d


# This "turns off" output to standard out if the Quiet option is selected
if args.q:
    sys.stdout = open(os.devnull, 'w')


# Evaluate the entered IP address to see if it is valid
print("Evaluating IP Address "+args.IPaddress+" ...",end=' ')
try:
    IPAddress = str(ipaddress.ip_address(args.IPaddress))
except:
    print("Invalid Address entered")
    raise SystemExit(1)


# IP Address appears to be valid and has passed the test
print("OK")
lenIPAddress = len(IPAddress)


# Evaluate the Number of Rows given to be sure they are in range
print(" "*(lenIPAddress+7),"Number of Rows ...",end=' ')
if args.r < 1:
    print("Error: Number of Rows must be more than zero.")
    raise SystemExit(1)

if args.r > 4000:
    print("Error: Number of Rows must be less than 4001.")
    raise SystemExit(1)


# Number of rows appears to be valid and has passed the tests
print("OK")
numrows = args.r


# Convert the entered path/filename into the proper format depending upon OS
print(" "*(lenIPAddress-5),"Checking filename and path ...",end=' ')
try:
    OutputFilePath = Path(args.o)
    OutputFilePath = OutputFilePath.expanduser()    
except:
    print("Error: Problem with filename or path.  Exiting.")
    raise SystemExit(1)


# Filename and path are valid
print("OK")


# Set the URL to use
fetchurl = 'http://www.pool.ntp.org/scores/' + IPAddress + '/log?limit=' + str(numrows)


# Perform the data fetch from the site
print(" "*(lenIPAddress+8),"Fetching Data ...",end=' ')
try:
    FetchedData = pd.read_csv(fetchurl)
except:
    print("Error: Cannot read from site.  Exiting.")
    raise SystemExit(1)


# Fetch of data completed OK
print("OK",len(FetchedData.index),"Rows")


# Reverse the order of the data, putting the newest record last
print(" "*(lenIPAddress+6),"Reordering Data ...",end=' ')
try:
    FetchedData=FetchedData.reindex(index=FetchedData.index[::-1])
except:
    print("Error: Problem reordering data.  Exiting.")
    raise SystemExit(1)


# Data re-order completed
print("OK",len(FetchedData.index),"Rows")


# Write the fetched data out to file
# The CSV Index is:
# ts_epoch,ts,offset,step,score,leap
#
# The first column of the data 'ts_epoch' is unique so it 
# can be used as a key or index in further analysis
#
# Note: this will simply append the new fetch onto the existing file
print(" "*(lenIPAddress-5),"Writing out to output file ...",end=' ')
try:
    OutputFile = open(str(OutputFilePath), 'a')
    FetchedData.to_csv(OutputFile,index=False,header=False)
    OutputFile.close()
except:
    print("Error: Problem writing to output file.  Exiting.")
    raise SystemExit(1)


# Write out to file completed
print("OK",len(FetchedData.index),"Rows")


# Now re-open the file fully into memory for duplicate processing...
print(" "*(lenIPAddress-3),"Opening file for reading ...",end=' ')
try:
    OutputFile = open(str(OutputFilePath), 'r')
    CheckData=pd.read_csv(OutputFile,names=['ts_epoch','ts','offset','step','score','leap'])
    OutputFile.close()
except:
    print("Error: Problem reading from file.  Exiting.")
    raise SystemExit(1)


# Check for existing header row in file
TestDupeHeader = CheckData.columns == CheckData.iloc[0]
if TestDupeHeader.all():
    # Drop that row containing header
    CheckData.drop(CheckData.head(1).index, inplace=True)


# Read of file completed OK
lenCheckData=len(CheckData.index)
print("OK",lenCheckData,"Rows")


# Drop the duplicate entries from the data
print(" "*(lenIPAddress-13),"Reindexing and dropping duplicates ...",end=' ')
try:
    CheckData.sort_values('ts_epoch',inplace=True)
    CheckData.drop_duplicates(subset='ts_epoch', keep='first', inplace=True)
except:
    print("Error: Unable to reindex and drop duplicates.  Exiting.")
    raise SystemExit(1)


# Data sort and drop duplicates completed
lenAfterDrop=len(CheckData.index)
print("OK",lenCheckData-lenAfterDrop,"Duplicate Rows discarded")


# Output the new data to the finished file
print(" "*(lenIPAddress-5),"Writing out to output file ...",end=' ')
try:
    IndexedOutputFile = open(str(OutputFilePath),'w')
    CheckData.to_csv(IndexedOutputFile,index=False,header=IncludeHeader)
    IndexedOutputFile.close()
except:
    print("Error: Problem writing to output file.  Exiting.")
    raise SystemExit(1)


# Write out to file with new data completed
print("OK",len(CheckData.index),"Rows written out",end=' ')
if IncludeHeader: 
    print("with header line")
else:
    print("without header line")


# All done, report and end
print()
print("Processing finished successfully.  No errors reported.  Inspect output file for results.")
raise SystemExit(0)