# peplink-nema-lan
Python 3 Script to Access NEMA data from the LAN of a Peplink MAX

# Background
In this Post: https://forum.peplink.com/t/accessing-gps-info-from-pepwave-max-routers/8262/3 
@Guido_Biosca wanted to access the GPS data from a MAX over the LAN using python to open the NEMA socket on.60660. I tried knocking out a Python 3 script to do just that and thought it would work but didn't have a Peplink MAX to hand with an active GPS so couldn't test it.

After testing I saw it didn't work as expected. I managed to grab the positioning data from the socket:

`$GPRMC,185546.0,A,5141.058053,N,00013.149088,W,50.8,94.9,180517,0.0,E,A*1B`

but assumed incorrectly that the positioning data just needed to be pulled out of that string eg:
**5141.058053N, 13.149088W**

Of course in hindsight I should have easily spotted that it wasn't valid lat longs. So what is it? 
Well its a decimal-decimal value, so it needs to be converted to degrees and minutes before its useful to us eg:

5141.058053 (ddmm.mmmmmm) = 51 41.058053 = 51 + 41.058053/60 = 51.684301 degrees

The attached script does exactly that and now it works as expected.
