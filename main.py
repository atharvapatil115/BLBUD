from src.ingestion.extractor import DocumentExtractor
from src.preprocessing.cleaner import process_text_folder
from src.chunking.chunker import process_chunking_folder
import os
from src.embeddings.embedder import EmbeddingPipeline
from src.embeddings.embedder import process_embeddings_folder
from src.retrieval.retriever import (
    Retriever,
    build_context
)
from src.retrieval.retriever import (
    Retriever,
    build_context
)

from src.llm.mistral import (
    MistralLLM
)
embedder = EmbeddingPipeline(api_key=os.getenv("MISTRAL_API_KEY"))
extractor = DocumentExtractor()

extractor.process_folder(
    input_folder="data/raw_docs",
    output_folder="data/extracted_text"

)

process_text_folder(
    input_folder="data/extracted_text",
    output_folder="data/cleaned_text"
)



process_chunking_folder(
    input_folder="data/cleaned_text",
    output_folder="data/chunks"
)


process_embeddings_folder(
    chunks_folder="data/chunks",
    vector_store_folder="data/vector_store"
    
)



# retriever = Retriever(
#     index_path="data/vector_store/index.faiss",
#     metadata_path="data/vector_store/metadata.pkl"
# )

# query = input(
#     "\nAsk Question: "
# )

# results = retriever.search(
#     query=query,
#     top_k=5
# )

# context = build_context(
#     results
# )

# print("\n")
# print("=" * 50)
# print("RETRIEVED CONTEXT")
# print("=" * 50)

# print(context)

# while True:
#     retriever = Retriever(
#         index_path="data/vector_store/index.faiss",
#         metadata_path="data/vector_store/metadata.pkl",

#     )

#     llm = MistralLLM()

#     query = input(
#         "\nAsk Question: "
#     )

#     results = retriever.search(
#         query=query,
#         top_k=5
#     )

#     context = build_context(
#         results
#     )

#     answer = llm.generate(
#         query=query,
#         context=context
#     )

#     print("\n")
#     print("=" * 50)
#     print("ANSWER")
#     print("=" * 50)
#     print(answer)