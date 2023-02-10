import math

import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="vuduc2001",
  database="shopeeproduct",
  port = 3307
)
mycursor = mydb.cursor()
insertSql = "INSERT INTO productshopeedetail (url,productname,pricebeforediscount,priceafterdiscount,position,sold,rating,category,feedback,discount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

# read by default 1st sheet of an excel file
df = pd.read_csv('D:\Downloads\Sendo_Bigdata.csv')
df = df.reset_index()  # make sure indexes pair with number of rows
# print(df)
for index, row in df.iterrows():
    try:
        url = row['URL']
        productname = row['productname']
        pricebeforediscount =str(row['pricebeforediscount']).replace("đ","")
        priceafterdiscount = str(row['priceafterdiscount']).replace("đ","")
        position = row['position']
        sold = row['Sold']
        rating = row['Rating']
        category = row['Category']
        feedback = row['Feedback']
        discount = float(row['Discount'].replace("%",""))*-1
        date = row['Date']
        if(math.isnan(discount)):
            discount= 0
        mycursor.execute(insertSql, (
            url, productname, pricebeforediscount, priceafterdiscount, position, sold, rating, category, feedback,
            discount))
        mydb.commit()
    except Exception as e:
        print(e)
        continue



# print(dataframe1)