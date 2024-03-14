from pydantic import BaseModel

class Region(BaseModel):
    id: int
    name: str