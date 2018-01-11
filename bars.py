import json
import sys
import argparse
import math
import pprint


# Парсим параметры командной строки
def parser_argv():
    parser = argparse.ArgumentParser(description='Информация о барах Москвы')
    parser.add_argument("-f","--file", default=["bars.json"], nargs=1, help="путь до файла")
    parser.add_argument("-l", "--location", nargs=2,\
                        help="долгота, широта Вашего местонахождения в десятичной форме", type=float)
    return parser.parse_args()


def load_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data=f.read()
            return json.loads(data)
    except FileNotFoundError:
        return None
    except AttributeError:
        return None


def get_biggest_bar(json_content):
    try:
        sort_bars = sorted(json_content['features'], key=lambda x: x['properties']['Attributes']['SeatsCount'])
        small_bars = []
        x = 0
        for bars in sort_bars[:10]:
            bar_zip = zip(bars['properties']['Attributes'].keys(), bars['properties']['Attributes'].values())
            small_bars.append(dict(bar_zip))
        return small_bars
    except IndexError:
        return None




def get_smallest_bar(json_content):
    try:
        sort_bars = sorted(json_content['features'],\
                           key=lambda x: x['properties']['Attributes']['SeatsCount'], reverse=True)
        small_bars = []
        x = 0
        for bars in sort_bars[:10]:
            bar_zip = zip(bars['properties']['Attributes'].keys(), bars['properties']['Attributes'].values())
            small_bars.append(dict(bar_zip))
        return small_bars
    except IndexError:
        return None


# Определение ближайшего бара.Формула для расчета:
# l=earth_radius * arcos(sin (latitude1)*sin (latitude2)+cos(latitude1)*cos(latitude2)*cos(longitude1-longitude2)
def get_closest_bar(json_content, longitude, latitude):
    try:
        if longitude < 180 and latitude < 90:
            earth_radius = 6372795
            cos_latitude = math.cos(math.radians(latitude))
            sin_latitude = math.sin(math.radians(latitude))
            coordinates = [x['geometry']['coordinates'] for x in json_content['features']]
            distance_bars = []
            # В цикле находим растояние до баров
            for coordinate_bar in coordinates:
                radians_coordinate_bar = [math.radians(x) for x in coordinate_bar]
                sin_latitude_bar = math.sin(radians_coordinate_bar[1])
                cos_latitude_bar = math.cos(radians_coordinate_bar[1])

                distance = earth_radius * math.acos(sin_latitude * sin_latitude_bar + \
                                                    cos_latitude * cos_latitude_bar * \
                                                    math.cos(math.radians(math.fabs(longitude - coordinate_bar[0]))))
                distance_bars.append(distance)
            min_distance_bar = min(distance_bars)
            index_min_distance_bar = distance_bars.index(min_distance_bar)
            return json_content['features'][index_min_distance_bar]["properties"]['Attributes'], min_distance_bar
        else:
            return None
    except IndexError:
        return None


if __name__ == '__main__':
    file_path = parser_argv().file[0]
    json_content = load_data(file_path)
    if json_content:
        smallest_bar = get_smallest_bar(json_content)
        biggest_bar = get_biggest_bar(json_content)
        if smallest_bar and biggest_bar:
            print("\n 10 самых маленьких баров:")
            pprint.pprint(smallest_bar)
            print("\n10 самых больших баров:")
            pprint.pprint(biggest_bar)
        else:
            print("Не могу прочитать. Неправильный формат данных")
    else:
        print("По указанному пути нет файла в формате json")
    if parser_argv().location:
        longitude, latitude = parser_argv().location
        closest_bar = get_closest_bar(json_content, longitude, latitude)
        if closest_bar:
            print("\nСамый близкий бар:")
            pprint.pprint(closest_bar[0])
            print("\n Расстояние до бара {} метров \n".format(int(closest_bar[1])))
        else:
            print("ВВедены неверные координаты")
    else:
        print ("Вы не ввели координаты!")
    print("Программа завершина.")













