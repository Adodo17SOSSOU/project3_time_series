import pandas as pd
import matplotlib.pyplot as plt

def visualize_time_series(csv_path='data/synthetic_time_series.csv', save_path='data/ts_plot.png'):
    """
    Load the synthetic time series and visualize each sensor.
    """
    # Load the CSV
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)

    # Create figure
    plt.figure(figsize=(15, 6))
    for column in df.columns:
        plt.plot(df.index, df[column], label=column, alpha=0.8)

    plt.title("Synthetic Multivariate Time Series")
    plt.xlabel("Time")
    plt.ylabel("Sensor Values")
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()

    # Save to file
    plt.savefig(save_path)
    print(f" Time series plot saved as {save_path}")

if __name__ == "__main__":
    visualize_time_series()

