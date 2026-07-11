from googlesearch import search
try:
    print("Testing Google Search...")
    # Advanced returns objects with .url, .title, .description
    for result in search('"Machine learning adalah pergeseran paradigma dari pemrograman eksplisit"', num_results=3, advanced=True):
        print(result.url, result.title)
except Exception as e:
    print("Google Search Error:", e)
