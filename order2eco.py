import sys
import webbrowser
import re

# const
## url
pref = "http://www.ecocion-shop.de/web/main.php/shop/addCart?live_pid="
inf = "&menge="

# load order list
f = open(sys.argv[1], 'r')
file = f.read();

# find first occurrence of 'Nummer    Menge   Name'
order = file.split('Nummer    Menge   Name',1)[1]

# split into lines
lines = order.split('\n')

# for each row of the text file split the line and add an
# order to the shop
for line in lines:
	data = re.split(r' +', line)
	if len(data)>3:
		webbrowser.open(pref+data[1]+inf+data[2])

# close file again
f.close()
