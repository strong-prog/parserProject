from unicodedata import category

import requests
from bs4 import BeautifulSoup
import json
import math

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0', 'Accept': '*/*'}
HOST = 'https://health-diet.ru'

urls = [
    'https://health-diet.ru/base_of_food/food_24507/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24523/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24509/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24502/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24513/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24526/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24515/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24525/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24522/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24519/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24508/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24512/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24517/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24506/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24501/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24527/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24518/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24503/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24528/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24511/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24504/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24514/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24529/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24516/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24524/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_food/food_24520/?utm_source=leftMenu&utm_medium=base_of_food',
    'https://health-diet.ru/base_of_meals/meals_21252/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21243/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21249/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21244/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21245/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21254/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21250/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21247/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21248/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21242/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21253/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21241/?utm_source=leftMenu&utm_medium=base_of_meals',
    'https://health-diet.ru/base_of_meals/meals_21251/?utm_source=leftMenu&utm_medium=base_of_meals',
]
for u in urls:
    URL = u

    def get_html(URL, params=None):
        result = requests.get(URL, headers=HEADERS, params=params)
        return result

    def write_json(mass, category):
        print(category)
        with open(f'{category}.json', 'w') as f:
            jsonData = json.dumps(mass)
            f.write(jsonData)
            #print(jsonData)

    def get_content(html):
        soup = BeautifulSoup(html, 'lxml')
        items = soup.find('tbody').find_all('tr')
        cat = soup.find('h1')
        category = cat.text.split('.')[0]
        mass = []
        for tr in items:
            tds = tr.find_all('td')
            product = tds[0].text.replace('\n', '')
            calorie = math.ceil(float(tds[1].text.split(' ')[0].replace(',', '.')))
            protein = math.ceil(float(tds[2].text.split(' ')[0].replace(',', '.')))
            fat = math.ceil(float(tds[3].text.split(' ')[0].replace(',', '.')))
            carbohydrate = math.ceil(float(tds[4].text.split(' ')[0].replace(',', '.')))
            pk = int(tr.find('a').get('href').split('/')[-1].split('.')[0])

            data = {
                'product': product,
                'calorie': calorie,
                'protein': protein,
                'fat': fat,
                'carbohydrate': carbohydrate,
                'category': category,
                'pk': pk
            }
            mass.append(data)

        write_json(mass, category)

    def parse():
        html = get_html(URL)
        if html.status_code == 200:
            get_content(html.text)
        else:
            print('Error')

    parse()
