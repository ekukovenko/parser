from typing import List, Union
from time import sleep
from abc import ABC, abstractmethod

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from item import Item
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Parser(ABC):
    @abstractmethod
    def get_product_list(self) -> List[Item]:
        pass

    @staticmethod
    def get_page_content(url: str,
                         scroll: bool = False,
                         scroll_timeout: Union[int, float] = 0.3) -> str:
        options = Options()
        options.add_argument("window-size=1920,1080")
        service = Service(ChromeDriverManager().install())

        all_content = []

        with (webdriver.Chrome(service=service, options=options) as driver):
            driver.get(url)
            if scroll:
                current_page = 1
                max_pages = 60
                while current_page <= max_pages:
                    sleep(2)
                    for i in range(18):
                        sleep(scroll_timeout)
                        driver.execute_script(f"window.scrollTo({i * 300}, {(i + 1) * 300})")
                        sleep(0.4)

                    page_content = driver.page_source
                    all_content.append(page_content)
                    sleep(1)
                    if current_page < 5:
                        try:
                            next_button = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//*[@id="main"]/div/div[2]/div/article/div/section[3]/div[2]/a[9]'))
                            )
                            next_button.click()
                        except Exception as e:
                            print(f"Не удалось найти кнопку 'Следующая' или произошла ошибка - 9: {e}")
                    elif current_page >= 5:
                        try:
                            next_button = WebDriverWait(driver, 20).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, '//*[@id="main"]/div/div[2]/div/article/div/section[3]/div[2]/a[11]'))
                            )
                            next_button.click()
                        except Exception as e:
                            print(f"Не удалось найти кнопку 'Следующая' или произошла ошибка - 11: {e}")
                    else:
                        break
                    current_page += 1
                    driver.execute_script("window.scrollTo(0, 0);")

        return all_content