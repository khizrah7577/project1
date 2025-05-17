from tkinter import Tk, Label, Button, Canvas
from PIL import Image, ImageTk
from login import FundManagementApp
from administrativelogin import FundManagement
class UniversityFundSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("University Fund System")
        self.master.geometry("1920x1080")
        image = Image.open("background.png")  
        self.bg_image = ImageTk.PhotoImage(image.resize((1800, 900)))
        self.canvas = Canvas(self.master, width=1200, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        self.title_label = Label(self.master, text="WELCOME TO FUND MANAGEMENT SYSTEM",font=("Arial", 24, "bold"), bg="#000", fg="white", padx=10, pady=5)
        self.title_label.place(relx=0.5, rely=0.22, anchor="center")
        btn_style = {"width": 15, "height": 2, "font": ("Arial", 12, "bold"), "bg": "#4CAF50", "fg": "white"}
        self.student_btn = Button(self.master, text="Student", **btn_style, command=self.student_click)
        self.admin_btn = Button(self.master, text="Administration", **btn_style, command=self.admin_click)
        self.student_btn.place(relx=0.50, rely=0.57, anchor="center")
        self.admin_btn.place(relx=0.68, rely=0.57, anchor="center")
    def student_click(self):
        for widget in self.master.winfo_children():  
            widget.destroy()
        obj = FundManagementApp(self.master)  
    def admin_click(self):
        for widget in self.master.winfo_children():  
            widget.destroy()
        obj1 = FundManagement(self.master) 
if __name__ == "__main__":
    root = Tk()
    app = UniversityFundSystem(root)
    root.mainloop()
