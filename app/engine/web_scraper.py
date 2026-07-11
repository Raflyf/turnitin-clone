import time
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from ddgs import DDGS

def get_candidate_urls(sentences, max_probes=15):
    """Mencari kandidat URL jurnal/referensi menggunakan sampel kalimat"""
    ddgs = DDGS()
    probes = random.sample(sentences, min(len(sentences), max_probes))
    urls = set()
    
    print(f"Mencari kandidat URL dari {len(probes)} sampel kalimat (Multi-Threading)...")
    
    for i, probe in enumerate(probes):
        try:
            # Batasi panjang probe maksimal 15 kata agar mesin pencari tidak error/menolak kueri
            short_probe = " ".join(probe.split()[:15])
            
            # Cari kalimat di web tanpa tanda kutip agar DDG mengembalikan hasil terkait
            results = ddgs.text(f'{short_probe}', max_results=8)
            for res in list(results):
                if 'href' in res and not res['href'].endswith('.pdf'): 
                    urls.add(res['href'])
            time.sleep(random.uniform(1.5, 3)) # Hindari blokir DDG
        except Exception as e:
            continue
            
    print(f"Berhasil mengumpulkan {len(urls)} kandidat URL.")
    return list(urls)

def scrape_url(url):
    """Mengunduh konten teks dari suatu URL (Mirip crawler bot Turnitin)"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Ambil semua teks dari tag paragraf
            paragraphs = soup.find_all(['p', 'div', 'span'])
            text = " ".join([p.get_text() for p in paragraphs])
            # Bersihkan teks
            import re
            text = re.sub(r'\s+', ' ', text).strip()
            return url, text
    except:
        pass
    return url, ""

def scrape_all_candidates(urls):
    """Mengeksekusi multi-threading untuk mendownload isi artikel dari web"""
    corpus = {}
    print(f"Mengunduh isi dari {len(urls)} sumber web secara paralel...")
    
    with ThreadPoolExecutor(max_workers=40) as executor:
        results = executor.map(scrape_url, urls)
        for url, text in results:
            if len(text) > 100: # Hanya simpan web yang memiliki konten valid
                corpus[url] = text
                
    return corpus
