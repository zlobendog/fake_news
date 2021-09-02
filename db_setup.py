import mysql.connector

# Establishing connection to a database
mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="init_pwd"
  )
cursor = mydb.cursor()
# Creating user for initial run, otherwise does nothing
cursor.execute("CREATE USER if not exists 'fake_news'@'%' IDENTIFIED BY 'f@ke_n3ws';")
# Creating database for initial run, otherwise does nothing
cursor.execute("CREATE DATABASE if not exists news;")
# Grants privileges to created user
cursor.execute("GRANT ALL PRIVILEGES on news.* TO 'fake_news';")

cursor.close()
# Establishing connection with a specific app-level user
mydb = mysql.connector.connect(
  host="mysqldb",
  user="fake_news",
  password="f@ke_n3ws",
  database="news"
)
cursor = mydb.cursor()
# Creating tables for initial run, otherwise does nothing
cursor.execute("CREATE TABLE if not exists news_articles (title VARCHAR(255), article_text VARCHAR(512), prediction BOOLEAN)")
cursor.close()