# ScrapeNTPMon
Scrape the monitoring data from www.pool.ntp.org and place it into a local file


#### Description:
Python program to scrape the monitoring data from www.pool.ntp.org and place it into a sorted, indexed, comma separated value file.
The data is received from the monitoring site, added to the file, which is then re-indexed and cleared of duplicates.

The Number of Rows to fetch from the monitoring site will vary depending upon how often this process is run.
When it is run frequently, the number may be lower.  When it is run once a day, a value around the default of 80 is suggested.
If, at the end of the program, many rows are marked as Duplicate and are dropped, consider lowering this number.

The monitoring site will not return more than 4000 rows in any single query, which corresponds to approximately two months worth of monitoring data.



#### Author:
Written and Tested by **CubeCentral Labs**

#### Contact:
cubecentralATgmailDOTcom


#### License:
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Review the GNU General Public License at <http://www.gnu.org/licenses/>


#### IMPORTANT NOTICE:
This program was written *without* the permission or direction of anyone, especially those at pool.ntp.org.
The use of this program should be done with consideration to their website and their infrastructure.
If they request that this program not be used against their website, then by all means CEASE RUNNING IT!
**CubeCentral Labs** will not be held responsible for the use or misuse of this program in any way shape or form and
strongly encourages everyone to use it carefully, lightly, and respectfully.  Comments and questions are welcome.


#### Less Important Notice:
I am not a professional programmer, and I am sure that it shows.  This was written at a hobbyist level for hobbyists.
Feel free to make changes to the program, and please do let me know of any changes or improvements that you make.
I am going to try to put this on GitHub, so we will see how well that goes.


### Usage:
python scrapentpmon.py -h

*or*

python3 scrapentpmon.py -h


```usage: scrapentpmon.py [-h] [-r R] [-o O] [-d] [-q] [-v] IPaddress

Scrape the monitoring data from www.pool.ntp.org and place it into a sorted,
indexed, comma separated value file. The data is received from the monitoring
site, added to the file, which is then re-indexed and cleared of duplicates.
The Number of Rows to fetch from the monitoring site will vary depending upon
how often this process is run. When it is run frequently, this number may be
lower. When it is run once a day, a value around the default of 80 is
suggested. If, at the end of the program, many rows are marked as Duplicate
and dropped, consider lowering this number. The monitoring site will not
return more than 4000 rows in any single query, which corresponds to
approximately two months worth of monitoring data.


##### positional arguments:


  *IPaddress*   the IP Address of NTP Pool Server data to lookup. Must be either
                an IPv4 or IPv6 address and not a hostname.
                
                

##### optional arguments:


  -h, --help  show this help message and exit
  
  -r R        the number of rows of data to fetch from monitoring site.
              Default is 80.
              
  -o O        the path and filename for the writeable result data file.
              Default is ./scrapentpmon.csv
              
  -d          include a header line in the data file describing the fields.
              Default is no header line.
              
  -q          quiet operation. Do not output any messages. This includes any
              errors or warnings. Use with care.
              
  -v          show program's version number and exit```


### Suggestion:
Put it in its own directory and run it from there.  The data file will be created there and may be accessed from there.
Once set up, one could add it to the system scheduler (like cron or AT) and have the data updated automatically.
