import customtkinter as ctk
import datetime

class LoggerWidget(ctk.CTkTextbox):
    """
    Custom widget turunan dari CTkTextbox untuk menampilkan console log 
    dengan cap waktu (timestamp).
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # Warna teks: Hijau tua (Light Mode), Hijau Emerald (Dark Mode)
        self.configure(state="disabled", text_color=("#006400", "#10B981"), font=ctk.CTkFont(family="Calibri", size=14)) 

    def log(self, message):
        """Menambahkan pesan ke dalam log."""
        self.configure(state="normal")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.insert("end", f"[{timestamp}] {message}\n")
        self.see("end") # auto scroll ke paling bawah
        self.configure(state="disabled")
