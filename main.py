from ui.app_interface import App
import os

if __name__ == "__main__":
    app = App()
    app.iconbitmap(default=os.path.join("assets", "icono.ico"))
    app.mainloop()
