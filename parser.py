from typing import List, Union
from time import sleep
from abc import ABC, abstractmethod

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from item import Item

class Parser(ABC):
    def get_page_content(self,
                         job_name: str,
                         url: str,
                         searchbar_xpath: str,
                         block_button_xpath: str,
                         scroll: bool = False,
                         scroll_timeout: Union[int, float] = 0.3) -> str:
        options = Options()
        options.add_argument("window-size=1920,1080")
        service = Service(ChromeDriverManager().install())
        with webdriver.Chrome(service=service, options=options) as driver:
            driver.get(url)
            sleep(5)

            # Переопределяем элемент поиска каждый раз перед взаимодействием
            search_element = driver.find_element(By.XPATH, searchbar_xpath)
            search_element.click()
            sleep(1)
            search_element.clear()
            search_element.send_keys(job_name)
            search_element.send_keys(Keys.ENTER)
            sleep(2)

            # Закрываем модальное окно, если оно появляется
            try:
                block_button_element = driver.find_element(By.XPATH, block_button_xpath)
                block_button_element.click()
            except Exception as e:
                print(f"No modal to close: {e}")

            # Добавляем ещё одно ожидание перед попыткой прокрутки
            if scroll:
                for i in range(5):
                    sleep(scroll_timeout)
                    driver.execute_script(f"window.scrollTo({i * 300}, {(i + 1) * 300})")

            # Возвращаем контент страницы
            content = driver.page_source
            return content
