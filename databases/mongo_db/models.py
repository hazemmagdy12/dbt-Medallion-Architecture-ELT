from pydantic import BaseModel, Field
from typing import List, Optional

class BurgerModel(BaseModel):
    name: str = Field(..., description="Name of the burger item")
    ingredients: List[str] = Field(..., min_items=1, description="List of included ingredients")
    price: float = Field(..., gt=0, description="Price of the burger")
    is_available: Optional[bool] = True