import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# TODO - fix legend
# TODO - Add system curve plotting option
# TODO - Add capability to provide custom AOR and POR points
# TODO - Add auto duty point based on system and pump curves


class Pump:

    default_speeds = [90, 80, 70, 60, 50]
    flow = None
    head = None

    def __init__(self, make, model, impeller=None, motor=None):
        self.make = make
        self.model = model
        self.impeller = impeller
        self.motor = motor

    def __repr__(self):
        return f"{self.make}, {self.model}"

    def fullname(self):
        """Return the pump make and model

        Returns:
            str: make and model of pump
        """
        return self.make + " " + self.model

    def define_pumpcurve(self, flow: list, head: list):
        """assigns flow and head curves to the pump

        Args:
            flow (list): list of flows
            head (list): list of head achieved at corresponding flows
        """
        self.flow = flow
        self.head = head

    def define_efficiency(self, efficiency: list, efficiency_flow: list = None):
        """Add an efficiency to the pump. By default this assume the efficiency values
        correspond to the flow defined in the pump head/flow curve. However this can be
        overwritten by providing a new efficiency_flow list to this method.

        Args:
            efficiency (list): pump efficiency list
            efficiency_flow (list, optional): Flow corresponding to efficiency values. Defaults to None.
        """
        self.efficiency = efficiency
        self.efficiency_flow = self.flow
        if efficiency_flow is not None:
            self.efficiency_flow = efficiency_flow

    def define_npshr(self, npshr: list, npshr_flow: list = None):
        """Add a net positive suction head required (npshr) to the pump.
        By default this assume the npshr values correspond to the flows
        defined in the pump head/flow curve. However this can be overwritten by
        providing a new npshr_flow list to this method.

        Args:
            npshr (list): npshr values
            npshr_flow (list, optional): flow corresponding to npshr. If none, this
            defaults to the flow provided in the flow/head curve. Defaults to None.
        """
        self.npshr = npshr
        self.npshr_flow = self.flow
        if npshr_flow is not None:
            self.npshr_flow = npshr_flow

    def BEP(self):
        """return the best efficiency point for a given pump.
        will return the best efficiency (%), followed by the corresponding flow and head

        Returns:
            tuple: BEP of the pump in (efficiency, flow, head)
        """
        try:
            _max_efficiency_index = self.efficiency.index(max(self.efficiency))
            poly = self.generate_curve_equation(
                self.efficiency_flow, self.head, deg=3
            )  # generating flow/head curve polynomial
            _max_efficiency_head = poly(self.efficiency_flow[_max_efficiency_index])

            best_efficiency_point = (
                max(self.efficiency),
                self.efficiency_flow[_max_efficiency_index],
                _max_efficiency_head,
            )
        except AttributeError:
            print("Error: Please assign efficiency before calculating the BEP")
            return None

        return best_efficiency_point

    def generate_affinity(self, new_speed: int):
        """Uses pump affinity laws to create new pump/head curves based on an inputted speed.
            This function expects the self.flow values to correspond to the pump at 100%.
        Args:
            new_speed (int): New pump speed to create flow/head values for

        Returns:
            (tuple): Tuple of two lists, containing reduced flow and reduced head values
        """
        flow_multplier, head_multipler = self.affinity_ratio(
            new_speed
        )  # assumes original pump curve is at 100% speed
        reduced_flow = [flow * flow_multplier for flow in self.flow]
        reduced_head = [head * head_multipler for head in self.head]

        return reduced_flow, reduced_head

    def generate_speed_curves(self, speeds: list = None):
        """generate multiple speeds curves for a given list.
        Default speeds are [90,80,70,60,50]% however these can be overwritted with a
        provided list of speeds.

        Args:
            speeds (list, optional): List of speeds to create. If none provided,
            speeds of [90,80,70,60,50]% are created. Defaults to None.

        Returns:
            dict: dictionary of speeds and corresponding head and flow.
            dict has structure {speed: ([flow], [head])}
        """
        if (isinstance(speeds, int)) or (isinstance(speeds, float)):
            speeds = [speeds]
        _speeds = self.default_speeds  # typical % speeds
        if speeds is not None:
            _speeds = speeds
        speed_curve_dict = {}  # empty dict to hold our speed data.
        for speed in _speeds:
            flow, head = self.generate_affinity(new_speed=speed)
            _temp_dict = {speed: (flow, head)}
            speed_curve_dict.update(_temp_dict)
        return speed_curve_dict

    def POR(self):
        """creates upper and lower preferred operating points for a given pump speed.
        This assume HI guidance (lower = 70% BEP flow, upper = 120% BEP flow)

        Returns:
            tuple: coordinates of upper and lower POR.
            POR_upper_flow, POR_upper_head, POR_lower_flow, POR_lower_head

        """
        poly = self.generate_curve_equation(
            self.flow, self.head, deg=3
        )  # generating flow/head curve polynomial

        _, BEP_flow, BEP_head = self.BEP()  # disregard the best efficiency (%)
        POR_lower_flow = (
            0.7 * BEP_flow
        )  # POR lower range is 70% of the BEP (Hydraulic Institute)
        POR_lower_head = poly(POR_lower_flow)
        POR_upper_flow = (
            1.2 * BEP_flow
        )  # POR upper range is 120% of the BEP (Hydraulic Institute)
        POR_upper_head = poly(POR_upper_flow)

        POR_dict = {
            "Upper Flow": POR_upper_flow,
            "Upper Head": POR_upper_head,
            "Lower Flow": POR_lower_flow,
            "Lower Head": POR_lower_head,
        }
        return POR_dict

    @staticmethod
    def generate_curve_equation(x: list, y: list, deg=3):
        """returns a 1d poly object for a given x and y

        Args:
            x (list): x values to curve fit
            y (list): y values to curve fit
            deg (int, optional): degree of curve. Defaults to 3.

        Returns:
            [poly1d]: np.poly1d object of curve
        """
        coeff = np.polyfit(x, y, deg)
        poly = np.poly1d(coeff)
        return poly

    def generate_speeds_BEP(self, speeds: list):
        """generates BEPs for various speeds. Argument should be a list of speeds, if a single speed is preferred, this
        can be passed as an int which is automatically mapped to a single element list.

        Args:
            speeds (list) : list of speeds to create BEPs for.

        Returns:
            dict: dictionary holding all the speed BEP data with structure: {speed: (BEP flow, BEP head)}
        """
        if (isinstance(speeds, int)) or (
            isinstance(speeds, float)
        ):  # allows single speed plotting
            speeds = [speeds]
        BEP_speeds_dict = {}
        _, BEP_flow, BEP_head = self.BEP()
        for speed in speeds:
            flow_multiplier, head_multiplier = self.affinity_ratio(speed)
            BEP_flow_speed = BEP_flow * flow_multiplier
            BEP_head_speed = BEP_head * head_multiplier
            _temp_dict = {speed: (BEP_flow_speed, BEP_head_speed)}
            BEP_speeds_dict.update(_temp_dict)
        return BEP_speeds_dict

    def generate_speeds_POR(self, speeds: list):
        """generate PORs for various speeds. If a single speed is preferred this can be passed as an int which is automatically
        mapped to a single element list.

        Args:
            speeds (list): list of speeds for POR points to be created for.

        Returns:
            dict: dictionary of speeds with corresponding POR data points. Structure:
            {Speed: (POR Flow - Upper, POR head - Upper, POR Flow - Lower, POR head - Lower)}
        """

        if (isinstance(speeds, int)) or (
            isinstance(speeds, float)
        ):  # allows single speed plotting
            speeds = [speeds]
        POR_speeds_dict = {}
        POR_dict = self.POR()
        for speed in speeds:
            flow_multiplier, head_multiplier = self.affinity_ratio(speed)
            POR_flow_speed_upper = POR_dict["Upper Flow"] * flow_multiplier
            POR_head_speed_upper = POR_dict["Upper Head"] * head_multiplier
            POR_flow_speed_lower = POR_dict["Lower Flow"] * flow_multiplier
            POR_head_speed_lower = POR_dict["Lower Head"] * head_multiplier
            _temp_dict = {
                speed: (
                    POR_flow_speed_upper,
                    POR_head_speed_upper,
                    POR_flow_speed_lower,
                    POR_head_speed_lower,
                )
            }
            POR_speeds_dict.update(_temp_dict)
        return POR_speeds_dict

    def affinity_ratio(self, speed: int):
        """Uses affinity laws to create flow and head multipliers for a given speed.

        Args:
            speed (int): new speed the ratio is to be calculated for

        Returns:
            flow_multiplier, head_multiplier (int, int): multipliers for flow and head
        """
        flow_multiplier = speed / 100
        head_multiplier = (speed / 100) ** 2
        return flow_multiplier, head_multiplier

    def BEP_at_speed(self, speed, print_string=False):
        best_efficiency, BEP_flow_100, BEP_head_100 = self.BEP()
        flow_multiplier, head_multiplier = self.affinity_ratio(speed)
        BEP_flow_speed = BEP_flow_100 * flow_multiplier
        BEP_head_speed = BEP_head_100 * head_multiplier
        if print_string:
            print(
                f"""The best efficiency at {speed}% speed is {round(best_efficiency,2)}, occuring at {round(BEP_flow_speed,2)} L/s and {round(BEP_head_speed,2)} m"""
            )
        return best_efficiency, BEP_flow_speed, BEP_head_speed

    #####-----------Plotting Functions------------######

    def generate_plot(self, BEP=False, POR=False):
        """Plots the 100% speed pump curve, with optional best efficiency and preferred
        operating point markers

        Args:
            BEP (bool, optional): Plot best efficiency point. Defaults to False.
            POR (bool, optional): Plot preferred operating range. Defaults to False.

        Returns:
            matplotlib ax object: plot of the 100% pump curve
        """
        self.fig, self.ax1 = plt.subplots()
        self.ax1.plot(self.flow, self.head, label="100%")
        self.ax1.set_xlabel("Flow (L/s)")
        self.ax1.set_ylabel("Head (m)")
        self.ax1.set_title(f"Pump Curve for {self.fullname()}")
        if BEP:
            _, BEP_flow, BEP_head = self.BEP()
            self.ax1.plot(BEP_flow, BEP_head, marker="o", label="BEP")
        if POR:
            POR_dict = self.POR()
            self.ax1.plot(
                POR_dict["Upper Flow"],
                POR_dict["Upper Head"],
                marker="x",
                color="r",
                label="POR",
            )
            self.ax1.plot(
                POR_dict["Lower Flow"], POR_dict["Lower Head"], marker="x", color="r"
            )
        return self

    def add_npshr(self):
        """adds an npshr plot to the plot object.
        This method requires the generate_plot method is called first.
        Also requires that some npshr data has been assigned to the pump object

        Raises:
            AttributeError: Raises error if no NPSHr data has been assigned to the pump object

        Returns:
            NPSHr plot on ax figure.
        """
        if not hasattr(self, "npshr_flow"):
            raise AttributeError(
                "Error: Please attribute NPSHr data with this pump object before attempting to plot NPSHr"
            )
        elif not hasattr(self, "ax1"):
            raise AttributeError(
                "Error: Please call generate_plot method before adding an NPSHr plot"
            )
        else:
            self.ax1.plot(
                self.npshr_flow,
                self.npshr,
                linestyle="-.",
                color="coral",
                label="NPSHr",
            )
            return self

    def add_efficiency(self):
        """Plots pump efficiency on a secondary y axis

        Returns:
            matplotlib ax figure
        """
        self.ax2 = self.ax1.twinx()
        self.ax2.plot(
            self.efficiency_flow,
            self.efficiency,
            linestyle="--",
            color="b",
            label="Efficiency (%)",
        )
        self.ax2.set_ylabel("Efficiency (%)")
        return self

    def plot_speeds(self, speeds=None, BEP=False, POR=False):
        """plots various speed curves.
        If no speeds are passed the method plots "typical" speeds (90,80,70,60,50)%.

        Args:
            speeds (bool, optional): If None, typical speeds are plotted. Custom speeds
            should be passed as a list.

            BEP (Bool, optional): If True, BEP points are plotted for the given speeds. Defaults to False.
            POR (Bool|Str, optional): Plotting method for POR. Accepts True, False, "marker", "line", or "fill".
                                        If True - Markers are plotted.
                                        If False - No POR is plotted.
                                        Defaults to False.

        Returns:
            matplotlib ax: ax object with new speed curves added
        """
        plot_params_dict = {
            "_marker": "x" if (POR == "marker") or (POR == True) else "None",
            "_linestyle": "dashed" if POR == "line" else "None",
            "_fill": True if POR == "fill" else False,
        }

        if speeds is None:
            speed_dict = self.generate_speed_curves()
        else:
            speed_dict = self.generate_speed_curves(speeds)
        for key, value in speed_dict.items():
            self.ax1.plot(
                value[0], value[1], label=str(key) + "%", alpha=0.2, color="tab:blue"
            )
        if BEP:
            if speeds is None:
                BEP_dict = self.generate_speeds_BEP(speeds=self.default_speeds)
            else:
                BEP_dict = self.generate_speeds_BEP(speeds)
            for key, value in BEP_dict.items():
                self.ax1.plot(value[0], value[1], marker="o", color="orange")
        if POR:
            if speeds is None:
                POR_dict = self.generate_speeds_POR(speeds=self.default_speeds)
            else:
                POR_dict = self.generate_speeds_POR(speeds=speeds)

            # grabbing the 100% POR points. Reqd to make the line meet the 100% speed curve
            upper_flows = [self.POR()["Upper Flow"]]
            upper_heads = [self.POR()["Upper Head"]]
            lower_flows = [self.POR()["Lower Flow"]]
            lower_heads = [self.POR()["Lower Head"]]
            # grabbing POR points for other speeds
            for key, value in POR_dict.items():
                upper_flows.append(value[0])
                upper_heads.append(value[1])
                lower_flows.append(value[2])
                lower_heads.append(value[3])

            if POR == "fill":
                self.ax1.fill(
                    np.append(upper_flows, lower_flows[::-1]),
                    np.append(upper_heads, lower_heads[::-1]),
                    color="red",
                    alpha=0.2,
                    linewidth=0,
                )
                # Filling gap between POR curve and 100% speed curve
                # Getting the ranges of the POR flow and creating a linear array
                POR_flows = np.linspace(
                    self.POR()["Upper Flow"], self.POR()["Lower Flow"], 50
                )
                # Getting the ranges of the POR head and creating a linear array
                POR_heads = np.linspace(
                    self.POR()["Upper Head"], self.POR()["Lower Head"], 50
                )
                pump_curve_coeffs = self.generate_curve_equation(self.flow, self.head)
                pump_flows = pump_curve_coeffs(POR_flows)
                self.ax1.fill_between(
                    x=POR_flows,
                    y1=POR_heads,
                    y2=pump_flows,
                    color="red",
                    alpha=0.2,
                    linewidth=0,
                )
                return self

            self.ax1.plot(
                upper_flows,
                upper_heads,
                marker=plot_params_dict["_marker"],
                linestyle=plot_params_dict["_linestyle"],
                color="red",
            )
            self.ax1.plot(
                lower_flows,
                lower_heads,
                marker=plot_params_dict["_marker"],
                linestyle=plot_params_dict["_linestyle"],
                color="red",
            )
        return self

    def add_duty(self, duty_flow, duty_head, line=False):
        """add a marker or line for a given duty point.

        Args:
            duty_flow (float or int): flow at duty point
            duty_head (float or int): head at duty point
            line (bool): if True, plots a line at the duty flow instead of a marker. Defaults to False.

        Returns:
            matplotlib axes object: plot with duty point added
        """
        if line:
            self.ax1.vlines(
                duty_flow,
                ymax=max(self.head),
                ymin=0,
                linestyles="dotted",
                colors="forestgreen",
                label="Duty",
            )
            return self
        self.ax1.plot(
            duty_flow,
            duty_head,
            marker="+",
            color="forestgreen",
            label="Duty Point",
            linestyle="None",
        )
        return self

    def get_legends(self):
        """gathering all the legend labels from all plots into one legend object

        Returns:
            matplotlib fig legend object: single legend object for all ax labels
        """
        lines_labels = [ax.get_legend_handles_labels() for ax in self.fig.axes]
        lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
        return self.fig.legend(
            lines,
            labels,
            bbox_to_anchor=(1, 0),
            loc="lower right",
            bbox_transform=self.fig.transFigure,
        )

    def show_plot(self, grid=True, save=False, save_dir: str = None):
        self.fig.tight_layout()
        self.get_legends()
        if grid:
            self.ax1.grid(linestyle="dotted", alpha=0.35, color="grey")
        plt.show()

        now = datetime.now()
        now = now.strftime("%d_%m_%Y__%H_%M_%S")
        filename = Path(f"Output Plot_{now}.png")  # saving with date and time appended

        if save:
            if save_dir is None:
                save_dir = Path.cwd()
            self.fig.savefig(fname=Path(save_dir / filename), format="png")
            print(f"Image saved as {filename} at {save_dir}")


class SystemCurve:
    def __init__(self, name, flow, head):
        self.name = name
        self.flow = flow
        self.head = head
