import json
import argparse
import math


def get_argv():
    parser = argparse.ArgumentParser(description='Информация о барах Москвы')
    parser.add_argument(
        '-f',
        '--file',
        default='bars.json',
        help='путь до файла'
    )
    parser.add_argument(
        '-l',
        '--location',
        nargs=2,
        help='долгота, широта Вашего местонахождения в десятичной форме',
        type=float
    )
    return parser.parse_args()


def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_content = file.read()
            return json.loads(json_content)['features']
    except FileNotFoundError:
        return None


def get_biggest_bar(bars):
    biggest_bar = max(
        bars,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return biggest_bar['properties']


def get_smallest_bar(bars):
    small_bars = min(
        bars,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return small_bars['properties']


def get_distance_bar(longitude, latitude, longitude_bar, latitude_bar):
    # ССылка на формулу для расчета растояния:
    # https://ru.wikipedia.org/wiki/Сфера
    earth_radius = 6372795
    cos_latitude = math.cos(math.radians(latitude))
    sin_latitude = math.sin(math.radians(latitude))
    cos_latitude_bar = math.cos(math.radians(latitude_bar))
    sin_latitude_bar = math.sin(math.radians(latitude_bar))
    distance = earth_radius * math.acos(
        sin_latitude * sin_latitude_bar + cos_latitude * cos_latitude_bar * math.cos(
            math.radians(abs(longitude - longitude_bar))
        )
    )
    return distance


def get_closest_bar(bars, longitude, latitude):
    if longitude < 180 and latitude < 90:
        closest_bar = min(
            bars,
            key=lambda x: get_distance_bar(
                longitude,
                latitude,
                x['geometry']['coordinates'][0],
                x['geometry']['coordinates'][1]
            )
        )
        return closest_bar['properties']
    else:
        return None


if __name__ == '__main__':
    argv = get_argv()
    bars = load_data(argv.file)
    if bars:
        name_smallest_bar = get_smallest_bar(bars)['Attributes']['Name']
        name_biggest_bar = get_biggest_bar(bars)['Attributes']['Name']
        print('Самый маленький бар: "{0}"'.format(name_smallest_bar))
        print('Cамый большой бар: "{0}"'.format(name_biggest_bar))
        if argv.location:
            longitude, latitude = argv.location
            name_closest_bar = get_closest_bar(bars, longitude, latitude)['Attributes']['Name']
            if name_closest_bar:
                print('Самый близкий бар: "{0}"'.format(name_closest_bar))
            else:
                print('Введены неверные координаты')
        else:
            print ('Вы не ввели координаты!')
    else:
        print('По указанному пути нет файла в формате json')
    print('Программа завершина.')
