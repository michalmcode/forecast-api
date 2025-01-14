import numpy as np
import pandas as pd

from api.utils import plot


def calculate(data: dict) -> tuple:
    """Generate a forecast using the Trend Method

    Args:
        data (dict): Dictionary with the data to be used in the forecast.
            It should have the following structure:
            ```
            {
                "periods": int,
                "values": list
            }
            ```

    Returns:
        tuple: A tuple with two elements: `(forecast, plot_filename)`.
    """
    periods = data["periods"] + 1

    df = pd.DataFrame(
        {
            "t": np.array(range(1, len(data["values"]) + 1), np.int64),
            "y": data["values"],
        }
    )

    df["t2"] = np.power(df["t"], 2)  # add a column with the time index squared
    df["yt"] = df["y"] * df["t"]  # add a column with the product of y and t

    # calculate the determinants
    # matrix W
    determinant_w = np.linalg.det(
        np.array(
            [
                [df["t"].iloc[-1], df["t"].sum()],
                [df["t"].sum(), df["t2"].sum()],
            ]
        )
    )

    # matrix Wa0
    determinant_wa0 = np.linalg.det(
        np.array(
            [
                [df["y"].sum(), df["t"].sum()],
                [df["yt"].sum(), df["t2"].sum()],
            ]
        )
    )

    # matrix Wa1
    determinant_wa1 = np.linalg.det(
        np.array(
            [
                [df["t"].iloc[-1], df["y"].sum()],
                [df["t"].sum(), df["yt"].sum()],
            ]
        )
    )

    a0 = determinant_wa0 / determinant_w  # calculate the a0 coefficient
    a1 = determinant_wa1 / determinant_w  # calculate the a1 coefficient

    # Forecasted value to existing ones
    df["y^"] = a0 + a1 * df["t"]

    # Calculate the forecast
    df_forecast = pd.DataFrame(
        np.array(range(df["t"].iloc[-1] + 1, df["t"].iloc[-1] + periods)),
        columns=["t"],
    )
    df_forecast["y*"] = np.round(a0 + a1 * df_forecast["t"], 2)

    # Calculate the error
    df["(y-y^)2"] = np.power(df["y"] - df["y^"], 2)
    df["(y-y_avg)2"] = np.power((df["y"] - df["y"].mean()), 2)
    df["(t-t_avg)2"] = np.power((df["t"] - df["t"].mean()), 2)

    variance = 1 / df["t"].iloc[-1] * df["(y-y^)2"].sum()
    standard_deviation = np.sqrt(variance)

    df_forecast["error"] = np.round(
        np.power(
            np.power(df_forecast["t"] - df["t"].mean(), 2) / df["(t-t_avg)2"].sum()
            + 1 / df["t"].iloc[-1]
            + 1,
            0.5,
        )
        * standard_deviation,
        2,
    )
    df_forecast["error_percentage"] = np.round(
        df_forecast["error"] / df_forecast["y*"] * 100, 2
    )

    # Generate the plot and upload to AWS S3
    plot_filename = ""
    try:
        plot_filename = plot.generate(df, df_forecast)
    except Exception:
        pass

    return (df_forecast.to_dict(orient="list"), plot_filename)
