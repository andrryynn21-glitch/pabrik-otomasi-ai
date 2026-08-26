import datetime
import os
import requests

def get_free_models():
    """Mengambil daftar semua model gratis yang tersedia di OpenRouter secara dinamis."""
    try:
        res = requests.get("https://openrouter.ai/api/v1/models", timeout=15)
        if res.status_code == 200:
            data = res.json().get("data", [])
            # Filter otomatis SEMUA model yang berakhiran :free
            free_models = [m["id"] for m in data if m.get("id", "").endswith(":free")]
            if free_models:
                print(f"-> Ditemukan {len(free_models)} model gratisan di OpenRouter!")
                return free_models
    except Exception as e:
        print(f"-> Gagal mengambil katalog model OpenRouter secara dinamis: {e}")
    
    # Fallback daftar manual jika fetch katalog utama bermasalah
    return [
        "google/gemma-4-31b-it:free",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "minimax/minimax-m3:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "deepseek/deepseek-r1:free",
        "liquid/lfm2.5-2.6b:free",
        "mistralai/mistral-7b-instruct:free",
        "qwen/qwen-2.5-72b-instruct:free"
    ]

def run_research():
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Memulai Riset Real-Time + OpenRouter AI...")
    
    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    fonnte_token = os.environ.get("FONNTE_TOKEN")
    wa_target = os.environ.get("WA_TARGET_NUMBER")

    if not openrouter_key:
        print("-> Error: OPENROUTER_API_KEY tidak ditemukan di environment.")
        return

   prompt_text = (
        "Kamu adalah pakar strategi konten komedi sosial media dan penulisan skrip kreatif untuk akun @candatawamu26.\n"
        "Tugas utama kamu adalah memberikan laporan riset tren harian dan draft skrip komedi berkualitas tinggi.\n\n"
        "Berikan output dengan format WhatsApp (Gunakan huruf tebal dengan bintang *teks*, JANGAN gunakan markdown hashtag ### atau ####):\n\n"
        "*1. 📊 TRENDING TOPIC HARI INI*\n"
        "Rangkuman 2-3 topik/isu/relate moment yang sedang ramai di Indonesia saat ini.\n\n"
        "*2. 🎭 IDE KONTEN KOMEDI (POV/Jokes)*\n"
        "Buat 2 konsep skrip komedi singkat khas @candatawamu26 lengkap dengan Hook (3 detik pertama), Jalan Cerita (POV), dan Punchline (Lucu/Plot twist).\n\n"
        "*3. 📌 REKOMENDASI CAPTION & HASHTAG*\n"
        "Berikan saran caption santai/lucu dan hashtag relevan.\n\n"
        "Gunakan bahasa Indonesia yang santai, komunikatif, relevan dengan anak muda, dan rapi agar nyaman dibaca di WhatsApp."
    )

    headers_ai = {
        "Authorization": f"Bearer {openrouter_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com",
        "X-Title": "Pabrik Otomasi AI"
    }
    
    # Ambil SEMUA model gratisan secara otomatis dari OpenRouter API
    candidate_models = get_free_models()

    output_text = None

    for model_name in candidate_models:
        print(f"-> Mencoba memanggil model: {model_name}...")
        payload_ai = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt_text}]
        }

        try:
            response_ai = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers_ai, json=payload_ai, timeout=45)
            res_data = response_ai.json()
            
            if response_ai.status_code == 200 and "choices" in res_data and len(res_data["choices"]) > 0:
                output_text = res_data["choices"][0]["message"]["content"]
                print(f"-> BERHASIL! Mendapat respon dari model: {model_name}")
                break
            else:
                err_msg = res_data.get('error', {}).get('message', 'Busy/Limit') if isinstance(res_data.get('error'), dict) else res_data.get('error', 'Busy/Limit')
                print(f"-> Skip {model_name}: {err_msg}")
        except Exception as e:
            print(f"-> Error koneksi ke {model_name}: {e}")

    if not output_text:
        output_text = "Gagal mengambil laporan dari AI. Semua kandidat model gratisan sedang sibuk/offline."

    # Simpan Hasil Riset ke File Teks
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f"laporan_riset_{today_str}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_text)
        
    print(f"-> Hasil analisis AI tersimpan di {filename}")

    # Pengiriman Notifikasi via Fonnte
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
        print("-> Error: Secret FONNTE_TOKEN atau WA_TARGET_NUMBER belum terdeteksi.")

if __name__ == "__main__":
    run_research()
