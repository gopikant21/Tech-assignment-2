from pydantic import BaseModel
from typing import Optional
from enum import Enum
from .entities import Location


class DeliverySpeed(str, Enum):
    STANDARD = "standard"
    EXPRESS = "express"


class TransportMode(str, Enum):
    AEROPLANE = "aeroplane"
    TRUCK = "truck"
    MINI_VAN = "mini_van"


# Request Schemas
class ShippingCalculateRequest(BaseModel):
    seller_id: str
    customer_id: str
    delivery_speed: DeliverySpeed


class NearestWarehouseRequest(BaseModel):
    seller_id: str
    product_id: str


# Response Schemas
class WarehouseResponse(BaseModel):
    warehouse_id: str
    warehouse_location: Location


class ShippingChargeResponse(BaseModel):
    shipping_charge: float


class ShippingCalculateResponse(BaseModel):
    shipping_charge: float
    nearest_warehouse: WarehouseResponse


class ErrorResponse(BaseModel):
    error: str
    message: str
