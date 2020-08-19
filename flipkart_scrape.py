import sys
import io
import csv
import requests
from bs4 import BeautifulSoup
import mysql.connector

mydb = mysql.connector.connect(host="localhost",user="monika",passwd="1234",database="flipkart")

headers = ['Name', 'Pricing', 'Rating','detalis','full_description']
products = []
prices = []
ratings = []
product_details = []

max_num = sys.maxsize
for i in range(0, max_num):
    url = 'https://www.flipkart.com/mobiles/mi~brand/pr?sid=tyy%2C4io&otracker=nmenu_sub_Electronics_0_Mi&page={}&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock'.format(i+1)
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
        f_url = "https://www.flipkart.com" + url2
        page2 = requests.get(f_url)
        soup2 = BeautifulSoup(page2.text, "html.parser")
        details = soup2.find(class_="_3WHvuP")
        table=soup2.find('table')
        full_description=[]
        table_rows = table.find_all('tr')

        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text.encode('utf-8') for i in td]
            full_description.append(row)
        
        mycursor = mydb.cursor()
        sql = "INSERT INTO Product_Data(Name, Pricing, Rating,Details,Description) VALUES (%s,%s,%s,%s,%s)"
        val = (str(name.text), str(price.text), str(ratings.text), str(details.text),str(full_description))
        mycursor.execute(sql, val)

        mydb.commit()

print(mycursor.rowcount, "record inserted.")

    
# with open("data.csv", "w", encoding="utf-8", newline='') as fp:
#     csv_writer = csv.writer(fp)
#     csv_writer.writerow(headers)
#     csv_writer.writerows(product_details)
