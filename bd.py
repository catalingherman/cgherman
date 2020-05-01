import mysql.connector

# MySQl databses details

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="am"
)
mycursor = mydb.cursor()

# Execute SQL Query =>>>> mycursor.execute("SQL Query")
#mycursor.execute("show tables")

#myresult = mycursor.fetchall()

