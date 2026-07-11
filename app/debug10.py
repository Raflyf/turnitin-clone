from engine.extractor import extract_text_from_pdf, get_sentences
from engine.web_scraper import get_candidate_urls, scrape_all_candidates
from engine.shingling import calculate_similarity
text = extract_text_from_pdf('d:/skripsi/skripsi_spam/Code_Spam_Email/uploads/skripsi_final_1783761567174.pdf')
print('Sentences:', len(get_sentences(text)))
urls = get_candidate_urls(get_sentences(text), max_probes=10)
print('URLs:', urls)
corpus = scrape_all_candidates(urls)
sorted_sources, sim, plag = calculate_similarity(text, corpus)
print('Sim:', sim)