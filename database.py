import pymysql
from tkinter import messagebox

def connect_database():
    global mycursor, conn
    try:
        conn = pymysql.connect(host='localhost', user='root',password='mrb@2001#mb')
        mycursor = conn.cursor()
    except:
        messagebox.showerror("Error", 'Please check your database connection.')
        return
    
    # CREATING DATABASE
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Employee_data")
    mycursor.execute("USE Employee_data")
    # CREATING TABLE IN DATABASE
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS EMPLOYEE_DATA (
            ID VARCHAR(30),
            NAME VARCHAR(50),
            PHONE VARCHAR(10),
            ROLE VARCHAR(50),
            GENDER VARCHAR(20),
            SALARY DECIMAL(20,2)
        )
    """)


# function for ems.py 
def insert(id, name, phone, role, gender, salary):
    mycursor.execute("INSERT INTO EMPLOYEE_DATA VALUES (%s, %s, %s, %s, %s, %s)", (id, name, phone, role, gender, salary))
    conn.commit()
    # conn.close()

def id_exist(id):
        mycursor.execute('SELECT COUNT(*) FROM employee_data WHERE id = %s', id)
        result = mycursor.fetchone()
        return result[0] > 0

def fetch_employee():
     mycursor.execute('SELECT * FROM employee_data')
     result = mycursor.fetchall()
     return result

def update_employee(id,new_name, new_phone, new_role, new_gender, new_salary):
     mycursor.execute('UPDATE employee_data SET NAME = %s,PHONE =%s,ROLE=%s,GENDER=%s,SALARY=%s WHERE ID =%s',(new_name, new_phone, new_role, new_gender, new_salary, id))
     conn.commit()
     conn.close()

def delete_employee(id):
     mycursor.execute('DELETE FROM employee_data WHERE id = %s', id)
     conn.commit()

def search_employee(option,value):
    query = 'SELECT * FROM employee_data WHERE {} = %s'.format(option)
    mycursor.execute(query, (value,))
    result = mycursor.fetchall()
    return result

def delete_all_records():
     mycursor.execute('TRUNCATE TABLE employee_data')
     conn.commit()


connect_database()