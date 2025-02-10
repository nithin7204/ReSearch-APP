import arxiv

class ArxivService:
    def __init__(self):
        self.client = arxiv.Client()

    def search(self, query, max_results=10):
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for paper in self.client.results(search):
            results.append({
                'id': paper.entry_id,
                'title': paper.title,
                'authors': [author.name for author in paper.authors],
                'abstract': paper.summary,
                'pdf_url': paper.pdf_url,
                'published': paper.published.strftime("%Y-%m-%d"),
                'source': 'arxiv'
            })
        
        return results
