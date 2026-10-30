# UAV Flight Telemetry Analysis and Anomaly Detection

A modular Python pipeline designed to process UAV flight telemetry, derive kinematic and electrical parameters, screen for flight envelope violations, and export multi-channel diagnostic dashboards.

## Architecture

data/raw/telemetry.csv
       |
       v
[data_loader.py]       -> Telemetry ingestion and validation
       |
       v
[kinematics.py]        -> Derives climb rates, roll rates and power draw
       |
       v
[anomaly_detector.py]  -> Multi-threshold envelope monitoring
       |
       v
[visualizer.py]        -> Generates 3-axis flight envelope plot
       |
       v
[main.py]              -> Mission metrics summary and report export

## Features

- Kinematic Derivations: Calculates vertical speed (climb rate) using rolling-window smoothing to eliminate numerical derivative noise, computes roll rate, and tracks total electrical power consumption (Watts).
- Rule-Based Anomaly Detection: Flags critical attitude limits (roll beyond 45 deg, pitch beyond 30 deg), excessive sink rates (faster than -8.0 m/s), and uncommanded high roll rates (above 150 deg/s).
- Multi-Channel Visualization: Generates a synchronized three-panel telemetry dashboard highlighting detected anomalies directly on the corresponding sensor channels.

## Project Structure

.
|-- data/
|   `-- raw/
|       `-- telemetry.csv
|-- reports/
|   |-- anomaly_report.csv
|   `-- flight_telemetry_analysis.png
|-- src/
|   |-- __init__.py
|   |-- data_loader.py
|   |-- kinematics.py
|   |-- anomaly_detector.py
|   |-- visualizer.py
|   `-- main.py
|-- requirements.txt
`-- README.md

## Installation and Usage

1. Install dependencies:
pip install -r requirements.txt

2. Run the processing pipeline:
python -m src.main

## Output

- reports/anomaly_report.csv: Tabular export containing all telemetry timestamps flagged for critical envelope exceedances.
- reports/flight_telemetry_analysis.png: Synchronized multi-panel plot covering altitude profiles, attitude angles, and angular rates.