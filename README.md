# Twitter Scraper

This project provides tools to scrape tweets from Twitter (X) using Selenium, with both a web interface (Flask) and a desktop GUI (Tkinter). It supports searching for tweets by query and country, and filtering by time interval.

## Features
- Scrape tweets by keyword and country
- Filter tweets by recency (interval in hours)
- View results in a web browser (Flask app) or desktop GUI (Tkinter)
- Handles Twitter login and session cookies automatically

## Requirements
- Python 3.8+
- Google Chrome browser
- ChromeDriver (place `chromedriver.exe` in the project root or ensure it is in your PATH)

### Python Packages
- selenium
- flask
- beautifulsoup4
- webdriver-manager
- pytz
- tzlocal

Install dependencies with:
```bash
pip install selenium flask beautifulsoup4 webdriver-manager pytz tzlocal
```

## Usage

### 1. Flask Web App
1. Start the Flask app:
    ```bash
    python tflask.py
    ```
2. Open your browser and go to [http://localhost:5000](http://localhost:5000)
3. Enter your search query, country, and interval (in hours), then submit.
4. Results will be displayed on the next page.

### 2. Tkinter Desktop GUI
1. Run the Tkinter app:
    ```bash
    python ttwitter.py
    ```
2. Enter your Twitter username, password, search query, country, and interval (in hours).
3. Click "Start Scraping" to view results in the GUI.

### 3. Command-Line Script
You can also run the scraping logic directly:
```bash
python main.py
```

## Notes
- The first time you run the scraper, you will need to log in to Twitter manually in the browser window that opens. Your session cookies will be saved for future runs.
- Make sure your ChromeDriver version matches your installed Chrome browser version.
- This tool is for educational and personal use only. Do not use it to violate Twitter's terms of service.

## File Structure
- `twitter_scraper.py` - Core scraping logic
- `tflask.py` - Flask web app
- `ttwitter.py` - Tkinter GUI app
- `main.py` - Command-line example
- `templates/` - HTML templates for Flask
- `logs.txt` - Stores session cookies

## License
MIT License 