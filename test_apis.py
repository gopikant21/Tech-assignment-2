import asyncio
import httpx
from app.database import db_manager


async def test_apis():
    """
    Simple test script to demonstrate API functionality.
    Make sure the server is running on localhost:8000 before running this.
    """
    base_url = "http://localhost:8000"

    async with httpx.AsyncClient() as client:
        print("🧪 Testing E-Commerce Shipping APIs\n")

        # Test 1: Health check
        print("1️⃣ Testing health endpoint...")
        response = await client.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")

        # Note: You'll need actual IDs from your seeded database
        # Run seed_data.py first and use the printed IDs

        # Test 2: Get nearest warehouse
        print("2️⃣ Testing nearest warehouse endpoint...")
        seller_id = "REPLACE_WITH_ACTUAL_SELLER_ID"
        product_id = "REPLACE_WITH_ACTUAL_PRODUCT_ID"

        try:
            response = await client.get(
                f"{base_url}/api/v1/warehouse/nearest",
                params={"sellerId": seller_id, "productId": product_id},
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Nearest Warehouse: {data}")
                warehouse_id = data["warehouseId"]
            else:
                print(f"Error: {response.json()}")
                return
        except Exception as e:
            print(f"⚠️ Replace IDs in test script with actual values from seed_data.py")
            print(f"Error: {e}")
            return

        print()

        # Test 3: Calculate shipping charge
        print("3️⃣ Testing shipping charge calculation...")
        customer_id = "REPLACE_WITH_ACTUAL_CUSTOMER_ID"

        try:
            response = await client.get(
                f"{base_url}/api/v1/shipping-charge",
                params={
                    "warehouseId": warehouse_id,
                    "customerId": customer_id,
                    "deliverySpeed": "standard",
                    "productWeight": 1.5,
                },
            )
            print(f"Status: {response.status_code}")
            print(f"Shipping Charge: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")

        print()

        # Test 4: End-to-end calculation
        print("4️⃣ Testing end-to-end shipping calculation...")

        try:
            response = await client.post(
                f"{base_url}/api/v1/shipping-charge/calculate",
                json={
                    "sellerId": seller_id,
                    "customerId": customer_id,
                    "deliverySpeed": "express",
                },
            )
            print(f"Status: {response.status_code}")
            print(f"Full Response: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    print("📝 Before running this test:")
    print("1. Start the FastAPI server: uvicorn app.main:app --reload")
    print("2. Run seed_data.py to populate the database")
    print("3. Update the IDs in this script with actual values")
    print("4. Then run this test script\n")

    asyncio.run(test_apis())
