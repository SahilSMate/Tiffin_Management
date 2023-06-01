import customtkinter as ctk
import mysql.connector as m
from tkinter import ttk
from datetime import datetime

mydb=m.connect(host="localhost",user="root",password="vivalasvegas",database="myproject")
cursor = mydb.cursor()
cursor.execute('select * from customer')
result = cursor.fetchall()
field_names = [i[0] for i in cursor.description]

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = ctk.CTk()
root.geometry('800x550')
root.title('NANDA MADAM TIFFIN')

#########FRAMES#######
cust_frame = ctk.CTkFrame(master=root)
order_frame = ctk.CTkFrame(master=root)
bill_frame = ctk.CTkFrame(master=root)
tmenu_frame = ctk.CTkFrame(master=root)
###################

####### FUNCTIONS FOR MENU FRAME #############
def cust_button():
    cust_frame.pack(expand = True,fill='both')
    order_frame.pack_forget()
    bill_frame.pack_forget()
    tmenu_frame.pack_forget()


def order_button():
    order_frame.pack(expand = True,fill='both')
    cust_frame.pack_forget()
    bill_frame.pack_forget()
    tmenu_frame.pack_forget()

def b_button():
    bill_frame.pack(expand = True,fill='both')
    cust_frame.pack_forget()
    order_frame.pack_forget()
    tmenu_frame.pack_forget()

def m_button():
    tmenu_frame.pack(expand = True,fill='both')
    cust_frame.pack_forget()
    order_frame.pack_forget()
    bill_frame.pack_forget()
############################



menu_frame = ctk.CTkFrame(master=root)
# menu_frame.pack(side= 'left',expand=True,fill='y',padx=0)
menu_frame.pack(side='left',fill='y',padx = 5)

customers_button = ctk.CTkButton(master=menu_frame,text='CUSTOMERS',command=cust_button,corner_radius=0)
customers_button.pack(pady=10)

orders_button = ctk.CTkButton(master=menu_frame,text='ORDERS',command=order_button,corner_radius=0)
orders_button.pack(pady=10)

bill_button = ctk.CTkButton(master=menu_frame,text='BILLING',command=b_button,corner_radius=0)
bill_button.pack(pady=10)

tmenu_button = ctk.CTkButton(master=menu_frame,text='THE MENU',command=m_button,corner_radius=0)
tmenu_button.pack(pady=10)

def change_appearance_mode_event(new_appearance_mode: str):
    ctk.set_appearance_mode(new_appearance_mode)

appearance_mode_optionmenu = ctk.CTkOptionMenu(master=menu_frame, values=["Light", "Dark", "System"],command=change_appearance_mode_event)
appearance_mode_optionmenu.pack(side='bottom',pady=5)
appearance_mode_label = ctk.CTkLabel(master=menu_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.pack(side='bottom',pady=5)
########### LABELS FOR MENU STUFF ###############################################
label1 = ctk.CTkLabel(cust_frame, text='CUSTOMERS',font=("Arial",15)).pack()


label2 = ctk.CTkLabel(order_frame, text='ORDERS',font=("Arial",15)).pack()
# label2.pack(expand = True,fill='both')

label3 = ctk.CTkLabel(bill_frame, text='BILL TABLE',font=("Arial",15)).pack()
# label3.pack(expand = True,fill='both')

label4 = ctk.CTkLabel(tmenu_frame, text='THE MENU',font=("Arial",15)).pack()
# label4.pack(expand = True,fill='both')

##################################################

#############CUSTOMER FRAME STUFF ###############
count = 0

cust_tree_frame = ctk.CTkFrame(cust_frame)
cust_tree_frame.pack(fill='both')

ctree_scroll = ctk.CTkScrollbar(cust_tree_frame)
ctree_scroll.pack(side='right', fill='y')



cust_tree = ttk.Treeview(master=cust_tree_frame,yscrollcommand=ctree_scroll.set,selectmode="extended")
cust_tree.pack(padx=5,pady=5,fill='x')
ctree_scroll.configure(command=cust_tree.yview)
cust_tree['columns'] = ("NAME","PHONE","LOCATION")

cust_tree.column("#0", width=0, stretch='no')
cust_tree.column("NAME", width=100,anchor='center')
cust_tree.column("PHONE", width=100,anchor='center')
cust_tree.column("LOCATION", width=100,anchor='center')

cust_tree.heading("NAME",text="NAME")
cust_tree.heading("PHONE",text="PHONE")
cust_tree.heading("LOCATION",text="LOCATION")

for record in result:
    cust_tree.insert(parent='',index='end',iid=count, text="", values=(record[0], record[1], record[2]))
    count += 1

add_frame = ctk.CTkFrame(master=cust_frame)
add_frame.pack(pady=10,expand = True,fill = 'both')
add_frame.columnconfigure(0,weight=1)
add_frame.columnconfigure(1,weight=1)
add_frame.columnconfigure(2,weight=1)
# labels
cname = ctk.CTkLabel(add_frame, text="NAME")
cname.grid(row=0, column=0)

phone = ctk.CTkLabel(add_frame, text="PHONE")
phone.grid(row=0, column=1)

location = ctk.CTkLabel(add_frame, text="LOCATION")
location.grid(row=0, column=2)


#entry boxes
cname_box = ctk.CTkEntry(add_frame)
cname_box.grid(row = 1,column = 0,pady = 5)

phone_box = ctk.CTkEntry(add_frame)
phone_box.grid(row = 1, column = 1,pady=5)

location_box = ctk.CTkEntry(add_frame)
location_box.grid(row = 1,column = 2,pady=5)


def add_record():
    global count
    cust_tree.insert(parent='',index='end',iid=count,text='',values=(cname_box.get(),phone_box.get(),location_box.get()))
    query = "insert into customer values(%s,%s,%s)"
    cursor.execute(query,[cname_box.get(),phone_box.get(),location_box.get()])
    mydb.commit()
    cname_box.delete(0,'end')
    phone_box.delete(0,'end')
    location_box.delete(0,'end')
    count += 1

def remove_record():
    x = cust_tree.selection()
    # rem_list = []
    query = "delete from customer where name=%s"
    for item in x:
        # rem_list.append(cust_tree.set(item,column="SNAME"))
        cursor.execute(query,[cust_tree.set(item,column="NAME")])
        cust_tree.delete(item)
        mydb.commit()
    # print(rem_list)

add_button = ctk.CTkButton(master=add_frame,command=add_record,text='ADD')
add_button.grid(row = 4,column = 1,pady = 15)

remove_button = ctk.CTkButton(master=add_frame,command=remove_record,text='REMOVE')
remove_button.grid(row = 5,column = 1,pady=5)


#################################################

################ ORDER FRAME STUFF ###################
global counto
counto = 0

order_tree_frame = ctk.CTkFrame(order_frame)
order_tree_frame.pack(fill='both')

otree_scroll = ctk.CTkScrollbar(order_tree_frame)
otree_scroll.pack(side='right', fill='y')

order_tree = ttk.Treeview(master=order_tree_frame,yscrollcommand=otree_scroll.set,selectmode="extended")
order_tree.pack(padx = 5,pady=5,fill='x')
otree_scroll.configure(command=order_tree.yview)
order_tree['columns'] = ("ORDER_ID","NAME","ORDER","DATE","QUANTITY")

order_tree.column("#0", width=0, stretch='no')
order_tree.column("ORDER_ID", width=40,anchor='center')
order_tree.column("NAME", width=100,anchor='center')
order_tree.column("ORDER", width=80,anchor='center')
order_tree.column("DATE", width=60,anchor='center')
order_tree.column("QUANTITY", width=40,anchor='center')

order_tree.heading("ORDER_ID",text="OID")
order_tree.heading("NAME",text="NAME")
order_tree.heading("ORDER",text="ORDER")
order_tree.heading("DATE",text="DATE")
order_tree.heading("QUANTITY",text="QUANTITY")

query = "select * from orders"
cursor.execute(query)
result = cursor.fetchall()
for item in result:
    order_tree.insert(parent='',index='end',iid=counto,values=(item[0],item[1],item[2],item[3],item[4]))
    counto += 1

add_frameo = ctk.CTkFrame(master=order_frame)
add_frameo.pack(pady=10,fill = 'both')
add_frameo.columnconfigure(0,weight=1)
add_frameo.columnconfigure(1,weight=1)
add_frameo.columnconfigure(2,weight=1)
add_frameo.columnconfigure(3,weight=1)

name = ctk.CTkLabel(add_frameo, text="NAME")
name.grid(row=0, column=0)

order = ctk.CTkLabel(add_frameo, text="ORDER")
order.grid(row=0, column=1)

date = ctk.CTkLabel(add_frameo, text="DATE")
date.grid(row=0, column=2)

quantity = ctk.CTkLabel(add_frameo, text="QUANTITY")
quantity.grid(row=0, column=3)

#entry boxes
name_box = ctk.CTkEntry(add_frameo)
name_box.grid(row = 1,column = 0,pady = 5)

order_box = ctk.CTkEntry(add_frameo)
order_box.grid(row = 1, column = 1,pady=5)

date_box = ctk.CTkEntry(add_frameo)
date_box.grid(row = 1,column = 2,pady=5)

quantity_box = ctk.CTkEntry(add_frameo)
quantity_box.grid(row = 1,column = 3,pady=5)

def add_order():
    now = datetime.now()
    global counto
    query = "insert into orders(name,ordername,date,quantity) values(%s,%s,%s,%s)"
    if date_box.get() == '':
        cursor.execute(query,[name_box.get(),order_box.get(),now.strftime('%Y-%m-%d'),int(quantity_box.get())])
        cursor.execute('select max(order_id) from orders')
        oid = cursor.fetchall()[0]
        order_tree.insert(parent='',index='end',iid=counto,text='',values=(oid,name_box.get(),order_box.get(),now.strftime('%Y-%m-%d'),quantity_box.get()))
        mydb.commit()
    else:
        cursor.execute(query,[name_box.get(),order_box.get(),date_box.get(),int(quantity_box.get())])
        cursor.execute('select max(order_id) from orders')
        oid = cursor.fetchall()[0]
        order_tree.insert(parent='',index='end',iid=counto,text='',values=(oid,name_box.get(),order_box.get(),date_box.get(),quantity_box.get()))
        mydb.commit()
    
    name_box.delete(0,'end')
    order_box.delete(0,'end')
    date_box.delete(0,'end')
    quantity_box.delete(0,'end')
    counto += 1

def remove_order():
    x = order_tree.selection()
    # rem_list = []
    query = "delete from orders where order_id=%s"
    for item in x:
        # rem_list.append(cust_tree.set(item,column="SNAME"))
        cursor.execute(query,[int(order_tree.set(item,column="ORDER_ID"))])
        order_tree.delete(item)
        mydb.commit()

def remove_all_orders():
    for record in order_tree.get_children():     # for clearing table
        order_tree.delete(record)
    query = "truncate orders"
    cursor.execute(query)
    mydb.commit()

add_buttono = ctk.CTkButton(master=add_frameo,command=add_order,text='ADD')
add_buttono.grid(row = 3,column = 1,pady = 5)

remove_buttono = ctk.CTkButton(master=add_frameo,command=remove_order,text='REMOVE')
remove_buttono.grid(row = 3,column = 2,pady=5)

remove_all = ctk.CTkButton(master=order_frame,text='REMOVE ALL',command=remove_all_orders)
remove_all.pack(side='bottom',pady=10)


#######################################################

########### MENU FRAME ##################
global countm
countm = 0

menu_tree_frame = ctk.CTkFrame(tmenu_frame)
menu_tree_frame.pack(fill='both')

mtree_scroll = ctk.CTkScrollbar(menu_tree_frame)
mtree_scroll.pack(side='right', fill='y')

tmenu_tree = ttk.Treeview(master=menu_tree_frame,yscrollcommand=mtree_scroll.set,selectmode="extended")
tmenu_tree.pack(padx = 5,pady=5,fill='x')
mtree_scroll.configure(command=tmenu_tree.yview)
tmenu_tree['columns'] = ("ITEM","PRICE")

tmenu_tree.column("#0", width=0, stretch='no')
tmenu_tree.column("ITEM", width=120,anchor='center')
tmenu_tree.column("PRICE", width=80,anchor='center')


tmenu_tree.heading("ITEM",text="ITEM")
tmenu_tree.heading("PRICE",text="PRICE")

query = "select * from menu"
cursor.execute(query)
result = cursor.fetchall()
for item in result:
    tmenu_tree.insert(parent='',index='end',iid=countm,values=(item[0],item[1]))
    countm += 1

add_framem = ctk.CTkFrame(master=tmenu_frame)
add_framem.pack(pady=10,expand = True,fill = 'both')
add_framem.columnconfigure(0,weight=1)
add_framem.columnconfigure(1,weight=1)

menu_item = ctk.CTkLabel(add_framem, text="ITEM")
menu_item.grid(row=0, column=0)

price = ctk.CTkLabel(add_framem, text="PRICE")
price.grid(row=0, column=1)

#entry boxes
menu_item_box = ctk.CTkEntry(add_framem)
menu_item_box.grid(row = 1,column = 0,pady = 5)

price_box = ctk.CTkEntry(add_framem)
price_box.grid(row = 1, column = 1,pady=5)

def add_menu():
    global countm
    tmenu_tree.insert(parent='',index='end',iid=countm,text='',values=(menu_item_box.get(),price_box.get()))
    query = "insert into menu values(%s,%s)"
    cursor.execute(query,[menu_item_box.get(),price_box.get()])
    mydb.commit()
    menu_item_box.delete(0,'end')
    price_box.delete(0,'end')
    countm += 1

def remove_menu():
    x = tmenu_tree.selection()
    query = "delete from menu where item=%s"
    for item in x:
        cursor.execute(query,[tmenu_tree.set(item,column="ITEM")])
        tmenu_tree.delete(item)
        mydb.commit()

add_buttonm = ctk.CTkButton(master=add_framem,command=add_menu,text='ADD')
add_buttonm.grid(row = 3,column = 0,pady = 5,sticky = 'e',padx = 5)

remove_buttonm = ctk.CTkButton(master=add_framem,command=remove_menu,text='REMOVE')
remove_buttonm.grid(row = 3,column = 1,pady=5,sticky = 'w',padx = 5)

########################################

########### BILL FRAME STUFF #############
global countb
countb = 0

bill_tree_frame = ctk.CTkFrame(bill_frame)
bill_tree_frame.pack(fill='both')

btree_scroll = ctk.CTkScrollbar(bill_tree_frame)
btree_scroll.pack(side='right', fill='y')

bill_tree = ttk.Treeview(master=bill_tree_frame,yscrollcommand=btree_scroll.set,selectmode="extended")
bill_tree.pack(padx = 5,pady=5,fill='x')
btree_scroll.configure(command=bill_tree.yview)
bill_tree['columns'] = ("NAME","AMOUNT","STATUS")

bill_tree.column("#0", width=0, stretch='no')
bill_tree.column("NAME", width=120,anchor='center')
bill_tree.column("AMOUNT", width=80,anchor='center')
bill_tree.column("STATUS", width=80,anchor='center')

bill_tree.heading("NAME",text="NAME")
bill_tree.heading("AMOUNT",text="AMOUNT")
bill_tree.heading("STATUS",text="STATUS")

query = "with tab as (select name,quantity*price Amount from orders o join menu m on o.ordername=m.item) select name,sum(Amount) from tab group by name"
cursor.execute(query)
resultb = cursor.fetchall()
for item in resultb:
    bill_tree.insert(parent='',index='end',iid=countb,values=(item[0],item[1],'0'))
    countb += 1

# add_frameb = ctk.CTkFrame(master=bill_frame)
# add_frameb.pack(pady=10,fill = 'x')

def refresh_fun():
    global countb
    for record in bill_tree.get_children():     # for clearing table
        bill_tree.delete(record)

    query = "with tab as (select name,quantity*price Amount from orders o join menu m on o.ordername=m.item) select name,sum(Amount) from tab group by name"
    cursor.execute(query)
    resultb = cursor.fetchall()
    for item in resultb:
        bill_tree.insert(parent='',index='end',iid=countb,values=(item[0],item[1],'0'))
        countb += 1

refresh_button = ctk.CTkButton(master=bill_frame,command=refresh_fun,text='REFRESH')
refresh_button.pack(pady=5)
##########################################

root.mainloop()

