import customtkinter as ctk
from gui.logger_widget import LoggerWidget
from gui.views.base_view import BaseView

# Import Core Handlers
from core.handlers.drafting_fk import DraftingFKHandler
from core.handlers.resub_fk import ResubFKHandler
from core.handlers.rm_merging import RMMergingHandler
from core.handlers.update_rm import UpdateRMHandler

class WelcomeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=40, pady=40)
        
        lbl = ctk.CTkLabel(container, text="Selamat Datang di Aplikasi Editor Data Pajak", font=ctk.CTkFont(family="Calibri", size=26, weight="bold"))
        lbl.pack(pady=(0, 10))
        
        desc = ctk.CTkLabel(container, text="Klik panduan menu di bawah ini untuk melihat detail/tutorialnya:", text_color="gray", font=ctk.CTkFont(family="Calibri", size=15))
        desc.pack(pady=(0, 20))
        
        # Pembagian Layout Tutorial
        tutor_frame = ctk.CTkFrame(container, fg_color="transparent")
        tutor_frame.pack(fill="both", expand=True)
        
        # Kolom Kiri: Tombol Menu
        btn_frame = ctk.CTkFrame(tutor_frame, fg_color="transparent", width=250)
        btn_frame.pack(side="left", fill="y", padx=(0, 20))
        
        # Kolom Kanan: Penjelasan (Boks teks)
        self.tutor_text = ctk.CTkTextbox(tutor_frame, font=ctk.CTkFont(family="Calibri", size=15), wrap="word", fg_color=("gray90", "gray15"))
        self.tutor_text.pack(side="left", fill="both", expand=True)
        self.tutor_text.insert("0.0", "Silakan klik salah satu tombol menu di samping untuk memunculkan teks tutorialnya di sini.\n\nAnda dapat mengisikan panduan langkah demi langkah tentang cara menggunakan menu tersebut.")
        self.tutor_text.configure(state="disabled")
        
        # Data List Menu
        from core.text_constants import TUTOR_DRAFTING_FK, TUTOR_RESUB_FK, TUTOR_RM_MERGING, TUTOR_UPDATE_RM
        
        menus = [
            ("Drafting FK", TUTOR_DRAFTING_FK),
            ("Resubmission FK", TUTOR_RESUB_FK),
            ("RM Merging", TUTOR_RM_MERGING),
            ("Update RM", TUTOR_UPDATE_RM)
        ]
        for name, tutor in menus:
            btn = ctk.CTkButton(btn_frame, text=name, command=lambda n=name, t=tutor: self.show_tutorial(n, t), fg_color=("#34495E", "#16A085"), text_color="white", hover_color=("#2C3E50", "#1ABC9C"))
            btn.pack(pady=5, fill="x")
            
    def show_tutorial(self, title, content):
        self.tutor_text.configure(state="normal")
        self.tutor_text.delete("0.0", "end")
        self.tutor_text.insert("0.0", f"--- 📖 Panduan: {title} 📖 ---\n\n{content}")
        self.tutor_text.configure(state="disabled")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Editor Data Pajak")
        self.geometry("1000x700")
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Konfigurasi grid root (2 kolom: sidebar & main)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_sidebar()
        self.setup_main_area()
        self.setup_views()
        
        # Tampilkan menu default pertama (Welcome Screen)
        self.views["Welcome"].tkraise()
        
    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="MENU NAVIGASI", font=ctk.CTkFont(family="Calibri", size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))
        
        # Daftar tombol menu
        self.menu_buttons = []
        menus = [
            ("Beranda", self.show_welcome, True),
            ("Drafting FK", self.show_drafting_fk, False),
            ("Resubmission FK", self.show_resub_fk, False),
            ("RM Merging", self.show_rm_merging, False),
            ("Update RM", self.show_update_rm, False),
            ("Keluar", self.quit, True), # Memanggil exit Tkinter
        ]
        
        for idx, (text, command, is_special) in enumerate(menus):
            if is_special:
                fg_c = "#2980B9"  # Warna Biru khusus
                hov_c = "#3498DB"
            else:
                fg_c = ("#34495E", "#16A085") # Default Teal/Slate
                hov_c = ("#2C3E50", "#1ABC9C")
                
            btn = ctk.CTkButton(self.sidebar_frame, text=text, command=command, anchor="w", 
                                font=ctk.CTkFont(family="Calibri", size=15, weight="bold" if is_special else "normal"),
                                fg_color=fg_c, 
                                text_color=("white", "white"), 
                                hover_color=hov_c)
            btn.grid(row=idx+1, column=0, padx=20, pady=(10, 20 if text == "Keluar" else 10), sticky="ew")
            self.menu_buttons.append(btn)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["System", "Light", "Dark"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set("System")
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))
        
    def setup_main_area(self):
        # Frame Kontainer utama (menampung frame menu + logger dipaling bawah)
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(0, weight=3) # Area Menu (besar)
        self.main_container.grid_rowconfigure(1, weight=1) # Area Log (kecil)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Area Dinamis untuk Menu Views
        self.views_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.views_container.grid(row=0, column=0, sticky="nsew")
        self.views_container.grid_rowconfigure(0, weight=1)
        self.views_container.grid_columnconfigure(0, weight=1)
        
        self.logger_widget = LoggerWidget(self.main_container, height=150)
        self.logger_widget.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        
        self.logger_widget.log("Aplikasi Sistem Pajak Multimenu dimulai...")
        
    def setup_views(self):
        self.views = {}
        
        # Inisialisasi masing-masing View dengan Handler khususnya
        # Semua ditaruh di self.views_container di row 0 col 0, lalu saling timpa
        
        from core.text_constants import TUTOR_RESUB_FK, TUTOR_DRAFTING_FK, TUTOR_RM_MERGING, TUTOR_UPDATE_RM
        
        self.views["Welcome"] = WelcomeView(self.views_container, fg_color="transparent")
        self.views["Drafting FK"] = BaseView(
            self.views_container, 
            "Drafting FK PKP / NON PKP", 
            self.logger_widget, 
            DraftingFKHandler(),
            description="Menu ini digunakan untuk mempersiapkan diri kamu (Dating/Drafting) sebelum ketemu si DIA (sistem PSIAP) 🌹🌹🌹.",
            tutorial=TUTOR_DRAFTING_FK
        )
        self.views["Resub FK"] = BaseView(
            self.views_container, 
            "Resubmission FK (Setelah Reject PSIAP)", 
            self.logger_widget, 
            ResubFKHandler(), 
            description="Menu ini di gunakan setelah kamu ditolak sama PSIAP. Tenang, kita coba lagi! 😊",
            tutorial=TUTOR_RESUB_FK
        )
        self.views["RM Merging"] = BaseView(
            self.views_container, 
            "RM Merging", 
            self.logger_widget, 
            RMMergingHandler(),
            description="Gabungkan berpuluh-puluh serpihan file Retur Masukan (RM) menjadi satu Kitab Sakti utuh (1 File)! �",
            tutorial=TUTOR_RM_MERGING
        )
        self.views["Update RM"] = BaseView(
            self.views_container, 
            "Update RM", 
            self.logger_widget, 
            UpdateRMHandler(),
            description="Ruang Tempa khusus menyulap baja mentah unduhan PSIAP (RM) menjadi sebilah Pedang Pusaka siap pakai (RFM). ⚔️",
            tutorial=TUTOR_UPDATE_RM
        )
        
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")
            
    def show_view(self, view_name):
        # Angkat view ke lapisan paling atas
        view = self.views[view_name]
        view.tkraise()
        if view_name == "Welcome":
            self.logger_widget.log("Beralih ke Layar Beranda")
        else:
            self.logger_widget.log(f"Beralih ke menu: {view_name}")
        
    def show_welcome(self): self.show_view("Welcome")
    def show_drafting_fk(self): self.show_view("Drafting FK")
    def show_resub_fk(self): self.show_view("Resub FK")
    def show_rm_merging(self): self.show_view("RM Merging")
    def show_update_rm(self): self.show_view("Update RM")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
