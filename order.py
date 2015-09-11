import webbrowser
import re

with open('input.txt', 'r') as file:
    for row in file:
        	new_row = re.sub(r' ', '', row)

webbrowser.open(url)