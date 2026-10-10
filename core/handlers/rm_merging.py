import os
import glob
import customtkinter as ctk

class RMMergingHandler:
    """Core logic untuk menu RM Merging"""
    def __init__(self):
        self.import_mode = "directory" # Custom atribut agar BaseView membuka folder picker
        self.filtered_lines = []

    def on_import_success(self, folderpath):
        """Hook otomatis dipanggil setelah folder di-import oleh BaseView"""
        csv_files = glob.glob(os.path.join(folderpath, "*.csv"))
        return f"[RM Merging] Mantap! Ditemukan {len(csv_files)} file CSV di dalam folder terpilih.\nKlik '2. Proses Data' untuk mulai menyatukannya."

    def process(self, dummy_df, folderpath):
        try:
            csv_files = glob.glob(os.path.join(folderpath, "*.csv"))
            if not csv_files:
                return None, "Gagal: Tidak ada ekstensi file CSV (.csv) yang ditemukan di dalam folder tersebut."
                
            merged_lines = []
            header_captured = False
            total_files_read = 0
            
            for fpath in csv_files:
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    with open(fpath, 'r', encoding='latin1') as f:
                        lines = f.readlines()
                        
                if len(lines) < 2:
                    continue # Lewati file kosong atau rusak tanpa error
                    
                total_files_read += 1
                
                # Mengambil baris 1 dan 2 (RM dan OF headers) hanya TEPAT SATU KALI dari file pertama
                if not header_captured:
                    merged_lines.append(lines[0])
                    if len(lines) > 1:
                        merged_lines.append(lines[1])
                    header_captured = True
                    
                # Menyisipkan row ke-3 hingga seterusnya
                for line in lines[2:]:
                    if line.strip(): # Cegah blank lines
                        merged_lines.append(line)
                        
            if total_files_read == 0:
                return None, "Gagal merangkai isi file dari folder tersebut. File mungkin kosong."
                
            self.filtered_lines = merged_lines
            return None, f"✨ Berhasil Merging! {total_files_read} kepingan file CSV telah bersatu menjadi {len(merged_lines)} baris sakti (termasuk header).\nSilakan klik '3. Export File' untuk menyimpannya!"
        except Exception as e:
            return None, f"Terjadi kesalahan saat proses merging: {str(e)}"

    def export_data(self):
        """Menyimpan hasil gabungan ke dalam file CSV baru"""
        if not hasattr(self, 'filtered_lines') or not self.filtered_lines:
            return False, "Gagal! Belum ada file gabungan yang siap diexport. Lakukan Proses Data dulu!"
            
        save_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="RM_Kitab_Suci_Utuh.csv",
            title="Simpan File Merging RM",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        
        if not save_path:
            return False, "Batal menyimpan file merging."
            
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.writelines(self.filtered_lines)
            
            # Reset state
            self.filtered_lines = []
            
            return True, f"✅ Sukses!! File Master RM gabungan berhasil disimpan di:\n{save_path}"
        except Exception as e:
            return False, f"❌ Gagal menyimpan file: {str(e)}"
