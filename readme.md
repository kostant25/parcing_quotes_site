# Парсер

Данная программа собирает данные с сайта https://quotes.toscrape.com/

А теперь не много пояснения

## 1. Что сделали?

Провели анализ сайта и данных которые он возвращает.
Посмотрев код страницы в инструментах разработчика в браузере я узнал по каким классам нужно будет искать нужные блоки с данными.
Если быть более точным:
* Блок со всем искомым контентом:
   ```html
    <div class="quote"></div>
   ```
* Блок с цитатой:
   ```html
    <span class="text"></span>
   ```
* Блок с автором:
   ```html
    <span>
        <small class="author"></small>
    </span>
   ```
* Блок со ссылкой на информацию об авторе:
   ```html
    <span>
        <small class="author"></small>
        <a href="/author/name"></a>
    </span>
   ```
* Блок с тэгами:
   ```html
    <div class="tags"></div>
   ```

После анализа можно приступать к выбору библиотек.

Мой выбор пал на библиотеку `Requests` для запросов к сайту.
Посчитал что она подойдет лучше в силу простоты.
Данный сайт не требует эмуляции браузера, поэтому `простой инструмент - лучший выбор`.

В ответах приходят html-файлы и для работы с ними была выбрана библиотека `BeautifulSoup4`.
Здесь выбор был еще проще, других библиотек для таких задач я не знаю.

Так же определился с видом json-файла. Это будет массив словарей вида:

```json
[
  {
    "quote": "\u201cIt is better to be hated for what you are than to be loved for what you are not.\u201d",
        "author": "Andr\u00e9 Gide",
        "about_author_link": "https://quotes.toscrape.com/author/Andre-Gide",
        "tags": [
            "life",
            "love"
        ]
  }
]
```

## 2. Как сделали?

Я решил отделить функцию запроса к серверу и парсинг полученных данных на отдельные функции.
А также вынес их в отдельный пакет. В файле `main.py` я лишь вызываю эти функции и полученные данные записываю в файл.

Чтобы сайт отвечал на мой запрос я отправляю также заголовки:
```python
HEADERS = {"User-Agent": ST_USERAGENT, "Accept": ST_ACCEPT}
```

Далее вызываю основную функцию которая вернет мне массив словарей готовых для записи в файл.
```python
json_data = get_json("https://quotes.toscrape.com", HEADERS)
```
На вход идет домен и те самые заголовки.

Когда данные получены просто записываю их в json-файл:
```python
with open("./output/output.json", "w") as file:
    json.dump(json_data, file, indent=4)
```

Теперь переходим в функцию `get_json`:
```python
src = get_raw_html(url, headers)
quotes = []
```
Вызываем функцию которая и делает запросы к сайту вытягивая всю информацию, так же делаю первоначальную обработку
и возвращает массив с блоками цитат.

А дальше мы проходим по каждому блоку в цикле, создаем словарь и записываем его в массив `quotes`.
```python
for s in src:
    quotes.append(
        {
            "quote": s.find("span", class_="text").text,
            "author": s.find("small", class_="author").text,
            "about_author_link": url + s.select("span > a")[0]["href"],
            "tags": [tag.text for tag in s.find_all("a", class_="tag")],
        }
    )
```
В конце возвращаем `quotes` - это готовые данные.

Ну и в конце поговорим о чуть ли не главной функции - `get_raw_html`.
```python
req = requests.get(url + next_page, headers=headers)
src = []
quotes = BeautifulSoup(req.text, "html.parser").find_all("div", class_="quote")
src.extend(quotes)
```
В начале мы делаем запрос на первую чтраницу с цитатами. С помощью `BeautifulSoup` вытаскиваем все блоки с цитатами.
И сохраняем их в масиив.
```python
next_page = BeautifulSoup(req.text, "html.parser").find("li", class_="next")
if next_page:
    src.extend(get_raw_html(url, headers, next_page.a["href"]))
return src
```
В этой строчкек мы пытаемся достать кнопку со ссылкой на следующую страницу и если она есть мы вызываем эту же функцию,
то есть уходим в рекурсию, но уже на следующую страницу. Когда не сможем найти эту кнопку,
начнем возвращать все полученные блоки с цитатами и добавлять их в массив.

Все. Все данные получены и отданны сначала на преобразование в словари, а после на запись в файл.