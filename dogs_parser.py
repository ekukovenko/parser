import re
import pandas as pd
from bs4 import BeautifulSoup
from parser import Parser


class DogsParser(Parser):
    def __init__(self) -> None:
        self.url = "https://www.petshop.ru/adverts/dogs/"
        self.source = "petshop.ru"
        self.scroll = True

    def clean_text(self, text: str) -> str:
        text = text.replace(';', '').strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    def parse_price(self, price_str: str) -> int:
        price_str = re.sub(r'[^\d\-]', '', price_str)

        if '-' in price_str:
            low, high = map(int, price_str.split('-'))
            if high < 1000:
                high *= 1000
            return high
        else:
            price = int(price_str)
            if price < 1000:
                price *= 1000
            return price

    def get_product_list(self) -> None:
        content_list = super().get_page_content(url=self.url, scroll=self.scroll)

        names = []
        breeds = []
        rare_gen = []
        prices = []
        descriptions = []
        regions = []
        dates = []
        images = []

        for content in content_list:
            soup = BeautifulSoup(content, features="lxml")

            raw_list = soup.find_all('div', attrs={'class': 'articles-item ng-scope'})

            for idx, raw in enumerate(raw_list, 1):
                soup = BeautifulSoup(str(raw), features='lxml')
                name = self.clean_text(soup.find('a', attrs={'class': "ng-binding"}).get_text())
                description = self.clean_text(soup.find('div', attrs={'class': "text ng-binding"}).get_text())

                raw_price = soup.find('div', attrs={'class': 'price ng-scope'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text() if soup.find('div', attrs={'class': 'price ng-scope'}) else "N/A"
                price = self.parse_price(self.clean_text(raw_price)) if raw_price != "N/A" else "N/A"

                breed = self.clean_text(soup.find('div', attrs={'class': 'breed'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text()) if soup.find('div', attrs={'class': 'breed'}) else "N/A"
                region = self.clean_text(soup.find('div', attrs={'class': 'region'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text()) if soup.find('div', attrs={'class': 'region'}) else "N/A"
                date = self.clean_text(soup.find('div', attrs={'class': 'date'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text()) if soup.find('div', attrs={'class': 'date'}) else "N/A"
                img_div = soup.find('div', attrs={'class': 'articles-img'})
                if img_div:
                    img_tag = img_div.find('img')
                    img = img_tag['ng-src'] if img_tag and 'ng-src' in img_tag.attrs else "N/A"
                else:
                    img = "N/A"

                gen = "ген" in description.lower()

                names.append(name)
                breeds.append(breed)
                rare_gen.append(gen)
                prices.append(price)
                descriptions.append(description)
                regions.append(region)
                dates.append(date)
                images.append(img)

        data = {
            'name': names,
            'breed': breeds,
            'rare_gen': rare_gen,
            'price': prices,
            'description': descriptions,
            'region': regions,
            'date': dates,
            'image_url': images,
        }
        df = pd.DataFrame(data)

        df.to_csv('dogs_dataset.csv', index=False, encoding='utf-8-sig')

        print('Data saved to dogs_dataset.csv in structured format.')
