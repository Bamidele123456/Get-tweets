import time
from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pytz
from tzlocal import get_localzone


def scrape_tweets(query, country, hours, username, password, cookies_file_path):
    local_timezone = get_localzone()
    current_time = datetime.now()
    search_query = f"https://x.com/search?f=top&q={query}+{country}&src=typed_query"
    options = Options()
    options.headless = False  # Set to True if you want it to run without opening a browser window
    chromedriver_path = 'chromedriver.exe'  # Assumes chromedriver is in the working directory or PATH
    s = Service(chromedriver_path)
    driver = webdriver.Chrome(service=s)
    login = "https://x.com/i/flow/login"
    all_data = []
    try:
        with open(cookies_file_path, 'r') as f:
            cookies = eval(f.read())
        time.sleep(5)
        driver.get(f"https://x.com/")
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get(search_query)
        time.sleep(10)
        driver.refresh()
        time.sleep(5)
        scroll_limit = 5
        for _ in range(scroll_limit):
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            aria_labels = soup.find_all('div', {'role': 'group'})
            for div in aria_labels:
                aria_label = div.get('aria-label')
                if aria_label:
                    data = {}
                    for item in aria_label.split(', '):
                        value, key = item.split(' ')
                        if key in ['replies', 'reposts', 'likes', 'bookmarks', 'views']:
                            data[key] = value
                        else:
                            try:
                                data[key] = int(value.replace('K', '000').replace('M', '000000'))
                            except ValueError:
                                data[key] = 0
                    parent_div = div.find_parent('article')
                    if parent_div:
                        post_link = parent_div.find('a', {'role': 'link', 'href': True, 'href': lambda href: '/status/' in href})
                        data['post_url'] = f"https://twitter.com{post_link['href']}" if post_link else 'No link found'
                        time_element = parent_div.find('time')
                        if time_element and time_element.get('datetime'):
                            try:
                                tweet_time_str = time_element['datetime']
                                tweet_time = datetime.strptime(tweet_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                                utc_time = pytz.utc.localize(tweet_time)
                                tweet_times = utc_time.astimezone(local_timezone)
                                time_difference = current_time - tweet_times.replace(tzinfo=None)
                                hours_difference = time_difference.total_seconds() / 3600
                                if hours_difference <= hours:
                                    if data not in all_data:
                                        all_data.append(data)
                            except Exception:
                                continue
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
    except FileNotFoundError:
        driver.get(login)
        time.sleep(60)
        input_field = driver.find_element(by="name", value="text")
        input_field.send_keys(username)
        input_field.send_keys(Keys.ENTER)
        time.sleep(10)
        password_field = driver.find_element(by="name", value="password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(90)
        cookies = driver.get_cookies()
        with open(cookies_file_path, 'w') as f:
            f.write(str(cookies))
        driver.get(search_query)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(5)
        scroll_limit = 5
        for _ in range(scroll_limit):
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            aria_labels = soup.find_all('div', {'role': 'group'})
            for div in aria_labels:
                aria_label = div.get('aria-label')
                if aria_label:
                    data = {}
                    for item in aria_label.split(', '):
                        value, key = item.split(' ')
                        if key in ['replies', 'reposts', 'likes', 'bookmarks', 'views']:
                            data[key] = value
                        else:
                            try:
                                data[key] = int(value.replace('K', '000').replace('M', '000000'))
                            except ValueError:
                                data[key] = 0
                    parent_div = div.find_parent('article')
                    if parent_div:
                        post_link = parent_div.find('a', {'role': 'link', 'href': True, 'href': lambda href: '/status/' in href})
                        data['post_url'] = f"https://twitter.com{post_link['href']}" if post_link else 'No link found'
                        time_element = parent_div.find('time')
                        if time_element and time_element.get('datetime'):
                            try:
                                tweet_time_str = time_element['datetime']
                                tweet_time = datetime.strptime(tweet_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                                utc_time = pytz.utc.localize(tweet_time)
                                tweet_times = utc_time.astimezone(local_timezone)
                                time_difference = current_time - tweet_times.replace(tzinfo=None)
                                hours_difference = time_difference.total_seconds() / 3600
                                if hours_difference <= hours:
                                    if data not in all_data:
                                        all_data.append(data)
                            except Exception:
                                continue
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
    driver.quit()
    return all_data 