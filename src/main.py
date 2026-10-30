import os
import pandas as pd
from data_loader import load_flight_data
from kinematics import calculate_kinematics
from anomaly_detector import detect_flight_anomalies
from visualizer import generate_flight_plots

def run_pipeline():
    raw_path="data/raw/telemetry.csv"
    print(f"[*] Ingesting flight telemetry: {raw_path}")
    df_raw=load_flight_data(raw_path)

    print(f"[*] Computing kinematics rates and power draw...")
    df_kin=calculate_kinematics(df_raw)

    print(f"[*] Evaluating attitude and envelope thresholds...")
    df_processed,anomalies=detect_flight_anomalies(df_kin)

    duration_sec=(df_processed['timestamp_ms'].iloc[-1]-df_processed['timestamp_ms'].iloc[0])/1000.0
    max_alt=df_processed['altitude_agl_m'].max()
    max_climb= df_processed['climb_rate_mps'].max()
    max_sink = df_processed['climb_rate_mps'].min()
    peak_power = df_processed['power_w'].max()
    total_anomalies = len(anomalies)

    print("\n================ FLIGHT TELEMETRY SUMMARY ================")
    print(f"Total Telemetry Frames : {len(df_processed)}")
    print(f"Mission Duration       : {duration_sec:.2f} s")
    print(f"Max Altitude (AGL)     : {max_alt:.2f} m")
    print(f"Max Climb Rate         : {max_climb:.2f} m/s")
    print(f"Max Sink Rate          : {max_sink:.2f} m/s")
    print(f"Peak Power Draw        : {peak_power:.2f} W")
    print(f"Critical Events Flagged: {total_anomalies}")
    print("==========================================================\n")

    
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/anomaly_report.csv"
    anomalies.to_csv(report_path, index=False)
    print(f"[+] Anomaly report successfully saved to: {report_path}")
    print("MIN CLIMB RATE :", df_processed['climb_rate_mps'].min())
    print("MAX CLIMB RATE :", df_processed['climb_rate_mps'].max())
    print("SINK ANOMALIES :", df_processed['anomaly_sink'].sum())

    plot_path="reports/flight_telemetry_analysis.png"
    generate_flight_plots(df_processed,output_path=plot_path)

run_pipeline()
