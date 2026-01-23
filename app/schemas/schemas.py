from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Product info
class ProductBase(BaseModel):
    sku: str
    product_type: str
    price: float
    availability: int

class ProductFull(ProductBase):
    num_products_sold: Optional[int]
    revenue_generated: Optional[float]
    customer_demographics: Optional[str]
    stock_levels: Optional[int]
    lead_times: Optional[int]
    order_quantities: Optional[int]
    shipping_times: Optional[int]
    shipping_carriers: Optional[str]
    shipping_costs: Optional[float]
    supplier_name: Optional[str]
    location: Optional[str]
    production_volumes: Optional[int]
    manufacturing_lead_time: Optional[int]
    manufacturing_costs: Optional[float]
    inspection_results: Optional[str]
    defect_rates: Optional[float]
    transportation_modes: Optional[str]
    routes: Optional[str]
    costs: Optional[float]
    record_hash: Optional[str]

    model_config = {
        "from_attributes": True
    }

# Blockchain trace log
class TraceLog(BaseModel):
    timestamp: datetime
    location: str
    status: str
    tx_hash: str

    class Config:
        orm_mode = True

# Latest product status
class ProductLatestStatus(BaseModel):
    sku: str
    latest_location: str
    status: str
    tx_hash: str
