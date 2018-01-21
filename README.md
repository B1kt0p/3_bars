# Находим самый большой, маленький и ближайший бар г. Москвы

Скрипт выводит название самого большого и малого бара. Если указаны координаты Вашего текущего местоположения -  название ближайшего от Вас бара.
Список московских баров в формате JSON можно взять [здесь](https://devman.org/media/filer_public/95/74/957441dc-78df-4c99-83b2-e93dfd13c2fa/bars.json) или  с сайта [data.mos.ru](https://data.mos.ru/).
Но для этого потребуется:
1. зарегистрироваться на сайте и получить ключ API;
2. скачать файл по ссылке вида https://apidata.mos.ru/v1/features/1796?api_key={place_your_API_key_here}.

Скрипт использует 2 необязательных аргумента:

```bash
 -f [--file] - путь до файла в формате json. По умолчанию  bars.json.
 -l [--location] - координаты Вашего местоположения в десятичном формате. В формате [долгота широта].
```
# Как запустить
Скрипт требует для своей работы установленного интерпретатора Python версии 3.5


Запуск на Linux:

```bash
python3 bars.py -f bars.json -l 37.492603324522143  55.82743717406442
Самый маленький бар: "БАР СОКИ"
Cамый большой бар: "Спорт бар «Красная машина»"
Самый близкий бар: "Альтернатива 2"
Программа завершина

```

Запуск на Windows происходит аналогично.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)
