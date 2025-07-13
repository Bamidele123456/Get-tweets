from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

from bs4 import BeautifulSoup


from selenium.webdriver.common.keys import Keys
from twitter_scraper import scrape_tweets


options = Options()
options.headless = False

s=Service('C:/Users/ACER/Downloads/chromedriver.exe')
driver = webdriver.Chrome(service=s)


if __name__ == "__main__":
    Query = "Banana"
    Country = "USA"
    Hours = 1
    username = ''
    password = ''
    cookies_file_path = 'logs.txt'
    all_data = scrape_tweets(query=Query, country=Country, hours=Hours, username=username, password=password, cookies_file_path=cookies_file_path)
    print(all_data)
