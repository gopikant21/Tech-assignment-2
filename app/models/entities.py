from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict
from pydantic_core import core_schema
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler
    ) -> core_schema.CoreSchema:
        return core_schema.with_info_plain_validator_function(
            cls.validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v, _info):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema, handler) -> Dict[str, Any]:
        return {"type": "string"}


class Location(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    lat: float
    lng: float


class Dimension(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    length: float  # in cm
    width: float  # in cm
    height: float  # in cm


class Product(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, json_encoders={ObjectId: str}
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    seller_id: PyObjectId
    price: float
    weight: float  # in kg
    dimensions: Dimension


class Customer(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, json_encoders={ObjectId: str}
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    phone: str
    location: Location


class Seller(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, json_encoders={ObjectId: str}
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    location: Location


class Warehouse(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, json_encoders={ObjectId: str}
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    name: str
    location: Location
