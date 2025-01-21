import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.nike.com/t/free-run-flyknit-2018-mens-road-running-shoes-RRT9elMk/942838-101')


soup = BeautifulSoup(response.text, 'html.parser')
# titles = soup.find_all('h1')               # headers and title of the page
# for title in titles:                       #find to fetch one and find_all to fetch all
#     print(title.text)

all_links = soup.find_all('a')
for links in all_links:
    print(links.text)                       # all the "a" tags of hte page
    print(links.get('href'))                 # all the links of the page

# first_link = all_links[0]                  # first 'a' tag and link of the page
# print("First 'a' tag of the page ", first_link.text)
# print("First link of the page ", first_link.get('href'))
