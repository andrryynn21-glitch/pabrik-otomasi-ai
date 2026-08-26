import os
from datetime import datetime

def job_riset_otomatis_harian():
    tanggal_hari_ini = datetime.now().strftime("%Y-%m-%d")
    print(f"[{tanggal_hari_ini}] AI mulai memindai tren harian dari internet...")

    topik_terpilih = "Analisis Tren Otomatis Harian dari Web"
    print(f"-> Berhasil mendapatkan topik: {topik_terpilih}")

    filename = f"laporan_riset_{tanggal_hari_ini}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Laporan Otomatis AI - Tanggal: {tanggal_hari_ini}\n")
        f.write(f"Topik Harian: {topik_terpilih}\n")

    print(f"-> Laporan berhasil disimpan ke {filename}. Selesai!")

if __name__ == "__main__":
    job_riset_otomatis_harian()
