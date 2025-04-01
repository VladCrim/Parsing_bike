from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv

# Настройка опций для Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Инициализация WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Открываем сайт
    driver.get("https://bike-place82.ru/velosipedy")
    print("Сайт успешно открыт")

    # Список для хранения данных
    all_bikes = []

    # Явное ожидание загрузки элементов с ценами
    wait = WebDriverWait(driver, 10)
    price_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@class, 'js-product-price') and contains(@class, 't-store__card__price-value')]")
        )
    )

    # Сбор названий велосипедов
    title_elements = driver.find_elements(
        By.XPATH, "//div[contains(@class, 'js-store-prod-name') and contains(@class, 't-store__card__title')]"
    )

    # Сохранение данных с первой страницы
    for i in range(len(title_elements)):
        title_text = title_elements[i].text.strip()
        price_text = price_elements[i].text.strip() if i < len(price_elements) else "Цена не указана"
        all_bikes.append({"title": title_text, "price": price_text})

    # Вывод всех собранных данных
    print("\nСписок всех велосипедов и их цен:")
    for bike in all_bikes:
        print(f"Велосипед: {bike['title']}, Цена: {bike['price']}")

    # Подсчет средней цены
    valid_prices = []
    for bike in all_bikes:
        price = bike['price'].replace('₽', '').replace(' ', '').strip()
        if price.isdigit():
            valid_prices.append(int(price))

    average_price = sum(valid_prices) / len(valid_prices) if valid_prices else 0
    print(f"\nСредняя цена: {average_price:.2f} ₽")

    # Сохранение данных в CSV-файл
    with open('bikes.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Обработка данных перед записью в CSV
        for bike in all_bikes:
            # Убираем "₽" и преобразуем цену в число
            price = bike['price'].replace('₽', '').replace(' ', '').strip()
            if price.isdigit():
                price = int(price)
            else:
                price = 0  # Если цена не число, записываем 0
            writer.writerow({'title': bike['title'], 'price': price})

    print("Данные успешно сохранены в файл 'bikes.csv'")

except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    # Закрываем браузер
    driver.quit()