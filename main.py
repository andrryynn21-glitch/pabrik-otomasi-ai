import os
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

def ambil_tren_realtime():
    """Mengambil 5 tren/berita terkini secara real-time dari RSS Google News"""
    url = "https://news.google.com/rss?hl=id&gl=ID&ceid=ID:id"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(response.content)
        
        items = root.findall('./channel/item')[:5]
        topik_list = []
        for item in items:
            title = item.find('title').text if item.find('title') is not None else "Tidak ada judul"
            topik_list.append(title)
        return topik_list
    except Exception as e:
        print(f"Gagal mengambil tren: {e}")
        return ["Kreativitas Pemuda & Tren Digital", "Peluang Otomasi Bisnis 2026"]

def job_riset_otomatis_harian():
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tanggal_file = datetime.now().strftime("%Y-%m-%d")
    print(f"[{waktu_sekarang}] Memulai Riset Otomatis Produk Digital & Konten...")
    
    tren_terbaru = ambil_tren_realtime()
    topik_utama = tren_terbaru[0] if tren_terbaru else "Tren Digital Harian"
    
    filename = f"laporan_riset_{tanggal_file}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("==============================================================\n")
        f.write(f"  PABRIK OTOMASI AI: MODUL 1 - RISET PRODUK DIGITAL & KONTEN\n")
        f.write(f"  Waktu Eksekusi: {waktu_sekarang}\n")
        f.write("==============================================================\n\n")
        
        f.write("--- [1. TREN VIRAL REAL-TIME HARI INI] ---\n")
        for i, t in enumerate(tren_terbaru, 1):
            f.write(f"{i}. {t}\n")
            
        f.write("\n--- [2. STRUKTUR PRODUK DIGITAL (MINI E-BOOK / GUIDE)] ---\n")
        f.write(f"Topik Utama Viral : {topik_utama}\n")
        f.write(f"Judul E-Book      : Panduan Kilat & Peluang Cuan dari '{topik_utama[:40]}...'\n")
        f.write("Format Produk     : PDF Guide / Playbook (10-15 Halaman)\n")
        f.write("Outline Isi E-Book:\n")
        f.write("  - Bab 1: Bedah Isu & Kenapa Tren Ini Viral Banget\n")
        f.write("  - Bab 2: 3 Peluang Cuan / Manfaat Nyata Buat Pemula\n")
        f.write("  - Bab 3: Langkah Praktis Eksekusi Tanpa Modal\n")
        f.write("  - Bab 4: Rekomendasi Tools & AI Pendukung Otomatis\n")
        f.write("Target Market     : Gen-Z, Content Creator, & Pemburu Peluang Digital\n")
        
        f.write("\n--- [3. DRAF KONTEN PROMOSI POV/KOMEDI (CANDATAWAMU26)] ---\n")
        f.write("Sudut Pandang (POV): 'POV lu panik karena orang lain udah pada paham tren ini'\n")
        f.write(f"Hook Skrip        : 'POV: Lu baru bangun tidur dan kaget liat orang-orang udah bahas {topik_utama[:25]}...'\n")
        f.write("Visual/Act        : Muka panik, bolak-balik ngetik di laptop, ekspresi bingung tapi kocak.\n")
        f.write("Call to Action    : 'Daripada lu bengong sendirian, amankan E-Book panduannya di link bio sekarang!'\n\n")
        f.write("==============================================================\n")
        f.write(" Generated Automatically by GitHub Actions Automation Pipeline\n")
    
    print(f"-> Laporan Produk Digital & Konten Berhasil Disimpan di {filename}!")

if __name__ == "__main__":
    job_riset_otomatis_harian()
