from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository implementing Repository pattern.
    Provides common CRUD operations for all repositories.
    """

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    @abstractmethod
    def _to_entity(self, doc: dict) -> T:
        """Convert MongoDB document to entity"""
        pass

    @abstractmethod
    def _to_document(self, entity: T) -> dict:
        """Convert entity to MongoDB document"""
        pass

    async def create(self, entity: T) -> T:
        """Create a new entity"""
        doc = self._to_document(entity)
        result = await self.collection.insert_one(doc)
        entity.id = result.inserted_id
        return entity

    async def find_by_id(self, entity_id: str) -> Optional[T]:
        """Find entity by ID"""
        doc = await self.collection.find_one({"_id": ObjectId(entity_id)})
        return self._to_entity(doc) if doc else None

    async def find_all(self) -> List[T]:
        """Find all entities"""
        cursor = self.collection.find()
        docs = await cursor.to_list(length=None)
        return [self._to_entity(doc) for doc in docs]

    async def update(self, entity_id: str, entity: T) -> Optional[T]:
        """Update entity"""
        doc = self._to_document(entity)
        doc.pop("_id", None)  # Remove _id from update document
        result = await self.collection.update_one(
            {"_id": ObjectId(entity_id)}, {"$set": doc}
        )
        return await self.find_by_id(entity_id) if result.modified_count > 0 else None

    async def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        result = await self.collection.delete_one({"_id": ObjectId(entity_id)})
        return result.deleted_count > 0
