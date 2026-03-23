import duckdb
import pandas as pd

def run_analysis():
    # 1. Connect to our warehouse
    con = duckdb.connect('../data/logistics_warehouse.duckdb')
    
    print("\n--- 🔍 GENERATING BUSINESS INSIGHTS ---")

    # 2. Executive Summary Query
    # This joins our Fact and Dimension tables to see performance
    summary_query = """
    SELECT 
        f.region,
        d.service_name,
        SUM(f.revenue) as total_revenue,
        SUM(f.profit) as total_profit,
        COUNT(f.shipment_id) as shipment_count,
        (SUM(f.profit) / SUM(f.revenue)) * 100 as profit_margin_pct
    FROM fact_shipments f
    JOIN dim_services d ON f.service_id = d.service_id
    GROUP BY f.region, d.service_name
    ORDER BY profit_margin_pct DESC;
    """
    
    df = con.execute(summary_query).df()

    # 3. Print the Regional Strategy Table
    print("\n📈 Service Performance by Region (Sorted by Profitability):")
    print(df.to_string(index=False))

    # 4. Find the "Danger Zone"
    # We identify which service/region has the lowest margin
    worst_performer = df.iloc[-1]
    print(f"\n⚠️ BUSINESS ALERT: {worst_performer['service_name']} in {worst_performer['region']} "
          f"has the lowest profit margin at {worst_performer['profit_margin_pct']:.2f}%!")
    
    con.close()

if __name__ == "__main__":
    run_analysis()