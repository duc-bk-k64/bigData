import np as np
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
import mysql.connector
import os
import sys
import numpy as np
from pyspark.sql.types import StructType

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="vuduc2001",
  database="shopeeproduct",
  port = 3307
)
mycursor = mydb.cursor()
sql = "SELECT * FROM productshopeedetail "
mycursor.execute(sql)
result= mycursor.fetchall()
spark = SparkSession.builder\
        .master("local[*]")\
        .appName('Shopee')\
        .getOrCreate()
productSchema = StructType() \
                    	.add("url", "string")\
                    	.add("name", "string")\
                    	.add("price_before_discount", "string")\
                    	.add("price_after_discount", "string")\
                        .add("position", "string")\
                        .add("sold", "string")\
                        .add("rate", "string")\
                        .add("type", "string")\
                        .add("time", "timestamp")\
                        .add("feedback", "string")\
                        .add("id", "integer")\
                        .add("discount", "string")\
#push data to hdfs

df=spark.createDataFrame(result,schema=productSchema)
df.show()
df.write.format("csv").mode('overwrite').save("hdfs://localhost:9000/shopeeProduct.csv")
# read data from hdfs
data=spark.read.csv("hdfs://localhost:9000/shopeeProduct.csv",schema=productSchema)
product = data.select('url','name','price_before_discount','price_after_discount','sold','rate','type','discount','feedback','id')
product.createOrReplaceTempView("product")
productFillter = spark.sql("SELECT * FROM product ")
productFillter.show()
