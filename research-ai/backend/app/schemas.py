from pydantic import BaseModel
from typing import List, Optional
import datetime

class SummarizeRequest(BaseModel):
    text: str
    discipline: str

class SummarizeResponse(BaseModel):
    short_summary: str
    detailed_summary: str
    keywords: List[str]
    key_insights: List[str]
    discipline_interpretation: str

class CrossDomainRequest(BaseModel):
    text: str

class ClusterRequest(BaseModel):
    texts: List[str]

class ClusterData(BaseModel):
    text: str
    cluster: int
    x: float
    y: float

class ClusterResponse(BaseModel):
    clusters: List[ClusterData]

class HistoryResponse(BaseModel):
    id: int
    filename: str
    discipline: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
