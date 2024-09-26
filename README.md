# reams2go-scraper
Grocery store inventory scraper
Reams2Go Product Scraper
This script is a web scraper for the Reams2Go website, designed to extract product information such as product names, prices, category IDs, and category names, and save the data into a CSV file for further analysis.

Features
Web Scraping: Connects to the Reams2Go API to fetch product data.
Category Navigation: Recursively traverses through all categories and subcategories.
Data Extraction: Collects detailed product information.
CSV Export: Saves the scraped data into reams2go_products.csv.
Logging: Provides detailed logs of the scraping process in scraper.log.
Randomized Timing: Includes randomized sleep intervals to mimic human browsing behavior.

Future Scope
Enhanced Error Handling: Improve exception handling to manage unexpected API responses or connection issues.
Multi-threading: Implement concurrency to speed up the scraping process.
Data Enrichment: Extract additional product details like descriptions, images, and stock availability.
Command-Line Arguments: Allow users to specify parameters like category filters, output file names, or logging levels.
Unit Tests: Develop tests to ensure code reliability and facilitate future development.

How to Use
Prerequisites
Python 3.7 or higher
Install required packages:
pip install requests

1.Running the Script
Clone the Repository
git clone https://github.com/yourusername/reams2go-scraper.git
cd reams2go-scraper

2.Run the Script
python scrape_reams2go.py

The script will start fetching product data from the Reams2Go website.

Progress and debug information will be logged to the console and scraper.log.

3. Check the output
The scraped data will be saved in reams2go_products.csv.

Logs detailing the scraping process are available in scraper.log.

Notes
Adjust Sleep Intervals: The random_sleep function introduces delays between requests. You can adjust the min_seconds and max_seconds parameters to control the delay.
Logging: Modify the logging level in the logging.basicConfig setup if you need more or less verbosity.
API Tokens: The script automatically fetches and updates the necessary API tokens required for the requests.

