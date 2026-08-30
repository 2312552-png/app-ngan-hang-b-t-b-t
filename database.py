import pymysql


def get_connection():

    conn = pymysql.connect(

        host="mysql-3a5ef2bc-binhquytoc.a.aivencloud.com",

        port=14483,

        user="avnadmin",

        password="AVNS_TX2oBXmTGGjXba6p7j1",

        database="company",

        ssl={
            "ca": "ca.pem"
        }

    )

    return conn
