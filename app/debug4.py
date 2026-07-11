from googlesearch import search
try:
    for r in search('"Machine learning adalah cabang kecerdasan buatan"', num_results=3, advanced=True):
        print(r.url)
except Exception as e:
    print("Error:", e)
