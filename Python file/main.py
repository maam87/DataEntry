import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import os
from style_themes import Light_Theme
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

conn = sqlite3.connect('DATABASE_FILE/DatabaseFix/DatabaseList.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS listData (
    ID INTEGER PRIMARY KEY,
    FileName TEXT,
    DataName TEXT)
    ''')

conn.commit()
conn.close()


class WindowApp:
    def __init__(self, master):

        # ----- global items -----
        # global number

        # ----- command   --------
        def newSeller():
            self.DatabaseName = self.SellerEntry.get().strip().upper() + '.db'
            self.FileDataName = self.SellerEntry.get().strip().upper()
            self.DataName = self.SellerEntry.get().strip().upper()

            if len(self.DatabaseName) != 0:
                connect = sqlite3.connect('DATABASE_FILE/DatabaseFix/DatabaseList.db')
                cursor = connect.cursor()

                cursor.execute(
                    "INSERT INTO listData (FileName, DataName) "
                    "VALUES (?, ?)", (self.FileDataName, self.DataName))

                connect.commit()
                connect.close()

                connect2 = sqlite3.connect('DATABASE_FILE/Database make it/' + self.DatabaseName)
                cursor2 = connect2.cursor()

                cursor2.execute(f'''CREATE TABLE IF NOT EXISTS {self.DataName} (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    BARCODE INTEGER,
                    DESCRIPTION TEXT,
                    UNIT TEXT,
                    QUANTITY TEXT,
                    TOTAL FLOAT,
                    RATE TEXT,
                    SHELF_PRICE FLOAT,
                    CATEGORY TEXT,
                    SHELF_NUM TEXT)''')

                connect2.commit()
                connect2.close()
            messagebox.showinfo('Attention', 'Database is ready!')
            refresh_combobox()

            self.SellerEntry.delete(0, 'end')
            self.BarcodeEntry.focus()

        def controlOther(e):
            current = self.RateComboBox.current()
            if current == 6:
                self.OtherRateEntry.configure(state='normal')
                self.OtherRateEntry.focus()
            else:
                self.OtherRateEntry.configure(state='disable')

        def addingData():
            # check_barcode()
            bar = self.BarcodeEntry.get()
            des = self.DescriptionEntry.get()
            unit = self.UnitEntry.get()
            qty = self.QuantityEntry.get()
            total = self.TotalValueEntry.get()
            category = self.CategoryComboBox.get()
            rate = self.RateComboBox.current()
            other = self.OtherRateEntry.get()
            shelf_num = self.ShelfNumComboBox.get()
            DataBaseFile = self.SellerComboBox.get().strip()

            if (len(DataBaseFile) != 0 and len(bar) != 0 and len(des) != 0 and len(unit) != 0 and
                    len(qty) != 0 and len(total) != 0 and len(category) != 0):

                connect = sqlite3.connect('DATABASE_FILE/Database make it/' + DataBaseFile + '.db')
                cursor = connect.cursor()

                if rate == 0:
                    rate = 1.1
                elif rate == 2:
                    rate = 1.3
                elif rate == 3:
                    rate = 1.4
                elif rate == 4:
                    rate = 1.5
                elif rate == 5:
                    rate = 2
                # else:
                #     rate = int(other)/100

                final2 = float(int(total) / (int(unit) * int(qty)) * rate)
                round2 = round(final2, 2)
                price_shelf = str(round2)

                # Insert data into the database
                cursor.execute(f'''INSERT INTO {DataBaseFile} 
                    (BARCODE, DESCRIPTION, UNIT, QUANTITY, TOTAL, RATE, SHELF_PRICE, CATEGORY, SHELF_NUM) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (bar, des.upper(), float(unit), float(qty), float(total), rate,
                                float(price_shelf), category, shelf_num))

                # Commit the transaction and close the connection
                connect.commit()
                connect.close()
                treeviewShow()
                clearInside()
                self.SellerComboBox.configure(state='normal')
                self.SellerComboBox.delete(0, 'end')
                self.SellerComboBox.configure(state='readonly')
            else:
                messagebox.showinfo('Attention Error!', 'Should be all TextBox Not Empty.\n'
                                                        'Special the Seller Name.')
                self.BarcodeEntry.focus()

        def treeviewShow():
            self.tree.delete(*self.tree.get_children())
            DatabaseFile = self.SellerComboBox.get()
            connect = sqlite3.connect('DATABASE_FILE/Database make it/' + DatabaseFile + '.db')
            cursor = connect.cursor()
            # Execute a SELECT statement to retrieve data from the database
            cursor.execute(f'''SELECT ID, BARCODE, DESCRIPTION, UNIT, QUANTITY, TOTAL, SHELF_PRICE,
                            CATEGORY FROM {DatabaseFile}''')
            rows = cursor.fetchall()
            connect.commit()
            connect.close()

            # Iterate over the retrieved rows and insert them into the treeview
            for row in rows:
                self.tree.insert('', 'end', values=row)

        def TreeData(e):
            try:
                self.tree.delete(*self.tree.get_children())
                connect = sqlite3.connect('DATABASE_FILE/Database make it/' + self.SellerComboBox.get() + '.db')
                cursor = connect.cursor()
                cursor.execute(f'''SELECT ID, BARCODE, DESCRIPTION, UNIT, QUANTITY,
                 TOTAL, SHELF_PRICE, CATEGORY FROM {self.SellerComboBox.get()}''')
                connect.commit()
                for row in cursor.fetchall():
                    self.tree.insert('', 'end', values=row)
                connect.close()

            except:
                pass

        def clearInside():
            self.BarcodeEntry.delete(0, 'end')
            self.DescriptionEntry.delete(0, 'end')
            self.UnitEntry.delete(0, 'end')
            self.QuantityEntry.delete(0, 'end')
            self.TotalValueEntry.delete(0, 'end')
            self.RateComboBox.current(2)
            self.OtherRateEntry.delete(0, 'end')
            self.CategoryComboBox.current(14)
            self.DeleteButton.configure(state='disable')
            self.UpdateButton.configure(state='disable')
            self.OtherRateEntry.configure(state='disable')
            self.ShelfNumComboBox.current(0)
            self.BarcodeEntry.focus()
            self.BarcodeEntry.focus()
            self.tree.delete(*self.tree.get_children())
            self.SearchEntry.delete(0, 'end')

        def on_double_click(e):
            item = self.tree.selection()[0]  # Get the selected item
            values = self.tree.item(item, 'values')
            self.BarcodeEntry.delete(0, 'end')
            self.DescriptionEntry.delete(0, 'end')
            self.UnitEntry.delete(0, 'end')
            self.QuantityEntry.delete(0, 'end')
            self.TotalValueEntry.delete(0, 'end')
            self.CategoryComboBox.current(14)
            # clearInside()
            self.BarcodeEntry.insert(0, values[1])
            self.DescriptionEntry.insert(0, values[2])
            self.UnitEntry.insert(0, values[3])
            self.QuantityEntry.insert(0, values[4])
            self.TotalValueEntry.insert(0, values[5])
            self.CategoryComboBox.set(values[7])
            self.UpdateButton.configure(state='normal')
            self.DeleteButton.configure(state='disabled')

        def on_click(e):
            self.DeleteButton.configure(state='normal')
            self.UpdateButton.configure(state='disabled')

        def delete_item():
            DataListFile = self.SellerComboBox.get()
            # Get the selected item from the TreeView
            Item_Selected = self.tree.selection()
            if Item_Selected:
                # Get the ID of the selected item
                item_id = self.tree.item(Item_Selected)['values'][0]

                # Delete the record from the database
                conn = sqlite3.connect('DATABASE_FILE/Database make it/' + DataListFile + '.db')
                cur = conn.cursor()
                cur.execute(f"DELETE FROM {DataListFile} WHERE ID=?", (item_id,))
                conn.commit()
                conn.close()

                # Remove the item from the TreeView
                self.tree.delete(Item_Selected)
                self.DeleteButton.configure(state='disable', style='DisableButton.TButton')

        def update_item():
            # Retrieve data from entry fields and combo-boxes
            bar = self.BarcodeEntry.get()
            des = self.DescriptionEntry.get()
            unit = float(self.UnitEntry.get())
            qty = float(self.QuantityEntry.get())
            total = float(self.TotalValueEntry.get())
            rate = self.RateComboBox.get()
            category = self.CategoryComboBox.get()
            shelf_num = self.ShelfNumComboBox.get()

            DatabaseFile = self.SellerComboBox.get()

            # Get the selected item from the TreeView
            ItemSelect = self.tree.selection()
            if ItemSelect:
                # Get the ID of the selected item
                item_id = self.tree.item(ItemSelect)['values'][0]

                # Calculate the final price based on the rate
                if rate == 'Other':
                    rate = int(self.OtherRateEntry.get()) / 100
                elif rate == self.valuesCombobox[0]:
                    rate = 1.1
                elif rate == self.valuesCombobox[1]:
                    rate = 1.3
                elif rate == self.valuesCombobox[2]:
                    rate = 1.4
                elif rate == self.valuesCombobox[3]:
                    rate = 1.5
                elif rate == self.valuesCombobox[4]:
                    rate = 2
                elif rate == self.valuesCombobox[5]:
                    rate = 3
                else:
                    rate = self.OtherRateEntry.get()

                final1 = (total / (unit * qty)) * rate
                round1 = round(final1, 2)
                price_shelf = float(round1)

                # Update the record in the database
                conn = sqlite3.connect('DATABASE_FILE/Database make it/' + DatabaseFile + '.db')
                cursor = conn.cursor()

                cursor.execute(f'''UPDATE {DatabaseFile} SET BARCODE=?, DESCRIPTION=?, UNIT=?, 
                                    QUANTITY=?, TOTAL=?, RATE=?, SHELF_PRICE=?, CATEGORY=?, SHELF_NUM=? WHERE ID=?''',
                               (bar, des, unit, qty, total, rate, price_shelf, category, shelf_num, item_id)
                               )
                conn.commit()
                conn.close()
                self.UpdateButton.configure(state='disable')

                # Update the item in the TreeView
                self.tree.item(ItemSelect, values=(item_id, bar, des, unit, qty, total, price_shelf, category))

                # clear everything after all done.
                clearInside()
                self.SellerComboBox.focus()

            treeviewShow()

        def refresh_combobox():
            self.SellerComboBox['values'] = [file[:-3] for file in os.listdir('DATABASE_FILE/Database make it/')
                                             if file.endswith(".db")]

        def check_barcode(e):
            barcode = int(self.CheckBarcodeEntry.get().strip())  # Get the entered barcode
            DataName = self.SellerComboBox.get()
            if barcode:
                connect = sqlite3.connect('DATABASE_FILE/Database make it/' + DataName + '.db')
                cursor = connect.cursor()
                cursor.execute(f"SELECT * FROM {DataName} WHERE BARCODE=?", (barcode,))
                data = cursor.fetchone()
                if data:
                    messagebox.showerror("Error", "This barcode is already taken.")
                    self.SearchEntry.insert(0, self.CheckBarcodeEntry.get())
                    self.CheckBarcodeEntry.delete(0, 'end')
                    self.SearchEntry.focus()
                    # Search()
                else:
                    pass
                    # messagebox.showinfo("Success", "Barcode is available.")

        def update_tree(query):
            self.tree.delete(*self.tree.get_children())
            data = self.SellerComboBox.get()

            connect = sqlite3.connect('DATABASE_FILE/Database make it/' + data + '.db')
            cursor = connect.cursor()

            if query:
                cursor.execute(f"SELECT ID, BARCODE, DESCRIPTION, UNIT, QUANTITY, TOTAL, "
                               f"SHELF_PRICE, CATEGORY FROM {data} WHERE barcode LIKE ? OR description LIKE ?",
                               ('%' + query + '%', '%' + query + '%'))
            else:
                cursor.execute(f"SELECT ID, BARCODE, DESCRIPTION, UNIT, QUANTITY, TOTAL, "
                               f"SHELF_PRICE, CATEGORY FROM {data}")
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)

        def Search(e):
            if type(self.SearchEntry.get()) == int:
                search_query = int(self.SearchEntry.get())
                update_tree(search_query)
            else:
                search_query = str(self.SearchEntry.get())
                update_tree(search_query)

        def clearSellerComboBox():
            self.SellerComboBox.configure(state='normal')
            self.SellerComboBox.delete(0, 'end')
            self.SellerComboBox.configure(state='readonly')

        def ClearText():
            self.SearchEntry.delete(0, 'end')

        def export_to_pdf():
            # series numbers with .txt
            with open("Note/number.txt", "r") as file1:
                number = int(file1.read())
                number += 1

            connect = sqlite3.connect('DATABASE_FILE/Database make it/' + self.SellerComboBox.get() + '.db')
            cursor = connect.cursor()
            cursor.execute(f'''SELECT ID, BARCODE, DESCRIPTION, SHELF_PRICE FROM {self.SellerComboBox.get()}''')
            data = cursor.fetchall()

            # Define filename based on specified format
            filename = f"{self.SellerComboBox.get()} List-{datetime.now().strftime('%d-%m-%Y')}-0{number}"

            table_data = [["ID", "Barcode", "Description", "PriceShelf"]]
            table_col = [50, 120, 250, 120]

            for row in data:
                table_data.append(row)

            c = canvas.Canvas("File PDF/" + filename + '.pdf', pagesize=A4)

            # Create the table
            table = Table(table_data, colWidths=table_col)

            # Add style to the table
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), HexColor('#99ffcc')),
                                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#9fc')),
                                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Times-Italic'),
                                ('FONTNAME', (2, 1), (2, -1), 'Times-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#CCE5FF')),
                                ('GRID', (0, 0), (-1, -1), 1, colors.white),
                                ('ALIGN', (2, 1), (2, -1), 'LEFT')])

            table.setStyle(style)

            # Add the table to the PDF document
            table.wrapOn(c, 0, 0)
            table.drawOn(c, 30, 600)
            c.save()

            # Save the current number to a file
            with open("Note/number.txt", "w") as file:
                file.write(str(number))
            messagebox.showinfo('Attention', 'Database file export to PDF file. Done!')

        # ----- Create option window -----

        self.m = master
        # self.m.geometry('1000x800+200+50')
        self.m.title('Abu Salim Supermarket-Application Data Entry')
        self.m.configure(background='#2b3e50')
        self.m.attributes('-fullscreen', True)

        # ----- Increment to try number -----
        # Initialize the number
        number = 0
        try:
            with open("Note/number.txt", "r") as file:
                number = int(file.read())
        except FileNotFoundError:
            # Save the current number to a file
            with open("Note/number.txt", "w") as file:
                file.write(str(number))

        # ----- Frames -----
        self.topFrame = ttk.Frame(self.m, style='f.TFrame')
        self.centerFrame = ttk.Frame(self.m, style='f.TFrame')
        self.bottomFrame = ttk.Frame(self.m, style='f.TFrame')

        # ----- position Frames -----
        self.topFrame.pack(padx=10, pady=10, expand=True, fill='x')
        self.centerFrame.pack(expand=True, padx=10, pady=10)
        self.bottomFrame.pack(fill='x', expand=True, padx=10, pady=10)

        # ----- Title App and icon
        self.icon1 = Image.open('image/images/online-shopping.png')
        self.iconResize = self.icon1.resize((25, 25))
        # icon for the application
        self.iconImage = ImageTk.PhotoImage(self.iconResize)

        # ----- Labels -----
        self.iconApp = ttk.Label(self.topFrame, image=self.iconImage, style='l.TLabel')
        self.titleApp = ttk.Label(self.topFrame, text='Abu Salim Supermarket-Yagoona', anchor='center',
                                  style='l.TLabel')

        # -----position Labels -----
        self.iconApp.pack(side='left')
        self.titleApp.pack(side='right', expand=True)

        # __________________________

        # ----- Left Label Frame ------
        self.leftLabelFrame = ttk.LabelFrame(self.centerFrame, text='Create Database Seller:',
                                             style='lf.TLabelframe')

        # ----- position Left Label Frame -----
        self.leftLabelFrame.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        # __________________________________

        # ----- Seller option(Entry, Button, Radiobutton, var -----
        self.SellerLabel = ttk.Label(self.leftLabelFrame, text='Seller Name:', style='l.TLabel')
        self.SellerEntry = ttk.Entry(self.leftLabelFrame, style='e.TEntry')
        self.var = tk.BooleanVar()
        self.SellerRadioButton1 = ttk.Radiobutton(self.leftLabelFrame, variable=self.var, value=True,
                                                  text='Automatic Data', style='r.TRadiobutton')
        self.SellerRadioButton2 = ttk.Radiobutton(self.leftLabelFrame, variable=self.var, value=False,
                                                  text='Manual Data', style='r.TRadiobutton')
        self.SellerButton = ttk.Button(self.leftLabelFrame, text='Create New Seller', command=newSeller,
                                       style='t.TButton')
        self.var.set(True)

        # ----- Seller position -----
        self.SellerLabel.grid(row=0, column=0, sticky='news', columnspan=2, padx=7, pady=10)
        self.SellerEntry.grid(row=1, column=0, sticky='news', columnspan=2, padx=7, pady=10)
        self.SellerRadioButton1.grid(row=2, column=0, sticky='news', padx=7, pady=7)
        self.SellerRadioButton2.grid(row=3, column=0, sticky='news', padx=7, pady=7)
        self.SellerButton.grid(row=4, column=0, columnspan=2, sticky='news', padx=7, pady=10)
        # ____________________________

        # ----- Right Label Frame ------
        self.rightLabelFrame = ttk.LabelFrame(self.centerFrame, text='Control Data Entry:', style='lf.TLabelframe')

        # ----- position Right Label Frame -----
        self.rightLabelFrame.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        # __________________________________

        # ----- Control Items(Label, Button, ComboBox) -----
        # ----- Labels -----
        self.SellerChooseLabel = ttk.Label(self.rightLabelFrame, text='Seller Name:', style='l.TLabel')
        self.BarcodeLabel = ttk.Label(self.rightLabelFrame, text='Barcode:', style='l.TLabel')
        self.DescriptionLabel = ttk.Label(self.rightLabelFrame, text='Description:', style='l.TLabel')
        self.UnitLabel = ttk.Label(self.rightLabelFrame, text='Unit In Box:', style='l.TLabel')
        self.QuantityLabel = ttk.Label(self.rightLabelFrame, text='Quantity Boxes:', style='l.TLabel')
        self.TotalValueLabel = ttk.Label(self.rightLabelFrame, text='Total Value for Item:', style='l.TLabel')
        self.CategoryLabel = ttk.Label(self.rightLabelFrame, text='Category/category:', style='l.TLabel')
        self.RateLabel = ttk.Label(self.rightLabelFrame, text='Rate:', style='l.TLabel')
        self.OtherRateLabel = ttk.Label(self.rightLabelFrame, text='Other Rate:', style='l.TLabel')
        self.ShelfNumLabel = ttk.Label(self.rightLabelFrame, text='Shelf Number:', style='l.TLabel')
        self.CheckBarcodeLabel = ttk.Label(self.rightLabelFrame, text='Check Barcode:', style='l.TLabel')

        # -----Position Labels -----
        self.SellerChooseLabel.grid(row=0, column=0, padx=5, pady=5, sticky='e')  # 01-1
        self.BarcodeLabel.grid(row=1, column=0, padx=5, pady=5, sticky='e')  # 02-1
        self.DescriptionLabel.grid(row=2, column=0, padx=5, pady=5, sticky='e')  # 02-2
        self.UnitLabel.grid(row=3, column=0, padx=5, pady=5, sticky='e')  # 02-3
        self.QuantityLabel.grid(row=4, column=0, padx=5, pady=5, sticky='e')  # 02-4
        self.TotalValueLabel.grid(row=5, column=0, padx=5, pady=5, sticky='e')  # 02-5
        self.CategoryLabel.grid(row=1, column=2, padx=5, pady=5, sticky='e')  # 03-1
        self.RateLabel.grid(row=2, column=2, padx=5, pady=5, sticky='e')  # 03-2
        self.OtherRateLabel.grid(row=3, column=2, padx=5, pady=5, sticky='e')  # 03-3
        self.ShelfNumLabel.grid(row=4, column=2, padx=5, pady=5, sticky='e')  # 03-4
        self.CheckBarcodeLabel.grid(row=5, column=2, padx=5, pady=5, sticky='e')

        # ----- ComboBox -----
        self.SellerComboBox = ttk.Combobox(self.rightLabelFrame, state='readonly', style='cb.TCombobox')
        self.SellerComboBox.bind('<FocusIn>', TreeData)
        # ----- Entry -----
        self.BarcodeEntry = ttk.Entry(self.rightLabelFrame, style='e.TEntry', font=('Courier', 15, 'italic'))
        self.DescriptionEntry = ttk.Entry(self.rightLabelFrame, style='e.TEntry', font=('Courier', 15, 'italic'))
        self.UnitEntry = ttk.Entry(self.rightLabelFrame, style='e.TEntry', font=('Courier', 15, 'italic'))
        self.QuantityEntry = ttk.Entry(self.rightLabelFrame, style='e.TEntry', font=('Courier', 15, 'italic'))
        self.TotalValueEntry = ttk.Entry(self.rightLabelFrame, style='e.TEntry', font=('Courier', 15, 'italic'))
        self.CheckBarcodeEntry = ttk.Entry(self.rightLabelFrame, style='e.TEntry', font=('Courier', 15, 'italic'))

        self.CheckBarcodeEntry.bind("<FocusOut>", check_barcode)

        # ----- Position Entry -----
        self.BarcodeEntry.grid(row=1, column=1, padx=5, pady=5)
        self.DescriptionEntry.grid(row=2, column=1, padx=5, pady=5)
        self.UnitEntry.grid(row=3, column=1, padx=5, pady=5)
        self.QuantityEntry.grid(row=4, column=1, padx=5, pady=5)
        self.TotalValueEntry.grid(row=5, column=1, padx=5, pady=5)
        self.CheckBarcodeEntry.grid(row=5, column=3, padx=5, pady=5)

        # ----- Values    ---------
        self.valuesCombobox = ['[+] Low rate: 10%', '[+] Medium rate: 20%', '[+] Default rate: 30%',
                               '[+] high rate: 40%', '[+] big high rate: 50%', '[+] Super high rate: 100%',
                               '[+] Other']

        self.valuesCategory1 = ['[+] Grocery', '[+] Deli', '[+] Bakery', '[+] Meat', '[+] Seafood', '[+] Dairy',
                                '[+] Frozen Foods', '[+] Canned Goods', '[+] Dry Goods', '[+] Snacks', '[+] Beverages',
                                '[+] International Foods', '[+] Organic and Natural', '[+] Gluten-Free',
                                '[+] Specialty Foods', '[+] Bulk Foods', '[+] Select Category']

        self.valuesShelf = ['[+] Select Number Shelf',
                            '[+] A1', '[+] A2', '[+] A3', '[+] A4', '[+] A5', '[+] A6', '[+] A7', '[+] A8',
                            '[+] B1', '[+] B2', '[+] B3', '[+] B4', '[+] B5', '[+] B6', '[+] B7', '[+] B8',
                            '[+] C1', '[+] C2', '[+] C3', '[+] C4', '[+] C5', '[+] C6', '[+] C7', '[+] C8',
                            '[+] D1', '[+] D2', '[+] D3', '[+] D4', '[+] D5', '[+] D6', '[+] D7', '[+] D8',
                            '[+] E1', '[+] E2', '[+] E3', '[+] E4', '[+] E5', '[+] E6', '[+] E7', '[+] E8',
                            '[+] F1', '[+] F2', '[+] F3', '[+] F4', '[+] F5', '[+] F6', '[+] F7', '[+] F8',
                            '[+] G1', '[+] G2', '[+] G3', '[+] G4', '[+] G5', '[+] G6', '[+] G7', '[+] G8',
                            '[+] H1', '[+] H2', '[+] H3', '[+] H4', '[+] H5', '[+] H6', '[+] H7', '[+] H8',
                            '[+] J1', '[+] J2', '[+] J3', '[+] J4', '[+] J5', '[+] J6', '[+] J7', '[+] J8',
                            '[+] K1', '[+] K2', '[+] K3', '[+] K4', '[+] K5', '[+] K6', '[+] K7', '[+] K8',
                            '[+] L1', '[+] L2', '[+] L3', '[+] L4', '[+] L5', '[+] L6', '[+] L7', '[+] L8',
                            '[+] M1', '[+] M2', '[+] M3', '[+] M4', '[+] M5', '[+] M6', '[+] M7', '[+] M8',
                            '[+] N1', '[+] N2', '[+] N3', '[+] N4', '[+] N5', '[+] N6', '[+] N7', '[+] N8',
                            '[+] O1', '[+] O2', '[+] O3', '[+] O4', '[+] O5', '[+] O6', '[+] O7', '[+] O8',
                            '[+] P1', '[+] P2', '[+] P3', '[+] P4', '[+] P5', '[+] P6', '[+] P7', '[+] P8',
                            '[+] Q1', '[+] Q2', '[+] Q3', '[+] Q4', '[+] Q5', '[+] Q6', '[+] Q7', '[+] Q8',
                            '[+] R1', '[+] R2', '[+] R3', '[+] R4', '[+] R5', '[+] R6', '[+] R7', '[+] R8']

        self.valuesCategory1 = sorted(self.valuesCategory1)

        # ----- ComboBox -----
        self.CategoryComboBox = ttk.Combobox(self.rightLabelFrame, values=self.valuesCategory1,
                                             state='readonly', style='cb.TCombobox')
        self.RateComboBox = ttk.Combobox(self.rightLabelFrame, values=self.valuesCombobox, state='readonly',
                                         style='cb.TCombobox')
        self.RateComboBox.bind('<FocusOut>', controlOther)

        self.OtherRateEntry = ttk.Entry(self.rightLabelFrame, state='disabled', style='e.TEntry')

        self.ShelfNumComboBox = ttk.Combobox(self.rightLabelFrame, values=self.valuesShelf, state='readonly',
                                             style='cb.TCombobox')

        # ----- Default Option for ComboBox -----
        self.CategoryComboBox.current(14)
        self.RateComboBox.current(2)
        self.ShelfNumComboBox.current(0)

        # ----- Position ComboBox -----
        self.SellerComboBox.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='news')
        self.CategoryComboBox.grid(row=1, column=3, padx=5, pady=5)
        self.RateComboBox.grid(row=2, column=3, padx=5, pady=5)
        self.ShelfNumComboBox.grid(row=4, column=3, padx=5, pady=5)

        # ----- Position Entry -----
        self.OtherRateEntry.grid(row=3, column=3, padx=5, pady=5)

        # ----- Bottom Label Frame -----
        self.BottomLabelFrame = ttk.LabelFrame(self.centerFrame, text='Button Control:', style='lf.TLabelframe')

        # ----- Position Bottom Label Frame -----
        self.BottomLabelFrame.grid(row=1, column=0, columnspan=2, sticky='news', padx=10, pady=10)

        # ----- Control Bottom(Button) -----
        self.width = 24
        self.UpdateButton = ttk.Button(self.BottomLabelFrame, text='Update', width=self.width,
                                       state='disabled', command=update_item, style='t.TButton')
        self.DeleteButton = ttk.Button(self.BottomLabelFrame, text='Delete', width=self.width,
                                       state='disabled', command=delete_item, style='t.TButton')
        self.RefreshButton = ttk.Button(self.BottomLabelFrame, text='Refresh', width=self.width,
                                        command=lambda: (clearInside(), clearSellerComboBox()),
                                        style='t.TButton')
        self.AddItemButton = ttk.Button(self.BottomLabelFrame, text='Add Items', width=self.width,
                                        command=addingData, style='t.TButton')

        # ----- Position Button -----
        self.UpdateButton.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        self.DeleteButton.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        self.RefreshButton.grid(row=0, column=2, padx=10, pady=10, sticky='news')
        self.AddItemButton.grid(row=0, column=3, padx=10, pady=10, sticky='news')
        # ___________________________

        # ----- Label Frame TreeView -----
        self.treeViewLabelFrame = ttk.LabelFrame(self.centerFrame, text='Tree View / Table From Data Base:',
                                                 style='lf.TLabelframe')

        # ----- Position Label Frame TreeView -----
        self.treeViewLabelFrame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='news')

        # ----- Canvas    ---------
        self.canvas = tk.Canvas(self.treeViewLabelFrame, highlightcolor='#e0e0e0', background='#2b3e50')

        self.canvas.grid(row=5, column=0, columnspan=7, padx=15, pady=5)
        # ----- Scrollbar ---------
        self.scrollBar = ttk.Scrollbar(self.canvas, orient='vertical')

        self.scrollBar.grid(row=1, column=4, sticky='news')

        # ----- frame control for treeview -----
        self.frameTree = ttk.Frame(self.canvas, style='f.TFrame')
        self.frameTree.grid(row=0, column=0, padx=5, pady=5, sticky='news')

        # ----- Value for ComboBox -----
        self.ValueSearch = ['Barcode', 'Description']
        # ----- Search (Label, Entry, Button -----
        self.SearchLabel = ttk.Label(self.frameTree, text='Search:', style='l.TLabel')
        self.SearchEntry = ttk.Entry(self.frameTree, style='e.TEntry', width=80)
        self.ClearSearchEntry = ttk.Button(self.frameTree, text='Clear', command=ClearText, style='t.TButton')

        self.SearchLabel.grid(row=0, column=0, padx=5, pady=5, sticky='news')
        self.SearchEntry.grid(row=0, column=1, padx=5, pady=5, sticky='news')
        self.ClearSearchEntry.grid(row=0, column=2, padx=5, pady=5, sticky='news')

        self.SearchEntry.bind('<KeyRelease>', Search)

        # ----- TreeView  ---------
        self.tree = ttk.Treeview(self.canvas, style="t.Treeview")
        self.tree.configure(yscrollcommand=self.scrollBar.set)

        self.tree['columns'] = ('id', 'barcode', 'description', 'unit', 'quantity', 'total_value',
                                'final_price', 'category')

        self.tree.heading('#0', text='', anchor='center')
        self.tree.heading('id', text='ID', anchor='center')
        self.tree.heading('barcode', text='Barcode', anchor='center')
        self.tree.heading('description', text='Description', anchor='w')
        self.tree.heading('unit', text='Unit In Box', anchor='center')
        self.tree.heading('quantity', text='Quantity', anchor='center')
        self.tree.heading('total_value', text='Total Values', anchor='center')
        self.tree.heading('final_price', text='Final Prices', anchor='center')
        self.tree.heading('category', text='Category', anchor='center')

        self.tree.column('#0', width=0, stretch=False)
        self.tree.column('id', width=45, anchor='center')
        self.tree.column('barcode', width=140, anchor='w')
        self.tree.column('description', width=270)
        self.tree.column('unit', width=100, anchor='center')
        self.tree.column('quantity', width=150, anchor='center')
        self.tree.column('total_value', width=100, anchor='center')
        self.tree.column('final_price', width=100, anchor='center')
        self.tree.column('category', width=130, anchor='w')

        self.tree.grid(row=1, column=0)
        self.tree.bind('<Double-1>', on_double_click)
        self.tree.bind('<Button-1>', on_click)
        # ----- Config Scrollbar ---------
        self.scrollBar.configure(command=self.tree.yview)

        # ----- Button Export pdf -----
        self.ExportButton = ttk.Button(self.canvas, text='Export PDF', command=export_to_pdf, style='t.TButton')

        self.ExportButton.grid(row=2, column=0, padx=15, pady=5, sticky='news')

        # ----- Method when the app Working -----
        # Value_combobox()
        refresh_combobox()
        Light_Theme()
        # update_tree()


if __name__ == '__main__':
    root = tk.Tk()
    window = WindowApp(root)
    root.mainloop()
