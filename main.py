import datetime
import os
import requests

def run_research():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Memulai Riset Real-Time + OpenRouter AI...")
    
    # 1. Mengambil Credentials dari Environment (GitHub Secrets)
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    fonnte_token = os.environ.get("FONNTE_TOKEN")
    wa_target = os.environ.get("WA_TARGET_NUMBER")

    if not openrouter_key:
        print("-> Error: OPENROUTER_API_KEY tidak ditemukan di environment.")
        return

    # 2. Prompt Spesifik Komedi & Riset Tren @candatawamu26
    prompt_text = (
        "Kamu adalah pakar strategi konten komedi sosial media dan penulisan skrip kreatif untuk akun @candatawamu26.\n"
        "Tugas utama kamu adalah memberikan laporan riset tren harian dan draft skrip komedi berkualitas tinggi.\n\n"
        "Berikan output dengan struktur berikut:\n"
        "1. 📊 TRENDING TOPIC HARI INI: Rangkuman 2-3 topik/isu/relate moment yang sedang ramai di Indonesia saat ini.\n"
        "2. 🎭 IDE KONTEN KOMEDI (POV/Jokes): Buat 2 konsep skrip komedi singkat khas @candatawamu26 lengkap dengan Hook (3 detik pertama), Jalan Cerita (POV), dan Punchline (Lucu/Plot twist).\n"
        "3. 📌 REKOMENDASI CAPTION & HASHTAG: Berikan saran caption santai/lucu dan hashtag relevan.\n\n"
        "Gunakan bahasa Indonesia yang santai, komunikatif, relevan dengan anak muda, dan rapi agar mudah dibaca di WhatsApp."
    )

    print("-> Mengirim data ke OpenRouter AI...")
    
    headers_ai = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json"
    }
    
payload_ai = {
        "model": "google/gemma-4-31b-it:free",
        "messages": [
            {"role": "user", "content": prompt_text}
        ]
    }

    try:
        response_ai = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers_ai, json=payload_ai)
        response_ai.raise_for_status()
        result_json = response_ai.json()
        output_text = result_json["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"-> Error saat memanggil OpenRouter AI: {e}")
        return

    # 3. Simpan Hasil Riset ke File Teks
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f"laporan_riset_{today_str}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_text)
        
    print(f"-> Berhasil! Hasil analisis AI tersimpan di {filename}")

    # 4. Pengiriman Notifikasi Hasil Riset ke WhatsApp via Fonnte
    if fonnte_token and wa_target:
        print("-> Mengirim laporan ke WhatsApp via Fonnte...")
        url_fonnte = "https://api.fonnte.com/send"
        
        payload_fonnte = {
            "target": wa_target,
            "message": output_text
        }
        
        headers_fonnte = {
            "Authorization": fonnte_token
        }
        
        try:
            res_fonnte = requests.post(url_fonnte, data=payload_fonnte, headers=headers_fonnte)
            print("-> Response Fonnte:", res_fonnte.json())
        except Exception as e:
            print(f"-> Error saat mengontak API Fonnte: {e}")
    else:
        print("-> Error: Secret FONNTE_TOKEN atau WA_TARGET_NUMBER belum terdeteksi di GitHub Secrets.")

if __name__ == "__main__":
    run_research()
