import re
import pandas as pd
from bs4 import BeautifulSoup
from parser import Parser

class HHParser(Parser):
    def __init__(self)->None:
        self.url = "https://spb.hh.ru/"
        self.searchbar_xpath = '//*[@id="a11y-search-input"]'
        self.block_button_xpath = '//*[@class="bloko-modal-close-button"]'
        self.source = "hh.ru"
        self.scroll = True

    def get_product_list(self, job_name: str) -> None:
        # Получаем HTML контент страницы
        content = super().get_page_content(job_name=job_name, url=self.url,
                                           searchbar_xpath=self.searchbar_xpath, block_button_xpath=self.block_button_xpath, scroll=self.scroll)
        soup = BeautifulSoup(content, features="lxml")

        names=[]

        raw_list = soup.find_all('div', attrs={'class': 'magritte-card___bhGKz_6-1-5 magritte-card-border-radius-24___o72BE_6-1-5 magritte-card-stretched___0Uc0J_6-1-5 magritte-card-action___4A43B_6-1-5 magritte-card-shadow-on-hover___BoRL3_6-1-5 magritte-card-with-border___3KsrG_6-1-5'})

        for raw in raw_list:
            soup = BeautifulSoup(str(raw), features='lxml')
            name = soup.find('a', attrs={'class': "magritte-text___tkzIl_4-3-2"}).get_text()
            names.append(name)

        df = pd.DataFrame({
            'Name': names,
        })
        df.to_csv(f'{job_name}_dataset.csv', index=False)
        print(f'Data saved to {job_name}_dataset.csv')