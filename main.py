import requests
import json

FILE = "vacancies.json"
URL = "https://remoteok.com/api"

def fetch_vacancies():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return []
    data = response.json()
    # Первый элемент — метаданные, пропускаем
    return data[1:]

def filter_vacancies(vacancies, keyword):
    keyword = keyword.lower()
    result = []
    for v in vacancies:
        position = v.get("position", "").lower()
        tags = " ".join(v.get("tags", [])).lower()
        if keyword in position or keyword in tags:
            result.append(v)
    return result

def save(vacancies):
    with open(FILE, "w") as f:
        json.dump(vacancies, f, indent=2)

def show_top(vacancies, n=10):
    if not vacancies:
        print("Ничего не найдено")
        return
    sorted_v = sorted(
        vacancies,
        key=lambda v: v.get("salary_min", 0) or 0,
        reverse=True
    )
    for v in sorted_v[:n]:
        company = v.get("company", "?")
        position = v.get("position", "?")
        salary = v.get("salary_min", 0) or 0
        url = v.get("url", "")
        print(f"\n{position} — {company}")
        if salary:
            print(f"  от ${salary}")
        print(f"  {url}")

def main():
    print("Скачиваю вакансии...")
    vacancies = fetch_vacancies()
    print(f"Получено: {len(vacancies)}")

    keyword = input("Ключевое слово (например python): ").strip()
    filtered = filter_vacancies(vacancies, keyword)
    print(f"Найдено по '{keyword}': {len(filtered)}")

    if filtered:
        save(filtered)
        print(f"Сохранено в {FILE}")
        show_top(filtered)

if __name__ == "__main__":
    main()