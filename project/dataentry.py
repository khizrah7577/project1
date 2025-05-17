import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from imageentry import ImageEntry
class Dataentry:
    def __init__(self, root):
        self.root = root
        self.root.title("University Fund System - Data Entry Form")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#d3cce3")
        self.create_form()
        self.create_buttons()
    def create_form(self):
        self.form_frame = tk.Frame(self.root, bg="#cbc3e3", padx=20, pady=20, relief="groove", borderwidth=2)
        self.form_frame.pack(pady=50)
        title_label = tk.Label(self.form_frame, text="User Information", font=("Arial", 12, "bold"), bg="#cbc3e3")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        labels = ["Name", "Father Name", "Phone", "Department", "Type", "Roll No",
                  "Address", "CNIC", "Gender", "Age"]
        self.entries = {}
        row_index = 1
        for i in range(0, len(labels), 3):
            for col_index, label in enumerate(labels[i:i + 3]):
                tk.Label(self.form_frame, text=label, bg="#cbc3e3", font=("Arial", 10)).grid(row=row_index, column=col_index, padx=10, pady=5)
                if label == "Department":
                    self.entries[label] = ttk.Combobox(self.form_frame, values=["CS", "HND", "ENGLISH", "VCD", "PSYCHOLOGY"], state="readonly", width=20)
                elif label == "Type":
                    self.entries[label] = ttk.Combobox(self.form_frame, values=["Merit", "Need"], state="readonly", width=20)
                elif label == "Gender":
                    self.entries[label] = ttk.Combobox(self.form_frame, values=["Male", "Female"], state="readonly", width=20)
                elif label == "Age":
                    self.entries[label] = ttk.Combobox(self.form_frame, values=[str(i) for i in range(18, 60)], state="readonly", width=5)
                else:
                    self.entries[label] = tk.Entry(self.form_frame, width=25)
                
                self.entries[label].grid(row=row_index + 1, column=col_index, padx=10, pady=5)
            
            row_index += 2
    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#d3cce3")
        btn_frame.pack(pady=20) 
        self.submit_btn = tk.Button(btn_frame, text="Submit", width=15,height=2,bg="#5A5A5A", fg="white", command=self.submit_data)
        self.submit_btn.grid(row=0, column=0, padx=20)
        self.clear_btn = tk.Button(btn_frame, text="Clear", width=15,height=2,bg="#5A5A5A", fg="white", command=self.clear_fields)
        self.clear_btn.grid(row=0, column=1, padx=20) 
        self.next_btn = tk.Button(btn_frame, text="Next", width=15,height=2,bg="#5A5A5A", fg="white", command=self.next_action)
        self.next_btn.grid(row=0, column=2, padx=20)   
    def connection(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="data"
            )
            return conn
        except mysql.connector.Error as er:
             messagebox.showerror("Database Error", f"{er}")
             return None
    def submit_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="university_fund")
            cursor = conn.cursor()
            query = "INSERT INTO user_data (name, fathername, phone, department, type, rollno, address, cnic, gender, age) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = tuple(self.entries[label].get() for label in self.entries) 
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            
            print("Data saved successfully!")
        except Exception as e:
            print("Error:", e)
    def clear_fields(self):
        for entry in self.entries.values():
            entry.set("") if isinstance(entry, ttk.Combobox) else entry.delete(0, tk.END)
    def next_action(self):
         for widget in self.root.winfo_children():
            widget.destroy()
         self.new_window = ImageEntry(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = Dataentry(root)
    root.mainloop()