import customtkinter as ctk

class BaseView(ctk.CTkFrame):
    """
    Template UI dasar (Base View) untuk setiap menu.
    Memiliki layout standar: Judul, Tombol Import, Proses, dan Export.
    """
    def __init__(self, master, title, logger, handler, description="", tutorial="", **kwargs):
        super().__init__(master, **kwargs)
        self.logger = logger
        self.handler = handler  # Inject logic handler (core)
        self.df_aktif = None    # Simpan dataframe yang sedang aktif
        self.filepath_aktif = None # Simpan filepath yang terbuka
        
        # Konfigurasi grid layout
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header Frame (menggantikan title langsung ditaruh di grid)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Judul Halaman
        self.lbl_title = ctk.CTkLabel(self.header_frame, text=title, font=ctk.CTkFont(family="Calibri", size=24, weight="bold"))
        self.lbl_title.pack(anchor="w")
        
        if description:
            self.lbl_desc = ctk.CTkLabel(self.header_frame, text=description, font=ctk.CTkFont(family="Calibri", size=14), text_color="gray")
            self.lbl_desc.pack(anchor="w", pady=(5, 0))
        
        # Area Tombol Aksi
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.btn_import = ctk.CTkButton(self.action_frame, text="1. Import File", font=ctk.CTkFont(family="Calibri", size=14), command=self.on_import)
        self.btn_import.pack(side="left", padx=10, pady=10)
        
        self.original_btn_color = self.btn_import.cget("fg_color")
        
        self.btn_process = ctk.CTkButton(self.action_frame, text="2. Proses Data", font=ctk.CTkFont(family="Calibri", size=14), command=self.on_process, state="disabled", fg_color="gray")
        self.btn_process.pack(side="left", padx=10, pady=10)
        
        self.btn_export = ctk.CTkButton(self.action_frame, text="3. Export File", font=ctk.CTkFont(family="Calibri", size=14), command=self.on_export, state="disabled", fg_color="gray")
        self.btn_export.pack(side="left", padx=10, pady=10)
        
        # Label Info ditaruh di sebelah kanan tombol aksi
        self.info_label = ctk.CTkLabel(self.action_frame, text="Belum ada data dimuat.", font=ctk.CTkFont(family="Calibri", size=14), text_color="gray")
        self.info_label.pack(side="right", padx=20, pady=10)
        
        # Area Konten / Boks Tutorial
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        self.tutor_text = ctk.CTkTextbox(self.content_frame, font=ctk.CTkFont(family="Calibri", size=15), wrap="word", fg_color=("gray90", "gray15"))
        self.tutor_text.pack(expand=True, fill="both", padx=10, pady=10)
        self.tutor_text.insert("0.0", tutorial if tutorial else "(Belum ada tutorial/langkah kerja terperinci untuk menu ini.)")
        self.tutor_text.configure(state="disabled")
        
    def on_import(self):
        import_mode = getattr(self.handler, "import_mode", "file")
        
        if import_mode == "directory":
            filepath = ctk.filedialog.askdirectory(title="Pilih Folder Berisi File CSV")
        else:
            filepath = ctk.filedialog.askopenfilename(
                title="Pilih File", 
                filetypes=(("CSV Files", "*.csv"), ("Excel Files", "*.xlsx"), ("All Files", "*.*"))
            )
            
        if not filepath:
            return
            
        # Reset state ketika user melakukan import file baru
        self.btn_process.configure(state="disabled", fg_color="gray")
        self.btn_export.configure(state="disabled", fg_color="gray")
        self.filepath_aktif = filepath
        
        if import_mode == "directory":
            self.info_label.configure(text=f"Folder terpilih: {filepath.split('/')[-1]}")
            self.logger.log(f"Memproses Import Folder: {filepath}")
            
            if hasattr(self.handler, "on_import_success"):
                hook_msg = self.handler.on_import_success(self.filepath_aktif)
                if hook_msg:
                    self.logger.log(hook_msg)
            
            self.btn_process.configure(state="normal", fg_color=self.original_btn_color)
            return
            
        self.logger.log(f"Memproses Import file: {filepath}")
        from core.file_io import FileIO
        df, msg = FileIO.load_file(filepath)
        
        if df is not None:
            self.df_aktif = df
            self.info_label.configure(text=f"File termuat: {filepath.split('/')[-1]} ({len(df)} baris)")
            self.logger.log(msg)
            
            # Panggil hook otomatis jika handler memilikinya (misal untuk auto-ekstrak)
            if hasattr(self.handler, "on_import_success"):
                hook_msg = self.handler.on_import_success(self.df_aktif)
                if hook_msg:
                    self.logger.log(hook_msg)
            
            # ENABLE TOMBOL PROSES
            self.btn_process.configure(state="normal", fg_color=self.original_btn_color)
        else:
            self.logger.log(f"ERROR Import: {msg}")
        
    def on_process(self):
        import_mode = getattr(self.handler, "import_mode", "file")
        
        if import_mode == "directory":
            if not getattr(self, "filepath_aktif", None):
                self.logger.log("Peringatan: Belum ada folder yang dipilih!")
                return
        else:
            if self.df_aktif is None:
                self.logger.log("Peringatan: Belum ada file yang di-import!")
                return
            
        self.logger.log(f"Memulai logika pemrosesan untuk {self.lbl_title.cget('text')}...")
        
        try:
            self.df_aktif, output_msg = self.handler.process(self.df_aktif, self.filepath_aktif)
        except TypeError:
            self.df_aktif, output_msg = self.handler.process(self.df_aktif)
            
        self.logger.log(output_msg)
        
        # ENABLE TOMBOL EXPORT JIKA TIDAK ADA PESAN GAGAL
        if "ERROR" not in output_msg.upper() and "GAGAL" not in output_msg.upper():
            self.btn_export.configure(state="normal", fg_color=self.original_btn_color)
        
    def on_export(self):
        if not hasattr(self.handler, "export_data"):
            self.logger.log("Peringatan: Funsionalitas export belum dikonfigurasi untuk menu ini.")
            return
            
        success, msg = self.handler.export_data()
        self.logger.log(msg)
        
        if success:
            # Memunculkan Pop up Modal custom (tidak bisa ditutup tanpa dipencet tombol)
            self.show_popup()
            
    def show_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Proses Selesai")
        popup.geometry("350x150")
        
        # Aturan Modal Window agar tidak bisa di minimize / maximize
        popup.attributes("-topmost", True)
        popup.resizable(False, False)
        popup.transient(self.master) # Ikat ke top window agar menghilangkan tombol min/max default Windows
        
        # Mencegah tombol [X] di pojok kanan atas agar tidak bisa klik "close"
        popup.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Menjadikan jendela modal (mengunci window utama)
        popup.grab_set() 
        
        # Pertanyaan lucu
        if self.lbl_title.cget("text") == "Resubmission FK (Setelah Reject PSIAP)":
            teks = "Kamu mau bikin pelet lagi?"
        else:
            teks = "Apakah Anda mau memproses data lagi?"
            
        lbl = ctk.CTkLabel(popup, text=teks, font=ctk.CTkFont(family="Calibri", size=16, weight="bold"))
        lbl.pack(pady=(25, 15))
        
        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack()
        
        def reset_semua():
            popup.grab_release()
            popup.destroy()
            self.reset_state()
            
        btn_ya = ctk.CTkButton(btn_frame, text="Ya", width=80, fg_color="#16A085", hover_color="#1ABC9C", command=reset_semua)
        btn_ya.pack(side="left", padx=10)
        
        btn_tidak = ctk.CTkButton(btn_frame, text="Engga", width=80, fg_color="#E74C3C", hover_color="#C0392B", command=reset_semua)
        btn_tidak.pack(side="left", padx=10)
        
    def reset_state(self):
        self.df_aktif = None
        self.info_label.configure(text="Belum ada data dimuat.")
        self.btn_process.configure(state="disabled", fg_color="gray")
        self.btn_export.configure(state="disabled", fg_color="gray")
        self.logger.log("Sistem telah di-reset. Siap menerima 'sasaran target' pelet yang baru.")
