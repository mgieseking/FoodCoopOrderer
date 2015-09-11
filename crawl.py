from bs4 import BeautifulSoup
import requests

CATEGORY_LIST = [
    ('http://www.ecocion-shop.de/Obst-frisch/Beeren%2C-Trauben_21327.html', 'Beeren und Trauben'),
    ('http://www.ecocion-shop.de/Obst-frisch/Kernobst_21328.html', 'Kernobst'),
    ('http://www.ecocion-shop.de/Obst-frisch/Steinobst_21329.html', 'Steinobst'),
    ('http://www.ecocion-shop.de/Obst-frisch/Suedfruechte_21330.html', 'Südfrüchte'),
    ('http://www.ecocion-shop.de/Obst-frisch/Zitrusfruechte_21331.html', 'Zitrusfrüchte'),
    ('http://www.ecocion-shop.de/Obst-frisch/Nuesse_21468.html', 'Nüsse'),
    ('http://www.ecocion-shop.de/Gemuese-frisch/Blattgemuese-Stangengemuese_21308.html', 'Blattgemüse und Stangengemüse'),
    ('http://www.ecocion-shop.de/Fruchtgemuese_21310.html', 'Fruchtgemüse'),
    ('http://www.ecocion-shop.de/Gemuese-frisch/Kohlgemuese_21311.html', 'Kohlgemüse'),
    ('http://www.ecocion-shop.de/Gemuese-frisch/Kraeuter-%26-Spargel_21312.html', 'Kräuter & Spargel'),
    ('http://www.ecocion-shop.de/Gemuese-frisch/Lauch--und-Zwiebelgemuese_21313.html', 'Lauch- und Zwiebelgemüse'),
    ('http://www.ecocion-shop.de/Gemuese-frisch/Pilze_21314.html', 'Pilze'),
    ('http://www.ecocion-shop.de/Gemuese-frisch/Salat_21315.html', 'Salat'),
    ('http://www.ecocion-shop.de/Gemuese-frisch/Kartoffeln_21316.html', 'Kartoffeln'),
    ('http://www.ecocion-shop.de/Gemuese-frisch/Wurzel--und-Knollengemuese_21317.html', 'Wurzel- und Knollengemüse'),
]
TROCKENWARE = 'Trockenware'
ALL_ITEMS = [('http://www.ecocion-shop.de/web/main.php/shop/index/seite/21273?pper_page=10000&switchView=true', TROCKENWARE)]
BUNDLE_CATEGORY = '0 Gebinde'


def write_file(filename, item_list):
    with open(filename, 'w') as file:
        for item in item_list:
            file.write(item + '\n')


if __name__ == '__main__':
    fresh_item_list = ['first row has to be empty']
    dry_item_list = ['first row has to be empty']

    for url, category in CATEGORY_LIST + ALL_ITEMS:
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        # print(soup.prettify())
        item_divs = soup.findAll('div', class_='plWrap')  # find <div class='plWrap'>
        for item_div in item_divs:
            bestellnummer = item_div.find('input', attrs={'name': 'live_pid'})['value']  # find <input name='live_pid' type='hidden' value='579440'/>
            preis = item_div.find('input', attrs={'name': 'preis'})['value']
            pfand = item_div.find('input', attrs={'name': 'pfand'})['value']
            name = item_div.find('input', attrs={'name': 'name'})['value']
            name = name[:59]  # cut too long names
            einheit = item_div.find('span', class_='plEinheit')['title']  # find <span class='plEinheit' id='einheit_579440' title='kg'>kg</span>)
            if einheit == '':
                einheit_dropdown = item_div.find('select', class_='stk_best')
                options = einheit_dropdown.findAll('option')  # find <option id="opt_660778" value="0"> Kg</option>
                einheit = options[0].string  # get ' Kg'
                append = ' ' + options[1].string.replace('Stk ', '')
                if len(name + append) > 60:  # cut name if name is too long
                    name = name[:(59 - len(append))]
                name = name + append
            if len(einheit) == 1:
                einheit = einheit + '_'
            notiz = item_div.find('a')['href']

            # add bundles
            if ' 5kg' in name:
                kategorie = BUNDLE_CATEGORY
                gebindegroesse = 5
                preis = float(preis) / gebindegroesse
                einheit = '1kg'
            elif ' 25kg' in name:
                kategorie = BUNDLE_CATEGORY
                gebindegroesse = 10
                preis = float(preis) / gebindegroesse
                einheit = '2.5kg'
            else:
                gebindegroesse = 1
                kategorie = category

            row = ';{bestellnummer};{name};{notiz};;;{einheit};{preis};{mehrwertsteuer};{pfand};{gebindegroesse};;;{kategorie}'
            # the foodsoft wants each row / item in this form, e.g. ;;Erdnussmus fein;;;;500 g;4,99;-0,17;0;1;;;Other
            mehrwertsteuer = '-17'
            item = row.format_map(vars())
            # print(item)
            same_bestellnummer = any([bestellnummer in item for item in fresh_item_list])
            same_name = any([name in item for item in dry_item_list])
            if not same_bestellnummer and not same_name:
                if category == TROCKENWARE:
                    dry_item_list.append(item)
                else:
                    fresh_item_list.append(item)

    fresh_item_list_without_bags = [item for item in fresh_item_list if 'Tüten' not in item]

    write_file('fresh_articles.csv', fresh_item_list_without_bags)
    write_file('dry_articles.csv', dry_item_list)
