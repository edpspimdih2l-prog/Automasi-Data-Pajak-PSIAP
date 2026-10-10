import pandas as pd

class FileIO:
    """Utility class khusus membaca dan menyimpan file"""
    
    @staticmethod
    def load_file(filepath):
        try:
            if filepath.endswith('.csv'):
                # Seringkali file DJP menggunakan pemisah pipa (|) atau titik koma (;)
                # Kita gunakan sep='|' secara default untuk kasus ini
                df = pd.read_csv(filepath, sep='|', dtype=str)
            elif filepath.endswith('.xlsx'):
                df = pd.read_excel(filepath, dtype=str)
            else:
                return None, "Format tidak didukung (.csv atau .xlsx)."
            return df, f"Berhasil memuat file {filepath.split('/')[-1]} ({len(df)} baris)."
        except Exception as e:
            return None, f"Gagal membaca file: {str(e)}"
            
    @staticmethod
    def save_file(df, filepath):
        if df is None:
            return False, "Data Kosong."
        try:
            if filepath.endswith('.csv'):
                df.to_csv(filepath, sep='|', index=False)
            elif filepath.endswith('.xlsx'):
                df.to_excel(filepath, index=False)
            else:
                return False, "Format output tidak didukung (.csv atau .xlsx)."
            return True, "Berhasil menyimpan file."
        except Exception as e:
            return False, f"Gagal menyimpan file: {str(e)}"
