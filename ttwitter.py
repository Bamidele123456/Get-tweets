import tkinter as tk
from tkinter import scrolledtext
from selenium.webdriver.chrome.options import Options
import urllib.parse
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import threading
import pytz
from tzlocal import get_localzone
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Ashhlyynxo
# Ayelen@123


# Function to handle the Selenium scraping in a separate thread
def start_scraping():
    query = query_input.get()
    local_timezone = get_localzone()
    country = country_input.get()
    hours = int(hours_input.get())
    current_date = datetime.now()
    current_time = datetime.now()
    until = datetime.now(local_timezone)
    start_time = current_time - timedelta(hours=hours)
    search_query = f"https://x.com/search?f=top&q={query}+{country}&src=typed_query"
    options = Options()
    options.headless = False  # Set to True if you want it to run without opening a browser window
    chromedriver_path = resource_path('chromedriver.exe')

    s = Service(chromedriver_path)
    driver = webdriver.Chrome(service=s)


    login = "https://x.com/i/flow/login"
    username = username_input.get()
    password = password_input.get()

    try:
        cookies_file_path = resource_path(f'Logs/{username}.txt')

        # Open and read the cookies file
        with open(cookies_file_path, 'r') as f:
            cookies = eval(f.read())
        time.sleep(10)
        driver.get(f"https://x.com/")

        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.get(search_query)

        time.sleep(10)
        current_url = driver.current_url


        if current_url == search_query:
            driver.refresh()
            time.sleep(5)

            time.sleep(20)
            all_data = []
            scroll_limit = 5  # Adjust this limit based on how many scrolls you want

            for _ in range(scroll_limit):
                # Use BeautifulSoup to parse page content
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                aria_labels = soup.find_all('div', {'role': 'group'})

                for div in aria_labels:
                    aria_label = div.get('aria-label')  # Get the aria-label attribute from each div
                    if aria_label:  # Ensure aria-label exists
                        data = {}
                        for item in aria_label.split(', '):
                            value, key = item.split(' ')
                            if key in ['replies', 'reposts', 'likes', 'bookmarks', 'views']:
                                data[key] = value
                            else:
                                try:
                                    data[key] = int(value.replace('K', '000').replace('M', '000000'))
                                except ValueError:
                                    data[key] = 0  # Fallback in case of conversion error

                        # Find post URL within parent div
                        parent_div = div.find_parent('article')
                        if parent_div:
                            post_link = parent_div.find('a', {'role': 'link', 'href': True,
                                                              'href': lambda href: '/status/' in href})
                            data[
                                'post_url'] = f"https://twitter.com{post_link['href']}" if post_link else 'No link found'

                            # Now handle timestamp and filtering based on the hours
                            time_element = parent_div.find('time')
                            if time_element and time_element.get('datetime'):
                                try:
                                    tweet_time_str = time_element['datetime']
                                    tweet_time = datetime.strptime(tweet_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")


                                    utc_time = pytz.utc.localize(tweet_time)

                                    tweet_times = utc_time.astimezone(local_timezone)

                                    # Calculate the time difference
                                    time_difference = current_time - tweet_times.replace(tzinfo=None)


                                    hours_difference = time_difference.total_seconds() / 3600

                                    if hours_difference <= hours:
                                        if data not in all_data:
                                            all_data.append(data)

                                except Exception as e:
                                    continue

                # Scroll down to load more content
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)  # Wait for new content to load

            output_box.delete('1.0', tk.END)  # Clear previous output
            output_box.insert(tk.END, "Viral Tweets\n\n")

            for i, data in enumerate(all_data, start=1):
                output_box.insert(tk.END, f"{i}.\n")  # Number each tweet
                for key, value in data.items():
                    output_box.insert(tk.END, f"   {key.capitalize()}: {value}\n")
                output_box.insert(tk.END, "\n")
        else:
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
            cookies_file_path = resource_path(f'Logs/{username}.txt')

            # Open and write to the cookies file
            with open(cookies_file_path, 'w') as f:
                f.write(str(cookies))
            driver.get(search_query)

            # Add cookies to the driver
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(5)
            # driver.get('https://x.com/search?q=dog&src=typed_query')
            time.sleep(20)
            all_data = []
            scroll_limit = 10  # Adjust this limit based on how many scrolls you want

            for _ in range(scroll_limit):
                # Use BeautifulSoup to parse page content
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                aria_labels = soup.find_all('div', {'role': 'group'})

                for div in aria_labels:
                    aria_label = div.get('aria-label')  # Get the aria-label attribute from each div
                    if aria_label:  # Ensure aria-label exists
                        data = {}
                        for item in aria_label.split(', '):
                            value, key = item.split(' ')
                            if key in ['replies', 'reposts', 'likes', 'bookmarks', 'views']:
                                data[key] = value
                            else:
                                try:
                                    data[key] = int(value.replace('K', '000').replace('M', '000000'))
                                except ValueError:
                                    data[key] = 0  # Fallback in case of conversion error

                        # Find post URL within parent div
                        parent_div = div.find_parent('article')
                        if parent_div:
                            post_link = parent_div.find('a', {'role': 'link', 'href': True,
                                                              'href': lambda href: '/status/' in href})
                            data[
                                'post_url'] = f"https://twitter.com{post_link['href']}" if post_link else 'No link found'

                            # Now handle timestamp and filtering based on the hours
                            tweets = driver.find_elements(By.CSS_SELECTOR, "article")
                            for tweet in tweets:
                                try:
                                    timestamp_element = tweet.find_element(By.CSS_SELECTOR, "time")
                                    tweet_time_str = timestamp_element.get_attribute("datetime")
                                    tweet_time = datetime.strptime(tweet_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

                                    utc_time = pytz.utc.localize(tweet_time)

                                    tweet_times = utc_time.astimezone(local_timezone)

                                    # Calculate the time difference
                                    time_difference = current_time - tweet_times.replace(tzinfo=None)

                                    hours_difference = time_difference.total_seconds() / 3600

                                    if hours_difference <= hours:
                                        if data not in all_data:
                                            all_data.append(data)

                                except Exception as e:
                                    continue

                # Scroll down to load more content
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)  # Wait for new content to load

            output_box.delete('1.0', tk.END)  # Clear previous output
            output_box.insert(tk.END, "Viral Tweets\n\n")

            for i, data in enumerate(all_data, start=1):
                output_box.insert(tk.END, f"{i}.\n")  # Number each tweet
                for key, value in data.items():
                    output_box.insert(tk.END, f"   {key.capitalize()}: {value}\n")
                output_box.insert(tk.END, "\n")



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
        cookies_file_path = resource_path(f'Logs/{username}.txt')

        # Open and write to the cookies file
        with open(cookies_file_path, 'w') as f:
            f.write(str(cookies))
        driver.get(search_query)

        # Add cookies to the driver
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(5)
        # driver.get('https://x.com/search?q=dog&src=typed_query')
        time.sleep(20)
        all_data = []
        scroll_limit = 10  # Adjust this limit based on how many scrolls you want

        for _ in range(scroll_limit):
            # Use BeautifulSoup to parse page content
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            aria_labels = soup.find_all('div', {'role': 'group'})

            for div in aria_labels:
                aria_label = div.get('aria-label')  # Get the aria-label attribute from each div
                if aria_label:  # Ensure aria-label exists
                    data = {}
                    for item in aria_label.split(', '):
                        value, key = item.split(' ')
                        if key in ['replies', 'reposts', 'likes', 'bookmarks', 'views']:
                            data[key] = value
                        else:
                            try:
                                data[key] = int(value.replace('K', '000').replace('M', '000000'))
                            except ValueError:
                                data[key] = 0  # Fallback in case of conversion error

                    # Find post URL within parent div
                    parent_div = div.find_parent('article')
                    if parent_div:
                        post_link = parent_div.find('a', {'role': 'link', 'href': True,
                                                          'href': lambda href: '/status/' in href})
                        data[
                            'post_url'] = f"https://twitter.com{post_link['href']}" if post_link else 'No link found'

                        # Now handle timestamp and filtering based on the hours
                        tweets = driver.find_elements(By.CSS_SELECTOR, "article")
                        for tweet in tweets:
                            try:
                                timestamp_element = tweet.find_element(By.CSS_SELECTOR, "time")
                                tweet_time_str = timestamp_element.get_attribute("datetime")
                                tweet_time = datetime.strptime(tweet_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

                                utc_time = pytz.utc.localize(tweet_time)

                                tweet_times = utc_time.astimezone(local_timezone)

                                # Calculate the time difference
                                time_difference = current_time - tweet_times.replace(tzinfo=None)

                                hours_difference = time_difference.total_seconds() / 3600

                                if hours_difference <= hours:
                                    if data not in all_data:
                                        all_data.append(data)

                            except Exception as e:
                                continue

            # Scroll down to load more content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for new content to load

        output_box.delete('1.0', tk.END)  # Clear previous output
        output_box.insert(tk.END, "Viral Tweets\n\n")

        for i, data in enumerate(all_data, start=1):
            output_box.insert(tk.END, f"{i}.\n")  # Number each tweet
            for key, value in data.items():
                output_box.insert(tk.END, f"   {key.capitalize()}: {value}\n")
            output_box.insert(tk.END, "\n")


# Function to start scraping in a new thread
def start_thread():
    threading.Thread(target=start_scraping).start()


# Create the GUI
root = tk.Tk()
root.title("Twitter Scraper")

# Labels and input fields for query, country, and hours
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
username_input = tk.Entry(root, width=30)
username_input.grid(row=0, column=1)

tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
password_input = tk.Entry(root, width=30, show="*")  # Mask the password with show='*'
password_input.grid(row=1, column=1)

# Labels and input fields for query, country, and hours
tk.Label(root, text="Query:").grid(row=2, column=0, padx=10, pady=10)
query_input = tk.Entry(root, width=30)
query_input.grid(row=2, column=1)

tk.Label(root, text="Country:").grid(row=3, column=0, padx=10, pady=10)
country_input = tk.Entry(root, width=30)
country_input.grid(row=3, column=1)

tk.Label(root, text="Interval (hours):").grid(row=4, column=0, padx=10, pady=10)
hours_input = tk.Entry(root, width=30)
hours_input.grid(row=4, column=1)

# Start button to begin scraping
start_button = tk.Button(root, text="Start Scraping", command=start_thread)
start_button.grid(row=5, column=0, columnspan=2, pady=20)

# Output box to display results
output_box = scrolledtext.ScrolledText(root, width=60, height=20)
output_box.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Run the GUI loop
root.mainloop()
