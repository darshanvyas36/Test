from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    """
    Custom Pydantic field type for MongoDB's ObjectId.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, *args, **kwargs):
        schema.update(type="string")


class AccountBase(BaseModel):
    """Base model with common fields."""
    username: str = Field(..., min_length=1, max_length=50)

class AccountCreate(AccountBase):
    """Model for creating a new account. Includes the password."""
    password: str = Field(..., min_length=6)

class AccountInDB(AccountBase):
    """Model representing the account as stored in the database."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True

class AccountPublic(AccountBase):
    """Model for representing an account in public-facing API responses."""
    id: str = Field(..., alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
