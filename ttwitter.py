import tkinter as tk
from tkinter import scrolledtext
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import threading

# Ashhlyynxo
# Ayelen@123


# Function to handle the Selenium scraping in a separate thread
def start_scraping():
    query = query_input.get()
    country = country_input.get()
    hours = int(hours_input.get())
    interval = hours * 3600

    # Set options for Selenium
    options = Options()
    options.headless = False  # Set to True if you want it to run without opening a browser window
    s=Service('C:/Users/ACER/Downloads/chromedriver.exe')
    driver = webdriver.Chrome(service=s)

    URL = "https://x.com/i/flow/login"
    login = "https://x.com/i/flow/login"
    username = username_input.get()
    password = password_input.get()

    while True:
        try:
            # Read cookies from a file if they exist
            with open(f'{username}.txt', 'r') as f:
                cookies = eval(f.read())

            # Navigate to the search query URL
            driver.get(f"https://x.com/search?q={query} {country}&src=typed_query")

            # Add cookies to the driver
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(5)

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            aria_labels = soup.find_all('div', {'role': 'group'})
            all_data = []

            for div in aria_labels:
                aria_label = div.get('aria-label')
                if aria_label:
                    data = {}
                    for item in aria_label.split(', '):
                        value, key = item.split(' ')
                        if key in ['replies', 'reposts', 'likes', 'bookmarks', 'views']:
                            data[key] = value

                    parent_div = div.find_parent('article')
                    if parent_div:
                        post_link = parent_div.find('a', {'role': 'link', 'href': True,
                                                          'href': lambda href: '/status/' in href})
                        if post_link:
                            post_url = post_link.get('href')
                            full_url = f"https://twitter.com{post_url}"
                            data['post_url'] = full_url
                        else:
                            data['post_url'] = 'No link found'
                    all_data.append(data)
                    print(all_data)

            # Display the data in the output box
            output_box.delete('1.0', tk.END)  # Clear previous output
            for post in all_data:
                output_box.insert(tk.END, f"{post}\n\n")

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
            with open('logs.txt', 'w') as f:
                f.write(str(cookies))
            driver.get(f"https://x.com/search?q={query} {country}&src=typed_query")

            # Add cookies to the driver
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(5)

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            aria_labels = soup.find_all('div', {'role': 'group'})
            all_data = []

            for div in aria_labels:
                aria_label = div.get('aria-label')
                if aria_label:
                    data = {}
                    for item in aria_label.split(', '):
                        value, key = item.split(' ')
                        if key in ['replies', 'reposts', 'likes', 'bookmarks', 'views']:
                            data[key] = value

                    parent_div = div.find_parent('article')
                    if parent_div:
                        post_link = parent_div.find('a', {'role': 'link', 'href': True,
                                                          'href': lambda href: '/status/' in href})
                        if post_link:
                            post_url = post_link.get('href')
                            full_url = f"https://twitter.com{post_url}"
                            data['post_url'] = full_url
                        else:
                            data['post_url'] = 'No link found'
                    all_data.append(data)

            # Display the data in the output box
            output_box.delete('1.0', tk.END)  # Clear previous output
            for post in all_data:
                output_box.insert(tk.END, f"{post}\n\n")

        # Sleep for the specified interval (in seconds)
        time.sleep(interval)


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