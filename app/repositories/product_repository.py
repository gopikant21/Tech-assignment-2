from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from ..models.entities import Product, Dimension
from .base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Repository for Product entities"""

    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    def _to_entity(self, doc: dict) -> Product:
        """Convert MongoDB document to Product entity"""
        return Product(
            id=doc["_id"],
            name=doc["name"],
            seller_id=doc["seller_id"],
            price=doc["price"],
            weight=doc["weight"],
            dimensions=Dimension(**doc["dimensions"]),
        )

    def _to_document(self, entity: Product) -> dict:
        """Convert Product entity to MongoDB document"""
        doc = {
            "name": entity.name,
            "seller_id": ObjectId(entity.seller_id),
            "price": entity.price,
            "weight": entity.weight,
            "dimensions": entity.dimensions.model_dump(),
        }
        if entity.id:
            doc["_id"] = ObjectId(entity.id)
        return doc

    async def find_by_seller_id(self, seller_id: str) -> List[Product]:
        """Find all products by seller ID"""
        cursor = self.collection.find({"seller_id": ObjectId(seller_id)})
        docs = await cursor.to_list(length=None)
        return [self._to_entity(doc) for doc in docs]
