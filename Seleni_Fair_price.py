import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.request import urlopen

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

# Web scrapper for infinite scrolling page 
# driver = webdriver.Chrome(executable_path=r"C:\Users\ankur\Downloads\chromedriver_win32\chromedriver.exe")
# driver = webdriver.Chrome()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

Fairprice_data=[]
count=0

# request send to category of fairprice
url = 'https://fairprice.com.sg/categories'
driver.get(url)
html_page = driver.page_source
soup = BeautifulSoup(html_page,'html.parser')
mai = soup.find_all("ul",class_="sc-qg4l23-7 gcQtZV")

for index_1,value_1 in enumerate(mai):
    # category_inp = int(input("Enter a number that you want to extract category items : "))
    # Give input of category that you want to extract data
    for t in range(19):
        if index_1==t:
            All_li_tags = value_1.find_all('li',class_="sc-qg4l23-8 ekvzaK")
            for index_of_li_tag,value_of_li_tag in enumerate(All_li_tags):
                if value_of_li_tag.find('a',class_="sc-qg4l23-9 jYHTwT"):
                    count+=1
            print(count)
            # Loop for finding each category link
            for index_2,value_2 in enumerate(All_li_tags):
                for u in range(count):
                    if index_2==u:
                        category_link = value_2.find('a',class_="sc-qg4l23-9 jYHTwT")['href']
                        base_category_link = f"https://fairprice.com.sg{category_link}"
                        print(base_category_link)
# scroll 
                        print("I am loop of category",t)

                        driver.get(base_category_link)
                        time.sleep(2)  # Allow 2 seconds for the web page to open
                        scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
                        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
                        i = 1

                        while True:
                            # scroll one screen height each time
                            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
                            i += 1
                            time.sleep(scroll_pause_time)
                            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
                            scroll_height = driver.execute_script("return document.body.scrollHeight;")  
                            # Break the loop when the height we need to scroll to is larger than the total scroll height
                            if (screen_height) * i > scroll_height:
                                break


                        # html_page1 = session.get(base_category_link)
                        html_page1 = driver.page_source
                        soup1 = BeautifulSoup(html_page1,'html.parser')

                        # Below code is for finding how many products are available in each category page link
                        try:
                            product_lim = soup1.find('span',class_="sc-1bsd7ul-1 kouteV").text
                            product_limit = int(product_lim[:2])
                        except:
                            product_limit = 50
                        print(product_limit)

                        link_of_div = soup1.find_all('div',class_="sc-1plwklf-0 iknXK product-container")

                        # Loop for finding items from product link
                        for index_3,value_3 in enumerate (link_of_div):
                            for akl in range(product_limit):
                                if index_3 == akl:
                                    print(f"I am loop of Product {akl} of category {t}")
                                    link_of_pro = value_3.find('a',class_="sc-1plwklf-3 bmUXOR")['href']
                                    base_link_of_pro = f"https://fairprice.com.sg{link_of_pro}"

                                    # Below code is used for finding all details of each product
                                    driver.get(base_link_of_pro)
                                    html_page2=driver.page_source
                                    soup2 = BeautifulSoup(html_page2,'html.parser')
                                    try:
                                        price = soup2.find('span',class_="sc-1bsd7ul-1 sc-13n2dsm-5 kxEbZl deQJPo").text
                                    except:
                                        price='None'
                                    try:
                                        name = soup2.find('span',class_="sc-1bsd7ul-1 cZuPIJ").text
                                    except:
                                        name="None"
                                    try:
                                        brand = soup2.find('a',class_="sc-13n2dsm-1 jLtMNk").text
                                    except:
                                        brand="None"
                                    try:
                                        sold_by = soup2.find('div',class_="sc-16yemxd-0 gOtEQZ").text
                                    except:
                                        sold_by='None'
                                    try:
                                        Net = soup2.find('span',class_="sc-1bsd7ul-1 sc-13n2dsm-13 gDxsDx liuneL").text
                                    except:
                                        Net='None'
                                    images = soup2.find_all('li',class_="sc-10zw1uf-14")
                                    img1='None'
                                    img2='None'
                                    img3='None'
                                    img4='None'
                                    for p,image in enumerate(images):
                                        if p==0:
                                            img1 = image.find('img',class_="sc-10zw1uf-11 gyQcYf")['src']
                                        elif p==1:
                                            img2 = image.find('img',class_="sc-10zw1uf-11 gyQcYf")['src']
                                        elif p==2:
                                            img3 = image.find('img',class_="sc-10zw1uf-11 gyQcYf")['src']
                                        elif p==3:
                                            img4 = image.find('img',class_="sc-10zw1uf-11 gyQcYf")['src']
                                    fair_price_data = {
                                        'Product Name':name.strip(),
                                        'Price':price.strip(),
                                        'Net':Net.strip(),
                                        'Brand':brand.strip(),
                                        'IMG1':img1.strip(),
                                        'IMG2':img2.strip(),
                                        'IMG3':img3.strip(),
                                        'IMG4':img4.strip(),
                                        'Sold By':sold_by.strip()
                                    }   
                                    Fairprice_data.append(fair_price_data)
                                    print(name)

                                    with open('Fairprice_data_5.csv','a') as f:
                                        df = pd.DataFrame(Fairprice_data)
                                        df.to_csv('Fair_price_data_5.csv')