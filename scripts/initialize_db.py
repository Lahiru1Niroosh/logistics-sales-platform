import duckdb

def setup_database():
    # 1. Connect to (or create) the database file
    # We store it in the 'data' folder
    con = duckdb.connect('../data/logistics_warehouse.duckdb')
    
    print("--- 🛠️ INITIALIZING LOGISTICS DATABASE ---")

    # 2. Create the 'Dimension' Table (The Categories)
    # This defines our shipping services at DHL
    con.execute("""
        CREATE OR REPLACE TABLE dim_services (
            service_id INTEGER PRIMARY KEY,
            service_name VARCHAR,
            base_rate_per_kg DOUBLE
        );
    """)

    # 3. Insert the Service Data
    con.execute("""
        INSERT INTO dim_services VALUES 
        (1, 'Express Worldwide', 15.50),
        (2, 'Economy Select', 8.20),
        (3, 'Global Freight', 4.50);
    """)

    # 4. Create the 'Fact' Table (The Transactions)
    # This is where the 50,000 shipments will live
    con.execute("""
        CREATE OR REPLACE TABLE fact_shipments (
            shipment_id UUID,
            ship_date DATE,
            customer_name VARCHAR,
            region VARCHAR,
            service_id INTEGER,
            weight_kg DOUBLE,
            revenue DOUBLE,
            cost DOUBLE,
            profit DOUBLE
        );
    """)

    print("✅ Database Schema and Service Table created successfully!")
    con.close()

if __name__ == "__main__":
    setup_database()