from duckduckgo_search import DDGS

try:
    print("Testing DDGS...")
    results = DDGS().text('"Machine learning adalah pergeseran paradigma dari pemrograman eksplisit"', max_results=3)
    print(list(results))
except Exception as e:
    print("DDGS Error:", e)
