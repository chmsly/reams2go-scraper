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