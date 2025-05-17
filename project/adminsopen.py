import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Scrollbar
from PIL import Image, ImageTk, ImageDraw
import mysql.connector
import os
import subprocess

BG_COLOR = "#D7D4F0"

class StudentProfile:
    def __init__(self, root):
        self.root = root
        self.root.title("University Fund System")
        self.root.geometry("1920x1080")
        self.root.configure(bg=BG_COLOR)
        self.image_references = []  # Store images to prevent garbage collection

        self.setup_ui()
        self.fetch_students()

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost", user="root", password="", database="data"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def fetch_students(self):
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            students = cursor.fetchall()
            conn.close()
            self.display_students(students)

    def setup_ui(self):
        # Welcome Message
        welcome_label = tk.Label(self.root, text="Welcome to the Student Management System!\nThis system provides detailed information about every student, allowing you to view and manage their profiles efficiently.", 
                                 font=("Arial", 16, "bold"), bg=BG_COLOR, fg="black", justify="center", wraplength=800)
        welcome_label.pack(pady=20)

        # Scrollable Frame Setup
        self.canvas = Canvas(self.root, bg=BG_COLOR, highlightthickness=4)
        self.scrollbar = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#f0f0f2")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, pady=10)  # Moved slightly lower
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def display_students(self, students):
        if students:
            for student in students:
                frame = tk.Frame(self.scroll_frame, bd=2, relief="ridge", padx=15, pady=10, bg="white")
                frame.pack(pady=5, padx=15, fill="x")

                image_path = self.validate_path(student.get("image_path", "default_profile.png"))
                img = self.load_profile_image(image_path, (60, 60))

                if img:
                    img_label = tk.Label(frame, image=img, bg="grey", cursor="hand2")
                    img_label.pack(side="left", padx=10)
                    img_label.bind("<Button-1>", lambda event, path=image_path: self.open_full_image(path))
                    self.image_references.append(img)

                name_label = tk.Label(frame, text=f"ID: {student['id']}", font=("Arial", 14, "bold"), bg="white")
                name_label.pack(side="left", padx=10)

                btn = ttk.Button(frame, text="View Profile", command=lambda s=student: self.open_profile_window(s))
                btn.pack(side="right", padx=10)
        else:
            tk.Label(self.root, text="No students found in the database.", font=("Arial", 14), bg="#f0f0f0").pack(pady=20)

    def validate_path(self, path):
        """ Validate file path and return a proper value """
        if not path or not os.path.exists(path):
            print(f"[WARNING] Path does not exist: {path}")
            return "not_available.png"  # Provide a default placeholder image
        return path

    def load_profile_image(self, image_path, size=(80, 80)):
        try:
            img = Image.open(image_path).resize(size, Image.LANCZOS)
            mask = Image.new("L", size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size[0], size[1]), fill=255)
            img.putalpha(mask)
            return ImageTk.PhotoImage(img)
        except Exception:
            print(f"[ERROR] Failed to load image: {image_path}")
            return None

    def open_full_image(self, image_path):
        if os.path.exists(image_path):
            try:
                if os.name == 'nt':
                    os.startfile(image_path)
                else:
                    subprocess.run(["xdg-open" if os.uname().sysname != 'Darwin' else "open", image_path])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open image: {e}")
        else:
            messagebox.showerror("Error", "Image not found!")

    def open_profile_window(self, student):
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"Profile - {student['id']}")
        profile_window.geometry("1920x1080")
        profile_window.configure(bg=BG_COLOR)

        image_path = self.validate_path(student.get("image_path", "default_profile.png"))
        img = self.load_profile_image(image_path, (120, 120))

        if img:
            img_label = tk.Label(profile_window, image=img, bg="#f7f7f7")
            img_label.pack(pady=10)
            self.image_references.append(img)

        details_frame = tk.Frame(profile_window, bg=BG_COLOR)
        details_frame.pack(pady=10, padx=20, fill="both")

        for key, value in student.items():
            if key not in ["image_path", "bformpath", "domicilepath", "payslippath"]:
                tk.Label(details_frame, text=f"{key.capitalize()}: {value}", font=("Arial", 12), bg="#f7f7f7").pack(anchor="w", padx=20, pady=3)

        self.create_clickable_label(profile_window, "B-Form", self.validate_path(student.get("bformpath")))
        self.create_clickable_label(profile_window, "Domicile", self.validate_path(student.get("domicilepath")))
        self.create_clickable_label(profile_window, "Pay Slip", self.validate_path(student.get("payslippath")))

    def create_clickable_label(self, parent, label_text, path):
        if path and os.path.exists(path):
            label = tk.Label(parent, text=f"{label_text}: {os.path.basename(path)}", font=("Arial", 12, "bold"), fg="blue", cursor="hand2", bg="#f7f7f7")
            label.pack(anchor="w", padx=20, pady=2)
            label.bind("<Button-1>", lambda event, p=path: self.open_full_image(p))
        else:
            tk.Label(parent, text=f"{label_text}: Not Available", font=("Arial", 12), bg="#f7f7f7").pack(anchor="w", padx=20, pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentProfile(root)
    root.mainloop()
