# Выпускная квалификационная работа

Данные и программы, используемы в [ВКР](../blob/main/PolinBV-thesis.pdf), для сбора и анализа данных о доходности инвестирования на арт-рынке

## Сбор данных

Программа реализована на Node.js, с помощью библиотеки puppeteer

Программа парсит сайт sothebys.com, полученные данные записывает в .json файлы

[index.js](../blob/main/index.json)

## Очистка данных

Программа реализована на Python

[Clear.py](../blob/main/Clear.py)

Программа считывает информацию из .json файла, очищает данные и записывает результат в .csv файл

## Данные и Дашборд

Итоговый датасет представлен в [Resale.csv](../blob/main/Resale.csv)

Данные были реализованы в виде [дашборда](https://datalens.yandex/y7tqzweb4djss) с помощью сервиса Yandex DataLens

## Линейная регрессия

Программа реализована на R

[LinearRegression.R](../blob/main/LinearRegression.R)

Программа считывает информацию из .xlsx файла, который содержит матрицу зависимости перменных для линейной регрессии, которая была посчитана в Microsoft Excel
