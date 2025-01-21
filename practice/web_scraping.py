# import bs4
# import requests
# # from bs4 import BeautifulSoup
#
# url = input("Enter your Url: ")
# response = requests.get(url)
#
# filename = "ForeFont_login_html"
# # "html.parser break down the HTML into its constituent elements such as tags, attributes, and text content
# # It creates a parse tree for documents that can be used to extract data from HTML
# bs = bs4.BeautifulSoup(response.text, "html.parser")
# formatted_text = bs.prettify()
#
#
# with open(filename, "w+") as file:  # "w+" if the file does not exist it will create the file
#     file.write(formatted_text)
# print("File has been created!")
#
# # if you want to find any tags in html we will give the tag name
# # tag_name = input("Enter the tag name to check the length: ")
# # tag_len = len(bs.find_all(tag_name))
# # print(f"There are {tag_len} {tag_name} tags ")

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = "https://www.nike.com/w/mens-shoes-nik1zy7ok"
driver.get(url)


def get_price():

    # Use the XPath to locate the element
    shoes_price = driver.find_elements(By.XPATH,
                                       '/html/body/div[4]/div/div/div[2]/div[4]/div/div[5]/div[2]/main/section/div/div[1]/div/figure/div/div[3]')

    if shoes_price:
        return shoes_price[0]  # Return the first element of the list


def get_title():
    # Use the XPath to locate the element
    shoes_title = driver.find_elements(By.XPATH,
                                       "/html/body/div[4]/div/div/div[2]/div[4]/div/div[5]/div[2]/main/section/div/div[2]/div/figure/div/div[1]/div[2]/div[1]")
    if shoes_title:
        return shoes_title[0]  # Return the first element of the list


def get_shoe_info():
    driver.find_element(By.XPATH, '//*[@id="modal-root"]/div/div/div/div/section/div[1]/button').click()
    time.sleep(5)
    titles = driver.find_elements(By.CLASS_NAME, 'product-card__title')
    prices = driver.find_elements(By.CLASS_NAME, 'product-price')

    for title in titles:
        print(title.text)

    for price in prices:
        print(price.text)

    print(len(titles))
    print(len(prices))


get_shoe_info()
driver.quit()

    # for title, price in zip(titles, prices):
    # # if titles and prices:
    #     print(f"Title: {title.text}. Price: {price.text}")
    # print(len(titles))
    # print(len(prices))


get_shoe_info()

