from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from ..models.entities import Seller, Location
from .base import BaseRepository


class SellerRepository(BaseRepository[Seller]):
    """Repository for Seller entities"""

    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    def _to_entity(self, doc: dict) -> Seller:
        """Convert MongoDB document to Seller entity"""
        return Seller(
            id=doc["_id"], name=doc["name"], location=Location(**doc["location"])
        )

    def _to_document(self, entity: Seller) -> dict:
        """Convert Seller entity to MongoDB document"""
        doc = {"name": entity.name, "location": entity.location.dict()}
        if entity.id:
            doc["_id"] = ObjectId(entity.id)
        return doc
