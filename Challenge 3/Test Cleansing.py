import sqlite3 as sq3
import csv
import pandas as pd

conn = sq3.connect('data/abusive_challenge.db')
conn = sq3.connect('data/data_challenge.db')
conn = sq3.connect('data/new_kamusalay_challenge.db')

cursor = conn.cursor()

sql = "CREATE TABLE IF NOT EXISTS ABUSIVE(teks CHAR(20) NOT NULL)"
cursor.execute(sql)

sql = "CREATE TABLE IF NOT EXISTS ALAY(teks_alay CHAR(100) NOT NULL, teks_baku CHAR(100) NOT NULL)"
cursor.execute(sql)


sql = "DELETE FROM ABUSIVE"
cursor.execute(sql)

sql = "DELETE FROM ALAY"
cursor.execute(sql)

# masukkan data csv kedalam table abusive
file = open('data/abusive.csv')
contents = csv.reader(file)
insert_records = "INSERT INTO ABUSIVE (teks) VALUES(?)"
cursor.executemany(insert_records, contents)


# masukkan data csv kedalam table alay
file = open('data/new_kamusalay.csv')
contents = csv.reader(file)
insert_records = "INSERT INTO ALAY (teks_alay,teks_baku) VALUES(?,?)"
cursor.executemany(insert_records, contents)


# cek isi tabel abusive
select_all = "SELECT * FROM ABUSIVE"
rows_abusive = cursor.execute(select_all).fetchall()


# menampilkan data yg sudah diinsert
df_abusive = pd.read_sql_query("select * from ABUSIVE", conn)
df_alay = pd.read_sql_query("select * from ALAY", conn)


# commit perubahan
conn.commit()

#tutup koneksi
conn.close()

df_abusive

dict_alay = dict(zip(df_alay['teks_alay'],df_alay['teks_baku']))
bool('asdsad' in dict_alay)
df_alay

try:
    # Making a connection between sqlite3
    # database and Python Program
    sqliteConnection = sq3.connect('data/abusive_challange.db')
     
    # If sqlite3 makes a connection with python
    # program then it will print "Connected to SQLite"
    # Otherwise it will show errors
    print("Connected to SQLite")
 
    # Getting all tables from sqlite_master
    sql_query = """SELECT name FROM sqlite_master
    WHERE type='table';"""
 
    # Creating cursor object using connection object
    cursor = sqliteConnection.cursor()
     
    # executing our sql query
    cursor.execute(sql_query)
    print("List of tables\n")
     
    # printing all tables list
    print(cursor.fetchall())
 
except sq3.Error as error:
    print("Failed to execute the above query", error)
     
# finally:
   
#     # Inside Finally Block, If connection is
#     # open, we need to close it
#     if sqliteConnection:
         
#         # using close() method, we will close
#         # the connection
#         sqliteConnection.close()
         
#         # After closing connection object, we
#         # will print "the sqlite connection is
#         # closed"
#         print("the sqlite connection is closed")

df_data = pd.read_csv('data/data.csv', encoding="latin-1")
df_data

df_data[['Tweet']]