import requests
import bs4
import json
import pprint
import os

class Amazon_Ecommerce:
    ''' Download Amazon Ecommerce Products and convert into Json format'''

    def Ecommerce_url(self, url):
        '''download url content'''
        r = requests.get(url)
        if r.status_code != 200:
            print('Download/requests failed')
            return 0
        else:
            print("Request Successful")
        print(r.headers['Content-Type'])
        k = bs4.BeautifulSoup(r.content, "html.parser")  # Parse html document and extracts content
        products = k.find_all("div", {"data-component-type": "s-search-result"})
        product_list = []
        for p in products:
            # Extract the product Details and add to Python Dictionary
            name = p.find("h2")
            n = name["aria-label"].strip() if name and 'aria-label' else "N/A"

            price = p.find("span", class_="a-price-whole")
            price = price.text.strip() if price else "N/A"

            rating = p.find("span", class_="a-icon-alt")
            rating = rating.text.strip() if rating else "N/A"

            link = p.find("a", class_="a-link-normal")
            link = f"https://amazon.in{link['href']}" if link else "N/A"

            product_list.append({
                "Product Name": n,
                "Price": price,
                "Rating": rating,
                "Link": link
            })
        return product_list

    def convert_json(self, product_list):
        '''convert dictionary to Json format'''
        product_json = json.dumps(product_list, indent=4)

        with open("products.json", "w") as json_file:
            json_file.write(product_json)

        print("Product details saved in products.json")

    def run_test_case(self):
        '''Run test case to verify scraping and JSON conversion'''
        print("Running test case...")

        # Step 1: Call Ecommerce_url to scrape product details
        product_list = self.Ecommerce_url("https://www.amazon.in/s?k=mobiles")
        
        # Test if product list is not empty
        if len(product_list) > 0:
            print(f"Scraped {len(product_list)} products successfully.")
        else:
            print("Test failed: No products were scraped.")
            return

        # Step 2: Call convert_json to save the product details to JSON file
        self.convert_json(product_list)

        # Test if the JSON file was created
        if os.path.exists("products.json"):
            print("Test passed: 'products.json' file created successfully.")
        else:
            print("Test failed: 'products.json' file not found.")
            return

        # Test if the JSON file has content
        with open("products.json", "r") as file:
            data = file.read()
            if len(data) > 0:
                print("Test passed: 'products.json' is not empty.")
            else:
                print("Test failed: 'products.json' is empty.")

if __name__ == '__main__':
    # Create an object of Amazon_Ecommerce class and run the test case
    obj = Amazon_Ecommerce()
    obj.run_test_case()
