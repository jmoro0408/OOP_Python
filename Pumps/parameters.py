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
            efficiency_flow (list, optional): Flow corrsponding to efficiency values. Defaults to None.
        """
        self.efficiency = efficiency
        self.efficiency_flow = self.flow
        if efficiency_flow is not None:
            self.efficiency_flow = efficiency_flow

    def BEP(self):
        """return the best efficiency point for a given pump

        Returns:
            tuple: BEP of the pump in (flow, head)
        """
        _max_efficiency_index = self.efficiency.index(max(self.efficiency))
        best_efficiency_point = (self.flow[_max_efficiency_index], max(self.efficiency))
        print(
            f"The BEP is {round(max(self.efficiency),2)}%, occuring at {round(self.flow[_max_efficiency_index],2)} L/s"
        )

        return best_efficiency_point
