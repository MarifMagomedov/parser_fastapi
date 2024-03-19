import bs4.element
from bs4 import BeautifulSoup
from parsers.driver import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class MegaMarketParser:
    base_url = 'https://megamarket.ru'

    @staticmethod
    def _get_source_html(url) -> str:
        try:
            driver.get(url)
            WebDriverWait(
                driver, 60,
            ).until(
                expected_conditions.presence_of_element_located(
                    (By.TAG_NAME, 'html')
                )
            )
            return driver.page_source
        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    @classmethod
    def get_items(cls, category: str) -> list[dict[str, str]]:
        file = cls._get_source_html(cls.base_url + '/catalog/' + category.replace(' ', '%20'))
        soup = BeautifulSoup(file, 'lxml')
        mobile_cards = soup.find_all('div', class_='catalog-item-mobile ddl_product')
        result_items = []
        for card in mobile_cards:
            item_info = card.find('div', class_='item-info')
            item_old_price = item_info.find('span', class_='crossed-old-price-discount__price')
            if isinstance(item_old_price, bs4.element.Tag):
                item_bonus = item_info.find('div', class_='item-bonus')
                if isinstance(item_bonus, bs4.element.Tag):
                    item_price = int(item_info.find(
                        'span', class_='bonus-amount bonus-amount_without-percent'
                    ).get_text().replace(' ', ''))
                    item_bonus = int(item_bonus.find(
                        'span', 'bonus-amount bonus-amount_without-percent'
                    ).get_text().replace(' ', ''))
                    item_href = cls.base_url + card.find('a', href=True)['href']
                    item_name = item_info.find('a', class_='ddl_product_link').get_text()
                    result_items.append({
                        'item_name': item_name.lstrip(),
                        'item_price': item_price,
                        'item_old_price': item_old_price.get_text(),
                        'item_bonus': item_bonus,
                        'item_href': item_href
                    })
        result_items.sort(key=lambda x: int(x['item_bonus']))
        return result_items
