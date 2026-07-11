import os
import sys
import time
import random
import argparse
import fitz  # PyMuPDF
from duckduckgo_search import DDGS

def read_document(filepath):
    """Membaca teks dari PDF atau TXT."""
    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    if ext == '.pdf':
        try:
            doc = fitz.open(filepath)
            for page in doc:
                text += page.get_text() + " "
            doc.close()
        except Exception as e:
            print(f"Error membaca PDF: {e}")
            sys.exit(1)
    elif ext == '.txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        print("Format tidak didukung. Gunakan .pdf atau .txt")
        sys.exit(1)
    return text

def extract_sentences(text):
    """Memecah teks menjadi kalimat dan memfilter kalimat terlalu pendek."""
    # Menghapus newline berlebihan
    text = text.replace('\n', ' ')
    import re
    # Pisahkan berdasarkan titik, tanda seru, atau tanda tanya
    sentences = re.split(r'(?<=[.!?]) +', text)
    valid_sentences = []
    for s in sentences:
        s = s.strip()
        # Filter kalimat yang kurang dari 6 kata (terlalu umum)
        if len(s.split()) >= 6:
            valid_sentences.append(s)
    return valid_sentences

def check_plagiarism(sentences, sample_size=20):
    """Mencari persentase plagiarisme via pencarian internet."""
    print(f"\nTotal kalimat ditemukan: {len(sentences)}")
    
    # Batasi sampel agar tidak terkena IP Ban
    if len(sentences) > sample_size:
        print(f"Mengambil sampel acak {sample_size} kalimat untuk mencegah blokir IP (Turnitin Mini Mode)...")
        sentences = random.sample(sentences, sample_size)
    else:
        print(f"Mengecek {len(sentences)} kalimat...")

    plagiarized_sentences = []
    ddgs = DDGS()
    
    for i, sentence in enumerate(sentences):
        # Gunakan exact match (tanda kutip)
        query = f'"{sentence}"'
        print(f"[{i+1}/{len(sentences)}] Memeriksa: {sentence[:50]}...")
        
        try:
            results = ddgs.text(query, max_results=3)
            # Karena generator, ubah ke list
            results_list = list(results)
            
            if len(results_list) > 0:
                print(f"   [!] PLAGIAT TERDETEKSI: Ditemukan di {results_list[0].get('href', 'Unknown')}")
                plagiarized_sentences.append({
                    "kalimat": sentence,
                    "sumber": results_list[0].get('href', 'Unknown')
                })
        except Exception as e:
            print(f"   [-] Gagal mencari (Mungkin rate limit): {e}")
            
        # Jeda 2-4 detik per pencarian agar aman dari blokir
        time.sleep(random.uniform(2, 4))
        
    return plagiarized_sentences, len(sentences)

def generate_report(plagiarized, total_checked, output_path="plagiarism_report.md"):
    """Menulis laporan akhir ke Markdown."""
    percentage = (len(plagiarized) / total_checked) * 100 if total_checked > 0 else 0
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 🕵️ Laporan Plagiarisme Mini Turnitin\n\n")
        f.write(f"- **Total Kalimat Diperiksa (Sampel):** {total_checked}\n")
        f.write(f"- **Kalimat Plagiat:** {len(plagiarized)}\n")
        f.write(f"- **Tingkat Plagiarisme (Indeks Kesamaan):** **{percentage:.2f}%**\n\n")
        
        if percentage > 25:
            f.write("> **⚠️ PERINGATAN:** Tingkat kemiripan tinggi (>25%). Harap lakukan parafrase!\n\n")
        else:
            f.write("> **✅ AMAN:** Tingkat kemiripan dalam batas toleransi akademik (<25%).\n\n")
            
        f.write("## 📝 Rincian Temuan\n\n")
        for i, item in enumerate(plagiarized):
            f.write(f"### Temuan {i+1}\n")
            f.write(f"> {item['kalimat']}\n\n")
            f.write(f"- 🔗 **Kemungkinan Sumber:** [{item['sumber']}]({item['sumber']})\n\n")

    print(f"\n[Selesai] Laporan disimpan ke {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Mini Turnitin - Local Plagiarism Checker via Web Search")
    parser.add_argument("file", help="Path ke file skripsi (.pdf atau .txt)")
    parser.add_argument("--sample", type=int, default=20, help="Jumlah kalimat acak untuk dicek (default 20 untuk hindari blokir IP)")
    args = parser.parse_args()
    
    text = read_document(args.file)
    sentences = extract_sentences(text)
    
    if not sentences:
        print("Tidak ada kalimat valid ditemukan di dokumen.")
        return
        
    plagiarized, total = check_plagiarism(sentences, sample_size=args.sample)
    generate_report(plagiarized, total, output_path=os.path.join(os.path.dirname(args.file), "plagiarism_report.md"))

if __name__ == "__main__":
    main()
