import pandas as pd
import numpy as np
import warnings
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import time
import os

warnings.filterwarnings("ignore")

WINDOW_SIZE = 100
THRESHOLD_STD = 3
LOG_FILE = "data/stream_log.csv"
PLOT_DIR = "data/anomaly_plots"  # Folder for saving plots

def stream_anomaly_detection_save(csv_path='data/synthetic_time_series.csv', sleep_time=0.05):
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)

    # Ensure plot folder exists
    os.makedirs(PLOT_DIR, exist_ok=True)

    # Initialize log file
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,sensor,actual,predicted,residual,anomaly\n")

    # Sliding window data
    window_data = {col: [] for col in df.columns}
    anomaly_points = {col: [] for col in df.columns}

    for timestamp, row in df.iterrows():
        for sensor in df.columns:
            # Update sliding window
            window_data[sensor].append(row[sensor])
            if len(window_data[sensor]) > WINDOW_SIZE:
                window_data[sensor].pop(0)

            # Detect anomalies only when window is full
            if len(window_data[sensor]) == WINDOW_SIZE:
                series = pd.Series(window_data[sensor])

                try:
                    model = ARIMA(series, order=(2, 0, 2))
                    model_fit = model.fit()
                    predicted = float(model_fit.forecast()[0])
                except Exception:
                    predicted = series.mean()  # fallback prediction

                residual = row[sensor] - predicted
                anomaly = abs(residual) > THRESHOLD_STD * series.std()

                # Log to CSV
                with open(LOG_FILE, "a") as f:
                    f.write(f"{timestamp},{sensor},{row[sensor]},{predicted},{residual},{int(anomaly)}\n")

                if anomaly:
                    anomaly_points[sensor].append((timestamp, row[sensor]))
                    print(f"[ALERT] {timestamp} - {sensor} anomaly detected: {row[sensor]:.2f} (pred {predicted:.2f})")

        time.sleep(sleep_time)

    # ===== After streaming: Generate PNGs =====
    #  Combined plot
    plt.figure(figsize=(12, 6))
    for sensor in df.columns:
        plt.plot(df.index, df[sensor], label=f"{sensor} Actual")
        if anomaly_points[sensor]:
            times, values = zip(*anomaly_points[sensor])
            plt.scatter(times, values, color='red', label=f"{sensor} Anomaly", marker='x')

    plt.title("Streaming Anomaly Detection - Combined")
    plt.xlabel("Timestamp")
    plt.ylabel("Sensor Values")
    plt.legend()
    plt.grid(True)
    combined_path = os.path.join(PLOT_DIR, "combined_anomalies.png")
    plt.savefig(combined_path, dpi=300)
    plt.close()

    #  Individual plots per sensor
    for sensor in df.columns:
        plt.figure(figsize=(12, 4))
        plt.plot(df.index, df[sensor], label=f"{sensor} Actual", color='blue')
        if anomaly_points[sensor]:
            times, values = zip(*anomaly_points[sensor])
            plt.scatter(times, values, color='red', label="Anomaly", marker='x')

        plt.title(f"Streaming Anomaly Detection - {sensor}")
        plt.xlabel("Timestamp")
        plt.ylabel("Sensor Value")
        plt.legend()
        plt.grid(True)
        sensor_path = os.path.join(PLOT_DIR, f"{sensor}_anomalies.png")
        plt.savefig(sensor_path, dpi=300)
        plt.close()

    print(f" Streaming complete. Log saved to {LOG_FILE}")
    print(f" Plots saved to folder: {PLOT_DIR}")

if __name__ == "__main__":
    stream_anomaly_detection_save()
