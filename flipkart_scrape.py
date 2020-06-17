import sys
import io
import csv
import requests
from bs4 import BeautifulSoup

headers = ['Name', 'Pricing', 'Rating']
products = []
prices = []
ratings = []
product_details = []
max_num = sys.maxsize

for i in range(1, max_num):
    url = 'https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy%2C4io&otracker=nmenu_sub_Electronics_0_Mi&page={}'.format(i+1)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    items = soup.findAll('a', href=True, attrs={'class': '_31qSD5'})
    if len(items) == 0:
            break
    for a in items:
        name = a.find('div', attrs={'class': '_3wU53n'})
        price = a.find('div', attrs={'class': '_1vC4OE _2rQ-NK'})
        ratings = a.find('div', attrs={'class': 'hGSR34'})
        url2 = a['href']
        f_url = "https://www.flipkart.com"+ url2
        page2 = requests.get(f_url)
        soup2 = BeautifulSoup(page2.text, "html.parser")
        details=soup2.find(class_="_3WHvuP")

        product_details.append([name.text, price.text, ratings.text,details.text])

        # print(product_details)

    with open("data.csv", "w", encoding="utf-8", newline='') as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerow(headers)
        csv_writer.writerows(product_details)
