import json
import argparse
import math


# Парсим параметры командной строки
def get_argv():
    parser = argparse.ArgumentParser(description='Информация о барах Москвы')
    parser.add_argument('-f', '--file', default='bars.json',
                        help="путь до файла")
    parser.add_argument('-l', '--location', nargs=2,
                        help="долгота, широта Вашего"
                             " местонахождения в десятичной форме", type=float)
    return parser.parse_args().file, parser.parse_args().location


def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json_content = f.read()
            return json.loads(json_content)['features']
    except (FileNotFoundError, AttributeError):
        return None


def get_biggest_bar(json_content):
    try:
        biggest_bar = max(
            json_content,
            key=lambda x:
            x['properties']['Attributes']['SeatsCount']
        )
        return biggest_bar['properties']['Attributes']['Name']
    # Сработает если JSON имеет отличные от указанных в коде ключи
    except IndexError:
        return None


def get_smallest_bar(json_content):
    try:
        small_bars = min(json_content,
                         key=lambda x:
                         x['properties']['Attributes']['SeatsCount'])
        return small_bars['properties']['Attributes']['Name']
    # Сработает если JSON имеет отличные от указанных в коде ключи
    except IndexError:
        return None


# ССылка на формулу для расчета растояния:
# https://ru.wikipedia.org/wiki/Сфера
def get_distance_bar(longitude, latitude, longitude_bar, latitude_bar):
    # Широта должна быть от 0 до 90;
    # Долгота должна быть от 0 до 180.
    if longitude < 180 and latitude < 90:
        earth_radius = 6372795
        cos_latitude = math.cos(math.radians(latitude))
        sin_latitude = math.sin(math.radians(latitude))
        cos_latitude_bar = math.cos(math.radians(latitude_bar))
        sin_latitude_bar = math.sin(math.radians(latitude_bar))
        distance = earth_radius * math.acos(
            sin_latitude * sin_latitude_bar + cos_latitude * cos_latitude_bar * math.cos(
                math.radians(abs(longitude - longitude_bar))))
        return distance
    else:
        return None


def get_closest_bar(json_content, longitude, latitude):
    try:
        closest_bar = min(
            json_content, key=lambda x: get_distance_bar(
                longitude, latitude, float(x['geometry']['coordinates'][0]),
                float(x['geometry']['coordinates'][1])
            ))
        return closest_bar['properties']['Attributes']['Name']
    # Сработает если ключи не совпадут или координаты не цифра
    except (IndexError, ValueError):
        return None


if __name__ == '__main__':
    file_path, location = get_argv()
    json_content = load_data(file_path)
    if json_content:
        smallest_bar = get_smallest_bar(json_content)
        biggest_bar = get_biggest_bar(json_content)
        if smallest_bar and biggest_bar:
            print('Самый маленький бар: "{0}"'.format(smallest_bar))
            print('Cамый большой бар: "{0}"'.format(biggest_bar))
        else:
            print('Не могу прочитать. Неправильный формат данных')
    else:
        print('По указанному пути нет файла в формате json')
    if location:
        longitude, latitude = location
        closest_bar = get_closest_bar(json_content, longitude, latitude)
        if closest_bar:
            print('Самый близкий бар: "{0}"'.format(closest_bar))
        else:
            print('ВВедены неверные координаты')
    else:
        print ('Вы не ввели координаты!')
    print('Программа завершина.')
