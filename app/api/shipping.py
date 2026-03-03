from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from ..models.schemas import (
    ShippingChargeResponse, 
    ShippingCalculateRequest, 
    ShippingCalculateResponse, 
    DeliverySpeed, 
    ErrorResponse
)
from ..services.shipping_service import ShippingService
from ..services.warehouse_service import WarehouseService
from ..database import get_shipping_service, get_warehouse_service, get_warehouse_repository

router = APIRouter(prefix="/api/v1", tags=["shipping"])


@router.get(
    "/shipping-charge",
    response_model=ShippingChargeResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    },
    summary="Get shipping charge from warehouse to customer",
    description="Calculate shipping charge based on warehouse, customer location, and delivery speed."
)
async def get_shipping_charge(
    warehouse_id: Annotated[str, Query(description="ID of the warehouse")],
    customer_id: Annotated[str, Query(description="ID of the customer")],
    delivery_speed: Annotated[DeliverySpeed, Query(description="Delivery speed: standard or express")],
    product_weight: Annotated[float, Query(description="Total weight of products in kg", gt=0)] = 1.0,
    shipping_service: ShippingService = Depends(get_shipping_service),
    warehouse_repo = Depends(get_warehouse_repository)
):
    """
    Calculate shipping charge from warehouse to customer.
    
    Args:
        warehouse_id: Warehouse unique identifier
        customer_id: Customer unique identifier
        delivery_speed: Standard or Express delivery
        product_weight: Total weight of products (default 1kg)
        shipping_service: Injected shipping service
        warehouse_repo: Injected warehouse repository
        
    Returns:
        Calculated shipping charge
        
    Raises:
        HTTPException: 404 if entities not found, 400 for validation errors
    """
    try:
        # Get warehouse
        warehouse = await warehouse_repo.find_by_id(warehouse_id)
        if not warehouse:
            raise HTTPException(
                status_code=404,
                detail={"error": "Not Found", "message": "Warehouse not found"}
            )
        
        # Calculate shipping charge
        charge = await shipping_service.calculate_shipping_charge(
            warehouse=warehouse,
            customer_id=customer_id,
            product_weights=product_weight,
            delivery_speed=delivery_speed
        )
        
        return ShippingChargeResponse(shipping_charge=charge)
        
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not Found", "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal Server Error", "message": "An unexpected error occurred"}
        )


@router.post(
    "/shipping-charge/calculate",
    response_model=ShippingCalculateResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    },
    summary="Calculate shipping charges for seller and customer",
    description="Calculate shipping charges by finding nearest warehouse and computing costs."
)
async def calculate_shipping_charges(
    request: ShippingCalculateRequest,
    shipping_service: ShippingService = Depends(get_shipping_service),
    warehouse_service: WarehouseService = Depends(get_warehouse_service)
):
    """
    Calculate shipping charges for a seller-customer transaction.
    
    Args:
        request: Request containing seller_id, customer_id, and delivery_speed
        shipping_service: Injected shipping service
        warehouse_service: Injected warehouse service
        
    Returns:
        Shipping charge and nearest warehouse information
        
    Raises:
        HTTPException: 404 if entities not found, 400 for validation errors
    """
    try:
        # Find nearest warehouse for seller
        warehouse = await warehouse_service.find_nearest_warehouse(request.seller_id)
        if not warehouse:
            raise HTTPException(
                status_code=404,
                detail={"error": "Not Found", "message": "Seller not found or no warehouses available"}
            )
        
        # For demo purposes, assume 1kg total weight
        # In real implementation, this would be calculated from the cart
        total_weight = 1.0
        
        # Calculate shipping charge
        charge = await shipping_service.calculate_shipping_charge(
            warehouse=warehouse,
            customer_id=request.customer_id,
            product_weights=total_weight,
            delivery_speed=request.delivery_speed
        )
        
        return ShippingCalculateResponse(
            shipping_charge=charge,
            nearest_warehouse={
                "warehouse_id": str(warehouse.id),
                "warehouse_location": warehouse.location
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail={"error": "Not Found", "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal Server Error", "message": "An unexpected error occurred"}
        )