from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from glob import glob
from os import path
class StockCSV(object):

    def __init__(self, driver="D:\chromedriver\chromedriver.exe"):
        options = Options()
        #options.add_argument("--headless")
        options.add_argument(driver)

        self.driver = webdriver.Chrome(options=options)
    def download_stock_diagram(self, url="https://finance.yahoo.com/quote/GOOGL/history?p=GOOGL"):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="btn primary"]')))
        element.click()
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="Fl(end) Mt(3px) Cur(p)"]')))
        self.driver.get(element.get_attribute('href'))
        sleep(2)
        self.driver.quit()
    @classmethod #change dir to ur download direction
    def get_stock_diagram(cls, dir=r'C:\Users\KamilB\Downloads\*', name=None):
        if name is None:
            return max(glob(dir), key=path.getctime)
        dir = dir[:-1]
        dir += name
        return dir




if __name__ == '__main__':
    S = StockCSV()
    S.download_stock_diagram()
    print(S.get_stock_diagram())
