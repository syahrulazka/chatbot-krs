# 🎓 Chatbot KRS (Kartu Rencana Studi)

Aplikasi chatbot berbasis web menggunakan Streamlit untuk membantu mahasiswa dalam hal tanya jawab seputar Kartu Rencana Studi (KRS). Chatbot ini menggunakan Natural Language Processing (NLP) dengan TF-IDF, fuzzy matching, dan sequence matching untuk memberikan jawaban yang akurat.

## ✨ Fitur

- **Multi-Method Matching**: Menggunakan TF-IDF, fuzzy matching, dan sequence matching untuk mencari jawaban terbaik
- **Normalisasi Teks**: Menangani variasi penulisan kata dalam bahasa Indonesia
- **Data Dinamis**: Dapat memuat data FAQ dari file JSON
- **Interface Interaktif**: Antarmuka chat yang responsif dengan Streamlit
- **Contoh Pertanyaan**: Sidebar dengan pertanyaan-pertanyaan umum
- **Similarity Score**: Menampilkan skor kemiripan dan metode yang digunakan

## 🛠️ Teknologi yang Digunakan

- **Python 3.7+**
- **Streamlit** - Framework web app
- **scikit-learn** - TF-IDF vectorization dan cosine similarity
- **pandas & numpy** - Data manipulation
- **fuzzywuzzy** - Fuzzy string matching
- **python-Levenshtein** - Optimasi untuk fuzzywuzzy

## 📋 Persyaratan Sistem

- Python 3.7 atau lebih baru
- Minimal 512MB RAM
- Koneksi internet untuk instalasi dependencies

## 🚀 Instalasi

1. **Clone repository ini:**
```bash
git clone https://github.com/syahrulazka/chatbot-krs.git
cd chatbot-krs
```

2. **Buat virtual environment (opsional tapi direkomendasikan):**
```bash
python -m venv venv

# Untuk Windows
venv\Scripts\activate

# Untuk Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Buat folder data dan tambahkan file JSON (opsional):**
```bash
mkdir data
```

## 🏃‍♂️ Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada alamat `http://localhost:8501`

## 📁 Struktur Project

```
chatbot-krs/
├── app.py                 # File utama aplikasi Streamlit
├── requirements.txt       # Dependencies Python
├── README.md             # Dokumentasi project
├── data/                 # Folder untuk file JSON (opsional)
│   ├── faq1_chatbot.json
│   ├── faq2_chatbot.json
│   └── ...
└── .gitignore           # File gitignore
```

## 📄 Format Data JSON

Jika Anda ingin menambahkan data FAQ sendiri, buat file JSON di folder `data/` dengan format berikut:

```json
[
  {
    "pertanyaan": "Apa itu KRS dan bagaimana cara mengisinya?",
    "jawaban": "KRS (Kartu Rencana Studi) adalah dokumen yang berisi daftar mata kuliah yang akan diambil mahasiswa pada semester tertentu..."
  },
  {
    "pertanyaan": "Berapa maksimal SKS yang bisa diambil dalam satu semester?",
    "jawaban": "Maksimal SKS yang bisa diambil tergantung pada IPK semester sebelumnya..."
  }
]
```

## 🤖 Cara Kerja Chatbot

Chatbot menggunakan 3 metode untuk mencari jawaban terbaik:

1. **TF-IDF + Cosine Similarity** (Metode utama)
   - Mengubah teks menjadi vektor TF-IDF
   - Menghitung cosine similarity dengan pertanyaan di database
   - Threshold: 0.4

2. **Fuzzy Matching** (Metode cadangan)
   - Menggunakan algoritma Levenshtein distance
   - Cocok untuk menangani typo dan variasi penulisan
   - Threshold: 90%

3. **Sequence Matching** (Untuk input pendek)
   - Menggunakan SequenceMatcher untuk input ≤ 3 kata
   - Threshold: 60%

## 🎯 Contoh Pertanyaan yang Didukung

- "Apa itu KRS?"
- "Berapa maksimal SKS yang bisa diambil dalam satu semester?"
- "Kapan deadline pengisian KRS?"
- "Bagaimana cara mengubah mata kuliah setelah KRS dikunci?"
- "Apa syarat mengambil mata kuliah lintas fakultas?"

## ⚙️ Konfigurasi

Anda dapat mengubah beberapa parameter di class `KRSChatbot`:

```python
# Threshold untuk TF-IDF similarity
self.similarity_threshold = 0.4

# Threshold untuk fuzzy matching
self.fuzzy_threshold = 90
```

## 🤝 Kontribusi

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

## 📝 Pengembangan Selanjutnya

- [ ] Integrasi dengan database
- [ ] Penambahan fitur pembelajaran (learning)
- [ ] Support untuk file PDF dan Word
- [ ] API REST untuk integrasi eksternal
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Voice input/output

## 🐛 Troubleshooting

**Masalah instalasi fuzzywuzzy:**
```bash
pip install python-Levenshtein
```

**Error module tidak ditemukan:**
```bash
pip install --upgrade -r requirements.txt
```

**Streamlit tidak bisa diakses:**
- Pastikan firewall tidak memblokir port 8501
- Coba jalankan dengan: `streamlit run app.py --server.port 8502`

## 📞 Kontak

**Developer:** Syahrul Azka  
**Email:** [email@example.com]  
**GitHub:** [syahrulazka](https://github.com/syahrulazka)

## 📄 Lisensi

Project ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.

---

⭐ Jika project ini membantu Anda, jangan lupa berikan star di GitHub!
