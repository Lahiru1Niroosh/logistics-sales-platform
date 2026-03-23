import duckdb
import yfinance as yf
import random

def ingest_data(n_rows=50000):
    # 1. Connect to our existing database
    con = duckdb.connect('../data/logistics_warehouse.duckdb')
    
    print(f"--- 🚀 STARTING INGESTION OF {n_rows} SHIPMENTS ---")

    # 2. EXTRACT: Get real-time Market Data (Fuel Price)
    # Why? Because DHL's profit is tied to fuel costs.
    try:
        fuel = yf.Ticker("CL=F").history(period="1mo")
        current_fuel_price = fuel['Close'].iloc[-1]
        print(f"✅ Market Data Fetched: Current Fuel Price is ${current_fuel_price:.2f}")
    except Exception as e:
        current_fuel_price = 80.0  # Fallback price if API fails
        print("⚠️ Market API failed, using fallback fuel price.")

    # 3. TRANSFORM & LOAD: Generate 'Smart' Logistics Data
    # We use SQL for high-speed insertion
    print("⏳ Processing 50,000 records... please wait.")
    
    # First, we insert the raw shipment structure
    con.execute(f"""
        INSERT INTO fact_shipments
        SELECT 
            gen_random_uuid() as shipment_id,
            '2024-01-01'::DATE + (random() * 800)::INT as ship_date, 
            'Customer_' || (random() * 500)::INT as customer_name,
            (ARRAY['EMEA','AMER','APAC','LATAM'])[1 + (random() * 4)::INT] as region,
            (random() * 2 + 1)::INT as service_id,
            (random() * 50 + 0.5) as weight_kg,
            0.0 as revenue, 0.0 as cost, 0.0 as profit
        FROM repeat('a', {n_rows})
    """)

    # 4. BUSINESS LOGIC: Apply Revenue & Cost formulas
    # Revenue = (Rate * Weight) + Fuel Surcharge (10% of fuel price)
    # Cost = (Weight * 2.5) + Fixed Ops Fee ($15)
    con.execute(f"""
        UPDATE fact_shipments 
        SET 
            revenue = (weight_kg * (SELECT base_rate_per_kg FROM dim_services WHERE dim_services.service_id = fact_shipments.service_id)) + ({current_fuel_price} * 0.1),
            cost = (weight_kg * 2.5) + 15.0,
            profit = revenue - cost
    """)

    print(f"✅ SUCCESS: {n_rows} shipments loaded with real-world profit logic.")
    con.close()

if __name__ == "__main__":
    ingest_data(50000)