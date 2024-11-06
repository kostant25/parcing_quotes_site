import json

from parser.parser import get_json

# Тип получаемых данных
ST_ACCEPT = "text/html"
# Имитируем подключенте через браузер
ST_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36"

# Заголовки для эмоляции реального пользователя
HEADERS = {"User-Agent": ST_USERAGENT, "Accept": ST_ACCEPT}

if __name__ == "__main__":
    # Запрашиваем все данные с сайта
    # На выходе получаем массив словарей
    json_data = get_json("https://quotes.toscrape.com", HEADERS)

    # Вывод общего количества записей
    print(f"Всего цитат получено: {len(json_data)}")

    # Сохраняем полученные данные в json-файл
    with open("./output/output.json", "w") as file:
        json.dump(json_data, file, indent=4)
