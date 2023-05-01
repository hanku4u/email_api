from typing import List, Optional
from pydantic import BaseModel


# Base model for item fields
class ItemBase(BaseModel):

    # Define the common fields for creating and updating an item
    name: str
    description: Optional[str] = None
    price: int

# Input model for creating a new item. Uses same fields as ItemBase
class ItemCreate(ItemBase):
    pass

# Output model for returning an item. Inherits from ItemBase and also requires id field
class Item(ItemBase):

    # Add an id field to the item output model
    id: int

    class Config:
        # enbales pydantic to interpret attributes of the Item class to a column in the database
        orm_mode = True

# Input model for updating an item. use all the same fields as ItemBase
class ItemUpdate(ItemBase):
    pass

# Output model for returning a list of items
class ItemList(BaseModel):

    # Define a list of Item objects as the output field
    items: List[Item]