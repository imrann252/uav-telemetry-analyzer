import pandas as pd
import numpy as np

def calculate_kinematics(df):
    data=df.copy()

    dt=data['timestamp_ms'].diff() / 1000.0

    altitude_smoothed = data['altitude_agl_m'].rolling(window=5, min_periods=1).mean()
    dh = altitude_smoothed.diff()
    data['climb_rate_mps'] = (dh / dt).fillna(0)

    d_roll=data['roll_deg'].diff()
    data['roll_rate_dps']=d_roll/dt

    data['power_w']=data['battery_voltage_v']*data['battery_current_a']
    data['climb_rate_mps']=data['climb_rate_mps'].fillna(0)
    data['roll_rate_dps']=data['roll_rate_dps'].fillna(0)

    return data
        
