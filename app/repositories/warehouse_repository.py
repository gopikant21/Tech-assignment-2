from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from ..models.entities import Warehouse, Location
from .base import BaseRepository


class WarehouseRepository(BaseRepository[Warehouse]):
    """Repository for Warehouse entities"""

    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    def _to_entity(self, doc: dict) -> Warehouse:
        """Convert MongoDB document to Warehouse entity"""
        return Warehouse(
            id=doc["_id"], name=doc["name"], location=Location(**doc["location"])
        )

    def _to_document(self, entity: Warehouse) -> dict:
        """Convert Warehouse entity to MongoDB document"""
        doc = {"name": entity.name, "location": entity.location.dict()}
        if entity.id:
            doc["_id"] = ObjectId(entity.id)
        return doc
