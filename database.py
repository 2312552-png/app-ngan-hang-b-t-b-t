import pymysql


def get_connection():

    conn = pymysql.connect(

        host="mysql-2170da25-dlu-b30a.c.aivencloud.com",

        port=25334,

        user="avnadmin",

        password="AVNS_uwfB8ePynsjV2HyJCSP",

        database="company1",

        ssl={
            "ca": "ca.pem"
        }

    )

    return conn
