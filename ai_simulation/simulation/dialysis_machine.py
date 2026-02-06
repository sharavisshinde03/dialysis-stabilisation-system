class DialysisMachine:
    def __init__(self):
        self.blood_flow = 300
        self.arterial_pressure = 120
        self.venous_pressure = 80
        self.treatment_seconds = 2 * 60 * 60  # 2 hours
        self.stabilisation_mode = False

    def update(self):
        if self.treatment_seconds > 0:
            self.treatment_seconds -= 1

        if self.stabilisation_mode:
            self.blood_flow = max(180, self.blood_flow - 5)
            self.arterial_pressure = 180
            self.venous_pressure = 160
        else:
            self.blood_flow = 300
            self.arterial_pressure = 120
            self.venous_pressure = 80

    def activate_stabilisation(self):
        self.stabilisation_mode = True

    def formatted_time(self):
        h = self.treatment_seconds // 3600
        m = (self.treatment_seconds % 3600) // 60
        s = self.treatment_seconds % 60
        return f"{h:02}:{m:02}:{s:02}"
