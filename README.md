# Logistics Sales & Forecasting Platform

An executive operations dashboard for logistics performance, margin stress-testing, and capacity planning. The application combines DuckDB analytics, simulated shipment data, market inputs, forecasting, and an interactive Streamlit interface.

![Live dashboard preview](assets/dashboard_latest2.png)

## What It Includes

- Regional operating-profit and margin analysis
- Live fuel-volatility and demand-surge scenarios
- AI capacity-balancing simulation
- System-wide margin gauge and operational alerts
- 30-day shipment forecast view
- DuckDB warehouse analytics model

## Technology

- **Frontend:** Streamlit
- **Analytics:** DuckDB, Pandas, NumPy, Plotly
- **Forecasting:** Prophet
- **Data pipeline:** Python, Faker, yfinance

## Run Locally

```powershell
git clone https://github.com/Lahiru1Niroosh/logistics-sales-platform.git
cd logistics-sales-platform

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts/initialize_db.py
python scripts/ingest_shipments.py
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

The checked-in DuckDB file at `data/logistics_warehouse.duckdb` allows the dashboard to run immediately. Re-run the initialization and ingestion scripts only when rebuilding the dataset.

## Project Structure

```text
app.py                         Streamlit dashboard
requirements.txt               Python dependencies
data/logistics_warehouse.duckdb Analytics database
scripts/initialize_db.py       Database setup
scripts/ingest_shipments.py    Shipment data ingestion
scripts/forecast_sales.py      Forecast generation
assets/dashboard_latest.png    Dashboard preview
```

## Publish With Streamlit Community Cloud

The repository is already connected to GitHub at:

<https://github.com/Lahiru1Niroosh/logistics-sales-platform>

1. Push the latest changes to the `main` branch.
2. Open <https://share.streamlit.io/> and sign in with GitHub.
3. Select **Create app**.
4. Choose `Lahiru1Niroosh/logistics-sales-platform`.
5. Set the branch to `main` and the main file to `app.py`.
6. Select **Deploy**.

The generated `streamlit.app` URL is the public live demo. Keep `app.py`, `requirements.txt`, the `data/` folder, and the DuckDB file in the repository because the hosted dashboard reads the database directly.

## Notes

- The forecast image is optional. The dashboard displays a notice if it has not been generated yet.
- Do not commit the local `venv/` folder.
- Do not commit API keys or other secrets.
