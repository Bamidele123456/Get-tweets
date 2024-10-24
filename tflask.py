from flask import Flask, request, redirect, render_template
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

from bs4 import BeautifulSoup


from selenium.webdriver.common.keys import Keys


app = Flask(__name__)
all_data = []


@app.route('/')
def main():
    return render_template("test.html")

@app.route('/test', methods=['POST'])
def test():
    options = Options()
    options.headless = False
    URL = "https://x.com/i/flow/login"
    login = "https://x.com/i/flow/login"
    username = ''
    password = ''

    s = Service('C:/Users/ACER/Downloads/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    Query = request.form['query']
    Country = request.form['country']
    interval = request.form['interval']
    times =int( interval * 60)
    try:
        with open('logs.txt', 'r') as f:
            cookies = eval(f.read())

        driver.get(f"https://x.com/search?q={Query} {Country}&src=typed_query")

        # Add cookies to the driver
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(5)
        time.sleep(20)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        aria_labels = soup.find_all('div', {'role': 'group'})


        # Loop over aria_labels and extract the data
        for div in aria_labels:
            aria_label = div.get('aria-label')  # Get the aria-label attribute from each div
            if aria_label:  # Make sure it exists
                data = {}
                for item in aria_label.split(', '):
                    value, key = item.split(' ')
                    # Store in the dictionary with the value as a string
                    if key in ['replies', 'reposts', 'likes', 'bookmarks', 'views']:
                        data[key] = value  # Keep the value as a string
                    else:
                        try:
                            data[key] = int(value.replace('K', '000').replace('M', '000000'))
                        except ValueError:
                            print(f"ValueError: Unable to convert '{value}' to an integer for key '{key}'")
                            data[key] = 0  # or some other default value

                # Find the closest <a> tag containing the post link within the parent of this aria-label
                parent_div = div.find_parent('article')  # or another parent tag that groups each post
                if parent_div:
                    post_link = parent_div.find('a', {'role': 'link', 'href': True, 'href': lambda
                        href: '/status/' in href})  # Find the link with '/status/' in the href
                    if post_link:
                        post_url = post_link.get('href')
                        full_url = f"https://twitter.com{post_url}"  # Construct the full URL to the post
                        data['post_url'] = full_url  # Add the URL to the data
                    else:
                        data['post_url'] = 'No link found'  # Handle cases where no link is found

                # Append the extracted data for this div to the list
                all_data.append(data)
        print(all_data)
    except FileNotFoundError:

        # Open Twitter URL in Chrome
        time.sleep(5)
        driver.get(login)
        time.sleep(60)
        input_field = driver.find_element(by="name", value="text")
        time.sleep(10)

        input_field.send_keys(username)
        time.sleep(10)
        input_field.send_keys(Keys.ENTER)
        time.sleep(10)

        password_field = driver.find_element(by="name", value="password")
        time.sleep(10)
        # Type your password into the password field
        password_field.send_keys(password)
        time.sleep(10)
        password_field.send_keys(Keys.ENTER)
        time.sleep(90)
        time.sleep(90)
        time.sleep(90)
        cookies = driver.get_cookies()
        # Save the cookies to a file
        with open('logs.txt', 'w') as f:
            f.write(str(cookies))
    return render_template("answer.html",all_data= all_data)




if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
