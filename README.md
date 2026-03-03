# E-Commerce Shipping Charge Estimator

A B2B e-commerce marketplace shipping charge calculator built with FastAPI and MongoDB Atlas. This system helps Kirana stores calculate shipping costs for product deliveries.

## 🏗️ Architecture & Design Patterns

### System Design Principles:

- **Repository Pattern**: Abstracts data access layer
- **Service Layer Pattern**: Encapsulates business logic
- **Strategy Pattern**: Pluggable transport pricing strategies
- **Factory Pattern**: Creates appropriate transport strategies
- **Dependency Injection**: Loose coupling between components
- **Singleton Pattern**: Database connection management

### Tech Stack:

- **FastAPI**: Modern Python web framework
- **MongoDB Atlas**: Cloud NoSQL database
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation and settings

## 📁 Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── database.py          # Database connection & DI
├── models/
│   ├── entities.py      # Domain models
│   └── schemas.py       # API request/response schemas
├── repositories/
│   ├── base.py         # Abstract repository
│   ├── customer_repository.py
│   ├── seller_repository.py
│   ├── product_repository.py
│   └── warehouse_repository.py
├── services/
│   ├── shipping_service.py    # Shipping logic + Strategy pattern
│   └── warehouse_service.py   # Warehouse operations
├── api/
│   ├── warehouse.py     # Warehouse endpoints
│   └── shipping.py      # Shipping endpoints
└── utils/
    └── distance_calculator.py  # Haversine distance formula
```

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Update `.env` file with your MongoDB Atlas connection string:

```env
MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net/"
DATABASE_NAME="ecommerce_shipping"
```

### 5. Seed Database

```bash
python seed_data.py
```

### 6. Start Application

```bash
uvicorn app.main:app --reload
```

### 7. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📋 API Endpoints

### 1. Get Nearest Warehouse

```http
GET /api/v1/warehouse/nearest?sellerId=123&productId=456
```

**Response:**

```json
{
  "warehouseId": "789",
  "warehouseLocation": { "lat": 12.99999, "lng": 37.923273 }
}
```

### 2. Calculate Shipping Charge

```http
GET /api/v1/shipping-charge?warehouseId=789&customerId=456&deliverySpeed=standard
```

**Response:**

```json
{
  "shippingCharge": 150.0
}
```

### 3. Calculate End-to-End Shipping

```http
POST /api/v1/shipping-charge/calculate
Content-Type: application/json

{
  "sellerId": "123",
  "customerId": "456",
  "deliverySpeed": "express"
}
```

**Response:**

```json
{
  "shippingCharge": 180.0,
  "nearestWarehouse": {
    "warehouseId": "789",
    "warehouseLocation": { "lat": 12.99999, "lng": 37.923273 }
  }
}
```

## 🚛 Shipping Logic

### Transport Modes (Strategy Pattern)

| Transport Mode | Distance Range | Rate             |
| -------------- | -------------- | ---------------- |
| Mini Van       | 0-100km        | ₹3 per km per kg |
| Truck          | 100-500km      | ₹2 per km per kg |
| Aeroplane      | 500km+         | ₹1 per km per kg |

### Delivery Speeds

| Speed    | Cost                                      |
| -------- | ----------------------------------------- |
| Standard | ₹10 base + transport cost                 |
| Express  | ₹10 base + ₹1.2/kg extra + transport cost |

## 🏛️ Design Patterns Explained

### Repository Pattern

```python
class BaseRepository(ABC, Generic[T]):
    async def create(self, entity: T) -> T: ...
    async def find_by_id(self, id: str) -> Optional[T]: ...
```

### Strategy Pattern

```python
class TransportPricingStrategy(ABC):
    def calculate_rate(self, distance: float, weight: float) -> float: ...

class AeroplanePricingStrategy(TransportPricingStrategy): ...
class TruckPricingStrategy(TransportPricingStrategy): ...
```

### Factory Pattern

```python
class TransportModeFactory:
    @classmethod
    def get_strategy(cls, distance: float) -> TransportPricingStrategy:
        for strategy in cls.STRATEGIES:
            if strategy.is_applicable(distance):
                return strategy
```

## 📊 Sample Data

The system includes sample data for:

- **3 Customers**: Kirana stores in different cities
- **3 Warehouses**: BLR, Mumbai, Delhi
- **3 Sellers**: Located across India
- **3 Products**: Different weights and dimensions

## 🔒 Error Handling

The API provides comprehensive error handling:

- **400**: Bad Request (validation errors)
- **404**: Not Found (entities don't exist)
- **500**: Internal Server Error

## 🧪 Testing

Run the seed script to populate test data:

```bash
python seed_data.py
```

Then test endpoints using the generated IDs or through the interactive API docs.

## 🎯 Key Features

✅ **Clean Architecture**: Separation of concerns with layers
✅ **Design Patterns**: Strategy, Factory, Repository, Singleton
✅ **Async/Await**: Non-blocking database operations
✅ **Type Safety**: Full Pydantic validation
✅ **Error Handling**: Comprehensive exception management
✅ **Documentation**: Auto-generated OpenAPI docs
✅ **Dependency Injection**: Testable and maintainable code

## 🔮 Future Enhancements

- **Caching**: Redis for frequently accessed data
- **Authentication**: JWT-based API security
- **Rate Limiting**: Prevent API abuse
- **Monitoring**: Logging and metrics
- **Testing**: Unit and integration tests
- **Containerization**: Docker deployment

---

**Contact**: shreya.palit@jumbotail.com"
