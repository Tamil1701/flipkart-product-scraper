import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def scrape_flipkart_product_data(product_name, pages=5):
    products = []
    for page in range(1, pages+1):
        flipkart_url = f"https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}"
        print(f"Scraping page {page}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(flipkart_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = soup.find_all('div', {'class': '_1AtVbE'})
        for result in results:
            name_tag = result.find('a', {'class': 's1Q9rs'})
            price_tag = result.find('div', {'class': '_30jeq3'})
            rating_tag = result.find('div', {'class': '_3LWZlK'})
            if name_tag and price_tag:
                name = name_tag.text.strip()
                price = price_tag.text.strip()
                rating = rating_tag.text.strip() if rating_tag else None
                product = {'Name': name, 'Price': price, 'Rating': rating}
                products.append(product)
    return products

def main():
    product_name = input("Enter the product name: ")
    flipkart_products = scrape_flipkart_product_data(product_name)

    if flipkart_products:
        # Convert to DataFrame
        df = pd.DataFrame(flipkart_products)

        # Sort by rating and price
        df['Price'] = df['Price'].str.replace('₹', '').str.replace(',', '').astype(float)
        df['Rating'] = df['Rating'].astype(float)
        df_sorted = df.sort_values(by=['Rating', 'Price'], ascending=[False, True])

        # Export to CSV
        csv_name = input("Enter the CSV file name to save the data: ")
        df_sorted.to_csv(f'{csv_name}.csv', index=False)
        print(f"Data exported to {csv_name}.csv")

        # Display results in console
        print("Flipkart Products:")
        print(df_sorted)

        # Display bar graph
        plt.figure(figsize=(10, 6))
        plt.bar(df_sorted['Name'], df_sorted['Price'], color='skyblue', label='Price')
        plt.bar(df_sorted['Name'], df_sorted['Rating'], color='orange', label='Rating')
        plt.xlabel('Product')
        plt.ylabel('Price / Rating')
        plt.title('Product Prices and Ratings on Flipkart')
        plt.xticks(rotation=90)
        plt.legend()
        plt.show()
    else:
        print("No products found for the given name.")

if __name__ == "__main__":
    main()
