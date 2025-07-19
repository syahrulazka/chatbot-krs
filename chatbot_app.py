import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
import json
import os
from datetime import datetime
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz, process

class KRSChatbot:
    def __init__(self):
        # Inisialisasi normalisasi kata terlebih dahulu
        self.word_normalizations = {
            'halo': ['halo', 'hallo', 'hai', 'hi', 'hello', 'hey'],
            'terima kasih': ['terima kasih', 'terimakasih', 'thanks', 'thx', 'makasih'],
            'tolong': ['tolong', 'tolongin', 'bantu', 'bantuin', 'help'],
            'selamat': ['selamat', 'slamat'],
            'bagaimana': ['bagaimana', 'gimana', 'gmn'],
            'kenapa': ['kenapa', 'mengapa', 'knp'],
            'dimana': ['dimana', 'di mana', 'dmn'],
            'kapan': ['kapan', 'kpn']
        }
        
        # Threshold settings
        self.similarity_threshold = 0.4
        self.fuzzy_threshold = 90  # Threshold untuk fuzzy matching
        
        # Load data dan inisialisasi model
        self.faq_data = self.load_json_data()
        
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words=self.get_indonesian_stopwords(),
            ngram_range=(1, 2),
            max_features=1000
        )
        
        self.questions = [item['pertanyaan'] for item in self.faq_data]
        self.answers = [item['jawaban'] for item in self.faq_data]
        
        processed_questions = [self.preprocess_text(q) for q in self.questions]
        self.tfidf_matrix = self.vectorizer.fit_transform(processed_questions)
    
    def load_json_data(self):
        data_folder = 'data'
        all_data = []
        
        # Baca semua file .json di folder data
        if os.path.exists(data_folder):
            json_files = [f for f in os.listdir(data_folder) if f.endswith('.json')]
            
            for json_file in json_files:
                file_path = os.path.join(data_folder, json_file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_data.extend(data)
                        else:
                            all_data.append(data)
                except Exception as e:
                    st.error(f"Error loading {json_file}: {e}")
        
        if not all_data:
            return self.get_default_data()
        
        return all_data
    
    def get_default_data(self):
        return [
            {
                "pertanyaan": "Apa itu KRS dan bagaimana cara mengisinya?",
                "jawaban": "KRS (Kartu Rencana Studi) adalah dokumen yang berisi daftar mata kuliah yang akan diambil mahasiswa pada semester tertentu. Cara mengisinya: 1) Login ke sistem akademik, 2) Pilih menu KRS, 3) Pilih mata kuliah yang diinginkan, 4) Pastikan tidak ada bentrok jadwal, 5) Submit KRS sebelum deadline."
            },
            {
                "pertanyaan": "Berapa maksimal SKS yang bisa diambil dalam satu semester?",
                "jawaban": "Maksimal SKS yang bisa diambil tergantung pada IPK semester sebelumnya: IPK ≥ 3.00 dapat mengambil maksimal 24 SKS, IPK 2.50-2.99 dapat mengambil maksimal 21 SKS, IPK 2.00-2.49 dapat mengambil maksimal 18 SKS, IPK < 2.00 dapat mengambil maksimal 15 SKS."
            },
            {
                "pertanyaan": "Kapan deadline pengisian KRS?",
                "jawaban": "Deadline pengisian KRS biasanya 2 minggu setelah masa registrasi dimulai. Tanggal pasti dapat dilihat di kalender akademik atau pengumuman dari bagian akademik."
            }
        ]
    
    def get_indonesian_stopwords(self):
        return [
            'yang', 'dan', 'di', 'ke', 'dari', 'dalam', 'dengan', 'untuk', 'pada', 'adalah',
            'atau', 'ini', 'itu', 'tidak', 'ada', 'akan', 'jika', 'bisa', 'dapat', 'sudah',
            'saya', 'anda', 'kamu', 'dia', 'mereka', 'kita', 'kami', 'nya', 'mu', 'ku',
            'apa', 'bagaimana', 'kapan', 'dimana', 'mengapa', 'siapa', 'berapa', 'mana',
            'juga', 'lebih', 'paling', 'sangat', 'sekali', 'masih', 'belum', 'sudah',
            'harus', 'perlu', 'ingin', 'mau', 'bisa', 'boleh', 'hanya', 'saja', 'lagi'
        ]
    
    def normalize_text(self, text):
        """Normalisasi teks dengan mengganti variasi kata"""
        text_lower = text.lower()
        
        for standard, variations in self.word_normalizations.items():
            for variation in variations:
                # Gunakan word boundary untuk menghindari partial match
                pattern = r'\b' + re.escape(variation) + r'\b'
                text_lower = re.sub(pattern, standard, text_lower)
        
        return text_lower
    
    def preprocess_text(self, text):
        # Normalisasi variasi kata terlebih dahulu
        text = self.normalize_text(text)
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def fuzzy_match(self, user_input, threshold=75):
        """Fuzzy matching menggunakan fuzzywuzzy"""
        try:
            # Cari pertanyaan dengan fuzzy matching
            matches = process.extract(user_input, self.questions, limit=3)
            
            best_matches = []
            for match, score in matches:
                if score >= threshold:
                    idx = self.questions.index(match)
                    best_matches.append({
                        'question': match,
                        'answer': self.answers[idx],
                        'score': score,
                        'index': idx
                    })
            
            return best_matches
            
        except Exception as e:
            st.error(f"Fuzzy matching error: {e}")
            return []
    
    def sequence_similarity(self, str1, str2):
        """Hitung similarity dengan SequenceMatcher"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def get_response(self, user_input):
        # Normalisasi input
        normalized_input = self.normalize_text(user_input)
        processed_input = self.preprocess_text(user_input)
        
        # 1. Coba TF-IDF similarity terlebih dahulu
        user_vector = self.vectorizer.transform([processed_input])
        similarities = cosine_similarity(user_vector, self.tfidf_matrix)[0]
        best_match_idx = np.argmax(similarities)
        best_similarity = similarities[best_match_idx]
        
        # 2. Jika TF-IDF similarity cukup tinggi, gunakan itu
        if best_similarity >= self.similarity_threshold:
            return {
                'answer': self.answers[best_match_idx],
                'similarity': best_similarity,
                'matched_question': self.questions[best_match_idx],
                'method': 'TF-IDF'
            }
        
        # 3. Jika TF-IDF gagal, coba fuzzy matching
        fuzzy_matches = self.fuzzy_match(user_input, self.fuzzy_threshold)
        if fuzzy_matches:
            best_fuzzy = fuzzy_matches[0]  # Ambil yang terbaik
            return {
                'answer': best_fuzzy['answer'],
                'similarity': best_fuzzy['score'] / 100,  # Konversi ke 0-1
                'matched_question': best_fuzzy['question'],
                'method': 'Fuzzy Matching'
            }
        
        # 4. Jika fuzzy matching gagal, coba sequence matching untuk input pendek
        if len(user_input.split()) <= 3:
            sequence_scores = []
            for i, question in enumerate(self.questions):
                score = self.sequence_similarity(user_input, question)
                sequence_scores.append((i, score))
            
            # Urutkan berdasarkan score
            sequence_scores.sort(key=lambda x: x[1], reverse=True)
            best_seq_idx, best_seq_score = sequence_scores[0]
            
            if best_seq_score > 0.6:  # Threshold untuk sequence matching
                return {
                    'answer': self.answers[best_seq_idx],
                    'similarity': best_seq_score,
                    'matched_question': self.questions[best_seq_idx],
                    'method': 'Sequence Matching'
                }
        
        # 5. Jika semua gagal, berikan fallback message
        return {
            'answer': self.get_fallback_message(),
            'similarity': best_similarity,
            'matched_question': None,
            'method': 'Fallback'
        }
    
    def get_fallback_message(self):
        return """Maaf, saya tidak dapat memahami pertanyaan Anda.

Berikut beberapa topik yang bisa saya bantu:

• Cara mengisi KRS dan deadline

• Batas maksimal SKS per semester

• Mata kuliah prasyarat

• Bentrok jadwal dan solusinya

• Konsultasi dengan dosen pembimbing

• Mata kuliah lintas fakultas

• Masalah teknis sistem akademik

• Biaya dan administrasi KRS

Silakan ajukan pertanyaan yang lebih spesifik."""

# Konfigurasi halaman
st.set_page_config(
    page_title="Chatbot KRS",
    page_icon="🎓",
    layout="centered"
)

# Inisialisasi chatbot
@st.cache_resource
def load_chatbot():
    return KRSChatbot()

# Inisialisasi session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Pesan pembuka dari chatbot
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Halo! Saya adalah chatbot KRS yang dapat membantu Anda seputar pertanyaan Kartu Rencana Studi. Silakan ajukan pertanyaan Anda!"
    })

# Header sederhana
st.title("🎓 Chatbot KRS")
st.markdown("Tanya jawab seputar Kartu Rencana Studi")

# Load chatbot
chatbot = load_chatbot()

# Tampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "similarity" in message:
            method = message.get('method', 'Unknown')
            st.caption(f"Similarity: {message['similarity']:.2f} | Method: {method}")

# Input dari user
if prompt := st.chat_input("Ketik pertanyaan Anda tentang KRS..."):
    # Tampilkan pesan user
    with st.chat_message("user"):
        st.write(prompt)
    
    # Tambahkan ke session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Proses dengan chatbot
    with st.chat_message("assistant"):
        with st.spinner("Memproses..."):
            response = chatbot.get_response(prompt)
        
        st.markdown(response['answer'])
        
        # Tampilkan info matching
        method = response.get('method', 'Unknown')
        st.caption(f"Similarity: {response['similarity']:.2f} | Method: {method}")
        
        # Tampilkan matched question jika ada
        if response['matched_question']:
            st.info(f"💡 Pertanyaan yang cocok: {response['matched_question']}")
    
    # Tambahkan respons ke session state
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response['answer'],
        "similarity": response['similarity'],
        "method": response.get('method', 'Unknown')
    })

# Sidebar dengan contoh pertanyaan
with st.sidebar:
    st.header("💡 Contoh Pertanyaan")
    
    sample_questions = [
        "Apa itu KRS?",
        "Berapa maksimal SKS yang bisa diambil dalam satu semester?",
        "Bagaimana prosedur pengajuan cuti akademik?",
        "Apa fungsi dosen pembimbing akademik?",
        "Kapan biasanya pengisian KRS dilakukan?",
        "Bagaimana jika terlambat mengisi KRS?",
        "Apakah mata kuliah bisa diganti setelah KRS dikunci?",
        "Apa pengertian cuti akademik?"
    ]
    
    for question in sample_questions:
        if st.button(question, key=f"sample_{question}"):
            # Tambahkan pertanyaan ke chat
            st.session_state.messages.append({"role": "user", "content": question})
            
            # Proses dengan chatbot
            response = chatbot.get_response(question)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response['answer'],
                "similarity": response['similarity'],
                "method": response.get('method', 'Unknown')
            })
            st.rerun()
    
    st.divider()
    
    # Tombol clear chat
    if st.button("🗑️ Hapus Chat"):
        st.session_state.messages = [
            {"role": "assistant", 
             "content": "Halo! Saya adalah chatbot KRS yang dapat membantu Anda seputar pertanyaan Kartu Rencana Studi. Silakan ajukan pertanyaan Anda!"}
        ]
        st.rerun()

# Footer
#st.markdown("---")
#st.markdown("Chatbot KRS - Universitas ABC")