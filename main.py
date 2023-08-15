from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
FOUNDING_DATE = 1920


def year_format(year):
    if (year % 10) == 1 and (year % 100)!= 11:
        return 'год'
    elif (year % 10) >= 2 and (year % 10) <= 4 and (year % 100) < 10 or (year % 100) >= 20:
        return 'года'
    else:
        return 'лет'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    now = datetime.datetime.now().year
    company_age = now - FOUNDING_DATE
    year_word = year_format(company_age)
    excel_data_df = pandas.read_excel('wine.xlsx')
    wine_json = excel_data_df.to_dict(orient='records')
    print(wine_json)
    rendered_page = template.render(
        wine=wine_json,
        company_age=company_age,
        year_word=year_word
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
