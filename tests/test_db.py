import mysql.connector

mydb = mysql.connector.connect(
    host="mysqldb",
    user="fake_news",
    password="f@ke_n3ws",
    database="news"
)


# Tests availability of the database for app-specific user
def test_database():
    assert mydb.is_connected()
