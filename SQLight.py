import tkinter as tk
from tkinter import messagebox
import sqlite3


class DatabaseCreatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("SQLite Database Creator")
        
        self.label = tk.Label(master, text="Enter Table Name:")
        self.label.grid(row=0, column=0, padx=10, pady=5)
        
        self.table_name_entry = tk.Entry(master)
        self.table_name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.add_column_button = tk.Button(master, text="Add Column", command=self.add_column)
        self.add_column_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.create_button = tk.Button(master, text="Create Database", command=self.create_database)
        self.create_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.columns = []
        
    def add_column(self):
        column_frame = tk.Frame(self.master)
        column_frame.grid(row=len(self.columns) + 3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        label = tk.Label(column_frame, text="Column Name:")
        label.grid(row=0, column=0, padx=5, pady=5)
        
        column_name_entry = tk.Entry(column_frame)
        column_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        data_type_label = tk.Label(column_frame, text="Data Type:")
        data_type_label.grid(row=0, column=2, padx=5, pady=5)
        
        data_type_entry = tk.Entry(column_frame)
        data_type_entry.grid(row=0, column=3, padx=5, pady=5)
        
        self.columns.append((column_name_entry, data_type_entry))
        
    def create_database(self):
        table_name = self.table_name_entry.get().strip()
        if not table_name:
            messagebox.showerror("Error", "Please enter a table name.")
            return
        
        if not self.columns:
            messagebox.showerror("Error", "Please add at least one column.")
            return
        
        columns_info = []
        for column_name_entry, data_type_entry in self.columns:
            column_name = column_name_entry.get().strip()
            data_type = data_type_entry.get().strip()
            if not column_name or not data_type:
                messagebox.showerror("Error", "Please fill in all column names and data types.")
                return
            columns_info.append((column_name, data_type))
        
        try:
            conn = sqlite3.connect("{}.db".format(table_name))
            c = conn.cursor()
            
            columns_str = ", ".join(["{} {}".format(name, data_type) for name, data_type in columns_info])
            c.execute("CREATE TABLE {} ({})".format(table_name, columns_str))
            
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Database {} created successfully.".format(table_name))
        except Exception as e:
            messagebox.showerror("Error", "An error occurred: {}".format(str(e)))

def main():
    root = tk.Tk()
    app = DatabaseCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
