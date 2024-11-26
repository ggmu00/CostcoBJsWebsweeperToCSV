import requests
from bs4 import BeautifulSoup
import pandas as pd


# Function to fetch the HTML content of a page
def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    return response.content


# Function to parse Costco food and beverage products
def parse_costco_foods(content):
    soup = BeautifulSoup(content, 'html.parser')
    products = []

    # Example: Locate product information (this is an example, adjust to Costco's HTML structure)
    for product in soup.find_all('div', class_='caption link-behavior'):  # Update based on Costco page structure
        name = product.find('span', class_='description').text.strip() if product.find('span',
                                                                                       class_='description') else 'N/A'
        price = product.find('span', class_='price').text.strip() if product.find('span', class_='price') else 'N/A'
        link = product.find('a', href=True)['href'] if product.find('a', href=True) else 'N/A'

        products.append([name, price, link])

    return products


# Function to parse BJ's food and beverage products
def parse_bjs_foods(content):
    soup = BeautifulSoup(content, 'html.parser')
    products = []

    # Example: Locate product information (this is an example, adjust to BJ's HTML structure)
    for product in soup.find_all('div', class_='product-tile'):  # Update based on BJ's page structure
        name = product.find('span', class_='product-title').text.strip() if product.find('span',
                                                                                         class_='product-title') else 'N/A'
        price = product.find('span', class_='price').text.strip() if product.find('span', class_='price') else 'N/A'
        link = product.find('a', href=True)['href'] if product.find('a', href=True) else 'N/A'

        products.append([name, price, link])

    return products


# Function to save the data into a CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Product Name', 'Price', 'Product Link'])
    df.to_csv(filename, index=False)


# Function to handle pagination and fetch all product pages for Costcodef fetch_all_costco_pages(base_url, max_pages=10):
def fetch_all_costco_pages(base_url, max_pages=10):
    all_products = []
    page_num = 1
    while page_num <= max_pages:
        url = f"{base_url}?currentPage={page_num}"
        print(f"Fetching page {page_num}...")
        content = fetch_page(url)
        products = parse_costco_foods(content)
        if not products:  # If no products are found, stop pagination
            break
        all_products.extend(products)
        page_num += 1
    return all_products


# Function to handle pagination and fetch all product pages for BJ's
def fetch_all_bjs_pages(base_url, max_pages=10):
    all_products = []
    page_num = 1
    while page_num <= max_pages:
        url = f"{base_url}?page={page_num}"
        print(f"Fetching page {page_num}...")
        content = fetch_page(url)
        products = parse_bjs_foods(content)
        if not products:  # If no products are found, stop pagination
            break
        all_products.extend(products)
        page_num += 1
    return all_products


# Main function to run the scraper
def main():
    costco_dessert_bakery_url = 'https://www.costco.com/cakes-cookies.html'
    costco_beverages_url = 'https://www.costco.com/beverages.html'
    costco_breakfast_url = 'https://www.costco.com/breakfast.html'
    costco_candy_url = 'https://www.costco.com/candy.html'
    costco_cheese_url = 'https://www.costco.com/cheese.html'
    costco_coffee_sweeteners_url = 'https://www.costco.com/coffee-sweeteners.html'
    costco_deli_url = 'https://www.costco.com/deli.html'
    costco_kirkland_signature_url = 'https://www.costco.com/kirkland-signature-groceries.html'
    costco_meat_url = 'https://www.costco.com/meat.html'
    costco_organic_url = 'https://www.costco.com/organic-groceries.html'
    costco_pantry_url = 'https://www.costco.com/pantry.html'
    costco_poultry_url = 'https://www.costco.com/poultry.html'
    costco_seafood_url = 'https://www.costco.com/seafood.html'
    costco_snacks_url = 'https://www.costco.com/snacks.html'
    bjs_url = 'https://www.bjs.com/category/food-beverages/3000000000000139980'  # Update to correct BJ's URL

    # Fetch and parse Costco products
    costco_dessert_bakery_data = fetch_all_costco_pages(costco_dessert_bakery_url)
    costco_beverages_data = fetch_all_costco_pages(costco_beverages_url)
    costco_breakfast_data = fetch_all_costco_pages(costco_breakfast_url)
    costco_candy_data = fetch_all_costco_pages(costco_candy_url)
    costco_cheese_data = fetch_all_costco_pages(costco_cheese_url)
    costco_coffee_sweeteners_data = fetch_all_costco_pages(costco_coffee_sweeteners_url)
    costco_deli_data = fetch_all_costco_pages(costco_deli_url)
    costco_kirkland_signature_data = fetch_all_costco_pages(costco_kirkland_signature_url)
    costco_meat_data = fetch_all_costco_pages(costco_meat_url)
    costco_organic_data = fetch_all_costco_pages(costco_organic_url)
    costco_pantry_data = fetch_all_costco_pages(costco_pantry_url)
    costco_poultry_data = fetch_all_costco_pages(costco_poultry_url)
    costco_seafood_data = fetch_all_costco_pages(costco_seafood_url)
    costco_snacks_data = fetch_all_costco_pages(costco_snacks_url)



    # Fetch and parse BJ's products
    bjs_data = fetch_all_bjs_pages(bjs_url)

    # Save Costco data to CSV
    save_to_csv(costco_dessert_bakery_data, 'costco_dessert_bakery.csv')
    save_to_csv(costco_beverages_data, 'costco_beverages.csv')
    save_to_csv(costco_breakfast_data, "costco_breakfast.csv")
    save_to_csv(costco_candy_data, 'costco_candy.csv')
    save_to_csv(costco_cheese_data, 'costco_cheese.csv')
    save_to_csv(costco_coffee_sweeteners_data, 'costco_coffee_sweeteners.csv')
    save_to_csv(costco_deli_data, 'costco_deli.csv')
    save_to_csv(costco_kirkland_signature_data, 'costco_kirkland_signature.csv')
    save_to_csv(costco_meat_data, 'costco_meat.csv')
    save_to_csv(costco_organic_data, 'costco_organic.csv')
    save_to_csv(costco_pantry_data, 'costco_pantry.csv')
    save_to_csv(costco_poultry_data, 'costco_poultry.csv')
    save_to_csv(costco_seafood_data, 'costco_seafood.csv')
    save_to_csv(costco_snacks_data, 'costco_snacks.csv')
    
    # Save BJ's data to CSV
    save_to_csv(bjs_data, 'bjs_food_beverages.csv')


if __name__ == '__main__':
    main()