from engine.web_scraper import scrape_all_candidates
urls=['https://aws.amazon.com/id/what-is/machine-learning/', 'https://medium.com/@rizkinurulfahmi/lets-defend-email-analysis-challenge-9d1dd4403564']
corpus = scrape_all_candidates(urls)
for u, t in corpus.items(): print(u, len(t))