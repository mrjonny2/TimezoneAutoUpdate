TimezoneAutoUpdate
==================

System to automatically adjust the offset for different timezones

Requirements:
=================
MySQL Server
Python
MySQL-Python
pytz

How To:
==================
1)	Import the table into a MySQL database
2)	add all your details into the relevant sections in the python code
3)	Run the python application to update the offsets and timezones

Notes:
==================
The code could be run on a cronjob
pytz should also be updated using a cronjob
Make sure the server is set to UTC local time