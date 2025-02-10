from .arxiv_service import ArxivService
from .pubmed_service import PubmedService
from concurrent.futures import ThreadPoolExecutor

class ResearchService:
    def __init__(self):
        self.arxiv_service = ArxivService()
        self.pubmed_service = PubmedService()

    def search(self, query, source='all', max_results=10):
        if source.lower() == 'arxiv':
            return self.arxiv_service.search(query, max_results)
        elif source.lower() == 'pubmed':
            return self.pubmed_service.search(query, max_results)
        
        # Search both sources in parallel if source is 'all'
        with ThreadPoolExecutor(max_workers=2) as executor:
            arxiv_future = executor.submit(self.arxiv_service.search, query, max_results // 2)
            pubmed_future = executor.submit(self.pubmed_service.search, query, max_results // 2)
            
            results = []
            try:
                results.extend(arxiv_future.result())
            except Exception as e:
                print(f"ArXiv search error: {str(e)}")
            
            try:
                results.extend(pubmed_future.result())
            except Exception as e:
                print(f"PubMed search error: {str(e)}")
            
        return sorted(results, key=lambda x: x.get('published', ''), reverse=True)
