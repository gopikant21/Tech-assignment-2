from abc import ABC, abstractmethod
from typing import Dict
from ..models.entities import Warehouse, Customer, Product
from ..models.schemas import DeliverySpeed, TransportMode
from ..repositories.customer_repository import CustomerRepository
from ..repositories.product_repository import ProductRepository
from ..utils.distance_calculator import DistanceCalculator


# Strategy Pattern: Transport Mode Strategies
class TransportPricingStrategy(ABC):
    """Abstract base strategy for transport pricing"""
    
    @abstractmethod
    def calculate_rate(self, distance: float, weight: float) -> float:
        pass
    
    @abstractmethod
    def is_applicable(self, distance: float) -> bool:
        pass


class AeroplanePricingStrategy(TransportPricingStrategy):
    """Pricing strategy for air transport"""
    
    def calculate_rate(self, distance: float, weight: float) -> float:
        return 1.0 * distance * weight  # 1 Rs per km per kg
    
    def is_applicable(self, distance: float) -> bool:
        return distance >= 500


class TruckPricingStrategy(TransportPricingStrategy):
    """Pricing strategy for truck transport"""
    
    def calculate_rate(self, distance: float, weight: float) -> float:
        return 2.0 * distance * weight  # 2 Rs per km per kg
    
    def is_applicable(self, distance: float) -> bool:
        return 100 <= distance < 500


class MiniVanPricingStrategy(TransportPricingStrategy):
    """Pricing strategy for mini van transport"""
    
    def calculate_rate(self, distance: float, weight: float) -> float:
        return 3.0 * distance * weight  # 3 Rs per km per kg
    
    def is_applicable(self, distance: float) -> bool:
        return 0 <= distance < 100


# Factory Pattern: Transport Mode Factory
class TransportModeFactory:
    """Factory for creating transport pricing strategies"""
    
    STRATEGIES = [
        AeroplanePricingStrategy(),
        TruckPricingStrategy(),
        MiniVanPricingStrategy()
    ]
    
    @classmethod
    def get_strategy(cls, distance: float) -> TransportPricingStrategy:
        """Get appropriate transport strategy based on distance"""
        for strategy in cls.STRATEGIES:
            if strategy.is_applicable(distance):
                return strategy
        
        # Default to mini van for very short distances
        return MiniVanPricingStrategy()


class ShippingService:
    """
    Service for shipping charge calculations.
    Implements Strategy and Factory patterns for extensibility.
    """
    
    STANDARD_COURIER_CHARGE = 10.0  # Rs 10 base charge
    EXPRESS_EXTRA_CHARGE_PER_KG = 1.2  # Rs 1.2 per kg extra for express
    
    def __init__(self, customer_repo: CustomerRepository, product_repo: ProductRepository):
        self.customer_repo = customer_repo
        self.product_repo = product_repo
        self.distance_calculator = DistanceCalculator()
    
    async def calculate_shipping_charge(
        self, 
        warehouse: Warehouse, 
        customer_id: str, 
        product_weights: float,  # Total weight of all products
        delivery_speed: DeliverySpeed
    ) -> float:
        """
        Calculate shipping charge from warehouse to customer.
        
        Args:
            warehouse: Source warehouse
            customer_id: Target customer ID
            product_weights: Total weight of products
            delivery_speed: Standard or Express
            
        Returns:
            Total shipping charge
        """
        # Get customer
        customer = await self.customer_repo.find_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer not found: {customer_id}")
        
        # Calculate distance
        distance = self.distance_calculator.calculate_distance(
            warehouse.location, customer.location
        )
        
        # Get transport strategy
        transport_strategy = TransportModeFactory.get_strategy(distance)
        
        # Calculate base transport charge
        base_transport_charge = transport_strategy.calculate_rate(distance, product_weights)
        
        # Calculate total charge based on delivery speed
        total_charge = self.STANDARD_COURIER_CHARGE + base_transport_charge
        
        if delivery_speed == DeliverySpeed.EXPRESS:
            express_extra = self.EXPRESS_EXTRA_CHARGE_PER_KG * product_weights
            total_charge += express_extra
        
        return total_charge
    
    async def get_product_weight(self, product_id: str) -> float:
        """
        Get weight of a specific product.
        
        Args:
            product_id: Product ID
            
        Returns:
            Product weight in kg
        """
        product = await self.product_repo.find_by_id(product_id)
        if not product:
            raise ValueError(f"Product not found: {product_id}")
        
        return product.weight