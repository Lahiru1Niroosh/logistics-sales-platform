import duckdb
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def run_forecast():
    # 1. Connect and Extract Time-Series Data
    con = duckdb.connect('../data/logistics_warehouse.duckdb')
    
    print("\n--- 🔮 GENERATING SHIPMENT FORECAST ---")

    # Prophet requires a specific format: 'ds' (date) and 'y' (value)
    query = """
    SELECT 
        ship_date as ds, 
        COUNT(shipment_id) as y 
    FROM fact_shipments 
    GROUP BY 1 
    ORDER BY 1
    """
    df = con.execute(query).df()
    con.close()

    # 2. Initialize and Fit the Model
    # We tell Prophet to look for weekly and yearly patterns
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
    model.fit(df)

    # 3. Create a future timeframe (Predict next 30 days)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # 4. Professional Visualization
    print("✅ Forecast Complete. Generating Plot...")
    fig1 = model.plot(forecast)
    plt.title("Logistics Volume Forecast: Next 30 Days")
    plt.xlabel("Date")
    plt.ylabel("Shipment Volume")
    
    # Save the result so we can use it in our GitHub README later
    plt.savefig('../data/shipment_forecast.png')
    print("💾 Forecast plot saved to data/shipment_forecast.png")
    
    # 5. Business Insight
    predicted_avg = forecast.tail(30)['yhat'].mean()
    print(f"\n💡 STRATEGIC INSIGHT: We expect an average of {int(predicted_avg)} shipments per day next month.")

if __name__ == "__main__":
    run_forecast()