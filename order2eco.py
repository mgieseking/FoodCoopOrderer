import sys
import webbrowser
import re
import time
import crawl

SHOP_URL = 'http://www.ecocion-shop.de/web/main.php/shop/addCart?live_pid='
DELAY = 3

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as input_file:
        fresh_item_list = ['empty row']
        crawl.crawl(fresh_item_list, fresh_item_list, crawl.FRESH_CATEGORIES_LIST)
        if 'frisch' not in input_file.name:
            dry_item_list = ['empty row']
            crawl.crawl(fresh_item_list, dry_item_list, crawl.ALL_ITEMS)

        with open(crawl.DRY_ARTICLES_CSV, 'r') as dry_file:  # for comparison to detect price changes
            old_dry_item_list = dry_file.readlines()

        # find first occurrence of 'Nummer    Menge   Name'
        order = input_file.read().split('Nummer    Menge   Name', 1)[1]

        # split into lines
        lines = order.split('\n')

        ask_to_proceed = False
        id_count_name_list = []
        for line in lines:
            splitted_line = re.split(r' +', line)  # e.g. ['', '392459', '2', 'Bioland', 'Joghurt', 'Natur', '1L']
            if len(splitted_line) > 3:
                product_id = splitted_line[1]
                count = splitted_line[2]
                name = ' '.join(splitted_line[3:])

                if 'frisch' not in input_file.name:
                    for item in old_dry_item_list:
                        if product_id in item:
                            old_price = item.split(';')[7]
                            for new_item in dry_item_list:
                                if product_id in new_item:
                                    new_price = new_item.split(';')[7]
                                    break
                            if old_price != new_price:
                                ask_to_proceed = True
                                print("Preisänderung bei '" + name + "': " + old_price + ' -> ' + new_price)
                            break

                id_count_name_list.append((product_id, count, name))
        if ask_to_proceed:
            proceed = input('There were some price changes. Proceed? Type y or n and press enter\n')
            if proceed != 'y':
                sys.exit(0)

        # for each row of the text file split the line and add an order to the shop
        webbrowser.open("workaround, because the first open() does not open anything")
        for product_id, count, name in id_count_name_list:
            if 'frisch' in input_file.name:
                for item in fresh_item_list:
                    if product_id in item:
                        if crawl.GRAMM in item:
                            count = str(float(count) / 10)
                            break
                        else:  # article is ordered by piece
                            break
                else:  # if for terminates normally (not by a break)
                    print('"' + name + '" ist ausverkauft.')
                    continue

            webbrowser.open(SHOP_URL + product_id + '&menge=' + count + '&wiegeartikel=1')
            time.sleep(DELAY)
