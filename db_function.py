# Importing Necessary Libraries for SQL Connectivity
import mysql.connector

# Database Initial Code
'''
CREATE database h1B;

USE h1b;

CREATE TABLE users
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(100) NOT NULL UNIQUE,
    user_password VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE tuples
(
    user_id INT,
    employer_name VARCHAR(80) NOT NULL,
    soc_name VARCHAR(50) NOT NULL,
    worksite VARCHAR(30) NOT NULL,
    prevailing_wage DOUBLE NOT NULL,
    fulltime_position VARCHAR(1) NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);
'''

# Code for Database Connectivity for new user signup
def new_user_signup(user_name, password):

    mydb = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="76876462sS$", 
        database="h1b"
    )

    mycursor = mydb.cursor()

    # query = f"INSERT INTO users(user_name, user_password) VALUES({user_name},{password})"

    val = (user_name, password)
    mycursor.execute("INSERT INTO users(user_name,user_password) VALUES(%s,%s)", val)
    mydb.commit()
    mydb.close()


# Code for Database Connectivity for record inserting
def new_record(user_id,employer_name,soc_name,worksite,prevailing_wage,fulltime_position,status):
    import mysql.connector
    mydb = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="76876462sS$", 
        database="h1b"
    )

    mycursor = mydb.cursor()

    val = (user_id,employer_name,soc_name,worksite,prevailing_wage,fulltime_position,status)
    mycursor.execute("INSERT INTO tuples(user_id,employer_name,soc_name,worksite,prevailing_wage,fulltime_position,status) VALUES(%s,%s,%s,%s,%s,%s,%s)", val)
    mydb.commit()
    mydb.close()
    

# Code for Database Connectivity for fetching records from database
def fetch_records():
    import mysql.connector
    mydb = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="76876462sS$", 
        database="h1b"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM tuples")
    records = mycursor.fetchall()

    for record in records:
        print(record)
    mydb.close()
