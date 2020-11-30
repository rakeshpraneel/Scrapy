import requests as rq
from bs4 import BeautifulSoup as bs

if __name__ == '__main__':

    # Url of the page from which data has to be collected
    Url_list = ['https://amzn.to/39coCB0','https://amzn.to/3749D9j', 'https://amzn.to/3fuEf83']

    for URL in Url_list:
        #We have to specify the browser agent in header dictionary
        #which we are using otherwise we won't be able to
        #extarct the total code from html.parser
        header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

        #We are storing the response of the request which we passed
        Response = rq.get(URL,headers=header)
        print('The Response of the url: ',Response)
        print("\n")

        #Using beautifulsoup framework to read the content of our response
        #and we are parsing the html code
        soup = bs(Response.content, 'html.parser')
        #print(soup)

        #We are searching for the keyword productTitle from the code
        Product_name = soup.find(id="productTitle").get_text()

        print("The product you are searching for is: ", Product_name.strip())
        print("\n")

        deal=0
        product_availability = 0

        #We are searching for the products price and whether it is in deal or not
        if soup.find(id="priceblock_ourprice"):
            Product_price = soup.find(id="priceblock_ourprice").get_text()
            product_availability = 1
        elif soup.find(id="priceblock_dealprice"):
            product_availability = 1
            deal = 1
            Product_price = soup.find(id="priceblock_dealprice").get_text()

            #The products which has deal price will have a timer for that deal to get end
            #Since the Expiry timer id_name will vay for each product hence we are getting the whole span line
            Expiry_time_seg = str(soup.find("span", {"id": lambda L: L and L.startswith('deal_expiry_timer')}).get_text)
            length=len(Expiry_time_seg)
            post = Expiry_time_seg.find("Ends")
            #Time stamp is obtained from whole string
            Expiry_time = Expiry_time_seg[post:length-8]

        if product_availability == 1:
            if deal == 1:
                print("Special offer is going on for this product!!!")
                print("Price of this product is:",Product_price)
                print("This Deal",Expiry_time)
            else:
                print("Price of this product is:", Product_price)
        else:
            print("Sorry the product is out of stock!!!")

        print(">>>>>>>><<<<<<<<\n")
