# FoodCoopOrderer
Two scripts for...

* importing articles from suppliers running the http://ecoinform.de/ system into the FoodSoft
* exporting FoodSoft orders to suppliers shops

## Install
* Install Python 3: https://www.python.org/downloads/
	* Check the checkbox 'Add to path'
* Install Python modules by entering in cmd.exe:
	* ```pip install beautifulsoup4```

## Run
1. Enter ```python crawl.py``` in cmd.exe
	* A ```articles.csv``` is created
	* Create all the categories in the FoodSoft
	* Create a new supplier in the FoodSoft and import the file 
2. Login on the supplier website and select a delivery date for your current shopping cart
	* In the FoodSoft, download the order summary Fax text file
	* Rename the file to ```input.txt```
	* Enter ```python order.py``` in cmd.exe
	* Many browser tabs will open, adding articles to your shopping cart
	* Compare the total costs of the supplier and the FoodSoft order