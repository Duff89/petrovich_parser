from pydantic import BaseModel


class Price(BaseModel):
    gold: float


class Product(BaseModel):
    price: Price
    title: str
    code: str


class Pagination(BaseModel):
    total: int


class Items(BaseModel):
    products: list[Product]
    pagination: Pagination
