import faiss
import pickle
import numpy as np
import os

from mistralai.client import Mistral


class Retriever:

    def __init__(
        self,
        index_path,
        metadata_path,
        
    ):

        print("Loading FAISS Index...")

        self.index = faiss.read_index(
            index_path
        )

        print("Loading Metadata...")

        with open(
            metadata_path,
            "rb"
        ) as file:

            self.metadata = pickle.load(
                file
            )

        print("Initializing Embedding Client...")

        self.client = Mistral(
            api_key=os.getenv("MISTRAL_API_KEY")
        )

        self.model = "mistral-embed"

        print("Retriever Ready!")

    def search(
        self,
        query,
        top_k=5
    ):

        # ✅ replace local encode with API call
        response = self.client.embeddings.create(
            model=self.model,
            inputs=[query]
        )

        query_embedding = np.array(
            [response.data[0].embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < len(
                self.metadata
            ):

                results.append(
                    self.metadata[idx]
                )

        return results
    

def build_context(
    retrieved_chunks
):

    context = ""

    for chunk in retrieved_chunks:

        context += (
            chunk["text"]
            + "\n\n"
        )

    return context