from parse_curve import parse_xylect_curve
from parameters import Pump

PUMP_CURVE_FILEPATH = (
    r"/Users/jamesmoro/Documents/Python/OOP_Python/Pumps/pump_curves.xls"
)


if __name__ == "__main__":
    pump_curve = parse_xylect_curve(
        PUMP_CURVE_FILEPATH
    )  # parsing the xylect .xls pump curve info as a dict

    pump1 = Pump(make="Xylem", model=pump_curve["Pump"], motor=pump_curve["Motor"])
    pump1.define_pumpcurve(flow=pump_curve["Flow [l/s]"], head=pump_curve["Head [m]"])
    pump1.define_efficiency(efficiency=pump_curve["Overall Efficiency [%]"])
    pump1.define_npshr(npshr=pump_curve["NPSHR-values [m]"])

    pump1.generate_plot(BEP=True, POR=True).add_npshr().plot_speeds(False).show_plot()
