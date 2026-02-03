from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.sql import func
from app.database.session import Base

class Product(Base):
    __tablename__ = "products"

    sku = Column(String, primary_key=True, index=True)
    product_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    availability = Column(Integer, default=0)
    num_products_sold = Column(Integer, default=0)
    revenue_generated = Column(Float, default=0.0)
    customer_demographics = Column(String, nullable=True)
    stock_levels = Column(Integer, default=0)
    lead_times = Column(Integer, default=0)
    order_quantities = Column(Integer, default=0)
    shipping_times = Column(Integer, default=0)
    shipping_carriers = Column(String, nullable=True)
    shipping_costs = Column(Float, default=0.0)
    supplier_name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    production_volumes = Column(Integer, default=0)
    manufacturing_lead_time = Column(Integer, default=0)
    manufacturing_costs = Column(Float, default=0.0)
    inspection_results = Column(String, nullable=True)
    defect_rates = Column(Float, default=0.0)
    transportation_modes = Column(String, nullable=True)
    routes = Column(String, nullable=True)
    costs = Column(Float, default=0.0)
    record_hash = Column(String, nullable=True)


class BlockchainUploadLog(Base):
    __tablename__ = "blockchain_upload_logs"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, nullable=False)
    block_number = Column(Integer, nullable=True)
    network = Column(String, nullable=False)
    wallet_address = Column(String, nullable=False)
    batch_number = Column(Integer, nullable=False)
    num_records = Column(Integer, nullable=False)
    skus = Column(String, nullable=False)
    gas_used = Column(BigInteger, nullable=True)
    gas_price = Column(BigInteger, nullable=True)
    tx_cost_wei = Column(BigInteger, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), default=func.now())
    tx_status = Column(Integer, default=1)  # 1=success, 0=failure
