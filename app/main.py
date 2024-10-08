import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from http import HTTPStatus

# Константы
DATA_DIR = "/data"
FILENAME = "dataset_v3.csv"
CSV_PATH = os.path.join(DATA_DIR, FILENAME)
CSV_SEP = ';'
CSV_ENCODING = 'utf-8-sig'
DAYS_IN_YEAR = 365  # Количество дней для парсинга
BASE_URL = "https://www.cbr-xml-daily.ru/archive/"
CURRENCY_CODE = 'USD'  # Код валюты

# Словарь основных кодов состояния HTTP
HTTP_STATUS_MESSAGES = {
    HTTPStatus.OK: "Успешно",
    HTTPStatus.BAD_REQUEST: "Неверный запрос",
    HTTPStatus.UNAUTHORIZED: "Не авторизован",
    HTTPStatus.FORBIDDEN: "Запрещено",
    HTTPStatus.NOT_FOUND: "Не найдено",
    HTTPStatus.INTERNAL_SERVER_ERROR: "Внутренняя ошибка сервера",
}


def save_to_csv(data, filename=CSV_PATH):
    """
    Сохраняет данные в файл CSV.

    :param data: словарь с данными для сохранения (дата: курс USD)
    :param filename: путь к файлу, в который сохраняются данные
    """
    if data:
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Преобразуем данные в DataFrame
        df = pd.DataFrame(list(data.items()), columns=["Дата", "Курс USD"])

        # Сохраняем данные в CSV файл
        df.to_csv(filename, sep=CSV_SEP, index=False, encoding=CSV_ENCODING)
    else:
        print("Нет данных для сохранения.")


# Основной код программы
if __name__ == "__main__":
    # Словарь для хранения данных о валюте
    currency_data = {}

    # Перебираем данные за последние несколько дней (например, 365 дней)
    for days_ago in range(DAYS_IN_YEAR):
        date_str = (datetime.now() - timedelta(days=days_ago)).strftime('%Y/%m/%d')
        url = f"{BASE_URL}{date_str}/daily_json.js"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Поднимает исключение при ошибках HTTP

            data = response.json()
            if 'Valute' not in data or CURRENCY_CODE not in data['Valute']:
                print(f"Данные за {date_str} отсутствуют или некорректны.")
                continue

            usd_rate = data['Valute'][CURRENCY_CODE]['Value']
            # Сохраняем дату и курс валюты в словарь
            currency_data[date_str] = usd_rate

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP ошибка: {http_err} ({date_str})")
        except requests.exceptions.RequestException as req_err:
            print(f"Ошибка запроса: {req_err} ({date_str})")
        except Exception as e:
            print(f"Ошибка: {e} ({date_str})")

    # Сохраняем данные в CSV файл
    save_to_csv(currency_data)
    print(f"Данные успешно сохранены в {FILENAME}")

