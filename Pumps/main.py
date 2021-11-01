from parse_curve import parse_xylect_curve, parse_excel_curve, parse_system_curve
from parameters import Pump, SystemCurve

PUMP_CURVE_FILEPATH = (
    r"/Users/jamesmoro/Documents/Python/OOP_Python/Pumps/pump_curves.xls"
)
GENERAL_CURVE_FILEPATH = (
    r"/Users/jamesmoro/Documents/Python/OOP_Python/Pumps/example_curves.xlsx"
)

SYSTEM_CURVE_FILEPATH = (
    r"/Users/jamesmoro/Documents/Python/OOP_Python/Pumps/system_curve.xlsx"
)


def xylect_test():
    pump_curve = parse_xylect_curve(
        PUMP_CURVE_FILEPATH
    )  # parsing the xylect .xls pump curve info as a dict

    pump1 = Pump(make="Xylem", model=pump_curve["Pump"], motor=pump_curve["Motor"])
    pump1.define_pumpcurve(flow=pump_curve["Flow [l/s]"], head=pump_curve["Head [m]"])
    pump1.define_efficiency(efficiency=pump_curve["Overall Efficiency [%]"])
    pump1.define_npshr(npshr=pump_curve["NPSHR-values [m]"])
    (
        pump1.generate_plot(BEP=True, POR=True)
        .add_npshr()
        .plot_speeds(BEP=True, POR="marker")
        .add_efficiency()
        .add_duty(duty_flow=300, duty_head=10, line=True)
        .show_plot(save=False, grid=True)
    )

    # pump1.BEP_at_speed(speed=70, print_string=True)


def general_curve_test():
    pump_curve = parse_excel_curve(
        GENERAL_CURVE_FILEPATH,
        flow="Flow",
        head="Head",
        efficiency="Efficiency",
        npshr="NPSHr",
    )
    pump1 = Pump(make="Xylem", model="test")
    pump1.define_pumpcurve(flow=pump_curve["Flow [l/s]"], head=pump_curve["Head [m]"])
    pump1.define_efficiency(efficiency=pump_curve["Overall Efficiency [%]"])
    pump1.define_npshr(npshr=pump_curve["NPSHR-values [m]"])
    (
        pump1.generate_plot(BEP=True, POR=True)
        .plot_speeds(BEP=True, POR="fill")
        .show_plot(grid=True)
    )
    pump1.BEP_at_speed(speed=70, print_string=True)


def system_curve_test():
    _system_curve = parse_system_curve(SYSTEM_CURVE_FILEPATH)
    system1 = SystemCurve(
        name="Test System", flow=_system_curve["Flow"], head=_system_curve["Head"]
    )
    system1.plot().show_plot()


import matplotlib.pyplot as plt

if __name__ == "__main__":
    xylect_test()
    # general_curve_test()
    # system_curve_test()
