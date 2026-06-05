import os
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(
        self,
        chunk_size=300,
        chunk_overlap=50
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def create_chunks(
        self,
        text
    ):

        return self.splitter.split_text(text)

    def save_chunks(
        self,
        chunks,
        source_file,
        output_path
    ):

        chunk_data = []

        for idx, chunk in enumerate(chunks):

            chunk_data.append(
                {
                    "chunk_id": idx,
                    "source_file": source_file,
                    "text": chunk
                }
            )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                chunk_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Saved {len(chunks)} chunks"
        )

def process_chunking_folder(
    input_folder,
    output_folder
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    chunker = TextChunker()

    for file_name in os.listdir(input_folder):

        if not file_name.endswith(".txt"):
            continue

        file_path = os.path.join(
            input_folder,
            file_name
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        chunks = chunker.create_chunks(
            text
        )

        output_file = (
            os.path.splitext(file_name)[0]
            + "_chunks.json"
        )

        output_path = os.path.join(
            output_folder,
            output_file
        )

        chunker.save_chunks(
            chunks,
            file_name,
            output_path
        )

        print(
            f" {file_name} -> {len(chunks)} chunks"
        )