from customtkinter import *
from PIL import Image 
from tkinter import ttk, messagebox
import database 

# Functions
def delete_all_records():
    result = messagebox.askyesno('Confirm','Do you want to delete all record ?')
    if result:
        database.delete_all_records()
        messagebox.showinfo('sucess','All data deleted sucessfully.')
        treeview_data()
        clear()
        return 
    else:
        pass

def show_all():
    treeview_data()
    search_Entry.delete(0,END)
    Search_Box.set('Search By')


def search_employee():
    if search_Entry.get() == '':
        messagebox.showerror('Error', 'Enter a value to search.')
        return
    if Search_Box.get() == 'Search By':
        messagebox.showerror('Error', 'Please select a valid search option.')
        return
    # Map user-friendly column names to actual database column names
    allowed_columns = {
        'Employee_Id' : 'id',
        'Employee_Name' :'name',
        'Contact' : 'phone',
        'Role' : 'role',
        'Gender' : 'gender',
        'Salary' : 'salary'
        }
    option = Search_Box.get()
    if option not in allowed_columns:
        messagebox.showerror("Error", "Invalid search option.")
        return
    corrected_option = allowed_columns[option]
    # Fetch data
    search_data = database.search_employee(corrected_option, search_Entry.get())

    tree.delete(*tree.get_children())
    for employee in search_data:
        tree.insert('', END, values=employee) 
    
    # Show a message if no results are found
    if not search_data:
        messagebox.showinfo("Not Found", "No employee found with that search value.")
        return search_data
    # print(search_data)  # Debugging

    
def delete_employee():
    selected_data = tree.selection()
    if not selected_data:
        messagebox.showerror('Error','Select data to delete')
    else:
        database.delete_employee(id_Entry.get())
        treeview_data()
        clear()
        messagebox.showerror('Error','Data is deleted.')

def update_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error','select data to update.')
        return
    
    employee_id = id_Entry.get().strip()
    name = name_Entry.get().strip()
    phone = phone_Entry.get().strip()
    role = role_Entry.get().strip()
    gender = gender_Entry.get().strip()
    salary = Salary_Entry.get().strip()

    if not employee_id or not name or not phone or not role or not gender or not salary:
        messagebox.showerror('Error', 'All fields must be filled before updating.')
        return
    
    if not phone.isdigit() or len(phone) < 10:
        messagebox.showerror('Error', 'Phone number must be at least 10 digits long.')
        return
    
    if not salary.isdigit():
        messagebox.showerror('Error', 'Salary must be a valid number.')
        return

    database.update_employee(employee_id, name, phone, role, gender, salary)
    treeview_data()
    clear()
    messagebox.showinfo('Sucess','Employee Data updated successfully.')
        

def selection(info):
    selection_item = tree.selection()
    if selection_item:
        row = tree.item(selection_item)['values']
        clear()
        id_Entry.insert(0,row[0])
        name_Entry.insert(0,row[1])
        phone_Entry.insert(0,row[2])
        role_Lable.setvar(row[3])
        gender_Lable.setvar(row[4])
        Salary_Entry.insert(0,row[5])
        # print(row)

def clear():#(value=False):        # commented alls are new button function
    # if value:
        # tree.selection_remove(tree.focus())
    id_Entry.delete(0,END)
    name_Entry.delete(0,END)
    phone_Entry.delete(0,END)
    role_Lable.setvar('Web Developer')
    gender_Lable.setvar('Female')
    Salary_Entry.delete(0,END)

def treeview_data():
    employees = database.fetch_employee()
    tree.delete(*tree.get_children())  # Clear the treeview and new records will be inserted
    for employee in employees:
        tree.insert('', END, values=employee)

def add_employee():
    if id_Entry.get() == '' or name_Entry.get() == '' or phone_Entry.get() == '' or Salary_Entry.get() == '':
        messagebox.showerror("Error", 'All fields are required.')

    elif database.id_exist(id_Entry.get()):
        messagebox.showerror("Error", 'ID Already Exists.')

    elif len(phone_Entry.get()) < 10:
        messagebox.showinfo('warning','add phone number at least 10 digit')
        return
    
    else:
        database.insert(id_Entry.get(), name_Entry.get(), phone_Entry.get(), role_Entry.get(), gender_Entry.get(), Salary_Entry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Sucess','Data Inserted Sucessfully.')


# GUI
window = CTk()
window.geometry("938x582+100+100") #1536x864  938x582
window.resizable(True,True)
window.title("Employee Management System")
window.configure(fg_color='#161C30')

logo = CTkImage(Image.open("Untitled design.png"),size=(1550,150)) # adjest the image size and change teh image size 
image_logo = CTkLabel(window,image=logo,text="")
image_logo.grid(row=0, column=0, columnspan=2)

# Left Frame Info.
leftFrame = CTkFrame(window,fg_color='#161C30')
leftFrame.grid(row=1, column=0, padx= 10 ,pady = 10)

# Id lable and entry
id_Lable=CTkLabel(leftFrame,text='Employee_Id',font=('arial',18,'bold'),text_color='White')
id_Lable.grid(row=0, column=0,padx=20,pady=15)
id_Entry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
id_Entry.grid(row=0,column=1)

# name lable and entry
name_Lable=CTkLabel(leftFrame,text='Employee_Name',font=('arial',18,'bold'),text_color='White')
name_Lable.grid(row=1, column=0,padx=20,pady=15)
name_Entry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
name_Entry.grid(row=1,column=1)

# phone lable and entry
phone_Lable=CTkLabel(leftFrame,text='Contact',font=('arial',18,'bold'),text_color='White')
phone_Lable.grid(row=2, column=0,padx=20,pady=15)
phone_Entry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
phone_Entry.grid(row=2,column=1)

# role lable and entry
role_Lable=CTkLabel(leftFrame,text='Role',font=('arial',18,'bold'),text_color='White')
role_Lable.grid(row=3, column=0,padx=20,pady=15)
Role=['Web Developer','Software Developer','Tester','Manager','HR','Accountant','Business Analyst','Data Scientist','Designer','Network Engineer ','Technical Support','UX/UI Designer']
role_Entry=CTkComboBox(leftFrame,values=Role,font=('arial',15,'bold'),width=180,state='readonly')
role_Entry.grid(row=3,column=1)
role_Entry.set(Role[0])

# gender lable and entry
gender_Lable=CTkLabel(leftFrame,text='Gender',font=('arial',18,'bold'),text_color='White')
gender_Lable.grid(row=4, column=0,padx=20,pady=15)
Gender=['Female','Male','Other']
gender_Entry=CTkComboBox(leftFrame,values=Gender,font=('arial',15,'bold'),width=180,state='readonly')
gender_Entry.grid(row=4,column=1)
gender_Entry.set(Gender[0])

# Salary lable and entry
Salary_Lable=CTkLabel(leftFrame,text='Salary',font=('arial',18,'bold'),text_color='White')
Salary_Lable.grid(row=5, column=0,padx=20,pady=15)
Salary_Entry=CTkEntry(leftFrame,font=('arial',15,'bold'),width=180)
Salary_Entry.grid(row=5,column=1)

# Right Frame Info.
rightFrame = CTkFrame(window)
rightFrame.grid(row=1, column=1 , padx= 0.1 ,pady = 15)

# Search Box and Entry
Search_option=['Employee_Id','Employee_Name','Contact','Role','Gender','Salary']
Search_Box=CTkComboBox(rightFrame,values=Search_option,width=180,state='readonly')
Search_Box.grid(row=0,column=0)
Search_Box.set('Search By')

search_Entry=CTkEntry(rightFrame)
search_Entry.grid(row=0,column=1)

# Search Button
Search_Button = CTkButton(rightFrame,text='Search',cursor='hand2',width=100,command=search_employee)
Search_Button.grid(row=0,column=2)

# Show all Button
Show_all_Button = CTkButton(rightFrame,text='Show All Employees',cursor='hand2',width=100,command=show_all)
Show_all_Button.grid(row=0,column=3,pady=5)

tree=ttk.Treeview(rightFrame,height=30)
tree.grid(row=1,column=0,columnspan=4)

tree['columns'] = ('Employee_Id', 'Employee_Name', 'Contact', 'Role', 'Gender', 'Salary')
tree.heading('Employee_Id', text='Employee_Id')
tree.heading('Employee_Name', text='Employee_Name')
tree.heading('Contact', text='Contact')
tree.heading('Role', text='Role')
tree.heading('Gender', text='Gender')
tree.heading('Salary', text='Salary')

tree.config(show='headings')
tree.column('Employee_Id', anchor=CENTER, width=140)
tree.column('Employee_Name', anchor=CENTER, width=160)
tree.column('Contact', anchor=CENTER, width=160)
tree.column('Role', anchor=CENTER, width=160)
tree.column('Gender', anchor=CENTER, width=100)
tree.column('Salary', anchor=CENTER, width=100)

# Tree View style 
style = ttk.Style()

style.configure("Treeview.Heading",font=('arial',13,'bold'))
style.configure("Treeview",font=('arial',14,'bold'),background='#161C30',rowheight=20,foreground='white')

scroll_bar = ttk.Scrollbar(rightFrame,orient=VERTICAL,command=tree.yview)
scroll_bar.grid(row=1,column=4,sticky='ns')
# scrollbar will change according data
tree.config(yscrollcommand=scroll_bar.set)


button_frame = CTkFrame(window,fg_color='#161C30')
button_frame.grid(row=2,column=0,columnspan = 2)

# newButton = CTkButton(button_frame,text=('New Employee'),font=('arial',15,'bold'),width=160,corner_radius=15,command=lambda:clear(True))
# newButton.grid(row=0,column=0,padx = 5, pady = 5)

addButton = CTkButton(button_frame,text=('Add Employee'),font=('arial',15,'bold'),width=160,corner_radius=15,command = add_employee)
addButton.grid(row=0,column=1,padx = 5,pady = 5)

updateButton = CTkButton(button_frame,text=('Update Employee'),font=('arial',15,'bold'),width=160,corner_radius=15,command=update_employee)
updateButton.grid(row=0,column=2,padx = 5,pady = 5)

deleteButton = CTkButton(button_frame,text=('Delete Employee'),font=('arial',15,'bold'),width=160,corner_radius=15,command=delete_employee)
deleteButton.grid(row=0,column=3,padx = 5,pady = 5)

delete_all_Button = CTkButton(button_frame,text=('Delete All'),font=('arial',15,'bold'),width=160,corner_radius=15,command=delete_all_records)
delete_all_Button.grid(row=0,column=4,padx = 5,pady = 5)

treeview_data()

window.bind('<ButtonRelease>',selection )

window.mainloop()
