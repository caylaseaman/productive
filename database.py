import pyodbc 
import pymysql
import mysql.connector
from secrets import user, password, host, database

def get_list():
    cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
    mycursor = cnx.cursor()

    mycursor.execute("SELECT * FROM test")
    myresult = mycursor.fetchall()
    # print(mycursor.description)
    # print(myresult)
    columns = ["id", "description"]
    results = []

    for row in myresult:
      d = dict(zip(columns,row))
      print(d)
      results.append(d)
      
    cnx.close()

  #  print(results)
    return results

def insert_post(content):
  cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
  cursor = cnx.cursor()
  value = content
  query = "INSERT INTO test (description) VALUES (%s)"
  cursor.execute(query,(value,))
 
  print("Inserted",cursor.rowcount,"row(s) of data.")
 
  # cursor.execute("""INSERT INTO test (description)
  #                   VALUES (\"?\")""", content)
  cnx.commit()
  cnx.close()
  # print(results)
   
def delete_post(task_id):
  cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
  cursor = cnx.cursor()
  query = "DELETE FROM test WHERE id=%s"
  cursor.execute(query,(task_id,))
  # results = cursor.execute("""DELETE FROM test WHERE id= ? """, task_id)
  
  cnx.commit()
  cnx.close()
  #   print(results) 

def switch_button(id):
  cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
  cursor = cnx.cursor()
  # query = "SELECT * FROM buttons WHERE description=%s"
  query = "UPDATE buttons SET onoff = 1 - onoff WHERE id=%s"

  cursor.execute(query,(id,))
 
  print(cursor.fetchall())
 
  # cursor.execute("""INSERT INTO test (description)
  #                   VALUES (\"?\")""", content)
  cnx.commit()
  cnx.close()
  # print(results)
  
def get_switch(button_id):
  cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
  mycursor = cnx.cursor()
  
  query = "SELECT * FROM buttons WHERE id=%s"

  mycursor.execute(query,(button_id,))
  myresult = mycursor.fetchall()
  columns = ["id", "description", "onoff"]
  results = []

  for row in myresult:
    d = dict(zip(columns,row))
    results.append(d)
    
  print(results)
  print(results[0]['onoff'])
  cnx.close()
  return str(results[0]['onoff'])

def get_switch_list():
  cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
  mycursor = cnx.cursor()

  mycursor.execute("SELECT * FROM buttons")
  myresult = mycursor.fetchall()

  columns = ["id", "description", "onoff"]
  results = []

  for row in myresult:
    d = dict(zip(columns,row))
    print(d)
    results.append(d)
    
  cnx.close()
  return results