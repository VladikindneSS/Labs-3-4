import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')  # Установка UTF-8 для корректного вывода в консоль

def get_vacancies(keyword="C#", pages=1):
    headers = {
        "User-Agent": "Python script",
    }

    salaries = []
    total_found = 0
    total_with_salary = 0

    for page in range(pages):
        url = "https://api.hh.ru/vacancies"
        params = {
            "text": keyword,
            "per_page": 100,
            "page": page,
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        total_found += len(data["items"])  # Считаем общее число вакансий

        for item in data["items"]:
            salary = item.get("salary")
            if salary and (salary["from"] or salary["to"]):
                total_with_salary += 1
                if salary["from"] and salary["to"]:
                    avg = (salary["from"] + salary["to"]) / 2
                    salaries.append(avg)
                elif salary["from"]:
                    salaries.append(salary["from"])
                elif salary["to"]:
                    salaries.append(salary["to"])

    print(f"\nКлючевое слово: «{keyword}»")
    print(f"Найдено вакансий: {total_found}")
    print(f"С зарплатой: {total_with_salary}")

    if salaries:
        average_salary = sum(salaries) / len(salaries)
        print(f"Средняя зарплата: {average_salary:.2f} RUB")
    else:
        print("Не удалось получить зарплатные данные.")

# Запускаем функцию с ключевым словом "C#" и количеством страниц = 1
get_vacancies(keyword="Гинеколог", pages=1)
