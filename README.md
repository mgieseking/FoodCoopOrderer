# FoodCoopOrderer
## Install
* Install Python 3: https://www.python.org/downloads/
	* Check the checkbox 'Add to path'
* Open up a command prompt:
	* Windows: Search for 'cmd.exe'
	* Linux, Mac: Search for 'Terminal'
* Install Python modules by entering in the command prompt:
	* ```pip install beautifulsoup4 requests```

## Use
#### Importing articles from suppliers running the http://ecoinform.de/ system into the FoodSoft
* Enter ```python ``` in the command prompt, drag'n'drop ```crawl.py``` and press enter
* The files ```fresh_articles.csv``` and ```dry_articles.csv``` are created
* Create all the categories in the FoodSoft
* Create a new supplier in the FoodSoft and import the file 

#### Exporting FoodSoft orders to suppliers shops
* Login on the supplier website and select a delivery date for your current shopping cart
* In the FoodSoft, download the order summary Fax text file
* Enter ```python ``` in the command prompt, drag'n'drop ```order2eco.py```, drag'n'drop your text file and press enter
* Many browser tabs will open, adding articles to your shopping cart
* Compare the total costs of the supplier and the FoodSoft order