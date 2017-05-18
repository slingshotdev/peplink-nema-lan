#peplink-gps.py
import socket, math, time

# PEPLINK GPS LOCATION OVER SOCKET EXAMPLE
# By MARTIN LANGMAID 
# 18th May 2017
#Change the IP below to the LAN IP of Your GPS enabled device
theIP = "192.168.50.1"
thePort = 60660

#Function decimalToDM (Decimal to Degrees & Mins)
#Convert the decimal-decimal degree value in the NEMA message to degrees and minutes
#eg 5141.058053 (ddmm.mmmmmm) = 51 41.058053 = 51 + 41.058053/60 = 51.684301 degrees
def decimalToDM( nemaIn ):
   #move decimal point for manipulation
   theDegrees= nemaIn / 100
   
   #create tuple of degrees and mins
   degsAndMins = math.modf(theDegrees)
   
   #Grab the Degrees as an integer
   theDegrees = int(degsAndMins[1]) 
   
   #restore original decimal point location
   theMins = degsAndMins[0] *100
   
   #grab the mins
   theMins=round(theMins,6)
   
   #convert decimal minutes to mins
   convertedMins=theMins/60
   
   #Add the degrees and mins together
   convertedResult=str(round(theDegrees + convertedMins,6))
   
   return convertedResult; 

#Set up a client socket to connect to the GPS enabled device
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(5)
#Connect to the device on the right Ip & port
try:
	client_socket.connect((theIP, thePort))
except socket.timeout:
	print("Can't connect to "+theIP+" on port "+str(thePort)+" : Timeout")
	quit()

while True:
	#Whilst we've received a response from the socket...
	data = client_socket.recv(1024)
	# make sure we actually have some data (and not just a response).
	if len(data) > 0:
		#decode the data from byte to string to make working with it easier
		thedata=data.decode('ascii')
		# split the data into a list of lines
		lines = thedata.splitlines(1)
		# iterate over each line
		for line in lines:
			#Data sent is coimma delimited so lets split it
			gpsstring = line.split(',')
			#if the first column contains $GPRMC and
			#if it has enough elements we have hit paydirt
			if gpsstring[0] == '$GPRMC' and len(gpsstring)>6:
				#check that there is returned GPS data
				if gpsstring[3]:
					#Get Lat and Long String by converting decimals and adding compass pos
					theLat = decimalToDM(float(gpsstring[3])) + (gpsstring[4])
					theLong = decimalToDM(float(gpsstring[5])) + (gpsstring[6])
					print ("Lat: " + theLat)
					print ("Long: " + theLong)
					#Wait 5 secs 
					time.sleep(5)
				
else:
	print("Can't connect to device...")
