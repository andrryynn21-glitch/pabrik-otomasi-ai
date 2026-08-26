import os
import xml.etree.ElementTree as ET
from datetime import datetime
import requests

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

def analisis_dengan_openrouter(tren_list):
    """Mengirim data tren ke OpenRouter API (Gratis & Stabil)"""
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Gagal analisis: API Key tidak ditemukan di GitHub Secrets!"

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
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "json"
    }
    payload = {
        # Menggunakan model gratis dari OpenRouter
"model": "openrouter/free",        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        if res.status_code == 200:
            data = res.json()
            return data['choices'][0]['message']['content']
        else:
            return f"Error OpenRouter API ({res.status_code}): {res.text}"
    except Exception as e:
        return f"Error HTTP Request: {e}"

def job_riset_otomatis_harian():
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tanggal_file = datetime.now().strftime("%Y-%m-%d")
    print(f"[{waktu_sekarang}] Memulai Riset Real-Time + OpenRouter AI...")
    
    # 1. Tarik Tren
    tren = ambil_tren_realtime()
    print("-> Berhasil menarik berita real-time!")
    
    # 2. Analisis via AI
    print("-> Mengirim data ke OpenRouter AI...")
    hasil_ai = analisis_dengan_openrouter(tren)
    
    # 3. Simpan ke File Laporan
    filename = f"laporan_riset_{tanggal_file}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("==============================================================\n")
        f.write(f"  PABRIK OTOMASI AI: HASIL ANALISIS AI & TREN REAL-TIME\n")
        f.write(f"  Waktu Eksekusi: {waktu_sekarang}\n")
        f.write("==============================================================\n\n")
        f.write("--- [DATA TREN REAL-TIME] ---\n")
        for i, t in enumerate(tren, 1):
            f.write(f"{i}. {t}\n")
        f.write("\n==============================================================\n")
        f.write("--- [ANALYSIS & GENERATION BY OPENROUTER AI] ---\n")
        f.write("==============================================================\n\n")
        f.write(hasil_ai)
        f.write("\n\n==============================================================\n")
        f.write(" Generated Automatically by GitHub Actions & OpenRouter API\n")
        
    print(f"-> Berhasil! Hasil analisis AI tersimpan di {filename}")

if __name__ == "__main__":
    job_riset_otomatis_harian()
