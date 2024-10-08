import re
import pandas as pd
from bs4 import BeautifulSoup
from parser import Parser

class HHParser(Parser):
    def __init__(self) -> None:
        self.url = "https://www.petshop.ru/adverts/dogs/"
        self.source = "petshop.ru"
        self.scroll = True

    def clean_text(self, text: str) -> str:
        text = text.replace(';', '').strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    def get_product_list(self) -> None:
        content_list = super().get_page_content(url=self.url, scroll=self.scroll)

        names = []
        descriptions = []
        prices = []
        breeds = []
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
                price = self.clean_text(soup.find('div', attrs={'class': 'price ng-scope'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text()) if soup.find('div',
                                                                     attrs={'class': 'price ng-scope'}) else "N/A"
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

                names.append(name)
                descriptions.append(description)
                prices.append(price)
                breeds.append(breed)
                regions.append(region)
                dates.append(date)
                images.append(img)

        data = {
            'name': names,
            'description': descriptions,
            'price': prices,
            'breed': breeds,
            'region': regions,
            'date': dates,
            'image_url': images
        }
        df = pd.DataFrame(data)

        df.to_csv('dogs_dataset.csv', index=False, encoding='utf-8-sig')

        print('Data saved to dogs_dataset.csv in structured format.')
