import io
import math
from uuid import uuid4

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

from api.utils import aws_storage

# allows charts to be generated without a display (within the flask app)
matplotlib.use("Agg")


def determine_step(mean_value: float) -> int:
    """Determine the step for the y-axis

    Args:
        mean_value (float): The mean value in the DataFrame

    Returns:
        int: The step for the y-axis
    """
    exponent = math.floor(math.log10(mean_value))
    return 10**exponent


def generate(df: pd.DataFrame, df_forecast: pd.DataFrame) -> str:
    """Generate a chart with the forecast and uploads it to an S3 bucket

    Args:
        df (pd.DataFrame): Base DataFrame with columns `t` and `y`
        df_forecast (pd.DataFrame): Forecast DataFrame with columns `t` and `y*`

    Returns:
        str: The filename of the generated chart
    """
    plot_filename = f"{str(uuid4())}.png"

    plt.figure(figsize=(12, 6))

    plt.plot(df["t"], df["y"], ".-")
    plt.plot(df_forecast["t"], df_forecast["y*"], ".-", color="orange")

    plt.ylabel("values")
    plt.xlabel("time (periods)")
    plt.title("Forecast")

    xticks = np.arange(1, df_forecast["t"].iloc[-1] + 1, step=1)
    plt.xticks(xticks)

    yticks = np.arange(
        0, df_forecast["y*"].max() + 1000, step=determine_step(df["y"].mean())
    )
    plt.yticks(yticks)

    plt.grid(axis="y")

    bytes_io = io.BytesIO()
    plt.savefig(bytes_io, format="png")
    bytes_io.seek(0)
    plt.close()

    aws_storage.upload_file(bytes_io, plot_filename)
    return plot_filename
