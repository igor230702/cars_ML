import time
import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
import pandas as pd
import numpy as np
import random
import os


def return_numbers(feature, delete_dot=False):
    """
    :param feature: column in our data
    :param delete_dot: delete dot from a number or not
    :return: number from string
    """
    feature[feature.isna()] = '0' # Заменяю NaN'ы нулями, чтобы обработать их как строки
    new_feature = np.array([])
    for i in range(feature.shape[0]):
        new_value = ''

        for s in feature.iloc[i]:
            if s in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']:
                new_value += s

        if delete_dot:
            new_value = new_value.replace('.', '')

        if len(new_value):
            new_value = float(new_value)
        else:
            new_value = np.NaN

        new_feature = np.append(new_feature, new_value)

    return pd.Series(new_feature).replace(0, np.NaN)


def main():

    headers = {
        'user_agent': 'Mozilla/5.0'
    }
    cols = ['Двигатель', 'Мощность', 'Коробка передач', 'Привод', 'Тип кузова', 'Цвет',
            'Пробег, км', 'Руль', 'Поколение', 'Комплектация', 'Цена']
    data = pd.DataFrame(columns=cols)  # это наш будущий датасет

    for i in range(100):

        print(f"Iteration: {i+1}")

        folder_path = fr"C:\Users\Игорь\PycharmProjects\TestProject\parsing\cars_parsing\data\data_{i + 1}"
        if os.path.exists(folder_path):
            print("Folder already exists")
        else:
            os.mkdir(folder_path)

        url = f"https://auto.drom.ru/all/page{i+1}/"
        req = requests.get(url)
        with open(rf"{folder_path}/cars_{i+1}.html", 'w', encoding='utf-8') as file:
            file.write(req.text)
        print(req.status_code)

        with open(rf"{folder_path}/cars_{i+1}.html", encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        cars = soup.find('div', class_='css-1nvf6xk eaczv700').find('div').find_all('a')

        # собираем ссылки
        car_urls = []
        for car in cars:
            car_url = car.get('href')
            car_urls.append(car_url)

        # с каждой ссылки собираем данные
        for j, car_url in enumerate(car_urls):
            file_name = f"{j+1}_{car_url.split('/')[3]}"

            req = requests.get(car_url, headers)
            with open(rf"{folder_path}\{file_name}.html", 'w', encoding='utf-8') as file:
                file.write(req.text)
            print(f"№{j + 1}: {req.status_code}")

            with open(rf"{folder_path}\{file_name}.html",
                      encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            try:
                feature_names = soup.find('table', class_='css-xalqz7 eppj3wm0').find_all('th', class_='css-16lvhul ezjvm5n1')
                car_data = soup.find('table', class_='css-xalqz7 eppj3wm0').find_all('td', class_='css-9xodgi ezjvm5n0')
                price = soup.find('div', class_='css-eazmxc e162wx9x0').text

                names = []
                values = []
                for name in feature_names:
                    names.append(normalize('NFKD', name.text))
                for value in car_data:
                    values.append(normalize('NFKD', value.text))
                names.append('Цена')
                values.append(price)
                data = data.append(dict(zip(names, values)), ignore_index=True)

            except Exception:
                print('Не получилось')

        time.sleep(random.randrange(2, 4))
        if i % 10 == 0:
            time.sleep(random.randrange(20, 30))

    # Обработаем данные, чтобы с нимми можно было работать: переименуем столбцы и вычленим численные значения:

    data = data.rename(columns={'Двигатель': 'engine',
                                'Мощность': 'power',
                                'Коробка передач': 'transmission',
                                'Привод': 'drive_unit',
                                'Тип кузова': 'body_type',
                                'Цвет': 'color',
                                'Пробег, км': 'mileage',
                                'Руль': 'steering_wheel',
                                'Поколение': 'gen',
                                'Комплектация': 'equipment',
                                'Цена': 'price'})

    data.engine = return_numbers(data.engine)
    data.power = return_numbers(data.power, delete_dot=True)
    data.price = return_numbers(data.price)
    data.mileage = return_numbers(data.mileage)
    data.gen = return_numbers(data.gen)
    data = data.iloc[:, :11]

    data.to_csv(r'C:\Users\Игорь\PycharmProjects\TestProject\parsing\cars_parsing\car_data.csv', sep=';', index=False)

if __name__ == '__main__':
    main()
