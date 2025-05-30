import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import time
import sys
import os

# Настройка кодировки для корректного вывода кириллицы
if os.name == 'nt':  # Windows
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleOutputCP(65001)  # Установка UTF-8 для вывода
    kernel32.SetConsoleCP(65001)  # Установка UTF-8 для ввода
else:
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Явная установка кодировки для stdout
sys.stdout.reconfigure(encoding='utf-8')

# Конфигурация
WIKIPEDIA_HISTORY_URL = "https://en.wikipedia.org/w/index.php?title=JSON&action=history"

def get_country_by_ip(ip):
    """Получение страны по IP-адресу через ipwhois.io"""
    url = f"http://ipwho.is/{ip}?fields=country"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        country = data.get("country", None)
        country_translations = {
            "United States": "США",
            "Germany": "Германия",
            "United Kingdom": "Великобритания",
            "Canada": "Канада",
            "France": "Франция",
            "Myanmar [Burma]": "Мьянма",
            "Thailand": "Таиланд",
            "Russia": "Россия",
            "Unknown": "Неизвестно"
        }
        return country_translations.get(country, country) if country else "Неизвестно"
    except requests.RequestException as e:
        print(f"Ошибка при запросе для IP {ip}: {e}")
        return "Неизвестно"

def main():
    # Получение HTML страницы истории правок
    try:
        response = requests.get(WIKIPEDIA_HISTORY_URL, timeout=10)
        response.raise_for_status()
        html_content = response.text
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы Википедии: {e}")
        return

    # Парсинг HTML для извлечения IP-адресов
    soup = BeautifulSoup(html_content, "html.parser")
    ip_elements = soup.find_all("a", class_="mw-anonuserlink")

    if not ip_elements:
        print("IP-адреса не найдены в истории правок.")
        return

    # Регулярное выражение для проверки валидности IPv4
    ip_regex = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    ip_addresses = set()

    for element in ip_elements:
        ip = element.text.strip()
        if ip_regex.match(ip):
            ip_addresses.add(ip)

    print(f"Найдено {len(ip_addresses)} уникальных IP-адресов.")

    # Подсчет стран
    country_counts = Counter()
    for ip in ip_addresses:
        country = get_country_by_ip(ip)
        country_counts[country] += 1
        # Задержка для соблюдения лимитов ipwhois.io (1 запрос/секунда)
        time.sleep(1)

    # Вывод рейтинга стран
    print("\nРейтинг стран по количеству редакторов:")
    for i, (country, count) in enumerate(country_counts.most_common(), 1):
        print(f"{i}. {country}: {count} редакторов")

if __name__ == "__main__":
    main()