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
from twitter_scraper import scrape_tweets

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
    country = country_input.get()
    hours = int(hours_input.get())
    username = username_input.get()
    password = password_input.get()
    cookies_file_path = resource_path(f'Logs/{username}.txt')
    
    all_data = scrape_tweets(query=query, country=country, hours=hours, username=username, password=password, cookies_file_path=cookies_file_path)

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
