from pydantic import BaseModel
from typing import List
import model.lga as lga
import model.region as region
import model.state as state

class SearchResponse(BaseModel):
    regions: List[region.Region]
    states: List[state.State]
    lgas: List[lga.LGA]