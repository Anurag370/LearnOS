from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.rag.chunking import split_documents
from app.ai.rag.loaders import load_document
from app.repositories.document import DocumentRepository
from app.ai.rag.embeddings import create_embedding_model


async def ingest_document(
    session: AsyncSession,
    course_id: int,
    file_path: str | Path,
    title: str | None = None,
    source: str | None = None,
) -> int:
    """
    Load, chunk, and persist a course document.

    Returns the database document ID.
    """

    path = Path(file_path)

    documents = load_document(path)

    if not documents:
        raise ValueError(
            f"No content found in document: {path}"
        )

    chunks = split_documents(documents)

    if not chunks:
        raise ValueError(
            f"No chunks generated from document: {path}"
        )

    embedding_model = create_embedding_model()

    texts = [
    chunk.page_content
    for chunk in chunks
    ]

    embeddings = embedding_model.embed_documents(
        texts
    )  

    repository = DocumentRepository(session)

    source = source or str(path)

    existing_document = await repository.get_by_source(
        source
    )

    if existing_document:
        raise ValueError(
            f"Document already exists: {source}"
        )

    document = await repository.create(
        course_id=course_id,
        title=title or path.stem,
        source=source,
        document_type=path.suffix.lower().lstrip("."),
    )

    for chunk, embedding in zip(chunks, embeddings):
        page_number = chunk.metadata.get("page")

        if page_number is not None:
            page_number = int(page_number) + 1

        await repository.create_chunk(
            document_id=document.id,
            chunk_index=chunk.metadata["chunk_index"],
            content=chunk.page_content,
            embedding=embedding,
            page_number=page_number,
        )

    await session.commit()

    return document.id