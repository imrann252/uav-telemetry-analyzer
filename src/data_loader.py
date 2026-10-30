import os
import pandas as pd

def load_flight_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Telemetry data not found at: {file_path}")
    
    print(f"Telemetry data found at {file_path}, loading...") 
    df=pd.read_csv(file_path)
    df.columns=[col.strip().lower() for col in df.columns]

    return df

