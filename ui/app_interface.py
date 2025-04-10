import customtkinter as ctk
from PIL import Image
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("I_hate_pdf")
        self.geometry("600x500")
        ctk.set_appearance_mode("Light")  # O "Dark" para modo oscuro
        logo_path = os.path.join("assets", "logo.png")
        self.logo_img = ctk.CTkImage(Image.open(logo_path), size=(200, 200))
        self.create_widgets()

    def create_widgets(self):
        logo_label = ctk.CTkLabel(self, image=self.logo_img, text="")
        logo_label.pack(pady=30)
