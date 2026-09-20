# Logistics Sales & Forecasting Platform

> An interactive operations intelligence dashboard for logistics performance, margin stress-testing, and capacity planning.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20Dashboard-ff4b4b?style=for-the-badge)](https://7qr53o653pfxp2bxhrsfku.streamlit.app/)
[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

## Live Demo

Explore the deployed dashboard:

**[Open the live Logistics Intelligence Dashboard](https://7qr53o653pfxp2bxhrsfku.streamlit.app/)**

![Live dashboard preview](assets/dashboard_latest2.png)

## Overview

This project models a global logistics network through an executive command-center interface. It combines a DuckDB warehouse, shipment analytics, forecast outputs, and interactive scenario controls so users can explore how demand and fuel conditions affect operational performance.

## Capabilities

- **Regional performance:** Compare operating profit across network regions with margin-based visual encoding.
- **Scenario modeling:** Test demand surges, fuel volatility, and AI capacity balancing in real time.
- **Executive KPIs:** Monitor revenue, operating profit, system-wide margin, and SLA compliance.
- **Operational signals:** Surface margin risk, demand pressure, fuel exposure, and data-quality status.
- **Forecasting:** Display a 30-day shipment-capacity outlook when the forecast artifact is available.
- **Portable analytics:** Run the complete dashboard from the bundled DuckDB database.

## Technology Stack

| Layer | Tools |
| --- | --- |
| Dashboard | Streamlit, Plotly |
| Analytics | DuckDB, Pandas, NumPy |
| Forecasting | Prophet |
| Data pipeline | Python, Faker, yfinance |
| Storage model | Fact and dimension tables in DuckDB |

## Run Locally

```powershell
git clone https://github.com/Lahiru1Niroosh/logistics-sales-platform.git
cd logistics-sales-platform

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

streamlit run app.py
```

Open <http://localhost:8501> in your browser.

The repository includes `data/logistics_warehouse.duckdb`, so the dashboard can run immediately. To rebuild the database and regenerate shipment data:

```powershell
python scripts/initialize_db.py
python scripts/ingest_shipments.py
python scripts/forecast_sales.py
```

## Repository Layout

```text
app.py                              Streamlit application
requirements.txt                    Runtime dependencies
data/logistics_warehouse.duckdb    Bundled analytics database
scripts/initialize_db.py            Database schema setup
scripts/ingest_shipments.py         Shipment data generation
scripts/forecast_sales.py           Forecast artifact generation
assets/dashboard_latest2.png        Current dashboard preview
```

## Deployment

The live application is hosted on Streamlit Community Cloud and deploys from the `main` branch of the GitHub repository:

- Repository: <https://github.com/Lahiru1Niroosh/logistics-sales-platform>
- App: <https://7qr53o653pfxp2bxhrsfku.streamlit.app/>

To deploy your own instance, create an app at <https://share.streamlit.io/>, select this repository, choose the `main` branch, and set `app.py` as the main file.

## Notes

- The bundled DuckDB file is required by the deployed dashboard.
- The forecast image is optional; the app displays a notice when it is unavailable.
- Keep the local `venv/` directory and secrets out of version control.
