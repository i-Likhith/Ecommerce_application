import requests
import bs4
import json
import pprint

class Amazon_Ecommerce:
    ''' Download Amazon Ecommerce Products and convert into Json format'''

    def Ecommerce_url(self,url):
        '''download url content'''
        r = requests.get(url)
        if(r.status_code != 200):
            print('download/requests is failed')
            return 0
        else:
            print("Request Successful")
        print(r.headers['Content-Type'])
        k=bs4.BeautifulSoup(r.content,"html.parser")
        products=k.find_all("div",{"data-component-type":"s-search-result"})
        product_list=[]
        for p in products:
            #extract the product Details and add to Python Dictionary
            name=p.find("h2")
            n=name["aria-label"].strip() if name and 'aria-label' else "N/A"
        
            price=p.find("span",class_="a-price-whole")
            price=price.text.strip() if price else "N/A"

            rating=p.find("span",class_="a-icon-alt")
            rating=rating.text.strip() if rating else "N/A"

            link=p.find("a",class_="a-link-normal")
            link=f"https://amazon.in{link['href']}" if link else "N/A"

            product_list.append({
                "Product Name":n,
                "Price":price,
                "Rating":rating,
                "Link":link
                })
        return product_list

    def convert_json(self,product_list):
        #convert dictionary to Json format
        product_json=json.dumps(product_list,indent=4)

        with open("products.json","w") as json_file:
            json_file.write(product_json)

        print("Products details is saved in products.json")


if __name__=='__main__':
    obj=Amazon_Ecommerce()
    result=obj.Ecommerce_url("https://www.amazon.in/s?k=mobiles")
    obj.convert_json(result)

