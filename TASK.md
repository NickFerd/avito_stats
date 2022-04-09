# Условия и требования

__Задача__:
Необходимо реализовать сервис, позволяющий следить за изменением количества объявлений в Авито по определённому поисковому запросу и региону.

Если совсем не получается парсить Авито, можно использовать как основу сервиса любой другой классифайд (на Ваш выбор, но лучше всё-таки Авито).

UI не нужен, достаточно сделать JSON API сервис.

Для написание сервиса можно использовать FastAPI или любой другой фреймворк.

- Метод /add Должен принимать поисковую фразу и регион, регистрировать их в системе. Возвращать id этой пары.
- Метод /stat Принимает на вход id связки поисковая фраза + регион и интервал, за который нужно вывести счётчики. Возвращает счётчики и соответствующие им временные метки (timestamp).

Частота опроса = 1 раз в час  для каждого id

Требования:
- Язык программирования: Python 3.7/3.8
- Использование Docker, сервис должен запускаться с помощью docker-compose up.
- Требований к используемым технологиям нет.
- Код должен соответствовать PEP, необходимо использование type hints, к публичным методам должна быть написана документация.

Чтобы получить число объявлений, можно:
- парсить web-страницу объявления (xpath, css-селекторы)
- самостоятельно проанализировать трафик на мобильных приложениях или мобильном сайте и выяснить какой там API для получения информации об объявлении (это будет круто!)

Усложнения:
- Написаны тесты (постарайтесь достичь покрытия в 70% и больше). Вы можете использовать pytest или любую другую библиотеку для тестирования.
- Сервис асинхронно обрабатывает запросы.
- Данные сервиса хранятся во внешнем хранилище, запуск которого также описан в docker-compose. Мы рекомендуем использовать MongoDB или - Postgres, но Вы можете использовать любую подходящую базу.
- По каждому id также собираются топ 5 объявлений. На их получение есть отдельная ручка, архитектуру продумайте самостоятельно



Решение (наброски): 
Запрос к API Авито, который возвращает количество объявлений по категории и локации:
https://www.avito.ru/web/1/js/items?locationId=662210&name=велосипеды&geoCoords=55.755814,37.617635&cd=0&s=101&p=1&countOnly=1


сайт с id регионов и категорий Авито:
https://rest-app.net/api/region - конкретный метод в апи этого сайта для получения всех регионов
https://rest-app.net/api#region