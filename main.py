from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import re
import csv_import
from multiprocessing import Pool
import math
chrome_options = Options()
chrome_options.add_argument("--headless")


def get_ticker_info(driver, exchange, ticker):
    try:
        driver.get(
            f'https://www.morningstar.com/stocks/{exchange}/{ticker}/quote')
        time.sleep(1)
        price = driver.find_element_by_id('message-box-price').text
        percent_change = driver.find_element_by_id('message-box-percentage')
        change_val = percent_change.text
        change_dir = percent_change.get_attribute('class').split()[-1]
        driver.find_element_by_xpath(
            '//*[@id="tabs"]/div/mds-button-group/div/slot/div/mds-button[3]/label/input').click()
        time.sleep(1)
        float_percent = driver.find_element_by_xpath(
            '//*[@id="__layout"]/div/div[2]/div[3]/main/div[2]/div/div/div[1]/sal-components/section/div/div/div/div/div[2]/div/div/div/div[2]/div[3]/div/div[2]/ul/li[4]/div/div[2]')
        #print(ticker, price, change_dir, change_val, float_percent.text)
        if (float(float_percent.text) > 50.0):
            print(f'{ticker}: HIGH SHORT PERCENT: {float_percent.text}')
        return (ticker, price, change_dir, change_val.split()[-1], float_percent.text)
    except:
        pass
        #print(ticker, e)
        #print(f'Could not get ticker {ticker}')


def run_func(tickers):
    driver = webdriver.Chrome(options=chrome_options,
                              executable_path='./chromedriver')
    for ticker in tickers:
        res = get_ticker_info(driver, 'xnas', ticker)
    driver.close()
    return res


def thread_cycle():
    pool = Pool(processes=64)
    data = list(csv_import.get_data())
    chunk_size = math.ceil(len(data) / 10)
    chunks = [data[x:x+chunk_size] for x in range(0, len(data), chunk_size)]
    res = pool.map(run_func, chunks)
    f = open('results.txt', 'w')
    for i in res:
        if i != None:
            f.write(" ".join([str(e) for e in i]))
    f.close()


def main():
    thread_cycle()


if __name__ == '__main__':
    main()
