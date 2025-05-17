import tkinter as tk
from tkinter import messagebox, Canvas
import mysql.connector
from PIL import Image, ImageTk 
from adminsopen import StudentProfile
BG_COLOR = "#D7D4F0"
class FundManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Fund Management System")
        self.root.geometry("1920x1080") 
        self.root.configure(bg=BG_COLOR)
        self.create_login_form()
    def connection(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="admin"
            )
            return conn
        except mysql.connector.Error as er:
            messagebox.showerror("Database Error", f"{er}")
            return None
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        conn = self.connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM infor WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            conn.close()
            if result:
                for widget in self.root.winfo_children():
                    widget.destroy()
                StudentProfile(self.root)  
            else:
                messagebox.showerror("Login Failed", "Invalid username or password!")
    def reset_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    def create_login_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.canvas = tk.Canvas(self.root, width=1920, height=1080, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        bg_image = Image.open("image.png") 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight() 
        login_x = screen_width // 2
        login_y = screen_height //2-100
        img_x = login_x
        img_y = login_y -200 
        self.bg_image = ImageTk.PhotoImage(bg_image.resize((600, 400)))
        self.canvas.create_image(img_x, img_y, anchor="center", image=self.bg_image)
        frame = tk.Frame(self.root, bg="#ffffff")
        frame.place(relx=0.5, rely=0.55, anchor="center")
        login_frame = tk.LabelFrame(self.root, text="User Login", font=("Arial", 12, "bold"),bg=BG_COLOR)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=200)
        tk.Label(login_frame, text="Username:", font=("Times New Roman", 14,"bold"),bg=BG_COLOR).grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(login_frame, width=40)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(login_frame, text="Password:", font=("Times New Roman", 14,"bold"),bg=BG_COLOR).grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(login_frame, show="*", width=40)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(login_frame, text="Login", width=15, bg="#5A5A5A", fg="white",command=self.login).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(login_frame, text="Cancel", width=15,bg="#5A5A5A", fg="white", command=self.reset_fields).grid(row=2, column=1, padx=10, pady=10)
if __name__ == "__main__":
    root = tk.Tk()
    app = FundManagement(root)
    root.mainloop()
