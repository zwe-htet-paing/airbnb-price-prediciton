# Monitoring Setup Guide

## Starting the Services

To start all required services, run the following command:

```bash
docker-compose up
```

This will launch the following services:
* `db`: PostgreSQL database for storing metrics data.
* `adminer`: A database management tool for interacting with the PostgreSQL database.
* `grafana`: A visual dashboarding tool for monitoring and visualizing metrics.

### Sending Data to the Database

To calculate Evidently metrics using Prefect and send them to the database, run:

```bash
python evidently_metrics_calculation.py
```
This script simulates batch monitoring by performing the following actions:
* Collects data for a daily batch every 10 seconds.
* Calculates metrics using Evidently.
* Inserts the calculated metrics into the PostgreSQL database.

Once executed, the metrics will be available on Grafana in a preconfigured dashboard.

### Accessing the Dashboard

To access the Grafana dashboard:

1. Open your browser and navigate to: `http://localhost:3000`.
2. Use the default login credentials:
    * Username: admin
    * Password: admin
3. Navigate to the General/Home menu and click on Home.
4. Inside the General folder, select New Dashboard to view the preconfigured monitoring dashboard.

### Ad-hoc Debugging

For ad-hoc debugging, use the provided Jupyter Notebook:
* Run the following notebook: `debugging_nyc_taxi_data.ipynb`.
* This notebook demonstrates how to perform debugging with the help of Evidently Test Suites and Reports.

### Stopping the Services
To stop all running services, execute:

```bash
docker-compose down
```