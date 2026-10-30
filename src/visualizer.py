import os
import matplotlib.pyplot as plt

def generate_flight_plots(df, output_path="reports/flight_telemetry_analysis.png"):
    time_sec = (df['timestamp_ms'] - df['timestamp_ms'].iloc[0]) / 1000.0

   
    fig, (ax_alt, ax_att, ax_rate) = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

  
    ax_alt.plot(time_sec, df['altitude_agl_m'], color='navy', label='Altitude AGL (m)', linewidth=1.5)
    
   
    if df['anomaly_sink'].any():
        ax_alt.scatter(
            time_sec[df['anomaly_sink']],
            df.loc[df['anomaly_sink'], 'altitude_agl_m'],
            color='red', s=25, label='Critical Sink Rate (< -5 m/s)', zorder=5
        )
    ax_alt.set_ylabel('Altitude (m)', fontweight='bold')
    ax_alt.legend(loc='upper right')
    ax_alt.set_title('UAV Flight Telemetry & Envelope Breakdown', fontsize=14, fontweight='bold')

   
    ax_att.plot(time_sec, df['roll_deg'], color='teal', label='Roll Angle (deg)', linewidth=1.2)
    ax_att.plot(time_sec, df['pitch_deg'], color='goldenrod', label='Pitch Angle (deg)', linewidth=1.2)
    
  
    ax_att.axhline(45, color='teal', linestyle=':', alpha=0.6, label='Roll Limit (±45°)')
    ax_att.axhline(-45, color='teal', linestyle=':', alpha=0.6)
    ax_att.axhline(30, color='goldenrod', linestyle=':', alpha=0.6, label='Pitch Limit (±30°)')
    ax_att.axhline(-30, color='goldenrod', linestyle=':', alpha=0.6)

    
    if df['anomaly_roll'].any():
        ax_att.scatter(time_sec[df['anomaly_roll']], df.loc[df['anomaly_roll'], 'roll_deg'], color='red', s=20, zorder=5)
    if df['anomaly_pitch'].any():
        ax_att.scatter(time_sec[df['anomaly_pitch']], df.loc[df['anomaly_pitch'], 'pitch_deg'], color='darkred', s=20, zorder=5)

    ax_att.set_ylabel('Attitude (deg)', fontweight='bold')
    ax_att.legend(loc='upper right')

   
    ax_rate.plot(time_sec, df['roll_rate_dps'], color='indigo', label='Roll Rate (deg/s)', linewidth=1.0)
    ax_rate.axhline(150, color='gray', linestyle='--', alpha=0.7, label='Rate Limit (±150°/s)')
    ax_rate.axhline(-150, color='gray', linestyle='--', alpha=0.7)

    if df['anomaly_rate'].any():
        ax_rate.scatter(
            time_sec[df['anomaly_rate']],
            df.loc[df['anomaly_rate'], 'roll_rate_dps'],
            color='crimson', s=25, label='High Roll Rate (> 150°/s)', zorder=5
        )
    ax_rate.set_ylabel('Roll Rate (deg/s)', fontweight='bold')
    ax_rate.set_xlabel('Mission Time (s)', fontweight='bold')
    ax_rate.legend(loc='upper right')

    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[+] Multi-channel telemetry dashboard saved to: {output_path}")