# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from typing import Optional
# from datetime import datetime

# from app.database.session import get_db
# from app.services.trace_service import fetch_product, fetch_trace_logs, fetch_latest_status

# router = APIRouter(prefix="/product", tags=["Product"])

# # GET /product/{sku}?full=true
# @router.get("/{sku}")
# def get_product_by_sku(
#     sku: str,
#     full: Optional[bool] = Query(False),
#     db: Session = Depends(get_db)
# ):
#     product = fetch_product(db, sku, full) # type: ignore
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product

# # GET /product/{sku}/trace
# @router.get("/{sku}/trace")
# def get_trace(
#     sku: str,
#     from_date: Optional[datetime] = Query(None),
#     to_date: Optional[datetime] = Query(None),
#     status: Optional[str] = Query(None),
#     db: Session = Depends(get_db)
# ):
#     logs = fetch_trace_logs(db, sku, from_date, to_date, status)
#     return logs

# # GET /product/{sku}/latest
# @router.get("/{sku}/latest")
# def get_latest(
#     sku: str,
#     db: Session = Depends(get_db)
# ):
#     status = fetch_latest_status(db, sku)
#     if not status:
#         raise HTTPException(status_code=404, detail="No trace logs found for product")
#     return status

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.database.session import get_db
from app.services.trace_service import fetch_product, fetch_trace_logs, fetch_latest_status

router = APIRouter(prefix="/product", tags=["Product"])

# GET /product/{sku}?full=true&verify=true
@router.get("/{sku}")
def get_product_by_sku(
    sku: str,
    full: Optional[bool] = Query(False),
    verify: Optional[bool] = Query(False),
    db: Session = Depends(get_db)
):
    product = fetch_product(db, sku, full)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if full and verify:
        # Only verify if full details requested
        logs = fetch_trace_logs(db, sku, verify=True)
        return {
            "product": product,
            "trace_logs": logs
        }
    
    return product

# GET /product/{sku}/trace?verify=true
@router.get("/{sku}/trace")
def get_trace(
    sku: str,
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    status: Optional[str] = Query(None),
    verify: Optional[bool] = Query(False),
    db: Session = Depends(get_db)
):
    logs = fetch_trace_logs(db, sku, from_date, to_date, status, verify)
    return logs

# GET /product/{sku}/latest?verify=true
@router.get("/{sku}/latest")
def get_latest(
    sku: str,
    verify: Optional[bool] = Query(False),
    db: Session = Depends(get_db)
):
    status = fetch_latest_status(db, sku, verify)
    if not status:
        raise HTTPException(status_code=404, detail="No trace logs found for product")
    return status
