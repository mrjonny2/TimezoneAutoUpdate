import datetime
import pytz
import MySQLdb as mdb
from pytz import timezone
import time

# Connect to the database, once in a variable and once globally (to prevent some MySQL going away issues)
con = mdb.connect('Database Address', 'Database Username', 'Database Password', 'Database name');
mdb.connect('Database Address', 'Database Username', 'Database Password', 'Database name');

###	Handles reconnecting to the database
def MySQLHandler():
	print "Jumped into the handler"

	con = mdb.connect('Database Address', 'Database Username', 'Database Password', 'Database name');
	con.ping(True)
	cur = con.cursor()
	cur.execute("SELECT timezones FROM timezones")

###	Check to see if database is online
try:
	con.ping(True)
	with con:
		cur = con.cursor()
		cur.execute("SELECT timezones FROM timezones")
       	alltimezones = cur.fetchall()
except mdb.OperationalError:
	print "MySQL has gone away - reconnecting"
	print mdb.OperationalError
	MySQLHandler()
	con.ping(True)
	with con:
		cur = con.cursor()
		cur.execute("SELECT timezones FROM timezones")
       	alltimezones = cur.fetchall()



print alltimezones[0][0]

for w in alltimezones:
	print w[0]
	zonename = w[0]
	timeoffset1 = (datetime.datetime.now(pytz.timezone(w[0])).strftime('%z'))
	timezonename = (datetime.datetime.now(pytz.timezone(w[0])).strftime('%Z'))
	timeoffset = timeoffset1[0] + timeoffset1[1] + timeoffset1[2] + '.' + timeoffset1[3] + timeoffset1[4]
	offsetfloat = float(timeoffset)
	print timeoffset1


	now = datetime.datetime.now(tz=timezone(zonename))
	dst_timedelta = now.dst()
	### dst_timedelta is offset to the winter time,
	### thus timedelta(0) for winter time and timedelta(0, 3600) for DST;
	### it returns None if timezone is not set
	print "DST" if dst_timedelta else "no DST"
	dstTuple = now.timetuple().tm_isdst


	### Update MySQL table with current offsets
	try:
		con.ping(True)
		with con:
			cur = con.cursor()
			cur.execute("UPDATE timezones SET timezonename = %s, offset = %s, isDST = %s WHERE timezones = %s ", (timezonename, timeoffset, dstTuple, w[0]))
	except mdb.OperationalError:
		print "MySQL had gone away - reconnecting"
		MySQLHandler()
		con.ping(True)
		with con:
			cur = con.cursor()
			cur.execute("UPDATE timezones SET timezonename = %s, offset = %s, isDST = %s WHERE timezones = %s ", (timezonename, timeoffset, dstTuple, w[0]))




