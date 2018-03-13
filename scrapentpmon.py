#!/usr/bin/python3
#
#   Description:
#   Python program to scrape the monitoring data from www.pool.ntp.org and place it into two comma separated value files.
#   The Raw Scrape file is the data received from the monitoring site, which is then processed into the Indexed Output.
#   The Indexed Output File is re-indexed and cleared of duplicates.
#   The Number of Rows to fetch from the monitoring site will vary depending upon how often this process is run.
#   If it is run frequently, the number may be lower.  If it is run once a day, a value around the default of 70 is suggested.
#   The monitoring site will not return more than 4000 rows in any query, which corresponds to approximately two months worth of monitoring data.   
#
#   Author:  Written and Tested by **CubeCentral Labs**          Contact:  cubecentralATgmailDOTcom
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
#   **CubeCentral Labs** will not be held responsible for the use or misuse of this program in any way shape or form and
#   strongly encourages everyone to use it carefully, lightly, and respectfully.  Comments and questions are welcome.
#
#

import sys, os
import pandas as pd
import csv
import argparse
from pathlib import Path
import socket

# Function to check validity of IPv4 Address Format
def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


# Set up command-line option parsing
parser = argparse.ArgumentParser(description="Scrapes the monitoring data from www.pool.ntp.org and places it into two comma separated value files.  The Raw Scrape file is the data received from the monitoring site, which is then processed into the Indexed Output.  The Indexed Output File is re-indexed and cleared of duplicates.  The Number of Rows to fetch from the monitoring site will vary depending upon how often this process is run.  If it is run frequently, the number may be lower.  If it is run once a day, a value around the default of 70 is suggested.  The monitoring site will not return more than 4000 rows in any query, which corresponds to approximately two months worth of monitoring data.")
parser.add_argument("IPv4Address",help="IP address of NTP Pool server data to lookup.  Must be IPv4 and not a hostname",type=str)
parser.add_argument("-r", help="number of rows of data to fetch from monitoring site.  Default is 70", default=70,type=int)
parser.add_argument("-s", help="path and filename for file used to store raw scrape data.  Default is ./RawScrapeData.csv", default='./RawScrapeData.csv',type=str)
parser.add_argument("-o", help="path and filename for file used to store re-indexed results.  Default is ./IndexedOutput.csv", default='./IndexedOutput.csv', type=str)
parser.add_argument("-d", help="Include a header line in re-indexed Indexed Output file.  Default is no header line.",default=False,action="store_true")
parser.add_argument("-q", action="store_true",help="Do not output any messages. This includes any errors or warnings.", default=False)
args = parser.parse_args()

HeaderInc = args.d


# This "turns off" output to standard out if the Quiet option is selected
if args.q:
    sys.stdout = open(os.devnull, 'w')

# Evaluate the entered IP address to see if it is valid - consists of two tests
print("Evaluating IP Address "+args.IPv4Address+" ...",end=' ')

if validate_ip(args.IPv4Address):
    print("OK")
else:
    print("ERROR: Invalid IP Address Format.")
    raise SystemExit(1)

print("   Testing IP Address "+args.IPv4Address+" ...",end=' ')

try:
    socket.inet_aton(args.IPv4Address)
    print("OK")
except socket.error:
    print("Error: IP Address failed test.")
    raise SystemExit(1)

# IPv4 Address appears to be valid and has passed the tests
ipaddr = args.IPv4Address
ipaddrlen = len(ipaddr)

# Evaluate the Number of Rows given to be sure they are in range
if args.r < 1:
    print("Error: Number of Rows must be more than zero.")
    raise SystemExit(1)

if args.r > 4000:
    print("Error: Number of Rows must be less than 4001.")
    raise SystemExit(1)

# Number of rows appears to be valid and has passed the tests
print(" "*(ipaddrlen+7),"Number of Rows ... OK")
numrows = args.r


# Convert the entered path/filename into the proper format depending upon OS
print(" "*(ipaddrlen-8),"Checking Raw Scrape Data file ...",end=' ')
try:
    RawScrapeFilePath = Path(args.s)
    RawScrapeFilePath = RawScrapeFilePath.expanduser()
    print("OK")
except:
    print("Error: Problem with Raw Scrape Data filename or path.  Exiting.")
    raise SystemExit(1)

print(" "*(ipaddrlen-7),"Checking Indexed Output file ...",end=' ')
try:
    IndexedOutputFilePath = Path(args.o)
    IndexedOutputFilePath = IndexedOutputFilePath.expanduser()
    print("OK")
except:
    print("Error: Problem with Indexed Output filename or path.  Exiting.")
    raise SystemExit(1)


print(" "*(ipaddrlen+2),"Filenames and paths ... OK")


# Set the URL to use
fetchurl = 'http://www.pool.ntp.org/scores/' + ipaddr + '/log?limit=' + str(numrows)

#
# BEGIN Processing
#

# Perform the data fetch from the site
print(" "*(ipaddrlen+8),"Fetching Data ...",end=' ')
try:
    FetchedData = pd.read_csv(fetchurl)
    print("OK",len(FetchedData.index),"Rows")
except:
    print("Error: Cannot read from site.  Exiting.")
    raise SystemExit(1)


# Reverse the order of the data, putting the newest record last
print(" "*(ipaddrlen+6),"Reordering Data ...",end=' ')
try:
    FetchedData=FetchedData.reindex(index=FetchedData.index[::-1])
    print("OK",len(FetchedData.index),"Rows")
except:
    print("Error: Problem reordering data.  Exiting.")
    raise SystemExit(1)

# Write the fetched data out to file
# The CSV Index is:
# ts_epoch,ts,offset,step,score,leap
#
# The first column of the data should be unique so it 
# can be used as a key or index in further analysis
#
# Note: this will simply append the new fetch onto the existing file
print(" "*(ipaddrlen-5),"Writing out to Scrape file ...",end=' ')
try:
    RawScrapeFile = open(str(RawScrapeFilePath), 'a')
    FetchedData.to_csv(RawScrapeFile,index=False,header=False)
    RawScrapeFile.close()
    print("OK",len(FetchedData.index),"Rows")
except:
    print("Error: Problem writing to Scrape File.  Exiting.")
    raise SystemExit(1)

# Now re-open the File fully into memory
# for duplicate processing...
print(" "*(ipaddrlen-10),"Opening Scrape file for reading ...",end=' ')
try:
    RawScrapeFile = open(str(RawScrapeFilePath), 'r')
    CheckData=pd.read_csv(RawScrapeFile,names=['ts_epoch','ts','offset','step','score','leap'])
    RawScrapeFile.close()
    lenCheckData=len(CheckData.index)
    print("OK",lenCheckData,"Rows")
except:
    print("Error: Problem reading from SCape File.  Exiting.")
    raise SystemExit(1)

# Drop the duplicate entries from the data
print(" "*(ipaddrlen-13),"Reindexing and dropping duplicates ...",end=' ')
try:
    CheckData.drop_duplicates(keep='first',inplace=True)
    lenAfterDrop=len(CheckData.index)
    print("OK",lenCheckData-lenAfterDrop,"Duplicate Rows discarded")
except:
    print("Error: Unable to reindex and drop duplicates.  Exiting.")
    raise SystemExit(1)

# Output the new data to the finished file
print(" "*(ipaddrlen-13),"Writing out to Indexed Output file ...",end=' ')
try:
    IndexedOutputFile = open(str(IndexedOutputFilePath),'w')
    CheckData.to_csv(IndexedOutputFile,index=False,header=HeaderInc)
    IndexedOutputFile.close()
    print("OK",len(CheckData.index),"Rows written out",end=' ')
    if HeaderInc: 
        print("with header line")
    else:
        print("without header line")
except:
    print("Error: Problem writing to Indexed Output file.  Exiting.")
    raise SystemExit(1)

print()
print("Processing finished successfully.  No errors reported.  Inspect Indexed Output file for results.")
raise SystemExit(0)


