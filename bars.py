import json
import argparse
import math


def get_argv():
    parser = argparse.ArgumentParser(description='Информация о барах Москвы')
    parser.add_argument(
        '-f',
        '--file',
        default='bars.json',
        help="путь до файла"
    )
    parser.add_argument(
        '-l',
        '--location',
        nargs=2,
        help="долгота, широта Вашего местонахождения в десятичной форме",
        type=float
    )
    return parser.parse_args()


def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_content = file.read()
            return json.loads(json_content)['features']
    except (FileNotFoundError, AttributeError):
        return None


def get_biggest_bar(bars):
    biggest_bar = max(
        bars,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return biggest_bar['properties']['Attributes']['Name']


def get_smallest_bar(bars):
    small_bars = min(
        bars,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return small_bars['properties']['Attributes']['Name']


def get_distance_bar(longitude, latitude, longitude_bar, latitude_bar):
    earth_radius = 6372795
    cos_latitude = math.cos(math.radians(latitude))
    sin_latitude = math.sin(math.radians(latitude))
    cos_latitude_bar = math.cos(math.radians(latitude_bar))
    sin_latitude_bar = math.sin(math.radians(latitude_bar))
    # ССылка на формулу для расчета растояния:
    # https://ru.wikipedia.org/wiki/Сфера
    distance = earth_radius * math.acos(
        sin_latitude * sin_latitude_bar + cos_latitude * cos_latitude_bar * math.cos(
            math.radians(abs(longitude - longitude_bar))
        )
    )
    return distance


def get_closest_bar(bars, longitude, latitude):
    # Широта должна быть от 0 до 90
    # Долгота должна быть от 0 до 180
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
        return closest_bar['properties']['Attributes']['Name']
    else:
        return None


if __name__ == '__main__':
    parse = get_argv()
    bars = load_data(parse.file)
    if bars:
        smallest_bar = get_smallest_bar(bars)
        biggest_bar = get_biggest_bar(bars)
        print('Самый маленький бар: "{0}"'.format(smallest_bar))
        print('Cамый большой бар: "{0}"'.format(biggest_bar))
        if parse.location:
            longitude, latitude = parse.location
            closest_bar = get_closest_bar(bars, longitude, latitude)
            if closest_bar:
                print('Самый близкий бар: "{0}"'.format(closest_bar))
            else:
                print('Введены неверные координаты')
        else:
            print ('Вы не ввели координаты!')
    else:
        print('По указанному пути нет файла в формате json')
    print('Программа завершина.')
