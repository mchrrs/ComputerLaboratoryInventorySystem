import tkinter as tk
from tkinter import PhotoImage, StringVar, OptionMenu
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import random
from datetime import datetime
from tkinter import ttk

class InventorySystem:
    def __init__(self):
        self.create_login_widgets()
        self.root = tk.Tk()
        self.root.title("Computer Laboratory Inventory System - Admin Login")
        self.root.geometry("1100x619")
        self.root.resizable(False, False)
        
        background_image_admin = Image.open("assets/background_main.jpg")
        self.background_photo_admin = ImageTk.PhotoImage(background_image_admin)

        self.background_label_admin = tk.Label(self.root, image=self.background_photo_admin)
        self.background_label_admin.place(relwidth=1, relheight=1)

        self.set_window_icon_photo(self.root)
        self.create_login_widgets()
    
    def set_window_icon_photo(self, window):
        image_path = 'assets/icon.png'
        icon_image = Image.open(image_path)
        window.iconphoto(True, ImageTk.PhotoImage(icon_image))

    def create_login_widgets(self):
        self.root = tk.Tk()
        self.root.title("Computer Laboratory Inventory System - Admin Login")
        self.root.geometry("1100x619")
        self.root.resizable(False, False)

        try:
            background_image_admin = Image.open("assets/admin.png")
            self.background_photo_admin = ImageTk.PhotoImage(background_image_admin)
        except IOError as e:
            print(f"Error loading background image: {e}")
            return

        self.background_label_admin = tk.Label(self.root, image=self.background_photo_admin)
        self.background_label_admin.place(relwidth=1, relheight=1)

        self.set_window_icon_photo(self.root)

        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.login, bg="green", fg="white", activebackground="green")
        login_button.grid(row=3, column=1, pady=20)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.root.mainloop()

    def open_homepage(self):
        self.homepage = tk.Toplevel()
        self.homepage.title("Computer Laboratory Inventory System")
        self.homepage.geometry("1100x619")
        self.homepage.resizable(False, False)

        background_image_homepage = Image.open("assets/background_main.jpg")
        background_photo_homepage = ImageTk.PhotoImage(background_image_homepage)

        background_label_homepage = tk.Label(self.homepage, image=background_photo_homepage)
        background_label_homepage.image = background_photo_homepage
        background_label_homepage.place(relwidth=1, relheight=1)

      
        
        button_params = {"width": 15, "height": 1, "font": ("Helvetica", 10)}

        add_part_button = tk.Button(self.homepage, text="Add Part", command=self.open_add_computer_part, **button_params)
        view_inventory_button = tk.Button(self.homepage, text="Refresh", command=lambda: self.populate_inventory_tree(tree), **button_params)
        view_serviceable_button = tk.Button(self.homepage, text="Serviceable Parts", command=self.view_serviceable_parts, **button_params)
        view_unserviceable_button = tk.Button(self.homepage, text="Unserviceable Parts", command=self.view_unserviceable_parts, **button_params)
        repair_part_button = tk.Button(self.homepage, text="Repair a Part", command=self.open_repair_part, **button_params)
        maintenance_records_button = tk.Button(self.homepage, text="Maintenance Records", command=self.open_maintenance_records, **button_params)
        delete_part_button = tk.Button(self.homepage, text="Delete Record", command=self.open_delete_part, **button_params)
        logout_button = tk.Button(self.homepage, text="Logout", bg="red", command=self.logout, **button_params)

        buttons = [add_part_button, view_inventory_button, view_serviceable_button,
                   view_unserviceable_button, repair_part_button, maintenance_records_button,
                   delete_part_button, logout_button]

        for i, button in enumerate(buttons):
            button.grid(row=1, column=i, padx=5, pady=5)
            
        tree = ttk.Treeview(self.homepage, style="Custom.Treeview")
        tree["columns"] = ("Record Number", "Computer Part", "Model", "Status", "Quantity", "Date Recorded", "Room Number")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Record Number", anchor=tk.CENTER, width=100)
        tree.column("Computer Part", anchor=tk.CENTER, width=150)
        tree.column("Model", anchor=tk.CENTER, width=100)
        tree.column("Status", anchor=tk.CENTER, width=80)
        tree.column("Quantity", anchor=tk.CENTER, width=60)
        tree.column("Date Recorded", anchor=tk.CENTER, width=100)
        tree.column("Room Number", anchor=tk.CENTER, width=80)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Record Number", text="Record Number", anchor=tk.CENTER)
        tree.heading("Computer Part", text="Computer Part", anchor=tk.CENTER)
        tree.heading("Model", text="Model", anchor=tk.CENTER)
        tree.heading("Status", text="Status", anchor=tk.CENTER)
        tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
        tree.heading("Date Recorded", text="Date Recorded", anchor=tk.CENTER)
        tree.heading("Room Number", text="Room Number", anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Custom.Treeview", padding=(5, 2))

        self.populate_inventory_tree(tree)
        tree.grid(row=2, column=0, columnspan=8, pady=10, padx=10, sticky="nsew")
        self.homepage.grid_rowconfigure(2, weight=1)
        self.homepage.grid_columnconfigure(0, weight=1)


    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "1234":
            self.open_homepage()
            self.root.withdraw()
        else:
            tk.messagebox.showerror("Unauthorized", "Invalid username or password")

    def view_serviceable_parts(self):
        self.view_parts_from_database("serviceable.db", "Serviceable Parts")


    def view_unserviceable_parts(self):
        self.view_parts_from_database("unserviceable.db", "Unserviceable Parts")

    def view_parts_from_database(self, database_name, window_title):
        parts_window = tk.Toplevel()
        parts_window.title(window_title)
        parts_window.geometry("800x400")

        parts_tree = ttk.Treeview(parts_window)
        parts_tree["columns"] = ("Record Number", "Computer Part", "Model", "Quantity", "Date Recorded", "Room Number")

        parts_tree.column("#0", width=0, stretch=tk.NO)
        parts_tree.column("Record Number", anchor=tk.CENTER, width=100)
        parts_tree.column("Computer Part", anchor=tk.CENTER, width=150)
        parts_tree.column("Model", anchor=tk.CENTER, width=100)
        parts_tree.column("Quantity", anchor=tk.CENTER, width=60)
        parts_tree.column("Date Recorded", anchor=tk.CENTER, width=100)
        parts_tree.column("Room Number", anchor=tk.CENTER, width=80)

        parts_tree.heading("#0", text="", anchor=tk.W)
        parts_tree.heading("Record Number", text="Record Number", anchor=tk.CENTER)
        parts_tree.heading("Computer Part", text="Computer Part", anchor=tk.CENTER)
        parts_tree.heading("Model", text="Model", anchor=tk.CENTER)
        parts_tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
        parts_tree.heading("Date Recorded", text="Date Recorded", anchor=tk.CENTER)
        parts_tree.heading("Room Number", text="Room Number", anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Custom.Treeview", padding=(5, 2))

        self.populate_parts_tree(parts_tree, database_name)

        parts_tree.pack(expand=tk.YES, fill=tk.BOTH)

    def populate_parts_tree(self, tree, database_name):
        table_name = "computer_parts"
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} "
                       "(id INTEGER PRIMARY KEY, record_number TEXT, part_name TEXT, model TEXT, status TEXT, "
                       "quantity INTEGER, date_recorded TEXT, room_number TEXT)")

        cursor.execute(f"SELECT record_number, part_name, model, quantity, date_recorded, room_number FROM {table_name}")
        data = cursor.fetchall()
        connection.close()
        tree.delete(*tree.get_children())

        for row in data:
            tree.insert("", tk.END, values=row)

    def open_add_computer_part(self):
        add_computer_part_window = tk.Toplevel()
        add_computer_part_window.title("Add Computer Part")
        add_computer_part_window.geometry("275x350")

        tk.Label(add_computer_part_window, text="Computer Part:").grid(row=0, column=0, pady=8, padx=10, sticky="w")
        computer_part_var = StringVar(add_computer_part_window)
        computer_parts = [
                        "CPU", "Motherboard", "Memory (RAM)",
                        "HDD", "SSD", "GPU", "PSU", "Computer Case (Chassis)", "CPU Cooler",
                        "Case Fans","GPU Cooler", "Keyboard", "Mouse","Webcam", "Microphone", "Monitor", "Speakers", "Printer",
                        "Network Interface Card (NIC)", "Router", "Modem", "Sound Card", "External Storage)", "USB Flash Drive",
                        "Card Reader", "Power Cables", "SATA", "HDMI", "USB", "BIOS/UEFI", "Operating System (OS)"
                    ]
        computer_part_var.set(computer_parts[0])
        computer_part_option_menu = OptionMenu(add_computer_part_window, computer_part_var, *computer_parts)
        computer_part_option_menu.grid(row=0, column=1, pady=8, padx=10, sticky="ew")

        tk.Label(add_computer_part_window, text="Model:").grid(row=1, column=0, pady=8, padx=10, sticky="w")
        model_entry = tk.Entry(add_computer_part_window)
        model_entry.grid(row=1, column=1, pady=8, padx=10, sticky="ew")

        tk.Label(add_computer_part_window, text="Status:").grid(row=2, column=0, pady=8, padx=10, sticky="w")
        status_var = StringVar(add_computer_part_window)
        status_var.set("Serviceable")
        status_option_menu = OptionMenu(add_computer_part_window, status_var, "Serviceable", "Unserviceable")
        status_option_menu.grid(row=2, column=1, pady=8, padx=10, sticky="ew")

        tk.Label(add_computer_part_window, text="Quantity:").grid(row=3, column=0, pady=8, padx=10, sticky="w")
        quantity_entry = tk.Entry(add_computer_part_window)
        quantity_entry.grid(row=3, column=1, pady=8, padx=10, sticky="ew")

        tk.Label(add_computer_part_window, text="Date Recorded:").grid(row=4, column=0, pady=8, padx=10, sticky="w")
        date_entry = tk.Entry(add_computer_part_window)
        date_entry.grid(row=4, column=1, pady=8, padx=10, sticky="ew")

        tk.Label(add_computer_part_window, text="Room:").grid(row=5, column=0, pady=8, padx=10, sticky="w")
        room_var = StringVar(add_computer_part_window)
        room_var.set("Room 101")
        room_option_menu = OptionMenu(add_computer_part_window, room_var, "Room 101", "Room 102", "Room 103",
                                      "Room 104", "Room 105", "Room 106", "Room 107", "Room 108", "Room 109", "Room 110")
        room_option_menu.grid(row=5, column=1, pady=8, padx=10, sticky="ew")

        tk.Button(
            add_computer_part_window,
            text="Add to Inventory",
            command=lambda: self.add_to_inventory(
                computer_part_var.get(), model_entry.get(),
                status_var.get(), quantity_entry.get(),
                date_entry.get(), room_var.get()
            ),
            font=("Arial", 10),
            width=10,
            height=1,
        ).grid(row=6, column=0, columnspan=2, pady=15, padx=10, sticky="ew")


    def add_to_inventory(self, part_name, model, status, quantity, date_recorded, room_number):
        record_number = f"CRN {random.randint(0, 999999):06d}"
        inventory_connection = sqlite3.connect("inventory.db")
        inventory_cursor = inventory_connection.cursor()

        inventory_cursor.execute("CREATE TABLE IF NOT EXISTS computer_parts "
                                 "(id INTEGER PRIMARY KEY, record_number TEXT, part_name TEXT, model TEXT, status TEXT, "
                                 "quantity INTEGER, date_recorded TEXT, room_number TEXT)")

        inventory_cursor.execute("INSERT INTO computer_parts (record_number, part_name, model, status, quantity, date_recorded, room_number) "
                                 "VALUES (?, ?, ?, ?, ?, ?, ?)",
                                 (record_number, part_name, model, status, int(quantity), date_recorded, room_number))

        inventory_connection.commit()
        inventory_connection.close()
        database_name = "serviceable.db" if status == "Serviceable" else "unserviceable.db"
        table_name = "computer_parts"
        
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} "
                       "(id INTEGER PRIMARY KEY, record_number TEXT, part_name TEXT, model TEXT, status TEXT, "
                       "quantity INTEGER, date_recorded TEXT, room_number TEXT)")

        cursor.execute(f"INSERT INTO {table_name} (record_number, part_name, model, status, quantity, date_recorded, room_number) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (record_number, part_name, model, status, int(quantity), date_recorded, room_number))

        connection.commit()
        connection.close()

        tk.messagebox.showinfo("Success", "Computer part added to inventory successfully!\nRecord Number: {}".format(record_number))
  
    def open_repair_part(self):
        repair_part_window = tk.Toplevel()
        repair_part_window.title("Repair a Part")
        repair_part_window.geometry("300x100")

        label = tk.Label(repair_part_window, text="Enter Record Number:")
        label.pack(pady=5)

        record_number_entry = tk.Entry(repair_part_window)
        record_number_entry.pack(pady=5)

        repair_button = tk.Button(repair_part_window, text="Repair", command=lambda: self.repair_computer_part(record_number_entry.get(), repair_part_window))
        repair_button.pack(pady=10)

    def repair_computer_part(self, record_number, repair_part_window):
        unserviceable_connection = sqlite3.connect("unserviceable.db")
        unserviceable_cursor = unserviceable_connection.cursor()

        unserviceable_cursor.execute("SELECT * FROM computer_parts WHERE record_number=?", (record_number,))
        part_data = unserviceable_cursor.fetchone()

        unserviceable_connection.close()

        if part_data:
            self.open_repair_form(record_number, part_data)
        else:
            tk.messagebox.showerror("Error", "Computer part not found in unserviceable inventory.")
        repair_part_window.destroy()

    def open_repair_form(self, record_number, part_data):
        repair_form_window = tk.Toplevel()
        repair_form_window.title("Record Maintenance")
        repair_form_window.geometry("300x150")

        tk.Label(repair_form_window, text="Technician Name:").grid(row=0, column=0, pady=5, padx=10, sticky="w")
        technician_name_entry = tk.Entry(repair_form_window)
        technician_name_entry.grid(row=0, column=1, pady=5, padx=10, sticky="ew")

        tk.Label(repair_form_window, text="Repair Date:").grid(row=1, column=0, pady=5, padx=10, sticky="w")
        repair_date_entry = tk.Entry(repair_form_window)
        repair_date_entry.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

        tk.Label(repair_form_window, text="Repair Description:").grid(row=2, column=0, pady=5, padx=10, sticky="w")
        repair_description_entry = tk.Entry(repair_form_window)
        repair_description_entry.grid(row=2, column=1, pady=5, padx=10, sticky="ew")

        save_button = tk.Button(
            repair_form_window,
            text="Save",
            command=lambda: self.save_maintenance_record(record_number, part_data, technician_name_entry.get(), repair_date_entry.get(), repair_description_entry.get(), repair_form_window),
        )
        save_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    def save_maintenance_record(self, record_number, part_data, technician_name, repair_date, repair_description, repair_form_window):
        maintenance_connection = sqlite3.connect("maintenance.db")
        maintenance_cursor = maintenance_connection.cursor()

        maintenance_cursor.execute("CREATE TABLE IF NOT EXISTS maintenance_records "
                                   "(id INTEGER PRIMARY KEY, record_number TEXT, part_name TEXT, model TEXT, status TEXT, "
                                   "quantity INTEGER, date_recorded TEXT, room_number TEXT, technician_name TEXT, repair_date TEXT, repair_description TEXT)")

        maintenance_cursor.execute("INSERT INTO maintenance_records (record_number, part_name, model, status, quantity, date_recorded, room_number, technician_name, repair_date, repair_description) "
                                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                   (record_number, part_data[2], part_data[3], part_data[4], part_data[5], part_data[6], part_data[7], technician_name, repair_date, repair_description))

        maintenance_connection.commit()
        maintenance_connection.close()

        unserviceable_connection = sqlite3.connect("unserviceable.db")
        unserviceable_cursor = unserviceable_connection.cursor()
        unserviceable_cursor.execute("SELECT * FROM computer_parts WHERE record_number=?", (record_number,))
        part_data = unserviceable_cursor.fetchone()
        unserviceable_cursor.execute("DELETE FROM computer_parts WHERE record_number=?", (record_number,))

        unserviceable_connection.commit()
        unserviceable_connection.close()
        
        inventory_connection = sqlite3.connect("inventory.db")
        inventory_cursor = inventory_connection.cursor()

        inventory_cursor.execute("UPDATE computer_parts SET status='Serviceable' WHERE record_number=?", (record_number,))

        inventory_connection.commit()
        inventory_connection.close()

        serviceable_connection = sqlite3.connect("serviceable.db")
        serviceable_cursor = serviceable_connection.cursor()

        serviceable_cursor.execute("CREATE TABLE IF NOT EXISTS computer_parts "
                                   "(id INTEGER PRIMARY KEY, record_number TEXT, part_name TEXT, model TEXT, status TEXT, "
                                   "quantity INTEGER, date_recorded TEXT, room_number TEXT)")

        serviceable_cursor.execute("INSERT INTO computer_parts (record_number, part_name, model, status, quantity, date_recorded, room_number) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (record_number, part_data[2], part_data[3], part_data[4], part_data[5], part_data[6], part_data[7]))


        serviceable_connection.commit()
        serviceable_connection.close()

        tk.messagebox.showinfo("Success", "Maintenance record saved successfully!")
        repair_form_window.destroy()

    def open_maintenance_records(self):
        maintenance_records_window = tk.Toplevel()
        maintenance_records_window.title("Maintenance Records")
        maintenance_records_window.geometry("1100x600")
        maintenance_tree = ttk.Treeview(maintenance_records_window)
        maintenance_tree["columns"] = ("Record Number", "Computer Part", "Model", "Quantity", "Date Recorded", "Room Number", "Technician Name", "Repair Date", "Repair Description")
        maintenance_tree.column("#0", width=0, stretch=tk.NO)  # Hidden column
        maintenance_tree.column("Record Number", anchor=tk.CENTER, width=100)
        maintenance_tree.column("Computer Part", anchor=tk.CENTER, width=150)
        maintenance_tree.column("Model", anchor=tk.CENTER, width=100)
        maintenance_tree.column("Quantity", anchor=tk.CENTER, width=60)
        maintenance_tree.column("Date Recorded", anchor=tk.CENTER, width=100)
        maintenance_tree.column("Room Number", anchor=tk.CENTER, width=80)
        maintenance_tree.column("Technician Name", anchor=tk.CENTER, width=120)
        maintenance_tree.column("Repair Date", anchor=tk.CENTER, width=100)
        maintenance_tree.column("Repair Description", anchor=tk.CENTER, width=150)

        maintenance_tree.heading("#0", text="", anchor=tk.W)
        maintenance_tree.heading("Record Number", text="Record Number", anchor=tk.CENTER)
        maintenance_tree.heading("Computer Part", text="Computer Part", anchor=tk.CENTER)
        maintenance_tree.heading("Model", text="Model", anchor=tk.CENTER)
        maintenance_tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
        maintenance_tree.heading("Date Recorded", text="Date Recorded", anchor=tk.CENTER)
        maintenance_tree.heading("Room Number", text="Room Number", anchor=tk.CENTER)
        maintenance_tree.heading("Technician Name", text="Technician Name", anchor=tk.CENTER)
        maintenance_tree.heading("Repair Date", text="Repair Date", anchor=tk.CENTER)
        maintenance_tree.heading("Repair Description", text="Repair Description", anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Custom.Treeview", padding=(5, 2))

        self.populate_maintenance_records_tree(maintenance_tree)

        maintenance_tree.pack(expand=tk.YES, fill=tk.BOTH)

    def populate_maintenance_records_tree(self, tree):
        connection = sqlite3.connect("maintenance.db")
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS maintenance_records "
                       "(id INTEGER PRIMARY KEY, record_number TEXT, part_name TEXT, model TEXT, status TEXT, "
                       "quantity INTEGER, date_recorded TEXT, room_number TEXT, technician_name TEXT, repair_date TEXT, repair_description TEXT)")

        cursor.execute("SELECT record_number, part_name, model, quantity, date_recorded, room_number, technician_name, repair_date, repair_description FROM maintenance_records")
        data = cursor.fetchall()
        connection.close()

        tree.delete(*tree.get_children())

        for row in data:
            tree.insert("", tk.END, values=row)
    
    def populate_inventory_tree(self, tree):
        database_name = "inventory.db"
        table_name = "computer_parts"
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} "
                       "(id INTEGER PRIMARY KEY, record_number TEXT, part_name TEXT, model TEXT, status TEXT, "
                       "quantity INTEGER, date_recorded TEXT, room_number TEXT)")

        cursor.execute(f"SELECT record_number, part_name, model, status, quantity, date_recorded, room_number FROM {table_name}")
        data = cursor.fetchall()
        connection.close()

        tree.delete(*tree.get_children())

        for row in data:
            tree.insert("", tk.END, values=row)
            
    def open_delete_part(self):
        delete_part_window = tk.Toplevel()
        delete_part_window.title("Delete Part")
        delete_part_window.geometry("300x100")

        label = tk.Label(delete_part_window, text="Enter Record Number:")
        label.pack(pady=5)

        record_number_entry = tk.Entry(delete_part_window)
        record_number_entry.pack(pady=5)

        delete_button = tk.Button(delete_part_window, text="Delete", command=lambda: self.delete_computer_part(record_number_entry.get(), delete_part_window))
        delete_button.pack(pady=10)

    def delete_computer_part(self, record_number, delete_part_window):
        inventory_connection = sqlite3.connect("inventory.db")
        inventory_cursor = inventory_connection.cursor()

        inventory_cursor.execute("DELETE FROM computer_parts WHERE record_number=?", (record_number,))

        inventory_connection.commit()
        inventory_connection.close()

        serviceable_connection = sqlite3.connect("serviceable.db")
        serviceable_cursor = serviceable_connection.cursor()

        serviceable_cursor.execute("DELETE FROM computer_parts WHERE record_number=?", (record_number,))

        serviceable_connection.commit()
        serviceable_connection.close()

        unserviceable_connection = sqlite3.connect("unserviceable.db")
        unserviceable_cursor = unserviceable_connection.cursor()

        unserviceable_cursor.execute("DELETE FROM computer_parts WHERE record_number=?", (record_number,))

        unserviceable_connection.commit()
        unserviceable_connection.close()

        maintenance_connection = sqlite3.connect("maintenance.db")
        maintenance_cursor = maintenance_connection.cursor()

        maintenance_cursor.execute("DELETE FROM maintenance_records WHERE record_number=?", (record_number,))

        maintenance_connection.commit()
        maintenance_connection.close()

        tk.messagebox.showinfo("Success", "Computer part deleted successfully!")
        delete_part_window.destroy()

    def reset_admin_page(self):
        self.root.destroy()
        self.root = tk.Tk()
        self.root.title("Computer Laboratory Inventory System - Admin Login")
        self.root.geometry("1100x619")
        self.root.resizable(False, False)
        try:
            background_image_admin = Image.open("assets/admin.png")
            self.background_photo_admin = ImageTk.PhotoImage(background_image_admin)
        except IOError as e:
            print(f"Error loading background image: {e}")
            return

        self.background_label_admin = tk.Label(self.root, image=self.background_photo_admin)
        self.background_label_admin.place(relwidth=1, relheight=1)

        self.set_window_icon_photo(self.root)

        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.login, bg="green", fg="white", activebackground="green")
        login_button.grid(row=3, column=1, pady=20)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.homepage = None

    def logout(self):
        if self.homepage:
            self.homepage.destroy()
        self.reset_admin_page()

if __name__ == "__main__":
    inventory_system = InventorySystem()
    inventory_system.root.mainloop()