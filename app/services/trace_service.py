from sqlalchemy.orm import Session
from app.crud import trace
from app.schemas.schemas import ProductFull, TraceLog, ProductLatestStatus
from typing import List, Optional
from datetime import datetime

def fetch_product(db: Session, sku: str, full: bool = False):
    product = trace.get_product(db, sku)
    if not product:
        return None
    if full:
        return ProductFull.model_validate(product)
    # Return basic
    return {
        "sku": product.sku,
        "product_type": product.product_type,
        "price": product.price,
        "availability": product.availability
    }

def fetch_trace_logs(
    db: Session, 
    sku: str, 
    from_date: Optional[datetime] = None, 
    to_date: Optional[datetime] = None,
    status: Optional[str] = None
) -> List[TraceLog]:
    logs = trace.get_trace_logs(db, sku, from_date, to_date, status)
    return [
        TraceLog(
            timestamp=log.uploaded_at, # type: ignore
            location=log.network,  # adjust mapping if needed # type: ignore
            status="Success" if log.tx_status == 1 else "Failure", # type: ignore
            tx_hash=log.tx_hash # type: ignore
        )
        for log in logs
    ]

def fetch_latest_status(db: Session, sku: str) -> Optional[ProductLatestStatus]:
    log = trace.get_latest_status(db, sku)
    if not log:
        return None
    return ProductLatestStatus(
        sku=sku,
        latest_location=log.network, # type: ignore
        status="Success" if log.tx_status == 1 else "Failure",  # type: ignore
        tx_hash=log.tx_hash  # type: ignore
    )
