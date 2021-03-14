from selenium import webdriver
import time
import re


def check_data(**kwargs):
    login, browser, password = kwargs.get('login'), kwargs.get('browser'), kwargs.get('password')

    if not all([login, browser, password]):
        raise Exception('Data were not entered')

    if browser not in webdriver.__dir__():
        raise Exception('Browser does not exist')


class Parser:
    """Class for parsing data in TimeWeb. Return uptime, uptime_percent, fee, remaining"""
    def __init__(self, browser: str = None, login: str = None, password: str = None):
        check_data(browser=browser, login=login, password=password)

        self.browser = browser.capitalize()
        self.login = login
        self.password = password

    @property
    def data(self) -> dict:
        return dict(browser=self.browser, login=self.login, password=self.password)

    @data.setter
    def data(self, kwargs):
        check_data(browser=kwargs.get('browser'), login=kwargs.get('login'), password=kwargs.get('password'))

        self.browser = kwargs.get('browser')
        self.login = kwargs.get('login')
        self.password = kwargs.get('password')

    def parse(self) -> dict:
        """Parse data and return it"""
        driver = webdriver.__dict__[self.browser]()
        driver.implicitly_wait(10)

        driver.get(url='https://hosting.timeweb.ru/login')
        driver.find_element_by_xpath("//input[@id='loginform-username']").send_keys(self.login)
        driver.find_element_by_xpath("//input[@id='loginform-password']").send_keys(self.password)
        driver.find_element_by_xpath("//button[@name='login-button']").click()

        for _ in range(10):
            try:
                uptime_data = driver.find_elements_by_xpath("//div[@id='up-time-info']//span")
                fee_data = driver.find_element_by_xpath("//p[@class='cpS-h-XS']")
                remaining_data = driver.find_element_by_xpath("//article[@class='cpS-icon-n-info-blk __last']")
                break
            except:
                time.sleep(1)

        uptime_data = driver.find_elements_by_xpath("//div[@id='up-time-info']//span")
        fee_data = driver.find_element_by_xpath("//p[@class='cpS-h-XS']")
        remaining_data = driver.find_element_by_xpath("//article[@class='cpS-icon-n-info-blk __last']")

        uptime = re.findall(r'\d+ .', uptime_data[0].text)
        uptime_percent = re.findall(r'\d*,\d+ .', uptime_data[2].text)[0]
        fee = re.findall(r'\d+', fee_data.text)[0]
        remaining = {'days': re.findall(r'\d+', remaining_data.text)[0],
                     'before': re.findall(r'\(.*\)', remaining_data.text)[0][1:-1]}

        driver.quit()
        return {
            'uptime': list(uptime),
            'uptime_percent': str(uptime_percent),
            'fee': str(fee),
            'remaining': dict(remaining)
        }