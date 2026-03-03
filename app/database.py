from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional
from .config import settings
from .repositories.customer_repository import CustomerRepository
from .repositories.seller_repository import SellerRepository
from .repositories.product_repository import ProductRepository
from .repositories.warehouse_repository import WarehouseRepository
from .services.shipping_service import ShippingService
from .services.warehouse_service import WarehouseService

# Global database client - Singleton pattern
class DatabaseManager:
    """
    Singleton database manager for MongoDB connections.
    Implements dependency injection for repositories and services.
    """
    
    _instance: Optional['DatabaseManager'] = None
    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(self):
        """Initialize database connection"""
        if self._client is None:
            self._client = AsyncIOMotorClient(settings.mongodb_url)
            self._database = self._client[settings.database_name]
    
    async def disconnect(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
    
    @property
    def database(self) -> AsyncIOMotorDatabase:
        """Get database instance"""
        if self._database is None:
            raise RuntimeError("Database not initialized. Call connect() first.")
        return self._database


# Global database manager instance
db_manager = DatabaseManager()


# Dependency injection functions for FastAPI
async def get_database() -> AsyncIOMotorDatabase:
    """Get database dependency"""
    return db_manager.database


# Repository dependencies
async def get_customer_repository() -> CustomerRepository:
    """Get customer repository dependency"""
    db = await get_database()
    return CustomerRepository(db.customers)


async def get_seller_repository() -> SellerRepository:
    """Get seller repository dependency"""
    db = await get_database()
    return SellerRepository(db.sellers)


async def get_product_repository() -> ProductRepository:
    """Get product repository dependency"""
    db = await get_database()
    return ProductRepository(db.products)


async def get_warehouse_repository() -> WarehouseRepository:
    """Get warehouse repository dependency"""
    db = await get_database()
    return WarehouseRepository(db.warehouses)


# Service dependencies
async def get_warehouse_service() -> WarehouseService:
    """Get warehouse service dependency"""
    warehouse_repo = await get_warehouse_repository()
    seller_repo = await get_seller_repository()
    return WarehouseService(warehouse_repo, seller_repo)


async def get_shipping_service() -> ShippingService:
    """Get shipping service dependency"""
    customer_repo = await get_customer_repository()
    product_repo = await get_product_repository()
    return ShippingService(customer_repo, product_repo)