class DialysisMachine:
    def __init__(self):
        self.blood_flow = 300
        self.arterial_pressure = 120
        self.venous_pressure = 80
        self.treatment_time = 120
        self.stabilisation_mode = False

    def update(self):
        if self.treatment_time > 0:
            self.treatment_time -= 1

        if self.stabilisation_mode:
            self.blood_flow = 200
            self.arterial_pressure = 100
            self.venous_pressure = 70
        else:
            self.blood_flow = 300
            self.arterial_pressure = 120
            self.venous_pressure = 80

    def activate_stabilisation(self):
        self.stabilisation_mode = True
