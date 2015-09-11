from bs4 import BeautifulSoup
import requests

CATEGORY_LIST = [
    ('http://www.ecocion-shop.de/Obst-frisch/Beeren%2C-Trauben_21327.html', 'Beeren und Trauben'),
    ('http://www.ecocion-shop.de/Obst-frisch/Kernobst_21328.html', 'Kernobst'),
    ('http://www.ecocion-shop.de/Obst-frisch/Steinobst_21329.html', 'Steinobst'),
]

if __name__ == '__main__':
    item_list = ['first row has to be empty']

    for url, category in CATEGORY_LIST:
        html_doc = requests.get(url).text
        soup = BeautifulSoup(html_doc, 'html.parser')
        # print(soup.prettify())
        item_divs = soup.findAll('div', class_='plWrap')  # find <div class='plWrap'>
        for item_div in item_divs:
            bestellnummer = item_div.find('input', attrs={'name': 'live_pid'})['value']  # find <input name='live_pid' type='hidden' value='579440'/>
            preis = item_div.find('input', attrs={'name': 'preis'})['value']
            pfand = item_div.find('input', attrs={'name': 'pfand'})['value']
            name = item_div.find('input', attrs={'name': 'name'})['value']
            einheit = item_div.find('span', class_='plEinheit')['title']  # find <span class='plEinheit' id='einheit_579440' title='kg'>kg</span>)
            if einheit == '':
                einheit_dropdown = item_div.find('select', class_='stk_best')
                options = einheit_dropdown.findAll('option')  # find <option id="opt_660778" value="0"> Kg</option>
                einheit = options[0].string  # get ' Kg'
                name += ' ' + options[1].string.replace('Stk ', '')
            notiz = item_div.find('a')['href']

            row = ';{bestellnummer};{name};{notiz};;;{einheit};{preis};{mehrwertsteuer};{pfand};{gebindegroesse};{staffelmenge};{staffelpreis};{category}'
            # the foodsoft wants each row / item in this form, e.g. ;;Erdnussmus fein;;;;500 g;4,99;-0,17;0;1;;;Other
            mehrwertsteuer = '-17'
            gebindegroesse = 1
            staffelmenge = ''
            staffelpreis = ''
            item = row.format_map(vars())
            # print(item)
            if not any([bestellnummer in item for item in item_list]): # prevent doubles
                item_list.append(item)

    item_list_without_bags = [item for item in item_list if 'Tüten' not in item]

    with open('articles.csv', 'w') as file:
        file.write(item + '\n')
        for item in item_list_without_bags:
            file.write(item + '\n')
