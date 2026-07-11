from engine.shingling import calculate_similarity
doc='Machine learning adalah cabang dari kecerdasan buatan. Model akan belajar dari data.'
corpus={'url1': 'Ini teks web. Machine learning adalah cabang dari kecerdasan buatan. Jadi begitu.'}
print(calculate_similarity(doc, corpus))