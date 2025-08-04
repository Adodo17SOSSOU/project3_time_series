import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

def detect_anomalies(csv_path='data/synthetic_time_series.csv', save_path='data/anomaly_plot.png'):
    """
    Detect anomalies in a multivariate time series using ARIMA residuals.
    """
    # Load the data
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)

    anomalies = []
    plt.figure(figsize=(15, 6))

    # Analyze each sensor independently
    for i, column in enumerate(df.columns):
        series = df[column]

        # Fit ARIMA (p=2, d=0, q=2)
        model = ARIMA(series, order=(2, 0, 2))
        model_fit = model.fit()

        # Calculate residuals
        residuals = series - model_fit.fittedvalues

        # Define anomalies (3 standard deviations)
        threshold = 3 * residuals.std()
        sensor_anomalies = residuals[abs(residuals) > threshold]
        anomalies.append(sensor_anomalies)

        # Plot
        plt.plot(series.index, series, label=f"{column}")
        plt.scatter(sensor_anomalies.index, series.loc[sensor_anomalies.index],
                    color='red', label=f"{column} anomalies", marker='x')

    plt.title("Time Series with Detected Anomalies")
    plt.xlabel("Time")
    plt.ylabel("Sensor Values")
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    print(f" Anomaly detection plot saved as {save_path}")

if __name__ == "__main__":
    detect_anomalies()
