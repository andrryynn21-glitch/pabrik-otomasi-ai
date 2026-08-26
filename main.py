import os
import xml.etree.ElementTree as ET
from datetime import datetime
import requests
from google import genai

def ambil_tren_realtime():
    """Mengambil 5 tren terkini secara real-time dari Google News RSS"""
    url = "https://news.google.com/rss?hl=id&gl=ID&ceid=ID:id"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        root = ET.fromstring(response.content)
        items = root.findall('./channel/item')[:5]
        topik_list = [item.find('title').text for item in items if item.find('title') is not None]
        return topik_list
    except Exception as e:
        print(f"Gagal mengambil tren: {e}")
        return ["Tren Digital 2026", "Teknologi AI & Komunitas Kreatif"]

def analisis_dengan_gemini(tren_list):
    """Mengirim data tren ke Gemini API untuk dianalisis jadi E-Book & Skrip Komedi"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("PERINGATAN: GEMINI_API_KEY tidak ditemukan!")
        return "Gagal analisis: API Key tidak tersedia."

    client = genai.Client(api_key=api_key)
    
    daftar_tren_str = "\n".join([f"- {t}" for t in tren_list])
    
    prompt = f"""
    Kamu adalah Manajer Produk Digital sekaligus Creative Content Strategist untuk akun komedi Gen-Z @candatawamu26.
    Berikut adalah 5 berita/tren viral terkini hari ini di Indonesia:
    {daftar_tren_str}

    Tolong buatkan analisis dan draf rencana otomatis dalam format teks rapi dengan struktur:
    1. BERITA/TOPIK PILIHAN UTAMA: (Pilih 1 topik paling menarik dari daftar di atas)
    2. IDE PRODUK DIGITAL (E-BOOK / GUIDE):
       - Judul E-Book yang Catchy & Menjual
       - Target Audience
       - Outline 4 Bab Utama (jelaskan singkat isi tiap babnya)
       - Solusi/Cuan yang didapat pembaca
    3. DRAF SKRIP KONTEN PROMOSI POV/KOMEDI (@candatawamu26):
       - Sudut Pandang (POV)
       - Hook 3 Detik Pertama (lucu/relatable)
       - Alur Aksi/Ekspresi Komedi
       - Call to Action (CTA) jualan E-Book tersebut
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error saat memanggil Gemini API: {e}")
        return f"Error Gemini API: {e}"

def job_riset_otomatis_harian():
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tanggal_file = datetime.now().strftime("%Y-%m-%d")
    print(f"[{waktu_sekarang}] Memulai Riset Real-Time + AI Gemini...")
    
    # 1. Tarik Tren
    tren = ambil_tren_realtime()
    print("-> Berhasil menarik berita real-time!")
    
    # 2. Analisis via Gemini AI
    print("-> Mengirim data ke Gemini AI untuk generate ide E-Book & Skrip...")
    hasil_ai = analisis_dengan_gemini(tren)
    
    # 3. Simpan ke File Laporan
    filename = f"laporan_riset_{tanggal_file}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("==============================================================\n")
        f.write(f"  PABRIK OTOMASI AI: HASIL ANALISIS GEMINI AI & TREN REAL-TIME\n")
        f.write(f"  Waktu Eksekusi: {waktu_sekarang}\n")
        f.write("==============================================================\n\n")
        f.write("--- [DATA TREN REAL-TIME] ---\n")
        for i, t in enumerate(tren, 1):
            f.write(f"{i}. {t}\n")
        f.write("\n==============================================================\n")
        f.write("--- [ANALYSIS & GENERATION BY GEMINI AI] ---\n")
        f.write("==============================================================\n\n")
        f.write(hasil_ai)
        f.write("\n\n==============================================================\n")
        f.write(" Generated Automatically by GitHub Actions & Gemini API\n")
        
    print(f"-> Berhasil! Hasil analisis AI tersimpan di {filename}")

if __name__ == "__main__":
    job_riset_otomatis_harian()
