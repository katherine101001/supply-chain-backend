#type: ignore

from sqlalchemy.orm import Session
from app.crud import trace
from app.schemas.schemas import ProductFull, TraceLog, ProductLatestStatus
from typing import List, Optional
from datetime import datetime
from app.blockchain.queries import verify_tx_on_chain

def fetch_product(db: Session, sku: str, full: bool = False):
    product = trace.get_product(db, sku)
    if not product:
        return None
    if full:
        return ProductFull.model_validate(product)
    # Basic info only
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
    status: Optional[str] = None,
    verify: bool = False
) -> List[TraceLog]:
    logs = trace.get_trace_logs(db, sku, from_date, to_date, status)
    result = []
    for log in logs:
        current_status = "Success" if log.tx_status == 1 else "Failure"
        verified_flag = None
        if verify:
            # Blockchain verification
            on_chain_success = verify_tx_on_chain(log.tx_hash)
            verified_flag = on_chain_success
            current_status = "Success" if on_chain_success else "Failure"

        result.append(
            TraceLog(
                timestamp=log.uploaded_at,
                blockchain_network=log.network,
                status=current_status,
                tx_hash=log.tx_hash,
                verified=verified_flag  
            )
        )
    return result

def fetch_latest_status(
    db: Session,
    sku: str,
    verify: bool = False
) -> Optional[ProductLatestStatus]:
    log = trace.get_latest_status(db, sku)
    if not log:
        return None

    status_text = "Success" if log.tx_status == 1 else "Failure"
    verified_flag = None
    if verify:
        on_chain_success = verify_tx_on_chain(log.tx_hash)
        verified_flag = on_chain_success
        status_text = "Success" if on_chain_success else "Failure"

    return ProductLatestStatus(
        sku=sku,
        latest_location=log.network,
        status=status_text,
        tx_hash=log.tx_hash,
        verified=verified_flag  # New field in schema
    )
