import sys
import webbrowser
import re
import time
import crawl

SHOP_URL = 'http://www.ecocion-shop.de/web/main.php/shop/addCart?live_pid='
DELAY = 3

if __name__ == '__main__':

    fresh_item_list = ['empty row']
    crawl.crawl(fresh_item_list, fresh_item_list, crawl.FRESH_CATEGORIES_LIST)

    with open(sys.argv[1], 'r') as file:
        # find first occurrence of 'Nummer    Menge   Name'
        order = file.read().split('Nummer    Menge   Name', 1)[1]

        # split into lines
        lines = order.split('\n')

        # for each row of the text file split the line and add an order to the shop
        webbrowser.open("workaround, because the first open() does not open anything")
        for line in lines:
            splitted_line = re.split(r' +', line)  # e.g. ['', '392459', '2', 'Bioland', 'Joghurt', 'Natur', '1L']
            if len(splitted_line) > 3:
                product_id = splitted_line[1]
                count = splitted_line[2]

                if 'frisch' in file.name:
                    for item in fresh_item_list:
                        if product_id in item:
                            if crawl.GRAMM in item:
                                count = str(float(count) / 10)
                                break
                            else:  # article is ordered by piece
                                break
                    else:  # if for terminates normally (not by a break)
                        print('"' + line + '" ist ausverkauft.')
                        continue

                webbrowser.open(SHOP_URL + product_id + '&menge=' + count + '&wiegeartikel=1')
                time.sleep(DELAY)
