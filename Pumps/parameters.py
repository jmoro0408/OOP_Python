class Pump:
    def __init__(self, make, model, speed):
        self.make = make
        self.model = model
        self.speed = speed

    def __repr__(self):
        return f"{self.make}, {self.model}, {self.speed}"

    def fullname(self):
        """Return the pump make and model

        Returns:
            str: make and model of pump
        """
        return self.make + " " + self.model

    # def define_pumpcurve(self, flow_head_dict: dict):


N3312 = Pump("Xylem", "N3312", 100)

print(N3312.fullname())
