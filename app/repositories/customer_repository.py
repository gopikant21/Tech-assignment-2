from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from ..models.entities import Customer, Location
from .base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    """Repository for Customer entities"""

    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    def _to_entity(self, doc: dict) -> Customer:
        """Convert MongoDB document to Customer entity"""
        return Customer(
            id=doc["_id"],
            name=doc["name"],
            phone=doc["phone"],
            location=Location(**doc["location"]),
        )

    def _to_document(self, entity: Customer) -> dict:
        """Convert Customer entity to MongoDB document"""
        doc = {
            "name": entity.name,
            "phone": entity.phone,
            "location": entity.location.dict(),
        }
        if entity.id:
            doc["_id"] = ObjectId(entity.id)
        return doc
