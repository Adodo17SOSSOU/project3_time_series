# Streaming Time Series Anomaly Detection

This project demonstrates **real-time anomaly detection** on time series sensor data using **ARIMA models**.
It simulates streaming data, detects anomalies, logs results, and **saves anomaly plots as PNGs**.

---

## 📂 Project Structure

```
project3_time_series/
│
├── data/
│   ├── synthetic_time_series.csv   # Input time series data
│   ├── stream_log.csv              # Streaming detection log
│   ├── anomaly_plots/              # Generated anomaly plots
│   │   ├── combined_anomalies.png
│   │   ├── sensor_1_anomalies.png
│   │   ├── sensor_2_anomalies.png
│   │   └── sensor_3_anomalies.png
│   └── ...
│
├── src/
│   ├── data_generator.py           # Generates synthetic time series
│   ├── anomaly_detector.py         # Core anomaly detection logic
│   ├── streaming_detector.py       # Simulates streaming + anomaly detection
│   ├── visualize.py                # Utility for plotting results
│   └── ...
│
├── requirements.txt
└── README.md
```

---

## ⚡ Features

* **Simulated streaming** from CSV files.
* **ARIMA-based anomaly detection** with sliding windows.
* **Automatic logging** of timestamps, sensor readings, predictions, residuals, and anomalies.
* **Visualization of anomalies** in PNG format (per sensor + combined view).

---

## 🛠 Installation

1. Clone the repository:

   ```bash
   git clone <your_repo_url>
   cd project3_time_series
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

### 1. Generate Synthetic Data

```bash
python src/data_generator.py
```

### 2. Run Streaming Anomaly Detection

```bash
python src/streaming_detector.py
```

* Logs results in `data/stream_log.csv`
* Prints alerts for detected anomalies

### 3. Visualize Anomalies

```bash
python src/visualize.py
```

* Saves anomaly plots to `data/anomaly_plots/`

---

## 📊 Output Example

* **CSV Log Example:**

```
timestamp,sensor,actual,predicted,residual,anomaly
2025-08-04 18:49:21,sensor_2,55.63,-91216.12,91271.75,1
2025-08-04 19:22:21,sensor_3,28.48,55.19,-26.71,0
```

* **Generated Plots:**

  * `sensor_1_anomalies.png`
  * `sensor_2_anomalies.png`
  * `sensor_3_anomalies.png`
  * `combined_anomalies.png`

---

## 📝 Notes

* Adjust `WINDOW_SIZE` and `THRESHOLD_STD` in `streaming_detector.py` for sensitivity tuning.
* Extremely large residuals or ARIMA failures will be logged with warnings.

---

## 📜 License

MIT License. Free to use and modify for research or production.
