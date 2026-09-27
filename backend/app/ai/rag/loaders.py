from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".md",
}


def load_document(path: str | Path) -> list[Document]:

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

    elif extension == ".md":
        content = file_path.read_text(
            encoding="utf-8"
        )

        documents = [
            Document(
                page_content=content,
                metadata={},
            )
        ]

    else:
        raise ValueError(
            f"Unsupported document type: {extension}"
        )

    for document in documents:
        document.metadata["source"] = str(file_path)
        document.metadata["file_name"] = file_path.name
        document.metadata["document_type"] = extension.lstrip(".")

    return documents