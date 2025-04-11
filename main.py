from ui.app_interface import App
import os

if __name__ == "__main__":
    try:
        app = App()
        icon_path = os.path.join("assets", "icono.ico")
        
        if os.path.exists(icon_path):
            app.iconbitmap(default=icon_path)
        else:
            print(f"Warning: Icon file not found at {icon_path}. Continuing without setting an icon.")
        
        app.mainloop()
    except FileNotFoundError as fnf_error:
        print(f"File error: {fnf_error}")
    except ImportError as imp_error:
        print(f"Import error: {imp_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
