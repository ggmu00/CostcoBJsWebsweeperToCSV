
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

# Function to parse BJ's food and beverage products
def parse_bjs_foods(content):

    soup = BeautifulSoup(content, 'html.parser')
    products = []

    for product in soup.find_all('div', class_='w-100'):  # Costco page structure
        name = product.find('p', class_='ProductTitlestyle_ProductTitleStyle-sc-1ypnhsh-0.sBYhJ').text.strip() if product.find('p',
                                                                                       class_='ProductTitlestyle_ProductTitleStyle-sc-1ypnhsh-0.sBYhJ') else 'N/A'
        price_tag = product.find('p', class_='Textstyle_StyledText-sc-1lq8adg-0.eYHhHv.display-price')
        if price_tag:
            # Extract dollars and cents separately if they exist
            dollars = price_tag.find('sup').previous_sibling.strip() if price_tag.find('sup') else ''
            cents = price_tag.find('sup').text.strip() if price_tag.find('sup') else ''
            price = f"${dollars}{cents}"
        else:
            price = 'N/A'

        # Extracting product link (looking for <a> tag with href)
        link_tag = product.find('a', href=True)
        link = link_tag['href'] if link_tag else 'N/A'


        # Add product to the list
        products.append([name, price, link])

    return products

# Function to save the data into a CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Product Name', 'Price', 'Product Link'])
    df.to_csv(filename, index=False)

# Function to handle pagination and fetch all product pages for BJ's
# Function to handle pagination and fetch all product pages for BJ's
def fetch_all_bjs(base_url, max_attempts=100):
    all_products = []
    page_num = 1

    while page_num <= max_attempts:
        print(f"Fetching page {page_num}...")

        # Fetch the page content
        content = fetch_page(base_url)
        products = parse_bjs_foods(content)

        if not products:  # If no products are found, stop
            print("No more products found.")
            break

        # Add products to the final list
        all_products.extend(products)

        # Check if there is a 'Load More' button or pagination link
        soup = BeautifulSoup(content, 'html.parser')

        # You may need to inspect the website and look for correct button or link class
        load_more_button = soup.find('a', {
            'class': 'Buttonstyle__ButtonStyle-sc-i4mtuw-0.gcIsno.load-more-button'})
        if load_more_button:
            print("Found 'Load More' button.")
            page_num += 1  # Continue to next page
        else:
            print("No more 'Load More' button found. Ending the scraping process.")
            break

        # Sleep to avoid hitting the server too quickly
        time.sleep(3)

    return all_products



    # Fetch and parse BJ's products
    bjs_data = fetch_all_bjs(bjs_url)


    # Save BJ's data to CSV
    save_to_csv(bjs_data, 'bjs_food_beverages.csv')