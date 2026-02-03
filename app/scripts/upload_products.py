

import pandas as pd
from sqlalchemy import create_engine
from web3 import Web3
from app.config import DB_URL, SEPOLIA_RPC_URL, CONTRACT_ADDRESS, PRIVATE_KEY
import json
import math
from tqdm import tqdm
from datetime import datetime, timezone
from hexbytes import HexBytes

# -------------------------------
# 1️⃣ Connect to MySQL Database
# -------------------------------
engine = create_engine(DB_URL, echo=True, connect_args={"sslmode": "require"})

def get_uploaded_hashes():
    try:
        # 修改为小写的 record_hash 和 products
        df_existing = pd.read_sql("SELECT record_hash FROM products", engine)
        return set(df_existing['record_hash'].tolist())
    except Exception as e:
        print(f"Checking existing records: {e}")
        return set()

def save_to_db(df):
    """Save new dataset with recordHash into MySQL."""
    if df.empty:
        print("⚠️ No new records to save to DB")
        return
    
    column_mapping = {
        "SKU": "sku",
        "Product type": "product_type",
        "Price": "price",
        "Availability": "availability",
        "Num products sold": "num_products_sold",
        "Revenue generated": "revenue_generated",
        "Customer demographics": "customer_demographics",
        "Stock levels": "stock_levels",
        "Lead times": "lead_times",
        "Order quantities": "order_quantities",
        "Shipping times": "shipping_times",
        "Shipping carriers": "shipping_carriers",
        "Shipping costs": "shipping_costs",
        "Supplier name": "supplier_name",
        "Location": "location",
        "Production volumes": "production_volumes",
        "Manufacturing lead time": "manufacturing_lead_time",
        "Manufacturing costs": "manufacturing_costs",
        "Inspection results": "inspection_results",
        "Defect rates": "defect_rates",
        "Transportation modes": "transportation_modes",
        "Routes": "routes",
        "Costs": "costs",
        "recordHash": "record_hash" # 注意这里！模型里通常是 record_hash
    }


    df_mapped = df.rename(columns=column_mapping)
    # 过滤掉不在 mapping 里的列（防止报错）
    df_mapped = df_mapped[[col for col in column_mapping.values() if col in df_mapped.columns]]


    df_mapped.to_sql("products", engine, if_exists="append", index=False)
    print(f"✅ {len(df_mapped)} new records saved into Supabase")


def log_transaction_to_db(tx_data):
    """Save transaction record into blockchain_upload_logs table."""
    df_tx = pd.DataFrame([tx_data])
    df_tx.to_sql("blockchain_upload_logs", engine, if_exists="append", index=False)
    print(f"✅ Logged batch {tx_data['batch_number']} to blockchain_upload_logs table")


# -------------------------------
# 2️⃣ Load CSV & compute recordHash
# -------------------------------
def compute_record_hash(row, skip_columns=None):
    """Generate a bytes32 hash from key product fields."""
    if skip_columns is None:
        skip_columns = [
            "Price","Revenue generated","Customer demographics","Stock levels",
            "Lead times","Order quantities","Shipping times","Shipping carriers",
            "Shipping costs","Production volumes","Manufacturing lead time",
            "Manufacturing costs","Costs"
        ]
    data = "".join([str(row[col]) for col in row.index if col not in skip_columns])
    return Web3.keccak(text=data).hex()  # 0x + 64 hex chars

csv_path = "app/scripts/supply_chain_data.csv"
df = pd.read_csv(csv_path)

# Compute recordHash for all rows
df['recordHash'] = df.apply(compute_record_hash, axis=1)
print("✅ Record hashes computed for all products")

# -------------------------------
# 3️⃣ Filter out duplicates already in DB
# -------------------------------
uploaded_hashes = get_uploaded_hashes()
df_new_db = df[~df['recordHash'].isin(uploaded_hashes)]
if not df_new_db.empty:
    save_to_db(df_new_db)
else:
    print("⚠️ No new records to save to DB (all exist in DB)")

# -------------------------------
# 4️⃣ Connect to Sepolia & contract
# -------------------------------
w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
acct = w3.eth.account.from_key(PRIVATE_KEY)

with open("app/scripts/SupplyChainRegistry.json") as f:
    abi = json.load(f)
    if isinstance(abi, dict) and 'abi' in abi:
        abi = abi['abi']

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# -------------------------------
# 5️⃣ Check blockchain for existing products
# -------------------------------
df_to_upload = []

for idx, row in df.iterrows():
    try:
        product = contract.functions.getProduct(row['SKU']).call()
        chain_hash = product[3]
        if chain_hash.hex() != row['recordHash']:
            df_to_upload.append(row)
    except Exception:
        df_to_upload.append(row)  # SKU not found on-chain → upload

df_to_upload = pd.DataFrame(df_to_upload)

if df_to_upload.empty:
    print("⚠️ All products already exist on-chain. Nothing to upload.")
    exit(0)

print(f"✅ {len(df_to_upload)} new products confirmed for blockchain upload")

# -------------------------------
# 6️⃣ Upload in small batches (1-2 products)
# -------------------------------
BATCH_SIZE = 2
num_batches = math.ceil(len(df_to_upload) / BATCH_SIZE)

skus = df_to_upload['SKU'].tolist()
productTypes = df_to_upload['Product type'].tolist()
locations = df_to_upload['Location'].tolist()
statuses = df_to_upload['Inspection results'].tolist()
recordHashes = df_to_upload['recordHash'].tolist()

print(f"Total new products: {len(df_to_upload)}, initial batches: {num_batches}")

for i in tqdm(range(num_batches), desc="Uploading batches", unit="batch"):
    start = i * BATCH_SIZE
    end = min((i + 1) * BATCH_SIZE, len(skus))

    batch_skus = skus[start:end]
    batch_types = productTypes[start:end]
    batch_locations = locations[start:end]
    batch_statuses = statuses[start:end]
    batch_hashes = recordHashes[start:end]
    batch_hashes_bytes32 = [HexBytes(h) for h in batch_hashes]

    # Estimate gas
    try:
        gas_estimate = contract.functions.addProductsBatch(
            batch_skus, batch_types, batch_locations, batch_statuses, batch_hashes_bytes32
        ).estimate_gas({'from': acct.address})
    except Exception as e:
        tqdm.write(f"⚠️ Gas estimate failed for batch {i+1}: {e}")
        gas_estimate = 500_000

    gas_price = w3.to_wei('20', 'gwei')
    balance = w3.eth.get_balance(acct.address)
    tx_cost = gas_estimate * gas_price

    # Adjust batch if balance is low
    while tx_cost > balance and len(batch_skus) > 1:
        new_size = max(1, int(len(batch_skus) * (balance / tx_cost)))
        batch_skus = batch_skus[:new_size]
        batch_types = batch_types[:new_size]
        batch_locations = batch_locations[:new_size]
        batch_statuses = batch_statuses[:new_size]
        batch_hashes_bytes32 = batch_hashes_bytes32[:new_size]

        try:
            gas_estimate = contract.functions.addProductsBatch(
                batch_skus, batch_types, batch_locations, batch_statuses, batch_hashes_bytes32
            ).estimate_gas({'from': acct.address})
        except Exception:
            gas_estimate = 500_000

        tx_cost = gas_estimate * gas_price
        tqdm.write(f"⚠️ Adjusted batch {i+1} to {len(batch_skus)} due to balance")

    # Send transaction
    try:
        tx = contract.functions.addProductsBatch(
            batch_skus, batch_types, batch_locations, batch_statuses, batch_hashes_bytes32
        ).build_transaction({
            "from": acct.address,
            "nonce": w3.eth.get_transaction_count(acct.address),
            "gas": gas_estimate,
            "gasPrice": gas_price
        })

        signed_tx = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tqdm.write(f"Transaction sent for batch {i+1}: {tx_hash.hex()}")

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            tqdm.write(f"✅ Batch {i+1} mined in block {receipt.blockNumber}")

            # Log transaction info to DB
            # Get the block timestamp for uploaded_at
            # Get actual block timestamp
            block = w3.eth.get_block(receipt.blockNumber)
            uploaded_at = datetime.fromtimestamp(block.timestamp, tz=timezone.utc)

            # Compute transaction cost
            tx_cost_wei = receipt.gasUsed * tx['gasPrice']

            # Prepare transaction record
            tx_data = {
                "tx_hash": tx_hash.hex(),
                "block_number": receipt.blockNumber,
                "network": "sepolia",
                "wallet_address": acct.address,
                "batch_number": i+1,
                "num_records": len(batch_skus),
                "skus": ",".join(batch_skus),
                "gas_used": receipt.gasUsed,
                "gas_price": tx['gasPrice'],
                "tx_cost_wei": tx_cost_wei,
                "uploaded_at": uploaded_at
            }

            # Log to DB
            log_transaction_to_db(tx_data)



        else:
            tqdm.write(f"❌ Batch {i+1} failed!")

    except Exception as e:
        tqdm.write(f"❌ Error uploading batch {i+1}: {e}")

print("✅ All new batches uploaded to Sepolia blockchain")
