import csv
import logging
import time
import random
import requests
import json
from logging.handlers import RotatingFileHandler

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler('scraper.log', maxBytes=10_000_000, backupCount=5)
    ]
)

BASE_URL = "https://reamsfoodstores.api.shophero.com/mobileapp/api/v2"

def random_sleep(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def get_session():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://reams2go.com",
        "Referer": "https://reams2go.com/"
    })

    url = f"{BASE_URL}/location/1/category-tree"
    response = session.get(url)
    if response.status_code == 200:
        x_api_token = response.headers.get('x-api-token')
        if x_api_token:
            session.headers.update({"x-api-token": x_api_token})
            logging.info(f"Obtained x-api-token: {x_api_token}")
        else:
            logging.error("Could not find x-api-token in the response headers.")
            exit()
    else:
        logging.error(f"Failed to obtain x-api-token. Status code: {response.status_code}")
        exit()

    return session

def get_category_ids(session):
    url = f"{BASE_URL}/location/1/category-tree"
    response = session.get(url)
    if response.status_code == 200:
        data = response.json()
        category_ids = []

        def extract_ids(categories_dict):
            for key, category in categories_dict.items():
                category_ids.append({
                    'name': category.get('category_name'),
                    'id': category.get('shophero_category_key')
                })
                if 'child_categories' in category and category['child_categories']:
                    extract_ids(category['child_categories'])

        extract_ids(data.get('child_categories', {}))
        return category_ids
    else:
        logging.error(f"Failed to fetch categories. Status code: {response.status_code}")
        return []

def fetch_products_api(session, category_id=None, category_name=None):
    if category_id is not None:
        logging.info(f"Fetching products for category ID: {category_id}")
        url = "https://reamsfoodstores.api.shophero.com/mobileapp/api/v2/location/1/category/"+category_id+"/products?o=0&l=500&f=1&z=status:;brands:&ea=true"
        params = {
            "page": 1,
            "per_page": 50
        }
        if category_id:
            params["category_ids"] = category_id
        
        logging.info(f"Making request to URL: {url}")
        logging.info(f"Request parameters: {params}")
        logging.info(f"Request headers: {json.dumps(dict(session.headers), indent=2)}")
        
        all_products = []
        logging.info(f"Fetching products for page {params['page']}")
        response = session.get(url, params=params)
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response headers: {json.dumps(dict(response.headers), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Response data: {json.dumps(data, indent=2)}")
            
            if isinstance(data, list):
                products = data
            elif isinstance(data, dict):
                products = data
            else:
                logging.error(f"Unexpected response type: {type(data)}")


            for product in products["filtered_products"]:
                all_products.append({
                    'name': product.get('product_name', ''),
                    'price': product.get('price').get("product_price"),
                    'category_id': category_id,
                    'category_name': category_name
                })
            params['page'] += 1
            random_sleep(1, 3)
        else:
            logging.error(f"Failed to fetch products. Status code: {response.status_code}")
            logging.error(f"Error response: {response.text}")
        return all_products

def scrape_reams2go():
    session = get_session()

    # Fetch and log the category tree
    category_tree_url = f"{BASE_URL}/location/1/category-tree"
    category_tree_response = session.get(category_tree_url)
    if category_tree_response.status_code == 200:
        logging.info(f"Category tree: {json.dumps(category_tree_response.json(), indent=2)}")
    else:
        logging.error(f"Failed to fetch category tree. Status code: {category_tree_response.status_code}")

    categories = get_category_ids(session)
    logging.info(f"Retrieved categories: {json.dumps(categories, indent=2)}")
    
    if not categories:
        logging.error("No categories found. Exiting.")
        return

    all_products = []

    
    # First, try to fetch products without a category
    logging.info("Fetching products without specifying a category")
    products = fetch_products_api(session)
    #logging.info(f"Fetched {len(products)} products without category")
    #all_products.extend(products)

    # Then, fetch products for each category
    
    with open('reams2go_products.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['name', 'price', 'category_id']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    for category in categories:
        try:
            category_id = category['id']
            category_name = category['name']
            logging.info(f"Fetching products for category: {category_name} (ID: {category_id})")
            products = None
            if category_id is not None:
                products = fetch_products_api(session, category_id, category_name)
                logging.info(f"Fetched {len(products)} products from category {category_name}")
                all_products.extend(products)
                
                with open('reams2go_products.csv', 'a', newline='', encoding='utf-8') as f:
                    fieldnames = ['name', 'price', 'category_id', 'category_name']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    for product in products:
                        writer.writerow(product)
                random_sleep(5, 10)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            logging.exception("Exception details:")
    # if all_products:
    #     logging.info("All products:" + str(all_products))
    #     with open('reams2go_products.csv', 'w', newline='', encoding='utf-8') as f:
            
    #     logging.info(f"Total products scraped: {len(all_products)}")
    #     logging.info("Products saved to reams2go_products.csv")
    # else:
    #     logging.info("No products were scraped.")

    # Log all category IDs that were processed
    logging.info("Processed category IDs:")
    for category in categories:
        logging.info(f"{category['name']}: {category['id']}")

if __name__ == "__main__":
    scrape_reams2go()