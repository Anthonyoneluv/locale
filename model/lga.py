from pydantic import BaseModel

class LGA(BaseModel):
    id: int
    name: str
    state_id: int