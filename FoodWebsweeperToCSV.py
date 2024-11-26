import glob
import os

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


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


# Function to handle pagination and fetch all product pages for Costco
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


# Function to split the item description and item count
def separate_item_count_from_csv(csv_file):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Function to separate item description and item count using regex
    def separate_item_count(item_description):
        # Use regex to search for the pattern 'number followed by "Count" or "Pack"'
        match = re.search(r'(\d+[-]?\d*)\s*(Count|count|Pack|pack)', item_description)

        if match:
            # Extract the item name and count
            item_name = item_description[:match.start()].strip()
            item_count = match.group(0)
            return item_name, item_count
        else:
            # If no match is found, return the original item description and None
            return item_description, None

    # Apply the method to separate item descriptions and counts
    df[['Product', 'Count']] = df['Product Name'].apply(lambda x: pd.Series(separate_item_count(x)))

    # Keep only the columns we need: item_name and item_count
    df = df[['Product', 'Count', 'Price']]

    # Save the updated DataFrame to a new CSV file
    updated_csv = csv_file.replace('.csv', '_updated.csv')  # Save as a new CSV with '_updated' in the name
    df.to_csv(updated_csv, index=False)

    os.remove(csv_file)

    # Return the updated CSV file path
    return updated_csv



# Main function to run the scraper
def main():
    # Dictionary of Costco product categories and their corresponding URLs
    costco_urls = {
        'beverages': 'https://www.costco.com/beverages.html',
        'breakfast': 'https://www.costco.com/breakfast.html',
        'candy': 'https://www.costco.com/candy.html',
        'cheese': 'https://www.costco.com/cheese.html',
        'coffee_sweeteners': 'https://www.costco.com/coffee-sweeteners.html',
        'deli': 'https://www.costco.com/deli.html',
        'dessert_bakery': 'https://www.costco.com/cakes-cookies.html',
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
        csv_file = f'CSV_Output/costco_{category}.csv'
        save_to_csv(data, csv_file)  # Save to CSV
        # Separate item count and save it to a new CSV
        updated_csv = separate_item_count_from_csv(csv_file)
        print(f"Processed and updated: {updated_csv}")

    csv_files = glob.glob("CSV_Output/*.csv")

    # Read each CSV file and store in a list
    dfs = [pd.read_csv(csv_file) for csv_file in csv_files]

    # Concatenate all DataFrames
    concatenated_df = pd.concat(dfs, axis=0, ignore_index=True)

    #   Save the concatenated DataFrame to a new CSV file
    concatenated_df.to_csv('concatenated_output.csv', index=False)

if __name__ == '__main__':
    main()
