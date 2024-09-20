import requests
import pandas as pd
from datetime import datetime, timedelta

# Функция для сохранения данных в файл CSV
def save_to_csv(data, filename="/data/dataset_v3.csv"):
    if data:  # Проверяем, есть ли данные для записи
        # Преобразуем данные в DataFrame
        df = pd.DataFrame(list(data.items()), columns=["Дата", "Курс USD"])
        # Сохраняем в CSV файл с точкой с запятой в качестве разделителя
        df.to_csv(filename, sep=';', index=False, encoding='utf-8-sig')
    else:
        print("Нет данных для сохранения.")

# Основной код программы
if __name__ == "__main__":
    # URL для получения исторических данных с курсами валют (за максимально возможный период)
    base_url = "https://www.cbr-xml-daily.ru/archive/"

    # Создаем словарь для хранения данных
    currency_data = {}

    # Перебираем данные за последние несколько дней, например, 365 дней
    for days_ago in range(365):
        date_str = (datetime.now() - timedelta(days=days_ago)).strftime('%Y/%m/%d')
        url = f"{base_url}{date_str}/daily_json.js"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'Valute' in data and 'USD' in data['Valute']:
                    usd_rate = data['Valute']['USD']['Value']
                    # Сохраняем дату и курс валюты в словарь
                    currency_data[date_str] = usd_rate
                else:
                    print(f"Данные за {date_str} отсутствуют или некорректны.")
            else:
                print(f"Не удалось получить данные за {date_str}, статус код: {response.status_code}")
        except Exception as e:
            print(f"Ошибка при получении данных за {date_str}: {e}")

    # Сохраняем данные в CSV файл
    save_to_csv(currency_data)
    print("Данные успешно сохранены в dataset_v3.csv")
