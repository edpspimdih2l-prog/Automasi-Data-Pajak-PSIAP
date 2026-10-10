import customtkinter as ctk

class UpdateRMHandler:
    """Core logic untuk menu Update RM"""
    def __init__(self):
        self.filtered_lines = []
        
    def on_import_success(self, df):
        return "[Update RM] File berhasil dibaca sistem. Klik '2. Proses Data' untuk menyulap RM menjadi RFM."

    def process(self, df, filepath):
        try:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin1') as f:
                    lines = f.readlines()
                    
            if len(lines) == 0:
                return df, "Gagal: File terlalu pendek atau kosong."
                
            output_lines = []
            
            # 1. Modifikasi Header
            header_line = lines[0]
            h_cols = header_line.split('|')
            if h_cols[0] in ["RM", '"RM"']:
                h_cols[0] = h_cols[0].replace("RM", "RFM")
            if len(h_cols) > 8:
                h_cols.insert(9, "IS_CREDITABLE")
            output_lines.append("|".join(h_cols))
            
            # 2. Modifikasi Sisa Data
            count_found = 0
            for line in lines[1:]:
                if line.startswith("RM|") or line.startswith('"RM"|'):
                    cols = line.split('|')
                    cols[0] = cols[0].replace("RM", "RFM")
                    
                    if len(cols) > 8:
                        cols.insert(9, "credited")
                        
                    output_lines.append("|".join(cols))
                    count_found += 1
                else:
                    output_lines.append(line)
                    
            self.filtered_lines = output_lines
            return df, f"✨ Berhasil menyihir status RM! Total {count_found} baris telah disisipkan 'credited' dan disulap menjadi RFM.\nSilakan klik '3. Export File' untuk menyelesaikannya!"
            
        except Exception as e:
            return df, f"Terjadi kesalahan saat memproses Update RM: {str(e)}"
            
    def export_data(self):
        """Menyimpan hasil RFM ke dalam file CSV baru"""
        if not hasattr(self, 'filtered_lines') or not self.filtered_lines:
            return False, "Gagal! Belum ada file yang siap diexport. Lakukan Proses Data dulu!"
            
        save_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="RFM_Pusaka_Excalibur.csv",
            title="Simpan File Update RM",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        
        if not save_path:
            return False, "Batal menyimpan file merging."
            
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(self.filtered_lines)
            
            self.filtered_lines = []
            return True, f"✅ Sukses!! File Master RFM (Update RM) berhasil disimpan di:\n{save_path}"
        except Exception as e:
            return False, f"❌ Gagal menyimpan file: {str(e)}"
