import mysql.connector

dataBase = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='password27',
)

# prepare a cursor object
cursorObject = dataBase.cursor()

# create a db
cursorObject.execute("CREATE DATABASE storefront")

print('DB setup done!')
