from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
from ..models.schemas import WarehouseResponse, ErrorResponse
from ..services.warehouse_service import WarehouseService
from ..database import get_warehouse_service

router = APIRouter(prefix="/api/v1", tags=["warehouse"])


@router.get(
    "/warehouse/nearest",
    response_model=WarehouseResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse}
    },
    summary="Get nearest warehouse for a seller",
    description="Given a seller ID and product ID, return the nearest warehouse where the seller can drop off the product."
)
async def get_nearest_warehouse(
    seller_id: Annotated[str, Query(description="ID of the seller")],
    product_id: Annotated[str, Query(description="ID of the product")],
    warehouse_service: WarehouseService = Depends(get_warehouse_service)
):
    """
    Get the nearest warehouse for a seller.
    
    Args:
        seller_id: Seller's unique identifier
        product_id: Product's unique identifier (for future extensibility)
        warehouse_service: Injected warehouse service
        
    Returns:
        Nearest warehouse information
        
    Raises:
        HTTPException: 404 if seller not found, 400 for other errors
    """
    try:
        # Find nearest warehouse
        warehouse = await warehouse_service.find_nearest_warehouse(seller_id)
        
        if not warehouse:
            raise HTTPException(
                status_code=404,
                detail={"error": "Not Found", "message": "Seller not found or no warehouses available"}
            )
        
        return WarehouseResponse(
            warehouse_id=str(warehouse.id),
            warehouse_location=warehouse.location
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "Bad Request", "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Internal Server Error", "message": "An unexpected error occurred"}
        )