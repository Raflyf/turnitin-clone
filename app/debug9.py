from engine.extractor import extract_text_from_pdf
text = extract_text_from_pdf('d:/skripsi/skripsi_spam/Code_Spam_Email/plagiarism_checker/app/uploads/skripsi_final_1783761567174.pdf')
print('Len:', len(text))
print(text[:200])