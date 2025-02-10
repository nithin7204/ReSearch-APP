import google.generativeai as genai
import os

class AIService:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_summary(self, abstract):
        prompt = f"""
        Please provide a concise summary of the following research paper abstract:
        {abstract}
        
        Focus on:
        1. Main research objective
        2. Key methodology
        3. Primary findings
        4. Significance of results
        
        Keep the summary clear and accessible while maintaining academic accuracy.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")

    def generate_preview(self, title, abstract):
        prompt = f"""
        Based on the following research paper title and abstract:
        Title: {title}
        Abstract: {abstract}
        
        Please provide:
        1. A one-sentence overview
        2. Three key takeaways
        3. Potential applications or implications
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error generating preview: {str(e)}")
