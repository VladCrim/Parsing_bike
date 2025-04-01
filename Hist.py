import csv
import matplotlib.pyplot as plt

# Чтение данных из CSV-файла
prices = []
with open('bikes.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        price = row['price']
        if price != '0':  # Исключаем нулевые цены (где цена не указана)
            prices.append(int(price))

# Построение гистограммы
plt.figure(figsize=(10, 6))  # Устанавливаем размер графика
plt.hist(prices, bins=10, color='skyblue', edgecolor='black')  # bins - количество столбцов

# Настройка графика
plt.title('Распределение цен на велосипеды', fontsize=14)
plt.xlabel('Цена (руб.)', fontsize=12)
plt.ylabel('Количество велосипедов', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Отображение графика
plt.show()