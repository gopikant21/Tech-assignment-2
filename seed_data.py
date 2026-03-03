import asyncio
from app.database import db_manager
from app.models.entities import Customer, Seller, Product, Warehouse, Location, Dimension
from app.repositories.customer_repository import CustomerRepository
from app.repositories.seller_repository import SellerRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.warehouse_repository import WarehouseRepository


async def seed_database():
    """
    Seed the database with sample data for testing.
    """
    print("Connecting to database...")
    await db_manager.connect()
    
    try:
        db = db_manager.database
        
        # Initialize repositories
        customer_repo = CustomerRepository(db.customers)
        seller_repo = SellerRepository(db.sellers)
        product_repo = ProductRepository(db.products)
        warehouse_repo = WarehouseRepository(db.warehouses)
        
        print("Clearing existing data...")
        # Clear existing collections (for demo purposes)
        await db.customers.delete_many({})
        await db.sellers.delete_many({})
        await db.products.delete_many({})
        await db.warehouses.delete_many({})
        
        # Create sample customers (Kirana stores)
        print("Creating customers...")
        customers = [
            Customer(
                name="Shree Kirana Store", 
                phone="9847******", 
                location=Location(lat=11.232, lng=23.445495)
            ),
            Customer(
                name="Andheri Mini Mart", 
                phone="9101******", 
                location=Location(lat=17.232, lng=33.445495)
            ),
            Customer(
                name="Delhi Corner Shop", 
                phone="9876******", 
                location=Location(lat=28.6139, lng=77.2090)
            )
        ]
        
        created_customers = []
        for customer in customers:
            created_customer = await customer_repo.create(customer)
            created_customers.append(created_customer)
            print(f"Created customer: {created_customer.name}")
        
        # Create sample warehouses
        print("Creating warehouses...")
        warehouses = [
            Warehouse(
                name="BLR_Warehouse", 
                location=Location(lat=12.99999, lng=37.923273)
            ),
            Warehouse(
                name="MUMB_Warehouse", 
                location=Location(lat=11.99999, lng=27.923273)
            ),
            Warehouse(
                name="DELHI_Warehouse", 
                location=Location(lat=28.7041, lng=77.1025)
            )
        ]
        
        created_warehouses = []
        for warehouse in warehouses:
            created_warehouse = await warehouse_repo.create(warehouse)
            created_warehouses.append(created_warehouse)
            print(f"Created warehouse: {created_warehouse.name}")
        
        # Create sample sellers
        print("Creating sellers...")
        sellers = [
            Seller(
                name="Nestle Seller", 
                location=Location(lat=12.9716, lng=77.5946)  # Bangalore
            ),
            Seller(
                name="Rice Seller", 
                location=Location(lat=19.0760, lng=72.8777)  # Mumbai
            ),
            Seller(
                name="Sugar Seller", 
                location=Location(lat=28.7041, lng=77.1025)  # Delhi
            )
        ]
        
        created_sellers = []
        for seller in sellers:
            created_seller = await seller_repo.create(seller)
            created_sellers.append(created_seller)
            print(f"Created seller: {created_seller.name}")
        
        # Create sample products
        print("Creating products...")
        products = [
            Product(
                name="Maggie 500g Packet",
                seller_id=created_sellers[0].id,
                price=10.0,
                weight=0.5,
                dimensions=Dimension(length=10, width=10, height=10)
            ),
            Product(
                name="Rice Bag 10Kg",
                seller_id=created_sellers[1].id,
                price=500.0,
                weight=10.0,
                dimensions=Dimension(length=50, width=30, height=20)
            ),
            Product(
                name="Sugar Bag 25kg",
                seller_id=created_sellers[2].id,
                price=700.0,
                weight=25.0,
                dimensions=Dimension(length=60, width=40, height=25)
            )
        ]
        
        for product in products:
            created_product = await product_repo.create(product)
            print(f"Created product: {created_product.name}")
        
        print("\n✅ Database seeded successfully!")
        print(f"Created {len(created_customers)} customers")
        print(f"Created {len(created_warehouses)} warehouses")
        print(f"Created {len(created_sellers)} sellers")
        print(f"Created {len(products)} products")
        
        # Print sample IDs for testing
        print("\n📋 Sample IDs for testing:")
        print(f"Customer ID: {created_customers[0].id}")
        print(f"Seller ID: {created_sellers[0].id}")
        print(f"Warehouse ID: {created_warehouses[0].id}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        await db_manager.disconnect()
        print("Database connection closed.")


if __name__ == "__main__":
    asyncio.run(seed_database())