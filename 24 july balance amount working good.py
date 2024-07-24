from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Style
import sqlite3
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import numpy as np
import os
import csv
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tkcalendar import Calendar

conn=sqlite3.connect('login.db')

root=Tk()
root.geometry('350x350+450+100')
root.title('Login Window')

global department, bg_image , budget_head, z
z=0

def nmrl_interface(department):
    root1=Toplevel(root)
    root1.title('Interface')
    root1.geometry('975x450+180+100')
        
    def load_image(image_path):
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load image. Error: {e}")
            return None
    
    def submit():
        '''CODE FOR 3RD WINDOW I.E. ITEMWISE BREAKDOWNNH'''
        def forecast_wali_window(p_no,p_details):
            global balance ,g
            a = submit_details(year, department) * 100000
            balance = float(a)
            root2 = Toplevel(root1)
            root2.geometry('975x800+180+20')
            root2.title('Forecast Window')

            '''BUDGET HEAD IS HERE'''
            bh = budget_head
            '''BUDGET HEAD IS HERE'''

            def load_image(image_path):
                try:
                    image = Image.open(image_path)
                    return image
                except Exception as e:
                    messagebox.showerror("Error", f"Unable to load image. Error: {e}")
                    return None

            def clear_input():
                e2.delete(0, END)
                e3.delete(0, END)
                e4.delete(0, END)

            def select_date():
                def set_date():
                    selected_date = cal.get_date()
                    # Convert selected date to dd/mm/yy format
                    day, month, year = selected_date.split('/')
                    formatted_date = f'{day}/{month}/{year[-2:]}'
                    e4.delete(0, END)  # Clear current content
                    e4.insert(0, formatted_date)
                    top.destroy()  # Close the calendar window after selection

                top = Toplevel(root2)
                # Create Calendar with dd/mm/yy format
                cal = Calendar(top, selectmode='day', year=2024, month=7, day=1, date_pattern='dd/mm/yy')
                cal.pack(padx=10, pady=10)
                select_button = Button(top, text="Select Date", command=set_date)
                select_button.pack(pady=10)

            def add_item():
                global balance,add_label,g
                
                if g>1:   
                    add_label.destroy()
                item_name = e2.get()
                amount = float(e3.get())
                expected_cashout = e4.get()
                balance = balance -amount
                g+=1
                add_label=Label(balance_frame, text=f'Remaining Balance: {balance}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                add_label.grid(row=0,column=5)
                

                if item_name and amount and expected_cashout:
                    treeview.insert("", "end", values=(item_name, amount, expected_cashout))
                    clear_input()
                else:
                    messagebox.showwarning("Input Error", "Please fill all fields before adding.")

            def delete_item():
                global balance,add_label,g
                # Get selected item
                selected_item = treeview.selection()
                if selected_item:
                    items = treeview.item(selected_item)
                    val = items['values']
                    if val:
                        value_to_delete=float(val[1])
                    
                    balance=balance+value_to_delete
                    #print(value_to_delete)
                    #print(balance)
                    treeview.delete(selected_item)

                    if g>1:   
                        add_label.destroy()
                    g+=1
                    add_label=Label(balance_frame, text=f'Remaining Balance: {balance}', font=('Times New Roman', 24, 'bold'),fg='blue', bd=6)
                    add_label.grid(row=0,column=5)
                else:
                    messagebox.showwarning("Delete Error", "No item selected to delete.")

            def red_label():
                global e2,e3,e4
                Label(table, text='Budget Head', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=0)
                Label(table, text='Item Name', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=2)
                Label(table, text='Amount', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=4)
                Label(table, text='Expected Cashout', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=6)
    
                Label(table, text=budget_head, font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2, column=0)
    
                e2 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e2.grid(row=2, column=2)
                e3 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e3.grid(row=2, column=4)
                e4 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e4.grid(row=2, column=6)
    
                open_calendar_button = Button(table, text="Open Calendar", command=select_date)
                open_calendar_button.grid(row=2, column=8)

            def list_table():
                global treeview
                add_btn = Button(list_frame, text='Add', width=10, bd=3, command=add_item)
                add_btn.grid(row=0, column=0, padx=40, pady=10, sticky="w")
    
                delete_btn = Button(list_frame, text='Delete Selected', width=15, bd=3, command=delete_item)
                delete_btn.grid(row=0, column=1, padx=40, pady=10, sticky="w")
    
                submit_btn = Button(list_frame, text='Submit', width=10, bd=3, command=submit_data)
                submit_btn.grid(row=0, column=2, padx=40, pady=10, sticky="w")
    
                # Treeview to display added items column-wise
                columns = ("Item Name", "Amount", "Expected Cashout")
                treeview = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode='browse')
                treeview.heading("Item Name", text="Item Name")
                treeview.heading("Amount", text="Amount")
                treeview.heading("Expected Cashout", text="Expected Cashout")
                treeview.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")
    
                # Adjust the column widths
                treeview.column("Item Name", width=200)
                treeview.column("Amount", width=100)
                treeview.column("Expected Cashout", width=150)
    
                # Create a scrollbar
                scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=treeview.yview)
                treeview.configure(yscroll=scrollbar.set)
                scrollbar.grid(row=1, column=4, sticky='ns')
    
                mainloop()
            
            def submit_data():
                global z
                # Create 'data' directory if it doesn't exist
                
                if not os.path.exists('data'):
                    os.makedirs('data')

                # Define file path for CSV
                if z==1:
                    file_path = f'data/{department}_forecast_{year}_Project_Revenue_&_Capital.csv'
                else:
                    file_path = f'data/{department}_forecast_{year}_General_Revenue_&_Capital.csv'

                # Write data to CSV
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Item Name", "Amount", "Expected Cashout"])

                    for row in treeview.get_children():
                        values = treeview.item(row, 'values')
                        writer.writerow(values)

                messagebox.showinfo("Success", f"Data has been saved to {file_path}")

            image_path = 'C:/Users/Administrator/Internship/nmrl_logo.jpg'
            image1 = load_image(image_path)
            if image1:
                image1 = image1.resize((100, 60), Image.LANCZOS)
                bg_image = ImageTk.PhotoImage(image1)

                # Create a canvas to place the image
                canvas = Canvas(root2, width=200, height=200)
                canvas.place(x=0, y=0, relwidth=1, relheight=1)
                canvas.create_image(50, 40, image=bg_image, anchor="center")

            header = Frame(root2, width=1370, bd=4, bg='orange')
            header.place(x=200, y=0)
            Label(header, text=f'{department} {year_og} Forecast Budget: {a:.2f}', font=('Times New Roman', 24, 'bold'), fg='black', bd=6).pack(side=TOP, fill=X)

            #input_frame = Frame(root2, width=1370, bd=4,relief='ridge')
            #input_frame.place(x=0, y=120)

            #number=p_no
            #details=p_details
            
            #Label(input_frame, text=f'{budget_head}', font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=0, column=2)
            if budget_head=='Project Revenue/Capital':
                z=1
                g=1
                input_frame = Frame(root2, width=1370, bd=4,relief='ridge')
                input_frame.place(x=0, y=120)
    
                number=p_no
                details=p_details
                balance_frame = Frame(root2, width=1370, bd=4)
                balance_frame.place(x=250, y=100)
                #balance=submit_details(year, department) * 100000
                add_label=Label(balance_frame,text='',font=('Times New Roman', 1, 'bold'),fg='white')
                add_label.grid(row=0,column=0)
                Label(input_frame,text=f'Project Number:{p_no}',font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=1,column=1)
                Label(input_frame,text=f'Project Details:{p_details}',font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=2,column=1)

                
                
                small_frame= Frame(root2, width=1370, bd=4)
                small_frame.place(x=0,y=210)
                
                Label(small_frame,text='Itemwise Breakdown',font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=3,column=1)
                #Label(input_frame, text='Itemwise Breakdown', font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=1, column=2)
    
                table = Frame(root2, width=1370, bd=4, relief='ridge')
                table.place(x=0, y=260)

                red_label()
                '''Label(table, text='Budget Head', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=0)
                Label(table, text='Item Name', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=2)
                Label(table, text='Amount', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=4)
                Label(table, text='Expected Cashout', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=6)
    
                Label(table, text=budget_head, font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2, column=0)
    
                e2 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e2.grid(row=2, column=2)
                e3 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e3.grid(row=2, column=4)
                
                e4 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e4.grid(row=2, column=6)
    
                open_calendar_button = Button(table, text="Open Calendar", command=select_date)
                open_calendar_button.grid(row=2, column=8)'''
    
                # Frame for the list display and buttons
                list_frame = Frame(root2, width=1370, bd=4, relief='ridge')
                list_frame.place(x=250, y=360)
    
                # Add, clear input fields, and submit buttons
                '''add_btn = Button(list_frame, text='Add', width=10, bd=3, command=add_item)
                add_btn.grid(row=0, column=0, padx=40, pady=10, sticky="w")
    
                delete_btn = Button(list_frame, text='Delete Selected', width=15, bd=3, command=delete_item)
                delete_btn.grid(row=0, column=1, padx=40, pady=10, sticky="w")
    
                submit_btn = Button(list_frame, text='Submit', width=10, bd=3, command=submit_data)
                submit_btn.grid(row=0, column=2, padx=40, pady=10, sticky="w")
    
                # Treeview to display added items column-wise
                columns = ("Item Name", "Amount", "Expected Cashout")
                treeview = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode='browse')
                treeview.heading("Item Name", text="Item Name")
                treeview.heading("Amount", text="Amount")
                treeview.heading("Expected Cashout", text="Expected Cashout")
                treeview.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")
    
                # Adjust the column widths
                treeview.column("Item Name", width=200)
                treeview.column("Amount", width=100)
                treeview.column("Expected Cashout", width=150)
    
                # Create a scrollbar
                scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=treeview.yview)
                treeview.configure(yscroll=scrollbar.set)
                scrollbar.grid(row=1, column=4, sticky='ns')
    
                mainloop()'''
                list_table()
            
            else:
                z=0
                input_frame = Frame(root2, width=1370, bd=4,relief='ridge')
                input_frame.place(x=0, y=120)
                g=1
                number=p_no
                details=p_details
                #small_frame= Frame(root2, width=1370, bd=4)
                #small_frame.place(x=0,y=120)
                balance_frame = Frame(root2, width=1370, bd=4)
                balance_frame.place(x=250, y=80)
                #balance=submit_details(year, department) * 100000
                add_label=Label(balance_frame,text='',font=('Times New Roman', 1, 'bold'),fg='white')
                add_label.grid(row=0,column=0)
                #Label(balance_frame, text=f'Remaining Balance: {balance}', font=('Times New Roman', 24, 'bold'), fg='blue', bd=6).grid(row=0,column=5)
                
                Label(input_frame,text='Itemwise Breakdown',font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=3,column=1)
                #Label(input_frame, text='Itemwise Breakdown', font=('Times New Roman', 18, 'bold'), fg='black', bd=6).grid(row=1, column=2)
    
                table = Frame(root2, width=1370, bd=4, relief='ridge')
                table.place(x=0, y=180)
    
                '''Label(table, text='Budget Head', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=0)
                Label(table, text='Item Name', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=2)
                Label(table, text='Amount', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=4)
                Label(table, text='Expected Cashout', font=('Times New Roman', 16, 'bold'), fg='black', bd=6).grid(row=0, column=6)
    
                Label(table, text=budget_head, font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2, column=0)
    
                e2 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e2.grid(row=2, column=2)
                e3 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e3.grid(row=2, column=4)
                
                e4 = Entry(table, font=('Times New Roman', 14, 'normal'), bd=4)
                e4.grid(row=2, column=6)
    
                open_calendar_button = Button(table, text="Open Calendar", command=select_date)
                open_calendar_button.grid(row=2, column=8)
                '''
                red_label()
    
                # Frame for the list display and buttons
                list_frame = Frame(root2, width=1370, bd=4, relief='ridge')
                list_frame.place(x=250, y=280)
    
                # Add, clear input fields, and submit buttons
                '''add_btn = Button(list_frame, text='Add', width=10, bd=3, command=add_item)
                add_btn.grid(row=0, column=0, padx=40, pady=10, sticky="w")
    
                delete_btn = Button(list_frame, text='Delete Selected', width=15, bd=3, command=delete_item)
                delete_btn.grid(row=0, column=1, padx=40, pady=10, sticky="w")
    
                submit_btn = Button(list_frame, text='Submit', width=10, bd=3, command=submit_data)
                submit_btn.grid(row=0, column=2, padx=40, pady=10, sticky="w")
    
                # Treeview to display added items column-wise
                columns = ("Item Name", "Amount", "Expected Cashout")
                treeview = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode='browse')
                treeview.heading("Item Name", text="Item Name")
                treeview.heading("Amount", text="Amount")
                treeview.heading("Expected Cashout", text="Expected Cashout")
                treeview.grid(row=1, column=0, columnspan=4, pady=10, sticky="ew")
    
                # Adjust the column widths
                treeview.column("Item Name", width=200)
                treeview.column("Amount", width=100)
                treeview.column("Expected Cashout", width=150)
    
                # Create a scrollbar
                scrollbar = Scrollbar(list_frame, orient=VERTICAL, command=treeview.yview)
                treeview.configure(yscroll=scrollbar.set)
                scrollbar.grid(row=1, column=4, sticky='ns')
    
                mainloop()'''
                list_table()

        def submit_details(year,dept_inp):

            global df, departments, X_train, X_test, y_train, y_test, dept_models, dept_rf_models
            df = pd.read_csv('C:/Users/gaura/Desktop/Scatter/NMRL/Latest task/BUDGET_DATASET.csv')
            years = df['FINANCIAL_YR']
            departments = df.columns[1:]  # Exclude the 'Year' column
                    
            # Convert to numpy array for modeling
            X = np.array(years).reshape(-1, 1)  # Years as input feature
                    
            # Split data into training and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, df.iloc[:, 1:], test_size=0.2, random_state=42)
                    
            # Train both linear regression and random forest models for each department
            dept_models = {}
            dept_rf_models = {}
            for dept in departments:
                y = df[dept]
                lin_model = LinearRegression()
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                lin_model.fit(X_train, y_train[dept])
                rf_model.fit(X_train, y_train[dept])
                dept_models[dept] = lin_model
                dept_rf_models[dept] = rf_model

            
            dept_fore = 0
            for dept, model in dept_models.items():
                if dept == dept_inp:
                    rf_model = dept_rf_models[dept]
                    lin_pred = model.predict(np.array(year).reshape(-1, 1))[0]
                    rf_pred = rf_model.predict(np.array(year).reshape(-1, 1))[0]
                    forecast_amount = (lin_pred + rf_pred) / 2
                    dept_fore = round(forecast_amount, 2)
                    return dept_fore

        def project_details(year,department):
            root3=Toplevel(root)
            root3.geometry('400x350+450+100')
            root3.title('Proect Information')
            
            def submit_project():
                p_no=e1.get()
                p_details=e2.get()
                forecast_wali_window(p_no,p_details)
                #submit_details(year,department)
            
            def clear_input():
                e1.delete(0,END)
                e2.delete(0,END)
            
            header = Frame(root3, width=1370, bd=4)
            header.pack(side=TOP, fill=X)
            Label(header,text='Project Details',font=('Times New Roman', 28, 'bold'), fg='black', bg='orange', bd=6, relief='ridge').pack(side=TOP, fill=X)
            
            input_frame= Frame(root3, width=1370, bd=4)
            input_frame.place(x=20,y=100)
            
            Label(input_frame,text='Project No:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=0,column=2)
            e1 = Entry(input_frame, font=('Times New Roman', 14, 'normal'), bd=4)
            e1.grid(row=0,column=4)
            
            Label(input_frame,text='Project Details:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2,column=2)
            e2 = Entry(input_frame, font=('Times New Roman', 14, 'normal'), bd=4)
            e2.grid(row=2,column=4)
            
            btn_frame= Frame(root3, width=1370, bd=4)
            btn_frame.place(x=150,y=180)
            
            sbt_btn = Button(btn_frame, text='Submit', width=10, bd=3, command=submit_project)
            sbt_btn.grid(row=0,column=3)
            
            clear_btn = Button(btn_frame, text='Clear', width=10, bd=3, command=clear_input)
            clear_btn.grid(row=0,column=5)
            
            mainloop()

        def new():
            pass
        year_og = year_var.get()
        year_str = year_og[0:4]
        year = int(year_str)
        budget_head = bh_var.get()

        if budget_head=='Project Revenue/Capital':
            project_details(year,department)
        elif budget_head=='General Revenue/Capital':
            p_no=''
            p_details=''
            forecast_wali_window(p_no,p_details)
        
        
    def clear_input():
        bh_var.set('')
        year_var.set('')
        
    image_path = 'C:/Users/Administrator/Internship/nmrl_logo.jpg'
    image1 = load_image(image_path)
    if image1:
        image1 = image1.resize((100, 60), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(image1)
    
         #Create a canvas to place the image
        canvas = Canvas(root1, width=200, height=200)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        canvas.create_image(50, 40, image=bg_image, anchor="center")
       
    header = Frame(root1, width=1370, bd=4)
    header.place(x=100,y=0)
    dept_text=f'{department} division'
    Label(header,text='NMRL BUDGET FORECAST SYSTEM',font=('Times New Roman', 36, 'bold'), fg='black', bg='orange', bd=6, relief='ridge').pack(side=TOP,fill=X)
    Label(header,text=dept_text,font=('Times New Roman', 28, 'bold'), fg='blue', bd=6).pack(side=TOP,fill=X)
    
    input_frame= Frame(root1, width=1370, bd=4)
    input_frame.place(x=40,y=120)
    
    Label(input_frame,text='FBE Year:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=0,column=2)
    
    # Dropdown menu for department selection
    year_var = StringVar(root1)
    year=['2024-25','2025-26','2026-27','2027-28','2028-29','2029-30']
    year_var.set(year[0])  # Default department selection
    year_menu = OptionMenu(input_frame, year_var, *year)
    year_menu.config(width=25)
    style=Style()
    style.configure('TMenubutton',background='aqua')
    year_menu.grid(row=0,column=4)
    year_var.set('')
    
    
    Label(input_frame,text='Budget Head:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2,column=2)
    bh_var = StringVar(root1)
    bh=['General Revenue/Capital','Project Revenue/Capital']
    bh_var.set(bh[0])  # Default department selection
    bh_menu = OptionMenu(input_frame, bh_var, *bh)
    bh_menu.config(width=25)
    style=Style()
    style.configure('TMenubutton1',background='aqua')
    bh_menu.grid(row=2,column=4)
    
    bh_var.set('')
    
    
    btn_frame= Frame(root1, width=1370, bd=4)
    btn_frame.place(x=150,y=200)
    
    sbt_btn = Button(btn_frame, text='Submit', width=10, bd=3, command=submit)
    sbt_btn.grid(row=0,column=3)
    
    clear_btn = Button(btn_frame, text='Clear', width=10, bd=3, command=clear_input)
    clear_btn.grid(row=0,column=5)
    
    mainloop()
    
def submit():
    department = department_var.get()
    password = e2.get()
    root.destroy()

def clear_input():
    e2.delete(0,END)                                                                    
    department_var.set('')

def login():
    department = department_var.get()
    password = e2.get()

    # Connect to SQLite database
    conn = sqlite3.connect('login.db')
    c = conn.cursor()
    # Retrieve password from database for the selected department
    c.execute('SELECT PASSWORD FROM DEPT_LOGIN WHERE BRANCH_NAME=?', (department,))
    row = c.fetchone()

    if row:
        correct_password = row[0]
        if password == correct_password:
            messagebox.showinfo("Login Successful", f"Welcome to {department}!")
            nmrl_interface(department)
            
        else:
            messagebox.showerror("Login Error", "Incorrect password. Please try again.")
            e2.delete(0,END)
    else:
        messagebox.showerror("Login Error", "Department not found.")

    # Close database connection
    conn.close()

# HEADER FRAME
header = Frame(root, width=1370, bd=4)
header.pack(side=TOP, fill=X)
Label(header,text='Welcome',font=('Times New Roman', 28, 'bold'), fg='black', bg='orange', bd=6, relief='ridge').pack(side=TOP, fill=X)

# SUBHEADER FRAME                                                                               
subtitle = Frame(root, width=1370, bd=4)
subtitle.pack(side=TOP, fill=X)

Label(subtitle,text='Please Login',font=('Times New Roman', 20, 'normal'),bg='white', fg='blue', bd=6).pack(side=TOP, fill=X)

# INPUT FRAME

input_frame= Frame(root, width=1370, bd=4)
input_frame.place(x=40,y=120)

Label(input_frame,text='Login:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=0,column=2)

conn = sqlite3.connect('login.db')
c = conn.cursor()

# Retrieve department names from the database
c.execute('SELECT BRANCH_NAME FROM DEPT_LOGIN')
departments = [row[0] for row in c.fetchall()]

# Close database connection
conn.close()

# Dropdown menu for department selection
department_var = StringVar(root)
department_var.set(departments[0])  # Default department selection
department_menu = OptionMenu(input_frame, department_var, *departments)
department_menu.config(width=25)
style=Style()
style.configure('TMenubutton',background='aqua')
department_menu.grid(row=0,column=4)

Label(input_frame,text='Password:',font=('Times New Roman', 14, 'bold'), fg='black', bd=6).grid(row=2,column=2)
e2 = Entry(input_frame, font=('Times New Roman', 14, 'normal'), bd=4,show='*')
e2.grid(row=2,column=4)

btn_frame= Frame(root, width=1370, bd=4)
btn_frame.place(x=150,y=200)

sbt_btn = Button(btn_frame, text='Submit', width=10, bd=3, command=login)
sbt_btn.grid(row=0,column=3)

clear_btn = Button(btn_frame, text='Clear', width=10, bd=3, command=clear_input)
clear_btn.grid(row=0,column=5)

mainloop()