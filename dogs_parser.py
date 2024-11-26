import re
from random import choice
from typing import Union
import pandas as pd
from bs4 import BeautifulSoup
from parser import Parser

KNOWN_BREEDS = [
    "Австралийская овчарка", "Австралийский келпи", "Австралийский терьер", "Акбаш",
    "Акита (Ину)", "Аляскинский маламут", "Американский бульдог", "Американский водяной спаниель",
    "Американский питбультерьер", "Американский стаффордширский терьер", "Английский бульдог",
    "Английский кокер спаниель", "Английский сеттер", "Английский спрингер спаниель", "Афганская борзая",
    "Басенджи", "Бассет (хаунд)", "Бедлингтон терьер", "Бельгийская овчарка", "Бернский зенненхунд",
    "Бигль", "Бишон Фризе", "Бладхаунд", "Боксер", "Бостон терьер", "Брюссельский гриффон",
    "Бульмастифф", "Бультерьер", "Веймаранер (веймарская легавая)", "Вельш корги кардиган (корги кардиган)",
    "Вельш корги пемброк (корги пемброк)", "Вельштерьер", "Венгерская короткошерстая легавая (выжлы)",
    "Вест хайленд уайт терьер (вест хайленд вайт терьер)", "Гаванский бишон (гаванская болонка)",
    "Далматин", "Джек рассел терьер", "Доберман пинчер", "Золотистый ретривер", "Ивицкая борзая (ивисская собака)",
    "Ирландский водяной (водный) спаниель", "Йоркшир терьер", "Кавалер кинг чарльз спаниель", "Кеесхонд",
    "Керри блю терьер", "Китайская хохлатая собака", "Коикерхондье", "Кокер спаниель", "Колли",
    "Лабрадор ретривер", "Левретка (итальянская левретка)", "Лейкленд терьер", "Леопардовая собака Катахулы (катахула)",
    "Лхасский апсо", "Малый пудель", "Мальтийская болонка", "Манчестерский терьер", "Маремма", "Мастиф",
    "Миниатюрная австралийская овчарка", "Миниатюрный бультерьер", "Миниатюрный пинчер", "Миниатюрный шнауцер",
    "Мопс", "Немецкая короткошерстная легавая (Курцхаар)", "Немецкая овчарка", "Папильон (папийон)",
    "Пиренейская горная собака", "Померанский шпиц", "Ризеншнауцер (гигантский шнауцер)", "Родезийский риджбек",
    "Ротвейлер", "Сенбернар", "Сиба-ину", "Среднеазиатская овчарка", "Стандартный шнауцер (миттельшнауцер, или миттель)",
    "Стаффордширский бультерьер", "Такса (Дексхунд)", "Той пудель", "Уиппет", "Фокстерьер жесткошерстый",
    "Харьер (Бигль)", "Чау-чау", "Чихуахуа", "Ши-тцу", "Шотландский терьер (скотч-терьер)", "Эрдельтерьер",
    "Японский хин", "Венгерская выгла", "Такса"
]


LIFE_EXPECTANCY = {
    "Австралийская овчарка": 13,
    "Австралийский келпи": 12,
    "Австралийский терьер": 15,
    "Акбаш": 12,
    "Акита (Ину)": 12,
    "Аляскинский маламут": 12,
    "Американский бульдог": 10,
    "Американский водяной спаниель": 12,
    "Американский питбультерьер": 12,
    "Американский стаффордширский терьер": 12,
    "Английский бульдог": 10,
    "Английский кокер спаниель": 12,
    "Английский сеттер": 12,
    "Английский спрингер спаниель": 12,
    "Афганская борзая": 12,
    "Басенджи": 12,
    "Бассет (хаунд)": 12,
    "Бедлингтон терьер": 14,
    "Бельгийская овчарка": 12,
    "Бернский зенненхунд": 8,
    "Бигль": 12,
    "Бишон Фризе": 15,
    "Бладхаунд": 10,
    "Боксер": 10,
    "Бостон терьер": 12,
    "Брюссельский гриффон": 15,
    "Бульмастифф": 8,
    "Бультерьер": 12,
    "Веймаранер (веймарская легавая)": 12,
    "Вельш корги кардиган (корги кардиган)": 12,
    "Вельш корги пемброк (корги пемброк)": 12,
    "Вельштерьер": 15,
    "Венгерская короткошерстая легавая (выжлы)": 12,
    "Вест хайленд уайт терьер (вест хайленд вайт терьер)": 12,
    "Гаванский бишон (гаванская болонка)": 15,
    "Далматин": 13,
    "Джек рассел терьер": 13,
    "Доберман пинчер": 10,
    "Золотистый ретривер": 12,
    "Ивицкая борзая (ивисская собака)": 12,
    "Ирландский водяной (водный) спаниель": 12,
    "Йоркшир терьер": 15,
    "Кавалер кинг чарльз спаниель": 12,
    "Кеесхонд": 12,
    "Керри блю терьер": 12,
    "Китайская хохлатая собака": 12,
    "Коикерхондье": 12,
    "Кокер спаниель": 12,
    "Колли": 14,
    "Лабрадор ретривер": 12,
    "Левретка (итальянская левретка)": 12,
    "Лейкленд терьер": 15,
    "Леопардовая собака Катахулы (катахула)": 12,
    "Лхасский апсо": 15,
    "Малый пудель": 15,
    "Мальтийская болонка": 15,
    "Манчестерский терьер": 12,
    "Маремма": 12,
    "Мастиф": 8,
    "Миниатюрная австралийская овчарка": 12,
    "Миниатюрный бультерьер": 12,
    "Миниатюрный пинчер": 15,
    "Миниатюрный шнауцер": 12,
    "Мопс": 12,
    "N/A": None,
    "Немецкая короткошерстная легавая (Курцхаар)": 12,
    "Немецкая овчарка": 10,
    "Папильон (папийон)": 15,
    "Пиренейская горная собака": 12,
    "Померанский шпиц": 12,
    "Ризеншнауцер (гигантский шнауцер)": 12,
    "Родезийский риджбек": 12,
    "Ротвейлер": 9,
    "Сенбернар": 8,
    "Сиба-ину": 13,
    "Среднеазиатская овчарка": 10,
    "Стандартный шнауцер (миттельшнауцер, или миттель)": 12,
    "Стаффордширский бультерьер": 12,
    "Такса (Дексхунд)": 15,
    "Той пудель": 15,
    "Уиппет": 12,
    "Фокстерьер жесткошерстый": 12,
    "Харьер (Бигль)": 12,
    "Чау-чау": 12,
    "Чихуахуа": 15,
    "Ши-тцу": 15,
    "Шотландский терьер (скотч-терьер)": 15,
    "Эрдельтерьер": 12,
    "Японский хин": 15
}


class DogsParser(Parser):
    def __init__(self) -> None:
        self.url = "https://www.petshop.ru/adverts/dogs/"
        self.source = "petshop.ru"
        self.scroll = True

    @staticmethod
    def clean_text(text: str) -> str:
        text = text.replace(';', '').strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    @staticmethod
    def parse_price(price_str: str) -> int:
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

    @staticmethod
    def parse_age(description: str) -> Union[float, str]:
        match = re.search(r'(\d+)\s*(лет|года|месяцев|месяца)', description, re.IGNORECASE)
        if match:
            age = int(match.group(1))
            unit = match.group(2).lower()
            if 'месяц' in unit:
                return round(age / 12, 1)
            else:
                return float(age)
        return "N/A"

    @staticmethod
    def get_life_expectancy(breed: str) -> Union[int, None]:
        return LIFE_EXPECTANCY.get(breed, 12)

    @staticmethod
    def find_breed(name: str, description: str) -> str:
        search_text = f"{name} {description}".lower()

        for breed in KNOWN_BREEDS:
            if breed.lower() in search_text:
                return breed

        return choice(KNOWN_BREEDS)

    @staticmethod
    def fix_age(age: Union[float, str]) -> float:
        if age == "N/A" or age > 20:
            return 0.5
        return age

    @staticmethod
    def generate_gen(description: str) -> bool:
        return bool(re.search(r'\bредкий ген\w*\b', description, re.IGNORECASE)) or \
            bool(re.search(r'\bчемпион\w*\b', description, re.IGNORECASE)) or \
            bool(re.search(r'\bвыстав\w*\b', description, re.IGNORECASE)) or \
            bool(re.search(r'\bтитул\w*\b', description, re.IGNORECASE))

    def get_product_list(self) -> None:
        content_list = super().get_page_content(url=self.url, scroll=self.scroll)

        names, breeds, rare_gen, prices, ages, life_expectancies = [], [], [], [], [], []
        descriptions, regions, dates, images = [], [], [], []

        for content in content_list:
            soup = BeautifulSoup(content, features="lxml")
            raw_list = soup.find_all('div', attrs={'class': 'articles-item ng-scope'})

            for raw in raw_list:
                soup = BeautifulSoup(str(raw), features='lxml')

                name = self.clean_text(soup.find('a', attrs={'class': "ng-binding"}).get_text())
                description = self.clean_text(soup.find('div', attrs={'class': "text ng-binding"}).get_text())
                raw_price = soup.find('div', attrs={'class': 'price ng-scope'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text() if soup.find('div', attrs={'class': 'price ng-scope'}) else "N/A"
                price = self.parse_price(self.clean_text(raw_price)) if raw_price != "N/A" else "N/A"
                breed = self.clean_text(soup.find('div', attrs={'class': 'breed'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text()) if soup.find('div', attrs={'class': 'breed'}) else "N/A"
                if breed == "Не указано":
                    breed = self.find_breed(name, description)

                region = self.clean_text(soup.find('div', attrs={'class': 'region'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text()) if soup.find('div', attrs={'class': 'region'}) else "N/A"
                if region == "Не указано":
                    region = "Москва"

                date = self.clean_text(soup.find('div', attrs={'class': 'date'}).find('span', attrs={
                    'class': 'ng-binding'}).get_text()) if soup.find('div', attrs={'class': 'date'}) else "N/A"

                img_div = soup.find('div', attrs={'class': 'articles-img'})
                img = img_div.find('img')['ng-src'] if img_div else "N/A"

                gen = self.generate_gen(description)

                age = self.parse_age(description)
                age = self.fix_age(age)
                life_expectancy = self.get_life_expectancy(breed)

                if price == "N/A":
                    continue

                names.append(name)
                breeds.append(breed)
                rare_gen.append(gen)
                prices.append(price)
                ages.append(age)
                life_expectancies.append(life_expectancy)
                descriptions.append(description)
                regions.append(region)
                dates.append(date)
                images.append(img)

        data = {
            'name': names,
            'breed': breeds,
            'rare_gen': rare_gen,
            'price': prices,
            'age': ages,
            'life_expectancy': life_expectancies,
            'description': descriptions,
            'region': regions,
            'date': dates,
            'image_url': images,
        }
        df = pd.DataFrame(data)
        df.to_csv('dogs_dataset.csv', index=False, encoding='utf-8-sig')

        print('Data saved to dogs_dataset.csv in structured format.')