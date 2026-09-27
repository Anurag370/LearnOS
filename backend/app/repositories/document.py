from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentChunk


class DocumentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_source(
        self,
        source: str,
    ) -> Document | None:
        result = await self.session.execute(
            select(Document).where(
                Document.source == source
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        course_id: int,
        title: str,
        source: str,
        document_type: str,
    ) -> Document:
        document = Document(
            course_id=course_id,
            title=title,
            source=source,
            document_type=document_type,
        )

        self.session.add(document)

        await self.session.flush()

        return document

    async def create_chunk(
        self,
        document_id: int,
        chunk_index: int,
        content: str,
        embedding: list[float],
        page_number: int | None = None,
        module_id: int | None = None,
        lesson_id: int | None = None,
    ) -> DocumentChunk:
        chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=chunk_index,
            content=content,
            embedding = embedding,
            page_number=page_number,
            module_id=module_id,
            lesson_id=lesson_id,
        )

        self.session.add(chunk)

        return chunk

    async def get_with_chunks(
        self,
        document_id: int,
    ) -> Document | None:
        result = await self.session.execute(
            select(Document)
            .where(Document.id == document_id)
        )

        return result.scalar_one_or_none()