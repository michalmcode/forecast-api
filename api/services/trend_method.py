import numpy as np
import pandas as pd


def calculate(data: dict) -> dict:
    periods = data["periods"] + 1

    df = pd.DataFrame(
        {
            "t": np.array(range(1, len(data["values"]) + 1), np.int64),
            "y": data["values"],
        }
    )

    df["t2"] = np.power(df["t"], 2)  # add a column with the time index squared
    df["yt"] = df["y"] * df["t"]  # add a column with the product of y and t
    df["t"] = df["t"].astype(np.int64)  # make sure it's an integer

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
    df_forecast

    return {
        "t": list(df_forecast["t"]),
        "forecast_value": list(df_forecast["y*"]),
        "error": list(df_forecast["error"]),
        "error_percentage": list(df_forecast["error_percentage"]),
    }
