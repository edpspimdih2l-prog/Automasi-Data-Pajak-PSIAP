import customtkinter as ctk

class DraftingFKHandler:
    """Core logic untuk menu Drafting FK PKP / NON PKP"""
    def __init__(self):
        self.filtered_lines = []

    def on_import_success(self, df):
        """Hook otomatis dipanggil setelah file di-import oleh BaseView"""
        return "[Drafting FK] File telah sukses dibaca di memori! Klik '2. Proses Data' untuk menyihir datanya."
        
    def process(self, df, filepath):
        try:
            # Membaca mentah baris per baris agar susunan FK dan OF sempurna
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin1') as f:
                    lines = f.readlines()
                    
            if len(lines) < 2:
                return df, "Gagal: File terlalu pendek atau kosong."
                
            output_lines = []
            output_lines.append(lines[0]) 
            if len(lines) > 1:
                output_lines.append(lines[1]) 
                
            count_found = 0
            
            for line in lines[2:]:
                if line.startswith("FK|") or line.startswith('"FK"|'):
                    cols = line.split('|')
                    count_found += 1
                    
                    if len(cols) >= 13:
                        original_npwp = cols[9]
                        cols[9] = "0000000000000000"
                        cols[10] = "3"
                        cols[11] = original_npwp
                        cols[12] = "IDN"
                        
                    modified_line = "|".join(cols)
                    output_lines.append(modified_line)
                else:
                    # Baris OF dll, selalu disalin karena ini adalah Drafting master
                    output_lines.append(line)
            
            self.filtered_lines = output_lines
            return df, f"✨ Berhasil nge-Draft! Seluruh {count_found} baris FK telah disihir identitasnya.\nSilakan klik '3. Export File' untuk menyimpannya!"
            
        except Exception as e:
            return df, f"Terjadi kesalahan saat memproses Drafting: {str(e)}"
            
    def export_data(self):
        """Menyimpan hasil drafting ke dalam file CSV"""
        if not hasattr(self, 'filtered_lines') or not self.filtered_lines:
            return False, "Gagal! Belum ada file racikan yang siap diexport. Lakukan Proses Data dulu!"
            
        save_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="FK_Drafting_App.csv",
            title="Simpan File Drafting FK",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        
        if not save_path:
            return False, "Batal menyimpan file drafting."
            
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(self.filtered_lines)
            
            # Reset state
            self.filtered_lines = []
            
            return True, f"✅ Sukses!! File drafting berhasil disimpan di:\n{save_path}"
        except Exception as e:
            return False, f"❌ Gagal menyimpan file: {str(e)}"
