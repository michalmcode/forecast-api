import numpy as np
import pandas as pd


def calculate(data: dict) -> dict:
    """Generate a forecast using the Moving Average Method

    Args:
        data (dict): Dictionary with the data to be used in the forecast.
            It should have the following structure:
            ```
            {
                "values": list
            }
            ```

    Returns:
        dict: A dictionary with the forecast.
    """
    window = 3

    df = pd.DataFrame(
        {
            "t": np.array(range(1, len(data["values"]) + 1), np.int64),
            "y": data["values"],
        }
    )
    df["y*"] = df["y"].rolling(window=window).mean().shift(1)
    df["error^2"] = np.power(df["y"] - df["y*"], 2)

    df_forecast = pd.DataFrame(
        {
            "t": [len(df) + 1],
            "y*": [np.round(df.tail(window)["y"].mean(), 2)],
            "error": [np.round(np.sqrt(df["error^2"].sum() / (len(df) - window)), 2)],
        }
    )

    return df_forecast.to_dict(orient="list")
