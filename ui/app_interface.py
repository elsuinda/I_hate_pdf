import sys
import os
import winsound  # Para reproducir sonidos en Windows

# Asegurarse de que el directorio 'utils' esté en el sys.path
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils'))
if (utils_path not in sys.path):
    sys.path.append(utils_path)

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES  # Importar TkinterDnD y DND_FILES
except ImportError:
    raise ImportError("El módulo 'tkinterdnd2' no está instalado. Instálalo con 'pip install tkinterdnd2'.")

import customtkinter as ctk
from PIL import Image, UnidentifiedImageError
from tkinter import filedialog, messagebox
from utils.file_converter import FileConverter

class App(TkinterDnD.Tk):  # Cambiar la herencia para usar TkinterDnD.Tk
    def __init__(self):
        super().__init__()
        self.title("I_hate_pdf")
        self.geometry("800x600")
        self.configure(bg="white")  # Cambiar fg_color a bg para TkinterDnD.Tk
        self.mode = "light"
        self.filepath = None  # Inicializar filepath como None

        # Configuración de apariencia de customtkinter
        ctk.set_appearance_mode("Light")  # O "Dark" para modo oscuro

        logo_path = os.path.join("assets", "logo.png")
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"El archivo de logo '{logo_path}' no existe.")
        
        try:
            self.logo_img = ctk.CTkImage(Image.open(logo_path), size=(200, 200))
        except UnidentifiedImageError:
            raise ValueError(f"El archivo '{logo_path}' no es una imagen válida.")

        self.create_widgets()

        # Title
        self.title_label = ctk.CTkLabel(self, text="I_hate_pdf", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)

        # Label para mostrar el path del archivo cargado
        self.filepath_label = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"), text_color="red", fg_color="black")
        self.filepath_label.pack(pady=10)

    def create_widgets(self):
        logo_label = ctk.CTkLabel(self, image=self.logo_img, text="")
        logo_label.pack(pady=30)

        # Mode toggle
        self.mode_button = ctk.CTkButton(self, text="Modo Oscuro", command=self.toggle_mode)
        self.mode_button.pack(pady=10)

        # Drag and Drop Frame
        self.drag_frame = ctk.CTkFrame(self, width=400, height=100, fg_color="lightgray")
        self.drag_frame.pack(pady=20)
        self.drag_label = ctk.CTkLabel(self.drag_frame, text="Arrastre aquí su archivo a convertir o presione el botón cargar archivo a convertir")
        self.drag_label.pack(pady=10)
        self.drag_frame.drop_target_register(DND_FILES)
        self.drag_frame.dnd_bind("<<Drop>>", self.handle_drop)

        # File selection
        self.file_button = ctk.CTkButton(self, text="Cargar Archivo", command=self.select_file)
        self.file_button.pack(pady=10)

        # Conversion options
        self.convert_to_word = ctk.CTkButton(self, text="Convertir a Word", command=lambda: self.convert("word"))
        self.convert_to_word.pack(pady=10)

        self.convert_to_excel = ctk.CTkButton(self, text="Convertir a Excel", command=lambda: self.convert("excel"))
        self.convert_to_excel.pack(pady=10)

        self.convert_to_pdf = ctk.CTkButton(self, text="Convertir a PDF", command=lambda: self.convert("pdf"))
        self.convert_to_pdf.pack(pady=10)

        # Footer message
        self.footer_label = ctk.CTkLabel(self, text="Gracias por usar este programa y no usar otras soluciones inseguras - by ElSuinda @v@", text_color="orange")
        self.footer_label.pack(side="bottom", pady=10)

    def toggle_mode(self):
        self.mode = "dark" if self.mode == "light" else "light"
        import customtkinter as ctk
        ctk.set_appearance_mode(self.mode)

        if self.mode == "dark":
            self.configure(bg="black")
            self.title_label.configure(text_color="green")
            self.footer_label.configure(text_color="orange")
            self.mode_button.configure(text="Modo Claro", fg_color="maroon", text_color="green")
            self.file_button.configure(fg_color="maroon", text_color="green")
            self.convert_to_word.configure(fg_color="maroon", text_color="green")
            self.convert_to_excel.configure(fg_color="maroon", text_color="green")
            self.convert_to_pdf.configure(fg_color="maroon", text_color="green")
        else:
            self.configure(bg="white")
            self.title_label.configure(text_color="black")
            self.footer_label.configure(text_color="orange")
            self.mode_button.configure(text="Modo Oscuro", fg_color="blue", text_color="white")
            self.file_button.configure(fg_color="blue", text_color="white")
            self.convert_to_word.configure(fg_color="blue", text_color="white")
            self.convert_to_excel.configure(fg_color="blue", text_color="white")
            self.convert_to_pdf.configure(fg_color="blue", text_color="white")

    def select_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("PDF, Word, Excel", "*.pdf;*.docx;*.xlsx;*.ods")])
        if self.filepath:
            print(f"Selected file: {self.filepath}")
            # Mostrar el path del archivo cargado en el label
            self.filepath_label.configure(text=f"Archivo cargado: {self.filepath}")

    def handle_drop(self, event):
        self.filepath = event.data.strip('{}')  # Remove curly braces from the path
        print(f"File dropped: {self.filepath}")
        # Mostrar el path del archivo cargado en el label
        self.filepath_label.configure(text=f"Archivo cargado: {self.filepath}")

    def convert(self, target_format):
        if not hasattr(self, "filepath") or not self.filepath:
            messagebox.showerror("Error", "¡No se ha seleccionado ningún archivo!")
            return
        try:
            print(f"Converting {self.filepath} to {target_format}...")
            output_path = FileConverter.convert(self.filepath, target_format)
            messagebox.showinfo("Conversión Completa", f"Se realizó la conversión y el resultado fue guardado en: {output_path}")
            # Ocultar el mensaje del archivo cargado después de la conversión
            self.filepath_label.configure(text="")
            self.filepath = None  # Reiniciar filepath después de la conversión
            # Reproducir sonido de éxito
            sound_path = os.path.join("assets", "success.wav")
            if os.path.exists(sound_path):
                winsound.PlaySound(sound_path, winsound.SND_FILENAME)
            else:
                print(f"Archivo de sonido no encontrado en: {sound_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la conversión: {e}")
