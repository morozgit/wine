import argparse
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

FOUNDING_DATE = 1920


def get_year_format(year):
    if year % 10 == 1 and year % 100 not in [11, 12, 13, 14]:
        year_format = 'год'
    elif year % 10 in [2, 3, 4]:
        year_format = 'года'
    else:
        year_format = 'лет'
    return year_format


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    now = datetime.datetime.now().year
    company_age = now - FOUNDING_DATE
    year_word = get_year_format(company_age)

    parser = argparse.ArgumentParser(
        description='Введите имя файла с расширением'
        )
    parser.add_argument('file_name', help='Имя файла')
    args = parser.parse_args()
    file_data = pandas.read_excel(args.file_name, na_values='nan',
                                  keep_default_na=False
                                  )
    wine = file_data.to_dict(orient='records')
    new_wine = defaultdict(list)
    for beverages in wine:
        beverages_category = next(iter(beverages))
        new_wine[beverages[beverages_category]].append(beverages)

    rendered_page = template.render(
        wine=new_wine,
        company_age=company_age,
        year_word=year_word
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
