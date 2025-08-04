import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class TimeSeriesDataGenerator:
    def __init__(self, n_series=3, length=1000, freq='1min', anomaly_ratio=0.01):
        """
        n_series: number of sensor time series to simulate
        length: number of timestamps
        freq: frequency of data (pandas offset alias)
        anomaly_ratio: fraction of points to mark as anomalies
        """
        self.n_series = n_series
        self.length = length
        self.freq = freq
        self.anomaly_ratio = anomaly_ratio

    def generate(self):
        # Create a time index
        start_time = datetime.now()
        timestamps = pd.date_range(start=start_time, periods=self.length, freq=self.freq)

        data = {}
        for i in range(self.n_series):
            # Generate base time series with trend + seasonality + noise
            trend = np.linspace(0, 5, self.length)  # linear trend
            seasonality = 10 * np.sin(np.linspace(0, 20*np.pi, self.length))  # sine wave
            noise = np.random.normal(0, 1, self.length)  # Gaussian noise

            series = 50 + trend + seasonality + noise
            data[f'sensor_{i+1}'] = series

        df = pd.DataFrame(data, index=timestamps)
        
        # Inject anomalies
        n_anomalies = int(self.length * self.anomaly_ratio)
        anomaly_indices = np.random.choice(self.length, n_anomalies, replace=False)
        for idx in anomaly_indices:
            sensor = np.random.randint(0, self.n_series)
            df.iloc[idx, sensor] += np.random.choice([30, -30])  # spike or drop

        # Save CSV
        df.to_csv('data/synthetic_time_series.csv')
        print(f" Generated dataset with shape {df.shape} and saved to data/synthetic_time_series.csv")

        return df

if __name__ == "__main__":
    generator = TimeSeriesDataGenerator(n_series=3, length=1440, freq='1min', anomaly_ratio=0.02)
    generator.generate()
