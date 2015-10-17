import sys
import webbrowser
import re
import time

SHOP = 'http://www.ecocion-shop.de/web/main.php/shop/addCart?live_pid='
INF = '&menge='
DELAY = 2

if __name__ == '__main__':

    with open(sys.argv[1], 'r') as file:
        # find first occurrence of 'Nummer    Menge   Name'
        order = file.read().split('Nummer    Menge   Name', 1)[1]

        # split into lines
        lines = order.split('\n')

        # for each row of the text file split the line and add an order to the shop
        for line in lines:
            data = re.split(r' +', line)
            if len(data) > 3:
                webbrowser.open(SHOP + data[1] + INF + data[2])
		time.sleep(DELAY)
