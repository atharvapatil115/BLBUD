import os
import json
import pickle
import faiss
import numpy as np
import time

from mistralai.client import Mistral


class EmbeddingPipeline:

    def __init__(self, api_key):

        print("Loading embedding model (Mistral API)...")

        self.client = Mistral(api_key=api_key)
        self.model = "mistral-embed"

        print("Embedding model ready.")

    def create_embeddings(self, texts):

        all_embeddings = []

        batch_size = 5   # ✅ smaller batch to avoid 429 errors
        max_retries = 5  # ✅ retry attempts

        for i in range(0, len(texts), batch_size):

            batch = texts[i:i + batch_size]

            for attempt in range(max_retries):
                try:
                    response = self.client.embeddings.create(
                        model=self.model,
                        inputs=batch
                    )

                    batch_embeddings = [
                        item.embedding for item in response.data
                    ]

                    all_embeddings.extend(batch_embeddings)

                    # ✅ slight delay to avoid burst traffic
                    time.sleep(1)

                    break  # ✅ success, exit retry loop

                except Exception as e:
                    if "429" in str(e):
                        wait_time = 2 ** attempt
                        print(f"⚠️ Rate limited (429). Retrying in {wait_time}s...")

                        time.sleep(wait_time)
                    else:
                        # ❌ unknown error → stop
                        print(f"❌ Unexpected error: {e}")
                        raise e

            else:
                raise Exception("❌ Max retries exceeded for embedding batch")

        return np.array(all_embeddings, dtype=np.float32)

    def build_faiss_index(self, embeddings):

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)

        index.add(embeddings.astype(np.float32))

        return index

    def save_index(self, index, output_path):

        faiss.write_index(index, output_path)

        print(f"FAISS index saved: {output_path}")

    def save_metadata(self, metadata, output_path):

        with open(output_path, "wb") as file:
            pickle.dump(metadata, file)

        print(f"Metadata saved: {output_path}")


def process_embeddings_folder(
    chunks_folder,
    vector_store_folder
):

    os.makedirs(vector_store_folder, exist_ok=True)

    pipeline = EmbeddingPipeline(
        api_key=os.getenv("MISTRAL_API_KEY")
    )

    all_chunks = []
    all_texts = []

    for file_name in os.listdir(chunks_folder):

        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(chunks_folder, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            chunk_data = json.load(file)

        for chunk in chunk_data:
            all_chunks.append(chunk)
            all_texts.append(chunk["text"])

    print(f"Loaded {len(all_texts)} chunks")

    # ✅ Create embeddings (safe version with retry + batching)
    embeddings = pipeline.create_embeddings(all_texts)

    # ✅ Build FAISS index
    index = pipeline.build_faiss_index(embeddings)

    # ✅ Save index
    pipeline.save_index(
        index,
        os.path.join(vector_store_folder, "index.faiss")
    )

    # ✅ Save metadata
    pipeline.save_metadata(
        all_chunks,
        os.path.join(vector_store_folder, "metadata.pkl")
    )

    print("✅ Knowledge Base Created Successfully")