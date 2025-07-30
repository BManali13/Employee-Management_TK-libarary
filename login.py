from customtkinter import * # customtkinter library for custom widgets and themse 
from PIL import Image # pillow library for imag processing
from tkinter import messagebox # tkinter library for message box for showing error messages

def login():
    if username.get() == '' or password.get() == '' :
        messagebox.showerror('Error','Please fill all the fields')
    elif username.get() == 'admin' and password.get() == '123':      
        messagebox.showinfo('Sucessful','Login Sucessful')
        root.destroy()
        import ems # imprting the ems file (Emplyee management system)
    else:
        print('Error',"Wrong Credentials")    


root = CTk()

root.geometry("1500 x 500") #1536x864
root.resizable(True,True)
root.title("Login Page")
image = CTkImage(Image.open("login.jpg"),size=(1536 ,864))
imageLable = CTkLabel(root,image=image,text="")
imageLable.place(x=0,y=0)

Heading = CTkLabel(root,text='Employee Management System',bg_color='#fffafd',font= ('Goudy Old Style',30,'bold'),text_color='Black')
Heading.place(x=80,y=100)

username = CTkEntry(root,placeholder_text='Enter Your Username',width=180)
username.place(x=150,y=150)

password = CTkEntry(root,placeholder_text='Enter Your Password',width=180,show='*')
password.place(x=150,y=200)

loginbutton = CTkButton(root,text='Login',cursor='hand2',command=login)
loginbutton.place(x=160,y=250)

root.mainloop()