from flask import Flask, request, redirect, render_template
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

from bs4 import BeautifulSoup


from selenium.webdriver.common.keys import Keys
from twitter_scraper import scrape_tweets


app = Flask(__name__)
all_data = []


@app.route('/')
def main():
    return render_template("test.html")

@app.route('/test', methods=['POST'])
def test():
    Query = request.form['query']
    Country = request.form['country']
    interval = request.form['interval']
    username = ''
    password = ''
    cookies_file_path = 'logs.txt'
    all_data = scrape_tweets(query=Query, country=Country, hours=int(interval), username=username, password=password, cookies_file_path=cookies_file_path)
    return render_template("answer.html", all_data=all_data)




if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
