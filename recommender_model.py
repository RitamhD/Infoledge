from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class Recommender:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
        self.vectorstore = Chroma(
            embedding_function=self.embedding_model,
            persist_directory='controllers/model/embeddings',
            collection_name='course_embeddings'
        )
    
    def getRecommendation(self, query: str):
        vectorstore = self.vectorstore
        results = vectorstore.similarity_search(query=query, k=12)
        recommendations = [
            {
                'title': doc.metadata.get('title', 'No Title'),
                'url': doc.metadata.get('url', '#'),
                'category': doc.metadata.get('category', 'Unknown'),
                'sub_category': doc.metadata.get('sub_category', 'Unknown'),
            } for doc in results
        ]
        return recommendations
