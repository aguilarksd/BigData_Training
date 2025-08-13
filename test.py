import mysql.connector
try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="b3e5fdf68",
      database="challenge1"
    )
except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        exit()

mycursor = mydb.cursor()
query = "SELECT * FROM sales"
mycursor.execute(query)
myresult = mycursor.fetchall()

for x in myresult:
  print(x)

