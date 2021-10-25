import numpy as np
import matplotlib.pyplot as plt


class Pump:

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

    def BEP(self, speed=100):
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
        ratio = new_speed / 100  # assumes original pump curve is at 100% speed
        reduced_flow = [flow * ratio for flow in self.flow]
        reduced_head = [head * ratio ** 2 for head in self.head]

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
        _speeds = [90, 80, 70, 60, 50]  # typical % speeds
        if speeds is not None:
            _speeds = speeds
        speed_curve_dict = {}  # empty dict to hold our speed data.
        for speed in _speeds:
            flow, head = self.generate_affinity(new_speed=speed)
            _temp_dict = {speed: (flow, head)}
            speed_curve_dict.update(_temp_dict)
        return speed_curve_dict

    def POR(self, speed=100):
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

        return POR_upper_flow, POR_upper_head, POR_lower_flow, POR_lower_head

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

    #####-----------Plotting Functions------------######

    def generate_plot(self, BEP=False, POR=False):
        fig, self.ax1 = plt.subplots()
        self.ax1.plot(self.flow, self.head, label="100%")
        self.ax1.set_xlabel("Flow (L/s)")
        self.ax1.set_ylabel("Head (m)")
        self.ax1.set_title(f"Pump Curve for {self.fullname()}")
        if BEP:
            _, BEP_flow, BEP_head = self.BEP()
            self.ax1.plot(BEP_flow, BEP_head, marker="o", label="BEP")
        if POR:
            POR_upper_flow, POR_upper_head, POR_lower_flow, POR_lower_head = self.POR()
            self.ax1.plot(
                POR_upper_flow, POR_upper_head, marker="x", color="r", label="POR"
            )
            self.ax1.plot(POR_lower_flow, POR_lower_head, marker="x", color="r")
        self.ax1.legend()
        return self

    def add_npshr(self):
        if hasattr(self, "npshr_flow"):
            self.ax1.plot(
                self.npshr_flow, self.npshr, linestyle="-.", color="g", label="NPSHr"
            )
            self.ax1.legend()
            return self
        else:
            raise AttributeError(
                "Error: Please add NPSHr data to the object before attempting to plot NPSHr"
            )

    def show_plot(self):
        plt.show()
