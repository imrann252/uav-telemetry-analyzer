import pandas as pd

def detect_flight_anomalies(df):
    data=df.copy()

    data['anomaly_roll'] = data['roll_deg'].abs() > 45
    data['anomaly_pitch'] = data['pitch_deg'].abs() > 30
    data['anomaly_sink'] = data['climb_rate_mps'] < -8.0
    data['anomaly_rate'] = data['roll_rate_dps'].abs() > 150


    data['is_anomaly'] = (
        data['anomaly_roll'] | 
        data['anomaly_pitch'] | 
        data['anomaly_sink'] | 
        data['anomaly_rate']
    )
   

    anomaly_events=data[data['is_anomaly']]

    return data,anomaly_events