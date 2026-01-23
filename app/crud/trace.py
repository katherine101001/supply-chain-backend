from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List, Optional
from app.models.models import Product, BlockchainUploadLog

# Get product by SKU
def get_product(db: Session, sku: str) -> Optional[Product]:
    return db.query(Product).filter(Product.sku == sku).first()


# Get blockchain trace logs for a product
def get_trace_logs(
    db: Session,
    sku: str,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    status: Optional[str] = None
) -> List[BlockchainUploadLog]:

    query = db.query(BlockchainUploadLog).filter(BlockchainUploadLog.skus.contains(sku))

    if from_date:
        query = query.filter(BlockchainUploadLog.uploaded_at >= from_date)
    if to_date:
        query = query.filter(BlockchainUploadLog.uploaded_at <= to_date)
    if status:
        query = query.filter(BlockchainUploadLog.tx_status == (1 if status.lower() == "success" else 0))

    return query.order_by(BlockchainUploadLog.uploaded_at.asc()).all()


# Get latest status for a product
def get_latest_status(db: Session, sku: str) -> Optional[BlockchainUploadLog]:
    return (
        db.query(BlockchainUploadLog)
        .filter(BlockchainUploadLog.skus.contains(sku))
        .order_by(BlockchainUploadLog.uploaded_at.desc())
        .first()
    )
