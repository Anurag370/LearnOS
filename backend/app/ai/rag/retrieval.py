from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentChunk
from app.ai.rag.embeddings import embed_query

from pgvector.sqlalchemy import Vector
from langchain_core.documents import Document as lang_doc


@dataclass
class RetrievedChunk:
    chunk_id: int
    document_id: int
    content: str
    page_number: int | None
    module_id: int | None
    lesson_id: int | None
    source: str
    similarity: float

    def to_langchain_document(self) -> lang_doc:
        return lang_doc(
            page_content=self.content,
            metadata={
                "chunk_id": self.chunk_id,
                "document_id": self.document_id,
                "source": self.source,
                "page_number": self.page_number,
                "module_id": self.module_id,
                "lesson_id": self.lesson_id,
                "similarity": self.similarity,
            },
        )


async def search_similar_chunks(
    session: AsyncSession,
    query_embedding: list[float],
    course_id: int,
    top_k: int = 5,
) -> list[RetrievedChunk]:
    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    )

    similarity = 1 - distance

    statement = (
        select(
            DocumentChunk,
            Document.source,
            similarity.label("similarity"),
        )
        .join(
            Document,
            Document.id == DocumentChunk.document_id,
        )
        .where(
            Document.course_id == course_id,
            DocumentChunk.embedding.is_not(None),
        )
        .order_by(distance)
        .limit(top_k)
    )

    result = await session.execute(statement)

    rows = result.all()

    return [
        RetrievedChunk(
            chunk_id=chunk.id,
            document_id=chunk.document_id,
            content=chunk.content,
            page_number=chunk.page_number,
            module_id=chunk.module_id,
            lesson_id=chunk.lesson_id,
            source=source,
            similarity=float(similarity_score),
        )
        for chunk, source, similarity_score in rows
    ]


async def retrieve(
    session: AsyncSession,
    query: str,
    course_id: int,
    top_k: int = 5,
) -> list[RetrievedChunk]:
    query_embedding = embed_query(query)

    return await search_similar_chunks(
        session=session,
        query_embedding=query_embedding,
        course_id=course_id,
        top_k=top_k,
    )