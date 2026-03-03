from typing import Optional
from ..repositories.warehouse_repository import WarehouseRepository
from ..repositories.seller_repository import SellerRepository
from ..models.entities import Warehouse, Seller
from ..utils.distance_calculator import DistanceCalculator


class WarehouseService:
    """
    Service for warehouse-related operations.
    Implements business logic for finding nearest warehouses.
    """
    
    def __init__(self, warehouse_repo: WarehouseRepository, seller_repo: SellerRepository):
        self.warehouse_repo = warehouse_repo
        self.seller_repo = seller_repo
        self.distance_calculator = DistanceCalculator()
    
    async def find_nearest_warehouse(self, seller_id: str) -> Optional[Warehouse]:
        """
        Find the nearest warehouse to a given seller.
        
        Args:
            seller_id: ID of the seller
            
        Returns:
            Nearest warehouse or None if seller not found
        """
        # Get seller location
        seller = await self.seller_repo.find_by_id(seller_id)
        if not seller:
            return None
        
        # Get all warehouses
        warehouses = await self.warehouse_repo.find_all()
        if not warehouses:
            return None
        
        # Find nearest warehouse using Strategy pattern approach
        nearest_warehouse = None
        min_distance = float('inf')
        
        for warehouse in warehouses:
            distance = self.distance_calculator.calculate_distance(
                seller.location, warehouse.location
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_warehouse = warehouse
        
        return nearest_warehouse