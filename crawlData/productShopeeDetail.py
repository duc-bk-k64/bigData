import random
from selenium import  webdriver
from time import  sleep
import mysql.connector
from selenium.webdriver import Keys
from datetime import date

def login(browser,username, password) :
    browser.get("https://shopee.vn/buyer/login")
    sleep(random.randint(3,5))
    usernameEl = browser.find_element("xpath","//*[@id='main']/div/div[2]/div/div/div/div[2]/form/div/div[2]/div[2]/div[1]/input")
    passwordEl = browser.find_element("xpath","//*[@id='main']/div/div[2]/div/div/div/div[2]/form/div/div[2]/div[3]/div[1]/input")
    usernameEl.send_keys(username)
    passwordEl.send_keys(password)
    usernameEl.send_keys(Keys.ENTER)
    sleep(40)

#main
browser = webdriver.Chrome(executable_path="chromedriver.exe")

login(browser,"0336280763","Lan717448")


#connect to mysql database

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="vuduc2001",
  database="shopeeproduct",
  port = 3307
)
mycursor = mydb.cursor()

sql = "SELECT * FROM productdetail "
insertSql = "INSERT INTO productshopeedetail (url,productname,pricebeforediscount,priceafterdiscount,position,sold,rating,category,feedback,discount,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
mycursor.execute(sql)
result= mycursor.fetchall()
k=0
for i in range(len(result)):
    if result[i][0] == "https://shopee.vn/%E3%80%90Giao-H%C3%A0ng-Trong-ng%C3%A0y-%E3%80%91%C4%90%C3%A8n-LED-laser-kh%C3%B4ng-d%C3%A2y-chi%E1%BA%BFu-h%C3%ACnh-%C4%91%E1%BB%99ng-g%E1%BA%AFn-c%E1%BB%ADa-xe-h%C6%A1i-v%E1%BB%9Bi-32-h%E1%BB%8Da-ti%E1%BA%BFt-t%C3%B9y-ch%E1%BB%8Dn-s%E1%BA%A1c-USB-i.321233992.15335215269?sp_atk=6ed37281-0e4d-47d0-90fc-40964eeee8f1&xptdk=6ed37281-0e4d-47d0-90fc-40964eeee8f1":
        k=i
        print(k)
        break


numberofexcept = 0;
for i in range(k+1,len(result)):
    url=result[i]
    try:
        browser.get(url[0])
        sleep(random.randint(4,7))

        productname = url[1]
        position = url[4]
        category = url[5]
        pricebeforeDiscount = browser.find_element("xpath",
                                                   "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div/div/div/div/div[1]").text
        priceafterDiscount = browser.find_element("xpath",
                                                  "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[1]").text
        sold = browser.find_element("xpath",
                                    "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[3]/div[1]").text
        rate = browser.find_element("xpath",
                                    "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[1]/div[1]").text
        feedback = browser.find_element("xpath",
                                               "//*[@id='main']/div/div[2]/div[1]/div/div[1]/div/div[2]/div[3]/div/div[2]/div[2]/div[1]").text
        discount = browser.find_element("xpath",
                                             "//*[@id='main']/div/div[2]/div[1]/div/div[1]/div/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[2]").text
        today = date.today()
        mycursor.execute(insertSql, (
        url[0], productname, pricebeforeDiscount, priceafterDiscount, position, sold, rate, category,feedback,discount,today))
        mydb.commit()

    except:
        try:
            productname = url[1]
            position = url[4]
            category = url[5]
            pricebeforeDiscount = browser.find_element("xpath",
                                                       "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div/div/div/div/div/div").text
            # priceafterDiscount = browser.find_element("xpath",
            #                                           "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[1]").text
            sold = browser.find_element("xpath",
                                        "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[3]/div[1]").text
            rate = browser.find_element("xpath",
                                        "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[1]/div[1]").text
            feedback = browser.find_element("xpath",
                                            "//*[@id='main']/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div[2]/div[2]/div[1]").text
            # discount = browser.find_element("xpath",
            #                                 "//*[@id='main']/div/div[2]/div[1]/div/div[1]/div/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[2]").text
            today = date.today()
            mycursor.execute(insertSql, (
                url[0], productname, pricebeforeDiscount, pricebeforeDiscount, position, sold, rate, category, feedback,
                "0% giam", today))
            mydb.commit()

        except Exception as e:
            numberofexcept = numberofexcept + 1
            print(numberofexcept)
            print(e)
            continue



    # print("Name:"+productname)
    # print("Position:"+position)
    # print("Category:"+category)
    # print("Price before disount:"+pricebeforeDiscount)
    # print("Price after discount:"+priceafterDiscount)
    # print("Sole: "+sold)
    # print("Rate:"+rate)
    # print("Product detail:" +proudctdetail)
    # print("Product describe:"+productdescribe)
    # break

browser.close()
