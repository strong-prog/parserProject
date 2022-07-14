import requests
from bs4 import BeautifulSoup
import json
import math

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0', 'Accept': '*/*'}

for num in range(1, 11297):
    if num == 1:
        URL = 'https://www.tablicakalorijnosti.ru/tablitsa-produktov'
    else:
        URL = f'https://www.tablicakalorijnosti.ru/tablitsa-produktov?page={num}'
    print(f'Парсинг {num} страницы')

    def get_html(URL, params=None):
        result = requests.get(URL, headers=HEADERS, params=params)
        return result

    def write_json(mass):
        with open('prod_data_base.json', 'a') as f:
            jsonData = json.dumps(mass)
            f.write(jsonData)

    def get_content(html):
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find('tbody').find_all('tr')
        mass = []

        for tr in items:
            trs = tr.find_all('td')
            product = trs[0].text.strip(' ').lower()
            try:
                calorie = trs[1].text.strip(' ').replace(',', '.')
                if calorie == '':
                    calorie = 0
                else:
                    calorie = math.ceil(float(calorie))
            except:
                continue

            try:
                protein = trs[2].text.strip(' ').replace(',', '.')
                if protein == '':
                    protein = 0
                else:
                    protein = math.ceil(float(protein))
            except:
                continue

            try:
                carbohydrate = trs[3].text.strip(' ').replace(',', '.')
                if carbohydrate == '':
                    carbohydrate = 0
                else:
                    carbohydrate = math.ceil(float(carbohydrate))
            except:
                continue

            try:
                fat = trs[4].text.strip(' ').replace(',', '.')
                if fat == '':
                    fat = 0
                else:
                    fat = math.ceil(float(fat))
            except:
                continue

            try:
                fiber = trs[5].text.strip(' ').replace(',', '.')
                if fiber == '':
                    fiber = 0
                else:
                    fiber = math.ceil(float(fiber))
            except:
                continue

            print(product, calorie, protein, carbohydrate, fat, fiber)

            data = {
                'product': product,
                'calorie': calorie,
                'protein': protein,
                'fat': fat,
                'carbohydrate': carbohydrate,
                'fiber': fiber
            }
            mass.append(data)

        write_json(mass)

    def parse():
        html = get_html(URL)
        if html.status_code == 200:
            get_content(html.text)
        else:
            print('Error')

    parse()