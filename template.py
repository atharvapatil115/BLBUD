import os

PROJECT_STRUCTURE = {
    "data": [
        "raw_docs",
        "extracted_text",
        "chunks",
        "vector_store"
    ],
    "models": [],
    "src": {
        "ingestion": ["extractor.py"],
        "preprocessing": ["cleaner.py"],
        "chunking": ["chunker.py"],
        "embeddings": ["embedder.py"],
        "retrieval": ["retriever.py"],
        "llm": ["mistral.py"],
        "utils": ["helpers.py"]
    }
}

ROOT_FILES = [
    "main.py",
    "requirements.txt",
    "Dockerfile",
    ".env",
    "README.md"
]


def create_structure(base_path="."):
    
    # Create root files
    for file in ROOT_FILES:
        open(os.path.join(base_path, file), "a").close()

    # Create directories and files
    for folder, content in PROJECT_STRUCTURE.items():

        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        if isinstance(content, list):
            for subfolder in content:
                os.makedirs(
                    os.path.join(folder_path, subfolder),
                    exist_ok=True
                )

        elif isinstance(content, dict):

            for subfolder, files in content.items():

                subfolder_path = os.path.join(
                    folder_path,
                    subfolder
                )

                os.makedirs(
                    subfolder_path,
                    exist_ok=True
                )

                # __init__.py
                open(
                    os.path.join(
                        subfolder_path,
                        "__init__.py"
                    ),
                    "a"
                ).close()

                for file in files:
                    open(
                        os.path.join(
                            subfolder_path,
                            file
                        ),
                        "a"
                    ).close()

    print("✅ Project structure created successfully!")


if __name__ == "__main__":
    create_structure()