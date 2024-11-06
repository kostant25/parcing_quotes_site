import requests
from bs4 import BeautifulSoup


def get_raw_html(url: str, headers: dict[str, str], next_page="/page/1/"):
    """Получает html код нужных блоков"""
    req = requests.get(url + next_page, headers=headers)
    src = []
    quotes = BeautifulSoup(req.text, "html.parser").find_all("div", class_="quote")
    src.extend(quotes)
    next_page = BeautifulSoup(req.text, "html.parser").find("li", class_="next")
    if next_page:
        src.extend(get_raw_html(url, headers, next_page.a["href"]))
    return src


def get_json(url, headers):
    """Преобразует все блоки в массив словарей"""
    src = get_raw_html(url, headers)
    quotes = []

    for s in src:
        quotes.append(
            {
                "quote": s.find("span", class_="text").text,
                "author": s.find("small", class_="author").text,
                "about_author_link": url + s.select("span > a")[0]["href"],
                "tags": [tag.text for tag in s.find_all("a", class_="tag")],
            }
        )

    return quotes
