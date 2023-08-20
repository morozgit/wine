import datetime
import os
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

FOUNDING_DATE = 1920


def year_format(year):
    if (year % 10) == 1 and (year % 100)!= 11:
        return 'год'
    elif (year % 10) >= 2 and (year % 10) <= 4 and (year % 100) < 10 or (year % 100) >= 20:
        return 'года'
    else:
        return 'лет'


def find_file():
    print('Путь к папке')
    folder_path = input()
    print('Имя файла')
    file_name = input()
    with os.scandir(folder_path) as files:
        for file in files:
            if file.name == file_name:
                return file
    return None


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    now = datetime.datetime.now().year
    company_age = now - FOUNDING_DATE
    year_word = year_format(company_age)
    file_data = pandas.read_excel(find_file(), na_values='nan',
                                  keep_default_na=False
                                  )
    wine_dict = file_data.to_dict(orient='records')
    new_wine_dict = defaultdict(list)
    for beverages in wine_dict:
        new_wine_dict[beverages[next(iter(beverages))]].append(beverages)

    rendered_page = template.render(
        wine=new_wine_dict,
        company_age=company_age,
        year_word=year_word
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
