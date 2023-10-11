import pandas as pd
import requests
from lxml import html


def parse_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Парсинг цен на основе данных из DataFrame.

    :param df: DataFrame с данными о продуктах, включая название, URL и путь к цене.
    :type df: pd.DataFrame

    :return: Новый DataFrame с добавленными ценами.
    :rtype: pd.DataFrame
    """
    parsed_data: dict[str, list] = {'title': [], 'url': [], 'xpath': [], 'price': []}

    for index, row in df.iterrows():
        url: str = row['url']
        xpath: str = row['xpath']

        page = requests.get(url)
        tree = html.fromstring(page.content)

        price_elements = tree.xpath(xpath)
        if price_elements:
            raw_price: str = ' '.join(element.text_content() for element in price_elements).replace(',', '.')
            cleaned_price: str = ''.join(c if c.isdigit() or c == '.' else '' for c in raw_price)
            price: float | None = float(cleaned_price) if cleaned_price else None
        else:
            price = None

        parsed_data['title'].append(row['title'])
        parsed_data['url'].append(url)
        parsed_data['xpath'].append(xpath)
        parsed_data['price'].append(price)

    parsed_df = pd.DataFrame(parsed_data)
    return parsed_df
