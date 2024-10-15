import pandas as pd
import chromadb
import uuid


class myPortfolio:
    def __init__(self, csv_path="techstack-portfolio.csv"):
        self.file_path = csv_path
        self.data = pd.read_csv(csv_path)
        self.chroma_client = chromadb.PersistentClient('my-vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="my-portfolio-collection")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])