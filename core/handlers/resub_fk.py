import customtkinter as ctk

class ResubFKHandler:
    """Core logic untuk menu Resubmission FK PKP / NON PKP"""
    def __init__(self):
        self.step = 1
        self.stored_fakturs = []
        self.filtered_lines = []
        
    def on_import_success(self, df):
        """Hook otomatis dijalankan sesaat setelah file pertama sukses diimport"""
        if 'FIELD_TAMBAHAN_4' in df.columns:
            fakturs = df['FIELD_TAMBAHAN_4'].dropna().tolist()
            self.stored_fakturs = [str(x).strip() for x in fakturs if str(x).strip() != '']
            self.step = 2
            return f"[Resub FK] Auto-ekstrak selesai. {len(self.stored_fakturs)} No Faktur telah disimpan di memori.\nKlik '2. Proses Data' untuk mengunggah file FK asli."
        else:
            return "[Resub FK] ERROR: Kolom 'FIELD_TAMBAHAN_4' tidak ditemukan, auto-ekstrak gagal!"

    def process(self, df):
        if self.step == 2:
            # Meminta user memilih file kedua (FK Asli)
            filepath = ctk.filedialog.askopenfilename(
                title="Pilih File FK Asli (File Jimat)", 
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
            )
            if not filepath:
                return df, "Pemilihan file FK asli dibatalkan oleh user."
                
            try:
                # Membaca baris per baris agar struktur FK & OF tidak hancur oleh Pandas
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    with open(filepath, 'r', encoding='latin1') as f:
                        lines = f.readlines()
                        
                if len(lines) < 2:
                    return df, "Gagal: File FK Asli terlalu pendek atau kosong."
                    
                output_lines = []
                output_lines.append(lines[0]) # Header 1 (FK)
                if len(lines) > 1:
                    output_lines.append(lines[1]) # Header 2 (OF)
                
                keep_current_fk = False
                count_found = 0
                
                for line in lines[2:]:
                    # Hanya membedah faktur yang bertipe FK
                    if line.startswith("FK|") or line.startswith('"FK"|'):
                        cols = line.split('|')
                        
                        # Cek apakah bagian dari baris mengandung no faktur yang kita simpan
                        found = False
                        for col in cols:
                            if col.strip() in self.stored_fakturs:
                                found = True
                                break
                                
                        if found:
                            keep_current_fk = True
                            count_found += 1
                            
                            # --- PROSES JAMPE-JAMPE (MODIFIKASI KOLOM KHUSUS FK) ---
                            # Pastikan daftar kolom cukup panjang menghindari error
                            if len(cols) >= 13:
                                original_npwp = cols[9]
                                cols[9] = "0000000000000000"
                                cols[10] = "3"
                                cols[11] = original_npwp
                                cols[12] = "IDN"
                                
                            modified_line = "|".join(cols)
                            output_lines.append(modified_line)
                        else:
                            keep_current_fk = False
                    else:
                        # Baris ini biasanya "OF|" (Item Faktur), akan disalin jika header FK-nya valid
                        if keep_current_fk:
                            output_lines.append(line)
                
                self.filtered_lines = output_lines
                return df, f"✨ Berhasil menjampe-jampe! Sistem berhasil menemukan {count_found} Faktur Keluaran dari target {len(self.stored_fakturs)} penolakan.\nSilakan klik '3. Export File' untuk menciptakan jimat resubmission Anda!"
                
            except Exception as e:
                return df, f"Terjadi kesalahan saat memproses jimat: {str(e)}"
            
        return df, "Harap import file Reject PSIAP terlebih dahulu di tahap 1."

    def export_data(self):
        """Menyimpan hasil racikan FK + OF ke dalam file CSV"""
        if not hasattr(self, 'filtered_lines') or not self.filtered_lines:
            return False, "Gagal! Belum ada file racikan yang siap diexport. Lakukan Proses Data dulu!"
            
        save_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="FK_Jimat_Balikan.csv",
            title="Simpan File Jimat FK Balikan",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        
        if not save_path:
            return False, "Batal menyimpan file jimat."
            
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(self.filtered_lines)
            
            # Reset state agar aplikasi siap untuk siklus berikutnya
            self.step = 1
            self.stored_fakturs = []
            self.filtered_lines = []
            
            return True, f"✅ Sukses!! File racikan jimat berhasil disimpan di:\n{save_path}\n\nSemoga berhasil! Silakan bawa file ini ke PSIAP!"
        except Exception as e:
            return False, f"❌ Gagal menyimpan file: {str(e)}"
