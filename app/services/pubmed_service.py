from Bio import Entrez
import json

class PubmedService:
    def __init__(self):
        Entrez.email = "your-email@example.com"  # Required by NCBI

    def search(self, query, max_results=10):
        # Search for paper IDs
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()

        if not record['IdList']:
            return []

        # Fetch paper details
        handle = Entrez.efetch(db="pubmed", id=record['IdList'], rettype="medline", retmode="text")
        papers = Entrez.read(handle)
        handle.close()

        results = []
        for paper in papers['PubmedArticle']:
            article = paper['MedlineCitation']['Article']
            results.append({
                'id': paper['MedlineCitation']['PMID'],
                'title': article['ArticleTitle'],
                'authors': [author['LastName'] + ' ' + author['ForeName'] 
                          for author in article.get('AuthorList', [])],
                'abstract': article.get('Abstract', {}).get('AbstractText', [''])[0],
                'published': article['Journal']['JournalIssue']['PubDate'].get('Year', ''),
                'source': 'pubmed'
            })

        return results
