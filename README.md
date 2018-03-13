# ScrapeNTPMon
Scrape the monitoring data from www.pool.ntp.org and place it into local files

Description:
Python program to scrape the monitoring data from www.pool.ntp.org and place it into two comma separated value files.
The Raw Scrape file is the data received from the monitoring site, which is then processed into the Indexed Output.
The Indexed Output File is re-indexed and cleared of duplicates.
The Number of Rows to fetch from the monitoring site will vary depending upon how often this process is run.
If it is run frequently, the number may be lower.  If it is run once a day, a value around the default of 70 is suggested.
The monitoring site will not return more than 4000 rows in any query, which corresponds to approximately two months worth of monitoring data.   

Author:
Written and Tested by **CubeCentral Labs**
Contact:
cubecentralATgmailDOTcom

License:
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Review the GNU General Public License at <http://www.gnu.org/licenses/>

IMPORTANT NOTICE:
This program was written *without* the permission or direction of anyone, especially those at pool.ntp.org.
The use of this program should be done with consideration to their website and their infrastructure.
If they request that this program not be used against their website, then by all means CEASE RUNNING IT!
**CubeCentral Labs** will not be held responsible for the use or misuse of this program in any way shape or form and
strongly encourages everyone to use it carefully, lightly, and respectfully.  Comments and questions are welcome.

Less Important Notice:
I am not a professional programmer, and I am sure that it shows.  This was written at a hobbyist level for hobbyists.
Feel free to make changes to the program, and please do let me know of any changes or improvements that you make.
I am going to try to put this on GitHub, so we will see how well that goes.

Usage:
python scrapentpmon.py -h

usage: scrapentpmon.py [-h] [-r R] [-s S] [-o O] [-q] IPv4Address

positional arguments:
  IPv4Address  IP address of NTP Pool server data to lookup. Must be IPv4 and
               not a hostname

optional arguments:
  -h, --help   show this help message and exit
  -r R         number of rows of data to fetch from monitoring site. Default
               is 70
  -s S         path and filename for file used to store raw scrape data.
               Default is ./RawScrapeData.csv
  -o O         path and filename for file used to store re-indexed results.
               Default is ./IndexedOutput.csv
  -q           Do not output any messages. This includes any errors or
               warnings.

Suggestion:
Put it in its own directory and run it from there.  The data files will be created there and accessed from there.
