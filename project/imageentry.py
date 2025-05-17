import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector

class ImageEntry:
    def __init__(self, root):
        self.root = root
        self.root.title("University Fund System")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#D7D4F0")

        title_label = tk.Label(root, text="Upload Required Documents", font=("Arial", 18, "bold"), bg="#D7D4F0")
        title_label.pack(pady=10)

        paragraph = tk.Label(root, text="Please upload the required documents for verification. "
                                        "Ensure that all images are clear and readable.", 
                             font=("Arial", 12), wraplength=800, bg="#D7D4F0", justify="center")
        paragraph.pack(pady=10)

        self.frame = tk.Frame(root, bg="#D7D4F0")
        self.frame.pack(pady=20)

        self.image_paths = {
            "domicile": {"path": None, "label": None},
            "payslip": {"path": None, "label": None},
            "cnic_front": {"path": None, "label": None},
            "cnic_back": {"path": None, "label": None},
            "last_result": {"path": None, "label": None}
        }

        self.create_image_section("Domicile", "domicile", 0, 0)
        self.create_image_section("Payslip", "payslip", 0, 1)
        self.create_image_section("CNIC Front", "cnic_front", 0, 2)
        self.create_image_section("CNIC Back", "cnic_back", 1, 0)
        self.create_image_section("Last Result", "last_result", 1, 1)

        button_frame = tk.Frame(root, bg="#D7D4F0")
        button_frame.pack(pady=10)

        self.submit_button = tk.Button(button_frame, text="Submit", font=("Arial", 14), command=self.submit_data,
                                       bg="black", fg="white", width=12, height=1)
        self.submit_button.pack(side=tk.LEFT, padx=170)

        self.next_button = tk.Button(button_frame, text="Next", font=("Arial", 14), command=self.next,
                                     bg="black", fg="white", width=12, height=1)
        self.next_button.pack(side=tk.LEFT, padx=170)

    def create_image_section(self, label_text, key, row, col):
        frame = tk.Frame(self.frame, bg="#D7D4F0")
        frame.grid(row=row, column=col, padx=20, pady=10)

        button = tk.Button(frame, text=f"Browse {label_text}", font=("Arial", 12),
                           command=lambda: self.browse_image(key))
        button.pack()

        label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="lightgrey", width=20, height=10, relief="solid")
        label.config(width=20, height=10)
        label.pack()
        self.image_paths[key]["label"] = label

    def browse_image(self, key):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if filepath:
             if not (filepath.lower().endswith(".png") or filepath.lower().endswith(".jpg") or filepath.lower().endswith(".jpeg")):
                messagebox.showerror("Invalid File", "Only PNG and JPG images are allowed.")
                return
        
        self.image_paths[key]["path"] = filepath
        self.display_image(filepath, key)
    def display_image(self, filepath, key):
        try:
            image = Image.open(filepath)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(image)

            label = self.image_paths[key]["label"]
            label.config(image=image, width=150, height=150)
            label.image = image
        except Exception as e:
            print(f"Error loading image: {e}")

    def submit_data(self):
        if not all(entry["path"] for entry in self.image_paths.values()):
            messagebox.showerror("Error", "Please select all images before submitting.")
            return
        self.save_to_database()

    def save_to_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="data"
            )
            cursor = conn.cursor()
            query = """INSERT INTO user_data (domicilepath, payslippath, cnic_front, cnic_back, last_result) 
                        VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (
                self.image_paths["domicile"]["path"],
                self.image_paths["payslip"]["path"],
                self.image_paths["cnic_front"]["path"],
                self.image_paths["cnic_back"]["path"],
                self.image_paths["last_result"]["path"]
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Images uploaded successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def next(self):
       new_window = tk.Toplevel(self.root)
       new_window.title("Application Submitted")
       new_window.geometry("1920x1080")  
       new_window.configure(bg="#D7D4F0")
       label = tk.Label(new_window, text="Thank you, your application has been proceeded.",
                     font=("Arial", 16, "bold"), bg="#D7D4F0")
       label.pack(pady=20)
       try:
         image = Image.open("thank.png") 
         image = image.resize((300, 300), Image.Resampling.LANCZOS)  
         img = ImageTk.PhotoImage(image)
         image_label = tk.Label(new_window, image=img, bg="#D7D4F0")
         image_label.image = img  
         image_label.pack(pady=20)
       except Exception as e:
          error_label = tk.Label(new_window, text=f"Error loading image: {e}", fg="red", bg="#D7D4F0")
          error_label.pack()
       ok_button = tk.Button(new_window, text="OK", font=("Arial", 14), command=self.ok,
                          bg="black", fg="white", width=10)
       ok_button.pack(pady=20)
    def ok(self):
        for widget in self.root.winfo_children():  
            widget.destroy()
        from main import UniversityFundSystem
        UniversityFundSystem(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEntry(root)
    root.mainloop()