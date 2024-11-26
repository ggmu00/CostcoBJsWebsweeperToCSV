
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

    for product in soup.find_all('div', class_='caption link-behavior'):  # Costco page structure
        name = product.find('span', class_='description').text.strip() if product.find('span',
                                                                                       class_='description') else 'N/A'
        price = product.find('div', class_='price').text.strip() if product.find('div', class_='price') else 'N/A'
        link = product.find('a', href=True)['href'] if product.find('a', href=True) else 'N/A'

        products.append([name, price, link])

    return products

# Function to save the data into a CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Product Name', 'Price', 'Product Link'])
    df.to_csv(filename, index=False)


# Function to handle pagination and fetch all product pages for Costcodef fetch_all_costco_pages(base_url, max_pages=10):
def fetch_all_costco_pages(base_url, max_pages=100):
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




# Main function to run the scraper
def main():
    # Dictionary of Costco product categories and their corresponding URLs
    costco_urls = {
        'dessert_bakery': 'https://www.costco.com/cakes-cookies.html',
        'beverages': 'https://www.costco.com/beverages.html',
        'breakfast': 'https://www.costco.com/breakfast.html',
        'candy': 'https://www.costco.com/candy.html',
        'cheese': 'https://www.costco.com/cheese.html',
        'coffee_sweeteners': 'https://www.costco.com/coffee-sweeteners.html',
        'deli': 'https://www.costco.com/deli.html',
        'kirkland_signature': 'https://www.costco.com/kirkland-signature-groceries.html',
        'meat': 'https://www.costco.com/meat.html',
        'organic': 'https://www.costco.com/organic-groceries.html',
        'pantry': 'https://www.costco.com/pantry.html',
        'poultry': 'https://www.costco.com/poultry.html',
        'seafood': 'https://www.costco.com/seafood.html',
        'snacks': 'https://www.costco.com/snacks.html'
    }

    # Iterate over the URLs, fetch the data, and save it to CSV
    for category, url in costco_urls.items():
        data = fetch_all_costco_pages(url)  # Fetch the data
        save_to_csv(data, f'costco_{category}.csv')  # Save to CSV with the category name


if __name__ == '__main__':
    main()
