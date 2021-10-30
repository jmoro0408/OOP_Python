from re import L
import pandas as pd
from pathlib import Path
import json


def parse_xylect_curve(pump_curve_filepath: str):
    """Function parse the output of a xylect pump curve into a dictionary.
    This function expects the excel file to be in the standard Xylect output format.
    It first grabs the first three rows of the file, which are typically information about
    the specific pump i.e model, motor, and impeller info and stores them in a dict.
    It then deletes these rows and convert the rest of the available info into a dict, which
    is combined with the pump info dict.

    Args:
        pump_curve_filepath (str): location of the exported xylect curve (.xls)

    Returns:
        dictionary: a dictionary containing all the information from the xylect .xls
    """
    _pump_curve = pd.read_excel(pump_curve_filepath)
    _pump_info_dict = {
        "Pump": _pump_curve["Unnamed: 1"][0],
        "Motor": _pump_curve["Unnamed: 1"][1],
        "Impeller": _pump_curve["Unnamed: 1"][2],
    }
    _pump_curve = _pump_curve.iloc[4:, :]  # dropping the info already retrieved
    _pump_curve = _pump_curve.rename(columns=_pump_curve.iloc[0]).drop(
        _pump_curve.index[0]
    )  # swapping the header names with the first row
    _pump_curve = _pump_curve.dropna()  # remove missing values
    _pump_curve = _pump_curve.astype(
        float
    )  # have to convert values to float for future data wranging

    _pump_curve_dict = _pump_curve.to_dict(
        orient="list"
    )  # converting df to dict with strutcture {column: [values]}
    pump_dict = {**_pump_info_dict, **_pump_curve_dict}  # combining the two dicts

    del _pump_curve, _pump_info_dict, _pump_curve_dict  # deleting unused data

    return pump_dict


def parse_excel_curve(
    filepath: str,
    flow: str,
    head: str,
    npshr: str = None,
    npshr_flow: str = None,
    efficiency: str = None,
    efficiency_flow: str = None,
):
    """parses general excel data file into xylect-like structure.
    The exact column names for flow, head, efficiency etc must be provided as arguments

    Args:
        filepath (str): Filepath location
        flow (str): exact name of the column containing flow data
        head (str): exact name of the column containing head data
        npshr (str, optional): exact name of the column containing npshr data. Defaults to None.
        npshr_flow (str, optional): exact name of the column containing npshr flow data. If npshr_flow = None and npshr is not none, flow is assumed to match the pump curve flow. Defaults to None. Defaults to None.
        efficiency (str, optional): exact name of the column containing efficiency data. Defaults to None.. Defaults to None.
        efficiency_flow (str, optional): exact name of the column containing npshr flow data. If efficiency_flow = None and efficiency is not none, flow is assumed to match the pump curve flow. Defaults to None. Defaults to None.

    Returns:
        dict: dictionary holding pump data
    """
    heading_names = {
        flow: "Flow [l/s]",
        head: "Head [m]",
        npshr: "NPSHR-values [m]",
        npshr_flow: "NPSHR-Flow [l/s]",
        efficiency: "Overall Efficiency [%]",
        efficiency_flow: "Overall Efficiency Flow [l/s",
    }
    _pump_curve = pd.read_excel(filepath)
    _pump_curve.dropna(axis=0, how="all", inplace=True)
    _pump_curve = _pump_curve.rename(columns=_pump_curve.iloc[0]).drop(
        _pump_curve.index[0]
    )  # swapping the header names with the first row
    _pump_curve.rename(heading_names, axis=1, inplace=True)
    _pump_curve_dict = _pump_curve.to_dict(orient="list")

    return _pump_curve_dict


def write_json(pump_dict: dict):
    cwd = Path.cwd()
    save_path = Path(cwd / "data.json")
    with open(save_path, "w") as fp:
        json.dump(pump_dict, fp, indent=4)
    print(f"Pump curve data saved as data.json in {cwd} ")
